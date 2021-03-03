import logging
import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse
from app.connectors.arkiv_downloader.queues import ArchiveDownloadRequestSender
from app.connectors.mailgun.mailgun_client import MailgunClient
from app.connectors.sas_generator.models import SASResponse
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.database.dbo.mottak import Invitasjon, Arkivuttrekk as Arkivuttrekk_DBO, Arkivkopi as Arkivkopi_DBO
from app.database.repositories import arkivkopi_repository, arkivuttrekk_repository, invitasjon_repository, \
    overforingspakke_repository
from app.domain.models.Arkivkopi import Arkivkopi
from app.domain.models.Arkivuttrekk import Arkivuttrekk
from app.domain.models.Invitasjon import InvitasjonStatus
from app.exceptions import ArkivuttrekkNotFound, ArkivkopiOfArchiveRequestFailed, \
    ArkivkopiOfOverforingspakkeRequestFailed, OverforingspakkeNotFound, SASTokenPreconditionFailed, InvitasjonNotFound

ZERO_GENERATION = "0"
OVERFORINGSPAKKE_CONTAINER = "tusd-storage"

logger = logging.getLogger(__name__)


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
        logger.warning(f"Invitasjon feilet for arkivuttrekk {arkivuttrekk.id} med {resp.status_code} {resp.text}")
        status = InvitasjonStatus.FEILET

    return invitasjon_repository.create(db, arkivuttrekk.id, arkivuttrekk.avgiver_epost, status, invitasjon_ekstern_id)


def _get_invitasjon_id(arkivuttrekk_id, db):
    invitasjon = invitasjon_repository.get_by_arkivuttrekk_id_newest(db, arkivuttrekk_id)
    if not invitasjon:
        raise InvitasjonNotFound(arkivuttrekk_id)
    return invitasjon.id

async def _generate_sas_token(container_id, sas_generator_client):
    sas_token = await sas_generator_client.request_sas(container_id)
    if not sas_token:
        raise SASTokenPreconditionFailed(container_id)
    return sas_token


async def request_download_of_archive(arkivuttrekk_id: int, db: Session,
                                      archive_download_request_client: ArchiveDownloadRequestSender,
                                      sas_generator_client: SASGeneratorClient) -> Optional[Arkivkopi_DBO]:
    invitasjon_id = _get_invitasjon_id(arkivuttrekk_id, db)
    container_id = await _get_container_id(invitasjon_id, db)
    sas_token = await _generate_sas_token(container_id, sas_generator_client)

    arkivkopi = _get_or_create_arkivkopi(arkivuttrekk_id, db, sas_token)

    request_sent = await archive_download_request_client.send_archive_download_request(sas_token, arkivkopi.id)

    if not request_sent:
        arkivkopi_repository.delete(db, arkivkopi)
        raise ArkivkopiOfArchiveRequestFailed(arkivuttrekk_id, container_id)
    return arkivkopi


def _get_container_id(invitasjons_id: int, db: Session) -> str:
    """
    Private function that returns the container_id associated with the given invitasjon.

    ____________________________________________________________________________________________________________________
    Documentation of container_id in the current implementation of mottak.

    In the current implementation we will assume that for every arkivuttrekk there is only one active invitasjon.
    It is assumed that the active invitasjon is the most recently created invitasjon.
    In other words, it is possible for an arkivuttrekk to have multiple associated invitasjons,
    but when requesting to download an arkivuttrekk to on-prem the most recently created invitasjon will be used.

    The container_id will be a string representation of the ekstern_id created in the method _send_invitation,
    and the generation of the archive, which for mottaksløsningen will always be the first (zero) generation.
    The container_id will be used as the target_container_name when unpacking the tar-file to an azure container
    during the argo-workflow step s3-unpack.

    In other words, the end result of uploading an archive can be found in an azure container named container_id.
    ____________________________________________________________________________________________________________________
    """
    invitasjon = invitasjon_repository.get_by_id(db, invitasjons_id)
    return f'{invitasjon.ekstern_id}-{ZERO_GENERATION}'


def update_arkivkopi_status(arkivkopi: ArkivkopiStatusResponse, db: Session) -> Optional[Arkivkopi_DBO]:
    result = arkivkopi_repository.update_status(db, arkivkopi.arkivkopi_id, arkivkopi.status)
    if not result:
        msg = f"Could not find arkivkopi with id={arkivkopi.arkivkopi_id} for updating of status={arkivkopi.status}"
        logger.error(msg)
    return result


async def get_arkivkopi_status(arkivuttrekk_id: int, db: Session) -> Optional[Arkivkopi_DBO]:
    results = arkivkopi_repository.get_by_arkivuttrekk_id_newest(db, arkivuttrekk_id)
    if not results:
        raise ArkivuttrekkNotFound(arkivuttrekk_id)
    return results


def _get_filnavn(arkivuttrekk_id: int, db: Session) -> str:
    arkivuttrekk = get_by_id(arkivuttrekk_id, db)
    filnavn = f"{arkivuttrekk.obj_id}.tar"
    return filnavn


def _get_source_name(arkivuttrekk_id: int, db: Session) -> str:
    overforingspakke = overforingspakke_repository.get_by_arkivuttrekk_id_newest(db, arkivuttrekk_id)
    if not overforingspakke:
        raise OverforingspakkeNotFound(arkivuttrekk_id)
    source_name = overforingspakke.tusd_objekt_navn
    return source_name


async def request_download_of_overforingspakke(arkivuttrekk_id: int, db: Session,
                                               archive_download_request_client: ArchiveDownloadRequestSender,
                                               sas_generator_client: SASGeneratorClient) -> Optional[Arkivkopi_DBO]:
    container_id = OVERFORINGSPAKKE_CONTAINER
    sas_token = await _generate_sas_token(container_id, sas_generator_client)

    filnavn = _get_filnavn(arkivuttrekk_id, db)
    arkivkopi = _get_or_create_arkivkopi(arkivuttrekk_id, db, sas_token, filnavn)

    source_name = _get_source_name(arkivuttrekk_id, db)
    request_sent = await archive_download_request_client.send_object_download_request(sas_token, arkivkopi.id,
                                                                                      filnavn, source_name)
    if not request_sent:
        arkivkopi_repository.delete(db, arkivkopi)
        raise ArkivkopiOfOverforingspakkeRequestFailed(arkivuttrekk_id, container_id)
    return arkivkopi


def _get_source_name(invitasjon_id: int, db: Session) -> str:
    """
    Returns the source name which is the name of the object stored in the tusd_container.
    """
    overforingspakke = overforingspakke_repository.get_by_invitasjon_id(db, invitasjon_id)
    if not overforingspakke:
        raise OverforingspakkeNotFound(invitasjon_id)
    source_name = overforingspakke.tusd_objekt_navn
    return source_name
