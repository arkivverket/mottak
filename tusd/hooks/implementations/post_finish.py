#!/usr/bin/env python3
import json
import logging
import os  # for getenv
import sys
from datetime import datetime

import psycopg2
import psycopg2.extras
from azure.servicebus import QueueClient, Message

from .models.DataFromDatabase import DataFromDatabase
from .models.HookData import HookData
from .hooks_utils import read_tusd_event, my_connect, get_data_from_db, my_disconnect
from .return_codes import SBERROR, JSONERROR, USAGEERROR, UNKNOWNEID, DBERROR, OK
from .status import OverforingspakkeStatus

try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    print('dotenv not loaded')

# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.
# Todo: clean up logging between hooks_utils and this file


def update_overforingspakke_in_db(conn, hook_data: HookData):
    """ Updates overforingspakke in mottak-arkiv-service db with size and filename
        We do this as tusd assigns a random name to each object """
    try:
        cur = conn.cursor()
        cur.execute('UPDATE overforingspakke '
                    'SET storrelse = %s, status = %s, endret = %s '
                    'WHERE tusd_id = %s',
                    (hook_data.transferred_bytes, OverforingspakkeStatus.OK, datetime.now(), hook_data.tusd_id))
        if cur.rowcount != 1:
            raise psycopg2.DataError
        logging.debug(f"Updated status to OK for tusd_id {hook_data.tusd_id}")
        conn.commit()
    except psycopg2.Error as exception:
        logging.error(f'Database error: {exception}')
        raise exception


def gather_params(data_from_db: DataFromDatabase, hook_data: HookData):
    """ create dict with the relevant data from metadata (from DB) and from data (from stdin) """
    # define en workflow parameters
    params = {
        'TUSD_OBJEKT_NAVN': hook_data.objekt_navn,
        'SJEKKSUM': data_from_db.sjekksum,
        'EKSTERN_ID': data_from_db.ekstern_id,
        'KOORDINATOR_EPOST': data_from_db.koordinator_epost,
        'ARKIVUTTREKK_OBJ_ID': data_from_db.arkivuttrekk_obj_id,
        'ARKIVUTTREKK_TITTEL': data_from_db.tittel
    }
    return params


def get_sb_sender(conn_str, queue):
    try:
        queue_client = QueueClient.from_connection_string(
            conn_str, queue)
        return queue_client.get_sender()
    except Exception as exception:
        logging.error(f'Could not connect to Service Bus Queue: {exception}')
        logging.error(f'Queue: {queue}')
        exit(SBERROR)


def argo_submit(params):
    """ Submit a job to argo. Takes a dict with parameters. """
    conn_str = os.getenv('AZ_SB_CON_KICKER')
    queue = os.getenv('AZ_SB_QUEUE')
    message = {
        'action': 'argo-verify-overforingspakke',
        'params': params,
    }
    qsender = get_sb_sender(conn_str, queue)
    with qsender:
        try:
            message = Message(json.dumps(message).encode('utf8'))
            logging.info(f'Sending message: {message}')
            qsender.send(message)
        except Exception as exception:
            logging.error(
                f'Failed to send message over service bus: {exception}')
            exit(SBERROR)


# Todo: refactor, this is pretty long and ugly.
def run():
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
    # Silence the overly verbose service bus lib:
    logging.getLogger("uamqp").setLevel(logging.WARNING)

    logging.info('Running post-finish hook')
    # parse json on stdin into this structure.
    try:
        input_data = sys.stdin
        tusd_data = read_tusd_event(step='post-finish', input_data=input_data, logger=logging)
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

    if not (os.getenv('DBSTRING')):
        logging.error("DBSTRING environment variable not set")
        exit(USAGEERROR)

    connection = my_connect(os.getenv('DBSTRING'), logger=logging)
    data_from_db = get_data_from_db(connection, hook_data.ekstern_id, logger=logging)
    if not data_from_db:
        logging.error(f"Could not fetch metadata for invitasjon with ekstern_id={hook_data.ekstern_id} in the database")
        exit(UNKNOWNEID)

    try:
        update_overforingspakke_in_db(connection, hook_data)
    except Exception as exception:
        logging.error(f"Error while updating database {exception}")
        exit(DBERROR)
    my_disconnect(connection)
    params = gather_params(data_from_db, hook_data)
    argo_submit(params)
    exit(OK)


if __name__ == "__main__":
    run()
