#!/usr/bin/env python3
import json
import psycopg2
import psycopg2.extras
import logging

from typing import TextIO

from .return_codes import DBERROR, JSONERROR


def read_tusd_event(step: str, input_data: TextIO, logger) -> dict:
    """ _ stdin and parse the JSON object. Step is given for error reporting.
    Returns a dict based on the JSON input given"""
    data = json.load(input_data)

    # Enable this when debugging the events. It dumps the input to /tmp so you can re-run the hook with stdin.
    try:
        with open(f'/tmp/json-event-{step}.json', 'w') as event_file:
            json.dump(data, event_file, sort_keys=True, indent=4)
    except Exception as exception:
        logger.error(f'Error while dumping JSON: {exception}')
        # Not really a fatal error. We can continue.
    logging.info(f'Got {step} data: {data}')
    return data


def my_connect(dbstring: str, logger):
    try:
        connection = psycopg2.connect(dbstring)
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error while connecting to PostgreSQL: {error}")
        raise (error)
    finally:
        return connection


def get_metadata(conn, invitasjon_ekstern_id: str, logger):
    """ Fetch metadata about an invitation from the database using the invitation id as key """
    try:
        dict_cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cursor.execute(
            'SELECT i.id            AS id, '
            'i.ekstern_id           AS uuid, '
            'a.sjekksum_sha256      AS checksum, '
            'false                  AS is_sensitive, '
            'a.avgiver_navn         AS name, '
            'a.avgiver_epost        AS email, '
            'a.type                 AS type, '
            'a.id                   AS arkivuttrekk_id, '
            'a.storrelse            AS storrelse '
            'FROM invitasjon i LEFT JOIN arkivuttrekk a ON i.arkivuttrekk_id = a.id '
            'WHERE i.ekstern_id =%s', (invitasjon_ekstern_id))
        rec = dict_cursor.fetchall()
        print(rec)
    except psycopg2.Error as exception:
        logger.error(f'Database error: {exception}')
        exit(DBERROR)

    if len(rec) == 0:
        return None
    else:
        return rec[0]


def my_disconnect(conn):
    conn.close()


def extract_filename_from_hook(tusd_data: dict):
    # Verify that we have a filename:
    try:
        return tusd_data['Upload']['Storage']['Key']
    except KeyError:
        logging.error("Could not find key/filename in JSON. Dumping JSON:")
        logging.error(json.dumps(tusd_data, indent=4, sort_keys=True))
        exit(JSONERROR)


def extract_size_in_bytes_from_hook(tusd_data: dict):
    # Verify that we have a filename:
    try:
        return tusd_data['Upload']['Size']  # Total size of upload in bytes
    except KeyError:
        logging.error("Could not find key/Size in JSON. Dumping JSON:")
        logging.error(json.dumps(tusd_data, indent=4, sort_keys=True))
        exit(JSONERROR)


def extract_tusd_id_from_hook(tusd_data: dict):
    # Verify that we have a filename:
    try:
        return tusd_data['Upload']['ID']  # Total size of upload in bytes
    except KeyError:
        logging.error("Could not find key/Size in JSON. Dumping JSON:")
        logging.error(json.dumps(tusd_data, indent=4, sort_keys=True))
        exit(JSONERROR)
