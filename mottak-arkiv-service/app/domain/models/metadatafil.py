from enum import Enum


class MetadataType(str, Enum):
    XML_METS = 'xml/mets'


def content_type2metadata_type(content_type):
    # FastAPI's UploadFile returns 'text/xml' as content type.
    # Consider parsing the XML for the METS value instead.
    if content_type == 'text/xml':
        return MetadataType.XML_METS
    else:
        raise ValueError(f"Content type {content_type} is not a valid type")


class Metadatafil:
    """
    Domain class to contain a Metadatafil while it exists in the service layer
    """
    id: int
    arkivuttrekk_id: int
    filnavn: str
    type = MetadataType
    innhold = str
    opprettet: str

    def __init__(self, filnavn: str, content_type: str, innhold: str):
        self.id = None
        self.arkivuttrekk_id = None
        self.filnavn = filnavn
        self.type = content_type2metadata_type(content_type)
        self.innhold = innhold
        self.opprettet = None
