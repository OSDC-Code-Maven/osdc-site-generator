#!/usr/bin/bash -e

# compare the CI filse of all the courses to the one in the skeleton

for name in osdc-2023-01-perl osdc-2023-01-public osdc-2023-03-azrieli
do
    echo "======"
    echo $name
    diff ../osdc-skeleton/.github/workflows/ci.yml ../$name/.github/workflows/ci.yml
done
