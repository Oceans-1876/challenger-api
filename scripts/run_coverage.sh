#! /usr/bin/env bash
set -e

bash scripts/run_tests.sh --cov=app --cov-report=term-missing --cov-report=html
