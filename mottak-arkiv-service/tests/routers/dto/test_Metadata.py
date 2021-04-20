from datetime import date
from uuid import UUID

import pytest

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType
from app.domain.models.Metadata import Metadata as Metadata_domain
from app.routers.dto.Metadata import Metadata


@pytest.fixture
def _metadata() -> Metadata_domain:
    return Metadata_domain(
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        arkivutrekk_type=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1864-04-10"),
        arkiv_sluttdato=date.fromisoformat("1900-05-12"),
        storrelse=0.4562,
        avtalenummer="01/12345",
    )


def test_init_from(_metadata):
    """
    GIVEN   a domain object of type Arkivuttrekk
    WHEN    calling the static method from_domain()
    THEN    check that returned DTO object ArkivuttrekkBase is correct
    """
    expected = Metadata(
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        arkivutrekk_type=ArkivuttrekkType.NOARK5,
        tittel="tittel",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1864-04-10"),
        arkiv_sluttdato=date.fromisoformat("1900-05-12"),
        storrelse=0.4562,
        avtalenummer="01/12345",
    )
    actual = Metadata.from_domain(_metadata)
    assert vars(actual) == vars(expected)
