#!/bin/sh -le

root=$(dirname $0)

pytest -svx $root/test_json.py
pytest -svx $root/test_urls.py
python $root/generate.py
