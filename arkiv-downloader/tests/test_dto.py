import logging
from uuid import uuid1
from arkiv_downloader.models.dto import ArkivuttrekkTransferInfo, ArkivuttrekkTransferStatus, TransferStatus

logging.disable(logging.CRITICAL)


def test_ArkivuttrekkTransferInfo_from_correct_string():
    json_string = '{"obj_id": "e9aa8f30-fda3-11ea-afc9-acde48001122", "container_sas_url": "https://storageaccount.blob.core.windows.net/containerid?sp=rl&st=2020-09-23T13:21:28Z&se=2020-09-24T13:21:28Z&sv=2019-12-12&sr=someSignature"}'
    a = ArkivuttrekkTransferInfo.from_string(json_string)
    assert a
    assert a.as_json_str() == json_string


def test_ArkivuttrekkTransferInfo_from_string_missing_obj_id():
    json_string = '{"container_sas_url": "https://storageaccount.blob.core.windows.net/containerid?sp=rl&st=2020-09-23T13:21:28Z&se=2020-09-24T13:21:28Z&sv=2019-12-12&sr=c&sig=someSignature"}'
    a = ArkivuttrekkTransferInfo.from_string(json_string)
    assert not a


def test_ArkivuttrekkTransferInfo_from_string_missing_container_sas_url():
    json_string = '{"obj_id": "e9aa8f30-fda3-11ea-afc9-acde48001122"}'
    a = ArkivuttrekkTransferInfo.from_string(json_string)
    assert not a


def test_ArkivuttrekkTransferStatus_obj_id_ok():
    uuid = uuid1()
    status = TransferStatus.STARTING_TRANSFER
    a = ArkivuttrekkTransferStatus(uuid, status)
    assert uuid == a.obj_id, 'ID should be identical'
    assert status == a.status, 'Status should be identical'


def test_ArkivuttrekkTransferStatus_as_json_str():
    uuid = uuid1()
    status = TransferStatus.STARTING_TRANSFER
    result = ArkivuttrekkTransferStatus(uuid, status).as_json_str()
    expected_id_in_string = f'"obj_id": "{uuid}"'
    expected_status_in_string = f'"status": "{status}"'
    assert expected_id_in_string in result, 'obj_id should be correct in json string'
    assert expected_status_in_string in result, 'status should be correct in json string'
