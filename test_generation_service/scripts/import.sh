#!/bin/bash

while read -r line; do export "$line"; done < .env

function import() {
  local COLECTION="$1"
  local FILE="$2"

  mongoimport \
    --host "$LEONARDO_MONGODB_HOST" \
    --port "$LEONARDO_MONGODB_PORT" \
    --db="$LEONARDO_MONGODB_DB" \
    --collection="$COLECTION" \
    --file "$FILE" --jsonArray

}

import questions scripts/data/questions.json
import tests scripts/data/tests.json
