from datetime import date
from typing import Optional
from uuid import UUID

from app.domain.models.Arkivuttrekk import ArkivuttrekkType


class Metadata:
    """
    Domain class to contain a Metadata while it exists in the service layer
    """

    obj_id: Optional[UUID]
    arkivutrekk_type: Optional[ArkivuttrekkType]
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

    def __init__(self, obj_id, status, arkivutrekk_type, tittel, sjekksum_sha256, avgiver_navn, avgiver_epost,
                 metadatafil_id, arkiv_startdato, arkiv_sluttdato, storrelse, avtalenummer):
        self.obj_id = obj_id
        self.status = status
        self.arkivutrekk_type = arkivutrekk_type
        self.tittel = tittel
        self.sjekksum_sha256 = sjekksum_sha256
        self.avgiver_navn = avgiver_navn
        self.avgiver_epost = avgiver_epost

        self.metadatafil_id = metadatafil_id
        self.arkiv_startdato = arkiv_startdato
        self.arkiv_sluttdato = arkiv_sluttdato
        self.storrelse = storrelse
        self.avtalenummer = avtalenummer
