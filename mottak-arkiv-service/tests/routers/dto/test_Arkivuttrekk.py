from datetime import datetime, date
from uuid import UUID

import pytest

from app.domain.models.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkStatus, ArkivuttrekkType
from app.routers.dto.Arkivuttrekk import Arkivuttrekk as Arkivuttrekk_dto

# Domain model
@pytest.fixture
def _arkivuttrekk(testfile_metadatfil) -> Arkivuttrekk:
    return Arkivuttrekk(
        id_=1,
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        type_=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        koordinator_epost="kornat@arkivverket.no",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1864-04-10"),
        arkiv_sluttdato=date.fromisoformat("1900-05-12"),
        storrelse=0.4562,
        avtalenummer="01/12345",
        opprettet=datetime.fromisoformat("2020-10-10"),
        endret=datetime.fromisoformat("2020-11-10")
    )

# DTO model
@pytest.fixture
def _arkivuttrekk_dto(testfile_metadatfil) -> Arkivuttrekk_dto:
    return Arkivuttrekk_dto(
        id=1,
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        type=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        koordinator_epost="kornat@arkivverket.no",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1864-04-10"),
        arkiv_sluttdato=date.fromisoformat("1900-05-12"),
        storrelse=0.4562,
        avtalenummer="01/12345",
        opprettet=datetime.fromisoformat("2020-10-10"),
        endret=datetime.fromisoformat("2020-11-10")
    )


def test_to_domain(_arkivuttrekk_dto):
    """
    GIVEN   an object of type ArkivuttrekkBase
    WHEN    calling the internal method to_domain()
    THEN    check that returned domain object Arkivuttrekk is correct
    """
    # Domain
    expected = Arkivuttrekk(
        id_=1,
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        type_=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        koordinator_epost="kornat@arkivverket.no",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1864-04-10"),
        arkiv_sluttdato=date.fromisoformat("1900-05-12"),
        storrelse=0.4562,
        avtalenummer="01/12345",
        opprettet=datetime.fromisoformat("2020-10-10"),
        endret=datetime.fromisoformat("2020-11-10")
    )
    actual = _arkivuttrekk_dto.to_domain()
    assert vars(actual) == vars(expected)
