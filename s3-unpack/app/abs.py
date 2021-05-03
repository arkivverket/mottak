import logging
import sys
from typing import Optional
from io import BytesIO

from azure.storage.blob import BlobServiceClient, ContainerClient,BlobClient
from azure.core.exceptions import ResourceExistsError, ClientAuthenticationError

from app.exitcodes import UPLOAD_ERROR, OBJECTSTORE_ERROR

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def get_blob_service_client(conn_str: str) -> BlobServiceClient:
    """
    Takes a Azure connection string and create a BlobServiceClient
    :param conn_str: the connection string
    :return: BlobServiceClient connected to AzureBlobStorage
    """
    try:
        client = BlobServiceClient.from_connection_string(conn_str)
        logger.info(f"Connected to Azure with API version {client.api_version}")
        return client
    except ClientAuthenticationError as err:
        logging.critical("An error occured while connecting to Azure, please check the credentials", err)
        sys.exit(OBJECTSTORE_ERROR)


def create_target_bucket(blob_service_client: BlobServiceClient, bucket_name: str) -> ContainerClient:
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
        sys.exit(OBJECTSTORE_ERROR)


def get_source_blob(blob_service_client: BlobServiceClient, source_bucket: str, source_object_name: str) -> BlobClient:
    """
    Creates a connection to a blob (need not already exist) on Azure Blob Storage
    :param blob_service_client: client connected to Azure Blob Storage
    :param source_bucket: the azure container containing the blob
    :param source_object_name: the object key
    :return: a BlobClient representing the given blob on Azure Blob Storage
    """
    return blob_service_client.get_blob_client(container=source_bucket, blob=source_object_name)


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
