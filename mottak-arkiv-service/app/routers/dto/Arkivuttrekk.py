from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType, Arkivuttrekk as Arkivuttrekk_domain


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

    @staticmethod
    def from_domain(arkivuttrekk: Arkivuttrekk_domain):
        return ArkivuttrekkBase(
            obj_id=arkivuttrekk.obj_id,
            status=arkivuttrekk.status,
            type=arkivuttrekk.type,
            tittel=arkivuttrekk.tittel,
            sjekksum_sha256=arkivuttrekk.sjekksum_sha256,
            avgiver_navn=arkivuttrekk.avgiver_navn,
            avgiver_epost=arkivuttrekk.avgiver_epost,
            koordinator_epost=arkivuttrekk.koordinator_epost,
            metadatafil_id=arkivuttrekk.metadatafil_id,
            arkiv_startdato=arkivuttrekk.arkiv_startdato,
            arkiv_sluttdato=arkivuttrekk.arkiv_sluttdato,
            storrelse=arkivuttrekk.storrelse,
            avtalenummer=arkivuttrekk.avtalenummer
        )


class Arkivuttrekk(ArkivuttrekkBase):
    """
    Used as the response model for all kinds of arkivuttrekk.
    """
    id: int
    opprettet: datetime
    endret: datetime

    class Config:
        orm_mode = True
