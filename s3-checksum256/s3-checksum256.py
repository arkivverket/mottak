#!/usr/bin/env python3
from __future__ import with_statement

import os
import sys
import logging
import hashlib
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

RESULT = '/tmp/result'
LOG = '/tmp/checksum.log'

def object_checksum(obj):
    sha256_hash = hashlib.sha256()
    try:
        for byte_block in obj:
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f'error caught while streaming/checksumming: {e}')

def write_result(res):
    with open(RESULT, "w") as res_file:
        res_file.write(res)

def get_object_stream():
    bucket = os.getenv('BUCKET')
    filename = os.getenv('OBJECT')
    logging.info(f'Opening a streaming connection to {filename} in {bucket}')    
    storage = ArkivverketObjectStorage()
    return storage.download_stream(bucket, filename)


def main():
        
    logging.basicConfig(level=logging.INFO, filename=LOG,
                        filemode='w', format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    try:
        obj = get_object_stream()
    except Exception as e:
        logging.error(f'Error whilst opening stream: {e}')
        exit(FILEERROR)
    checksum = object_checksum(obj)
    expected = os.getenv('CHECKSUM')
    if checksum == expected:
        logging.info(f'Checksum ({checksum}) verified')
        write_result('ok')
    else:
        logging.warning(f"Expected checksum {expected} doesn't match calculated {checksum}")
        write_result('mismatch')
        exit(CHECKSUMERROR)

if __name__ == "__main__":
    main()
