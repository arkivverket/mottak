#!/bin/bash

set -e
echo "Object:        $OBJECT"
echo "Archieve type: $ARCHIEVE_TYPE"
echo "UUID:          $UUID"

STORE="/objectstore"
TARGET="$STORE/$UUID/content"

mkdir -p input output tmp
mkdir -p $STORE

dotnet /opt/Arkade5CLI-1.5.1/Arkivverket.Arkade.CLI.dll \
    -a $TARGET \
    -p /opt/tmp -o /opt/output -s packing \
    -m /tmp/dias-mets.xml -t $ARCHIEVE_TYPE

# The report is available at /opt/output/Arkaderapport-$UUID.html
# Move it to a know location so Argo can get at it.
mv -v /opt/output/Arkaderapport-$UUID.html /tmp/arkade.html

echo "Arkade report is at /tmp/arkade.html"
fusermount -u "$STORE"
