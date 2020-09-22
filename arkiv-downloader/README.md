# Arkiv-downloader

This application listens on a azure service bus queue for SAS requests to download Arkivuttrekk to a local server.
Status reports are then loaded back onto another service bus queue.

Env variables needed:
- QUEUE_CLIENT_STRING


## Running locally
Run
- Run `poetry install`
- Create a `.env` file in [root folder](.) containing env variables
- Run `python arkiv_downloader/main.py`

## Incomming message example
````json
{
  "obj_id": "c05a214c-fcc5-11ea-8558-acde48001122",
  "blob_sas_url": "https://<storage_account>.blob.core.windows.net/<container>?<sas_token>"
}
````

## Outgoing status messages example
````json
{
  "obj_id": "c05a214c-fcc5-11ea-8558-acde48001122",
  "status": "TRANSFERING",
  "statusCreatedTime": "2020-09-22 13:32:20.612712"
````
