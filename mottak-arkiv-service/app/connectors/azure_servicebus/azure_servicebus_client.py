import logging
import os

from azure.servicebus.aio import QueueClient, Message
from azure.servicebus.common.errors import MessageSendFailed

from app.domain.models.Bestilling import BestillingRequest


class AzureServicebus():
    def __init__(self):
        self.sender_con_string = os.environ['ARCHIVE_DOWNLOAD_REQUEST_SENDER_SB_CON_STRING']
        self.sender_queue_name = 'archive-download-request'

    @staticmethod
    def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
        return QueueClient.from_connection_string(queue_client_string, queue_name)

    async def request_download(self, arkivkopi_request: BestillingRequest) -> bool:
        queue_client = self.create_queue_client(self.sender_con_string,
                                                self.sender_queue_name)

        message = Message(arkivkopi_request.as_json_str())

        try:
            await queue_client.send(message)
        except MessageSendFailed:
            logging.error(f"Could not send message to the {self.sender_queue_name} queue with the following data: {arkivkopi_request.as_json_str()}")
            return False

        return True
