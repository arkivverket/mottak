from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.mappers.metadatafil import map_dbo2model
from app.database.repository import metadatafil_create, metadatafil_get_by_id
from app.domain.mappers.metadatafil import map_domain2dto_base
from app.domain.xmlparser import create_arkivuttrekk_from_parsed_content
from app.routers.mappers.metadafil import metadatafil_mapper
from app.domain.models.Arkivuttrekk import Arkivuttrekk


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_content(id_: int, db: Session) -> str:
    dbo = metadatafil_get_by_id(db, id_)
    return dbo.innhold if dbo else None


def get_parsed_content(id_: int, db: Session) -> Arkivuttrekk:
    """
    Method that retrieves an Metadatafil database object by the input id_
    and parses its content for values used when initializing an object of type ArkivuttrekkBase.
    """
    metadatafil_dbo = metadatafil_get_by_id(db, id_)
    if not metadatafil_dbo:
        return None
    else:
        metadatafil = map_dbo2model(metadatafil_dbo)
        arkivuttrekk = create_arkivuttrekk_from_parsed_content(metadatafil)
        return map_domain2dto_base(arkivuttrekk)
