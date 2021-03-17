#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scans a tar archive stored in a objectstore """

import os
import sys
import logging
import tarfile

from collections import namedtuple
from pyclamd import ClamdUnixSocket
from pyclamd.pyclamd import ConnectionError, BufferTooLongError
from typing import Tuple
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

from app.blob import Blob, DEFAULT_BUFFER_SIZE
from app.utils import sizeof_format, wait_for_port, fix_encoding

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")

MEGABYTES = 1024 ** 2
UINT_MAX = 2 ** 32 - 1

# Exit values
UNKNOWNERROR = 1
AZUREERROR = 2
OBJECTERROR = 3
CLAMAVERROR = 10


def stream_tar(stream: Blob) -> tarfile.TarFile:
    """Takes a Blob stream and opens it as a tarfile

    :param Blob stream: the incoming

    :returns TarFile: opened tarfile ready for interaction

    :raises Exception: if an error is encountered
    """
    try:
        tar_file = tarfile.open(fileobj=stream, mode="r")
    except Exception as exception:
        logging.critical(f"Failed to open stream to object {stream.client.container_name}/{stream.client.blob_name}")
        logging.critical(f"Error: {exception}")
        raise exception
    return tar_file


def scan_archive(blob: Blob, clamd_socket: ClamdUnixSocket, buffer_size: int) -> Tuple[int, int, int]:
    """Takes a Blob stream and opens it as a tarfile and iterates over the files.
    Each file is passed on to clamd for antivirus scan. If the the files is greater
    than the 4GB limit, it is skipped, and the Blob stream is fast-forwarded to
    the next file

    A larger buffer_size might slow down the scanning, as it has to download more
    of each file if they are >4GB before it can iterate further

    :param Blob blob: the incoming blob stream
    :param ClamdUnixSocket clamd_socket: ClamAV socket to connect to
    :param int buffer_size: how much of the stream to store in memory

    :returns Tuple[int, int, int]: a named tuple of the scan resutls (clean, virus, skippd)

    :raises Exception: when an unkown error is encountered
    """
    clean, virus, skipped = 0, 0, 0
    tar_file = stream_tar(blob)

    for member in tar_file:
        file_name = fix_encoding(member.name)
        # The file is larger than the ClamAV max file size (4GiB)
        if member.size > UINT_MAX:
            skipped += 1
            logging.warning(
                f"Skipping {file_name} ({sizeof_format(member.size)}) because it exceeds the {sizeof_format(UINT_MAX)} size limit"
            )
            continue

        tar_member = tar_file.extractfile(member)
        if tar_member is None or member.size == 0:
            # Handle is none - likely a directory.
            logging.debug(f"Handle ({file_name}) is none. Skipping...")
            continue
        try:
            logging.info(f"Scanning {file_name} at {sizeof_format(member.size)}...")
            result = clamd_socket.scan_stream(stream=tar_member, chunk_size=buffer_size)

            # No viruses found
            if result is None:
                clean += 1
                logging.info(f"clean  - {file_name}")
            else:
                virus += 1
                logging.critical(f'Virus found! {result["stream"][1]} in {file_name}')

        except BufferTooLongError:
            skipped += 1
            logging.error("clamd reset the connection. Increase max scan size for clamd.")
            logging.warning(f"SKIPPED (File too big) - {file_name}")
            continue
        except ConnectionError as exception:
            skipped += 1
            logging.critical(f"A connection error occured with clamd while scanning {file_name}")
            logging.critical(exception)
            continue
        except Exception as exception:
            logging.error(f"Failed to scan {file_name}")
            logging.error(exception)
            raise exception

    logging.debug(f"clean: {clean}, virus: {virus}, skipped: {skipped}")
    ret = namedtuple("scan", ["clean", "virus", "skipped"])
    return ret(clean, virus, skipped)


def main() -> None:
    """ Run from here, really """
    logging.basicConfig(level=logging.INFO, filename=os.getenv("AVLOG", "/tmp/avlog"),
                        filemode="w", format="%(asctime)s | %(levelname)s | %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.ERROR)
    logging.info("Starting s3-scan-tar")

    # Also known as a Container in Azure Blob Storage
    bucket = os.getenv("BUCKET")
    objectname = os.getenv("TUSD_OBJECT_NAME")
    buffer_size = int(os.getenv("BUFFER_SIZE", DEFAULT_BUFFER_SIZE))
    max_concurrency = int(os.getenv("MAX_CONCURRENCY", 4))

    # Test the access to the object stream, so we can return early if there are any issues
    logging.info("Initialising connection to Azure Blob Storage")
    try:
        blob = Blob(
            BlobClient.from_connection_string(
                conn_str=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
                container_name=bucket,
                blob_name=objectname,
            ),
            max_concurrency,
            buffer_size,
        )
        logging.info(f"Connected to Azure with API version {blob.client.api_version}")
    except ResourceNotFoundError:
        logging.critical(f"An error occured while getting the object handle {objectname} in bucket {bucket}")
        sys.exit(OBJECTERROR)
    except ClientAuthenticationError:
        logging.critical("An error occured while connecting to Azure, please check the credentials")
        sys.exit(AZUREERROR)
    except Exception as exception:
        logging.critical("Unkown error occured while getting the object")
        logging.critical(exception)
        sys.exit(UNKNOWNERROR)

    # Starts freshclamd daemon, which allows the databases to be updated while running, if the scanning takes a while
    logging.info("Refreshing ClamAV signatures")
    os.system("freshclam -d")

    # Starts clamd in the background (eventhough we run clamd in the foreground)
    logging.info("Starting ClamAV")
    os.system("clamd &")

    logging.info("Initialising connection to clamd")
    try:
        wait_for_port(3310)
        clamd_socket = ClamdUnixSocket()
        logging.info(f"Connected to clamd version {clamd_socket.version()}")
    except TimeoutError as exception:
        logging.critical(exception)
        sys.exit(CLAMAVERROR)
    except FileNotFoundError as exception:
        logging.critical("Could not find a clamd socket")
        logging.critical(exception)
        sys.exit(CLAMAVERROR)
    except ConnectionError as exception:
        logging.critical("Could not connect to clamd socket")
        logging.critical(exception)
        sys.exit(CLAMAVERROR)

    logging.info(f"Initialising scan on {bucket}/{objectname} with a scan limit of {sizeof_format(UINT_MAX)}")
    logging.info(f"Buffer size is set to {sizeof_format(buffer_size)}")
    scan_ret = scan_archive(blob, clamd_socket, buffer_size)

    logging.info(f"{scan_ret.clean} files scanned and found clean")
    logging.info(f"{scan_ret.virus} viruses found")
    logging.info(f"{scan_ret.skipped} files skipped")
    logging.info("Archive scanned - exiting")


# ===========================================================================
# Run from here.
# ===========================================================================
if __name__ == "__main__":
    main()
