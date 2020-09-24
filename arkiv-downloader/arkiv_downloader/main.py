import os
import logging
import subprocess
from uuid import uuid1, UUID
from typing import Optional

from azure.servicebus import QueueClient, Message

from arkiv_downloader.models.dto import TransferStatus, ArkivuttrekkTransferInfo, ArkivuttrekkTransferStatus

try:
    # Importing .env file if it exists
    import dotenv
    dotenv.load_dotenv()
    del dotenv
except ImportError:
    pass


BLOB_SAS_URL = os.getenv('BLOB_SAS_URL')
QUEUE_CLIENT_STRING = os.getenv('QUEUE_CLIENT_STRING')
STORAGE_LOCATION = os.getenv('STORAGE_LOCATION')

logging.basicConfig(level=logging.INFO)
logging.getLogger('uamqp').setLevel(logging.WARNING)  # Reducing noise in the logs from overly verbose logger


def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(queue_client_string, queue_name)


def send_message_to_queue(message: str, client: QueueClient):
    msg = Message(message)
    client.send(msg)


def get_message_from_queue(client: QueueClient) -> Optional[ArkivuttrekkTransferInfo]:
    with client.get_receiver() as receiver:
        message = receiver.next()
        message_str = str(message)
        message.complete()
        logging.info(f'Got message: {message_str}')  # Todo Remove this? It will print the entire sas url
        return ArkivuttrekkTransferInfo.from_string(message_str)


def download_blob(arkivuttrekk: ArkivuttrekkTransferInfo, write_location: str) -> TransferStatus:
    save_path = write_location + os.path.sep + str(arkivuttrekk.obj_id) + os.path.sep
    azcopy_command = ['./azcopy/azcopy', 'cp', f'{arkivuttrekk.container_sas_url}', save_path, '--recursive']
    logging.info(f'Starting transfer of obj_id {arkivuttrekk.obj_id} to {save_path}')
    try:
        response = subprocess.check_output(
            azcopy_command,
            stderr=subprocess.STDOUT
        )
        logging.info(response.decode('utf-8'))
        return TransferStatus.FINISHED
    except subprocess.CalledProcessError as e:
        logging.error(e.output.decode('utf-8'))
        return TransferStatus.FAILED
    except FileNotFoundError as e:
        logging.error('Could not find azcopy', e)
        return TransferStatus.FAILED


def send_status_message(obj_id: UUID, status: TransferStatus, client: QueueClient):
    status_obj = ArkivuttrekkTransferStatus(obj_id, status)
    message = Message(status_obj.as_json_str())
    client.send(message)


def run(queue_client_downloader: QueueClient, queue_client_status: QueueClient, storage_location: str):
    while True:
        arkivuttrekk = get_message_from_queue(queue_client_downloader)
        if arkivuttrekk:
            send_status_message(arkivuttrekk.obj_id, TransferStatus.STARTING_TRANSFER, queue_client_status)
            status = download_blob(arkivuttrekk, storage_location)
            send_status_message(arkivuttrekk.obj_id, status, queue_client_status)


# TODO remove this
def mock_input(client: QueueClient):
    a = ArkivuttrekkTransferInfo(uuid1(), BLOB_SAS_URL)
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
    _queue_client_downloader = create_queue_client(QUEUE_CLIENT_STRING, 'downloader')
    _queue_client_status = create_queue_client(QUEUE_CLIENT_STRING, 'status')

    mock_input(_queue_client_downloader)  # Todo remove from final code

    run(_queue_client_downloader, _queue_client_status, STORAGE_LOCATION)

    mock_get_status(_queue_client_status)  # Todo remove from final code
