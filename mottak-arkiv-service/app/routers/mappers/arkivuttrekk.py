from app.database.dbo.mottak import Arkivuttrekk
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase


def map_from_domain_model(arkivuttrekk: Arkivuttrekk):
    return ArkivuttrekkBase(
        obj_id=arkivuttrekk.obj_id,
        status=arkivuttrekk.status,
        type_=arkivuttrekk.type,
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
