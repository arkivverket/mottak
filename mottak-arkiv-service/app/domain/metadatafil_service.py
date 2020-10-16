from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.mappers.metadatafil import map_dbo2model
from app.database.repository import metadatafil_create, metadatafil_get_by_id
from app.routers.mappers.metadafil import metadatafil_mapper
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_content(id_: int, db: Session) -> str:
    dbo = metadatafil_get_by_id(db, id_)
    return dbo.innhold if dbo else None


def get_parsed_content(id_: int, db: Session) -> ArkivuttrekkBase:
    """
    Method that retrieves an Metadatafil database object by the input id_
    and parses its content for values used when initializing an object of type ArkivuttrekkBase.
    """
    metadatafil_dbo = metadatafil_get_by_id(db, id_)
    if not metadatafil_dbo:
        return None
    else:
        metadatafil = map_dbo2model(metadatafil_dbo)
        return metadatafil.as_arkivuttrekk_base()
