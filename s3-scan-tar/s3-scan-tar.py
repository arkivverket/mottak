#!/usr/bin/env python3
import os
import sys
import logging
import io
import tarfile
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
import pyclamd
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

from _version import __version__


# Exit values

CLAMAVERROR = 10

class BinaryFileLimitedOnSize(io.RawIOBase):
    """ Subclassing the file/RawIOBase class to impose limits on file size by throwing EOF Exception
    when we cross the limit.Used to handle the 4GB limit in clamav."""
    def __init__(self, fh, maxsize=None):
        self.maxsize = maxsize
        self.fh = fh

    def write(self, s) -> int:
        if self.maxsize and self.fh.tell() + len(s) > self.maxsize:
            raise(EOFError("write would cross maxsize boundry"))
        return self.fh.write(s)

    def read(self, read_length) -> bytes:
        if self.maxsize:
            if not read_length:
                # no lenght given, not sure we if can read this without going over the limit
                raise(EOFError("Unlimited read requested. Not supported"))
            if self.fh.tell() + read_length >= self.maxsize:
                raise(EOFError("read would cross maxsize boundry"))
            else:
                return self.fh.read(read_length)
    
    def tell(self):
        return self.fh.tell()
    
    def seek(self, pos):
        raise(io.UnsupportedOperation)


def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    There is no try/except here as we won't this error to propagate up.
    """
    socket = os.getenv('CLAMD_SOCK', default='/var/run/clamav/clamd.ctl')
    csock = None
    csock = pyclamd.ClamdUnixSocket(socket)
    csock.ping()
    return csock

# ===========================================================================
# Run from here.
# ===========================================================================

logging.basicConfig(level=logging.INFO)
logging.info(f'{__file__} version {__version__} running')

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')
avlogfile = os.getenv('AVLOG', default='/tmp/avlog')

storage = ArkivverketObjectStorage()
obj = storage.download_stream(bucket, filename)
file_stream = MakeIterIntoFile(obj)


# If you wanna test this on local files do something like this:
#file_stream = open(filename,'br')
#print("Local File opened:", file_stream)

if file_stream is None:
    logging.error("Could not open file.")
    raise Exception('Could not get object handle')

tfi = None
try:
    tf = tarfile.open(fileobj=file_stream, mode='r|')
    mytfi = TarfileIterator(tf)
    tfi = iter(mytfi)
except Exception as exception:
    logging.error(f'Failed to open stream to object: {bucket} / {filename}')
    logging.error(f'Error: {exception}')
    raise exception

cd = None
try:
    cd = get_clam()
    cver = cd.version()
except Exception as exception:
    logging.error(f'Could not connect to clam: {exception}')
    exit(CLAMAVERROR)

print(f'Intializing scan on {bucket}/{filename} using {cver}')

virus = 0
skipped = 0

with open(avlogfile,mode='w') as avlog:
    print(f'{__file__} version {__version__} running', file=avlog)
    for member in tfi:
        tar_member =  tf.extractfile(member)
        if tar_member == None:
            # Handle is none - likely a directory.
            print("Handle is none. Skipping...")
            continue
        handle = BinaryFileLimitedOnSize(tar_member, 1024**3)
        # print(handle.read())
        try:
            result = cd.scan_stream(handle)
            if (result is None):
                print(f'OK - {member.name}', file=avlog)
            else:
                print(f'Virus found! {result["stream"][1]} in {member.name}', file=avlog)
                virus += 1
        except EOFError as exception:
            print(f'SKIPPED (File to big) - {member.name}', file=avlog)
            skipped += 1
        except Exception as e:
            logging.error(f"Failed to scan {member.name}")
            logging.error(f'Error: {e}')
            raise(e)
    print("========", file=avlog)
    print(f"{virus} viruses found", file=avlog)
    print(f"{skipped} files skipped", file=avlog)
    print(f"Archive scanned. Log created as {avlogfile}")





