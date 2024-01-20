#!/bin/bash

set -e # stop immediately on errors
set -o pipefail # do not silently ignore errors in pipelines
cd "${0%/*}" # cd into script's current location
cd .. # cd into the root directory of the project

echo "=== Add all challenges locally ==="
for i in `find . -name 'challenge.yml' 2>/dev/null | sort`; do
    dir=$(dirname $i)
    echo " [*] Adding $dir ($i)"
    ctf challenge add "$dir"
done


