import logging

from typing import List
from azure.servicebus.aio import QueueClient, Message
from azure.servicebus.common.errors import MessageSendFailed


logger = logging.getLogger(__name__)


class AzureServicebus():
    def __init__(self, connection_string: str, queue_name: str):
        self.queue_name = queue_name
        self.queue_client = self.create_queue_client(connection_string, queue_name)

    @staticmethod
    def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
        return QueueClient.from_connection_string(queue_client_string, queue_name)


class AzureQueueReceiver(AzureServicebus):
    def __init__(self, connection_string: str, queue_name: str):
        super().__init__(connection_string, queue_name)
        self.receiver = self.queue_client.get_receiver()

    async def receive_messages(self, max_batch_size: int = 1) -> List[str]:
        messages = await self.receiver.fetch_next(timeout=5, max_batch_size=max_batch_size)
        result = []
        for message in messages:
            result.append(await self.message_to_str(message))
            await message.complete()
        return result

    @staticmethod
    async def message_to_str(_message: Message) -> str:
        """ Method that converts a message to a string"""
        message_str = str(_message)
        return message_str


class AzureQueueSender(AzureServicebus):
    def __init__(self, connection_string: str, queue_name: str):
        super().__init__(connection_string, queue_name)
        self.sender = self.queue_client.get_sender()

    async def send_message(self, _message: str) -> bool:
        message = Message(_message)

        try:
            await self.sender.send(message)
        except MessageSendFailed:
            logger.error(f"Could not send message to the {self.queue_name} queue with the following data: {_message}")
            return False

        return True
