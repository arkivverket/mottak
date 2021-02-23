import logging
import os
import subprocess
from typing import Optional
from uuid import UUID

from typing import List
from azure.servicebus import QueueClient, Message

from arkiv_downloader.models.dto import ArkivkopiStatus, ArkivkopiRequest, ArkivkopiStatusResponse

try:
    # Importing .env file if it exists
    import dotenv

    dotenv.load_dotenv()
    del dotenv
except ImportError:
    pass

ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING')
ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_QUEUE_NAME = 'archive-download-request'
ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING')
ARCHIVE_DOWNLOAD_STATUS_SENDER_QUEUE_NAME = 'archive-download-status'
ARCHIVE_TARGET_LOCATION = os.getenv('ARCHIVE_TARGET_LOCATION')


def get_sas_url(arkivkopi_request: ArkivkopiRequest) -> str:
    """ Returns the URL of the blob to be downloaded."""
    return f"https://{arkivkopi_request.storage_account}.blob.core.windows.net/{arkivkopi_request.container}?{arkivkopi_request.sas_token}"


def generate_azcopy_command(arkivkopi_request: ArkivkopiRequest, save_path: str) -> List[str]:
    """ Returns the command to download a blob using azcopy."""
    # return ['azcopy', 'cp', get_sas_url(arkivkopi_request), save_path, '--recursive']  # For local test
    return ['./azcopy/azcopy', 'cp', get_sas_url(arkivkopi_request), save_path, '--recursive']  # Docker container


def download_blob(arkivuttrekk: ArkivkopiRequest, storage_location: str) -> ArkivkopiStatus:
    azcopy_command = generate_azcopy_command(arkivuttrekk, storage_location)
    logging.info(f'Starting transfer of container {arkivuttrekk.container} to {storage_location}')
    try:
        response = subprocess.check_output(
            azcopy_command,
            stderr=subprocess.STDOUT
        )
        logging.info(response.decode('utf-8'))
        return ArkivkopiStatus.OK
    except subprocess.CalledProcessError as e:
        logging.error(e.output.decode('utf-8'))
        return ArkivkopiStatus.FEILET
    except FileNotFoundError as e:
        logging.error('Could not find azcopy', e)
        return ArkivkopiStatus.FEILET


def send_status_message(arkivkopi_id: int, status: ArkivkopiStatus, client: QueueClient):
    status_obj = ArkivkopiStatusResponse(arkivkopi_id, status)
    message = Message(status_obj.as_json_str())
    client.send(message)


def download_arkivkopi(arkivkopi_request: ArkivkopiRequest,
                       queue_client_status: QueueClient,
                       storage_location: str) -> None:
    logging.info(f'Got download request for container with container name: {arkivkopi_request.container}')
    send_status_message(arkivkopi_request.arkivkopi_id, ArkivkopiStatus.STARTET, queue_client_status)
    status = download_blob(arkivkopi_request, storage_location)
    send_status_message(arkivkopi_request.arkivkopi_id, status, queue_client_status)


def process_message(message: Message) -> Optional[ArkivkopiRequest]:
    """ Method that process a message containing an ArkivkopiRequest."""
    logging.info('Got a message on the service bus')
    message_str = str(message)
    arkivkopi_request = ArkivkopiRequest.from_string(message_str)  # logs error if it fails to parse
    message.complete()
    return arkivkopi_request if arkivkopi_request else None


def run(queue_client_downloader: QueueClient, queue_client_status: QueueClient, storage_location: str):
    """ The main loop that listens to the service bus queue"""
    keep_running = True
    with queue_client_downloader.get_receiver() as receiver:
        logging.info(f"Starting receiving messages on queue {queue_client_downloader.name}")
        while keep_running:
            messages = receiver.fetch_next(timeout=3, max_batch_size=1)  # reads 1 messages then waits for 3 seconds
            for message in messages:
                arkivkopi_request = process_message(message)
                if arkivkopi_request:
                    download_arkivkopi(arkivkopi_request, queue_client_status, storage_location)
    logging.info(f"Closing receiver {queue_client_downloader.name}")


def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(queue_client_string, queue_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('arkiv_downloader starting up')
    logging.getLogger('uamqp').setLevel(logging.WARNING)  # Reducing noise in the logs from overly verbose logger

    # create queues
    _request_receiver = create_queue_client(ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING,
                                            ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_QUEUE_NAME)
    _status_sender = create_queue_client(ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING,
                                         ARCHIVE_DOWNLOAD_STATUS_SENDER_QUEUE_NAME)

    # start main loop
    run(_request_receiver, _status_sender, ARCHIVE_TARGET_LOCATION)
