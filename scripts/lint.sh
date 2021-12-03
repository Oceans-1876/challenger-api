#!/usr/bin/env bash

set -x

mypy app
black alembic app --check
isort --check-only alembic app
isort .
flake8
