#!/usr/bin/env python
from azure.servicebus import QueueClient, Message

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production.")


print('Connection string: ', os.getenv('AZURE_SB_STR'))

queue_client = QueueClient.from_connection_string(os.getenv('AZURE_SB_STR'), "taskqueue")
# Send a test message to the queue
msg = Message(b'Test Message')
queue_client.send(msg)
print('Message sent')
