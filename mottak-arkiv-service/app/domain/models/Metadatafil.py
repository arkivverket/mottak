from datetime import datetime
from enum import Enum

from app.domain.xmlparser import create_arkivuttrekk_from_parsed_innhold
from app.domain.models.Arkivuttrekk import Arkivuttrekk


class MetadataType(str, Enum):
    XML_METS = 'xml/mets'


class Metadatafil:
    """
    Domain class to contain a Metadatafil while it exists in the service layer
    """
    id: int
    filnavn: str
    type = MetadataType
    innhold = str
    opprettet: datetime

    def __init__(self,
                 id_=None,
                 filnavn=None,
                 type_=None,
                 innhold=None,
                 opprettet=None):
        self.id = id_
        self.filnavn = filnavn
        self.type = type_
        self.innhold = innhold
        self.opprettet = opprettet

    def as_arkivuttrekk(self) -> Arkivuttrekk:
        return create_arkivuttrekk_from_parsed_innhold(self.id, self.innhold)
