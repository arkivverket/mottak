from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivuttrekk as Arkivuttrekk_DBO, Metadatafil as Metadatafil_DBO
from app.domain.models.Metadatafil import Metadatafil


def metadatafil_create(db: Session, metadatfil: Metadatafil) -> Metadatafil_DBO:
    dbo = Metadatafil_DBO(**vars(metadatfil))
    db.add(dbo)
    db.commit()
    return dbo


def metadatafil_get_by_id(db: Session, id_: int) -> Metadatafil_DBO:
    return db.query(Metadatafil_DBO).get(id_)


def arkivuttrekk_get_all(db: Session, skip: int, limit: int) -> List[Arkivuttrekk_DBO]:
    return db.query(Arkivuttrekk_DBO).order_by(desc(Arkivuttrekk_DBO.endret)).offset(skip).limit(limit).all()


def arkivuttrekk_get_by_id(db: Session, id_: int) -> Arkivuttrekk_DBO:
    return db.query(Arkivuttrekk_DBO).get(id_)
