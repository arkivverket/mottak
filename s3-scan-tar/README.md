## Scan-tar

This container performs an antivirus-scan on an object read from objectstorage.

The container does a streaming read of a tar-file (object in objectstorage)
and feeds each element of it to [ClamAV](https://www.clamav.net/) over a socket.

### Environment variables
* TUSD_OBJECT_NAME, what to scan, must be a tar file, uncompressed
* AVLOG, output (report), default /tmp/avlog

The remaining variables shown below are used to access the objectstore with [py-objectstore](https://github.com/arkivverket/py-objectstore).


The values given here are examples or hints to proper variables.
```yaml
- TUSD_OBJECT_NAME=ok63e2f0-39bf-4fea-a741-58d472664ce2
- AVLOG=/tmp/avlog
- OBJECTSTORE=abs
- BUCKET=bucket-storage
- AZURE_ACCOUNT=myazureaccdev
- AZURE_KEY=secret
```

