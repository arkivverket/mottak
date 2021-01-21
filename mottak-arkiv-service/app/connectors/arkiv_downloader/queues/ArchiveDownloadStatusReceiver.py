import logging

from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse
from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueReceiver
from app.connectors.connectors_variables import get_status_con_str
from app.domain.arkivuttrekk_service import update_arkivkopi_status

STATUS_RECEIVER_QUEUE_NAME = 'archive-download-status'


class ArchiveDownloadStatusReceiver(AzureQueueReceiver):
    """
    Class which contains the queue that recieves ArkivkopiStatus from arkiv_downloader
    """

    def __init__(self, db: Session):
        super().__init__(connection_string=get_status_con_str(), queue_name=STATUS_RECEIVER_QUEUE_NAME)
        self.db = db

    async def a_run(self):
        """ Async function that is run from a scheduler to receive messages from the service bus receiver queue"""
        messages = await self.receiver.fetch_next(timeout=5, max_batch_size=1)
        for message in messages:
            # logging.info('Got a message on the service bus')
            print('Got a message on the service bus')
            message_str = await self.a_message_to_str(message)
            arkivkopi_status_response = ArkivkopiStatusResponse.from_string(message_str)
            if arkivkopi_status_response:
                update_arkivkopi_status(arkivkopi_status_response, self.db)
                await self.a_message_processed(message)

    def s_run(self):
        """ Sync function that is run from a scheduler to receive messages from the service bus receiver queue"""
        message = self.receiver.next()
        if message:
            # logging.info('Got a message on the service bus')
            print('Got a message on the service bus')
            message_str = self.s_message_to_str(message)
            arkivkopi_status_response = ArkivkopiStatusResponse.from_string(message_str)
            if arkivkopi_status_response:
                update_arkivkopi_status(arkivkopi_status_response, self.db)

