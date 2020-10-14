from sqlalchemy.orm import Session

from app.database.repository import arkivuttrekk_get_by_id, arkivuttrekk_get_all, arkivuttrekk_create
from routers.dto.Arkivuttrekk import ArkivuttrekkBase


def create(arkivuttrekk: ArkivuttrekkBase, db: Session):
    return arkivuttrekk_create(db, arkivuttrekk)


def get_by_id(arkivuttrekk_id: int, db: Session):
    return arkivuttrekk_get_by_id(db, arkivuttrekk_id)


def get_all(db: Session, skip: int, limit: int):
    return arkivuttrekk_get_all(db, skip, limit)
