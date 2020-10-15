import re

from fastapi import UploadFile

from app.domain.models.metadatafil import MetadataType, Metadatafil, ParsedMetadatafil
from app.routers.dto.Metadatafil import ParsedMetadatafil as ParsedMetadatafil_DTO


def content_type2metadata_type(content_type: str):
    """
    Method that converts the field "content_type" in FastAPI's UploadFile object
    to a MetadataType Enum value.
    """
    # FastAPI's UploadFile returns 'text/xml' as content type.
    # Consider parsing the XML for the METS value instead.
    if content_type == 'text/xml':
        return MetadataType.XML_METS
    else:
        raise ValueError(f"Content type {content_type} is not a valid type")


def get_file_content(file: UploadFile):
    """
    Method that extract the XML from the content of the file,
    the xml may be prettyprinted XML, which can be difficult to deal with,
    we therefore turn prettyprinted XMLs into a spaceless string version
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
    return Metadatafil(filnavn=file.filename,
                       type=content_type2metadata_type(file.content_type),
                       innhold=get_file_content(file))
