# TUSD

Documentation: [https://github.com/tus/tusd](https://github.com/tus/tusd)

Tusd handles incomming data from the upload client. You need to have one more more instances running and typically you'll have this open to the internet.

The uploader is invoked with an URL. This is a JSON object that is base64 encoded. It contains an URL pointing at tusd as well as some other data about the upload.

Whenever an upload is started or finishes tusd runs some hooks. See the hooks folder for details.

# Prerequisite
The dependency `psycopg2` requires that you have installed postgresql on mac:
`brew install postgresql`

# What is needed to get this running
 * DBSTRING, URI formatting: `postgresql://[user[:password]@][netloc][:port][,...][/dbname][?param1=value1&...]`
 * BUCKET
 * Object-store specifics. See start.sh for details as well as the deployment YAML.
 * Azure service bus settings.
   * AZ_SB_CON_KICKER - connection string
   * AZ_SB_QUEUE - what queue


# Testing with Azure
## Building and running docker image
To test this, you need these env variables in your `.env`
```env
DBSTRING=
BUCKET=
OBJECTSTORE=
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_KEY=
AZ_SB_CON_KICKER=
AZ_SB_QUEUE=
```

Build the docker image locally
```shell
docker build --tag da-mottak/tusd .
```

And then run it locally
```shell
docker run --rm -it --env-file=.env -p 1080:1080 da-mottak/tusd
```
The `--env-file=.env` is important to no expose secrets in your terminal history and adds less arguments to run.
Ensure that you are in the same directory as your `.env` file.

## Testing an upload

Modify line 6, 7 and 22 in [tests/tus-uploader/tus-uploader.py](tests/tus-uploader/tus-uploader.py) to point to your docker container, usually `tusd_url = 'http://localhost:1080/tusd/files/'` and then `file_name` to point to a local test archive.<br />
The `invitasjonEksternId` has to match an UUID in the `invitasjon` table, and can only be used once, unless you delete it from the `overføringspakke` table after transfer.


To start the upload
```shell
poetry run python tests/tus-uploader/tus-uploader.py
```
