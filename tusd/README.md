# tusd

tusd handles incomming data from the upload client. You need to have one more more instances running and typically you'll have this open to the internet.

The uploader is invoked with an URL. This is a JSON object that is base64 encoded. It contains an URL pointing at tusd as well as some other data about the upload.

Whenever an upload is started or finishes tusd runs some hooks. See the hooks folder for details.

# What is needed to get this running on Azure w/minio gw or AWS

 * DBSTRING, PHP-like formatting, needed for running the hooks
 * AWS_ACCESS_KEY_ID
 * AWS_SECRET_ACCESS_KEY
 * AWS_REGION
 * ENDPOINT
 * BUCKET

See start.sh for details as well as the deployment YAML.



For GCS - set OBJECTSTORE to gcs and mount the GCS secret JSON file and point GCS_SERVICE_ACCOUNT_FILE to it.


