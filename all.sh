#!/usr/bin/bash -e

# A development helper script to run the generate code on all the courses listed here
# TODO maybe we could create the list of course automatically

for name in osdc-2023-01-perl osdc-2023-01-public osdc-2023-03-azrieli
do
    echo "======"
    echo $name
    cd ../$name
    ../osdc-site-generator/generate.py
    cd -
done
