"""Configuration management for Personal-Claw."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    
    discord_bot_token: str
    discord_allowlisted_user_id: int
    gmail_credentials_path: str = "credentials.json"
    gmail_token_path: str = "token.json"


def load_config() -> Config:
    """
    Load configuration from environment variables.
    
    Loads .env file if present, then validates all required configuration
    values are set. Fails fast with clear error messages if required
    variables are missing.
    
    Returns:
        Config: Configuration instance with all values loaded
        
    Raises:
        ValueError: If required environment variables are missing or invalid
    """
    # Load .env file if it exists
    load_dotenv()
    
    # Required variables
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    discord_user_id = os.getenv("DISCORD_ALLOWLISTED_USER_ID")
    
    # Validate required variables
    missing = []
    if not discord_token:
        missing.append("DISCORD_BOT_TOKEN")
    if not discord_user_id:
        missing.append("DISCORD_ALLOWLISTED_USER_ID")
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Copy .env.example to .env and fill in required values."
        )
    
    # At this point, we know both values are not None due to the check above
    assert discord_token is not None
    assert discord_user_id is not None
    
    # Validate Discord user ID is numeric
    try:
        user_id = int(discord_user_id)
    except ValueError:
        raise ValueError(
            f"DISCORD_ALLOWLISTED_USER_ID must be a valid integer, got: {discord_user_id}"
        )
    
    # Optional variables with defaults
    gmail_creds = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    gmail_token = os.getenv("GMAIL_TOKEN_PATH", "token.json")
    
    return Config(
        discord_bot_token=discord_token,
        discord_allowlisted_user_id=user_id,
        gmail_credentials_path=gmail_creds,
        gmail_token_path=gmail_token,
    )
