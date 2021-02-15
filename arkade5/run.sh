#!/bin/bash

set -e
# set -x
echo "Target Bucket Name:   $TARGET_BUCKET_NAME"
echo "Archive type:         $ARKIV_TYPE"
echo "Account               $AZURE_ACCOUNT"

STORE="/objectstore"
TARGET="$STORE/content"  # TODO Update TARGET after structure of objectpath has been decided
CONTAINER="$TARGET_BUCKET_NAME"


mkdir -p /opt/output
mkdir -p $STORE

/usr/local/bin/goofys "wasb://${CONTAINER}@${AZURE_ACCOUNT}.blob.core.windows.net" "$STORE"

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
