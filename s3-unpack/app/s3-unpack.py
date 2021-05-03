#!/usr/bin/env python3
import os
import logging
import tarfile

from azure.storage.blob import BlobServiceClient, ContainerClient


from app.abs import create_target_bucket, get_source_blob, upload_file, get_blob_service_client
from app.blob import Blob, DEFAULT_BUFFER_SIZE
from app.utils import fix_encoding, get_sha256


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


# ENV variables
source_bucket = os.getenv('SOURCE_BUCKET')  # Also known as a Container in Azure Blob Storage
source_object_name = os.getenv('SOURCE_OBJECT_NAME')
target_bucket_name = os.getenv('TARGET_BUCKET_NAME')
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
max_concurrency = int(os.getenv("MAX_CONCURRENCY", 4))
buffer_size = int(os.getenv("BUFFER_SIZE", DEFAULT_BUFFER_SIZE))
os.getenv("OUTPUT_PATH_LOG", "/tmp/unpack.log")


def stream_tar(stream: Blob) -> tarfile.TarFile:
    """Takes a Blob stream and opens it as a tarfile
    :param Blob stream: the incoming
    :returns TarFile: opened tarfile ready for interaction
    :raises Exception: if an error is encountered
    """
    try:
        tar_file = tarfile.open(fileobj=stream, mode="r|")
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


def main():
    logger.info("Starting s3-unpack")
    blob_service_client: BlobServiceClient = get_blob_service_client(conn_str)
    logger.info(f"Unpacking {source_object_name} into container {target_bucket_name}")
    target_bucket = create_target_bucket(blob_service_client, target_bucket_name)
    azure_blob = get_source_blob(blob_service_client, source_bucket, source_object_name)
    blob = Blob(azure_blob, max_concurrency, buffer_size)
    unpack_tar(target_bucket, blob)
    logger.info(f"Finished unpacking {source_object_name} into container {target_bucket_name} - exiting")


if __name__ == "__main__":
    main()
