import json
import pytest
from app.connectors.arkiv_downloader.models import ArkivkopiRequest, ArkivkopiStatusResponse, ArkivkopiRequestBlobInfo
from app.connectors.sas_generator.models import SASResponse
from app.domain.models.Arkivkopi import ArkivkopiStatus


arkivkopi_id = 1
storage_account = "storage_account_test"
container = "container_test"
sas_token = "se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
source_name = "some/random/file"
target_name = "target_filename.tar"
status = ArkivkopiStatus.BESTILT


@pytest.fixture
def testobj_arkivkopi_request_with_blob(testobj_arkivkopi_request) -> ArkivkopiRequest:
    blob_info = ArkivkopiRequestBlobInfo(source_name="some/random/file", target_name="target_filename.tar")
    testobj_arkivkopi_request.blob_info = blob_info
    return testobj_arkivkopi_request


@pytest.fixture
def arkivkopi_status_response():
    return ArkivkopiStatusResponse(arkivkopi_id, status)


def test_arkivkopirequest_equals(testobj_arkivkopi_request):
    result = ArkivkopiRequest(arkivkopi_id, storage_account, container, sas_token)
    assert result == testobj_arkivkopi_request


def test_arkivkopirequest_not_equals(testobj_arkivkopi_request):
    arkivkopi_request_2 = ArkivkopiRequest(arkivkopi_id+1, storage_account, container, sas_token)
    assert testobj_arkivkopi_request != arkivkopi_request_2


def test_arkivkopirequest_from_id_and_token(testobj_arkivkopi_request):
    sas_response = SASResponse(storage_account, container, sas_token)
    result = ArkivkopiRequest.from_id_and_token(arkivkopi_id, sas_response)
    assert testobj_arkivkopi_request == result


def test_arkivkopirequest_as_json(testobj_arkivkopi_request):
    result = testobj_arkivkopi_request.as_json_str()
    expected = json.dumps(testobj_arkivkopi_request.__dict__)
    assert expected == result


def test_arkivkopirequest_with_blob_info(testobj_arkivkopi_request_with_blob):
    blob_info = {"source_name": source_name, "target_name": target_name}
    expected = ArkivkopiRequest(arkivkopi_id, storage_account, container, sas_token, blob_info)
    assert expected == testobj_arkivkopi_request_with_blob


def test_arkivkopistatus_response_equals(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id, status)
    assert arkivkopi_status_response == arkivkopi_status_response_2


def test_arkivkopistatus_response_not_equals(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id+1, status)
    assert arkivkopi_status_response != arkivkopi_status_response_2


def test_arkivkopistatus_response_not_equals_status(arkivkopi_status_response):
    arkivkopi_status_response_2 = ArkivkopiStatusResponse(arkivkopi_id, ArkivkopiStatus.OK)
    assert arkivkopi_status_response != arkivkopi_status_response_2


def test_arkivkopistatus_response_from_string(arkivkopi_status_response):
    arkivkopi_status_response_str = '{"arkivkopi_id": ' + str(arkivkopi_id) + ', "status": "' + status + '"}'
    arkivkopi_status_response_2 = ArkivkopiStatusResponse.from_string(arkivkopi_status_response_str)
    assert arkivkopi_status_response == arkivkopi_status_response_2
