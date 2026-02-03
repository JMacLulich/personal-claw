#!/bin/bash

# Development run script for Personal-Claw
# This script activates the virtual environment and runs the bot
# Follows cmd line toolo best practice

set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Run the bot
echo "🚀 Starting Personal-Claw..."
python src/bot.py
