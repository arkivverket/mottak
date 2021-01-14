from sqlalchemy.orm import Session
from typing import Optional

from app.database.dbo.mottak import Arkivkopi as Arkivkopi_DBO
from app.domain.models.Arkivkopi import ArkivkopiStatus


def get_by_id(db: Session, id_: int) -> Arkivkopi_DBO:
    return db.query(Arkivkopi_DBO).get(id_)


def get_by_arkivuttrekk_id(db: Session, arkivuttrekk_id) -> Arkivkopi_DBO:
    return db.query(Arkivkopi_DBO).filter(Arkivkopi_DBO.arkivuttrekk_id == arkivuttrekk_id).first()


def update_status(db: Session, id_: int, status: ArkivkopiStatus) -> Optional[Arkivkopi_DBO]:
    arkivkopi = get_by_id(db, id_)
    arkivkopi.status = status
    db.commit()
    return arkivkopi
