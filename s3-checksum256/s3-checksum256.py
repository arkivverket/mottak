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

ENVERROR = 1
FILEERROR = 2

RESULT = '/tmp/result'

def checksum(obj):
    sha256_hash = hashlib.sha256()

    for byte_block in obj:
        sha256_hash.update(byte_block)
    try:
        with open(RESULT, "w") as res_file:
            checksum = sha256_hash.hexdigest()
            expected = os.getenv('CHECKSUM')
            if (checksum == expected):
                print("ok", file=res_file)
                print(f"Expected checksum '{expected}' matched {checksum}")
            else:
                print("error", file=res_file)
                print(
                    f"Checksum mismatch. Expected'{expected}' - got {checksum}")

    except EnvironmentError as e:
        logging.error("Failed to open %s: %s" % (RESULT, e))
        exit(FILEERROR)


bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')

storage = ArkivverketObjectStorage()
obj = storage.download_stream(bucket, filename)


if checksum(obj):
    sys.exit(1)
else:
    sys.exit(0)
