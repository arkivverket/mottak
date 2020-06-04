# Arkade5

This step runs Arkade5 on an archive and creates a report which is picked up by Argo and stored as an artifact.

It needs the following environment variables set:
 * $CONTAINER, the container which contains the unpacked archive to be processed.
 * $UUID, the ID of the archive.
 * $AZURE_STORAGE_ACCOUNT
 * $AZURE_STORAGE_KEY

The pods mounts the storage container using Goofys. In order to FUSE-mount it needs the SYS_ADMIN privilege. 

The reason we use Goofys and not Blobfuse is 1) it doesn't rely on local caching in order to work, we'll quickly run out of storage if there are big files and 2) performance with Goofys is better.

The report is dumped in /tmp where Argo picks it up.