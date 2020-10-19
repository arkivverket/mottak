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
helm template --values "values/$ENV/values.yaml" --output-dir "$OUTPUT_FOLDER" k8s/
