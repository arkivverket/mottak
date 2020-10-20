# Azure deploy pipeline and cluster setup
This folder contains the files needed for setting up mottak on a new cluster,
including the helm scripts used for CD.

## Continious Deployment
Pushing a new image to [arkivverket.azurecr.io](arkivverket.azurecr.io) will
trigger the Azure DevOps pipeline [deploy-pipeline.yaml](pipelines/deploy-pipeline.yaml)
(see containers supported in the pipeline file), and push the updated deployment
yaml to the kubernetes cluster.

## Setting up from scratch
#### Setting up the cluster
Prerequisites:
- A cluster setup up by the platform team, named: `av-plattform-<env>-aks`
- A namespace in the cluster named: `av-mottak-<env>`
- Azure cli installed on your machine, and you are signed in with
a user with enough permissions.

Then follow these steps:
- Open [setup.py](setup.sh) and edit the ENV variable.
- Make sure you have values-<env>.yaml with correct values (see [values-dev.yaml](values/dev/values-dev.yaml))
- Run `zsh setup.sh`

#### Adding pipeline to Azure DevOps
Go to [https://dev.azure.com/arkivverket](https://dev.azure.com/arkivverket) and add the
pipeline from GIT (connect to Github and select [deploy-pipeline.yaml](pipelines/deploy-pipeline.yaml))
