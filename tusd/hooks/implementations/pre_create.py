#!/usr/bin/env python3
import logging
import os  # for getenv
import sys

from hooks.implementations.hooks_utils import read_tusd_event, my_connect, get_data_from_db, my_disconnect
from hooks.implementations.return_codes import JSONERROR, USAGEERROR, UNKNOWNEID, UUIDERROR, OK
from hooks.models.HookData import HookData

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('dotenv not loaded')


# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.
# Todo clean up logging between hooks_utils and this file


# Todo: refactor, this is pretty long and ugly.
def run():
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
    # Silence the overly verbose service bus lib:
    logging.getLogger("uamqp").setLevel(logging.WARNING)

    logging.info('Running pre-create hook')
    # parse json on stdin into this structure.
    try:
        input_data = sys.stdin
        tusd_data = read_tusd_event(step='pre-create', input_data=input_data, logger=logging)
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
        exit(UNKNOWNEID)
    logging.info(f"Invitasjon_ekstern_id from JSON: {hook_data.ekstern_id}")

    if not (os.getenv('DBSTRING')):
        logging.error("DBSTRING environment variable not set")
        exit(USAGEERROR)

    connection = my_connect(os.getenv('DBSTRING'), logger=logging)
    data_from_db = get_data_from_db(connection, hook_data.ekstern_id, logger=logging)
    my_disconnect(connection)
    if not data_from_db:
        logging.error(f"Could not fetch metadata for invitasjon with ekstern_id={hook_data.ekstern_id} in the database")
        exit(UNKNOWNEID)
    if not data_from_db.ekstern_id:
        logging.error(f'Error while looking up ekstern_id from invitasjon ({hook_data.ekstern_id}) from DB:')
        exit(UNKNOWNEID)

    # This is the pre-create hook. The only concern here is to validate the UUID
    if hook_data.ekstern_id == data_from_db.ekstern_id:
        logging.info('Invitation ID verified.')
        exit(OK)
    else:
        logging.error(
            f'Ekstern_id mismatch (from DB:{data_from_db.ekstern_id} - from tusd: {hook_data.ekstern_id}')
        logging.error("Aborting")
        exit(UUIDERROR)


if __name__ == "__main__":
    run()
