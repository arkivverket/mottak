# Arkiv-downloader
Application meant to run on-prem for downloading arkivuttrekk from Azure Blob Storage to
on-prem storage location. It collects download messages from azure service bus queue containing a SAS token/url.
It then uses azcopy and the sas token/url to download the arkivuttrekk to a local location.
Download location will be `STORAGE_LOCATION/<azure blob container name>` or `STORAGE_LOCATION/target_name`
Status reports are sent back to mottak-arkiv-service through another service bus queue.
NB: Note the trailing `/` on `STORAGE_LOCATION`

Env variables needed:
- ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING: `Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-receiver;SharedAccessKey=<some_secret_key>`
- ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING: `Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-sender;SharedAccessKey=<some_secret_key>`
- STORAGE_LOCATION : `path/to/where/arkivuttrekk/will/be/downloaded/to/`


## Running locally
- Download [azcopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) and put under [root/arkiv_downloader/azcopy](arkiv_downloader/azcopy)
- Run `poetry install`
- Create a `.env` file in [root folder](.) containing env variables
- Run `python arkiv_downloader/main.py`


## Incomming message example
Note that `blob_info` is optional, and that if it is omitted, the entire container will be downloaded.
````json
{
  "arkivkopi_id": 1,
  "storage_account": "damottakdevsa",
  "container": "<container name>",
  "sas_token": "<sas_token>",
  "blob_info" : {
    "source_name": "<name/of/blob/in/container>",
    "target_name": "target_name.tar"
  }
}
````


## Outgoing status messages example
````json
{
  "arkivkopi_id": 1,
  "status": "Startet"
}
````
