#! /usr/bin/env bash
set -e

# Read POSTGRES_TEST_DB from .env file
export POSTGRES_TEST_DB=tests_fastapi
export $(cat .env | grep POSTGRES_TEST_DB) 1>/dev/null

dropdb --if-exists $POSTGRES_TEST_DB
createdb $POSTGRES_TEST_DB

export PYTHON_TEST=true

bash scripts/run_migrations.sh

pytest --cov=app --cov-report=term-missing --cov-report=html app/tests "${@}"
