import os
import sys
import logging
import psycopg2
import psycopg2.extras

from .return_codes import JSONERROR, OK
from .status import OverforingspakkeStatus
from .hooks_utils import read_tusd_event, my_connect, my_disconnect, extract_tusd_id_from_hook, \
    extract_filename_from_hook, extract_offset_size_in_bytes_from_hook, get_metadata


DBSTRING = os.getenv('DBSTRING')


def add_overforingspakke_to_db(conn, metadata: dict, tusd_data: dict):
    """ Adds overforingspakke to mottak-arkiv-service db
        We do this as tusd assigns a random name to each object """
    offset_size = extract_offset_size_in_bytes_from_hook(tusd_data)
    filename = extract_filename_from_hook(tusd_data)
    tusd_id = extract_tusd_id_from_hook(tusd_data)
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO overforingspakke (arkivuttrekk_id, tusd_id, navn, storrelse, status) '
            'VALUES (%s, %s, %s, %s, %s)',
            (metadata['arkivuttrekk_id'], tusd_id, filename, offset_size, OverforingspakkeStatus.STARTET))
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

    invitasjon_ekstern_id = tusd_data["Upload"]["MetaData"]["invitasjonEksternId"]

    connection = my_connect(DBSTRING, logger=logging)
    metadata = get_metadata(connection, invitasjon_ekstern_id, logging)
    add_overforingspakke_to_db(connection, metadata, tusd_data)
    my_disconnect(connection)
    exit(OK)


if __name__ == '_main__':
    run()
