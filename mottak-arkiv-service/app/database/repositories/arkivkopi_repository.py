from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivkopi as Arkivkopi_DBO
from app.domain.models.Arkivkopi import ArkivkopiStatus, Arkivkopi


def create(db: Session, arkivkopi: Arkivkopi) -> Arkivkopi_DBO:
    dbo = Arkivkopi_DBO(**vars(arkivkopi))
    db.add(dbo)
    db.commit()
    return dbo


def get_by_id(db: Session, id_: int) -> Arkivkopi_DBO:
    return db.query(Arkivkopi_DBO).get(id_)


def get_archive_by_invitasjonId_newest(db: Session, invitasjon_id: int) -> Optional[Arkivkopi_DBO]:
    return db.query(Arkivkopi_DBO)\
        .filter(Arkivkopi_DBO.invitasjon_id == invitasjon_id)\
        .filter(Arkivkopi_DBO.is_object == False)\
        .order_by(desc(Arkivkopi_DBO.endret))\
        .first()


def get_overforingspakke_by_invitasjonId_newest(db: Session, invitasjon_id: int) -> Optional[Arkivkopi_DBO]:
    return db.query(Arkivkopi_DBO)\
        .filter(Arkivkopi_DBO.invitasjon_id == invitasjon_id)\
        .filter(Arkivkopi_DBO.is_object == True)\
        .order_by(desc(Arkivkopi_DBO.endret))\
        .first()


def delete(db: Session, arkivkopi: Arkivkopi):
    db.delete(arkivkopi)
    db.commit()


def update_status(db: Session, id_: int, status: ArkivkopiStatus) -> Optional[Arkivkopi_DBO]:
    arkivkopi = get_by_id(db, id_)
    if not arkivkopi:
        return None
    arkivkopi.status = status
    db.commit()
    return arkivkopi
