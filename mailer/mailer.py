#!/usr/bin/env python
""" Simple service container to send email in a k8s application """

# pylint: disable=logging-fstring-interpolation
import os
import logging
import glob
import requests

from _version import __version__

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Could not load dotenv. No worries")

ENVERROR = 10


def verify_environment():
    """Verify that the required environment variables are set.
    exits if is unhappy.
    """
    reqs = ['NAME', 'RECIPIENT', 'SUBJECT', 'MESSAGE',
            'MAILGUN_API_KEY', 'MAILGUN_DOMAIN']
    for req in reqs:
        if not os.getenv(req):
            raise ValueError('Environment variable ' + req + ' is not set')


def find_attachments(path):
    """ Returns a list of files at the given path """
    files = []
    if path and os.path.isdir(path):
        files = glob.glob(path + "/*")
        return files
    return files


def process_message(msg):
    """ Evaluate the string msg. If it starts with a / then we assume
    it is a path and load that file """
    if msg and os.path.isfile(msg):
        msg = open(msg, "r").read()
    return msg


def send_message(name, recipient, subject, message, attachments):
    """ Invoke the mailgun api """
    logging.info(f"Sending message to '{name}' <{recipient}>")
    logging.info(f"Subject is '{subject}'")
    logging.info(f"Message is '{message}'")
    logging.info(
        "Message has attachments" if attachments else "No attachments")
    ret = requests.post(
        "https://api.mailgun.net/v3/%s/messages" % os.getenv('MAILGUN_DOMAIN'),
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": "The Mailgun <donotreply@%s>" % os.getenv('MAILGUN_DOMAIN'),
              "to": [name, recipient],
              "subject": subject,
              "text": message},
        files=attachments)
    ret.raise_for_status()
    logging.info(f'Status code: {ret.status_code}')
    logging.info(f'Status message: {ret.text}')


def main():
    """ Run from here """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info(f'{__file__} version {__version__} running')
    # Check that we got what we need to run:
    verify_environment()

    # Map environment into Python:
    recipient = os.getenv('RECIPIENT')
    name = os.getenv('NAME')
    message = os.getenv('MESSAGE')
    subject = os.getenv('SUBJECT')
    files = find_attachments(os.getenv('ATTACHMENTS'))
    if files:
        logging.info(f"Attachments: {files}")

    # Process the message. If it starts with a / we load the file.
    message = process_message(message)

    # Transform the file list into something like this:
    #        files=[("attachment", ("test.jpg", open("files/test.jpg","rb").read())),
    #               ("attachment", ("test.txt", open("files/test.txt","rb").read()))],
    attachments = list(
        map(lambda file:
            ('attachment', (os.path.basename(file), open(file, "rb").read())), files)
    )
    send_message(recipient=recipient, name=name, subject=subject,
                 message=message, attachments=attachments)


if __name__ == '__main__':
    main()
