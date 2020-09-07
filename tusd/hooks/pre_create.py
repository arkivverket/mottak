#!/usr/bin/env python3
# TODO clean up logging between hooks_utils and this file
# TODO Remove unused imports
# TODO Split hooks_utils into more files (ie db_utils)

import os                               # for getenv
import sys
import json
import psycopg2
import psycopg2.extras

import logging

from hooks.hooks_utils import read_tusd_event, my_connect, create_db_access, get_metadata, my_disconnect

from azure.servicebus import QueueClient, Message

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('dotenv not loaded')

# Todo: check that the uploader URL has not been tampered with - add some crypto
# Todo: improve error handling.
# Todo: this should have tests.

# Return codes.
UUIDERROR = 1    # invalid UUID
DBERROR = 10     #
JSONERROR = 11   # JSON parsing
IOERROR = 12
USAGEERROR = 13  # some sort of user error.
ARGOERROR = 14   # no in use anymore
UNKNOWNUUID = 15  # unknown UUID
UNKNOWNIID = 16  # unknown invitation
SBERROR = 17


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
    if (hook_name == 'pre-create'):
        if (uuid == metadata['uuid']):
            logging.info('Invitation ID verified.')
            exit(0)
        else:
            logging.error(
                f'UUID mismatch (from DB:{metadata["uuid"]} - from tusd: {uuid}')
            logging.error("Aborting")
            exit(UUIDERROR)
    else:
        logging.error(f'Unsupported hook: {hook_name}')
        exit(USAGEERROR)

    ########################################################
    ############# Run from here  ###########################
    ########################################################


if __name__ == "__main__":
    main()
