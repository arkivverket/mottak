#!/usr/bin/env python

# For blob stuff:
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import AccountSasPermissions, generate_container_sas

# service bus.
from azure.servicebus import QueueClient, Message
from azure.servicebus.common.constants import ReceiveSettleMode

# generic stuff
import json
import os
import logging

# return codes
SBERROR = 10
SASERROR = 11


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('Did not load env file.')


def get_service_url(account):
    return f"https://{account}.blob.core.windows.net"


def generate_sas(client, container):
    sas_token = generate_container_sas(
        client.account_name,
        container_name=container,
        account_key=client.credential.account_key,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return sas_token


def generation_action(token, bucket, account):
    """ Generate JSON with the SAS token"""
    obj = {
        'action': 'transfer',
        'container': bucket,
        'account': account,
        'sas_token': token
    }
    return json.dumps(obj)


def send_message(q_client, message):
    # Encode the string and generate a message object:
    m = Message(message.encode('utf8'))

    with q_client.get_sender() as sender:
        ret = sender.send(m)
        if not ret:
            logging.info(f'Message sent - OK')
        else:
            logging.warning(f'Message send returned {ret}')
    return ret


def main():
    logging.basicConfig(level=logging.WARNING)

    account = os.getenv('AZURE_ACCOUNT')
    key = os.getenv('AZURE_KEY')
    bucket = os.getenv('BUCKET')
    try:
        queue_client = QueueClient.from_connection_string(
            os.getenv('AZ_SB_CON_KICKER'), os.getenv('AZ_SB_QUEUE'))
        logging.info('Connected to the message queue')
    except Exception as e:
        logging.error(f'Could not connect to the azure service bus: {e}')
        exit(SBERROR)
    try:
        blob_service_client = BlobServiceClient(account_url=get_service_url(account),
                                                credential=key)
        logging.info('Connected to the blob service')

    except Exception as e:
        logging.error(f'Could not initiate connection to blob storage: {e}')
        exit(SASERROR)

    token = generate_sas(blob_service_client, bucket)
    j = generation_action(token, bucket, account)
    logging.info(f'Message generated: {j}')
    parsed = json.loads(j)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    try:
        send_message(queue_client, j)
    except Exception as e:
        logging.error(f'Could not send message: {e}')


if __name__ == "__main__":
    main()
