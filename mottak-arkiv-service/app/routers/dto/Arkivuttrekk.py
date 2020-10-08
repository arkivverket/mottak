from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


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
    Used as the input parameter in POST "/arkivuttrekk/"
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
    Used as the response model for all kinds of arkivuttrekk.
    """
    id: int
    opprettet: datetime
    endret: datetime

    class Config:
        orm_mode = True
