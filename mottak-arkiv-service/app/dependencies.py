from app.connectors.azure_servicebus.azure_servicebus_client import AzureServicebus
from app.connectors.connectors_variables import get_sender_con_str, get_status_con_str, REQUEST_SENDER_QUEUE_NAME, STATUS_RECEIVER_QUEUE_NAME


def create_request_sender_queue() -> AzureServicebus:
    return AzureServicebus(get_sender_con_str(), REQUEST_SENDER_QUEUE_NAME)


def create_status_receiver_queue() -> AzureServicebus:
    return AzureServicebus(get_status_con_str(), STATUS_RECEIVER_QUEUE_NAME)
