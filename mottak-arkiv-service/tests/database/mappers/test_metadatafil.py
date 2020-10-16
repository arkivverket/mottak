from datetime import datetime

import pytest

from app.database.dbo.mottak import Metadatafil as Metadatafil_DBO
from app.database.mappers.metadatafil import map_dbo2model
from app.domain.models.Metadatafil import Metadatafil


@pytest.fixture
def _dbo():
    return Metadatafil_DBO(
        id=1,
        type='xml/mets',
        innhold='innhold',
        filnavn='filnavn',
        opprettet=datetime.fromisoformat('2020-10-13 00:00:00'),
        endret=datetime.fromisoformat('2020-10-14 00:00:00'),
    )


def test_map_dbo2model(_dbo):
    """"
    GIVEN   a database object of type Metadatafil
    WHEN    calling the method map_dbo2model
    THEN    check that the returned domain object Metadatafil is correct
    """
    expected = Metadatafil(
        id_=1,
        type_='xml/mets',
        innhold='innhold',
        filnavn='filnavn',
        opprettet=datetime.fromisoformat('2020-10-13 00:00:00'),
        endret=datetime.fromisoformat('2020-10-14 00:00:00'),
    )

    actual = map_dbo2model(_dbo)

    assert vars(actual) == vars(expected)
