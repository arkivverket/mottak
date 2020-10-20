## Mottak-arkiv-web

Application responsible for user interaction against mottak-arkiv-service. The application presents information about digital archives to be uploaded and allows the user to upload XML files created by Arkade5.

### Application flow
- TBW

### Environment variables needed
The values given here are examples. Please adjust to your local API url.
- API_BASEURL : `http://localhost:8000`

### Running locally
- Run `yarn install`
- Create a `.env` file in [root folder](.) containing env variables
- Run `yarn start` (or optionally `API_BASEURL=http://api.somewhere.local/api/path yarn start`)
- Open the web ui [http://localhost:3000](http://localhost:3000) in a browser

### Building and running in a Docker container
- Build the docker image `docker build -t mottak-arkiv-web:prod .`
- Start the docker container at port 3080 `docker run --name mottak-arkiv-web -it -p 3080:80 -e API_BASEURL=http://api.elsewhere.local/api mottak-arkiv-web:prod`

