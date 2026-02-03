"""Gmail API client wrapper.

Provides high-level interface for Gmail operations with automatic OAuth handling.
"""
from __future__ import annotations

from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import Config
from src.token_manager import TokenManager


class GmailClient:
    """Gmail API client with automatic authentication and token management.
    
    Features:
    - Lazy connection (only connects when needed)
    - Automatic token refresh via TokenManager
    - Read-only operations for Phase 1
    - Error handling with clear logging
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize Gmail client with configuration.
        
        Args:
            config: Application configuration with Gmail paths
        """
        self.config = config
        self.token_manager = TokenManager(
            credentials_path=config.gmail_credentials_path,
            token_path=config.gmail_token_path
        )
        self._service: Any = None  # Lazy-loaded Gmail service
    
    def _ensure_connected(self) -> None:
        """Ensure Gmail service is initialized and authenticated.
        
        Creates service connection if not already established.
        TokenManager handles credential refresh automatically.
        """
        if self._service is not None:
            return
        
        # Get valid credentials (TokenManager handles refresh)
        creds = self.token_manager.get_credentials()
        
        # Build Gmail service
        self._service = build('gmail', 'v1', credentials=creds)
        print("Gmail service initialized")
    
    def list_messages(self, max_results: int = 10, query: str = '') -> list[dict[str, Any]]:
        """List messages from Gmail inbox.
        
        Args:
            max_results: Maximum number of messages to return (default: 10)
            query: Gmail query string for filtering (default: empty = all messages)
                   Examples: "is:unread", "from:accountant@example.com"
        
        Returns:
            List of message metadata dicts with 'id' and 'threadId'
            
        Raises:
            HttpError: If Gmail API call fails
        """
        self._ensure_connected()
        
        try:
            # Call Gmail API to list messages
            results = self._service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            print(f"Listed {len(messages)} messages")
            return messages
            
        except HttpError as error:
            print(f"Gmail API error listing messages: {error}")
            raise
    
    def get_message(self, message_id: str, format: str = 'full') -> dict[str, Any]:
        """Get full message details from Gmail.
        
        Args:
            message_id: Gmail message ID
            format: Message format (default: 'full')
                   Options: 'minimal', 'full', 'raw', 'metadata'
        
        Returns:
            Full message object with headers, body, labels, etc.
            
        Raises:
            HttpError: If Gmail API call fails
        """
        self._ensure_connected()
        
        try:
            # Call Gmail API to get message details
            message = self._service.users().messages().get(
                userId='me',
                id=message_id,
                format=format
            ).execute()
            
            print(f"Retrieved message {message_id}")
            return message
            
        except HttpError as error:
            print(f"Gmail API error getting message {message_id}: {error}")
            raise
    
    def get_inbox_summary(self) -> dict[str, Any]:
        """Get inbox summary for testing connection.
        
        Returns:
            Dict with message count and basic info about recent messages
        """
        self._ensure_connected()
        
        try:
            # Get recent messages
            messages = self.list_messages(max_results=5)
            
            summary = {
                'message_count': len(messages),
                'messages': []
            }
            
            # Get basic info for each message
            for msg_meta in messages:
                try:
                    msg = self.get_message(msg_meta['id'], format='metadata')
                    
                    # Extract subject and from headers
                    headers = msg.get('payload', {}).get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    
                    summary['messages'].append({
                        'id': msg['id'],
                        'subject': subject,
                        'from': from_addr
                    })
                except HttpError as error:
                    print(f"Error getting message {msg_meta['id']}: {error}")
                    # Continue with other messages
                    continue
            
            return summary
            
        except HttpError as error:
            print(f"Gmail API error getting inbox summary: {error}")
            raise
