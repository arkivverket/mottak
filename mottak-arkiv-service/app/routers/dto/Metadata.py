from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.Arkivuttrekk import ArkivuttrekkType
from app.domain.models.Metadata import Metadata as Metadata_domain


class Metadata(BaseModel):
    """
    Used as response model for GET "/metadatafile/{id}/parsed
    """

    obj_id: Optional[UUID]
    type: Optional[ArkivuttrekkType]
    tittel: Optional[str]
    status: Optional[str]
    sjekksum_sha256: Optional[str]
    avgiver_navn: Optional[str]
    avgiver_epost: Optional[str]
    metadatafil_id: Optional[int]
    arkiv_startdato: Optional[date]
    arkiv_sluttdato: Optional[date]
    storrelse: Optional[float]
    avtalenummer: Optional[str]

    @staticmethod
    def from_domain(metadata: Metadata_domain):
        return Metadata(
            obj_id=metadata.obj_id,
            status=metadata.status,
            type=metadata.arkivutrekk_type,
            tittel=metadata.tittel,
            sjekksum_sha256=metadata.sjekksum_sha256,
            avgiver_navn=metadata.avgiver_navn,
            avgiver_epost=metadata.avgiver_epost,
            metadatafil_id=metadata.metadatafil_id,
            arkiv_startdato=metadata.arkiv_startdato,
            arkiv_sluttdato=metadata.arkiv_sluttdato,
            storrelse=metadata.storrelse,
            avtalenummer=metadata.avtalenummer
        )
