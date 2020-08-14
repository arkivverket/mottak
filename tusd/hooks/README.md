# tusd hooks.

These hooks are run whenever something is uploaded to tusd.

When tusd runs a hook to opens the hook and feeds it a JSON document on STDIN. The document varies depending on what kind of event it is. We use pre- and post-hooks. The pre-hook just makes sure that the client has a valid invitation. The event looks like this:

{
  "Upload": {
    "ID": "",
    "Size": 440320,
    "SizeIsDeferred": false,
    "Offset": 0,
    "MetaData": {
      "fileName": "df53d1d8-39bf-4fea-a741-58d472664ce2.tar",
      "invitation_id": "7"
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

The post-upload hook will start argo and feed it the relevant stuff. The event itself looks like this:

{
  "Upload": {
    "ID": "9090fe36854e6761925e6e9ec475c17f",
    "Size": 440320,
    "SizeIsDeferred": false,
    "Offset": 440320,
    "MetaData": {
      "fileName": "df53d1d8-39bf-4fea-a741-58d472664ce2.tar",
      "invitation_id": "7"
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
