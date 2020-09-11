#!/bin/python3
import logging
import base64
from tusclient import client
import json
import argparse
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="base64 input fra invitasjon", action="store")
parser.add_argument("-r", "--resume", help="resume upload", action="store_true")
args = parser.parse_args()

class Metadata(dict):
    pass

metadata_input = json.loads(base64.b64decode(args.input))
print(metadata_input)
tus_client = client.TusClient(
    url=metadata_input['uploadUrl']
)
metadata = dict({'invitation_id': str(metadata_input['meta']['invitation_id'])})
uploader = tus_client.uploader(file_path=f"{metadata_input['reference']}.{metadata_input['uploadType']}",
                               metadata=metadata,
                               chunk_size=1024*1024*16
                               )
uploader.upload()
print("Upload done.....")

