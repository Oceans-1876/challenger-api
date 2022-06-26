#! /usr/bin/env bash

set -e

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
export PYTHONPATH=$PROJECT_ROOT

if [[ -z "$1" ]]; then
  echo "Specify the revision to reverse to."
  exit 1
fi

# Run migrations
alembic downgrade "$1"
