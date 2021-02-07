# tusd hooks

These hooks are run whenever something is uploaded to tusd.

Documentation: https://github.com/tus/tusd/blob/master/docs/hooks.md

For testability we have separated the tusd hook files from the logic. tusd does not allow `.py` extension, and thus the
logic is found under [implementations](implementations).

When tusd runs a hook to opens the hook and feeds it a JSON document on STDIN. The document varies depending on what
kind of event it is. We use pre- and post-hooks. The pre-hook just makes sure that the client has a valid invitation.
The event looks like this:
```Json
{
  "Upload": {
    "ID": "",
    "Size": 440320,
    "SizeIsDeferred": false,
    "Offset": 0,
    "MetaData": {
      "fileName": "df53d1d8-39bf-4fea-a741-58d472664ce2.tar",
      "invitasjonEksternId": "80895248-3d0d-477c-948e-7b0de59d7f6b"
    },
    "IsPartial": false,
    "IsFinal": false,
    "PartialUploads": null,
    "Storage": null
  },
  "HTTPRequest": {
    "Method": "POST",
    "URI": "/files",
    "RemoteAddr": "10.52.0.1:58955",
    "Header": {
      "Connection": ["Keep-Alive"],
      "Content-Length": ["0"],
      "Tus-Resumable": ["1.0.0"],
      "Upload-Length": ["440320"],
      "Upload-Metadata": [
        "invitation_id Nw==,fileName ZGY1M2QxZDgtMzliZi00ZmVhLWE3NDEtNThkNDcyNjY0Y2UyLnRhcg=="
      ],
      "Via": ["1.1 google"],
      "X-Cloud-Trace-Context": [
        "b167c3b206b0f8d40b1bfc018db3912f/16434868822010988609"
      ],
      "X-Forwarded-For": ["128.39.57.12, 34.107.169.47"],
      "X-Forwarded-Proto": ["https"]
    }
  }
}
```
The post-upload hook will start argo and feed it the relevant stuff. The event itself looks like this:

```json
{
  "Upload": {
    "ID": "9090fe36854e6761925e6e9ec475c17f",
    "Size": 440320,
    "SizeIsDeferred": false,
    "Offset": 440320,
    "MetaData": {
      "fileName": "df53d1d8-39bf-4fea-a741-58d472664ce2.tar",
      "invitasjonEksternId": "80895248-3d0d-477c-948e-7b0de59d7f6b"
    },
    "IsPartial": false,
    "IsFinal": false,
    "PartialUploads": null,
    "Storage": {
      "Bucket": "mottak2",
      "Key": "9090fe36854e6761925e6e9ec475c17f",
      "Type": "gcsstore"
    }
  },
  "HTTPRequest": {
    "Method": "PATCH",
    "URI": "/files/9090fe36854e6761925e6e9ec475c17f",
    "RemoteAddr": "10.52.0.1:50725",
    "Header": {
      "Connection": ["Keep-Alive"],
      "Content-Length": ["440320"],
      "Content-Type": ["application/offset+octet-stream"],
      "Tus-Resumable": ["1.0.0"],
      "Upload-Offset": ["0"],
      "Via": ["1.1 google"],
      "X-Cloud-Trace-Context": [
        "6e79e59c2a4408d889c3422178dd074f/7868454035101903276"
      ],
      "X-Forwarded-For": ["128.39.57.12, 34.107.169.47"],
      "X-Forwarded-Proto": ["https"]
    }
  }
}
```

General information about the hook event JSON document
````json
{
  // The upload object contains the upload's details
  "Upload": {
    // The upload's ID. Will be empty during the pre-create event
    "ID": "14b1c4c77771671a8479bc0444bbc5ce",
    // The upload's total size in bytes.
    "Size": 46205,
    // The upload's current offset in bytes.
    "Offset": 1592,
    // These properties will be set to true, if the upload as a final or partial
    // one. See the Concatenation extension for details:
    // http://tus.io/protocols/resumable-upload.html#concatenation
    "IsFinal": false,
    "IsPartial": false,
    // If the upload is a final one, this value will be an array of upload IDs
    // which are concatenated to produce the upload.
    "PartialUploads": null,
    // The upload's meta data which can be supplied by the clients as it wishes.
    // All keys and values in this object will be strings.
    // Be aware that it may contain maliciously crafted values and you must not
    // trust it without escaping it first!
    "MetaData": {
      "filename": "transloadit.png"
    },
    // Details about where the data store saved the uploaded file. The different
    // availabl keys vary depending on the used data store.
    "Storage": {
      // For example, the filestore supplies the absolute file path:
      "Type": "filestore",
      "Path": "/my/upload/directory/14b1c4c77771671a8479bc0444bbc5ce",
      // The S3Store and GCSStore supply the bucket name and object key:
      "Type": "s3store",
      "Bucket": "my-upload-bucket",
      "Key": "my-prefix/14b1c4c77771671a8479bc0444bbc5ce"
    }
  },
  // Details about the HTTP request which caused this hook to be fired.
  // It can be used to record the client's IP address or inspect the headers.
  "HTTPRequest": {
    "Method": "PATCH",
    "URI": "/files/14b1c4c77771671a8479bc0444bbc5ce",
    "RemoteAddr": "1.2.3.4:47689",
    "Header": {
      "Host": ["myuploads.net"],
      "Cookies": ["..."]
    }
  }
}
````
