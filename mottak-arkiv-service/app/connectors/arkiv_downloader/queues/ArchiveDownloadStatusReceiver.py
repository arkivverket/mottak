from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueReceiver

STATUS_RECEIVER_QUEUE_NAME = 'archive-download-status'


class ArchiveDownloadStatusReceiver(AzureQueueReceiver):
    """
    Class which contains the queue that recieves ArkivkopiStatus from arkiv_downloader
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string=connection_string, queue_name=STATUS_RECEIVER_QUEUE_NAME)
