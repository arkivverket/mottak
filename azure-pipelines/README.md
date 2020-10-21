# Azure deploy pipeline and cluster setup
This folder contains the files needed for setting up mottak on a new cluster,
including the helm scripts used for CD.

## Continious Deployment
Pushing a new image/tag to one of the watched repositories at [arkivverket.azurecr.io](arkivverket.azurecr.io) will
trigger the matching Azure DevOps pipeline in [pipelines](pipelines). Ie a new image to
[av-mottak/kicker](arkivverket.azurecr.io/av-mottak/kicker) will trigger
[kicker-deploy.yaml](pipelines/kicker-deploy.yaml).

## Adding pipeline to Azure DevOps
- Create a new deployment file <name>-deploy.yaml in [pipelines](pipelines), see [pipelines/kicker-deploy.yaml](pipelines/kicker-deploy.yaml).
- If you copy paste an existing pipeline, you should only have to change `registry` under `resources.containers` and the `variables`
- Once it has been commited and merged to develop, go to [https://dev.azure.com/arkivverket](https://dev.azure.com/arkivverket) and add the
pipeline from GIT.

## Setting up from scratch
#### Setting up the cluster
Prerequisites:
- A cluster setup up by the platform team, named: `av-plattform-<env>-aks`
- A namespace in the cluster named: `av-mottak-<env>`
- Azure cli installed on your machine, and you are signed in with
a user with enough permissions.

Then follow these steps:
- Open [setup.py](setup.sh) and edit the ENV variable.
- Make sure you have values.yaml and values-containers.yaml in `values/<env>/` with correct values (see dev for example [values/dev/values.yaml](values/dev/values.yaml))
- Run `zsh setup.sh`

#### Add piplines
See [Adding pipeline to azure DevOps](#adding-pipeline-to-azure-devops)
