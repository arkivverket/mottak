#!/bin/bash

SECRETS_FILE=/vault/secrets/config

if test -f "$SECRETS_FILE"; then
  echo "Will source $SECRETS_FILE"
  . $SECRETS_FILE
else
  echo "Secrets file not found at $SECRETS_FILE"
fi

exec "$@"
