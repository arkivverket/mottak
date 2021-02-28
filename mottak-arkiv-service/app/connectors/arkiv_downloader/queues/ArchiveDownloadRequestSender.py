from app.connectors.arkiv_downloader.models import ArkivkopiRequest
from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueSender
from app.connectors.sas_generator.models import SASResponse

REQUEST_SENDER_QUEUE_NAME = 'archive-download-request'


class ArchiveDownloadRequestSender(AzureQueueSender):
    """
    Class which contains the queue that sends ArkivkopiRequest to the arkiv_downloader
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string=connection_string, queue_name=REQUEST_SENDER_QUEUE_NAME)

    async def send_archive_download_request(self, sas_token: SASResponse, arkivkopi_id: int) -> bool:
        """
        Sends a archive download request on queue
        :param sas_token: SAS token containing information about what to download, including access key
        :param arkivkopi_id: id of this download request
        :return: True if message added to queue, else False
        """
        arkivkopi_request = ArkivkopiRequest.for_archive_download(arkivkopi_id, sas_token)
        return await super().send_message(arkivkopi_request.as_json_str())

    async def send_object_download_request(self, sas_token: SASResponse, arkivkopi_id: int,
                                           target_name: str, source_name: str) -> bool:
        """
        Sends a download request for an object on queue
        :param sas_token: SAS token containing information about what to download, including access key
        :param arkivkopi_id: id of this download request
        :param target_name: the name of the object when uploaded to on-prem (a.k.a. filnavn in Arkivkopi)
        :param source_name: the name of the object on cloud storage
        :return: True if message added to queue, else False
        """
        arkivkopi_request = ArkivkopiRequest.for_object_download(arkivkopi_id, sas_token, target_name, source_name)
        return await super().send_message(arkivkopi_request.as_json_str())
