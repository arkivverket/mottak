# Mottak-arkiv-service

Application responsible for serving the application mottak-arkiv-web with viewing data and orchestrating the process of storing digital archives

### Application flow
- The user(coordinator) sends in an XML file created by Arkade5 containing metadata about the archive to be uploaded.
- The application will parse the XML file and return a partially filled out form.
- The user will be able to change and add information to the form before committing the data to the application.
- Once the data has been persisted, an email will be sent out to the archive uploader, inviting them to upload the archive.
- The archive is uploaded to an agreed upon object storage.

### Environment variables needed
The values given here are examples. Please adjust to your local database.
- DBSTRING: `postgresql://<username>:<password>@localhost:5432/postgres`
- MAILGUN_DOMAIN: `<some_id>.mailgun.org`
- MAILGUN_SECRET: `<secret used for auth againt mailgun>`
- TUSD_URL: `<public url to tusd>`
- TUSD_DOWNLOAD_LOCATION_CONTAINER: `<container_id for objects uploaded throught tusd>`
- ARCHIVE_DOWNLOAD_REQUEST_SENDER_SB_CON_STRING: `Endpoint=sb://av-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-request-sender;SharedAccessKey=<some_secret_key>`
- ARCHIVE_DOWNLOAD_STATUS_RECEIVER_SB_CON_STRING: `Endpoint=sb://av-mottak-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=archive-download-status-receiver;SharedAccessKey=<some_secret_key>`
- SAS_GENERATOR_HOST: `<base url for sas generator>`
- RUN_SCHEDULER: `<optional boolean, default: True>`

### Prerequisites
- [`poetry`](https://python-poetry.org/docs/)

### Running locally
- Run `poetry install` to [install the project dependencies](https://python-poetry.org/docs/cli/#install)
- Run `poetry shell` to [load the virtual enviroment created by poetry](https://python-poetry.org/docs/cli/#shell)
- Setup local database
  - Install postgres: `brew install postgres` (macOS)
  - Set up database:
    - Run `psql postgres` to connect to postgres. This will open a new editor inside your terminal.
      - Run `CREATE DATABASE mottak;` to create the database and `exit` to quit psql
- Create a `.env` file in [root folder](.) containing env variables
  - Use `.env.default` as a template
  - If using local database based on setup above: `DBSTRING=postgresql://localhost:5432/mottak`

- Initiate the database by running `alembic upgrade head`
- Run `uvicorn app.main:app --reload`

### Swagger
local = http://localhost:8000/docs
