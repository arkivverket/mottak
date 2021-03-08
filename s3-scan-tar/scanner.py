#!/usr/bin/env python3
""" Scans a tar archive stored in a objectstore """
# pylint: disable=logging-fstring-interpolation

import os
import sys
import logging
import io
import tarfile
import socket
import time
from typing import Tuple
from collections import namedtuple
from libcloud.storage.types import ObjectDoesNotExistError
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
import pyclamd

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")

MEGABYTES = 1024 ** 2

# Exit values
CLAMAVERROR = 10


def wait_for_port(port, host='localhost', timeout=5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the port {} on host {} to start accepting '
                                   'connections.'.format(port, host)) from ex


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    There is no try/except here as we want this error to propagate up.
    """
    csock = pyclamd.ClamdUnixSocket()
    csock.ping()
    return csock


def stream_tar(stream):
    """ Takes a stream and created both a tarfile object
    as well as a TarfileIterator using the stream """
    try:
        # @TODO: Check if latin1 encoding will cause issues later down the line
        # Perhaps it is possible to extract a file-list, and check for issues,
        # and then decide on the encoding?
        t_f = tarfile.open(fileobj=stream, mode='r|', encoding='latin1')
        tar_iterator = TarfileIterator(t_f)
    except Exception as exception:
        logging.error(f'Failed to open stream to object {stream}')
        logging.error(f'Error: {exception}')
        raise exception
    return tar_iterator, t_f


def scan_archive(tar_file, clamd_socket, limit) -> Tuple[int, int, int]:
    """ Takes a tar_file typically a cloud storage object) and scans
    it. Returns the named tuple (clean, virus, skipped)"""
    clean, virus, skipped = 0, 0, 0
    tar_stream, tar_file = stream_tar(tar_file)
    for member in tar_stream:
        # The file is larger that the limit
        if member.size > limit:
            logging.warning(f'Skipping {member.name} because it exceeds the {sizeof_fmt(member.size)} file size limit')
            tar_file.next()
            skipped += 1
            continue

        tar_member = tar_file.extractfile(member)
        if tar_member is None:
            # Handle is none - likely a directory.
            logging.debug("Handle is none. Skipping...")
            continue
        try:
            logging.info(f'Scanning {member.name} at {sizeof_fmt(member.size)}...')
            result = clamd_socket.scan_stream(tar_member)

            # No virus found
            if result is None:
                logging.info(f'clean - {member.name}')
                clean += 1
            else:
                logging.warning(
                    f'Virus found! {result["stream"][1]} in {member.name}')
                virus += 1

        except ConnectionResetError:
            logging.error(
                'clamd reset the connection. Increase max scan size for clamd.')
            logging.warning('Flushing the file.')
            tar_file.next()
            logging.warning(f'SKIPPED (File too big) - {member.name}')
            skipped += 1
        except Exception as exception:
            logging.error(f"Failed to scan {member.name}")
            logging.error(f'Error: {exception}')
            raise exception
    logging.debug(f'clean: {clean}, virus: {virus}, skipped: {skipped}')
    ret = namedtuple("scan", ["clean", "virus", "skipped"])
    return ret(clean, virus, skipped)


def main():
    """ Run from here, really """
    logging.basicConfig(level=logging.INFO, filename='/tmp/avlog',
                        filemode='w', format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info("Starting s3-scan-tar")

    bucket = os.getenv('BUCKET')
    objectname = os.getenv('TUSD_OBJECT_NAME')

    # Max file size for ClamAV is 4GiB, or UINT_MAX, or 4294967295 bytes (2^32-1)
    scan_limit = 2**32-1
    logging.info(f'Intializing scan on {bucket}/{objectname} with scan limit {sizeof_fmt(scan_limit)}')

    try:
        storage = ArkivverketObjectStorage()
        obj = storage.download_stream(bucket, objectname)
        object_stream = MakeIterIntoFile(obj)
        # If you wanna test this on local files do something like this:
        # object_stream = open(objectname,'br')
        # print("Local File opened:", object_stream)
    except ObjectDoesNotExistError as exception:
        logging.error(f'An error occured while getting the object handle {objectname}')
        sys.exit(CLAMAVERROR)
    except IOError as exception:
        logging.error(f'An error occuder while loading the file {objectname}')
        sys.exit(CLAMAVERROR)
    except Exception as exception:
        logging.error("Unkown error occured while getting the object")
        logging.error(exception)
        sys.exit(CLAMAVERROR)

    logging.info("Refreshing ClamAV signatures")
    os.system("freshclam -d")

    logging.info("Starting ClamAV")
    os.system("clamd &")

    try:
        logging.info("Waiting for clamd to be ready")
        wait_for_port(3310, timeout=30.0)
    except TimeoutError as exception:
        logging.error(exception)
        sys.exit(CLAMAVERROR)

    try:
        clamd_socket = get_clam()
        clam_ver = clamd_socket.version()
        logging.info(f'Connected to Clamd {clam_ver}')
    except FileNotFoundError as exception:
        logging.error("Could not find a clamd socket")
        logging.error(exception)
        sys.exit(CLAMAVERROR)
    except pyclamd.pyclamd.ConnectionError as exception:
        logging.error("Could not connect to clamd socket")
        logging.error(exception)
        sys.exit(CLAMAVERROR)
    scan_ret = scan_archive(
        object_stream, clamd_socket, scan_limit)

    logging.info(f"{scan_ret.clean} files scanned and found clean")
    logging.info(f"{scan_ret.virus} viruses found")
    logging.info(f"{scan_ret.skipped} files skipped")
    logging.info("Archive scanned - exiting")


# ===========================================================================
# Run from here.
# ===========================================================================
if __name__ == "__main__":
    main()
