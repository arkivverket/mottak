from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType


class ArkivuttrekkBase(BaseModel):
    """
    Used as the input parameter in POST "/arkivuttrekk/"
    and the response model for GET "/metadatafile/{id}/parsed
    """
    obj_id: UUID
    status: ArkivuttrekkStatus
    type: ArkivuttrekkType
    tittel: str
    sjekksum_sha256: str
    avgiver_navn: str
    avgiver_epost: str
    koordinator_epost: str = None
    metadatafil_id: int
    arkiv_startdato: date
    arkiv_sluttdato: date
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
