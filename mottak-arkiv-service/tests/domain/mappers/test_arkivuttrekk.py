from datetime import date
from uuid import UUID

import pytest

from app.domain.mappers.arkivuttrekk import map_domain2dto_base
from app.domain.models.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkStatus, ArkivuttrekkType
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase


@pytest.fixture
def _arkivuttrekk():
    return Arkivuttrekk(
        obj_id=UUID('aa3835f4-514e-488f-b928-28d552d2d4d8'),
        status=ArkivuttrekkStatus.UNDER_OPPRETTING,
        type_=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="sjekksum_sha256",
        avgiver_navn="avgiver_navn",
        avgiver_epost="avgiver_epost",
        koordinator_epost="koordinator_epost",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1891-05-03"),
        arkiv_sluttdato=date.fromisoformat("1921-12-16"),
        storrelse=15.8,
        avtalenummer="avtalenummer"
    )


def test_map_domain2dto_base(_arkivuttrekk):
    """
    GIVEN   a domain object of type Arkivuttrekk
    WHEN    calling the method map_domain2dto_base
    THEN    check that the returned ArkivuttrekkBase DTO object is correct
    """
    expected = ArkivuttrekkBase(
        obj_id="aa3835f4-514e-488f-b928-28d552d2d4d8",
        status=ArkivuttrekkStatus.UNDER_OPPRETTING,
        type=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="sjekksum_sha256",
        avgiver_navn="avgiver_navn",
        avgiver_epost="avgiver_epost",
        koordinator_epost="koordinator_epost",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1891-05-03"),
        arkiv_sluttdato=date.fromisoformat("1921-12-16"),
        storrelse=15.8,
        avtalenummer="avtalenummer"
    )
    actual = map_domain2dto_base(_arkivuttrekk)
    assert vars(actual) == vars(expected)
