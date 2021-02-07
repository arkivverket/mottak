#!/usr/bin/env python3
import json
import logging
import os  # for getenv
import sys
from datetime import datetime

import psycopg2
import psycopg2.extras
from azure.servicebus import QueueClient, Message

from hooks.models.DataFromDatabase import DataFromDatabase
from hooks.models.HookData import HookData
from .hooks_utils import read_tusd_event, my_connect, get_metadata, my_disconnect
from .return_codes import SBERROR, JSONERROR, USAGEERROR, UNKNOWNIID, DBERROR, OK, UNKNOWNUUID
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
        'UUID': data_from_db.ekstern_id,
        'OBJECT': hook_data.objekt_navn,
        'CHECKSUM': data_from_db.sjekksum,  # THE ONLY PARAM WE KEEP AFTER MOL-284 CHANGES
        'ARCHIEVE_TYPE': data_from_db.arkiv_type,
        'NAME': data_from_db.avgiver_navn,
        'EMAIL': data_from_db.avgiver_epost,
        'INVITATIONID': data_from_db.invitasjon_id,
        # THESE ARE NEW KEYS, REMOVE UNUSED AFTER ALL MOL-284 CHANGES ARE DONE IN KICKER AND ENTAILING COMPONENTS
        'TARGET_CONTAINER_NAME': data_from_db.ekstern_id,
        'TUSD_OBJECT_NAME': hook_data.objekt_navn,
        'EXTERNAL_ID': data_from_db.ekstern_id,
        'ARCHIVE_TYPE': data_from_db.arkiv_type,
        'SUBMITTER_NAME': data_from_db.avgiver_navn,
        'SUBMITTER_EMAIL': data_from_db.avgiver_epost,
        'INVITATION_ID': data_from_db.invitasjon_id
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
        'action': 'argo-submit',
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
    hook_data = HookData(tusd_data)
    if not hook_data.ekstern_id:
        logging.error("Could not find invitasjon_ekstern_id in JSON from hook event")
        exit(UNKNOWNIID)
    logging.info(f"Invitasjon_ekstern_id from JSON: {hook_data.ekstern_id}")

    if not (os.getenv('DBSTRING')):
        logging.error("DBSTRING environment variable not set")
        exit(USAGEERROR)

    connection = my_connect(os.getenv('DBSTRING'), logger=logging)
    metadata = get_metadata(connection, hook_data.ekstern_id, logger=logging)
    my_disconnect(connection)
    if not metadata:
        logging.error(
            f"Failed to fetch metadata for invitation {hook_data.ekstern_id} - no invitation?")
        exit(UNKNOWNIID)

    # map metadata dict to parameter class
    data_from_db = DataFromDatabase.init_from_dict(metadata)
    if not data_from_db.ekstern_id:
        logging.error(f'Error while looking up ekstern_id from invitasjon ({hook_data.ekstern_id}) from DB:')
        exit(UNKNOWNUUID)

    try:
        update_overforingspakke_in_db(connection, hook_data)
    except Exception as exception:
        logging.error(f"Error while updating database {exception}")
        exit(DBERROR)

    params = gather_params(data_from_db, hook_data)
    argo_submit(params)
    exit(OK)


if __name__ == "__main__":
    run()
