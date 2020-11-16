import json
import psycopg2
import pytest
from hooks.implementations.post_create import add_overforingspakke_to_db

post_event = """{"Upload":{"ID":"9090fe36854e6761925e6e9ec475c17f","Size":440320,"SizeIsDeferred":false,"Offset":440320,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitasjonEksternId":"d703908a-f39e-4e38-a0bf-64f64b6b7c86"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":{"Bucket":"mottak2","Key":"9090fe36854e6761925e6e9ec475c17f","Type":"gcsstore"}},"HTTPRequest":{"Method":"PATCH","URI":"/files/9090fe36854e6761925e6e9ec475c17f","RemoteAddr":"10.52.0.1:50725","Header":{"Connection":["Keep-Alive"],"Content-Length":["440320"],"Content-Type":["application/offset+octet-stream"],"Tus-Resumable":["1.0.0"],"Upload-Offset":["0"],"Via":["1.1 google"],"X-Cloud-Trace-Context":["6e79e59c2a4408d889c3422178dd074f/7868454035101903276"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""

mock_metadata = {'id': 2, 'uuid': 'df53d1d8-39bf-4fea-a741-58d472664ce2',
                 'checksum': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                 'is_sensitive': False, 'name': 'Per Buer', 'email': 'perbue@arkivverket.no',
                 'type': 'noark5', 'arkivuttrekk_id': 1, 'storrelse': 100}


def test_add_overforingspakke_to_db(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 1
    add_overforingspakke_to_db(mock_con, mock_metadata, json.loads(post_event))
    mock_cur.execute.assert_called_once()


def test_add_overforingspakke_to_db_fail(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 0
    with pytest.raises(psycopg2.DataError):
        add_overforingspakke_to_db(mock_con, mock_metadata, json.loads(post_event))
    mock_cur.execute.assert_called_once()
