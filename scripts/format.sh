#!/bin/sh -e

set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports alembic app
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py alembic app
black alembic app
isort alembic app
