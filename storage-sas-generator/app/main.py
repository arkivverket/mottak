""" SAS Generator service. Runs on Azure. Generates SAS tokens which are used whenever we
wanna export an container somehow. Called by the dashboard when the downloader
needs a SAS token."""

from datetime import datetime, timedelta
import os
import logging

# FastAPI and Starlette:
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_412_PRECONDITION_FAILED

# Azure Blob Storage
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import generate_container_sas, ContainerSasPermissions

# Model
from app.model.dto import SASRequest, SASResponse
from app.model.global_state import GlobalState
from app.constants import *  # pylint: disable=wildcard-import

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print('Could not load dotenv module. No worries.')

# pylint: disable=logging-fstring-interpolation

app = FastAPI()

global_state = GlobalState(status_code=STATUS_INITIALIZING,
                           status_message='Initializing',
                           azure_client=None)

runtime_config = {
    'status': STATUS_ERROR
}


async def register_status(status_code: int, message: str) -> None:
    """
    Register a status internally. Used for the health check.

    Parameters:
          status_code: int, constant
          message: str - description of the state

          Returns None.
    """
    global_state.status_code = status_code
    global_state.status_message = message


async def get_service_url(account: str) -> str:
    """ Returns the URL of the blob storage service"""
    return f"https://{account}.blob.core.windows.net"


async def validate_container(client: BlobServiceClient, container: str) -> None:
    """ This makes sure that the given container exists and we have access to it.
    Will raise an error which is caught further out. """
    container_client = client.get_container_client(container)
    props = await container_client.get_container_properties()
    logging.info(props)
    return None


async def create_sas(container: str, duration_hours: int = 1) -> SASResponse:
    """ Creates the actual SAS signature.

    Gets the client connection from runtime_config.

    Parameters:
        container: str  - The container which we should download
        duration_hours: int - How long should the SAS token be valid. Defaults to 1 hour

    Returns:
        SASResponse - An object containing information about the storage account and container
        as well as the generated SAS (sas_token).
    """
    client = runtime_config["client"]

    # Validate that the container is online. Will raise an exception on error.
    await validate_container(client, container)

    sas_token = generate_container_sas(
        client.account_name,
        container_name=container,
        account_key=client.credential.account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=duration_hours)
    )
    return SASResponse(storage_account=client.account_name, container=container, sas_token=sas_token)


@app.on_event("startup")
async def startup_event():
    """ Async function which is run on FastAPI startup.
    Put your bootup code here.
    """
    logging.basicConfig(level=logging.INFO)
    # Silence the somewhat verbose Azure libs...
    logging.getLogger("azure.core.pipeline.policies").setLevel(logging.WARNING)
    account = os.getenv('AZURE_ACCOUNT_NAME')
    key = os.getenv('AZURE_ACCOUNT_KEY')
    logging.info(f'Using storage account: "{account}"')
    if key:
        logging.info('Storage key is set')
    else:
        raise ValueError('Environment variable AZURE_KEY is not set')

    blob_service_client = BlobServiceClient(account_url=await get_service_url(account),
                                            credential=key)
    logging.info(f'Connected to Azure Blob Service version {blob_service_client.api_version}')
    # This forces some talk on the wire to verify that we can talk to the Azure API.
    runtime_config["client"] = blob_service_client  # TODO Skal denne clienten også settes i global_state.client? Får feilmelding i IDE at den er None
    logging.info('Probing storage layer.')
    try:
        await blob_service_client.get_account_information()
        await register_status(STATUS_OK, 'OK')
    except ServiceRequestError as exception:
        await register_status(STATUS_ERROR, exception)
        logging.error(f"Something went wrong when talking to Azure: {exception}")


@app.get("/healthz")
async def health_check():
    """ Health check.
    Pings the Azure blob service. Used by kubernetes.
    """
    status = global_state.status_code
    message = global_state.status_message
    if status != STATUS_OK:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Service is experiencing failure: {message}")
    return {"status": "Hunky dory"}


@app.post("/generate_sas")
async def generate_sas(dto: SASRequest):
    """This generates an SAS signature for a given container.
    Will fail with a 412 if the container cannot be found.
    """
    logging.info(f'Generating SAS for container: "{dto.container}"')
    try:
        sas_response = await create_sas(container=dto.container, duration_hours=dto.duration_hours)
        return sas_response
    except ResourceNotFoundError as exception:
        raise HTTPException(status_code=HTTP_412_PRECONDITION_FAILED,
                            detail="The specified container does not exist") from exception


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
