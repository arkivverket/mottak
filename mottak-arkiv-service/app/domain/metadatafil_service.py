import re

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.repository import metadatafil_create, metadatafil_get_by_id
from app.domain.models.metadatafil import Metadatafil, MetadataType


def content_type2metadata_type(content_type):
    # FastAPI's UploadFile returns 'text/xml' as content type.
    # Consider parsing the XML for the METS value instead.
    if content_type == 'text/xml':
        return MetadataType.XML_METS
    else:
        raise ValueError(f"Content type {content_type} is not a valid type")


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
    spaceless_xmlstring = re.sub(r'\s+(?=<)', '', prettyprinted_xmlstring)
    return spaceless_xmlstring


def metadatafil_mapper(file: UploadFile) -> Metadatafil:
    """
    Method that map an UploadFile file to a Metadatafil domain object.
    """
    return Metadatafil(
        file.filename,
        content_type2metadata_type(file.content_type),
        get_file_content(file))


def post_upload_metadatafil(file: UploadFile, db: Session):
    metadatafil = metadatafil_mapper(file)
    return metadatafil_create(db, metadatafil)


def get_metadatafil_get_content(id: int, db: Session) -> str:
    metadatafil = metadatafil_get_by_id(db, id)
    return metadatafil.innhold
