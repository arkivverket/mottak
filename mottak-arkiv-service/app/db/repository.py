from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.schemas.mottak import Arkivuttrekk, Metadatafil
from app.dto.Metadatafil import BaseMetadatafil


def get_arkivuttrekk(db: Session, arkivuttrekk_id: int):
    return db.query(Arkivuttrekk).get(arkivuttrekk_id)


def get_all_arkivuttrekk(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Arkivuttrekk) \
        .order_by(desc(Arkivuttrekk.opprettet)).offset(skip).limit(limit).all()


def create_metadatafil(db: Session, base_metadatafil: BaseMetadatafil) -> int:
    db_metadatafil = Metadatafil(**base_metadatafil.dict())
    db.add(db_metadatafil)
    db.commit()
    return db_metadatafil.id
