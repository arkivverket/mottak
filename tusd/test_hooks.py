
import pytest
import tusdhooks
import psycopg2
import psycopg2.errors
import io
import json
import unittest

print("We're running tests....")

pre_event = """{"Upload":{"ID":"","Size":440320,"SizeIsDeferred":false,"Offset":0,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitation_id":"2"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":null},"HTTPRequest":{"Method":"POST","URI":"/files","RemoteAddr":"10.52.0.1:58955","Header":{"Connection":["Keep-Alive"],"Content-Length":["0"],"Tus-Resumable":["1.0.0"],"Upload-Length":["440320"],"Upload-Metadata":["invitation_id Nw==,fileName ZGY1M2QxZDgtMzliZi00ZmVhLWE3NDEtNThkNDcyNjY0Y2UyLnRhcg=="],"Via":["1.1 google"],"X-Cloud-Trace-Context":["b167c3b206b0f8d40b1bfc018db3912f/16434868822010988609"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""
post_event = """{"Upload":{"ID":"9090fe36854e6761925e6e9ec475c17f","Size":440320,"SizeIsDeferred":false,"Offset":440320,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitation_id":"2"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":{"Bucket":"mottak2","Key":"9090fe36854e6761925e6e9ec475c17f","Type":"gcsstore"}},"HTTPRequest":{"Method":"PATCH","URI":"/files/9090fe36854e6761925e6e9ec475c17f","RemoteAddr":"10.52.0.1:50725","Header":{"Connection":["Keep-Alive"],"Content-Length":["440320"],"Content-Type":["application/offset+octet-stream"],"Tus-Resumable":["1.0.0"],"Upload-Offset":["0"],"Via":["1.1 google"],"X-Cloud-Trace-Context":["6e79e59c2a4408d889c3422178dd074f/7868454035101903276"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""
db_dict = {'user': 'test_user', 'password': 'test_password',
           'host': 'test_host', 'dbname': 'test_dbname'}


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


def test_create_db_access():
    info_str = 'pgsql::/user=test_user;password=test_password;host=test_host;dbname=test_dbname'
    generated_dict = tusdhooks.create_db_access(info_str)
    assert(generated_dict == db_dict)


def test_db_connect(mocker):
    # pylint: disable=no-member
    mocker.patch('psycopg2.connect')
    conn = tusdhooks.my_connect(db_dict)
    assert(conn)
    psycopg2.connect.assert_called_once() 


def test_read_tusd_pre_event(mocker):
    mocker.patch('sys.stdin', io.StringIO(pre_event))
    ret = tusdhooks.read_tusd_event('foo')
    assert(ret["Upload"]["MetaData"]["fileName"] ==
           "df53d1d8-39bf-4fea-a741-58d472664ce2.tar")
    assert(ret["Upload"]["MetaData"]["invitation_id"] == str(2))


def test_read_tusd_post_event(mocker):
    mocker.patch('sys.stdin', io.StringIO(post_event))
    ret = tusdhooks.read_tusd_event('bar')
    assert(ret["Upload"]["MetaData"]["fileName"] ==
           "df53d1d8-39bf-4fea-a741-58d472664ce2.tar")
    assert(ret["Upload"]["Storage"]["Key"] ==
           "9090fe36854e6761925e6e9ec475c17f")


def test_read_tusd_garbage(mocker):
    ret = None
    mocker.patch('sys.stdin', io.StringIO(' '))
    with pytest.raises(json.decoder.JSONDecodeError):
        ret = tusdhooks.read_tusd_event('foo')
    assert(ret == None)


def test_get_metadata1(mocker):
    print("Getting metadata...")
    mock_metadata = [{'invitation.id': 2, 'uuid': 'df53d1d8-39bf-4fea-a741-58d472664ce2',
                      'checksum': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                      'is_sensitive': False, 'name': 'Per Buer', 'email': 'perbue@arkivverket.no',
                      'type': 'noark5'}]

    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    # return this when calling cur.fetchall()
    mock_cur.fetchall.return_value = mock_metadata

    # mock_connection.return_value.cursor.return_value.fetch_all.return_value = mock_metadata
    ret_metadata = tusdhooks.get_metadata(mock_con, 2)
    assert(ret_metadata)
    assert(ret_metadata['invitation.id'] == 2)


def test_update_db_with_objectname(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 1
    tusdhooks.update_db_with_objectname(mock_con, 2, 'foo.txt')
    mock_cur.execute.assert_called_once()


def test_update_db_with_objectname_fail(mocker):

    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 0
    with pytest.raises(psycopg2.DataError):
        tusdhooks.update_db_with_objectname(mock_con, 2, 'foo.txt')
    mock_cur.execute.assert_called_once()


def test_get_sb_sender(mocker):
    # This is just a wrapper function. I'm not gonna test it.
    pass
    


def test_gather_params(mocker):
    expected = {'UUID': 'df53d1d8-39bf-4fea-a741-58d472664ce2', 'OBJECT': '9090fe36854e6761925e6e9ec475c17f', 'CHECKSUM': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a', 'ARCHIEVE_TYPE': 'noark5', 'NAME': 'Joe Black', 'EMAIL': 'perbue@arkivverket.no', 'INVITATIONID': 2}
    data = json.loads(post_event)
    metadata = invitation_dict
    params = tusdhooks.gather_params(data=data, dbdata=metadata)
    assert(params['UUID'] == 'df53d1d8-39bf-4fea-a741-58d472664ce2')
    assert(params['CHECKSUM'] == '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a')
    assert(params['EMAIL'] == 'perbue@arkivverket.no')
    assert(params == expected)



def test_argo_submit(mocker):
    pass
