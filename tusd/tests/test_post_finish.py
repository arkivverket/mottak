import psycopg2
import pytest

from hooks.implementations.post_finish import gather_params, update_overforingspakke_in_db
from hooks.implementations.models.DataFromDatabase import DataFromDatabase
from hooks.implementations.models.HookData import HookData


mock_hook_data = HookData(tusd_id="9090fe36854e6761925e6e9ec475c17f",
                          ekstern_id="df53d1d8-39bf-4fea-a741-58d472664ce2",
                          transferred_bytes=440320,
                          objekt_navn="9090fe36854e6761925e6e9ec475c17f")

mock_dbdata = DataFromDatabase(ekstern_id="df53d1d8-39bf-4fea-a741-58d472664ce2",
                               sjekksum="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
                               avgiver_navn="Per Buer",
                               avgiver_epost="perbue@arkivverket.no",
                               koordinator_epost="laralv@arkivverket.no",
                               arkiv_type="Noark5",
                               arkivuttrekk_id=1,
                               storrelse=440320,
                               arkivuttrekk_obj_id="ed889fdc-b4d0-49fe-bf4b-caa0834cab2d")


def test_update_overforingspakke_in_db(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 1
    update_overforingspakke_in_db(mock_con, mock_hook_data)
    mock_cur.execute.assert_called_once()


def test_update_overforingspakke_in_db_fail(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 0
    with pytest.raises(psycopg2.DataError):
        update_overforingspakke_in_db(mock_con, mock_hook_data)
    mock_cur.execute.assert_called_once()


def test_gather_params(mocker):
    expected = {'TARGET_BUCKET_NAME': 'df53d1d8-39bf-4fea-a741-58d472664ce2-0',
                'TUSD_OBJEKT_NAVN': '9090fe36854e6761925e6e9ec475c17f',
                'SJEKKSUM': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
                'EKSTERN_ID': 'df53d1d8-39bf-4fea-a741-58d472664ce2', 'ARKIV_TYPE': 'Noark5',
                # 'AVGIVER_NAVN': 'Per Buer', 'AVGIVER_EPOST': 'perbue@arkivverket.no',
                'KOORDINATOR_EPOST': 'laralv@arkivverket.no',
                'ARKIVUTTREKK_OBJ_ID': "ed889fdc-b4d0-49fe-bf4b-caa0834cab2d"}
    # data = json.loads(post_event)
    # metadata = invitation_dict
    params = gather_params(hook_data=mock_hook_data, data_from_db=mock_dbdata)
    assert (params['TARGET_BUCKET_NAME'] == 'df53d1d8-39bf-4fea-a741-58d472664ce2-0')
    assert (params['SJEKKSUM'] == '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a')
    assert (params['KOORDINATOR_EPOST'] == 'laralv@arkivverket.no')
    assert (params == expected)
