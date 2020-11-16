#!/usr/bin/env python3
import os  # for getenv
import sys
import json
import psycopg2
import psycopg2.extras
import logging
from azure.servicebus import QueueClient, Message

from .hooks_utils import read_tusd_event, my_connect, get_metadata, my_disconnect, extract_size_in_bytes_from_hook, \
    extract_filename_from_hook, extract_tusd_id_from_hook
from .return_codes import SBERROR, JSONERROR, USAGEERROR, UNKNOWNIID, DBERROR, UUIDERROR, OK

try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    print('dotenv not loaded')


# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.
# Todo: clean up logging between hooks_utils and this file


def update_overforingspakke_in_db(conn, tusd_data: dict):
    """ Updates overforingspakke in mottak-arkiv-service db with size and filename
        We do this as tusd assigns a random name to each object """
    object_size = extract_size_in_bytes_from_hook(tusd_data)
    tusd_id = extract_tusd_id_from_hook(tusd_data)
    try:
        cur = conn.cursor()
        cur.execute('UPDATE overforingspakke '
                    'SET storrelse = %s, status = %s '
                    'WHERE tusd_id = %s',
                    (object_size, 'OK', tusd_id))
        if cur.rowcount != 1:
            raise psycopg2.DataError
        logging.debug(f"Updated status to OK for tusd_id {tusd_id}")
        conn.commit()
    except psycopg2.Error as exception:
        logging.error(f'Database error: {exception}')
        raise exception


def gather_params(dbdata, data):
    """ create dict with the relevant data from metadata (from DB) and from data (from stdin) """
    # define en workflow parameters
    params = {
        'UUID': dbdata['uuid'],
        'OBJECT': data['Upload']['Storage']['Key'],
        'CHECKSUM': dbdata['checksum'],
        'ARCHIVE_TYPE': dbdata['type'],
        'NAME': dbdata['name'],
        'EMAIL': dbdata['email'],
        'INVITATION_ID': dbdata['id']
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
            ret = qsender.send(message)
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

    if not (os.getenv('DBSTRING')):
        logging.error("DBSTRING environment variable not set")
        exit(USAGEERROR)

    try:
        invitasjon_ekstern_id = tusd_data["Upload"]["MetaData"]["invitasjonEksternId"]
        logging.info(f"Invitation ID from JSON: {invitasjon_ekstern_id}")
        # todo: Specify exception.
    except:
        logging.error(f"Could not find invitation_id in JSON: {invitasjon_ekstern_id}")
        exit(UNKNOWNIID)

    connection = my_connect(os.getenv('DBSTRING'), logger=logging)
    metadata = get_metadata(connection, invitasjon_ekstern_id, logger=logging)
    if not metadata:
        logging.error(
            f"Failed to fetch metadata for invitation {invitasjon_ekstern_id} - no invitation?")
        exit(UNKNOWNIID)

    try:
        uuid = metadata['uuid']
    except Exception as exception:
        logging.error(
            f'Error while looking up uuid from invition ({invitasjon_ekstern_id}) from DB: {exception}')
        exit(UNKNOWNIID)

    try:
        update_overforingspakke_in_db(connection, metadata, tusd_data)
    except Exception as exception:
        logging.error("Error while updating database {exception}")
        exit(DBERROR)

    if metadata and ('uuid' in metadata):
        params = gather_params(metadata, tusd_data)
        argo_submit(params)
        my_disconnect(connection)
        exit(OK)
    else:
        logging.error("Unknown UUID:" + uuid)
        exit(UUIDERROR)


if __name__ == "__main__":
    run()
