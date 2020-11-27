import json
import base64
from tusclient import client


invitation_string = 'eyJyZWZlcmVuY2UiOiAiZWQ4ODlmZGMtYjRkMC00OWZlLWJmNGItY2FhMDgzNGNhYjJkIiwgInVwbG9hZFVybCI6ICJodHRwczovL21vdHRhay5wbGF0dGZvcm0uYXJraXZ2ZXJrZXQuZGV2L3R1c2QiLCAidXBsb2FkVHlwZSI6ICJ0YXIiLCAibWV0YSI6IHsiaW52aXRhc2pvbkVrc3Rlcm5JZCI6ICI4ZGU3NWMwNS03NDRkLTQ2MjItYWYzOC1mYWQ1YjZmMWRjMzAifX0='
tusd_url = 'https://mottak.plattform.arkivverket.dev/tusd/files/'
file_name = '../../../../eksempel-arkiv/large/ed889fdc-b4d0-49fe-bf4b-caa0834cab2d.tar'
chunk_size_in_bytes = 4096

prefix_dev = 'dpldrdev://'
prefix = 'dpldr://'


def convert_to_dict(base64_str: str) -> dict:
    inv_str = str(base64.standard_b64decode(base64_str), 'utf-8')
    return json.loads(inv_str)


def upload(path_to_file: str, metadata: dict, chunk_size_bytes):
    print(f'Creating tus client with url {tusd_url}')
    tus_client = client.TusClient(tusd_url)
    print(f'Creating uploader with chunk size {chunk_size_bytes} and metadata {metadata}')
    uploader = tus_client.uploader(path_to_file, chunk_size=chunk_size_bytes, metadata=metadata)
    print(f'Starting upload of {file_name}')
    uploader.upload()
    print('Upload done')


if __name__ == '__main__':
    json_dict = convert_to_dict(invitation_string)
    upload(file_name, json_dict['meta'], chunk_size_in_bytes)
