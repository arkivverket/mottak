import os
import sys
import pathlib
import logging
import requests

BLOB_SAS_TOKEN = 'sp=r&st=2020-09-15T06:00:00Z&se=2020-09-15T14:04:04Z&sip=84.209.175.165&spr=https&sv=2019-12-12&sr=b&sig=cMFXw9Tr6gV0A1q7lJs7wl%2FbxFFdpk3jlBpA8Yd7VhM%3D'
BLOB_SAS_URL = 'https://mottakmvp.blob.core.windows.net/mottak/9ac53268505260cbc78e195693e2335e?sp=r&st=2020-09-15T06:00:00Z&se=2020-09-15T14:04:04Z&sip=84.209.175.165&spr=https&sv=2019-12-12&sr=b&sig=cMFXw9Tr6gV0A1q7lJs7wl%2FbxFFdpk3jlBpA8Yd7VhM%3D'

logging.basicConfig(level=logging.INFO)


def download_blob(sas_url: str):
    azcopy_command = './azcopy/azcopy cp "{}" "local_file.tar" --recursive'.format(sas_url)
    print('Running: {}'.format(azcopy_command))
    os.system(azcopy_command)


def run(sas_url: str):
    download_blob(sas_url)


if __name__ == '__main__':
    # sas_url_arg = sys.argv[1]
    sas_url_arg = BLOB_SAS_URL
    run(sas_url_arg)
