#!/usr/bin/env python3
import os
import sys
import logging
import hashlib

import tarfile
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator
from _version import __version__
from io import BufferedReader

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')
uuid = os.getenv('UUID')
ZERO_GENERATION = '0'
target_container = f'{uuid}-{ZERO_GENERATION}'
storage = ArkivverketObjectStorage()

obj = storage.download_stream(bucket, filename)
file_stream = MakeIterIntoFile(obj)


TAR_ERROR = 10
UPLOAD_ERROR = 11
OBJECTSTORE_ERROR = 12

def create_file(name, handle, target_container):
    logging.debug(f"Creating {name} in {target_container}")
    # handle = iter(handle)
    try:
        storage.upload_stream(target_container, name, handle)
    except Exception as e:
        logging.error(f'Failed to do streaming upload to {target_container} / {name}: {e}')
        exit(UPLOAD_ERROR)



def unpack_tar(object_name, target_container):
    try:
        tf = tarfile.open(fileobj=file_stream, mode='r|')
        tfi = TarfileIterator(tf)
    except Exception as e:
        logging.error(f'Failed to open stream to object: {bucket} / {filename}')
        logging.error(f'Error: {e}')
        exit(TAR_ERROR)
    for member in tfi:
        # If it is a directory or if a slash is the last char (root node?)
        if member.isdir() or member.name[-1] == '/':
            # Handle is none - likely a directory.
            logging.info(f'Skipping {member.name} of type {int(member.type)} and size {member.size}')
            continue
        handle = tf.extractfile(member)
        checksum = get_SHA256(handle)
        logging.info(f'Unpacking {member.name} of size {member.size} with checksum {checksum}')
        create_file(name=member.name, handle=handle, target_container= target_container)


def create_target(container_name):
    try:
        logging.info(f'Creating container {container_name}')
        container = storage.create_container(container_name)
        return container
    except Exception as e:
        logging.error(f'While creating container {container_name}: {e}')
        raise(e)
    

def get_SHA256(handle: BufferedReader):
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
    logging.basicConfig(level=logging.INFO, filename='/tmp/unpack.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')
    # Also log to STDERR so k8s understands what is going on.
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f'{__file__} version {__version__} running')
    logging.info(f"Unpacking {filename} into container {target_container}")
    target = create_target(target_container)
    #target = storage.get_container(target_container)
    unpack_tar(filename, target)

if __name__ == "__main__":
    main()
