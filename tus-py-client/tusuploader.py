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


# file_path='/Volumes/Untitled/Arkadepakke-85ec069e-f41b-42f1-8c78-7b0c1faebe69/85ec069e-f41b-42f1-8c78-7b0c1faebe69.tar',
uploader = tus_client.uploader(file_path=f"{metadata_input['reference']}.{metadata_input['uploadType']}",
                               metadata=metadata,
                               chunk_size=1024*1024*16
                               )
uploader.upload()
print("Upload done.....")


#{'reference': 'c17b9be8-493f-47b8-bf5b-65840d8523d2',
# 'uploadUrl': 'https://tusd.mottak.arkivverket.dev/files',
# 'uploadType': 'tar',
# 'meta': {'invitation_id': 4}}
