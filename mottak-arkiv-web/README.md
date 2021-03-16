## Mottak-arkiv-web

Application responsible for user interaction against mottak-arkiv-service. The application presents information about digital archives to be uploaded and allows the user to upload XML files created by Arkade5.

### Application flow
- TBW

### Environment variables needed
The values given here are examples. Please adjust to your local API url.
- `API_BASEURL=http://localhost:8000`

### Prerequisites
- [`yarn`](https://classic.yarnpkg.com/en/docs/install)

### Running locally
- Run `yarn install`
- Create a `.env` file in [root folder](.) containing env variables
- Run `yarn start` (or optionally `API_BASEURL=http://api.somewhere.local/api/path yarn start`)
- Open the web ui [http://localhost:3000](http://localhost:3000) in a browser
   - Remember to start [`mottak-arkiv-service`](../mottak-arkiv-service/) with `PYTHON_ENV=local` to enable the correct CORS headers


### Building and running in a Docker container
- Build the docker image `docker build -t mottak-arkiv-web:prod .`
- Start the docker container at port 3080
    - By specifying the API base URL on the command line: `docker run --name mottak-arkiv-web -it -p 3080:80 -e API_BASEURL=http://api.elsewhere.local/api mottak-arkiv-web:prod`
    - By reading the API base URL from the environment variable API_BASEURL: `docker run --name mottak-arkiv-web -it -p 3080:80 -e API_BASEURL mottak-arkiv-web:prod`
    - By reading the API base URL from an env file: `docker run --name mottak-arkiv-web -it -p 3080:80 --env-file myenvfile mottak-arkiv-web:prod`
