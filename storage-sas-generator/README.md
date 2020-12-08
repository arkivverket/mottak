# Storage SAS generator

Generates SAS signatures used inside of Azure to give other services access to an archive.

Needs two environment variables to function.
 - AZURE_ACCOUNT_NAME
 - AZURE_ACCOUNT_KEY

To run locally on your development machine:
```shell script
uvicorn app.main:app --reload
```

To test using httpie:
```
http POST localhost:8000/generate_sas container=mottak duration_hours=3
```
Use the docker image in production.
