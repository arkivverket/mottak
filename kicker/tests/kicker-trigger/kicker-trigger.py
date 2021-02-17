import os
import json
from azure.servicebus import QueueClient, Message


try:
    # Importing .env file if it exists
    import dotenv
    dotenv.load_dotenv()
    del dotenv
except ImportError:
    pass

QUEUE_CLIENT_CONNECTION_STRING = os.getenv('QUEUE_CLIENT_CONNECTION_STRING')
QUEUE_NAME = os.getenv('QUEUE_NAME')


# Edit the values in this method
def get_params() -> dict:
    return {
        'TARGET_BUCKET_NAME': '8de75c05-744d-4622-af38-fad5b6f1dc30-0',
        'TUSD_OBJEKT_NAVN': '85a7d9cf0aac32393c82a70b20db5f9c',
        'SJEKKSUM': 'd35e6aa1aa46275ca825d1b5e3eb6c6442f91e1c1ad3153f354dd6467a759df1',
        'EKSTERN_ID': '8de75c05-744d-4622-af38-fad5b6f1dc30',
        'ARKIV_TYPE': 'Noark5',
        'KOORDINATOR_EPOST': 'kriwal@arkivverket.no',
        'ARKIVUTTREKK_OBJ_ID': 'c8db1f06-4495-4c18-bfd4-ccb0a450cba5'
    }


def create_message(params: dict) -> dict:
    return {
        'action': 'argo-submit',
        'params': params,
    }


def send_message(message: dict):
    m = Message(json.dumps(message).encode('utf8'))
    client.send(m)


def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(queue_client_string, queue_name)


if __name__ == '__main__':
    print(f'Creating queue client for {QUEUE_NAME}')
    client = create_queue_client(QUEUE_CLIENT_CONNECTION_STRING, QUEUE_NAME)
    message = create_message(get_params())
    print(f'Publishing {message} to kicker queue')
    send_message(message)
    print('Message published')
