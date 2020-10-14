#!/usr/bin/env bash
# Sets up things i mottak namespace

ENV="dev"
OUTPUT_FOLDER="k8s/output"

zsh run_helm_dev.sh $ENV $OUTPUT_FOLDER

TEMPLATE_FOLDER="$OUTPUT_FOLDER/$ENV/av-mottak/templates/"


kubectl apply -f "$TEMPLATE_FOLDER/csi-driver-link.yaml"
kubectl apply -f "$TEMPLATE_FOLDER/mount_the_secrets.yaml"
kubectl apply -f "$TEMPLATE_FOLDER/minio-deployment.yaml"
