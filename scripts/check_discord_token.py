#!/usr/bin/env python3
"""Quick Discord token validation."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import discord

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config


async def _check_token(token: str) -> None:
    intents = discord.Intents.none()
    client = discord.Client(intents=intents)
    try:
        await client.login(token)
        user = client.user
        if user:
            print(f"✓ Discord token valid: {user.name} ({user.id})")
        else:
            print("✓ Discord token valid")
    finally:
        await client.close()


def main() -> None:
    print("=== Discord Token Check ===\n")
    config = load_config()
    try:
        asyncio.run(_check_token(config.discord_bot_token))
    except discord.LoginFailure:
        print("✗ Invalid Discord token")
    except Exception as exc:
        print(f"✗ Discord token check failed: {exc}")


if __name__ == "__main__":
    main()
