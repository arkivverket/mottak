import os
import logging
import subprocess
from uuid import uuid1, UUID
from typing import Optional

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
ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING')
STORAGE_LOCATION = os.getenv('STORAGE_LOCATION')


def get_sas_url(arkivkopi_request: ArkivkopiRequest) -> str:
    """ Returns the URL of the blob to be downloaded."""
    return f"https://{arkivkopi_request.storage_account}.blob.core.windows.net/" \
           f"{arkivkopi_request.container}?{arkivkopi_request.sas_token}"


def get_save_path(arkivuttrekk_id: UUID, write_location: str) -> str:
    """ Returns the path to where the downloaded blob should be saved"""
    return os.path.join(write_location, str(arkivuttrekk_id)) + os.path.sep
    # return write_location + os.path.sep + str(arkivuttrekk_id) + os.path.sep


def generate_azcopy_command(arkivkopi_request: ArkivkopiRequest, save_path: str) -> list[str]:
    """ Returns the command to download a blob using azcopy."""
    return ['./azcopy/azcopy', 'cp',
            get_sas_url(arkivkopi_request), save_path, '--recursive']


def download_blob(arkivuttrekk: ArkivkopiRequest, write_location: str) -> ArkivkopiStatus:
    save_path = get_save_path(arkivuttrekk.arkivuttrekk_id, write_location)
    azcopy_command = generate_azcopy_command(arkivuttrekk, save_path)
    logging.info(f'Starting transfer of obj_id {arkivuttrekk.arkivuttrekk_id} to {save_path}')
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


def send_status_message(obj_id: UUID, status: ArkivkopiStatus, client: QueueClient):
    status_obj = ArkivkopiStatusResponse(obj_id, status)
    message = Message(status_obj.as_json_str())
    client.send(message)


def run(queue_client_downloader: QueueClient, queue_client_status: QueueClient, storage_location: str):
    # with client.get_receiver() as receiver: legg til her
    while True:
        arkivuttrekk = get_message_from_queue(queue_client_downloader) # TODO legg til await hvis ingen melding finnes. er dette automatisk?
        if arkivuttrekk:
            send_status_message(arkivuttrekk.obj_id, ArkivkopiStatus.STARTET, queue_client_status)
            status = download_blob(arkivuttrekk, storage_location)
            send_status_message(arkivuttrekk.obj_id, status, queue_client_status)


# TODO remove this
def mock_input(client: QueueClient):
    a = ArkivkopiRequest(uuid1(), BLOB_SAS_URL)
    m = Message(a.as_json_str())
    client.send(m)


# TODO remove this
def mock_get_status(queue_client_status: QueueClient):
    with queue_client_status.get_receiver() as receiver:
        for i in [1, 2]:
            message = receiver.next()
            message_str = str(message)
            print(f'Got message {message_str}')
            message.complete()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('arkiv_downloader starting up')
    logging.getLogger("uamqp").setLevel(logging.WARNING)
    _queue_client_archive_request_receiver = \
        create_queue_client(ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING, 'archive-download-request-receiver')
    _queue_client_archive_status_sender = \
        create_queue_client(ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING, 'archive-download-status-sender')

    mock_input(_queue_client_archive_request_receiver)  # TODO remove from final code

    run(_queue_client_archive_request_receiver, _queue_client_archive_status_sender, STORAGE_LOCATION)

    mock_get_status(_queue_client_archive_status_sender)  # TODO remove from final code
