#! /usr/bin/env bash

export PYTHONPATH=$PWD

# Run migrations
alembic upgrade head

# Create initial data in DB
python $PWD/app/db/init_data.py
