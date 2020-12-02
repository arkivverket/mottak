# Kicker trigger
A small python script for adding messages to the service bus Kicker is listening on.

Env variables are read from [.env](../../.env) file in root folder.

Env variables needed:
- `QUEUE_CLIENT_CONNECTION_STRING` = `Endpoint=sb://<namespace>-servicebus.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<secret>`
- `QUEUE_NAME` = `<queue name>`

Find the post-finish hook in [mottak/tusd](../../../tusd) for object
structure expected.

Update the `get_params()` with the values you want sent on the queue.
