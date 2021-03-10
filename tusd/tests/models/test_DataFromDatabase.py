import pytest

from hooks.implementations.models.DataFromDatabase import DataFromDatabase


@pytest.fixture
def _database_dict():
    return {
        'invitasjon_id': 22,
        'ekstern_id': 'e4397dc9-a659-4788-838e-91611a38fae2',
        'koordinator_epost': 'koord@arkivverkettest.no'
    }


def test_init_from_dict(_database_dict):
    expected = DataFromDatabase(invitasjon_id=22,
                                ekstern_id="e4397dc9-a659-4788-838e-91611a38fae2",
                                koordinator_epost="koord@arkivverkettest.no")

    actual = DataFromDatabase.init_from_dict(_database_dict)
    assert actual == expected
