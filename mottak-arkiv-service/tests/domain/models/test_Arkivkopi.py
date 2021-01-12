import logging

import pytest

from app.domain.models.Arkivkopi import ArkivkopiRequest, ArkivkopiStatusResponse, ArkivkopiStatus

logging.disable(logging.CRITICAL)


@pytest.fixture
def teststr_json_string() -> str:
    return '{"arkivkopi_id": 1, "status": "Startet"}'


@pytest.fixture
def testobj_arkivkopi_request() -> ArkivkopiRequest:
    return ArkivkopiRequest(
        arkivkopi_id=1,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )


@pytest.fixture
def _arkivkopi_status_response() -> ArkivkopiStatusResponse:
    return ArkivkopiStatusResponse(arkivkopi_id=1,
                                   status=ArkivkopiStatus.STARTET)


def test_arkivkopirequest_as_json_str(testobj_arkivkopi_request):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as_json_str() on the ArkivkopiRequest object
    THEN    control that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'
    actual = testobj_arkivkopi_request.as_json_str()
    assert actual == expected


def test_arkivkopirequest_from_string(teststr_json_string):
    """
    GIVEN   a json string containing an ArkivkopiStatusResponse
    WHEN    calling the method from_string() in ArkivkopiStatusResponse
    THEN    control that the returned ArkivkopiStatusResponse is correct
    """
    expected = ArkivkopiStatusResponse(arkivkopi_id=1, status=ArkivkopiStatus.STARTET)
    actual = ArkivkopiStatusResponse.from_string(teststr_json_string)
    assert actual == expected
