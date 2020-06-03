import requests
from requests.exceptions import HTTPError
import os
import uuid
import json
import logging
import base64
import time
import magic
import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('Could not load dotenv modules or .env file. Ignoring.')


def get_mime(path):
    return magic.from_file(path, mime=True)


def log(endpoint, token, uuid, path, name, mime, condition, message):
    print(f'uuid: {uuid}, path: {path}, name: {name}, mime: {mime}')

    # Note that we need a string, which is why it is encoded as utf.
    with open(path, 'rb') as myfile:
        content = base64.b64encode(myfile.read()).decode('utf-8')

    log_obj = {
        'archuuid': uuid,
        'sender': 'logger.py',
        'time_recorded': datetime.datetime.now().isoformat(),
        'message': message,
        'condition': condition,
        'attachment': content,
        'attachment_mime': mime,
        'attachment_name': name
    }
    response = requests.post(endpoint,
                        headers={'access_token':token},
                        data=json.dumps(log_obj)
                        )

    # Bail if it fails.
    response.raise_for_status()

    logging.info(f'{name} logged OK')
    


def main():
    files = os.getenv('FILES').split(';')
    uuid = os.getenv('UUID')
    condition = os.getenv('CONDITION', 'ok')
    message = os.getenv('MESSAGE', '')
    baseurl = os.getenv('BASEURL', 'http://localhost:8000/')
    endpoint = baseurl + 'ingest'
    token = os.getenv('TOKEN', 'test_token')
    for lfile in files:        
        mime = get_mime(lfile)
        name = os.path.basename(lfile)
        logging.info(f'UUID({uuid}): Logging ({name}), type {mime} to {endpoint}')
        log(endpoint, token, uuid, lfile, name, mime, condition, message)


if __name__ == "__main__":
    main()



