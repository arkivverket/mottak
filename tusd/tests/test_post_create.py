from hooks.implementations.post_create import add_overforingspakke_to_db
from hooks.implementations.models.DataFromDatabase import DataFromDatabase
from hooks.implementations.models.HookData import HookData

mock_hook_data = HookData(tusd_id="9090fe36854e6761925e6e9ec475c17f",
                          ekstern_id="df53d1d8-39bf-4fea-a741-58d472664ce2",
                          transferred_bytes=440320,
                          objekt_navn="9090fe36854e6761925e6e9ec475c17f")

mock_dbdata = DataFromDatabase(invitasjon_id=1,
                               ekstern_id="df53d1d8-39bf-4fea-a741-58d472664ce2")


def test_add_overforingspakke_to_db(mocker):
    # result of psycopg2.connect(**connection_stuff)
    mock_con = mocker.MagicMock()
    # result of con.cursor(cursor_factory=DictCursor)
    mock_cur = mock_con.cursor.return_value
    mock_cur.rowcount = 1
    add_overforingspakke_to_db(mock_con, mock_dbdata, mock_hook_data)
    mock_cur.execute.assert_called_once()
