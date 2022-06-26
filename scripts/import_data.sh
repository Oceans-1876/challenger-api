#! /usr/bin/env bash

set -e

TEST=0

while test $# -gt 0; do
    case "$1" in
    -t | --test)
        TEST=1
        shift
        ;;
    esac
done

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
export PYTHONPATH=$PROJECT_ROOT

# Create initial data in DB
if [ "$TEST" == 1 ]; then
   python app/db/init_data.py --testing
else
   python app/db/init_data.py
fi
