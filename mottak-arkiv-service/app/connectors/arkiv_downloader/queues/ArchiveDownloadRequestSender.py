from __future__ import annotations

from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueSender
from app.connectors.connectors_variables import get_sender_con_str

REQUEST_SENDER_QUEUE_NAME = 'archive-download-request'


class ArchiveDownloadRequestSender(AzureQueueSender):
    """
    Class which contains the queue that sends ArkivkopiRequest to the arkiv_downloader
    """
    def __init__(self):
        super().__init__(connection_string=get_sender_con_str(), queue_name=REQUEST_SENDER_QUEUE_NAME)
