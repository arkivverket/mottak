import logging

import pytest

from arkiv_downloader.models.dto import ArkivkopiRequest, ArkivkopiStatusResponse, ArkivkopiStatus

logging.disable(logging.CRITICAL)


@pytest.fixture
def _arkivkopi_status_response() -> ArkivkopiStatusResponse:
    return ArkivkopiStatusResponse(arkivkopi_id=1,
                                   status=ArkivkopiStatus.STARTET)


def test_arkivkopirequest_from_string(teststr_json_string):
    """
    GIVEN   a json string containing an ArkivkopiRequest
    WHEN    calling the method from_string() in ArkivkopiRequest
    THEN    controll that the returned ArkivkopiRequest is correct
    """
    expected = ArkivkopiRequest(
        arkivkopi_id=1,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )
    actual = ArkivkopiRequest.from_string(teststr_json_string)
    assert actual == expected


def test_arkivkopirequest_as_json_str(testobj_arkivkopi_request):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as_json_str() on the ArkivkopiRequest object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature", "object_name": null}'
    actual = testobj_arkivkopi_request.as_json_str()
    assert actual == expected


def test_arkivkopistatus_as_json_str(_arkivkopi_status_response):
    """
    GIVEN   an ArkivkopiStatus object
    WHEN    calling the method as_json_str() on the ArkivkopiStatus object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, "status": "Startet"}'
    actual = _arkivkopi_status_response.as_json_str()
    assert actual == expected


def test_arkivkopirequest_as_safe_json_str(testobj_arkivkopi_request):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as__safe_json_str() on the ArkivkopiRequest object
    THEN    controll that the returned json is correct without sas_token
    """
    expected = '{"arkivkopi_id": 1, ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"<secret>", "object_name": null}'
    actual = testobj_arkivkopi_request.as_safe_json_str()
    assert actual == expected


def test_arkivkopirequest_with_object_name_as_json_str(testobj_arkivkopi_request_with_object_name):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as_json_str() on the ArkivkopiRequest object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature", '\
               '"object_name": "some/random/blob.tar"}'
    actual = testobj_arkivkopi_request_with_object_name.as_json_str()
    assert actual == expected
