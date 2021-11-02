#! /usr/bin/env bash

export PYTHONPATH=$PWD

# Create initial data in DB
if [ "$PYTHON_TEST" == true ]
then
   python app/db/init_data.py --testing True
else
   python app/db/init_data.py
fi
