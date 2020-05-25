#!/usr/bin/env python3

# This creates /tmp/dias-mets.xml so we can feed this into Arkade

import os                               # for getenv
import psycopg2
import psycopg2.extras


import logging
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('Dotenv not loaded.')

UUIDERROR = 1  # invalid UUID
DBERROR = 10


def create_db_access(dbstring):
    """Create a psycopg2 compatible object from the connection string.
    The string is from PHP and we reuse it here
    """
    mystr = dbstring[6:]
    mystr = mystr.rstrip()
    d = dict(re.findall(r'(\w+)=([^;]+);?', mystr))
    # Validate dbstring:
    for key in ['user', 'password', 'host', 'dbname']:
        if key not in d.keys():
            logging.error('%s not found in DBSTRING' % key)
            exit(DBERROR)
    return d

def my_connect(conn_info):
    try:
        connection = psycopg2.connect(user=conn_info['user'],
                                      host=conn_info['host'],
                                      dbname=conn_info['dbname'],
                                      password=conn_info['password'],
                                      connect_timeout=10)

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")
        exit(DBERROR)
    finally:
        return connection

def get_mets(conn, iid):
    try:
        dict_cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cursor.execute('SELECT contents '
                            'FROM mets_files '
                            'WHERE invitation_id=%s', (iid,))
        rec = dict_cursor.fetchall()
    except psycopg2.Error as e:
        logging.error(f'SQL Query error: {e}')
        exit(DBERROR)

    if len(rec) == 0:
        return None
    else:
        return rec[0]['contents']

iid = os.getenv('INVITATIONID')
dsn = os.getenv('DBSTRING')
conn_info = create_db_access(dsn)
conn = my_connect(conn_info)

mets = get_mets(conn, iid)
if not mets:
    raise("Invitation not found")

with open('/tmp/dias-mets.xml', 'w') as metsfh:
    print(mets, file=metsfh)
