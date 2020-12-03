#!/bin/zsh
# Sets up initial set-up of mottak namespace

# Change this to match current env.
# Expects to find a values-<env>.yaml file in same folder as this script.
ENV="dev"


OUTPUT_FOLDER="k8s/output/$ENV"
CLUSTER_NAME="av-plattform-$ENV-aks"
PLATFORM_RESOURCE_GROUP="av-plattform-$ENV-rg"
MOTTAK_RESOURCE_GROUP="av-mottak-$ENV-rg"
NAMESPACE="av-mottak-$ENV"
STORAGE_ACCOUNT_NAME="avmottak${ENV}sacc"
MOTTAK_VAULT_NAME="av-mottak-$ENV-vault"

## Auth against cluster
echo
echo "Setting up aks credentials for cluster $CLUSTER_NAME in resource group $PLATFORM_RESOURCE_GROUP"
az aks get-credentials --name "$CLUSTER_NAME" --resource-group "$PLATFORM_RESOURCE_GROUP"

# Installing argo workflows in namespace
echo
echo "Installing argo in namespace: $NAMESPACE"
kubectl apply -n "$NAMESPACE" -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/namespace-install.yaml


# Build helm templates and apply to cluster
OUTPUT_TEMPLATE_FOLDER="$OUTPUT_FOLDER/av-mottak/templates/"

echo
echo "Building helm templates"
zsh run_helm_dev.sh $ENV $OUTPUT_FOLDER

echo
echo "Running kubectl apply -f on setup yamls"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/csi-driver-link.yaml"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/mount_the_secrets.yaml"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/minio-deployment.yaml"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/argo-rbac.yaml"

echo
echo "Setting up ingress"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/ingress.yaml"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/nginx.yaml"
kubectl apply -f "$OUTPUT_TEMPLATE_FOLDER/oauth2-proxy.yaml"

#echo
#echo "Setting up av-mottak-$ENV-rg"
#az storage container create --name "tusd-target" --account-name $STORAGE_ACCOUNT_NAME --resource-group $MOTTAK_RESOURCE_GROUP

#echo
#echo "Setting up av-mottak-$ENV-vault"
#az keyvault secret set --name "mailgun-secret" --vault-name "$MOTTAK_VAULT_NAME" --description "Secret for using mailgun API"
