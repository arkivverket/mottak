import asyncio


from azure.servicebus.aio import ServiceBusClient, Message
from azure.servicebus.common.constants import ReceiveSettleMode

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production.")

print('Connection string: ', os.getenv('AZURE_SB_STR'))

async def send_batch():
    client = ServiceBusClient.from_connection_string(os.getenv('AZURE_SB_STR'))

    queue_client = client.get_queue('taskqueue')
    async with queue_client.get_sender() as sender:
        for i in range(2):
            message = Message("Sample message no. {}".format(i))
            print('Sending message: ', message)
            await sender.send(message)
        print('Sending message: shutdown')
        await sender.send(Message("shutdown"))

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_batch())
    finally:
        print("Finally!")