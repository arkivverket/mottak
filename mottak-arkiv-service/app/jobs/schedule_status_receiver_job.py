import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.models import ArkivkopiStatusResponse
from app.connectors.arkiv_downloader.queues.ArchiveDownloadStatusReceiver import ArchiveDownloadStatusReceiver
from app.database.session import get_session
from app.domain.arkivuttrekk_service import update_arkivkopi_status


async def init_scheduled_job() -> [AsyncIOScheduler, str]:
    scheduler = AsyncIOScheduler()
    db_session = get_session()
    status_receiver = ArchiveDownloadStatusReceiver()
    queue_name = status_receiver.queue_name
    scheduler.add_job(fetch, 'interval', seconds=10, args=[status_receiver, db_session])
    return scheduler, queue_name


async def fetch(status_receiver: ArchiveDownloadStatusReceiver, db_session: Session):
    """
    A scheduled job to fetch one message from the service bus receiver queue.
    """
    messages = await status_receiver.receiver.fetch_next(timeout=5, max_batch_size=1)
    for message in messages:
        logging.info('Got a message on the service bus')
        message_str = await status_receiver.message_to_str(message)
        arkivkopi_status_response = ArkivkopiStatusResponse.from_string(message_str)
        if arkivkopi_status_response:
            update_arkivkopi_status(arkivkopi_status_response, db_session)



