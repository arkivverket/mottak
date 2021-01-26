from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueReceiver
from app.connectors.connectors_variables import get_status_con_str

STATUS_RECEIVER_QUEUE_NAME = 'archive-download-status'


class ArchiveDownloadStatusReceiver(AzureQueueReceiver):
    """
    Class which contains the queue that recieves ArkivkopiStatus from arkiv_downloader
    """

    def __init__(self):
        super().__init__(connection_string=get_status_con_str(), queue_name=STATUS_RECEIVER_QUEUE_NAME)
