#!/usr/bin/env python3
import os                               # for getenv
import sys
import json
import psycopg2
import psycopg2.extras
import logging
from azure.servicebus import QueueClient, Message

from .hooks_utils import read_tusd_event, my_connect, create_db_access, get_metadata, my_disconnect
from .error_codes import SBERROR, JSONERROR, USAGEERROR, UNKNOWNIID, DBERROR, UUIDERROR

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('dotenv not loaded')

# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.
# TODO clean up logging between hooks_utils and this file


def update_db_with_objectname(conn, iid, objectname):
    """ Update the database with the name of the relevant object as it is named in the object store.
        We do this as tusd assigns a random name to each object """
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE invitations SET object_name = %s WHERE id = %s", (objectname, iid))
        if cur.rowcount != 1:
            raise psycopg2.DataError
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
        'ARCHIEVE_TYPE': dbdata['type'],
        'NAME': dbdata['name'],
        'EMAIL': dbdata['email'],
        'INVITATIONID': dbdata['id']
    }
    return params


def get_sb_sender(conn_str, queue):
    try:
        queue_client = QueueClient.from_connection_string(
            conn_str, queue)
        return queue_client.get_sender()
    except Exception as exception:
        logging.error(f'Could not connect to Service Bus Queue: {exception}')
        logging.error(f'Connection string: {conn_str}')   # Todo: Potential security issue here. Filter out parts of the string?
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
        iid = tusd_data["Upload"]["MetaData"]["invitation_id"]
        logging.info(f"Invitation ID from JSON: {iid}")
        # todo: Specify exception.
    except:
        logging.error(f"Could not find invitation_id in JSON: {iid}")
        exit(UNKNOWNIID)

    connection = my_connect(create_db_access(os.getenv('DBSTRING'), logger=logging), logger=logging)
    metadata = get_metadata(connection, iid, logger=logging)
    if not metadata:
        logging.error(
            f"Failed to fetch metadata for invitation {iid} - no invitation?")
        exit(UNKNOWNIID)

    try:
        uuid = metadata['uuid']
    except Exception as exception:
        logging.error(
            f'Error while looking up uuid from invition ({iid}) from DB: {exception}')
        exit(UNKNOWNIID)

    # Verify that we have a filename:
    try:
        filename = tusd_data['Upload']['Storage']['Key']
        logging.debug(f"File name (in objectstore) is {filename}")
    except:
        logging.error("Could not key/filename in JSON. Dumping JSON:")
        logging.error(json.dumps(tusd_data, indent=4, sort_keys=True))
        exit(JSONERROR)

    try:
        update_db_with_objectname(connection, iid, filename)
        logging.debug(
            f"Set object_name to {filename} for iid {iid} in database.")
    except Exception as exception:
        logging.error("Error while updating database {exception}")
        exit(DBERROR)

    if metadata and ('uuid' in metadata):
        params = gather_params(metadata, tusd_data)
        argo_submit(params)
        my_disconnect(connection)
        exit(0)
    else:
        logging.error("Unknown UUID:" + uuid)
        exit(UUIDERROR)


if __name__ == "__main__":
    run()
