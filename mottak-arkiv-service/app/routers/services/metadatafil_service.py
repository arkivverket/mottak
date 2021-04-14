from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.mappers.metadatafil import map_dbo2model
from app.database.repositories import metadatafil_repository
from app.exceptions import MetadatafilNotFound
from app.routers.dto.Metadatafil import Metadatafil
from app.routers.mappers.metadafil import metadatafil_mapper


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_repository.create(db, metadatafil)


def _get_dbo_by_id(db: Session, id_: int):
    dbo = metadatafil_repository.get_by_id(db, id_)
    if not dbo:
        raise MetadatafilNotFound(id_)
    return dbo


def get_content(id_: int, db: Session) -> str:
    dbo = _get_dbo_by_id(db, id_)
    return dbo.innhold


# TODO: Find good name for this method
# TODO: Update desc
def get_metadata(id_: int, db: Session) -> Metadatafil:
    """
    Method that retrieves an Metadatafil database object by the input id_
    and parses its content for values used when initializing an object of type ArkivuttrekkBase.
    """
    metadatafil_dbo = _get_dbo_by_id(db, id_)
    metadatafil = map_dbo2model(metadatafil_dbo)
    return metadatafil
