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

AZ_SB_CON_KICKER = os.getenv('AZ_SB_CON_KICKER')
AZ_SB_QUEUE = os.getenv('AZ_SB_QUEUE')


# Edit the values in this method
def get_params() -> dict:
    return {
        'TUSD_OBJEKT_NAVN': "6bf65f3c3700f1152d4429f3d6599e8c",
        'EKSTERN_ID': "c574653e-f58c-4efe-b670-afe6fabea715",
        'SJEKKSUM': "55a6b7b3f4d1bf2377af2a0f591106ff2df5a4e9d7699f6f5e38cadf2d738fda",
        'KOORDINATOR_EPOST': "marelm@arkivverket.no",
        'ARKIVUTTREKK_OBJ_ID': "38da4005-92de-4aea-81ac-2262f90d0f5b"
    }


def create_message(params: dict) -> dict:
    return {
        'action': 'argo-verify-overforingspakke',
        'params': params,
    }


def send_message(message: dict):
    m = Message(json.dumps(message).encode('utf8'))
    client.send(m)


def create_queue_client(queue_client_string: str, queue_name: str) -> QueueClient:
    return QueueClient.from_connection_string(queue_client_string, queue_name)


if __name__ == '__main__':
    print(f'Creating queue client for {AZ_SB_QUEUE}')
    client = create_queue_client(AZ_SB_CON_KICKER, AZ_SB_QUEUE)
    message = create_message(get_params())
    print(f'Publishing {message} to kicker queue')
    send_message(message)
    print('Message published')
