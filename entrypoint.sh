#!/usr/bin/env bash
set -le

root=$(dirname $0)
printenv | sort
#ls -l /usr/bin/
#which bash

pytest -svx $root/test_json.py
# pytest -svx $root/test_urls.py
if [ "$GITHUB_ACTOR" == "" ] || [ "$GITHUB_ACTOR" == "szabgab" ];
then
    echo "run $root/generate.py"
    python $root/generate.py
fi
