import os
import sys
import pathlib
import logging
import requests

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
        os.system('unzip -j {}'.format(filename))  # Unpacks in current folder
        # os.system('unzip {}'.format(filename))
    elif filename.endswith('.tar.gz'):
        os.system('tar --strip-components=1 -zxvf {}'.format(filename))  # Unpacks in current folder
        # os.system('tar -zxvf {}'.format(filename))
    os.system('rm {}'.format(filename))


def download_blob(sas_url: str):
    azcopy_command = './azcopy cp "{}" "local_file.tar" --recursive'.format(sas_url)
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
