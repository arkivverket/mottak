# Arkade5

This step runs Arkade5 on an archive and creates a report which is picked up by Argo and stored as an artifact.

It needs the following environment variables set:

    * UUID, the obj id of the archive
    * ARCHIEVE_TYPE, type of archive, ie Noark3
    * INVITATIONID, the name of the Azure Blob Storage container containing the archive
    * AZURE_ACCOUNT, Azure Storage account
    * AZURE_STORAGE_KEY, Azure Storage account key

The pods mounts the storage container using Goofys. In order to FUSE-mount it needs the SYS_ADMIN privilege.

The reason we use Goofys and not Blobfuse is 1) it doesn't rely on local caching in order to work, we'll quickly run out of storage if there are big files and 2) performance with Goofys is better.

The report is dumped in /tmp where Argo picks it up.

## Running locally
Create a `.env` in root and add the needed env variables with correct values.
Run the container with:
`docker run --privileged --env-file=.env <container_name>`
