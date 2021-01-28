import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from app.connectors.arkiv_downloader.queues.ArchiveDownloadStatusReceiver import ArchiveDownloadStatusReceiver
from app.connectors.connectors_variables import get_status_con_str
from app.database.session import get_session
from app.domain.arkivuttrekk_service import update_arkivkopi_status


async def init_scheduled_job() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    db_session = get_session()
    status_receiver = ArchiveDownloadStatusReceiver(get_status_con_str())
    logging.info("Adding job arkivkopi status job")
    scheduler.add_job(arkivkopi_status_job, 'interval', seconds=10, args=[status_receiver, db_session])
    return scheduler


async def arkivkopi_status_job(status_receiver: ArchiveDownloadStatusReceiver, db_session: Session):
    """
    A scheduled job to fetch arkiv kopi status messages from the service bus receiver queue, and update the database
    accordingly
    :param status_receiver: ArchiveDownloadStatusReceiver to fetch messages from the queue
    :param db_session: A session with the database
    """
    arkivkopi_statuses = await status_receiver.receive_messages()
    for arkivkopi_status in arkivkopi_statuses:
        if arkivkopi_status:
            update_arkivkopi_status(arkivkopi_status, db_session)
