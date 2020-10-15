from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.mappers.metadatafil import map_dbo2model
from app.database.repository import metadatafil_create, metadatafil_get_by_id
from app.domain.models.metadatafil import ParsedMetadatafil
from app.domain.xmlparser import get_parsedmetadatafil
from app.routers.mappers.metadafil import metadatafil_mapper, map_parsed_domain2dto
from app.exceptions import MetadatafilNotFound


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_dbo_by_id(db: Session, id: int):
    dbo = metadatafil_get_by_id(db, id)
    if not dbo:
        raise MetadatafilNotFound(id)
    return dbo


def get_content(id: int, db: Session) -> str:
    dbo = get_dbo_by_id(db, id)
    return dbo.innhold


def get_parsed_content(id: int, db: Session) -> ParsedMetadatafil:
    dbo = get_dbo_by_id(db, id)
    domain_model = map_dbo2model(dbo)
    domain_parsed = get_parsedmetadatafil(domain_model)
    return map_parsed_domain2dto(domain_parsed)
