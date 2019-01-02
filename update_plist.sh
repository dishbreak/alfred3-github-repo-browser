#!/bin/bash

ALFRED_WORKFLOW_DIR="$HOME/Library/Application Support/Alfred 3/Alfred.alfredpreferences/workflows/"
OUR_WORKFLOW_KEYWORD="Alfred Github Repo Browser"

WORKFLOW_DIR=$(dirname "$(grep -ir "$OUR_WORKFLOW_KEYWORD" "$ALFRED_WORKFLOW_DIR" | cut -d ":" -f 1)")

cat "$WORKFLOW_DIR"/info.plist > ./info.plist
