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

    async def run(self):
        """ A running loop that listens to the service bus receiver queue"""
        # keep_running = True
        with self.receiver as receiver:
            print(f"Starting receiving messages on queue {receiver.queue_name}")
            # while keep_running:
            messages = receiver.fetch_next(timeout=5, max_batch_size=1)  # reads 1 messages then waits for 3 seconds
            for message in messages:
                logging.info('Got a message on the service bus')
                message_str = await self.message_to_str(message)
                arkivkopi_status_response = ArkivkopiStatusResponse.from_string(message_str)
                if arkivkopi_status_response:
                    update_arkivkopi_status(arkivkopi_status_response, self.db)
        logging.info(f"Closing receiver {self.queue_name}")
