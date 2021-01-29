import logging

from app.connectors.arkiv_downloader.queues.ArchiveDownloadRequestSender import ArchiveDownloadRequestSender, \
    REQUEST_SENDER_QUEUE_NAME
from app.connectors.sas_generator.sas_generator_client import SASGeneratorClient
from app.connectors.connectors_variables import get_sender_con_str, get_sas_generator_host
from app.database.session import get_session


async def get_db_session():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


async def get_request_sender() -> ArchiveDownloadRequestSender:
    logging.info(f"Create queue client for sending messages on queue {REQUEST_SENDER_QUEUE_NAME}")
    return ArchiveDownloadRequestSender(get_sender_con_str())


async def get_sas_generator_client() -> SASGeneratorClient:
    return SASGeneratorClient(get_sas_generator_host())
