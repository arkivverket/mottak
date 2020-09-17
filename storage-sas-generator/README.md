# Storage SAS generator

Generates SAS signatures used inside of Azure to give other services access to an archive.

Needs two environment variables to function.
 - AZURE_ACCOUNT
 - AZURE_KEY

To run locally on your development machine:
```shell script
uvicorn app.main:app --reload
```
Use the docker image in production.
