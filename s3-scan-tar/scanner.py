#!/usr/bin/env python3
""" Scans a tar archive stored in a objectstore """
# pylint: disable=logging-fstring-interpolation

import os
import sys
import logging
import io
import tarfile
from typing import Any
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
import pyclamd

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")

from _version import __version__

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
        while len(self.filehandle.read(1024 ** 2)) > 0:  # read big chunks...
            pass

    def tell(self):
        return self.filehandle.tell()

    def seek(self, pos: Any, **kwargs) -> int:
        raise io.UnsupportedOperation


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


def scan_archive(tar_file, clamd_socket, limit) -> (int, int, int):
    """ Takes a tar_file typically a cloud storage object) and scans
    it. Returns the tuple (clean, virus, skipped)"""
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

            if result is None:
                logging.info(f'clean - {member.name}')
                clean += 1
            else:
                logging.warning(
                    f'Virus found! {result["stream"][1]} in {member.name}')
                virus += 1
            if handle.restricted:
                logging.warning(
                    'Scan was restricted by size limit. Scan incomplete.')
                skipped += 1
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
    return clean, virus, skipped


def main():
    """ Run from here, really """
    logging.basicConfig(level=logging.INFO, filename='/tmp/avlog',
                        filemode='w', format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f'{__file__} version {__version__} running')

    bucket = os.getenv('BUCKET')
    filename = os.getenv('OBJECT')
    # Get the max file size for clamd. Default is 1023 MiB
    scan_limit = int(os.getenv('MAXFILESIZE', '1023')) * 1024 ** 2

    logging.info(f'Intializing scan on {bucket}/{filename} with scan limit {scan_limit} MiB')

    storage = ArkivverketObjectStorage()
    obj = storage.download_stream(bucket, filename)
    file_stream = MakeIterIntoFile(obj)
    # If you wanna test this on local files do something like this:
    # file_stream = open(filename,'br')
    # print("Local File opened:", file_stream)

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
    (clean, virus, skipped) = scan_archive(
        file_stream, clamd_socket, scan_limit)

    logging.info(f"{clean} files scanned and found clean")
    logging.info(f"{virus} viruses found")
    logging.info(f"{skipped} files skipped")
    logging.info("Archive scanned - exiting")


# ===========================================================================
# Run from here.
# ===========================================================================
if __name__ == "__main__":
    main()
