#!/bin/sh
# Used to remove all environment variables needed to run arkiv-downloader
# Usage: source unset-arkiv-downloader-envvars.sh
unset REQUEST_RECEIVER_DEV
unset REQUEST_RECEIVER_TEST
unset REQUEST_RECEIVER_PROD

unset STATUS_SENDER_DEV
unset STATUS_SENDER_TEST
unset STATUS_SENDER_PROD

unset ARCHIVE_TARGET_LOCATION_DEV
unset ARCHIVE_TARGET_LOCATION_TEST
unset ARCHIVE_TARGET_LOCATION_PROD
