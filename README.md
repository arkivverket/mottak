# Archive Ingress Processing Application for Norways National Archives

Prototype application for recieving archives and processing them so they can later be put into storage.

The application allow someone to upload a [DIAS](https://www.arkivverket.no/forvaltning-og-utvikling/regelverk-og-standarder/dias-prosjektet-digital-arkivpakkestruktur)-encapsulated archieve into an objectstore. 

## Workflow outline
 - Agreement is reached on transfer of an archive
 - Archive is created. The external METS XML document is sent over to an executive officer
 - The executive offiser uses the invitation UI (runs in the invation container) to send an invitation to upload. This is sent through email, using mailgun.
 - The creator of the archive clicks the link. This invokes the [archive uploader](https://github.com/arkivverket/archive-uploader). The creator selects the created archive and uploads it.
 - The tusd container will first run the pre-upload hook an verify that there is a valid invitation for the upload.
 - Once the upload is complete the post-upload hook is run. This invokes Argo and fires off the Argo Workflow DAG.
 - The Argo Workflow will:
   - Verify the checksum of the archive
     - If the checksum doesn't match the archive is deleted and the creator is notified
   - Run antivirus on the archive
   - Unpack the archive into a new blob storage container
   - Pass the archive to the arkade5 container, which will generate a HTML-based report
   - invoke the logging container to send all the artifacts generated to the archive log service.
   - Send off an email to $SOMEBODY that there is a new archive available for further processing. Attached to the email is the log from the antivirus as well as the report generated by Arkade
  

## Requirements
 - docker containers for each component.
 - Kubernetes with Argo for workflow processing
 - Postgresql for metadata for invitations
 - Objectstore for archieves - we're using Azure Blob Storage but adding support for others is resonable simple, thanks to libcloud.

## How to setup a new enviroment

 - get a kubernetes cluster and make sure kubectl is operational
 - make sure the cluster has akv2k8s running so we can get to the secrets
 - create a namespace: ```kubectl create name namespace mottak```
 - install argo into the namespace
 - use helm to install mottak into the namespace
 - Allocate an IP address
 - Get some TLS certs. You'll need two, one for invitation and one for tusd
 - Set up an ingress controller (I used nginx installed though Helm), make the TLS certs available to it
 - Get mailgun credentials so you can get outbound mail
 - allocate API key for the log archive service
 
At this point everything should work.

## Secrets used 

We assume the following secrets are in your vault.

| secret name                | format                               | used by                                     |
| archive-log-service-apikey | random string (no funny characters)  | archive-log-service and the logger          |
| archive-log-service-dsn    | psycop2 connection url               | archive-log-service                         |
| invitation-secret          | random string                        | internally in invitation (protect from XSS) |
| mailgun-secret             | whatever mailgun gives you           | invitation, mailer                          |
| mottakmvp-dsn              | PHP DB DSN (key/value)               | invitation, tusd-hooks                      |
| storage-key                | What Azure gives you                 | s3-*, arkade, tusd                          |
| storage-user               | What Azure gives you.                | s3-*, arkade, tusd                          |

## How to make sure this thing works

In order to make sure this works you can do the following.

 - Get yourself a NOARK5 archive. Get the METS-file (external METS)
 - Upload it to the invitation UI
 - Click the link in your email
 - Upload the archive
 - You can now run "argo list" and see if the archive is being processed
   - argo logs $job will give you progress
 - You should now get a message that a new archive has been processed with some attachments


## For devs and ops ppl:

You can view the Argo UI by setting up a kube proxy:

kubectl -n argo port-forward deployment/argo-ui 8001:8001

Then visit http://localhost:8001/ to view the UI.


## Deploying manually with Helm

To deploy the mottak Helm Charts with Helm _manually_ (work in progress), do the following:

* Make sure that your kubectl context points to the cluster you want to deploy to.

* Check what is already there with the command:

    helm ls -aA
    
* Find out which deploy-time parameters you need to set for each chart. Put these in a file called `values.yaml`.

E.g.:

```
invitation:
  mailgun_domain: ...
  upload_url: ...

tusd:
  other stuff

...
```

* Run the helm command against the cluster:

    helm upgrade --install --namespace mottak --wait mottak.mottak path/to/mottak/toplevel/helm/chart --values values.yaml
