#!/usr/bin/env python3
import os
import sys
import logging
from av_objectstore import ArkivverketObjectStorage
from _version import __version__

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

SUCCESS = 0
ENVERROR = 1
DELETEERROR = 2

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')

logging.basicConfig(level=logging.INFO, 
                    filemode='w', format='%(asctime)s %(levelname)s %(message)s')
logging.info(f'{__file__} version {__version__} running')

storage = ArkivverketObjectStorage()
if storage.delete(bucket, filename):
    logging.info(f"Object deleted {filename} succesfully from {bucket}")
    sys.exit(SUCCESS)
else:
    logging.error(f"Failed to delete {filename} from {bucket}")
    sys.exit(DELETEERROR)
