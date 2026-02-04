#!/usr/bin/env python3
"""Quick Gmail token validation without inbox access."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_gmail_config
from src.token_manager import TokenManager


def main() -> None:
    print("=== Gmail Token Check ===\n")

    config = load_gmail_config()
    token_manager = TokenManager(
        credentials_path=config.gmail_credentials_path,
        token_path=config.gmail_token_path,
    )

    ok, message = token_manager.health_check()
    if ok:
        print(f"✓ {message}")
        print(f"Token: {config.gmail_token_path}")
        return

    print(f"✗ {message}")
    print("If this is unexpected, delete token.json and re-run ./scripts/bootstrap.sh")


if __name__ == "__main__":
    main()
