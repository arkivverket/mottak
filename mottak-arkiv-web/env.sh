#!/bin/bash

ENV_FILE=".env"
ENV_VARIABLES=("API_BASEURL")

# Recreate config file
rm -rf ./env-config.js
touch ./env-config.js

# Add assignment
echo "window._env_ = {" >> ./env-config.js

if [ -f "$ENV_FILE" ]; then
  # Read each line in .env file
  # Each line represents key=value pairs
  while read -r line || [[ -n "$line" ]];
  do
    # Split env variables by character `=`
    if printf '%s\n' "$line" | grep -q -e '='; then
      varname=$(printf '%s\n' "$line" | sed -e 's/=.*//')
      varvalue=$(printf '%s\n' "$line" | sed -e 's/^[^=]*=//')
    fi

    # Append configuration property to JS file
    echo "	$varname: '$varvalue'," >> ./env-config.js
  done < "$ENV_FILE"
else
  # .env doesn't exist, needs to use env variables from list
  # Read each env variable name from list and get value from env variable
  for env_var in "${ENV_VARIABLES[@]}";
  do
    # Read value of current variable if exists as Environment variable
    value=$(printf '%s\n' "${!env_var}")

    # Append configuration property to JS file
    echo "	$env_var: '$value'," >> ./env-config.js
  done
fi

echo "}" >> ./env-config.js
