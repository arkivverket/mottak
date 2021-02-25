import logging
import os
import subprocess
from typing import Optional

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

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logging.getLogger('uamqp').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING')
ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_QUEUE_NAME = 'archive-download-request'
ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING')
ARCHIVE_DOWNLOAD_STATUS_SENDER_QUEUE_NAME = 'archive-download-status'
ARCHIVE_TARGET_LOCATION = os.getenv('ARCHIVE_TARGET_LOCATION')


def get_sas_url(arkivkopi_request: ArkivkopiRequest) -> str:
    """ Returns the URL of the blob to be downloaded."""
    if arkivkopi_request.blob_info:
        return f"https://{arkivkopi_request.storage_account}.blob.core.windows.net/{arkivkopi_request.container}/{arkivkopi_request.blob_info.source_name}?{arkivkopi_request.sas_token}"
    else:
        return f"https://{arkivkopi_request.storage_account}.blob.core.windows.net/{arkivkopi_request.container}?{arkivkopi_request.sas_token}"


def get_target(arkivkopi_request: ArkivkopiRequest, save_path: str) -> str:
    """
    Generates target location and filename `save_path/target_file.extension` if source is an object, otherwise save_path
    """
    if arkivkopi_request.blob_info:
        return save_path + arkivkopi_request.blob_info.target_name
    else:
        return save_path


def generate_azcopy_command(arkivkopi_request: ArkivkopiRequest, save_path: str) -> List[str]:
    """ Returns the command to download a blob using azcopy."""
    # return ['azcopy', 'cp', get_sas_url(arkivkopi_request), save_path, '--recursive']  # For local test
    target_file = get_target(arkivkopi_request, save_path)
    return ['./azcopy/azcopy', 'cp', get_sas_url(arkivkopi_request), target_file, '--recursive']  # Docker container


def download(arkivuttrekk: ArkivkopiRequest, storage_location: str) -> ArkivkopiStatus:
    azcopy_command = generate_azcopy_command(arkivuttrekk, storage_location)
    logger.info(f'Starting transfer of arkivkopi {arkivuttrekk.arkivkopi_id} to {storage_location}')
    try:
        response = subprocess.check_output(
            azcopy_command,
            stderr=subprocess.STDOUT
        )
        logger.info(response.decode('utf-8'))
        return ArkivkopiStatus.OK
    except subprocess.CalledProcessError as e:
        logger.error(e.output.decode('utf-8'))
        return ArkivkopiStatus.FEILET
    except FileNotFoundError as e:
        logger.error('Could not find azcopy', e)
        return ArkivkopiStatus.FEILET


def send_status_message(arkivkopi_id: int, status: ArkivkopiStatus, client: ServiceBusSender):
    status_obj = ArkivkopiStatusResponse(arkivkopi_id, status)
    message = ServiceBusMessage(status_obj.as_json_str())
    client.send_messages(message)
    logger.info(f'Status message sent {status_obj.as_json_str()}')


def download_arkivkopi(arkivkopi_request: ArkivkopiRequest,
                       queue_client_status: ServiceBusSender,
                       storage_location: str) -> None:
    send_status_message(arkivkopi_request.arkivkopi_id, ArkivkopiStatus.STARTET, queue_client_status)
    status = download(arkivkopi_request, storage_location)
    send_status_message(arkivkopi_request.arkivkopi_id, status, queue_client_status)


def process_message(message: ServiceBusMessage) -> Optional[ArkivkopiRequest]:
    """ Method that process a message containing an ArkivkopiRequest."""
    logger.info('Got a message on the service bus')
    message_str = str(message)
    arkivkopi_request = ArkivkopiRequest.from_string(message_str)  # logs error if it fails to parse
    if arkivkopi_request:
        logger.info(f'Received download request {arkivkopi_request.as_safe_json_str()}')
        return arkivkopi_request
    else:
        return None


def run(queue_client_downloader: ServiceBusReceiver, queue_client_status: ServiceBusSender, storage_location: str):
    """ The main loop that listens to the service bus queue"""
    keep_running = True
    with queue_client_downloader as receiver:
        logger.info(f"Starting receiving messages on queue {receiver.entity_path}")
        while keep_running:
            messages = receiver.receive_messages(max_message_count=1)  # reads 1 message at the time
            for message in messages:
                arkivkopi_request = process_message(message)
                receiver.complete_message(message)
                if arkivkopi_request:
                    download_arkivkopi(arkivkopi_request, queue_client_status, storage_location)
        logger.info(f"Closing receiver {receiver.entity_path}")


def create_queue_client(queue_client_string: str) -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(queue_client_string)


def create_queue_sender_client(queue_client_string: str, queue_name: str) -> ServiceBusSender:
    return create_queue_client(queue_client_string).get_queue_sender(queue_name)


def create_queue_receiver_client(queue_client_string: str, queue_name: str) -> ServiceBusReceiver:
    return create_queue_client(queue_client_string).get_queue_receiver(queue_name)


if __name__ == '__main__':
    logger.info('arkiv_downloader starting up')

    # create queues
    _request_receiver = create_queue_receiver_client(ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING,
                                                     ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_QUEUE_NAME)

    _status_sender = create_queue_sender_client(ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING,
                                                ARCHIVE_DOWNLOAD_STATUS_SENDER_QUEUE_NAME)

    # start main loop
    run(_request_receiver, _status_sender, ARCHIVE_TARGET_LOCATION)
