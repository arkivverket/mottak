#!/usr/bin/env python3
import os
import sys
import logging
import hashlib
import tarfile

from io import BufferedReader
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
from _version import __version__

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

# Constants
LOG_PATH = '/tmp/unpack.log'
ZERO_GENERATION = '0'
METS_FILENAME = "dias-mets.xml"

TAR_ERROR = 10
UPLOAD_ERROR = 11
OBJECTSTORE_ERROR = 12

# Environment variables
MANDATORY_ENV_VARS = ['BUCKET', 'OBJECT', 'UUID']
for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError(f"Failed because {var} is not set in .env")

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')
uuid = os.getenv('UUID')

# Global variables
storage = ArkivverketObjectStorage()

def create_file(name, handle, target_container):
    logging.debug(f"Creating {name} in {target_container}")
    try:
        storage.upload_stream(target_container, name, handle)
    except Exception as e:
        logging.error(f'Failed to do streaming upload to {target_container} / {name}: {e}')
        sys.exit(UPLOAD_ERROR)


def unpack_tar(target_container):
    try:
        obj = storage.download_stream(bucket, filename)
        file_stream = MakeIterIntoFile(obj)
        tf = tarfile.open(fileobj=file_stream, mode='r|')
        tfi = TarfileIterator(tf)
    except Exception as e:
        logging.error(f'Failed to open stream to object: {bucket} / {filename}')
        logging.error(f'Error: {e}')
        sys.exit(TAR_ERROR)
    for member in tfi:
        # If it is a directory or if a slash is the last char (root node?)
        if member.isdir() or member.name[-1] == '/':
            # Handle is none - likely a directory.
            logging.info(f'Skipping {member.name} of size {member.size}')
            continue
        # If non directory member isn't a file, logg warning
        elif not member.isfile():
            logging.warning(f"Content {member.name} has not been unpacked because it is not a regular type of file")
            continue
        handle = tf.extractfile(member)
        # If member is the mets file, calculate sha256 checksum and log it
        if member.name.endswith(METS_FILENAME):
            checksum = get_sha256(handle)
            logging.info(f'Unpacking {member.name} of size {member.size} with checksum {checksum}')
            continue
        logging.info(f'Unpacking {member.name} of size {member.size}')
        create_file(name=member.name, handle=handle, target_container=target_container)


def create_target(container_name):
    try:
        logging.info(f'Creating container {container_name}')
        container = storage.create_container(container_name)
        return container
    except Exception as e:
        logging.error(f'While creating container {container_name}: {e}')
        raise e


def get_sha256(handle: BufferedReader):
    """
    Get SHA256 hash of the file, directly in memory
    """
    sha = hashlib.sha256()
    byte_array = bytearray(128 * 1024)
    memory_view = memoryview(byte_array)

    for n in iter(lambda: handle.readinto(memory_view), 0):
        sha.update(memory_view[:n])

    return sha.hexdigest()


def main():
    logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s')
    # Also log to STDERR so k8s understands what is going on.
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f'{__file__} version {__version__} running')

    target_container_name = f'{uuid}-{ZERO_GENERATION}'
    logging.info(f"Unpacking {filename} into container {target_container_name}")
    target_container = create_target(target_container_name)
    # target_container = storage.get_container(target_container_name)
    unpack_tar(target_container)

if __name__ == "__main__":
    main()
