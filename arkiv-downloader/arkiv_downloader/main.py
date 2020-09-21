import os
import logging
import subprocess
from uuid import uuid1, UUID
from dotenv import load_dotenv

from azure.servicebus import QueueClient, Message

from arkiv_downloader.models.dto import TransferStatus, ArkivuttrekkTransferInfo, ArkivuttrekkTransferStatus

load_dotenv()
BLOB_SAS_URL = os.getenv('BLOB_SAS_URL')
QUEUE_CLIENT_STRING = os.getenv('QUEUE_CLIENT_STRING')

logging.basicConfig(level=logging.INFO)


def create_queue_client(queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(QUEUE_CLIENT_STRING, queue_name)


def send_message_to_queue(message: str, client: QueueClient):
    msg = Message(message)
    client.send(msg)


def get_message_from_queue(client: QueueClient) -> ArkivuttrekkTransferInfo:
    with client.get_receiver() as receiver:
        message = receiver.next()
        message_str = str(message)
        print(f'Got message {message_str}')
        arkivuttrekk = ArkivuttrekkTransferInfo.from_string(message_str)
        message.complete()
        return arkivuttrekk


def download_blob(sas_url: str):
    azcopy_command = './azcopy/azcopy cp "{}" "local_file.tar" --recursive'.format(sas_url)
    print('Running: {}'.format(azcopy_command))
    subprocess.check_output(
        azcopy_command,
        stderr=subprocess.STDOUT,
        shell=True
    )
    os.system(azcopy_command)


def send_status_message(obj_id: UUID, status: TransferStatus, client: QueueClient):
    status_obj = ArkivuttrekkTransferStatus(obj_id, status)
    message = Message(status_obj.as_json_str())
    client.send(message)


def run(queue_client_downloader: QueueClient, queue_client_status: QueueClient):
    while True:
        arkivuttrekk = get_message_from_queue(queue_client_downloader)
        send_status_message(arkivuttrekk.obj_id, TransferStatus.TRANSFERING, queue_client_status)
        download_blob(arkivuttrekk.blob_sas_url)
        send_status_message(arkivuttrekk.obj_id, TransferStatus.FINISHED, queue_client_status)
        break


def mock_input(client: QueueClient):
    a = ArkivuttrekkTransferInfo(uuid1(), BLOB_SAS_URL)
    m = Message(a.as_json_str())
    client.send(m)


def mock_get_status(queue_client_status: QueueClient):
    with queue_client_status.get_receiver() as receiver:
        for i in [1, 2]:
            print(i)
            message = receiver.next()
            message_str = str(message)
            print(f'Got message {message_str}')
            message.complete()


if __name__ == '__main__':
    _queue_client_downloader = create_queue_client('downloader')
    _queue_client_status = create_queue_client('status')

    mock_input(_queue_client_downloader)

    run(_queue_client_downloader, _queue_client_status)

    mock_get_status(_queue_client_status)
