import logging

from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.queues.ArchiveDownloadRequestSender import ArchiveDownloadRequestSender, \
    REQUEST_SENDER_QUEUE_NAME
from app.connectors.arkiv_downloader.queues.ArchiveDownloadStatusReceiver import ArchiveDownloadStatusReceiver, \
    STATUS_RECEIVER_QUEUE_NAME
from app.database.session import get_session


async def get_db_session():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


async def get_status_receiver(db: Session) -> ArchiveDownloadStatusReceiver:
    logging.info(f"Create queue client for receiving messages on queue {STATUS_RECEIVER_QUEUE_NAME}")
    return ArchiveDownloadStatusReceiver(db)


async def get_request_sender() -> ArchiveDownloadRequestSender:
    logging.info(f"Create queue client for sending messages on queue {REQUEST_SENDER_QUEUE_NAME}")
    return ArchiveDownloadRequestSender()
