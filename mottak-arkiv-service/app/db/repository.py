from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.schemas.mottak import Arkivuttrekk


def get_all_arkivuttrekk(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Arkivuttrekk) \
        .order_by(desc(Arkivuttrekk.opprettet)).offset(skip).limit(limit).all()

