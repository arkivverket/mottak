#!/usr/bin/env zsh

# Small bash script that makes a copy of and replaces the <LANGUAGE>_COMPONENT_NAME_TEMPLATE string in the <language>-workflow-template.yaml file.
# This is used for supporting similar Github Action workflows for multiple components in the mottak repo.

# Expects the component/service to be in its own folder in root of repo, mottak/<component-name>
# I.E: mottak/mottak-arkiv-service
PYTHON_COMPONENT_NAMES=("mottak-arkiv-service" "arkiv-downloader" "tusd" "kicker" "storage-sas-generator" "s3-delete" "s3-scan-tar" "s3-unpack" "s3-checksum256" "mailer")
REACT_COMPONENT_NAMES=("mottak-arkiv-web")
BASH_COMPONENT_NAMES=("arkade5")

declare -A COMPONENT_CONTAINER_MAPPING # Declaring dictionary
# Mapping components to value container tag
COMPONENT_CONTAINER_MAPPING=(["mottak-arkiv-service"]="DA_MOTTAK_ARKIV_SERVICE_TAG" ["arkiv-downloader"]="DA_ARKIV_DOWNLOADER_TAG" ["tusd"]="DA_MOTTAK_TUSD_TAG"
  ["kicker"]="DA_MOTTAK_KICKER_TAG" ["storage-sas-generator"]="DA_MOTTAK_STORAGE_SAS_GENERATOR_TAG" ["s3-delete"]="DA_MOTTAK_S3_DELETE_TAG"
  ["s3-scan-tar"]="DA_MOTTAK_S3_SCAN_TAR_TAG" ["s3-unpack"]="DA_MOTTAK_S3_UNPACK_TAG" ["s3-unpack"]="DA_MOTTAK_S3_UNPACK_TAG" ["s3-checksum256"]="DA_MOTTAK_S3_CHECKSUM256_TAG"
  ["mailer"]="DA_MOTTAK_MAILER_TAG" ["mottak-arkiv-web"]="DA_MOTTAK_ARKIV_WEB_TAG" ["arkade5"]="DA_MOTTAK_ARKADE5_TAG")


# Templates
COMPONENT_NAME_TEMPLATE='!COMPONENT_NAME!'
TOP_COMMENT_TEMPLATE='!TOP_COMMENT!'
TOP_COMMENT='THIS FILE IS AUTOGENERATED. EDIT TEMPLATES IN PARENT FOLDER'
PYTHON_TEMPLATE_FILE_NAME="templates/python-workflow-template.yaml"
REACT_TEMPLATE_FILE_NAME="templates/react-workflow-template.yaml"
BASH_TEMPLATE_FILE_NAME="templates/bash-workflow-template.yaml"
COMPONENT_CONTAINER_NAME_TAG_TEMPLATE='!COMPONENT_CONTAINER_NAME_TAG_NAME!'

for COMPONENT in "${PYTHON_COMPONENT_NAMES[@]}"
do
  OUTPUT_FILE='workflows/'"$COMPONENT"'-workflow.yaml'
  REPLACE_COMPONENT_NAME_CMD='s,'"$COMPONENT_NAME_TEMPLATE"','"$COMPONENT"',g'
  REPLACE_COMMENT_CMD='s,'"$TOP_COMMENT_TEMPLATE"','"$TOP_COMMENT"',g'
  REPLACE_CONTAINER_NAME_TAG_CMD='s,'"$COMPONENT_CONTAINER_NAME_TAG_TEMPLATE"','"${COMPONENT_CONTAINER_MAPPING[$COMPONENT]}"',g'

  echo "Adapting $PYTHON_TEMPLATE_FILE_NAME into $OUTPUT_FILE"
  sed -e "$REPLACE_COMPONENT_NAME_CMD" -e "$REPLACE_COMMENT_CMD" -e "$REPLACE_CONTAINER_NAME_TAG_CMD" "$PYTHON_TEMPLATE_FILE_NAME" > "$OUTPUT_FILE"
done

for COMPONENT in "${REACT_COMPONENT_NAMES[@]}"
do
  OUTPUT_FILE='workflows/'"$COMPONENT"'-workflow.yaml'
  REPLACE_COMPONENT_NAME_CMD='s,'"$COMPONENT_NAME_TEMPLATE"','"$COMPONENT"',g'
  REPLACE_COMMENT_CMD='s,'"$TOP_COMMENT_TEMPLATE"','"$TOP_COMMENT"',g'
  REPLACE_CONTAINER_NAME_TAG_CMD='s,'"$COMPONENT_CONTAINER_NAME_TAG_TEMPLATE"','"${COMPONENT_CONTAINER_MAPPING[$COMPONENT]}"',g'

  echo "Adapting $REACT_TEMPLATE_FILE_NAME into $OUTPUT_FILE"
  sed -e "$REPLACE_COMPONENT_NAME_CMD" -e "$REPLACE_COMMENT_CMD" -e "$REPLACE_CONTAINER_NAME_TAG_CMD" "$REACT_TEMPLATE_FILE_NAME" > "$OUTPUT_FILE"
done

for COMPONENT in "${BASH_COMPONENT_NAMES[@]}"
do
  OUTPUT_FILE='workflows/'"$COMPONENT"'-workflow.yaml'
  REPLACE_COMPONENT_NAME_CMD='s,'"$COMPONENT_NAME_TEMPLATE"','"$COMPONENT"',g'
  REPLACE_COMMENT_CMD='s,'"$TOP_COMMENT_TEMPLATE"','"$TOP_COMMENT"',g'
    REPLACE_CONTAINER_NAME_TAG_CMD='s,'"$COMPONENT_CONTAINER_NAME_TAG_TEMPLATE"','"${COMPONENT_CONTAINER_MAPPING[$COMPONENT]}"',g'

  echo "Adapting $BASH_TEMPLATE_FILE_NAME into $OUTPUT_FILE"
  sed -e "$REPLACE_COMPONENT_NAME_CMD" -e "$REPLACE_COMMENT_CMD" -e "$REPLACE_CONTAINER_NAME_TAG_CMD" "$BASH_TEMPLATE_FILE_NAME" > "$OUTPUT_FILE"
done
