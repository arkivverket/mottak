#!/usr/bin/env python3
import json
import logging
from typing import TextIO, Optional

import psycopg2
import psycopg2.extras

from hooks.implementations.models.DataFromDatabase import DataFromDatabase
from hooks.implementations.return_codes import DBERROR


def read_tusd_event(step: str, input_data: TextIO, logger) -> dict:
    """ _ stdin and parse the JSON object. Step is given for error reporting.
    Returns a dict based on the JSON input given"""
    data = json.load(input_data)

    # Enable this when debugging the events. It dumps the input to /tmp so you can re-run the hook with stdin.
    # try:
    #     with open(f'/tmp/json-event-{step}.json', 'w') as event_file:
    #         json.dump(data, event_file, sort_keys=True, indent=4)
    # except Exception as exception:
    #     logger.error(f'Error while dumping JSON: {exception}')
    #     # Not really a fatal error. We can continue.
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


def get_data_from_db(conn, invitasjon_ekstern_id: str, logger) -> Optional[DataFromDatabase]:
    """ Fetch metadata about an invitation from the database using the invitation id as key """
    rec = []
    try:
        dict_cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cursor.execute(
            'SELECT i.id            AS invitasjon_id, '
            'i.ekstern_id           AS ekstern_id, '
            'a.sjekksum_sha256      AS sjekksum, '
            'a.avgiver_navn         AS avgiver_navn, '
            'a.avgiver_epost        AS avgiver_epost, '
            'a.koordinator_epost    AS koordinator_epost, '
            'a.type                 AS arkiv_type, '
            'a.id                   AS arkivuttrekk_id, '
            'a.obj_id               AS arkivuttrekk_obj_id '
            'a.storrelse            AS storrelse '
            'FROM invitasjon i LEFT JOIN arkivuttrekk a ON i.arkivuttrekk_id = a.id '
            'WHERE i.ekstern_id =%s', [invitasjon_ekstern_id])
        rec = dict_cursor.fetchall()
        print(rec)
    except psycopg2.Error as exception:
        logger.error(f'Database error: {exception}')
        exit(DBERROR)

    if len(rec) == 0:
        return None
    else:
        return DataFromDatabase.init_from_dict(rec[0])


def my_disconnect(conn):
    conn.close()
