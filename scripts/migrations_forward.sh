#! /usr/bin/env bash

set -e

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
export PYTHONPATH=$PROJECT_ROOT

# Forward migrations to the given revision. Default to `head` if a revision is not passed.
alembic upgrade "${1:-head}"
