import logging
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.connectors.azure_servicebus.azure_servicebus_client import AzureServicebus
from app.connectors.connectors_variables import REQUEST_SENDER_QUEUE_NAME, get_sas_generator_host, get_sender_con_str
from app.connectors.mailgun.mailgun_client import MailgunClient
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.connectors.sas_generator.models import SASResponse
from app.database.dbo.mottak import Invitasjon, Arkivuttrekk as Arkivuttrekk_DBO
from app.database.repositories import arkivuttrekk_repository, invitasjon_repository
from app.domain.models.Arkivuttrekk import Arkivuttrekk
from app.domain.models.Arkivkopi import ArkivkopiRequest
from app.domain.models.Invitasjon import InvitasjonStatus
from app.exceptions import ArkivuttrekkNotFound


def create(arkivuttrekk: Arkivuttrekk, db: Session):
    return arkivuttrekk_repository.create(db, arkivuttrekk)


def get_by_id(arkivuttrekk_id: int, db: Session):
    result = arkivuttrekk_repository.get_by_id(db, arkivuttrekk_id)
    if not result:
        raise ArkivuttrekkNotFound(arkivuttrekk_id)
    return result


def get_all(db: Session, skip: int, limit: int):
    return arkivuttrekk_repository.get_all(db, skip, limit)


async def create_invitasjon(arkivuttrekk_id: int, db: Session, mailgun_client: MailgunClient) -> Optional[Invitasjon]:
    arkivuttrekk = get_by_id(arkivuttrekk_id, db)
    return await _send_invitasjon(arkivuttrekk, db, mailgun_client)


async def _send_invitasjon(arkivuttrekk: Arkivuttrekk_DBO, db: Session, mailgun_client: MailgunClient):
    invitasjon_ekstern_id = uuid.uuid4()
    resp = await mailgun_client.send_invitasjon([arkivuttrekk.avgiver_epost], arkivuttrekk.obj_id,
                                                invitasjon_ekstern_id)

    if resp.status_code == 200:
        status = InvitasjonStatus.SENDT
    else:
        logging.warning(f"Invitasjon feilet for arkivuttrekk {arkivuttrekk.id} med {resp.status_code} {resp.text}")
        status = InvitasjonStatus.FEILET

    return invitasjon_repository.create(db, arkivuttrekk.id, arkivuttrekk.avgiver_epost, status, invitasjon_ekstern_id)


async def request_download(arkivuttrekk_id: int, db: Session):
    arkivuttrekk = get_by_id(arkivuttrekk_id, db)
    sas_token = await _request_sas_token(arkivuttrekk)
    if not sas_token:
        return {"status": 500}

    request_download = await _request_download(sas_token, arkivuttrekk)
    if not request_download:
        return {"status": 500}

    return {"status": 200}


async def _request_sas_token(arkivuttrekk: Arkivuttrekk_DBO):
    # ObjectID of the Arkivutrekk is name of the container
    sas_generator_client = SASGeneratorClient(get_sas_generator_host())
    return await sas_generator_client.request_sas(arkivuttrekk.obj_id)


async def _request_download(sas_token: SASResponse, arkivuttrekk: Arkivuttrekk_DBO):
    arkivkopi_request = ArkivkopiRequest(arkivkopi_id=arkivuttrekk.id,
                                         storage_account=sas_token["storage_account"],
                                         container=sas_token["container"],
                                         sas_token=sas_token["sas_token"])

    service_bus = AzureServicebus(get_sender_con_str(), REQUEST_SENDER_QUEUE_NAME)
    return await service_bus.send_message(arkivkopi_request.as_json_str())
