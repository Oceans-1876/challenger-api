#! /usr/bin/env bash

export PYTHONPATH=$PWD

# Create initial data in DB
python app/db/init_test_data.py