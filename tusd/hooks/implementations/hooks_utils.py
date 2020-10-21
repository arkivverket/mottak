#!/usr/bin/env python3
import json
import psycopg2
import psycopg2.extras
import re

from typing import TextIO

from .return_codes import DBERROR


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
    return data


def my_connect(connection_str: str, logger):
    try:
        connection = psycopg2.connect(connection_str)
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error while connecting to PostgreSQL: {error}")
        raise(error)
    finally:
        return connection


def get_metadata(conn, invitation_id: str, logger):
    """ Fetch metadata about an invitation from the database using the invitation id as key """
    try:
        dict_cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cursor.execute('SELECT invitations.id, uuid, checksum, is_sensitive, name, email, type '
                            'FROM invitations, archive_types '
                            'WHERE archive_type_id=archive_types.id '
                            'AND invitations.id=%s', (invitation_id))
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
