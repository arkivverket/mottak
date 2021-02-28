#!/usr/bin/env python3
""" Scans a tar archive stored in a objectstore """
# pylint: disable=logging-fstring-interpolation

import os
import sys
import logging
import io
import tarfile
from typing import Tuple
from collections import namedtuple
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
import pyclamd

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")

from _version import __version__

MEGABYTES = 1024 ** 2

# Exit values
CLAMAVERROR = 10


class BinaryFileLimitedOnSize(io.RawIOBase):
    """ Subclassing the file/RawIOBase class to impose limits on file size by returning short reads
    when we cross the limit. Used to handle the 4GB limit in clamav."""

    def __init__(self, filehandle, maxsize=None):
        super().__init__()
        self.maxsize = maxsize
        self.filehandle = filehandle
        self.restricted = False

    def write(self, s) -> int:
        raise NotImplementedError("write() not supported")

    def read(self, read_length: int) -> bytes:
        if self.maxsize:
            if not read_length:
                # no lenght given, not sure we if can read this without going over the limit
                raise NotImplementedError("Unlimited read requested. Not supported")
            if self.filehandle.tell() + read_length > self.maxsize:
                logging.warning(
                    "Restricting file object and discarding the rest of the contents")
                self.restricted = True
                self.read_flush()
                return b''
        return self.filehandle.read(read_length)

    def read_flush(self):
        """ Read and discard the rest of the file. """
        while len(self.filehandle.read(MEGABYTES)) > 0:  # read big chunks...
            pass

    def tell(self):
        return self.filehandle.tell()

    def seek(self, pos: int, **kwargs) -> int:
        raise io.UnsupportedOperation

# TODO - Use parameters instead of environment variables in functions
def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    There is no try/except here as we want this error to propagate up.
    """
    socket = os.getenv('CLAMD_SOCK', default='/var/run/clamav/clamd.ctl')
    csock = pyclamd.ClamdUnixSocket(socket)
    csock.ping()
    return csock


def stream_tar(stream):
    """ Takes a stream and created both a tarfile object
    as well as a TarfileIterator using the stream """
    if stream is None:
        logging.error("Could not open file.")
        raise Exception('Could not get object handle')
    try:
        t_f = tarfile.open(fileobj=stream, mode='r|')
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
        tar_member = tar_file.extractfile(member)
        if tar_member is None:
            # Handle is none - likely a directory.
            logging.debug("Handle is none. Skipping...")
            continue
        handle = BinaryFileLimitedOnSize(tar_member, limit)
        try:
            logging.info(f'Scanning {member.name}...')
            result = clamd_socket.scan_stream(handle)

            # No virus found
            if result is None:
                # but the scan was not completed.
                if handle.restricted:
                    logging.warning(
                        'Scan was restricted by size limit. Scan incomplete.')
                    skipped += 1
                else:
                    # the scan WAS completed
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
            handle.read_flush()
            logging.warning(f'SKIPPED (File to big) - {member.name}')
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
    logging.info(f'{__file__} version {__version__} running')

    bucket = os.getenv('BUCKET')
    objectname = os.getenv('TUSD_OBJECT_NAME')
    # Get the max file size for clamd. Default is 1023 MiB
    scan_limit = int(os.getenv('MAXFILESIZE', '1023')) * MEGABYTES  # TODO Find out why the limit is 1023?

    logging.info(f'Intializing scan on {bucket}/{objectname} with scan limit {scan_limit} MiB')

    storage = ArkivverketObjectStorage()
    obj = storage.download_stream(bucket, objectname)
    object_stream = MakeIterIntoFile(obj)
    # If you wanna test this on local files do something like this:
    # object_stream = open(objectname,'br')
    # print("Local File opened:", object_stream)

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
