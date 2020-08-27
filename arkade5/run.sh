#!/bin/bash

set -e
# set -x
echo "Object:        $OBJECT"
echo "Archieve type: $ARCHIEVE_TYPE"
echo "UUID:          $UUID"
echo "Account        $AZURE_ACCOUNT"

STORE="/objectstore"
TARGET="$STORE/$UUID/content"
CONTAINER="$UUID-0"

mkdir -p input output tmp
mkdir -p $STORE

/usr/local/bin/goofys "wasb://${CONTAINER}@${AZURE_ACCOUNT}.blob.core.windows.net" "$STORE"

dotnet /opt/arkade5/Arkivverket.Arkade.CLI.dll \
    test \
    -a "$TARGET" \
    -p /opt/tmp -o /opt/output  \
     -t "$ARCHIEVE_TYPE"

# The report is available at /opt/output/Arkaderapport-$UUID.html
# Move it to a know location so Argo can get at it.
mv -v /opt/output/Arkaderapport-*.html /tmp/arkade.html

echo "Arkade report is at /tmp/arkade.html"
fusermount -u "$STORE"
