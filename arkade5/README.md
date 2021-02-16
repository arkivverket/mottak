## Arkade5

This container analyze if the uploaded archive is in accordance with the current archive standards.

It uses the application [Arkade5](https://arkade.arkivverket.no/) for doing the analysis, and the output is stored in
`/tmp` where the argo workflow can pick it up and use it for logging purposes.
Uploading an archive that fails the current standard will not abort the rest of the uploading process.
Errors in Arkade5 will be manually handled by the coordinator in charge.

The current solution supports Azure Blob Storage.

The pods mounts the storage container using Goofys. In order to FUSE-mount it needs the SYS_ADMIN privilege.

The reason we use Goofys and not Blobfuse is 1) it doesn't rely on local caching in order to work,
we'll quickly run out of storage if there are big files and 2) performance with Goofys is better.

### Environment variables

* ARCHIVE_BUCKET, the bucket/container where the archive is stored
* ARKIV_TYPE, supported [archive types](http://docs.arkade.arkivverket.no/no/latest/Brukerveiledning.html#innlasting)
* AZURE_STORAGE_ACCOUNT, Azure values used by [Goofys](https://github.com/kahing/goofys/blob/master/README-azure.md) to access stored archive
* AZURE_STORAGE_KEY

The values given here are examples
```yaml
- ARCHIVE_BUCKET=43c9ea13-afba-4e42-80e7-5d8deaa6edff-0
- ARKIV_TYPE=SIARD
- AZURE_STORAGE_ACCOUNT=myazureaccdev
- AZURE_STORAGE_KEY=<secret>
```

## Running locally
Create a `.env` in root and add the needed env variables with correct values.
Run the container with:

```shell
docker run --privileged --env-file=.env <image>
```
