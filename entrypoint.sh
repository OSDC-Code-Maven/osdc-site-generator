#!/usr/bin/env bash
set -ex

root=$(dirname $0)
printenv | sort
#ls -l /usr/bin/
#which bash

python $root/check_json.py
# pytest -svx $root/test_urls.py

echo "GITHUB_ACTOR=$GITHUB_ACTOR"
# if [ "$GITHUB_ACTOR" == "" ] || [ "$GITHUB_ACTOR" == "szabgab" ];

echo "GITHUB_EVENT_NAME=$GITHUB_EVENT_NAME"
if [ "$GITHUB_EVENT_NAME" != "pull_request" ];
then
    echo "not a pull-request so we run $root/generate.py"
    python $root/generate.py
fi
