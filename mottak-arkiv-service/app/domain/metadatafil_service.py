from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.repository import metadatafil_create, metadatafil_get_by_id
from database.mappers.metadatafil import map_dbo2model
from domain.models.metadatafil import ParsedMetadatafil
from domain.xmlparser import get_parsedmetadatafil
from routers.mappers.metadafil import metadatafil_mapper, map_parsed_domain2dto


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_content(id: int, db: Session) -> str:
    dbo = metadatafil_get_by_id(db, id)
    if not dbo:
        return None
    else:
        return dbo.innhold


def get_parsed_content(id: int, db: Session) -> ParsedMetadatafil:
    dbo = metadatafil_get_by_id(db, id)
    if not dbo:
        return None
    else:
        domain_model = map_dbo2model(dbo)
        domain_parsed = get_parsedmetadatafil(domain_model)
        return map_parsed_domain2dto(domain_parsed)
