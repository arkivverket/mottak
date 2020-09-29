from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


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


class ArkivuttrekkBase(BaseModel):
    """
    This version of Arkivuttrekk is created by parsing the metadatafile.
    All initial (parsed) information must be approved by personal of role coordinator.
    """
    obj_id: UUID = None
    status: ArkivuttrekkStatus = None
    type: ArkivuttrekkType = None
    tittel: str = None
    beskrivelse: str = None
    sjekksum_sha256: str = None
    avgiver_navn: str = None
    avgiver_epost: str = None
    koordinator_epost: str = None


class Arkivuttrekk(ArkivuttrekkBase):
    """
    This version of Arkivuttrekk has been persisted in and returned from the database.
    It contains fields generated in the database.
    """
    id: int
    opprettet: datetime
    endret: datetime

    class Config:
        orm_mode = True
