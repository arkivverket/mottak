#!/usr/bin/env python3
import os
import sys
import logging
import hashlib
import tarfile
from io import BytesIO
from typing import Optional

from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError


from app.blob import Blob, DEFAULT_BUFFER_SIZE
from app.utils import fix_encoding

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    logger.info("Failed to load dotenv file. Assuming production")

# Constants
METS_FILENAME = "dias-mets.xml"

# Exit values
TAR_ERROR = 10
UPLOAD_ERROR = 11
OBJECTSTORE_ERROR = 12


# ENV variables
source_bucket = os.getenv('SOURCE_BUCKET')  # Also known as a Container in Azure Blob Storage
source_object_name = os.getenv('SOURCE_OBJECT_NAME')
target_bucket_name = os.getenv('TARGET_BUCKET_NAME')
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
max_concurrency = int(os.getenv("MAX_CONCURRENCY", 4))
buffer_size = int(os.getenv("BUFFER_SIZE", DEFAULT_BUFFER_SIZE))
os.getenv("OUTPUT_PATH_LOG", "/tmp/unpack.log")


def upload_file(name: str, handle: Optional[BytesIO], target_bucket: ContainerClient) -> None:
    """Uploades a file to Azure Blob Storage

    :param name: the name of the target object on ABS
    :param handle: bytes buffer of the file
    :param target_bucket: container/bucket to store the file in
    """
    logger.debug(f"Creating {name} in {target_bucket}")
    try:
        blob_client = target_bucket.get_blob_client(blob=name)
        blob_client.upload_blob(handle)
    except Exception as e:
        logger.error(f'Failed to do streaming upload to {target_bucket} / {name}: {e}')
        sys.exit(UPLOAD_ERROR)


def stream_tar(stream: Blob) -> tarfile.TarFile:
    """Takes a Blob stream and opens it as a tarfile
    :param Blob stream: the incoming
    :returns TarFile: opened tarfile ready for interaction
    :raises Exception: if an error is encountered
    """
    try:
        tar_file = tarfile.open(fileobj=stream, mode="r")
    except Exception as exception:
        logging.critical(f"Failed to open stream to object {stream.client.container_name}/{stream.client.blob_name}")
        logging.critical(f"Error: {exception}")
        raise exception
    return tar_file


def unpack_tar(target_bucket: ContainerClient, source_blob: Blob) -> None:
    """Unpacks a tar file from Azure Blob Storage and writes the extracted
    back to an new bucket on Azure Blob Storage

    :param target_bucket: container/bucket to write the unpacked files to
    :param source_blob: the tar file to unpack
    """
    tar_file = stream_tar(source_blob)
    for member in tar_file:
        file_name = fix_encoding(member.name)
        # If it is a directory or if a slash is the last char (root node?)
        if member.isdir() or file_name[-1] == '/':
            # Handle is none - likely a directory.
            logger.info(f'Skipping {file_name} of size {member.size}')
            continue
        # If non directory member isn't a file, logg warning
        elif not member.isfile():
            logger.warning(f"Content {file_name} has not been unpacked because it is not a regular type of file")
            continue
        handle = tar_file.extractfile(member)
        # If member is the mets file, calculate sha256 checksum and log it
        if file_name.endswith(METS_FILENAME):
            checksum = get_sha256(handle)
            logger.info(f'Unpacking {file_name} of size {member.size} with checksum {checksum}')
            continue
        logger.info(f'Unpacking {file_name} of size {member.size}')
        upload_file(name=file_name, handle=handle, target_bucket=target_bucket)


def create_target_bucket(bucket_name: str, blob_service_client: BlobServiceClient) -> ContainerClient:
    """Creates a new bucket on Azure Blob Storage

    :param bucket_name: the name of the new bucket
    :param blob_service_client: A Blob Service Client with the rights to create a new bucket
    :return: a container client of the new bucket
    :raises: ResourceExistsError if the bucket already exists
    """
    try:
        logger.info(f'Creating container {bucket_name}')
        return blob_service_client.create_container(bucket_name)
    except ResourceExistsError as e:
        logger.error(f'Error while creating container {bucket_name}: {e}')
        raise e


def get_source_blob(blob_service_client: BlobServiceClient) -> Blob:
    azure_blob = blob_service_client.get_blob_client(container=source_bucket, blob=source_object_name)
    blob = Blob(azure_blob, max_concurrency, buffer_size)
    logger.info(f"Connected to Azure with API version {blob.client.api_version}")
    return blob


def get_sha256(handle: Optional[BytesIO]) -> str:
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
    logger.info("Starting s3-unpack")
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(conn_str)
    logger.info(f"Unpacking {source_object_name} into container {target_bucket_name}")
    target_bucket = create_target_bucket(target_bucket_name, blob_service_client)
    source_blob = get_source_blob(blob_service_client)
    unpack_tar(target_bucket, source_blob)


if __name__ == "__main__":
    main()
