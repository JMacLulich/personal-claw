#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run ./scripts/bootstrap.sh first."
    exit 1
fi

source .venv/bin/activate
python scripts/check_token.py
