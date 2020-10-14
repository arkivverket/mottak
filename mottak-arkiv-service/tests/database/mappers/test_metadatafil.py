from datetime import datetime

import pytest

from app.database.dbo.mottak import Metadatafil as Metadatafil_DBO
from app.database.mappers.metadatafil import map_dbo2model
from app.domain.models.metadatafil import Metadatafil as Metadatafil_domain


@pytest.fixture
def test_dbo():
    return Metadatafil_DBO(
        id=1,
        type='xml/mets',
        innhold='innhold',
        filnavn='filnavn',
        opprettet=datetime.fromisoformat('2020-10-13 00:00:00'),
        endret=datetime.fromisoformat('2020-10-14 00:00:00'),
    )


def test_map_dbo2model(test_dbo):
    """"
    GIVEN   a database object of type Metadatafil
    WHEN    calling the method map_dbo2model
    THEN    check that the returned domain object Metadatafil is correct
    """
    expected = Metadatafil_domain(
        id=1,
        type='xml/mets',
        innhold='innhold',
        filnavn='filnavn',
        opprettet='2020-10-13 00:00:00',
        endret='2020-10-14 00:00:00',
    )

    actual = map_dbo2model(test_dbo)

    assert vars(actual) == vars(expected)
