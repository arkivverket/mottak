#!/bin/sh
if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage: zsh $0 <env> <image_tag>"
    exit 1
fi
case $1:l in
    dev|test|prod)  ENV=$1:l;;
    *)              echo "<env>=$1. Must be one of dev, test or prod"
                    exit 1;;
esac

ENV_U=$ENV:u  # Uppercase version of <env>, used when creating environment variables
TAG=$2
echo "Trying to run arkiv-downloader:$TAG in $ENV-environment"

container_name=arkiv-downloader-$ENV
running_container="$(docker ps -aq --filter=name="$container_name")"
if [ -n $running_container ]; then
    echo "Stop and remove running container '$container_name'"
    echo "Stopping... " && docker container stop $container_name
    echo "Removing... " && docker container rm $container_name
fi

env_target_location="ARCHIVE_TARGET_LOCATION_$ENV_U"
eval target_location=\$$env_target_location

env_request_receiver="REQUEST_RECEIVER_$ENV_U"
eval request_receiver=\$$env_request_receiver

env_status_sender="STATUS_SENDER_$ENV_U"
eval status_sender=\$$env_status_sender

echo "Starting container '$container_name' and store downloaded archives in folder '$target_location'"
docker run --name=$container_name -d \
    -v $target_location:$target_location \
    -e ARCHIVE_TARGET_LOCATION=$target_location \
    -e ARCHIVE_DOWNLOAD_REQUEST_RECEIVER_SB_CON_STRING=$request_receiver \
    -e ARCHIVE_DOWNLOAD_STATUS_SENDER_SB_CON_STRING=$status_sender \
    -it arkivverket.azurecr.io/da-mottak/arkiv-downloader:$TAG
