import json
import pytest
from app.connectors.arkiv_downloader.models import ArkivkopiRequest, ArkivkopiStatusResponse
from app.connectors.sas_generator.models import SASResponse
from app.domain.models.Arkivkopi import ArkivkopiStatus


arkivkopi_id = 1
storage_account = "dasaccdev"
container = "33e8d091-48fd-4718-9c7a-abb9a266ee8f"
sas_token = "st=2021-01-28T12%3A44%3A26Z&se=2021-01-29T00%3A59%3A26Z&sp=rl&sv=2020-02-10&sr=c&sig=IGAxVlPEF1Y%2B6Xh9mCEa90Dtq8VXP3GVJaa2f/5P%2BMA%3D"
status = ArkivkopiStatus.BESTILT

@pytest.fixture()
def arkivkopi_request():
    return ArkivkopiRequest(arkivkopi_id, storage_account, container, sas_token)

@pytest.fixture()
def arkivkopi_status_response():
    return ArkivkopiStatusResponse(arkivkopi_id, status)


def test_arkivkopirequest_equals(arkivkopi_request):
    arkivkopi_request_2 = ArkivkopiRequest(arkivkopi_id, storage_account, container, sas_token)
    assert arkivkopi_request == arkivkopi_request_2


def test_arkivkopirequest_not_equals(arkivkopi_request):
    arkivkopi_request_2 = ArkivkopiRequest(arkivkopi_id+1, storage_account, container, sas_token)
    assert arkivkopi_request != arkivkopi_request_2


def test_arkivkopirequest_from_id_and_token(arkivkopi_request):
    sas_response = SASResponse(storage_account, container, sas_token)
    result = ArkivkopiRequest.from_id_and_token(arkivkopi_id, sas_response)
    assert arkivkopi_request == result


def test_arkivkopirequest_as_json(arkivkopi_request):
    result = arkivkopi_request.as_json_str()
    expected = json.dumps(arkivkopi_request.__dict__)
    assert expected == result


def test_arkivkopistatus_response_equals(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id, status)
    assert arkivkopi_status_response == arkivkopi_status_response_2


def test_arkivkopistatus_response_not_equals(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id+1, status)
    assert arkivkopi_status_response != arkivkopi_status_response_2


def test_arkivkopistatus_response_not_equals_status(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id, ArkivkopiStatus.BESTILLING_FEILET)
    assert not arkivkopi_status_response == arkivkopi_status_response_2


def test_arkivkopistatus_response_from_string(arkivkopi_status_response):
    arkivkopi_status_response_str = '{"arkivkopi_id": ' + str(arkivkopi_id) + ', "status": "' + status + '"}'
    arkivkopi_status_response_2 = ArkivkopiStatusResponse.from_string(arkivkopi_status_response_str)
    assert arkivkopi_status_response == arkivkopi_status_response_2
