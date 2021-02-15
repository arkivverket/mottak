## Unpack

This container takes a tar file in an objectstore, streams it and unpacks it on the fly into another objectstore.

It creates a log of the operation that argo can pick up as an artifact.

Inputs:
 * TUSD_OBJECT_NAME, the object to be unpacked
 * TARGET_BUCKET_NAME, the name of the bucket where the object will be unpacked into
 * The remaining variables are used when downloading and uploading objects with ArkivverketObjectStorage
   from [py-objectstore](https://github.com/arkivverket/py-objectstore)

### Environment variables
The values given here are examples where we have chosen Azure blob storage as objectstore
```yaml
- TUSD_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- TARGET_BUCKET_NAME=ee2af706-117f-43e3-98de-59db2cc6f231-0
- OBJECTSTORE=abs
- BUCKET=bucket-storage
- AZURE_ACCOUNT=myazureaccdev
- AZURE_KEY=secret
```
