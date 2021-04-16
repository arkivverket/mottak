from datetime import date
from uuid import UUID

from app.domain.models.Arkivuttrekk import ArkivuttrekkStatus, ArkivuttrekkType
from app.domain.models.Metadata import Metadata


def test_as_arkivuttrekk(testfile_metadatfil):
    """
    GIVEN   a Metadatafil domain object
    WHEN    calling the internal method .as_arkivuttrekk()
    THEN    control that the returned Arkivuttrekk domain object is correct
    """
    expected = Metadata(
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        arkivutrekk_type=ArkivuttrekkType.NOARK5,
        tittel="The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1863-01-01"),
        arkiv_sluttdato=date.fromisoformat("1864-12-31"),
        storrelse=0.44032,
        avtalenummer="01/12345"
    )
    actual = testfile_metadatfil.as_metadata()
    assert vars(actual) == vars(expected)
