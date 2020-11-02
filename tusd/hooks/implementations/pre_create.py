#!/usr/bin/env python3
import os                               # for getenv
import sys
import logging

from .hooks_utils import read_tusd_event, my_connect, get_metadata, my_disconnect
from .return_codes import JSONERROR, USAGEERROR, UNKNOWNIID, UUIDERROR, OK, UNKNOWNUUID

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

    if not (os.getenv('DBSTRING')):
        logging.error("DBSTRING environment variable not set")
        exit(USAGEERROR)

    try:
        invitasjon_ekstern_id = tusd_data["Upload"]["MetaData"]["invitasjonEksternId"]
        logging.info(f"Invitation ID from JSON: {invitasjon_ekstern_id}")
        # todo: Specify exception.
    except:
        logging.error(f"Could not find invitasjon_ekstern_id in JSON: {invitasjon_ekstern_id}")
        exit(UNKNOWNIID)

    connection = my_connect(os.getenv('DBSTRING'), logger=logging)
    metadata = get_metadata(connection, invitasjon_ekstern_id, logger=logging)
    my_disconnect(connection)
    if not metadata:
        logging.error(
            f"Failed to fetch metadata for invitation {invitasjon_ekstern_id} - no invitation?")
        exit(UNKNOWNIID)

    try:
        uuid = metadata['uuid']
    except Exception as exception:
        logging.error(
            f'Error while looking up uuid from invition ({invitasjon_ekstern_id}) from DB: {exception}')
        exit(UNKNOWNUUID)

    # This is the pre-create hook. The only concern here is to validate the UUID
    if uuid == metadata['uuid']:
        logging.info('Invitation ID verified.')
        exit(OK)
    else:
        logging.error(
            f'UUID mismatch (from DB:{metadata["uuid"]} - from tusd: {uuid}')
        logging.error("Aborting")
        exit(UUIDERROR)


if __name__ == "__main__":
    run()
