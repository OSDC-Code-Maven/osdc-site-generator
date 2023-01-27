#!/usr/bin/env bash
set -ex

root=$(dirname $0)
printenv | sort
#ls -l /usr/bin/
#which bash

pytest -svx $root/test_json.py
# pytest -svx $root/test_urls.py
# if [ "$GITHUB_ACTOR" == "" ] || [ "$GITHUB_ACTOR" == "szabgab" ];
if [ "$GITHUB_EVENT_NAME" != "pull_request" ];
then
    echo "run $root/generate.py"
    python $root/generate.py
fi
