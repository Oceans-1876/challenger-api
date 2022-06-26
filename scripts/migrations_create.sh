#! /usr/bin/env bash

set -e

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
export PYTHONPATH=$PROJECT_ROOT

alembic-autogen-check || alembic revision --autogenerate -m "${@}"
