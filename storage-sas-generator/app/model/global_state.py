
from dataclasses import dataclass
from azure.storage.blob.aio import BlobServiceClient


@dataclass
class GlobalState():
    status_code: int
    status_message: str
    azure_client: BlobServiceClient


