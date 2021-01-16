#!/usr/bin/env bash

# copy the config.yml to the host if it doesn't exist yet
# or copy it to the source if does exist
if test -f /conf/config.yml; then
  cp /conf/config.yml /app/config.yml
else
  cp /app/config.yml /conf/config.yml
fi

cd /app && python app.py
