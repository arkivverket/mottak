from typing import List

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivuttrekk as Arkivuttrekk_DBO
from app.domain.models.Arkivuttrekk import Arkivuttrekk


def create(db: Session, arkivuttrekk: Arkivuttrekk) -> Arkivuttrekk_DBO:
    dbo = Arkivuttrekk_DBO(**vars(arkivuttrekk))
    db.add(dbo)
    db.commit()
    return dbo


def get_all(db: Session, skip: int, limit: int) -> List[Arkivuttrekk_DBO]:
    return db.query(Arkivuttrekk_DBO).order_by(desc(Arkivuttrekk_DBO.endret)).offset(skip).limit(limit).all()


def get_count(db: Session) -> int:
    return db.query(func.count(Arkivuttrekk_DBO.id)).scalar()


def get_by_id(db: Session, id_: int) -> Arkivuttrekk_DBO:
    return db.query(Arkivuttrekk_DBO).get(id_)
