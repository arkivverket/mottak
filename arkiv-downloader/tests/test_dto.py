import logging
from uuid import UUID

import pytest

from arkiv_downloader.models.dto import ArkivkopiRequest, ArkivkopiStatusResponse, ArkivkopiStatus

logging.disable(logging.CRITICAL)


@pytest.fixture
def _arkivkopi_status_response() -> ArkivkopiStatusResponse:
    return ArkivkopiStatusResponse(arkivuttrekk_id=UUID("bb5fc65e-386d-11eb-915c-acde48001122"),
                                   status=ArkivkopiStatus.STARTET)


def test_arkivkopirequest_from_string(teststr_json_string):
    """
    GIVEN   a json string containing an ArkivkopiRequest
    WHEN    calling the method from_string() in ArkivkopiRequest
    THEN    controll that the returned ArkivkopiRequest is correct
    """
    expected = ArkivkopiRequest(
        arkivkopi_id=1,
        arkivuttrekk_id=UUID("bb5fc65e-386d-11eb-915c-acde48001122"),
        status=ArkivkopiStatus.BESTILT,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )
    actual = ArkivkopiRequest.from_string(teststr_json_string)
    assert vars(actual) == vars(expected)


def test_arkivkopirequest_as_json_str(testobj_arkivkopi_request):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as_json_str() on the ArkivkopiRequest object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, "arkivuttrekk_id": "bb5fc65e-386d-11eb-915c-acde48001122", "status": "Bestilt", ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'
    actual = testobj_arkivkopi_request.as_json_str()
    assert actual == expected


def test_arkivkopistatus_as_json_str(_arkivkopi_status_response):
    """
    GIVEN   an ArkivkopiStatus object
    WHEN    calling the method as_json_str() on the ArkivkopiStatus object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivuttrekk_id": "bb5fc65e-386d-11eb-915c-acde48001122", "status": "Startet"}'
    actual = _arkivkopi_status_response.as_json_str()
    assert actual == expected

