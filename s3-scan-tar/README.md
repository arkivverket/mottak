# Scan-tar

This container performs an antivirus-scan on an object read from objectstorage.

The container does a streaming read of a tar-file (object in objectstorage)
and feeds each element of it to [ClamAV](https://www.clamav.net/) over a socket.

## Environment variables

* TUSD_OBJECT_NAME, what to scan, must be a tar file, uncompressed
* OUTPUT_PATH_LOG, output (report), default /tmp/avlog
* OUTPUT_PATH_RESULT, output message (str), default /tmp/result

The remaining variables shown below are used to access the objectstore with [py-objectstore](https://github.com/arkivverket/py-objectstore).

The values given here are examples or hints to proper variables.

```yaml
- TUSD_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- OUTPUT_PATH_LOG=/tmp/avlog
- OUTPUT_PATH_RESULT=/tmp/result
- BUCKET=bucket-storage
- AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=**********;AccountKey=**********;EndpointSuffix=core.windows.net
```

The environment variables `BUFFER_SIZE` and `MAX_CONCURRENCY` can be adjusted to tweak the performance.
Their default values are set to give, on average, the best performane, and are therefore it is not commonly needed to adjust them.

## Testing

### Running locally (docker)

If you are running Docker for Mac locally, you have to assign the Docker VM more memory and/or SWAP space.

Recommended is 4 GB SWAP and 4 GB up with memory, `clamd` is memory heavy whilst starting up, as it's loading its databases to memory.

### Running locally (without clamd installed)

Add this snippet to [`scanner.py`](app/scanner.py), which mocks the `ClamdUnixSocket` class and the `wait_for_port`. This allows to test the blob downlaod stream.

```python
class ClamdUnixSocket:
    def __init__(*args, **kwargs) -> None:
        """Mocks pylclamd.ClamdUnixSocket"""
        pass

    def scan_stream(*args, **kwargs) -> None:
        return None

    def version(*args, **kwargs) -> str:
        return "1.0.0"


def wait_for_port(*args):
    pass
```

And start the scanner with this command

```console
python -m app.scanner
```

## Testing with Azurite

`s3-scan-tar` supports testing against [Azurite](https://github.com/Azure/Azurite)

### Running Azurite

```console
docker run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite azurite-blob --blobHost 0.0.0.0 --loose
```

Set your `AZURE_STORAGE_CONNECTION_STRING` in `.env` to this string. Replace `127.0.0.1` if you run it on another host.

```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;
```

Upload a file to Azurite. If you are running Azurite on a different host, set the `AZURITE_STORAGE_CONNECTION_STRING` enviornment variable.

```console
poetry run tests/azurite/azurite_upload.py /path/to/tar/file.tar
```
