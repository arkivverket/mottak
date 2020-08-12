#!/usr/bin/env python

from azure.servicebus import QueueClient, Message
from azure.servicebus.common.constants import ReceiveSettleMode

import logging
import os
import json

import tempfile

import subprocess
from subprocess import PIPE  # For python 3.6

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production.")

MQ_SHUTDOWN = False # if True we allow the MQ to shutdown the process by sending action: shutdown over the MQ.

UUIDERROR = 10
ARGOERROR = 11
SBERROR = 12


def create_param_file(params):
    """ Create a parameter YAML-file for Argo to ingest.
        This file contains the workflow parameters referenced in the workflow.

     """
    tmpfile = tempfile.NamedTemporaryFile(mode='w',delete=False)
    logging.debug('Creating PARAM file for ARGO')
    for key in params:
        logging.info(f'Param set: {key}: {params[key]}')
        print(f"{key}: {params[key]}", file=tmpfile)
    return tmpfile.name


def argo_submit(workflowfile,params):
    """ Submit a job to argo. Takes a YAML file as parameter """
    paramfile = create_param_file(params)
    argocmd = ["argo", "submit", "--parameter-file", paramfile, workflowfile]
    logging.info(f"Argo cmd line: {argocmd}")
    submit = subprocess.run(argocmd, timeout=20, stdout=PIPE, stderr=PIPE)
    # stupid debugging hack to avoid spamming argo.
    #submit = subprocess.run("ls", timeout=20, stdout=PIPE, stderr=PIPE)
    if not (submit.returncode == 0):
        logging.error("Argo submit failed")
        if submit.stderr:
            logging.error(f"Stderr: {submit.stderr.decode('utf-8')}")
        if submit.stdout:
            logging.error(f"Stdout: {submit.stdout.decode('utf-8')}")
        exit(ARGOERROR)
    os.remove(paramfile)


def runq():
    conn_str = os.getenv('AZ_SB_CON_KICKER')
    queue = os.getenv('AZ_SB_QUEUE')
    try:
        queue_client = QueueClient.from_connection_string(
            conn_str, queue)
    except Exception as e:
        logging.error(f'Failed to connect to "{queue}" using "{conn_str}"')
        logging.error(e)
        exit(SBERROR)

    logging.info('Service bus connection to {queue} is OK')

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
                if parsed["action"] == 'argo-submit':
                    logging.info('Got a argo submission. Submitting.')
                    argo_submit(workflowfile=os.getenv('WORKFLOW'), params=parsed['params'])
                elif parsed["action"] == 'shutdown':
                    if not MQ_SHUTDOWN:
                        logging.info('Ignoring shutdown message. Enable MQ shutdown in the code to ... enable this.')
                    else:
                        logging.info('Got a shutdown message. Closing down.')
                        keep_running = False
                message.complete()
    print('Closing receiver')


if __name__ == '__main__':
    # print(get_workflows(argo))
    logging.basicConfig(level=logging.INFO )     # format='%(asctime)s %(levelname)s %(message)s'                        
    logging.info('kicker starting up.')
    logging.getLogger("uamqp").setLevel(logging.WARNING)
    runq()