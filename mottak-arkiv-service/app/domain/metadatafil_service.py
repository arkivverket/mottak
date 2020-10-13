from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.repository import metadatafil_create, metadatafil_get_by_id
from routers.mappers.metadafil import metadatafil_mapper


def upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_content(id: int, db: Session) -> str:
    metadatafil = metadatafil_get_by_id(db, id)
    if not metadatafil:
        return None
    else:
        return metadatafil.innhold
