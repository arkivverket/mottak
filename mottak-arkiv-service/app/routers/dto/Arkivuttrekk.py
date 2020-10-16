from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType


class ArkivuttrekkBase(BaseModel):
    """
    Used as the input parameter in POST "/arkivuttrekk/"
    and the response model for GET "/metadatafile/{id}/parsed
    """
    obj_id: UUID = None
    status: ArkivuttrekkStatus = None
    type: ArkivuttrekkType = None
    tittel: str = None
    sjekksum_sha256: str = None
    avgiver_navn: str = None
    avgiver_epost: str = None
    koordinator_epost: str = None
    metadatafil_id: int = None
    arkiv_startdato: date = None
    arkiv_sluttdato: date = None
    storrelse: float
    avtalenummer: str


class Arkivuttrekk(ArkivuttrekkBase):
    """
    Used as the response model for all kinds of arkivuttrekk.
    """
    id: int
    opprettet: datetime
    endret: datetime

    class Config:
        orm_mode = True
