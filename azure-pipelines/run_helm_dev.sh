#!/bin/zsh

if [ -z "$1" ]
  then
    echo "Please use scripts as run_helm.sh <env> <outputfolder>"
fi
if [ -z "$2" ]
  then
    echo "Please use scripts as run_helm.sh <env> <output_location>"
fi
ENV=$1:l
OUTPUT_FOLDER="$2"


## Build yaml files
helm template --values "values-$ENV.yaml" --output-dir "$OUTPUT_FOLDER" k8s/
#helm template --values "values-$ENV.yaml" --set AV_NAMESPACE=testingIt --output-dir "$OUTPUT_FOLDER" k8s/ # Test for replacing values
