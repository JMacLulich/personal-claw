#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Running Gmail OAuth bootstrap..."
python scripts/test_gmail.py
