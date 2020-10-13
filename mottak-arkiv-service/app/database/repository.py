from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivuttrekk as Arkivuttrekk_DBO, Metadatafil as Metadatafil_DBO
from app.services.domain.metadatafil import Metadatafil


def metadatafil_create(db: Session, metadatfil: Metadatafil) -> Metadatafil_DBO:
    dbo = Metadatafil_DBO(**vars(metadatfil))
    db.add(dbo)
    db.commit()
    return dbo


def arkivuttrekk_get_all(db: Session, skip: int, limit: int) -> List[Arkivuttrekk_DBO]:
    return db.query(Arkivuttrekk_DBO).order_by(desc(Arkivuttrekk_DBO.endret)).offset(skip).limit(limit).all()


def arkivuttrekk_get_by_id(db: Session, arkivuttrekk_id: int) -> Arkivuttrekk_DBO:
    return db.query(Arkivuttrekk_DBO).get(arkivuttrekk_id)
