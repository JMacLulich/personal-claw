#!/usr/bin/env python3
"""Manual test script for Gmail connection.

This script tests the OAuth flow and Gmail API connection end-to-end.
Requires real credentials.json file and user interaction for OAuth.

Usage:
    python scripts/test_gmail.py

Prerequisites:
    1. Create OAuth 2.0 credentials in Google Cloud Console
    2. Download credentials.json and place in project root
    3. Run this script - it will open browser for OAuth authorization
    4. After authorization, token.json will be saved for future use
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config
from src.gmail_client import GmailClient


def main() -> None:
    """Test Gmail connection with real OAuth flow."""
    print("=== Gmail Connection Test ===\n")
    
    # Load configuration
    try:
        config = load_config()
        print(f"✓ Configuration loaded")
        print(f"  Credentials: {config.gmail_credentials_path}")
        print(f"  Token: {config.gmail_token_path}\n")
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return
    
    # Create Gmail client
    try:
        client = GmailClient(config)
        print("✓ Gmail client created\n")
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
    
    # Test OAuth flow and get inbox summary
    try:
        print("Testing Gmail connection...")
        print("(This may open a browser window for OAuth authorization)\n")
        
        summary = client.get_inbox_summary()
        
        print("✓ Gmail connection successful!\n")
        print(f"Inbox summary:")
        print(f"  Total messages: {summary['message_count']}\n")
        
        if summary['messages']:
            print("Recent messages:")
            for i, msg in enumerate(summary['messages'], 1):
                print(f"  {i}. From: {msg['from']}")
                print(f"     Subject: {msg['subject']}")
                print(f"     ID: {msg['id']}\n")
        else:
            print("  No messages found (inbox may be empty)")
        
        print("\n✓ All tests passed!")
        print(f"Token saved to: {config.gmail_token_path}")
        print("Future runs will use saved token (no browser required)")
        
    except Exception as e:
        print(f"\n✗ Gmail connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Gmail API is enabled in Google Cloud Console")
        print("2. Check credentials.json is valid")
        print("3. Verify OAuth consent screen is configured")
        print("4. If token.json exists, try deleting it and re-authorizing")


if __name__ == '__main__':
    main()
