## Unpack

This container takes a tar file in Azure Blob Storage, streams it and unpacks it on the fly into a new container on
Azure Blob Storage.

It creates a log of the operation that argo can pick up as an artifact.


### Environment variables
The values given here are examples where we have chosen Azure blob storage as objectstore
```yaml
- SOURCE_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- SOURCE_BUCKET=bucket-storage
- TARGET_BUCKET_NAME=ee2af706-117f-43e3-98de-59db2cc6f231
- AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=**********;AccountKey=**********;EndpointSuffix=core.windows.net
- OUTPUT_PATH_LOG= Optional, defaults to "/tmp/unpack.log"
- MAX_CONCURRENCY= Optional, defaults to 4
- BUFFER_SIZE= Optional, defaults to blob.DEFAULT_BUFFER_SIZE
```
