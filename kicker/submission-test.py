# import asyncio
from azure.servicebus import QueueClient, Message
# from azure.servicebus import ServiceBusClient, Message

import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production.")

print('Connection string: ', os.getenv('AZ_SB_CON_KICKER'))


def send_batch():
    params = {
        'UUID': 'df53d1d8-39bf-4fea-a741-58d472664ce2',
        'OBJECT': '8ce0f19f7644ebfa4ec1cdda8803a2db',
        'CHECKSUM': '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a',
        'ARCHIEVE_TYPE': 'noark5',
        'NAME': 'Per Buer',
        'EMAIL': 'perbue@arkivverket.no',
        'INVITATIONID': 2
    }

    message = {
        'action': 'argo-submit',
        'params': params,
    }

    shutdown = {
        'action': 'shutdown'
    }

    queue_client = QueueClient.from_connection_string(
        os.getenv('AZ_SB_CON_KICKER'), os.getenv('AZ_SB_QUEUE'))

    with queue_client.get_sender() as sender:
        message = Message(json.dumps(message).encode('utf8'))
        print('Sending message: ', message)
        ret = sender.send(message)
        print('ret:', ret)
        message = Message(json.dumps(shutdown).encode('utf8'))
        print('Sending message: ', message)
        ret = sender.send(message)
        print('Ret:', ret)


if __name__ == '__main__':
    print('Sending messages....')
    send_batch()
