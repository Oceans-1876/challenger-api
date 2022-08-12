#!/bin/sh

set -e

docker build -f ./docker/Dockerfile -t oceans-1876/challenger-api .
