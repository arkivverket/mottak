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

    def __init__(self,
                 id: int = None,
                 filnavn: str = None,
                 type: str = None,
                 innhold: str = None,
                 opprettet: str = None):
        self.id = id
        self.filnavn = filnavn
        self.type = type
        self.innhold = innhold
        self.opprettet = opprettet


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

    def __init__(self):
        self.tittel = "Tittel  (ARCHIVIST - ORGANIZATION + LABEL)"
        self.endret = "Sist endret (tidspunkt for siste handling på pakken)"
        self.kontaktperson = "Kontaktperson (Navn (e-post) SUBMITTER - INDIVIDUAL)"
        self.arkivtype = "Arkivtype"
        self.objekt_id = "UUID"
        self.storrelse = "Størrelse (METS FILE ID SIZE)"
        self.tidsspenn = "(STARTDATE + ENDDATE)"
        self.saksnummer = "(SUBMISSION AGREEMENT)"

