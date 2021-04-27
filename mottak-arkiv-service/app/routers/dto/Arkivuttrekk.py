from typing import List
from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType, Arkivuttrekk as Arkivuttrekk_domain


class Arkivuttrekk(BaseModel):
    """
    Used as the input parameter in POST "/arkivuttrekk/"
    """
    id: Optional[int]
    obj_id: UUID
    status: ArkivuttrekkStatus
    type: ArkivuttrekkType
    tittel: str
    sjekksum_sha256: str
    avgiver_navn: str
    avgiver_epost: str
    koordinator_epost: Optional[str]
    metadatafil_id: int
    arkiv_startdato: date
    arkiv_sluttdato: date
    storrelse: float
    avtalenummer: str
    opprettet: Optional[datetime]
    endret: Optional[datetime]

    def to_domain(self) -> Arkivuttrekk_domain:
        return Arkivuttrekk_domain(
            id_=self.id,
            obj_id=self.obj_id,
            status=self.status,
            type_=self.type,
            tittel=self.tittel,
            sjekksum_sha256=self.sjekksum_sha256,
            avgiver_navn=self.avgiver_navn,
            avgiver_epost=self.avgiver_epost,
            koordinator_epost=self.koordinator_epost,
            metadatafil_id=self.metadatafil_id,
            arkiv_startdato=self.arkiv_startdato,
            arkiv_sluttdato=self.arkiv_sluttdato,
            storrelse=self.storrelse,
            avtalenummer=self.avtalenummer,
            opprettet=self.opprettet,
            endret=self.endret
        )

    class Config:
        orm_mode = True


class AllArkivuttrekk(BaseModel):
    """
    """

    result: List[Arkivuttrekk]
    count: int
