#!/bin/sh
# Used to add all environment variables needed to run arkiv-downloader
# This version have the secrets removed. These must be added when runnning the scripts
# Usage: source export-arkiv-downloader-envvars.sh
export REQUEST_RECEIVER_DEV="Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-receiver;SharedAccessKey=<secret>"
export REQUEST_RECEIVER_TEST="Endpoint=sb://da-mottak-test-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-receiver;SharedAccessKey=<secret>"
export REQUEST_RECEIVER_PROD="Endpoint=sb://da-mottak-prod-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-receiver;SharedAccessKey=<secret>"

export STATUS_SENDER_DEV="Endpoint=sb://da-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-sender;SharedAccessKey=<secret>"
export STATUS_SENDER_TEST="Endpoint=sb://da-mottak-test-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-sender;SharedAccessKey=<secret>"
export STATUS_SENDER_PROD="Endpoint=sb://da-mottak-prod-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-sender;SharedAccessKey=<secret>"

export ARCHIVE_TARGET_LOCATION_DEV="/arkivuttrekk/da-mottak-dev/"
export ARCHIVE_TARGET_LOCATION_TEST="/arkivuttrekk/da-mottak-test/"
export ARCHIVE_TARGET_LOCATION_PROD="/arkivuttrekk/da-mottak-prod/"
