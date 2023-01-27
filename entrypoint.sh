#!/usr/bin/bash -le

root=$(dirname $0)
printenv | sort

pytest -svx $root/test_json.py
# pytest -svx $root/test_urls.py
if [ "$GITHUB_ACTOR" == "" ] || [ "$GITHUB_ACTOR" == "osdc-code-maven" ];
then
    echo "run $root/generate.py"
    python $root/generate.py
fi
