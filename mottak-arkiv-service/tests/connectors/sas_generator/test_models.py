from app.connectors.sas_generator.models import SASTokenRequest

CONTAINER = 'e2ea3677-a0c6-4979-b478-fafdbcc9559b-0'


def test_SASTokenRequest():
    """
    GIVEN   static input data to SASTokenRequest
    WHEN    calling the method as_json()
    THEN    verify that the correct json string is returned
    """

    expected = '{"container": "e2ea3677-a0c6-4979-b478-fafdbcc9559b-0", "duration_hours": 24}'
    request = SASTokenRequest(container_id=CONTAINER, duration_hours=24)

    assert request.as_json() == expected
