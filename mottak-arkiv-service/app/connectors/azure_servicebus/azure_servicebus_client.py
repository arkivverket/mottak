"""
{
  "obj_id": "c05a214c-fcc5-11ea-8558-acde48001122",
  "blob_sas_url": "https://<storage_account>.blob.core.windows.net/<container>?<arkivkopi_request>"
}
"""

import os
import json
from uuid import UUID
from azure.servicebus.aio import QueueClient, Message
from azure.servicebus.common.errors import MessageSendFailed

from app.connectors.azure_servicebus.models import ArkivkopiRequest
from app.connectors.azure_servicebus.utils import UUIDEncoder

class AzureServicebus():
    def __init__(self):
        self.sender_con_string = os.environ['ARCHIVE_DOWNLOAD_REQUEST_SENDER_SB_CON_STRING']
        self.sender_queue_name = 'archive-download-request'

    @staticmethod
    def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
        return QueueClient.from_connection_string(queue_client_string, queue_name)

    async def request_download(self, arkivkopi_request: ArkivkopiRequest) -> bool:
        queue_client = self.create_queue_client(self.sender_con_string,
                                                self.sender_queue_name)

        message = Message(json.dumps(arkivkopi_request, cls=UUIDEncoder, default=str))

        # try:
        #     await queue_client.send(message)
        # except MessageSendFailed:
        #     return False

        return True
