import os
import sys
import pathlib
import logging
import requests

BLOB_SAS_TOKEN = 'sp=r&st=2020-09-15T06:00:00Z&se=2020-09-15T14:04:04Z&sip=84.209.175.165&spr=https&sv=2019-12-12&sr=b&sig=cMFXw9Tr6gV0A1q7lJs7wl%2FbxFFdpk3jlBpA8Yd7VhM%3D'
BLOB_SAS_URL = 'https://mottakmvp.blob.core.windows.net/mottak/9ac53268505260cbc78e195693e2335e?sp=r&st=2020-09-15T06:00:00Z&se=2020-09-15T14:04:04Z&sip=84.209.175.165&spr=https&sv=2019-12-12&sr=b&sig=cMFXw9Tr6gV0A1q7lJs7wl%2FbxFFdpk3jlBpA8Yd7VhM%3D'
logging.basicConfig(level=logging.INFO)


class Platform:
    def __init__(self, platform_str):
        self.platform = platform_str
        if platform_str == 'darwin':  # OSX
            self.azcopy_url = 'https://aka.ms/downloadazcopy-v10-mac'
        elif platform_str == 'linux':  # LINUX
            self.azcopy_url = 'https://aka.ms/downloadazcopy-v10-linux'
        else:
            logging.error("Unsupported operating system {}".format(platform_str))
            sys.exit(1)


def finds_azcopy() -> bool:
    return pathlib.Path('azcopy').is_file()


def download_and_unpack_azcopy(platform: Platform):
    logging.info("Will download azcopy for {}".format(platform.platform))
    resp = requests.get(platform.azcopy_url, allow_redirects=True)
    if not resp.ok:
        logging.error('Failed to download azcopy, got: {} {}'.format(resp.status_code, resp.reason))
        sys.exit(1)
    filename = resp.url.split('/')[-1]
    open(filename, 'wb').write(resp.content)
    if filename.endswith('.zip'):
        os.system('unzip -j {}'.format(filename))
    elif filename.endswith('.tar.gz'):
        os.system('tar --strip-components=1 -zxvf {}'.format(filename))
    os.system('rm {}'.format(filename))


def download_blob(sas_url: str):
    azcopy_command = './azcopy cp "{}" "local_file.tar"'.format(sas_url)
    print('Running: {}'.format(azcopy_command))
    os.system(azcopy_command)


def run(sas_url: str):
    platform = Platform(sys.platform)
    if not finds_azcopy():
        logging.info("azcopy not found")
        download_and_unpack_azcopy(platform)
    download_blob(sas_url)


if __name__ == '__main__':
    # sas_url_arg = sys.argv[1]
    sas_url_arg = BLOB_SAS_URL
    run(sas_url_arg)
