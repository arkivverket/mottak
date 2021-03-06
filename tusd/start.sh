#!/bin/bash
# We only enable the hooks we have. This will reduce logging somewhat.
# Consider hooking into post-terminate for logging.
OPT_PARAMS="-hooks-enabled-events pre-create,post-create,post-finish -base-path ${BASE_PATH:-/tusd/files/}"

echo "Enviroment overview:"
echo "Bucket: ${BUCKET}"
echo "Endpoint: ${ENDPOINT}"
echo "Objectstore: ${OBJECTSTORE}"
echo "AWS Key: ${AWS_ACCESS_KEY_ID}"
if [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "AWS_SECRET_ACCESS_KEY is set (secret)"
fi
echo "AWS Region: ${AWS_REGION}"
echo "GCS AUTH_TOKEN: ${AUTH_TOKEN}"

echo "AZURE_STORAGE_ACCOUNT: ${AZURE_STORAGE_ACCOUNT}"
if [ -n "$AZURE_STORAGE_KEY" ]; then
    echo "AZURE_STORAGE_KEY is set (secret)"
fi

echo "Mailgun domain: ${MAILGUN_DOMAIN}"
if [ -n "$MAILGUN_API_KEY" ]; then
    echo "MAILGUN_API_KEY is set (secret)"
fi
echo "Hooks present:"
find /srv/hooks

# pick GCS:
if [ "$OBJECTSTORE" == "gcs" ]; then
    echo "Backend is GCS (bucket: $BUCKET). Setting GCS_SERVICE_ACCOUNT_FILE to $AUTH_TOKEN"
    export GCS_SERVICE_ACCOUNT_FILE=$AUTH_TOKEN
    TUSD_PARAMS="-hooks-dir /srv/hooks -behind-proxy -gcs-bucket ${BUCKET}"
# handle Azure here if we're supporting it:
elif [ "$OBJECTSTORE" == "azure" ]; then
    echo "Backend is Azure Blob Storage."
    #  Use Azure BlockBlob Storage with this container name as a storage backend
    # (requires the AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_KEY environment variable to be set)

    TUSD_PARAMS="-hooks-dir /srv/hooks -behind-proxy -azure-storage ${BUCKET}"
else
    echo "Assuming we're using the S3 backend"
    TUSD_PARAMS="-hooks-dir /srv/hooks -behind-proxy -s3-bucket ${BUCKET} -s3-endpoint ${ENDPOINT}"
fi

echo "============"
echo "Running tusd with these flags: ${TUSD_PARAMS} ${OPT_PARAMS}"
echo "============"
tusd ${TUSD_PARAMS} ${OPT_PARAMS}
