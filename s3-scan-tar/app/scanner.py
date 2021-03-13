#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scans a tar archive stored in a objectstore """

import os
import sys
import logging
import tarfile

from collections import namedtuple
from libcloud.storage.types import ObjectDoesNotExistError
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
from pyclamd import ClamdUnixSocket
from pyclamd.pyclamd import ConnectionError
from typing import Any, Tuple
from app.utils import sizeof_fmt, wait_for_port, fix_encoding

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")

MEGABYTES = 1024 ** 2
UINT_MAX = 2**32-1

# Exit values
UNKNOWNERROR = 1
AZUREERROR = 2
OBJECTERROR = 3
CLAMAVERROR = 10


def stream_tar(stream) -> Tuple[Any, tarfile.TarFile]:
    """ Takes a stream and created both a tarfile object
    as well as a TarfileIterator using the stream """
    try:
        t_f = tarfile.open(fileobj=stream, mode='r|')
        tar_iterator = TarfileIterator(t_f)
    except Exception as exception:
        logging.critical(f'Failed to open stream to object {stream.client.container_name}/{stream.client.blob_name}')
        logging.critical(f'Error: {exception}')
        raise exception
    return tar_iterator, t_f


def scan_archive(tar_file, clamd_socket: ClamdUnixSocket) -> Tuple[int, int, int]:
    """ Takes a tar_file typically a cloud storage object) and scans
    it. Returns the named tuple (clean, virus, skipped)"""
    clean, virus, skipped = 0, 0, 0
    tar_stream, tar_file = stream_tar(tar_file)

    # By using continue, we technically use the tarfile.next() function via the TarfileIterator wrapper
    for member in tar_stream:
        file_name = fix_encoding(member.name)
        # The file is larger that the limit
        if member.size > UINT_MAX:
            skipped += 1
            logging.warning(
                f'Skipping {file_name} ({sizeof_fmt(member.size)}) because it exceeds the {sizeof_fmt(UINT_MAX)} size limit'
            )
            continue

        tar_member = tar_file.extractfile(member)
        if tar_member is None or member.size == 0:
            # Handle is none - likely a directory.
            logging.debug(f"Handle ({file_name}) is none. Skipping...")
            continue
        try:
            logging.info(
                f'Scanning {file_name} at {sizeof_fmt(member.size)}...')
            result = clamd_socket.scan_stream(tar_member)

            # No viruses found
            if result is None:
                clean += 1
                logging.info(f'clean - {file_name}')
            else:
                virus += 1
                logging.critical(
                    f'Virus found! {result["stream"][1]} in {file_name}')

        except ConnectionResetError:
            skipped += 1
            logging.error(
                'clamd reset the connection. Increase max scan size for clamd.')
            logging.warning(f'SKIPPED (File too big) - {file_name}')
            continue
        except Exception as exception:
            logging.error(f"Failed to scan {file_name}")
            logging.error(f'Error: {exception}')
            raise exception

    logging.debug(f'clean: {clean}, virus: {virus}, skipped: {skipped}')
    ret = namedtuple("scan", ["clean", "virus", "skipped"])
    return ret(clean, virus, skipped)


def main():
    """ Run from here, really """
    logging.basicConfig(level=logging.INFO, filename='/tmp/avlog', filemode='w',
                        format='%(asctime)s | %(levelname)s | %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Starting s3-scan-tar")

    # Also known as a Contaienr in Azure Blob Storage
    bucket = os.getenv('BUCKET')
    objectname = os.getenv('TUSD_OBJECT_NAME')

    # Test the access to the object stream, so we can return early if there are any issues
    logging.info('Initialising connection to Azure Blob Storage')
    try:
        storage = ArkivverketObjectStorage()
        obj = storage.download_stream(bucket, objectname)
        object_stream = MakeIterIntoFile(obj)
        # If you wanna test this on local files do something like this:
        # object_stream = open(objectname,'br')
        # print("Local File opened:", object_stream)
    except ObjectDoesNotExistError:
        logging.critical(f'An error occured while getting the object handle {objectname} in bucket {bucket}')
        sys.exit(OBJECTERROR)
    except IOError:
        logging.critical(f'An error occuder while loading the file {objectname}')
        sys.exit(OBJECTERROR)
    except Exception as exception:
        logging.critical("Unkown error occured while getting the object")
        logging.critical(exception)
        sys.exit(UNKNOWNERROR)

    # Starts freshclamd daemon, which allows the databases to be updated while running, if the scanning takes a while
    logging.info("Refreshing ClamAV signatures")
    os.system("freshclam -d")

    # Starts clamd in the background (eventhough we run clamd in the foreground)
    logging.info("Starting ClamAV")
    os.system("clamd &")

    logging.info('Initialising connection to clamd')
    try:
        wait_for_port(3310)
        clamd_socket = ClamdUnixSocket()
        logging.info(f'Connected to clamd version {clamd_socket.version()}')
    except TimeoutError as exception:
        logging.critical(exception)
        sys.exit(CLAMAVERROR)
    except FileNotFoundError as exception:
        logging.critical("Could not find a clamd socket")
        logging.critical(exception)
        sys.exit(CLAMAVERROR)
    except ConnectionError as exception:
        logging.critical("Could not connect to clamd socket")
        logging.critical(exception)
        sys.exit(CLAMAVERROR)

    logging.info(f'Initialising scan on {bucket}/{objectname} with a scan limit of {sizeof_fmt(UINT_MAX)}')
    scan_ret = scan_archive(object_stream, clamd_socket)

    logging.info(f"{scan_ret.clean} files scanned and found clean")
    logging.info(f"{scan_ret.virus} viruses found")
    logging.info(f"{scan_ret.skipped} files skipped")
    logging.info("Archive scanned - exiting")


# ===========================================================================
# Run from here.
# ===========================================================================
if __name__ == "__main__":
    main()
