import json
import base64
from tusclient import client


tusd_url = 'https://mottak.plattform.arkivverket.dev/tusd/files/'
file_name = '../../../../eksempel-arkiv/large/ed889fdc-b4d0-49fe-bf4b-caa0834cab2d.tar'
# 16 MiB = 16777216 bytes
# 1 MiB = 1048576 bytes
chunk_size_in_bytes = 1048576


prefix_dev = 'dpldrdev://'
prefix = 'dpldr://'

invitation = {
    "reference": "ed889fdc-b4d0-49fe-bf4b-caa0834cab2d",
    "uploadUrl": "https://mottak.plattform.arkivverket.dev/tusd/files",
    "uploadType": "tar",
    "meta": {
        # Replace this with an UUID from the "invitasjon" table
        "invitasjonEksternId": "3d4a64c4-c187-4e64-8f28-1f4a8b775b2e"
    }
}


def upload(path_to_file: str, metadata: dict, chunk_size_bytes):
    print(f'Creating tus client with url {tusd_url}')
    tus_client = client.TusClient(tusd_url)
    print(f'Creating uploader with chunk size {chunk_size_bytes} and metadata {metadata}')
    uploader = tus_client.uploader(path_to_file, chunk_size=chunk_size_bytes, metadata=metadata)
    print(f'Starting upload of {file_name}')
    uploader.upload()
    print('Upload done')


if __name__ == '__main__':
    upload(file_name, invitation['meta'], chunk_size_in_bytes)
