#!/usr/bin/env python3
"""OAuth bootstrap script for Gmail.

Creates or refreshes token.json using credentials.json.

Usage:
    python scripts/test_gmail.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_gmail_config
from src.token_manager import TokenManager


def main() -> None:
    """Test Gmail connection with real OAuth flow."""
    print("=== Gmail OAuth Bootstrap ===\n")
    
    # Load configuration
    try:
        config = load_gmail_config()
        print("✓ Configuration loaded")
        print(f"  Credentials: {config.gmail_credentials_path}")
        print(f"  Token: {config.gmail_token_path}\n")
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return
    
    # Create token manager
    try:
        token_manager = TokenManager(
            credentials_path=config.gmail_credentials_path,
            token_path=config.gmail_token_path,
        )
        print("✓ Token manager created\n")
    except FileNotFoundError as e:
        print(f"✗ {e}\n")
        print("Setup instructions:")
        print("1. Go to https://console.cloud.google.com/apis/credentials")
        print("2. Create OAuth 2.0 Client ID (Desktop app)")
        print("3. Download JSON and save as credentials.json")
        print("4. Enable Gmail API for your project")
        return
    except Exception as e:
        print(f"✗ Failed to create Gmail client: {e}")
        return
    
    # Run OAuth flow and persist token.json
    try:
        print("Starting OAuth flow...")
        print("(This may open a browser window for authorization)\n")

        token_manager.get_credentials()

        print("✓ OAuth completed successfully!")
        print(f"Token saved to: {config.gmail_token_path}")
        print("Future runs will use the saved token (no browser required)")
        
    except Exception as e:
        print(f"\n✗ OAuth flow failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Gmail API is enabled in Google Cloud Console")
        print("2. Check credentials.json is valid")
        print("3. Verify OAuth consent screen is configured")
        print("4. If token.json exists, try deleting it and re-authorizing")


if __name__ == '__main__':
    main()
