#!/usr/bin/env python
""" This service listens to the Azure service bus and fires off Argo
when we recieve a message to do so. This decouples argo..."""
# pylint: disable=logging-fstring-interpolation
import logging
import os
import json
import sys

import tempfile

import subprocess
from subprocess import PIPE  # For python 3.6

from azure.servicebus import QueueClient
from azure.servicebus.common.errors import ServiceBusError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production.")

# if True we allow the MQ to shutdown the process by sending "action: shutdown" over the MQ.
MQ_SHUTDOWN = False

UUIDERROR = 10
ARGOERROR = 11
SBERROR = 12


def create_param_file(params):
    """ Create a parameter YAML-file for Argo to ingest.
        This file contains the workflow parameters referenced in the workflow.

     """
    tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    logging.debug('Creating PARAM file for ARGO')
    for key in params:
        logging.info(f'Param set: {key}: {params[key]}')
        print(f"{key}: {params[key]}", file=tmpfile)
    return tmpfile.name

# TODO få inn en .env variabel for miljø her. da-mottak-dev er hardkodet
def argo_submit(workflowfile, params, namespace):
    """ Submit a job to argo. Takes a YAML file as parameter """
    paramfile = create_param_file(params)
    argocmd = ["argo", "submit", "--namespace", namespace, "--parameter-file", paramfile, workflowfile]
    logging.info(f"Argo cmd line: {argocmd}")
    try:
        submit = subprocess.run(argocmd, timeout=20, check=True, stdout=PIPE, stderr=PIPE)
        if not submit.returncode == 0:
            logging.error("Argo submit failed")
            if submit.stderr:
                logging.error(f"Stderr: {submit.stderr.decode('utf-8')}")
            if submit.stdout:
                logging.error(f"Stdout: {submit.stdout.decode('utf-8')}")
            sys.exit(ARGOERROR)
    except subprocess.CalledProcessError as exception:
        logging.error(f"Invoking argo client: {exception}")
        logging.error(f"Stderr: {exception.stderr.decode('utf-8')}")

    os.remove(paramfile)


def runq():
    """ The main loop that listens to the service bus"""

    conn_str = os.getenv('AZ_SB_CON_KICKER')
    queue = os.getenv('AZ_SB_QUEUE')
    namespace = os.getenv('NAMESPACE')
    try:
        # Note: This is lazy.
        queue_client = QueueClient.from_connection_string(
            conn_str, queue)
        logging.info(queue_client.get_properties())  # This tests if we're actually connected.
    except ServiceBusError as exception:
        logging.error(f'Failed to connect or use queue "{queue}" using "{conn_str}"')
        logging.error(exception)
        sys.exit(SBERROR)

    logging.info(f'Service bus connection to {queue} is OK')

    keep_running = True
    with queue_client.get_receiver() as queue_receiver:
        while keep_running:
            messages = queue_receiver.fetch_next(timeout=3)
            for message in messages:
                logging.info('Got a message on the service bus')
                # message is a generator. fetch the content, decode it and concat it:
                msg = ''.join(map(lambda x: x.decode('utf-8'), message.body))
                logging.info(f'Got a message on the service bus: {msg}')

                parsed = json.loads(msg)

                # Here we actually look at the message and decide what to do with it.
                if parsed["action"] == 'argo-submit-overforingspakke':
                    logging.info('Got an argo submission of an overforingspakke. Submitting.')
                    argo_submit(workflowfile=os.getenv('WORKFLOW'), params=parsed['params'], namespace=namespace)
                elif parsed["action"] == 'shutdown':
                    if not MQ_SHUTDOWN:
                        logging.info('Ignoring shutdown message.')
                    else:
                        logging.info('Got a shutdown message. Closing down.')
                        keep_running = False
                message.complete()
    print('Closing receiver')


if __name__ == '__main__':
    # print(get_workflows(argo))
    logging.basicConfig(level=logging.INFO)
    logging.info('kicker starting up.')
    logging.getLogger("uamqp").setLevel(logging.WARNING)
    runq()
