from uuid import UUID

import pytest

from arkiv_downloader.models.dto import ArkivkopiRequest, ArkivkopiStatus


@pytest.fixture
def teststr_json_string() -> str:
    return '{"arkivkopi_id": 1, "arkivuttrekk_id": "bb5fc65e-386d-11eb-915c-acde48001122", ' \
           '"storage_account": "storage_account_test", "container": "container_test", "sas_token": ' \
           '"se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"}'


@pytest.fixture
def testobj_arkivkopi_request() -> ArkivkopiRequest:
    return ArkivkopiRequest(
        arkivkopi_id=1,
        arkivuttrekk_id=UUID('bb5fc65e-386d-11eb-915c-acde48001122'),
        storage_account="storage_account_test",
        container="container_test",
        sas_token="se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    )
