from datetime import date
from uuid import UUID

import pytest

from app.domain.models.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkStatus, ArkivuttrekkType
from app.domain.models.Metadata import Metadata
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase


@pytest.fixture
def _arkivuttrekk(testfile_metadatfil) -> Metadata:
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
        opprettet=date.fromisoformat("2020-10-10"),
        endret=date.fromisoformat("2020-11-10")
    )


@pytest.fixture
def _arkivuttrekk_base(testfile_metadatfil) -> ArkivuttrekkBase:
    return ArkivuttrekkBase(
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
    )


# def test_to_domain(_arkivuttrekk_base):
#     """
#     GIVEN   an object of type ArkivuttrekkBase
#     WHEN    calling the internal method to_domain()
#     THEN    check that returned domain object Arkivuttrekk is correct
#     """
#     expected = Metadata(
#         obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
#         status=ArkivuttrekkStatus.OPPRETTET,
#         type_=ArkivuttrekkType.NOARK5,
#         tittel="tittel",
#         sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
#         avgiver_navn="Lewis Caroll",
#         avgiver_epost="lewis@caroll.net",
#         koordinator_epost="kornat@arkivverket.no",
#         metadatafil_id=1,
#         arkiv_startdato=date.fromisoformat("1864-04-10"),
#         arkiv_sluttdato=date.fromisoformat("1900-05-12"),
#         storrelse=0.4562,
#         avtalenummer="01/12345",
#     )
#     actual = _arkivuttrekk_base.to_domain()
#     assert vars(actual) == vars(expected)


def test_init_from(_arkivuttrekk):
    """
    GIVEN   a domain object of type Arkivuttrekk
    WHEN    calling the static method from_domain()
    THEN    check that returned DTO object ArkivuttrekkBase is correct
    """
    expected = ArkivuttrekkBase(
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
    )
    actual = ArkivuttrekkBase.from_domain(_arkivuttrekk)
    assert vars(actual) == vars(expected)
