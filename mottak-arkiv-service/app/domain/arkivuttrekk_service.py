import logging
import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse
from app.connectors.arkiv_downloader.queues import ArchiveDownloadRequestSender
from app.connectors.mailgun.mailgun_client import MailgunClient
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.database.dbo.mottak import Arkivuttrekk as Arkivuttrekk_DBO, Arkivkopi as Arkivkopi_DBO
from app.database.repositories import arkivkopi_repository, arkivuttrekk_repository, invitasjon_repository, \
    overforingspakke_repository
from app.domain.models.Arkivkopi import Arkivkopi, ArkivkopiRequestParameters
from app.domain.models.Arkivuttrekk import Arkivuttrekk
from app.domain.models.Invitasjon import InvitasjonStatus, Invitasjon
from app.exceptions import ArkivuttrekkNotFound, ArkivkopiOfArchiveRequestFailed, \
    ArkivkopiOfOverforingspakkeRequestFailed, OverforingspakkeNotFound, SASTokenPreconditionFailed, InvitasjonNotFound, \
    ArkivkopiOfOverforingspakkeNotFound

ZERO_GENERATION = "0"
TAR_SUFFIX = ".tar"
FOLDER_SUFFIX = "/"

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
    resp = await mailgun_client.send_invitasjon([arkivuttrekk.avgiver_epost], arkivuttrekk.obj_id, arkivuttrekk.tittel,
                                                invitasjon_ekstern_id)

    if resp.status_code == 200:
        status = InvitasjonStatus.SENDT
    else:
        logger.warning(f"Invitasjon feilet for arkivuttrekk {arkivuttrekk.id} med {resp.status_code} {resp.text}")
        status = InvitasjonStatus.FEILET

    return invitasjon_repository.create(db, arkivuttrekk.id, arkivuttrekk.avgiver_epost, status, invitasjon_ekstern_id)


async def request_download_of_archive(arkivuttrekk_id: int, db: Session,
                                      archive_download_request_client: ArchiveDownloadRequestSender,
                                      sas_generator_client: SASGeneratorClient) -> Optional[Arkivkopi_DBO]:
    invitasjon = _get_invitasjon(arkivuttrekk_id, db)
    container_id = _get_container_id(invitasjon.ekstern_id)
    sas_token = await _generate_sas_token(container_id, sas_generator_client)

    target_name = _get_target_name(ekstern_id=invitasjon.ekstern_id, is_object=False)
    arkivkopi = arkivkopi_repository.create(db, Arkivkopi.create_from(invitasjon_id=invitasjon.id,
                                                                      sas_token=sas_token,
                                                                      target_name=target_name))

    parameters = ArkivkopiRequestParameters(arkivkopi_id=arkivkopi.id, sas_token=sas_token)
    request_sent = await archive_download_request_client.send_download_request(parameters)

    if not request_sent:
        arkivkopi_repository.delete(db, arkivkopi)
        raise ArkivkopiOfArchiveRequestFailed(arkivuttrekk_id, container_id)
    return arkivkopi


def _get_invitasjon(arkivuttrekk_id, db) -> Invitasjon:
    invitasjon_dbo = invitasjon_repository.get_by_arkivuttrekk_id_newest(db, arkivuttrekk_id)
    if not invitasjon_dbo:
        raise InvitasjonNotFound(arkivuttrekk_id)
    return Invitasjon(id_=invitasjon_dbo.id,
                      ekstern_id=invitasjon_dbo.ekstern_id,
                      arkivuttrekk_id=invitasjon_dbo.arkivuttrekk_id,
                      avgiver_epost=invitasjon_dbo.avgiver_epost,
                      status=invitasjon_dbo.status,
                      opprettet=invitasjon_dbo.opprettet)


def _get_container_id(ekstern_id: uuid.UUID) -> str:
    """
    Private function that returns the container_id associated with the given invitasjon.

    ____________________________________________________________________________________________________________________
    Documentation of container_id in the current implementation of mottak.

    In the current implementation we will assume that for every arkivuttrekk there is only one active invitasjon.
    It is assumed that the active invitasjon is the most recently created invitasjon.
    In other words, it is possible for an arkivuttrekk to have multiple associated invitasjons,
    but when requesting to download an arkivuttrekk to on-prem the most recently created invitasjon will be used.

    The container_id will be a string representation of the ekstern_id created in the method _send_invitation.
    The container_id will be used as the target_container_name when unpacking the tar-file to an azure container
    during the argo-workflow step s3-unpack.

    In other words, the end result of uploading an archive can be found in an azure container named container_id.
    ____________________________________________________________________________________________________________________
    """
    return str(ekstern_id)


async def _generate_sas_token(container_id, sas_generator_client):
    sas_token = await sas_generator_client.request_sas(container_id)
    if not sas_token:
        raise SASTokenPreconditionFailed(container_id)
    return sas_token


def _get_target_name(ekstern_id: uuid.UUID, is_object: bool) -> str:
    target_name = str(ekstern_id)
    if is_object:
        target_name = target_name + TAR_SUFFIX
    else:
        target_name = target_name + FOLDER_SUFFIX
    return target_name


def update_arkivkopi_status(arkivkopi: ArkivkopiStatusResponse, db: Session) -> Optional[Arkivkopi_DBO]:
    result = arkivkopi_repository.update_status(db, arkivkopi.arkivkopi_id, arkivkopi.status)
    if not result:
        msg = f"Could not find arkivkopi with id={arkivkopi.arkivkopi_id} for updating of status={arkivkopi.status}"
        logger.error(msg)
    return result


async def get_arkivkopi_status_of_archive(arkivuttrekk_id: int, db: Session) -> Optional[Arkivkopi_DBO]:
    invitasjon = _get_invitasjon(arkivuttrekk_id, db)
    results = arkivkopi_repository.get_all_by_invitasjon_id(db, invitasjon.id)
    if not results:
        raise ArkivkopiNotFound(invitasjon.id)
    arkivkopi_arkiv = [arkivkopi for arkivkopi in results if not arkivkopi.is_object]
    return arkivkopi_arkiv.pop() if arkivkopi_arkiv else None


async def request_download_of_overforingspakke(arkivuttrekk_id: int, db: Session,
                                               archive_download_request_client: ArchiveDownloadRequestSender,
                                               sas_generator_client: SASGeneratorClient,
                                               tusd_download_location_container: str) -> Optional[Arkivkopi_DBO]:
    invitasjon = _get_invitasjon(arkivuttrekk_id, db)
    container_id = tusd_download_location_container
    sas_token = await _generate_sas_token(container_id, sas_generator_client)

    target_name = _get_target_name(ekstern_id=invitasjon.ekstern_id, is_object=True)
    source_name = _get_source_name(invitasjon.id, db)
    arkivkopi = arkivkopi_repository.create(db, Arkivkopi.create_from(invitasjon_id=invitasjon.id,
                                                                      sas_token=sas_token,
                                                                      target_name=target_name,
                                                                      is_object=True))

    parameters = ArkivkopiRequestParameters(arkivkopi_id=arkivkopi.id, sas_token=sas_token,
                                            target_name=target_name, source_name=source_name)
    request_sent = await archive_download_request_client.send_download_request(parameters)

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
    return overforingspakke.tusd_objekt_navn


async def get_arkivkopi_status_of_overforingspakke(arkivuttrekk_id: int, db: Session) -> Arkivkopi_DBO:
    invitasjon = _get_invitasjon(arkivuttrekk_id, db)
    arkivkopi = arkivkopi_repository.get_overforingspakke_by_invitasjonId_newest(db, invitasjon.id)
    if not arkivkopi:
        raise ArkivkopiOfOverforingspakkeNotFound(invitasjon.id)
    return arkivkopi
