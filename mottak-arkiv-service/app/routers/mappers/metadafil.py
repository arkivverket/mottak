import re

from fastapi import UploadFile

from app.domain.models.Metadatafil import MetadataType, Metadatafil
from app.exceptions import InvalidContentType
from app.routers.dto.Metadata import Metadata


def _content_type2metadata_type(content_type: str) -> MetadataType:
    """
    Method that converts the field "content_type" in FastAPI's UploadFile object
    to a MetadataType Enum value.
    """
    # FastAPI's UploadFile returns 'text/xml' as content type.
    # Consider parsing the XML for the METS value instead.
    if content_type == 'text/xml':
        return MetadataType.XML_METS
    else:
        raise InvalidContentType(content_type)


def _get_file_content(file: UploadFile) -> str:
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
                       type_=_content_type2metadata_type(file.content_type),
                       innhold=_get_file_content(file))


def to_metadata(metadatafil: Metadatafil) -> Metadata:
    parsed_metadatafil = metadatafil.as_metadata()
    return Metadata.from_domain(parsed_metadatafil)
