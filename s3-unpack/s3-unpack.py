#!/usr/bin/env python3
import os
import sys
import logging
import hashlib
import tarfile

from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

# Constants
LOG_PATH = '/tmp/unpack.log'
METS_FILENAME = "dias-mets.xml"

TAR_ERROR = 10
UPLOAD_ERROR = 11
OBJECTSTORE_ERROR = 12

# Environment variables
MANDATORY_ENV_VARS = ['BUCKET', 'TUSD_OBJECT_NAME', 'TARGET_BUCKET_NAME']
for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError(f"Failed because {var} is not set in .env")

bucket = os.getenv('BUCKET')
objectname = os.getenv('TUSD_OBJECT_NAME')
target_bucket_name = os.getenv('TARGET_BUCKET_NAME')

# Global variables
storage = ArkivverketObjectStorage()


def create_file(name, handle, target_container):
    logging.debug(f"Creating {name} in {target_container}")
    try:
        storage.upload_stream(target_container, name, handle)
    except Exception as e:
        logging.error(f'Failed to do streaming upload to {target_container} / {name}: {e}')
        sys.exit(UPLOAD_ERROR)


def stream_tar(stream):
    """ Takes an stream and created both a tarfile object
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


def unpack_tar(target_container):
    obj = storage.download_stream(bucket, objectname)
    file_stream = MakeIterIntoFile(obj)
    tar_iterator, tar_file = stream_tar(file_stream)

    for member in tar_iterator:
        # If it is a directory or if a slash is the last char (root node?)
        if member.isdir() or member.name[-1] == '/':
            # Handle is none - likely a directory.
            logging.info(f'Skipping {member.name} of size {member.size}')
            continue
        # If non directory member isn't a file, logg warning
        elif not member.isfile():
            logging.warning(f"Content {member.name} has not been unpacked because it is not a regular type of file")
            continue
        handle = tar_file.extractfile(member)
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
        logging.error(f'Error while creating container {container_name}: {e}')
        raise e


def get_sha256(handle):
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
    logging.info("Starting s3-unpack")

    logging.info(f"Unpacking {objectname} into container {target_bucket_name}")
    target_container = create_target(target_bucket_name)
    unpack_tar(target_container)


if __name__ == "__main__":
    main()
