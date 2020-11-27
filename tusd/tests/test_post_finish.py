import json
import psycopg2
import pytest

from hooks.implementations.post_finish import gather_params, update_overforingspakke_in_db

post_event = """{"Upload":{"ID":"9090fe36854e6761925e6e9ec475c17f","Size":440320,"SizeIsDeferred":false,"Offset":440320,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitasjonEksternId":"d703908a-f39e-4e38-a0bf-64f64b6b7c86"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":{"Bucket":"mottak2","Key":"9090fe36854e6761925e6e9ec475c17f","Type":"gcsstore"}},"HTTPRequest":{"Method":"PATCH","URI":"/files/9090fe36854e6761925e6e9ec475c17f","RemoteAddr":"10.52.0.1:50725","Header":{"Connection":["Keep-Alive"],"Content-Length":["440320"],"Content-Type":["application/offset+octet-stream"],"Tus-Resumable":["1.0.0"],"Upload-Offset":["0"],"Via":["1.1 google"],"X-Cloud-Trace-Context":["6e79e59c2a4408d889c3422178dd074f/7868454035101903276"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""

invitation_dict = {'id': 2,
                   'created_at': '2020-05-20 10:32:45',
                   'updated_at': '2020-05-20 10:32:59',
                   'archive_type_id': 2,
                   'uuid': 'df53d1d8-39bf-4fea-a741-58d472664ce2',
                   'checksum': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                   'is_sensitive': False,
                   'name': 'Joe Black',
                   'email': 'perbue@arkivverket.no',
                   'is_uploaded': False,
                   'object_name': None,
                   'archive': 'Statens Institutt for forbruksforskning (2003 - 2016) - 4152',
                   'type': 'noark5'
                   }


def test_update_overforingspakke_in_db(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 1
    update_overforingspakke_in_db(mock_con, json.loads(post_event))
    mock_cur.execute.assert_called_once()


def test_update_overforingspakke_in_db_fail(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 0
    with pytest.raises(psycopg2.DataError):
        update_overforingspakke_in_db(mock_con, json.loads(post_event))
    mock_cur.execute.assert_called_once()


def test_gather_params(mocker):
    expected = {'UUID': 'df53d1d8-39bf-4fea-a741-58d472664ce2', 'OBJECT': '9090fe36854e6761925e6e9ec475c17f',
                'CHECKSUM': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                'ARCHIVE_TYPE': 'noark5', 'NAME': 'Joe Black', 'EMAIL': 'perbue@arkivverket.no', 'INVITATION_ID': 2}
    data = json.loads(post_event)
    metadata = invitation_dict
    params = gather_params(data=data, dbdata=metadata)
    assert (params['UUID'] == 'df53d1d8-39bf-4fea-a741-58d472664ce2')
    assert (params['CHECKSUM'] == '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a')
    assert (params['EMAIL'] == 'perbue@arkivverket.no')
    assert (params == expected)