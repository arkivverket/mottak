import logging

from azure.servicebus.aio import QueueClient, Message
from azure.servicebus.common.errors import MessageSendFailed


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

    @staticmethod
    async def a_message_to_str(_message: Message) -> str:
        """ Method that converts a message to a string"""
        message_str = str(_message)
        return message_str

    @staticmethod
    def s_message_to_str(_message: Message) -> str:
        message_str = str(_message)
        _message.complete()
        return message_str

    @staticmethod
    async def a_message_processed(_message: Message):
        """ Method that removes message from queue"""
        await _message.complete()


class AzureQueueSender(AzureServicebus):
    def __init__(self, connection_string: str, queue_name: str):
        super().__init__(connection_string, queue_name)
        self.sender = self.queue_client.get_sender()

    async def send_message(self, _message: str) -> bool:
        message = Message(_message)

        try:
            await self.sender.send(message)
        except MessageSendFailed:
            logging.error(f"Could not send message to the {self.queue_name} queue with the following data: {_message}")
            return False

        return True
