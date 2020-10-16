from app.domain.models.Arkivuttrekk import Arkivuttrekk
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase


def map_domain2dto_base(domain: Arkivuttrekk) -> ArkivuttrekkBase:
    """
    Method that converts a domain object of type Arkivuttrekk into a DTO of type ArkivuttrekkBase.
    """
    dto = ArkivuttrekkBase(
        obj_id= domain.obj_id,
        status=domain.status,
        type=domain.type,
        tittel=domain.tittel,
        sjekksum_sha256=domain.sjekksum_sha256,
        avgiver_navn=domain.avgiver_navn,
        avgiver_epost=domain.avgiver_epost,
        koordinator_epost=domain.koordinator_epost,
        metadatafil_id=domain.metadatafil_id,
        arkiv_startdato=domain.arkiv_startdato,
        arkiv_sluttdato=domain.arkiv_sluttdato,
        storrelse=domain.storrelse,
        avtalenummer=domain.avtalenummer
    )
    return dto
