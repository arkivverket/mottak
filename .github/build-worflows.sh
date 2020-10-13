#!/bin/bash

# Small bash script that makes a copy of and replaces the COMPONENT_NAME_TEMPLATE string in the python-workflow-template.yaml file.
# This is used for supporting similar Github Action workflows for multiple components in the mottak repo.

# Expects the component/service to be in its own folder in root of repo, mottak/<component-name>
# I.E: mottak/mottak-arkiv-service
COMPONENT_NAMES=("mottak-arkiv-service" "arkiv-downloader" "tusd")

# Templates
COMPONENT_NAME_TEMPLATE='!COMPONENT_NAME!'
TOP_COMMENT_TEMPLATE='!TOP_COMMENT!'
TOP_COMMENT='THIS FILE IS AUTOGENERATED. EDIT TEMPLATES IN PARENT FOLDER'
TEMPLATE_FILE_NAME="python-workflow-template.yaml"



for COMPONENT in "${COMPONENT_NAMES[@]}"
do
  OUTPUT_FILE='workflows/'"$COMPONENT"'-workflow.yaml'
  REPLACE_COMPONENT_NAME_CMD='s,'"$COMPONENT_NAME_TEMPLATE"','"$COMPONENT"',g'
  REPLACE_COMMENT_CMD='s,'"$TOP_COMMENT_TEMPLATE"','"$TOP_COMMENT"',g'

  echo "Adapting $TEMPLATE_FILE_NAME into $OUTPUT_FILE"
  sed -e "$REPLACE_COMPONENT_NAME_CMD" -e "$REPLACE_COMMENT_CMD" "$TEMPLATE_FILE_NAME" > "$OUTPUT_FILE"
done