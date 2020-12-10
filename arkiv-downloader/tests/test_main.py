import os

import pytest

from arkiv_downloader.main import get_sas_url, get_save_path, generate_azcopy_command
from arkiv_downloader.utils import get_project_root


@pytest.fixture
def _write_location() -> str:
    return str(get_project_root() / 'tests' / 'testdata')


def test_get_sas_url(testobj_arkivkopi_request):
    """
    GIVEN   an object of type ArkivkopiRequest
    WHEN    calling the method get_sas_url()
    THEN    check that the returned string is correct
    """
    expected = "https://storage_account_test.blob.core.windows.net/container_test?" \
               "se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    actual = get_sas_url(testobj_arkivkopi_request)
    assert actual == expected


def test_get_save_path(testobj_arkivkopi_request, _write_location):
    """
    GIVEN   an object of type ArkivkopiRequest
    WHEN    calling the method get_save_path()
    THEN    check that the returned string is correct
    """
    expected = \
        str(get_project_root() / 'tests' / 'testdata' / 'bb5fc65e-386d-11eb-915c-acde48001122') \
        + os.path.sep
    actual = get_save_path(testobj_arkivkopi_request.arkivuttrekk_id, _write_location)
    assert actual == expected


def test_generate_azcopy_command(testobj_arkivkopi_request, _write_location):
    """
    GIVEN   an object of type ArkivkopiRequest and a write_location
    WHEN    calling the method generate_azcopy_command()
    THEN    check that the returned string is correct
    """
    sas_token = "https://storage_account_test.blob.core.windows.net/container_test?" \
                "se=2020-12-05T14%3A40%3A54Z&sp=r&sv=2020-02-10&sr=c&sig=someSignature"
    save_path = _write_location + os.path.sep + "bb5fc65e-386d-11eb-915c-acde48001122" + os.path.sep
    expected = ['./azcopy/azcopy', 'cp', sas_token, save_path, '--recursive']
    actual = generate_azcopy_command(testobj_arkivkopi_request, save_path)
    assert actual == expected
