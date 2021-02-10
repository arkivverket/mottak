import pytest
import psycopg2.errors
import io
import logging
import json

from hooks.implementations.hooks_utils import get_data_from_db, my_connect, read_tusd_event


pre_event = """{"Upload":{"ID":"","Size":440320,"SizeIsDeferred":false,"Offset":0,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitasjonEksternId":"d703908a-f39e-4e38-a0bf-64f64b6b7c86"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":null},"HTTPRequest":{"Method":"POST","URI":"/files","RemoteAddr":"10.52.0.1:58955","Header":{"Connection":["Keep-Alive"],"Content-Length":["0"],"Tus-Resumable":["1.0.0"],"Upload-Length":["440320"],"Upload-Metadata":["invitation_id Nw==,fileName ZGY1M2QxZDgtMzliZi00ZmVhLWE3NDEtNThkNDcyNjY0Y2UyLnRhcg=="],"Via":["1.1 google"],"X-Cloud-Trace-Context":["b167c3b206b0f8d40b1bfc018db3912f/16434868822010988609"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""
post_event = """{"Upload":{"ID":"9090fe36854e6761925e6e9ec475c17f","Size":440320,"SizeIsDeferred":false,"Offset":440320,"MetaData":{"fileName":"df53d1d8-39bf-4fea-a741-58d472664ce2.tar","invitasjonEksternId":"d703908a-f39e-4e38-a0bf-64f64b6b7c86"},"IsPartial":false,"IsFinal":false,"PartialUploads":null,"Storage":{"Bucket":"mottak2","Key":"9090fe36854e6761925e6e9ec475c17f","Type":"gcsstore"}},"HTTPRequest":{"Method":"PATCH","URI":"/files/9090fe36854e6761925e6e9ec475c17f","RemoteAddr":"10.52.0.1:50725","Header":{"Connection":["Keep-Alive"],"Content-Length":["440320"],"Content-Type":["application/offset+octet-stream"],"Tus-Resumable":["1.0.0"],"Upload-Offset":["0"],"Via":["1.1 google"],"X-Cloud-Trace-Context":["6e79e59c2a4408d889c3422178dd074f/7868454035101903276"],"X-Forwarded-For":["128.39.57.12, 34.107.169.47"],"X-Forwarded-Proto":["https"]}}}"""
db_string = 'postgresql://user@resource_group:random_pwd@server.postgres.database.azure.com:5432/postgres?sslmode=require'

ekstern_id = 'df53d1d8-39bf-4fea-a741-58d472664ce2'
mock_metadata = {'invitasjon_id': 2,
                 'ekstern_id': ekstern_id,
                 'sjekksum': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                 'avgiver_navn': 'Per Buer',
                 'avgiver_epost': 'perbue@arkivverket.no',
                 'koordinator_epost': 'marelm@arkivverket.no',
                 'arkiv_type': 'noark5',
                 'arkivuttrekk_id': 1,
                 'storrelse': 100}


def test_db_connect(mocker):
    # pylint: disable=no-member
    mocker.patch('psycopg2.connect')
    conn = my_connect(db_string, logging)
    assert conn
    psycopg2.connect.assert_called_once()


def test_read_tusd_pre_event(mocker):
    ret = read_tusd_event('foo', io.StringIO(pre_event), logging)
    assert (ret["Upload"]["MetaData"]["fileName"] ==
            "df53d1d8-39bf-4fea-a741-58d472664ce2.tar")
    assert (ret["Upload"]["MetaData"]["invitasjonEksternId"] == "d703908a-f39e-4e38-a0bf-64f64b6b7c86")


def test_read_tusd_post_event(mocker):
    ret = read_tusd_event('bar', io.StringIO(post_event), logging)
    assert (ret["Upload"]["MetaData"]["fileName"] ==
            "df53d1d8-39bf-4fea-a741-58d472664ce2.tar")
    assert (ret["Upload"]["Storage"]["Key"] ==
            "9090fe36854e6761925e6e9ec475c17f")


def test_read_tusd_garbage(mocker):
    ret = None
    with pytest.raises(json.decoder.JSONDecodeError):
        ret = read_tusd_event('foo', io.StringIO(' '), logging)
    assert (ret is None)


def test_get_metadata1(mocker):
    print("Getting metadata...")
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    # return this when calling cur.fetchall()
    mock_cur.fetchall.return_value = [mock_metadata]

    # mock_connection.return_value.cursor.return_value.fetch_all.return_value = mock_metadata
    data_from_db = get_data_from_db(mock_con, ekstern_id, logging)
    assert data_from_db
    assert data_from_db.ekstern_id == ekstern_id


def test_get_sb_sender(mocker):
    # This is just a wrapper function. I'm not gonna test it.
    pass


def test_argo_submit(mocker):
    pass
