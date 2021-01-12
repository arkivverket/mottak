import logging

from app.connectors.azure_servicebus.azure_servicebus_client import AzureQueueSender, AzureQueueReceiver
from app.connectors.connectors_variables import get_sender_con_str, get_status_con_str
from app.database.session import get_session
from typing import Optional

REQUEST_SENDER_QUEUE_NAME = 'archive-download-request'
STATUS_RECEIVER_QUEUE_NAME = 'archive-download-status'


async def get_db_session():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


def get_queue_sender() -> Optional[AzureQueueSender]:
    logging.info(f"Create queue client for sending messages on queue {REQUEST_SENDER_QUEUE_NAME}")
    sender = AzureQueueSender(get_sender_con_str(), REQUEST_SENDER_QUEUE_NAME)
    return sender if sender else None
# try:
#     logging.info(f"Create queue client for sending messages on queue {REQUEST_SENDER_QUEUE_NAME}")
#     client = AzureServicebus(get_sender_con_str(), REQUEST_SENDER_QUEUE_NAME)
#     yield client
# finally:
#     logging.info(f"Closing queue {REQUEST_SENDER_QUEUE_NAME}")


def get_queue_receiver() -> Optional[AzureQueueReceiver]:
    logging.info(f"Create queue client for receiving messages on queue {STATUS_RECEIVER_QUEUE_NAME}")
    receiver = AzureQueueReceiver(get_status_con_str(), STATUS_RECEIVER_QUEUE_NAME)
    return receiver if receiver else None
