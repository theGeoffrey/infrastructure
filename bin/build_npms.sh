#!/bin/bash
set -e
BASE_PATH=`pwd`
NODE_BIN="$BASE_PATH/node_modules/.bin"
PATH="$NODE_BIN:$PATH"

cd "$BASE_PATH/geoffrey/ui" && npm install && grunt build