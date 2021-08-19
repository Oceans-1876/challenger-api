#!/bin/sh

# Exit on error
set -e

# use DEBUG=echo ./docker.sh to print all commands
export DEBUG=${DEBUG:-""}


# Build docker image
$DEBUG docker build -t oceans-1876/api .
