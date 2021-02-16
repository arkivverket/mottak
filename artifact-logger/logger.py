#!/usr/bin/env python
""" This container takes artifacts and logs them to the log-archive service """
# pylint: disable=logging-fstring-interpolation,too-many-arguments

import base64
import datetime
import json
import logging
import os
import uuid

import magic
import requests
from _version import __version__

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print('Could not load python-dotenv. Production assumed.')


def get_mime(path):
    """ Fetches the mine type of a file """
    return magic.from_file(path, mime=True)


def log(endpoint, token, arch_uuid, path, name, mime, condition, message):
    """ Logs to the remote log api """
    print(f'uuid: {arch_uuid}, path: {path}, name: {name}, mime: {mime}')

    # Note that we need a string, which is why it is encoded as utf.
    with open(path, 'rb') as myfile:
        content = base64.b64encode(myfile.read()).decode('utf-8')

    log_obj = {
        'archuuid': arch_uuid,
        'sender': 'logger.py',
        'time_recorded': datetime.datetime.now().isoformat(),
        'message': message,
        'condition': condition,
        'attachment': content,
        'attachment_mime': mime,
        'attachment_name': name
    }
    response = requests.post(endpoint,
                             headers={'access_token': token},
                             data=json.dumps(log_obj)
                             )

    # Bail if it fails.
    response.raise_for_status()

    logging.info(f'{name} logged OK')


def main():
    """ main method. Run from here unless imported"""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info(f'{__file__} version {__version__} running')

    files = os.getenv('FILES').split(';')
    arch_uuid = os.getenv('ARCHIVE_OBJ_ID')
    condition = os.getenv('CONDITION', 'ok')
    message = os.getenv('MESSAGE', '')
    baseurl = os.getenv('BASEURL', 'http://localhost:8000/')
    endpoint = baseurl + 'ingest'
    token = os.getenv('TOKEN', 'test_token')
    for lfile in files:
        mime = get_mime(lfile)
        name = os.path.basename(lfile)
        logging.info(
            f'UUID({uuid}): Logging ({name}), type {mime} to {endpoint}')
        log(endpoint, token, arch_uuid, lfile, name, mime, condition, message)


if __name__ == "__main__":
    main()
