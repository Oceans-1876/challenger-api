#! /usr/bin/env bash

set -e

python -m smtpd -c DebuggingServer -n localhost:1025
