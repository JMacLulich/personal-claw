#!/bin/bash

set -e

if [ ! -f ".env" ]; then
    echo ".env not found. Copy .env.example to .env first."
    exit 1
fi

missing=()

if ! grep -q "^DISCORD_BOT_TOKEN=" .env; then
    missing+=("DISCORD_BOT_TOKEN")
fi

if ! grep -q "^DISCORD_ALLOWLISTED_USER_ID=" .env; then
    missing+=("DISCORD_ALLOWLISTED_USER_ID")
fi

if [ ${#missing[@]} -gt 0 ]; then
    echo "Missing required entries in .env: ${missing[*]}"
    exit 1
fi

echo "Discord env vars present in .env"
