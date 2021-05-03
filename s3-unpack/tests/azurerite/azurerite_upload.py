#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple script to upload file to Azurite Blob Storage"""

import os
import sys
import uuid

from azure.storage.blob import ContainerClient, BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from dotenv import load_dotenv

load_dotenv()

try:
    file_path = sys.argv[1]
except Exception:
    print("Missing file path in arguments")
    print("Usage: azurite_upload.py /path/to/tar/file.tar")
    exit(1)

default_conn_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

conn_str = os.getenv("AZURITE_STORAGE_CONNECTION_STRING", default_conn_str)
container_name = os.getenv("BUCKET", "tusd-storage")
blob_name = os.getenv("TUSD_OBJECT_NAME", str(uuid.uuid4()))

if "devstoreaccount1" not in conn_str:
    print(
        "'devstoreaccount1' not found in AZURE_STORAGE_CONNECTION_STRING. Are you sure you're trying to connect to Azurite?"
    )
    sys.exit(1)

container_client = ContainerClient.from_connection_string(
    conn_str,
    container_name=container_name,
)

print(conn_str)

try:
    container_client.create_container()
except ResourceExistsError:
    pass


blob = container_client.get_blob_client(blob=blob_name)

try:
    blob.delete_blob()
except ResourceNotFoundError:
    pass


print(f"Uploading {file_path}")
print(f"container_name={container_name}, blob_name={blob_name}")
with open(file_path, "rb") as data:
    blob.upload_blob(data)
