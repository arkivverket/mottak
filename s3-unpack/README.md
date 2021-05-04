# Unpack

This container takes a tar file in Azure Blob Storage, streams it and unpacks it on the fly into a new container on
Azure Blob Storage.

It creates a log of the operation that argo can pick up as an artifact.


## Environment variables

The values given here are examples.

### Required env variables

```dotenv
- SOURCE_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- SOURCE_BUCKET=bucket-storage
- TARGET_BUCKET_NAME=ee2af706-117f-43e3-98de-59db2cc6f231
- AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=**********;AccountKey=**********;EndpointSuffix=core.windows.net

```

### Optional env variables
```dotenv
- OUTPUT_PATH_LOG="/tmp/unpack.log"
- MAX_CONCURRENCY="4"
- BUFFER_SIZE="4194304"
```

## Running locally

### Prerequisites
Create `.env` file in [root folder](.) containing env variables, use [`.env.default`](.env.default) as a template.

### With Azurite

`s3-unpack` supports testing against [Azurite](https://github.com/Azure/Azurite)

```console
docker run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite azurite-blob --blobHost 0.0.0.0 --loose
```

Set your `AZURE_STORAGE_CONNECTION_STRING` in `.env` to this string. Replace `127.0.0.1` if you run it on another host.

```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;
```

Upload a tar file to Azurite with [azurerite_upload](tests/azurerite/azurerite_upload.py). If you are running Azurite on a different host, set the `AZURITE_STORAGE_CONNECTION_STRING` enviornment variable.

Run s3-unpack
