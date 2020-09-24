from typing import List
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.schemas import mottak
from app.dto.Arkivuttrekk import ArkivuttrekkOut


def get_arkivuttrekk(db: Session, obj_id: UUID):
    return db.query(mottak.Arkivuttrekk).filter(mottak.Arkivuttrekk.obj_id == obj_id).first()


def get_all_arkivuttrekk(db: Session, skip: int = 0, limit: int = 10) -> List[ArkivuttrekkOut]:
    return db.query(mottak.Arkivuttrekk) \
        .order_by(desc(mottak.Arkivuttrekk.opprettet)).offset(skip).limit(limit).all()
