#! /usr/bin/env bash

set -e

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
export PYTHONPATH=$PROJECT_ROOT

python app/utils/create_env_file.py
