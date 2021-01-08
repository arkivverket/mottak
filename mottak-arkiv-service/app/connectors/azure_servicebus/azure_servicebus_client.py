import logging

from azure.servicebus.aio import QueueClient, Message
from azure.servicebus.common.errors import MessageSendFailed


class AzureServicebus():
    def __init__(self, connection_string: str, queue_name: str):
        self.queue_client = self.create_queue_client(connection_string, queue_name)

    @staticmethod
    def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
        return QueueClient.from_connection_string(queue_client_string, queue_name)

    async def request_download(self, _message: str) -> bool:
        message = Message(_message)

        try:
            await self.queue_client.send(message)
        except MessageSendFailed:
            logging.error(f"Could not send message to the {self.queue_name} queue with the following data: {_message}")
            return False

        return True
