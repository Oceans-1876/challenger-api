#! /usr/bin/env bash
set -e

export PYTHON_TEST=true

# Read POSTGRES_TEST_DB from .env file
export $(cat .env | grep POSTGRES_TEST_DB) 1>/dev/null

dropdb --if-exists "$POSTGRES_TEST_DB"
createdb "$POSTGRES_TEST_DB"
echo "CREATE EXTENSION postgis" | psql -d "$POSTGRES_TEST_DB"
echo "CREATE EXTENSION pg_trgm" | psql -d "$POSTGRES_TEST_DB"

bash scripts/migrations_forward.sh

bash scripts/import_data.sh

pytest app/tests "${@}"
