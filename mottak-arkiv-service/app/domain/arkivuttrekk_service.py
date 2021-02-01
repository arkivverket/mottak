import logging
import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse
from app.connectors.arkiv_downloader.queues import ArchiveDownloadRequestSender
from app.connectors.mailgun.mailgun_client import MailgunClient
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.database.dbo.mottak import Invitasjon, Arkivuttrekk as Arkivuttrekk_DBO, Arkivkopi as Arkivkopi_DBO
from app.database.repositories import arkivkopi_repository, arkivuttrekk_repository, invitasjon_repository
from app.domain.models.Arkivkopi import Arkivkopi
from app.domain.models.Arkivuttrekk import Arkivuttrekk
from app.domain.models.Invitasjon import InvitasjonStatus
from app.exceptions import ArkivuttrekkNotFound, ArkivkopiRequestFailed


def create(arkivuttrekk: Arkivuttrekk, db: Session) -> Arkivuttrekk_DBO:
    return arkivuttrekk_repository.create(db, arkivuttrekk)


def get_by_id(arkivuttrekk_id: int, db: Session) -> Arkivuttrekk_DBO:
    result = arkivuttrekk_repository.get_by_id(db, arkivuttrekk_id)
    if not result:
        raise ArkivuttrekkNotFound(arkivuttrekk_id)
    return result


def get_all(db: Session, skip: int, limit: int) -> List[Arkivuttrekk_DBO]:
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


async def request_download(arkivuttrekk_id: int, db: Session,
                           archive_download_request_client: ArchiveDownloadRequestSender,
                           sas_generator_client: SASGeneratorClient) -> Optional[Arkivkopi_DBO]:
    arkivuttrekk = get_by_id(arkivuttrekk_id, db)
    sas_token = await sas_generator_client.request_sas(arkivuttrekk.obj_id)
    if not sas_token:
        raise ArkivkopiRequestFailed(arkivuttrekk.obj_id)

    arkivkopi = arkivkopi_repository.create(db, Arkivkopi.from_id_and_token(arkivuttrekk_id, sas_token))

    request_sent = await archive_download_request_client.send_download_request(sas_token, arkivkopi.id)
    if not request_sent:
        arkivkopi_repository.delete(db, arkivkopi)
        raise ArkivkopiRequestFailed(arkivuttrekk.obj_id)

    return arkivkopi


def update_arkivkopi_status(arkivkopi: ArkivkopiStatusResponse, db: Session) -> Optional[Arkivkopi_DBO]:
    result = arkivkopi_repository.update_status(db, arkivkopi.arkivkopi_id, arkivkopi.status)
    if not result:
        msg = f"Could not find arkivkopi with id={arkivkopi.arkivkopi_id} for updating of status={arkivkopi.status}"
        logging.error(msg)
    return result


async def get_arkivkopi_status(arkivuttrekk_id: int, db: Session) -> Optional[Arkivkopi_DBO]:
    results = arkivkopi_repository.get_by_arkivuttrekk_id_newest(db, arkivuttrekk_id)
    if not results:
        raise ArkivuttrekkNotFound(arkivuttrekk_id)
    return results
