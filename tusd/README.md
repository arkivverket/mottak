# tusd

tusd handles incomming data from the upload client. You need to have one more more instances running and typically you'll have this open to the internet.

The uploader is invoked with an URL. This is a JSON object that is base64 encoded. It contains an URL pointing at tusd as well as some other data about the upload.

Whenever an upload is started or finishes tusd runs some hooks. See the hooks folder for details.

# Prerequisite
The dependency `psycopg2` requires that you have installed postgresql on mac:
`brew install postgresql`

# What is needed to get this running

 * DBSTRING, PHP-like formatting, needed for running the hooks
 * BUCKET
 * Object-store specifics. See start.sh for details as well as the deployment YAML.
 * Azure service bus settings.
   * AZ_SB_CON_KICKER - connection string
   * AZ_SB_QUEUE - what queue


