import logging
import pytest

from uuid import UUID
from arkiv_downloader.models.dto import ArkivkopiRequest, ArkivkopiStatusResponse, ArkivkopiStatus

logging.disable(logging.CRITICAL)


@pytest.fixture
def _json_string() -> str:
    return '{"arkivkopi_id": 1, "arkivuttrekk_id": "e9aa8f30-fda3-11ea-afc9-acde48001122", "status": "Bestilt", ' \
           '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
           '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'


@pytest.fixture
def _arkivkopi_request(_json_string) -> ArkivkopiRequest:
    return ArkivkopiRequest.from_string(_json_string)


@pytest.fixture
def _arkivkopi_status_response() -> ArkivkopiStatusResponse:
    return ArkivkopiStatusResponse(arkivuttrekk_id=UUID("e9aa8f30-fda3-11ea-afc9-acde48001122"),
                                   status=ArkivkopiStatus.STARTET)


def test_arkivkopirequest_from_string(_json_string):
    """
    GIVEN   a json string containing an ArkivkopiRequest
    WHEN    calling the method from_string() in ArkivkopiRequest
    THEN    controll that the returned ArkivkopiRequest is correct
    """
    expected = ArkivkopiRequest(
        arkivkopi_id=1,
        arkivuttrekk_id=UUID("e9aa8f30-fda3-11ea-afc9-acde48001122"),
        status=ArkivkopiStatus.BESTILT,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )
    actual = ArkivkopiRequest.from_string(_json_string)
    assert vars(actual) == vars(expected)


def test_arkivkopirequest_as_json_str(_arkivkopi_request):
    """
    GIVEN   an ArkivkopiRequest object
    WHEN    calling the method as_json_str() on the ArkivkopiRequest object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivkopi_id": 1, "arkivuttrekk_id": "e9aa8f30-fda3-11ea-afc9-acde48001122", "status": "Bestilt", ' \
               '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
               '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'
    actual = _arkivkopi_request.as_json_str()
    assert actual == expected


def test_arkivkopistatus_as_json_str(_arkivkopi_status_response):
    """
    GIVEN   an ArkivkopiStatus object
    WHEN    calling the method as_json_str() on the ArkivkopiStatus object
    THEN    controll that the returned json is correct
    """
    expected = '{"arkivuttrekk_id": "e9aa8f30-fda3-11ea-afc9-acde48001122", "status": "Startet"}'
    actual = _arkivkopi_status_response.as_json_str()
    assert actual == expected

