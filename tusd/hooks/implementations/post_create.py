import logging
import os
import sys

import psycopg2
import psycopg2.extras

from hooks.implementations.hooks_utils import read_tusd_event, my_connect, my_disconnect, get_data_from_db
from hooks.implementations.return_codes import JSONERROR, OK, UNKNOWNEID, DBERROR
from hooks.implementations.status import OverforingspakkeStatus
from hooks.implementations.models.DataFromDatabase import DataFromDatabase
from hooks.implementations.models.HookData import HookData

DBSTRING = os.getenv('DBSTRING')


def add_overforingspakke_to_db(conn, data_from_db: DataFromDatabase, hook_data: HookData):
    """ Adds overforingspakke to mottak-arkiv-service db
        We do this as tusd assigns a random name to each object """
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO overforingspakke (arkivuttrekk_id, tusd_id, navn, storrelse, status) '  # TODO navn -> objekt_navn
            'VALUES (%s, %s, %s, %s, %s)',
            (data_from_db.arkivuttrekk_id, hook_data.tusd_id, hook_data.objekt_navn, hook_data.transferred_bytes,
             OverforingspakkeStatus.STARTET))
        conn.commit()
    except psycopg2.Error as exception:
        logging.error(f'Database error: {exception}')
        raise exception


def run():
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
    # Silence the overly verbose service bus lib:
    logging.getLogger("uamqp").setLevel(logging.WARNING)

    logging.info('Running post-create hook')
    # parse json on stdin into this structure.
    try:
        input_data = sys.stdin
        tusd_data = read_tusd_event(step='post-create', input_data=input_data, logger=logging)
    except Exception as exception:
        logging.error(exception)
        exit(JSONERROR)

    if not tusd_data:
        logging.error("Could not read tusd event.")
        exit(JSONERROR)

    # map tusd_data to parameter class
    hook_data = HookData.init_from_dict(tusd_data)
    if not hook_data.ekstern_id:
        logging.error("Could not find invitasjon_ekstern_id in JSON from hook event")
        exit(UNKNOWNEID)
    logging.info(f"Invitasjon_ekstern_id from JSON: {hook_data.ekstern_id}")

    connection = my_connect(DBSTRING, logger=logging)
    data_from_db = get_data_from_db(connection, hook_data.ekstern_id, logging)
    my_disconnect(connection)
    if not data_from_db:
        logging.error(f"Could not fetch metadata for invitasjon with ekstern_id={hook_data.ekstern_id} in the database")
        exit(UNKNOWNEID)

    try:
        add_overforingspakke_to_db(connection, data_from_db, hook_data)
    except Exception as exception:
        logging.error(f"Error while creating overforingspakke in database {exception}")
        exit(DBERROR)
    exit(OK)


if __name__ == '_main__':
    run()
