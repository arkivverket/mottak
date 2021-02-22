import logging
import os
import subprocess
from typing import Optional
from uuid import UUID

from typing import List
from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiver, ServiceBusSender

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


def get_save_path(write_location: str) -> str:
    """ Returns the path to where the downloaded blob should be saved"""
    return write_location + os.path.sep


def generate_azcopy_command(arkivkopi_request: ArkivkopiRequest, save_path: str) -> List[str]:
    """ Returns the command to download a blob using azcopy."""
    # return ['azcopy', 'cp', get_sas_url(arkivkopi_request), save_path, '--recursive']  # For local test
    return ['./azcopy/azcopy', 'cp', get_sas_url(arkivkopi_request), save_path, '--recursive']  # Docker container


def download_blob(arkivuttrekk: ArkivkopiRequest, write_location: str) -> ArkivkopiStatus:
    save_path = get_save_path(write_location)
    azcopy_command = generate_azcopy_command(arkivuttrekk, save_path)
    logging.info(f'Starting transfer of container {arkivuttrekk.container} to {save_path}')
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


def send_status_message(arkivkopi_id: int, status: ArkivkopiStatus, client: ServiceBusSender):
    status_obj = ArkivkopiStatusResponse(arkivkopi_id, status)
    message = ServiceBusMessage(status_obj.as_json_str())
    client.send_messages(message)


def download_arkivkopi(arkivkopi_request: ArkivkopiRequest,
                       queue_client_status: ServiceBusSender,
                       storage_location: str) -> None:
    logging.info(f'Got download request for container with container name: {arkivkopi_request.container}')
    send_status_message(arkivkopi_request.arkivkopi_id, ArkivkopiStatus.STARTET, queue_client_status)
    status = download_blob(arkivkopi_request, storage_location)
    send_status_message(arkivkopi_request.arkivkopi_id, status, queue_client_status)


def process_message(message: ServiceBusMessage) -> Optional[ArkivkopiRequest]:
    """ Method that process a message containing an ArkivkopiRequest."""
    logging.info('Got a message on the service bus')
    message_str = str(message)
    arkivkopi_request = ArkivkopiRequest.from_string(message_str)  # logs error if it fails to parse
    return arkivkopi_request if arkivkopi_request else None


def run(queue_client_downloader: ServiceBusReceiver, queue_client_status: ServiceBusSender, storage_location: str):
    """ The main loop that listens to the service bus queue"""
    keep_running = True
    with queue_client_downloader as receiver:
        logging.info(f"Starting receiving messages on queue {receiver}")
        while keep_running:
            messages = receiver.receive_messages(max_wait_time=3, max_message_count=1)  # reads 1 messages then waits for 3 seconds
            for message in messages:
                arkivkopi_request = process_message(message)
                receiver.complete_message(message)
                if arkivkopi_request:
                    download_arkivkopi(arkivkopi_request, queue_client_status, storage_location)
    logging.info(f"Closing receiver")


def create_queue_client(queue_client_string: str) -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(queue_client_string)


def create_queue_sender_client(queue_client_string: str, queue_name: str) -> ServiceBusSender:
    return ServiceBusClient.from_connection_string(queue_client_string).get_queue_sender(queue_name)


def create_queue_receiver_client(queue_client_string: str, queue_name: str) -> ServiceBusReceiver:
    return ServiceBusClient.from_connection_string(queue_client_string).get_queue_receiver(queue_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('arkiv_downloader starting up')
    logging.getLogger('uamqp').setLevel(logging.WARNING)  # Reducing noise in the logs from overly verbose logger

    # create queues
    _request_receiver = create_queue_receiver_client(ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING,
                                                     ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_QUEUE_NAME)

    _status_sender = create_queue_sender_client(ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING,
                                                ARCHIVE_DOWNLOAD_STATUS_SENDER_QUEUE_NAME)

    # start main loop
    run(_request_receiver, _status_sender, ARCHIVE_TARGET_LOCATION)
