# kicker

Kicker listens to the service bus is Azure and fires off the Argo client to initiate running the DAGs.

Supported DAGs:
 - submit-archive

Planned dags:
 - deploy-decom
   - create an objectstore (container) named $UUID.tfstate
   - create a fileshare ($UUID.fileshare)
   - copy the contents of the archive using az-copy
   - run the terraform-container
   - tell the user the VM is go
 - destroy-decom
   - tf destroy
   - delete the objectstore
 - submit-to-preservation
   - get a SAS-ticket to the objectstore in question.
   - send a MQ message to preservation ("bevaring") with the UUID
   - note that the archive is send to preservation
 - delete preserved archive
   - remove object stores that have been sent to preservation.

This decouples running the DAG.


## Testing in dev
There is a small script [kicker-trigger](tests/kicker-trigger) that puts a message on the service bus queue in dev.
This can be used to trigger kicker and argo in dev.
Env variables needed:
- `QUEUE_CLIENT_CONNECTION_STRING="Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=argo-kicker;SharedAccessKey=<secret>"`
- `QUEUE_NAME="argo-workflow"`
