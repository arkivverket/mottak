## Checksum

This container verifies the checksum of an arbitrary file in the objectstore.

It leaves it's verdicts in /tmp/result which is picked up by Argo and used to control the workflow.

Todo:
 * We should generate a proper log artifact that can be logged to the archive-log-service for posterity.
 * Make RESULT and LOG into environment variables

### Environment variables needed
The values given here are examples
- OBJECT_NAME='ok63e2f0-39bf-4fea-a741-58d472664ce2'
- CHECKSUM='5cgdde307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a'
- OBJECTSTORE='abs'
- BUCKET='bucket-storage'
- AZURE_ACCOUNT='myazureaccdev'
- AZURE_KEY='secret'
