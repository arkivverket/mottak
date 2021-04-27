# Mottak-arkiv-service

Application responsible for serving the application mottak-arkiv-web with viewing data and orchestrating the process of storing digital archives

## Application flow

- The user(coordinator) sends in an XML file created by Arkade5 containing metadata about the archive to be uploaded.
- The application will parse the XML file and return a partially filled out form.
- The user will be able to change and add information to the form before committing the data to the application.
- Once the data has been persisted, an email will be sent out to the archive uploader, inviting them to upload the archive.
- The archive is uploaded to an agreed upon object storage.

## Environment variables

The values given here are examples. Please adjust to your local database.

### Required env variables

```env
DBSTRING="postgresql://<username>:<password>@localhost:5432/postgres"
MAILGUN_DOMAIN="<some_id>.mailgun.org"
MAILGUN_SECRET="<secret used for auth againt mailgun>"
TUSD_URL="<public url to tusd>"
TUSD_DOWNLOAD_LOCATION_CONTAINER="<container_id for objects uploaded throught tusd>"
ARCHIVE_DOWNLOAD_REQUEST_SENDER_SB_CON_STRING="Endpoint=sb://av-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-sender;SharedAccessKey=<some_secret_key>"
ARCHIVE_DOWNLOAD_STATUS_RECEIVER_SB_CON_STRING="Endpoint=sb://av-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-receiver;SharedAccessKey=<some_secret_key>"
SAS_GENERATOR_HOST="<base url for sas generator>"
```

### Optional env variables

```env
RUN_SCHEDULER=<optional boolean, default: True>
```

If you are working with [`mottak-arkiv-web`](../mottak-arkiv-web/), this variable has to be set to enable CORS

```env
PYTHON_ENV=local
```

## Project prerequisites

- [`python >= 3.8`]([https://](https://www.python.org/downloads/))
- [`poetry`](https://python-poetry.org/docs/)

## Running locally

Swagger can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs)

### Prerequisites

Create `.env` file in [root folder](.) containing env variables, use [`.env.default`](.env.default) as a template.

If using the local database from [setup local database](#setup-the-local-database)

```env
DBSTRING=postgresql://localhost:5432/mottak
```

#### [Install the project dependencies](https://python-poetry.org/docs/cli/#install)

```console
poetry install
```

#### Setup the local database

Install the postgres database (macOS)

```console
brew install postgres
```

Connect to postgres, this will open a new editor inside your terminal

```console
psql postgres
```

Create the database and exit psql

```sql
CREATE DATABASE mottak;
exit;
```

Initiate the database

```console
poetry run alembic upgrade head
```

### Starting the application

```console
poetry run uvicorn app.main:app --reload
```
