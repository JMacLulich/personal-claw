"""OAuth token management for Gmail API.

Handles token lifecycle: initial OAuth flow, storage, expiry checking, and automatic refresh.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class TokenManager:
    """Manages OAuth tokens for Gmail API with automatic refresh.
    
    Handles:
    - Initial OAuth flow for new tokens
    - Token persistence to disk
    - Expiry detection and automatic refresh
    - Health checks for proactive monitoring
    
    Scopes: Read-only access to Gmail (gmail.readonly) for Phase 1.
    """
    
    # Read-only scope for Phase 1 - send capability comes later
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: str, token_path: str) -> None:
        """Initialize token manager with file paths.
        
        Args:
            credentials_path: Path to credentials.json (OAuth client ID from Google Cloud Console)
            token_path: Path to token.json (stored access/refresh tokens)
        """
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        
        # Validate credentials file exists
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {credentials_path}\n"
                "Download credentials.json from Google Cloud Console:\n"
                "1. Go to https://console.cloud.google.com/apis/credentials\n"
                "2. Create OAuth 2.0 Client ID (Desktop app)\n"
                "3. Download JSON and save as credentials.json"
            )
    
    def get_credentials(self) -> Credentials:
        """Get valid credentials, refreshing if needed or running OAuth flow if not found.
        
        Returns:
            Valid OAuth2 credentials for Gmail API
            
        Raises:
            Exception: If OAuth flow fails or refresh fails
        """
        creds: Credentials | None = None
        
        # Load existing token if available
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), self.SCOPES)
        
        # If no valid credentials available, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Token expired but we have refresh token - refresh it
                print("Token expired, refreshing...")
                creds.refresh(Request())
                print("Token refreshed successfully")
            else:
                # No token or no refresh token - run OAuth flow
                print("No valid token found, starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), self.SCOPES
                )
                # Run local server flow (opens browser for authorization)
                creds = flow.run_local_server(port=0)
                print("OAuth flow completed successfully")
            
            # Save the credentials for the next run
            self._save_token(creds)
        
        return creds
    
    def _save_token(self, creds: Credentials) -> None:
        """Save credentials to token file.
        
        Args:
            creds: OAuth2 credentials to save
        """
        # Ensure token directory exists
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save credentials to JSON file
        with open(self.token_path, 'w') as token_file:
            token_file.write(creds.to_json())
        
        print(f"Token saved to {self.token_path}")
    
    def health_check(self) -> bool:
        """Check if credentials are valid without triggering refresh.
        
        Returns:
            True if credentials are valid and not expired, False otherwise
        """
        if not self.token_path.exists():
            return False
        
        try:
            creds = Credentials.from_authorized_user_file(str(self.token_path), self.SCOPES)
            # Check if credentials exist and are valid (not expired)
            return creds and creds.valid
        except Exception:
            # Any error reading/parsing token = not healthy
            return False
