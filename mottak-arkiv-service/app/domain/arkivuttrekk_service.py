import logging
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.connectors.mailgun.mailgun_client import MailgunClient
from app.database.dbo.mottak import Invitasjon, Arkivuttrekk as Arkivuttrekk_DBO
from app.database.repositories import arkivuttrekk_repository, invitasjon_repository
from app.domain.models.Arkivuttrekk import Arkivuttrekk
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
        # TODO Update status of arkivuttrekk and save it to database when MOL-122 is done. Create invitasjon in domain models?
        return invitasjon_repository.create(db, arkivuttrekk.id, arkivuttrekk.avgiver_epost, InvitasjonStatus.SENT,
                                            invitasjon_ekstern_id)
    else:
        logging.warning(f"Invitasjon feilet for arkivuttrekk {arkivuttrekk.id} med {resp.status_code} {resp.text}")
        return invitasjon_repository.create(db, arkivuttrekk.id, arkivuttrekk.avgiver_epost, InvitasjonStatus.FEILET,
                                            invitasjon_ekstern_id)
