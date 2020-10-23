import logging
from sqlalchemy.orm import Session
from typing import Optional

from app.database.repository import arkivuttrekk_get_by_id, arkivuttrekk_get_all, invitasjon_create
from app.database.dbo.mottak import Invitasjon
from app.connectors.mailgun_client import MailgunClient
from app.domain.models.Invitasjon import InvitasjonStatus



def get_by_id(arkivuttrekk_id: int, db: Session):
    return arkivuttrekk_get_by_id(db, arkivuttrekk_id)


def get_all(db: Session, skip: int, limit: int):
    return arkivuttrekk_get_all(db, skip, limit)


async def create_invitasjon(arkivuttrekk_id: int, db: Session, mailgun_client: MailgunClient) -> Optional[Invitasjon]:
    arkivuttrekk = arkivuttrekk_get_by_id(db, arkivuttrekk_id)
    if not arkivuttrekk:
        return None
    resp = await mailgun_client.send_invitaion([arkivuttrekk.avgiver_epost], 3)
    if resp.status_code == 200:
        return invitasjon_create(db, arkivuttrekk_id, InvitasjonStatus.SENT)
    else:
        logging.warning(f"Invitasjon feilet for arkivuttrekk {arkivuttrekk_id} med {resp.status_code} {resp.text}")
        return invitasjon_create(db, arkivuttrekk_id, InvitasjonStatus.FEILET)
