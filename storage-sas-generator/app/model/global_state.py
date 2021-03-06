""" Global state handling."""
from dataclasses import dataclass
from typing import Optional

from azure.storage.blob.aio import BlobServiceClient


@dataclass
class GlobalState:
    """We keep global state in an object like this. """
    status_code: int
    status_message: str
    azure_client: Optional[BlobServiceClient]
