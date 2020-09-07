#!/usr/bin/env python3
# TODO clean up logging between hooks_utils and this file
# TODO Remove unused imports
# TODO Split hooks_utils into more files (ie db_utils)

import os                               # for getenv
import sys
import logging


from hooks.implementations.hooks_utils import read_tusd_event, my_connect, create_db_access, get_metadata, my_disconnect
from hooks.implementations.error_codes import *


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('dotenv not loaded')

# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.


# Todo: refactor, this is pretty long and ugly.
def main():
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
    # Silence the overly verbose service bus lib:
    logging.getLogger("uamqp").setLevel(logging.WARNING)

    hook_name = os.path.basename(__file__)
    logging.info(f'hook running as {hook_name}')
    # parse json on stdin into this structure.
    try:
        input_data = sys.stdin
        tusd_data = read_tusd_event(step=hook_name, input_data=input_data)
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

    connection = my_connect(create_db_access(os.getenv('DBSTRING')))
    metadata = get_metadata(connection, iid)
    my_disconnect(connection)
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

    # This is the pre-create hook. The only concern here is to validate the UUID
    if (uuid == metadata['uuid']):
        logging.info('Invitation ID verified.')
        exit(0)
    else:
        logging.error(
            f'UUID mismatch (from DB:{metadata["uuid"]} - from tusd: {uuid}')
        logging.error("Aborting")
        exit(UUIDERROR)



if __name__ == "__main__":
    main()
