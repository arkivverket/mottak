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

# TODO Remove this env variable when ready. This will be a part of incoming message things are more ready.
BLOB_SAS_URL = os.getenv('BLOB_SAS_URL')
ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING')
ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING = os.getenv('ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING')
QUEUE_CLIENT_STRING = os.getenv('QUEUE_CLIENT_STRING')
STORAGE_LOCATION = os.getenv('STORAGE_LOCATION')

logging.basicConfig(level=logging.INFO)
logging.getLogger('uamqp').setLevel(logging.WARNING)  # Reducing noise in the logs from overly verbose logger


def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(queue_client_string, queue_name)


def send_message_to_queue(message: str, client: QueueClient):
    msg = Message(message)
    client.send(msg)


def get_message_from_queue(client: QueueClient) -> Optional[ArkivkopiRequest]:
    with client.get_receiver() as receiver:
        message = receiver.next()  # TODO Trenger vi noen kontroll for om det er melding på køen her?
        message_str = str(message)
        message.complete()
        logging.info(f'Got download request for: {message to json-> obj_id}')  # Todo Remove this? Got downlo
        return ArkivkopiRequest.from_string(message_str)


def download_blob(arkivuttrekk: ArkivkopiRequest, write_location: str) -> ArkivkopiStatus:
    save_path = write_location + os.path.sep + str(arkivuttrekk.obj_id) + os.path.sep
    azcopy_command = ['./azcopy/azcopy', 'cp', f'{arkivuttrekk.container_sas_url}', save_path, '--recursive']
    logging.info(f'Starting transfer of obj_id {arkivuttrekk.obj_id} to {save_path}')
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
