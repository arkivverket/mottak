## Delete

This container is used to delete an object in the objectstore.

Invoked by Argo whenever Argo decides something needs to die.
When invoked by Argo it means the workflow has failed and the transferred archive must be manually controlled before
it is re-submitted to the application. This container will remove the received tar-file from the tusd-storage container.

### Environment variables needed
The values given here are examples or hints.
All are used when deleting an object using ArkivverketObjectStorage from [py-objectstore](https://github.com/arkivverket/py-objectstore)
```yaml
- TUSD_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- OBJECTSTORE=abs
- BUCKET=bucket-storage
- AZURE_ACCOUNT=myazureaccdev
- AZURE_KEY=secret
```
