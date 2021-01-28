from typing import List

from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueReceiver
from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse

STATUS_RECEIVER_QUEUE_NAME = 'archive-download-status'


class ArchiveDownloadStatusReceiver(AzureQueueReceiver):
    """
    Class which contains the queue that recieves ArkivkopiStatus from arkiv_downloader
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string=connection_string, queue_name=STATUS_RECEIVER_QUEUE_NAME)

    async def receive_messages(self, max_batch_size: int = 1) -> List[ArkivkopiStatusResponse]:
        """
        Receives ArchiveDownloadStatus messages from the service bus
        :param max_batch_size: Number of messages to process
        :return: list with ArkivkopiStatus objects
        """
        messages = await super().receive_messages()
        return [ArkivkopiStatusResponse.from_string(message) for message in messages]
