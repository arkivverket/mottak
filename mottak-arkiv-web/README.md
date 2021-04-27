# Mottak-arkiv-web

Application responsible for user interaction against mottak-arkiv-service. The application presents information about digital archives to be uploaded and allows the user to upload XML files created by Arkade5.

## Application flow

- TBW

## Environment variables needed

The values given here are examples. Please adjust to your local API url.

### Required env variables

```env
API_BASEURL=http://localhost:8000
```

## Project prerequisites

- [`yarn`](https://classic.yarnpkg.com/en/docs/install)

## Running locally

### Prerequisites

Create `.env` file in [root folder](.) containing env variables, use [`.env.default`](.env.default) as a template.

```env
API_BASEURL=http://localhost:8000
```

#### [Install the project dependencies](https://classic.yarnpkg.com/en/docs/install/#mac-stable)

```console
yarn install
```

### Starting the application

Remember to start [`mottak-arkiv-service`](../mottak-arkiv-service/) with `PYTHON_ENV=local` to enable the correct CORS headers

```console
yarn start
```

Open the web ui [http://localhost:3000](http://localhost:3000) in a browser

### Building and running in a Docker container

#### Building docker image

```console
docker build -t mottak-arkiv-web:prod .
```

#### Starting the docker container

This loads your local .env file, remember to change your `API_BASEURL` variable to point to the correct API endpoint.

```console
docker run -it \
    --name mottak-arkiv-web \
    --env-file=.env \
    -p 3080:80 \
    mottak-arkiv-web:prod
```

Open the web ui [http://localhost:3080](http://localhost:3080) in a browser
