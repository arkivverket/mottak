#!/usr/bin/env python3
from __future__ import with_statement

import hashlib
import logging
import os

from py_objectstore import ArkivverketObjectStorage

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print("Failed to load dotenv file. Assuming production.")
    print(e)

CHECKSUMERROR = 1
ENVERROR = 10
FILEERROR = 11


def object_checksum(obj):
    sha256_hash = hashlib.sha256()
    for byte_block in obj:
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def write_to_file(checksum_result: str, target_path: str):
    with open(target_path, "w") as result_file:
        result_file.write(checksum_result)


def get_object_stream(bucket: str, objectname: str):
    logging.info(f'Opening a streaming connection to {objectname} in {bucket}')
    storage = ArkivverketObjectStorage()
    return storage.download_stream(bucket, objectname)


def main():
    bucket = os.getenv('BUCKET')
    objectname = os.getenv('TUSD_OBJECT_NAME')
    expected_checksum = os.getenv('SJEKKSUM')
    log_path = os.getenv('OUTPUT_PATH_LOG', '/tmp/log')
    summary_path = os.getenv('OUTPUT_PATH_RESULT', '/tmp/result')

    logging.basicConfig(level=logging.INFO, filename=log_path,
                        filemode='w', format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f'Starting s3-checksum256')

    try:
        obj = get_object_stream(bucket, objectname)
    except Exception as e:
        logging.error(f'Error whilst opening stream: {e}')
        exit(FILEERROR)
    try:
        checksum = object_checksum(obj)
    except Exception as e:
        logging.error(f'error caught while streaming/checksumming: {e}')
        exit(FILEERROR)

    if checksum == expected_checksum:
        logging.info(f'Checksum ({checksum}) verified')
        write_to_file('Status etter kontroll av sjekksum: ok', summary_path)
    else:
        logging.warning(f"Expected checksum {expected_checksum} doesn't match calculated {checksum}")
        write_to_file('Status etter kontroll av sjekksum: Ikke ok', summary_path)


if __name__ == "__main__":
    main()
