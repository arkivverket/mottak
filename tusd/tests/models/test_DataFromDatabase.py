import pytest

from hooks.models.DataFromDatabase import DataFromDatabase


@pytest.fixture
def _database_dict():
    return {
        'invitasjon_id': 33,
        'ekstern_id': 'e4397dc9-a659-4788-838e-91611a38fae2',
        'sjekksum': '30899115bd4fa04778e2cd13c80236b46b6aa4f7dfec33fa0996228e673d9946',
        'avgiver_navn': 'Avgiver Avgiversen',
        'avgiver_epost': 'avgav@arkivverkettest.no',
        'koordinator_epost': 'koord@arkivverkettest.no',
        'arkiv_type': 'Noark5',
        'arkivuttrekk_id': 22,
        'storrelse': 440320
    }


def test_init_from_dict(_database_dict):
    expected = DataFromDatabase(invitasjon_id=33,
                                ekstern_id="e4397dc9-a659-4788-838e-91611a38fae2",
                                sjekksum="30899115bd4fa04778e2cd13c80236b46b6aa4f7dfec33fa0996228e673d9946",
                                avgiver_navn="Avgiver Avgiversen",
                                avgiver_epost="avgav@arkivverkettest.no",
                                koordinator_epost="koord@arkivverkettest.no",
                                arkiv_type="Noark5",
                                arkivuttrekk_id=22,
                                storrelse=440320)

    actual = DataFromDatabase.init_from_dict(_database_dict)
    assert actual == expected
