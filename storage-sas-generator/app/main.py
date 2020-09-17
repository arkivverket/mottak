""" SAS Generator service. Runs on Azure. Generates SAS tokens which are used whenever we
wanna exportan container somehow. Called by the dashboard when the downloader
needs a SAS token."""

from datetime import datetime, timedelta
import os
import logging

# FastAPI and Starlette:
from fastapi import FastAPI, HTTPException

# Azure Blob Storage
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import AccountSasPermissions, generate_container_sas
from azure.storage.blob._generated.models import StorageErrorException

# Model
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_412_PRECONDITION_FAILED

from app.model.dto import SASRequest

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print('Could not load dotenv module. No worries.')

# pylint: disable=logging-fstring-interpolation

app = FastAPI()

STATUS_OK = 0
STATUS_ERROR = 1

runtime_config = {
    'status': STATUS_ERROR
}


async def get_service_url(account):
    """ Returns the URL of the blob storage service"""
    return f"https://{account}.blob.core.windows.net"


async def validate_container(client, container: str) -> bool:
    """ This makes sure that the given container exists and we have access to it.
    Will raise an error which is caught further out. """
    container_client = client.get_container_client(container)
    props = await container_client.get_container_properties()
    logging.info(props)
    return None


async def create_sas(container: str, duration_hours: int = 1) -> str:
    """ Creates the actual SAS signature.

    Gets the client connection from runtime_config.

    Parameters:
        container: str  - The container which we should download
        duration_hours: int - How long should the SAS token be valid. Defaults to 1 hour

    Returns:
        str - the generated SAS (sas_token).
    """
    client = runtime_config["client"]

    # Validate that the container is online. Will raise an exception on error.
    await validate_container(client, container)

    sas_token = generate_container_sas(
        client.account_name,
        container_name=container,
        account_key=client.credential.account_key,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=duration_hours)
    )
    return sas_token


@app.on_event("startup")
async def startup_event():
    """ Async function which is run on FastAPI startup.
    Put your bootup code here.
    """
    logging.basicConfig(level=logging.INFO)
    # Silence the somewhat verbose Azure libs...
    logging.getLogger("azure.core.pipeline.policies").setLevel(logging.WARNING)
    account = os.getenv('AZURE_ACCOUNT')
    key = os.getenv('AZURE_KEY')
    logging.info(f'Using storage account: "{account}"')
    if key:
        logging.info('Storage key is set')
    else:
        raise ValueError('Environment variable AZURE_KEY is not set')

    blob_service_client = BlobServiceClient(account_url=await get_service_url(account),
                                            credential=key)
    logging.info(f'Connected to Azure Blob Service version {blob_service_client.api_version}')
    # This forces some talk on the wire to verify that we can talk to the Azure API.
    runtime_config["client"] = blob_service_client

    try:
        await blob_service_client.get_account_information()
        runtime_config["status"] = STATUS_OK
    except StorageErrorException as exception:
        runtime_config["status"] = STATUS_ERROR
        logging.error(f"Something went wrong when talking to Azure: {exception}")


@app.get("/healthz")
async def health_check():
    """ Health check.
    Pings the Azure blob service.
    """
    status = runtime_config["status"]
    if status != STATUS_OK:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Service is experiencing failure")
    return {"status": "Hunky dory"}

@app.post("/generate_sas")
async def generate_sas(dto: SASRequest):
    """This generates an SAS signature for a given container.
    Will fail with a 412 if the container cannot be found.
    """
    logging.info(f'Generating SAS for container: "{dto.container}"')
    try:
        sas = await create_sas(container=dto.container, duration_hours=dto.duration_hours)
        return {"sas": sas}
    except ResourceNotFoundError as exception:
        raise HTTPException(status_code=HTTP_412_PRECONDITION_FAILED,
                            detail="The specified container does not exist") from exception
