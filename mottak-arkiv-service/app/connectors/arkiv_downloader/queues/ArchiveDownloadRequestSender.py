from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueSender

REQUEST_SENDER_QUEUE_NAME = 'archive-download-request'


class ArchiveDownloadRequestSender(AzureQueueSender):
    """
    Class which contains the queue that sends ArkivkopiRequest to the arkiv_downloader
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string=connection_string, queue_name=REQUEST_SENDER_QUEUE_NAME)
