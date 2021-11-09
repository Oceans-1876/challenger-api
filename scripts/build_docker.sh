#!/bin/sh

# Exit on error
set -e

# Build docker image
docker build -f ./docker/Dockerfile -t oceans-1876/challenger-api .
