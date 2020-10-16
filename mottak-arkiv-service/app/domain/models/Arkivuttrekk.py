from datetime import date, datetime
from enum import Enum
from uuid import UUID


class ArkivuttrekkStatus(str, Enum):
    UNDER_OPPRETTING = 'Under oppretting'
    INVITERT = "Invitert"
    UNDER_BEHANDLING = "Under behandling"
    AVVIST = "Avvist"
    SENT_TIL_BEVARING = "Sent til bevaring"


class ArkivuttrekkType(str, Enum):
    NOARK3 = "Noark3"
    NOARK5 = "Noark5"
    FAGSYSTEM = "Fagsystem"


class Arkivuttrekk:
    """
    Domain class to contain a Arkivuttrekk while it exists in the service layer
    """
    id: int
    obj_id: UUID
    status: ArkivuttrekkStatus
    type: ArkivuttrekkType
    tittel: str
    sjekksum_sha256: str
    avgiver_navn: str
    avgiver_epost: str
    koordinator_epost: str
    metadatafil_id: int
    arkiv_startdato: date
    arkiv_sluttdato: date
    storrelse: float
    avtalenummer: str
    opprettet: datetime
    endret: datetime

    def __init__(self,
                 id_=None,
                 obj_id=None,
                 status=None,
                 type_=None,
                 tittel=None,
                 sjekksum_sha256=None,
                 avgiver_navn=None,
                 avgiver_epost=None,
                 koordinator_epost=None,
                 metadatafil_id=None,
                 arkiv_startdato=None,
                 arkiv_sluttdato=None,
                 storrelse=None,
                 avtalenummer=None,
                 opprettet=None,
                 endret=None):
        self.id = id_
        self.obj_id = obj_id
        self.status = status
        self.type = type_
        self.tittel = tittel
        self.sjekksum_sha256 = sjekksum_sha256
        self.avgiver_navn = avgiver_navn
        self.avgiver_epost = avgiver_epost
        self.koordinator_epost = koordinator_epost
        self.metadatafil_id = metadatafil_id
        self.arkiv_startdato = arkiv_startdato
        self.arkiv_sluttdato = arkiv_sluttdato
        self.storrelse = storrelse
        self.avtalenummer = avtalenummer
        self.opprettet = opprettet
        self.endret = endret
