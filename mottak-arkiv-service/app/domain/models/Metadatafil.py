from datetime import datetime
from enum import Enum


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
    endret: datetime

    def __init__(self,
                 id_=None,
                 filnavn=None,
                 type_=None,
                 innhold=None,
                 opprettet=None,
                 endret=None):
        self.id = id_
        self.filnavn = filnavn
        self.type = type_
        self.innhold = innhold
        self.opprettet = opprettet
        self.endret = endret
