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
    opprettet: str
    endret: str

    def __init__(self,
                 id=None,
                 filnavn=None,
                 type=None,
                 innhold=None,
                 opprettet=None,
                 endret=None):
        self.id = id
        self.filnavn = filnavn
        self.type = type
        self.innhold = innhold
        self.opprettet = opprettet
        self.endret = endret


class ParsedMetadatafil:
    """
    Domain class used to store information parsed from the Metadatafil.innhold document
    """
    tittel: str
    endret: str
    kontaktperson: str
    arkivtype: str
    objekt_id: str
    storrelse: str
    tidsspenn: str
    saksnummer: str

    def __init__(self,
                 tittel=None,
                 endret=None,
                 kontaktperson=None,
                 arkivtype=None,
                 objekt_id=None,
                 storrelse=None,
                 tidsspenn=None,
                 saksnummer=None):
        self.tittel = tittel
        self.endret = endret
        self.kontaktperson = kontaktperson
        self.arkivtype = arkivtype
        self.objekt_id = objekt_id
        self.storrelse = storrelse
        self.tidsspenn = tidsspenn
        self.saksnummer = saksnummer
