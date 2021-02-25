from uuid import UUID

import pytest

from arkiv_downloader.models.dto import ArkivkopiRequest, ArkivkopiStatus


@pytest.fixture
def teststr_json_string() -> str:
    return '{"arkivkopi_id": 1, ' \
           '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
           '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'


@pytest.fixture
def testobj_arkivkopi_request() -> ArkivkopiRequest:
    return ArkivkopiRequest(
        arkivkopi_id=1,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )


@pytest.fixture
def testobj_arkivkopi_request_with_blob_info() -> ArkivkopiRequest:
    return ArkivkopiRequest(
        arkivkopi_id=1,
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature",
        blob_info={"source_name": "some/random/file", "target_name": "target_filename.tar"}
    )
