from uuid import UUID

from app.connectors.sas_generator.models import SASTokenRequest

CONTAINER = UUID('e2ea3677-a0c6-4979-b478-fafdbcc9559b')


def test_SASTokenRequest():
    """
    GIVEN   static input data to SASTokenRequest
    WHEN    calling the method as_json()
    THEN    verify that the correct json string is returned
    """

    expected = '{"container": "e2ea3677-a0c6-4979-b478-fafdbcc9559b-0", "duration": 24}'
    request = SASTokenRequest(container=CONTAINER, duration=24)

    assert request.as_json() == expected
