import pytest

from hooks.models.HookData import HookData


@pytest.fixture
def _hook_event_dict():
    return {
        "Upload": {
            "ID": "d1485b17-388f-4ec3-915f-c1fd60d8ef98",
            "Size": 440320,
            "SizeIsDeferred": False,
            "Offset": 0,
            "MetaData": {
                "fileName": "e4397dc9-a659-4788-838e-91611a38fae2.tar",
                "invitasjonEksternId": "e4397dc9-a659-4788-838e-91611a38fae2"
            },
            "IsPartial": False,
            "IsFinal": False,
            "PartialUploads": None,
            "Storage": {
                "Bucket": "tusd-storage",
                "Key": "d1485b17-388f-4ec3-915f-c1fd60d8ef98",
                "Type": "azurestore"
            }
        },
        "HTTPRequest": {
            "Method": "PATCH",
            "URI": "/files/9090fe36854e6761925e6e9ec475c17f",
            "RemoteAddr": "10.52.0.1:50725",
            "Header": {
                "Connection": ["Keep-Alive"],
                "Content-Length": ["440320"],
                "Content-Type": ["application/offset+octet-stream"],
                "Tus-Resumable": ["1.0.0"],
                "Upload-Offset": ["0"],
                "Via": ["1.1 google"],
                "X-Cloud-Trace-Context": [
                    "6e79e59c2a4408d889c3422178dd074f/7868454035101903276"
                ],
                "X-Forwarded-For": ["128.39.57.12, 34.107.169.47"],
                "X-Forwarded-Proto": ["https"]
            }
        }
    }


def test_hook_data(_hook_event_dict):
    expected = HookData(tusd_id="d1485b17-388f-4ec3-915f-c1fd60d8ef98",
                        ekstern_id="e4397dc9-a659-4788-838e-91611a38fae2",
                        transferred_bytes=0,
                        objekt_navn="d1485b17-388f-4ec3-915f-c1fd60d8ef98")
    actual = HookData.init_from_dict(_hook_event_dict)
    assert actual == expected


