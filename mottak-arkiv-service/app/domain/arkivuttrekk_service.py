from sqlalchemy.orm import Session

from app.database.repository import arkivuttrekk_get_by_id, arkivuttrekk_get_all, arkivuttrekk_create
from domain.metadatafil_service import get_content
from domain.xmlparser import get_checksum
from exceptions import ArkivuttrekkNotFound, MetadatafilMissingInnhold
from routers.dto.Arkivuttrekk import ArkivuttrekkBase


def get_missing_checksum(metadatafil_id: int, db: Session) -> str:
    """
    Method that checks if missing checksum can be found in the XML document of the metadatafil
    """
    innhold = get_content(metadatafil_id, db)
    if not innhold:
        raise MetadatafilMissingInnhold(metadatafil_id)
    return get_checksum(innhold)


def create(arkivuttrekk: ArkivuttrekkBase, db: Session):
    if arkivuttrekk.sjekksum_sha256 is None:
        arkivuttrekk.sjekksum_sha256 = get_missing_checksum(arkivuttrekk.metadatafil_id, db)
    return arkivuttrekk_create(db, arkivuttrekk)


def get_by_id(arkivuttrekk_id: int, db: Session):
    result = arkivuttrekk_get_by_id(db, arkivuttrekk_id)
    if not result:
        raise ArkivuttrekkNotFound(arkivuttrekk_id)
    return result


def get_all(db: Session, skip: int, limit: int):
    return arkivuttrekk_get_all(db, skip, limit)
