# Arkiv-downloader
Application meant to run on-prem for downloading arkivuttrekk from Azure Blob Storage to
on-prem storage location. It collects download messages from azure service bus queue containing a SAS token/url.
It then uses azcopy and the sas token/url to download the arkivuttrekk to a local location.
Download location will be `STORAGE_LOCATION/<azure blob container name>`.
Status reports are back to mottak-arkiv-service through another service bus queue.

Env variables needed:
- ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING: `Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-receiver;SharedAccessKey=<some_secret_key>`
- ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING: `Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-sender;SharedAccessKey=<some_secret_key>`
- STORAGE_LOCATION : `path/to/where/arkivuttrekk/will/be/downloaded/to`


## Running locally
- Download [azcopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) and put under [root/arkiv_downloader/azcopy](arkiv_downloader/azcopy)
- Run `poetry install`
- Create a `.env` file in [root folder](.) containing env variables
- Run `python arkiv_downloader/main.py`

## Incomming message example
````json
{
  "id": 1,
  "arkivuttrekk_id": "c05a214c-fcc5-11ea-8558-acde48001122",
  "storage_account": "damottakdevsa",
  "container":
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
