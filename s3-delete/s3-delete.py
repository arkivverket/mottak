#!/usr/bin/env python3
import os
import sys
import logging
from av_objectstore import ArkivverketObjectStorage

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

SUCCESS = 0
ENVERROR = 1
DELETEERROR = 2

bucket = os.getenv('BUCKET')
objectname = os.getenv('TUSD_OBJECT_NAME')

logging.basicConfig(level=logging.INFO,
                    filemode='w', format='%(asctime)s %(levelname)s %(message)s')
logging.info("Starting s3-delete")

storage = ArkivverketObjectStorage()
if storage.delete(bucket, objectname):
    logging.info(f"Object {objectname} deleted succesfully from {bucket}")
    sys.exit(SUCCESS)
else:
    logging.error(f"Failed to delete {objectname} from {bucket}")
    sys.exit(DELETEERROR)
