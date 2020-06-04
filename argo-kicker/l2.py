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



async def runq():
    client = ServiceBusClient.from_connection_string(os.getenv('AZURE_SB_STR'))
    queue_client = client.get_queue('taskqueue')

    keep_running = True
    async with queue_client.get_receiver(idle_timeout=1) as receiver:
        while keep_running:
            if receiver.queue_size == 0:
                print('Zero messages')
                await asyncio.sleep(1)
                continue

            print('Fetching')
            # Receive list of messages as a batch
            next = await receiver.fetch_next(max_batch_size=1, timeout=1)
            print('Gathering....')
            await asyncio.gather(*[m.complete() for m in next])
            # Receive messages as a continuous generator
            print('Processing messages....')
            async for message in receiver:
                print("Message: {}".format(message))
                print("  Sequence number: {}".format(message.sequence_number))
                await message.complete()
                if message == 'shutdown':
                    print('Stopping now.')
                    keep_running = False
    print('Closing receiver')
        


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(runq())
        loop.run_forever()
    finally:
        print("Finally!")