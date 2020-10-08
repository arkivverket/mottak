#!/usr/bin/env bash

ENV='dev'

CLUSTER_NAME="av-plattform-$ENV-aks"
RESOURCE_GROUP="av-plattform-$ENV-rg"

OUTPUT_FOLDER="k8s/output/$ENV"

## Auth against cluster
az aks get-credentials --name "$CLUSTER_NAME" --resource-group "$RESOURCE_GROUP"

## Build yaml files
helm template --values "values-$ENV.yaml" --output-dir "$OUTPUT_FOLDER" k8s/
#helm template --values "values-$ENV.yaml" --set AV_NAMESPACE=testingIt --output-dir "$OUTPUT_FOLDER" k8s/ # Test for replacing values

## Deploy yaml files
#kubectl apply -f
