import re

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.repository import arkivuttrekk_get_by_id, arkivuttrekk_get_all, metadatafil_create
from app.services.domain.metadatafil import Metadatafil


def get_file_content(file: UploadFile):
    """"
    Method that extract the XML from the content of the file,
    the xml may be prettyprinted XML, which can be difficult to deal with,
    we therfore turn prettyprinted XMLs into a spaceless string version
    before returning the string.
    """
    # If other content_types than XML are added,
    # include parameter content_type and extract the file content accordingly
    prettyprinted_xmlstring = file.file.read().decode('utf-8')
    spaceless_xmlstring = re.sub('\s+(?=<)', '', prettyprinted_xmlstring)
    return spaceless_xmlstring


def metadatafil_mapper(file: UploadFile) -> Metadatafil:
    """
    Method that map an UploadFile file to a Metadatafil domain object.
    """
    return Metadatafil(file.filename, file.content_type, get_file_content(file))


def post_upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_arkivuttrekk_get_by_id(arkivuttrekk_id: int, db: Session):
    return arkivuttrekk_get_by_id(db, arkivuttrekk_id)


def get_arkivuttrekk_get_all(db: Session, skip: int, limit: int):
    return arkivuttrekk_get_all(db, skip, limit)
