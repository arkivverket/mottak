#!/bin/bash

set -e
# set -x
echo "Archive bucket:       $ARCHIVE_BUCKET"
echo "Archive obj_id:"      $ARKIVUTTREKK_OBJ_ID
echo "Archive type:         $ARKIV_TYPE"
echo "Azure Storage Account $AZURE_STORAGE_ACCOUNT"

STORE="/objectstore"
TARGET="$STORE/$ARKIVUTTREKK_OBJ_ID/content"  # TODO Update TARGET after structure of objectpath has been decided
CONTAINER="$ARCHIVE_BUCKET"


mkdir -p /opt/output
mkdir -p $STORE

/usr/local/bin/goofys "wasb://${CONTAINER}@${AZURE_STORAGE_ACCOUNT}.blob.core.windows.net" "$STORE"

dotnet /opt/arkade5/Arkivverket.Arkade.CLI.dll \
    test \
    -a "$TARGET" \
    -p /tmp -o /opt/output  \
    -t "$ARKIV_TYPE"

# The report is available at /opt/output/Arkaderapport-.html
# Move it to a known location so Argo can get at it.
mv -v /opt/output/Arkaderapport-*.html /tmp/arkade.html

echo "Arkade report is at /tmp/arkade.html"
fusermount -u "$STORE"
