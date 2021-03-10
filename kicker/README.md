# Kicker

This container listens on a queue where it receives messages from the Tusd container.
A message is in essence a request to process an uploaded archive (tar-file) that is stored in the tusd container,
by controlling for [virus](https://github.com/arkivverket/mottak/tree/develop/s3-scan-tar),
checking that the [checksums](https://github.com/arkivverket/mottak/tree/develop/s3-checksum256) match before and after the transmission,
and [unpack](https://github.com/arkivverket/mottak/tree/develop/s3-unpack) the tar-file into its original archive format and store it in Azure Blob Storage.
Lastly it will also run the unpacked archive through [Arkade5](https://github.com/arkivverket/mottak/tree/develop/arkade5)
to see if the archive is in accordance with the current archive standards.

We use [Argo Workflows](https://argoproj.github.io/projects/argo) where each step in the DAG is done by invoking a container
running a component from the [arkivverket/mottak](https://github.com/arkivverket/mottak) repo.

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


### Environment variables needed
```yaml
- AZ_SB_CON_KICKER=Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=argo-kicker;SharedAccessKey=<secret>
- AZ_SB_QUEUE=argo-workflow
- WORKFLOW=/opt/workflows/<name-of-workflow>
- NAMESPACE=da-mottak-<env>
- AVSCAN_TAG=<image tag for component 's3-scan-tar'>
- MAILER_TAG=<image tag for component 'mailer'>
```
