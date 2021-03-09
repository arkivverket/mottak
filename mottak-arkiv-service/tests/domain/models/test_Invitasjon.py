from datetime import datetime
from uuid import UUID

import pytest

from app.domain.models.Invitasjon import Invitasjon, InvitasjonStatus


@pytest.fixture
def testobj_invitasjon():
    return Invitasjon(id_=1,
                      ekstern_id=UUID('b4c67f0d-4451-4473-b95a-4956e405c600'),
                      arkivuttrekk_id=1,
                      avgiver_epost="marelm@arkivverket.no",
                      status=InvitasjonStatus.SENDT,
                      opprettet=datetime.fromisoformat("2021-03-10T15:00:00+01:00"))


def test_eq(testobj_invitasjon):
    result = Invitasjon(id_=1,
                        ekstern_id=UUID('b4c67f0d-4451-4473-b95a-4956e405c600'),
                        arkivuttrekk_id=1,
                        avgiver_epost="marelm@arkivverket.no",
                        status=InvitasjonStatus.SENDT,
                        opprettet=datetime.fromisoformat("2021-03-10T15:00:00+01:00"))

    assert result == testobj_invitasjon
