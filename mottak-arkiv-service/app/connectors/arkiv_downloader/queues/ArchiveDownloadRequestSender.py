from app.connectors.arkiv_downloader.models import ArkivkopiRequest
from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueSender
from app.domain.models.Arkivkopi import ArkivkopiRequestParameters

REQUEST_SENDER_QUEUE_NAME = 'archive-download-request'


class ArchiveDownloadRequestSender(AzureQueueSender):
    """
    Class which contains the queue that sends ArkivkopiRequest to the arkiv_downloader
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string=connection_string, queue_name=REQUEST_SENDER_QUEUE_NAME)

    async def send_download_request(self, parameters: ArkivkopiRequestParameters) -> bool:
        """
        Sends a download request on queue
        :param parameters: a parameter class containing
            - arkivkopi_id: id of this download request
            - sas_token: SAS token containing information about what to download, including access key
            - source_name: the name of the object to download from cloud storage if object download else None
            - target_name: the name of the uploaded content on-prem, folder name or object name
        :return: True if message added to queue, else False
        """
        arkivkopi_request = ArkivkopiRequest.from_parameters(parameters)
        return await super().send_message(arkivkopi_request.as_json_str())

