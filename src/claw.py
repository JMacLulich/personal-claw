"""Personal-Claw application orchestrator.

This is the main business logic layer that coordinates between Discord bot
and Gmail client. The bot handles UI (commands, responses), PersonalClaw
handles what to do, and GmailClient handles how to fetch from Gmail.

Clean separation of concerns:
- Discord bot: UI layer (commands, responses)
- PersonalClaw: Business logic (what to do with data)
- GmailClient: Data layer (how to fetch from Gmail)
"""

from __future__ import annotations

from typing import Any

from googleapiclient.errors import HttpError

from src.config import Config
from src.gmail_client import GmailClient


class PersonalClaw:
    """Main application orchestrator for Personal-Claw.
    
    Coordinates between Discord commands and Gmail operations.
    Provides high-level methods that Discord bot can call.
    """
    
    def __init__(self, config: Config) -> None:
        """Initialize PersonalClaw with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.gmail_client = GmailClient(config)
        print("PersonalClaw initialized")
    
    async def check_inbox(self) -> str:
        """Check Gmail inbox and return formatted summary.
        
        Returns:
            User-friendly string with inbox summary
            Format: "📬 You have X messages in your inbox"
            
        Handles Gmail API errors gracefully with user-friendly messages.
        """
        try:
            summary = self.gmail_client.get_inbox_summary()
            message_count = summary['message_count']
            
            if message_count == 0:
                return "📭 Your inbox is empty. Nice!"
            elif message_count == 1:
                return "📬 You have 1 message in your inbox"
            else:
                return f"📬 You have {message_count} messages in your inbox"
        
        except HttpError as error:
            print(f"Gmail API error in check_inbox: {error}")
            return "❌ Sorry, I couldn't reach Gmail right now. Try again in a moment?"
        
        except Exception as error:
            print(f"Unexpected error in check_inbox: {error}")
            return "❌ Something went wrong. Let me know if this keeps happening."
    
    def get_message_count(self) -> int:
        """Get count of messages in inbox.
        
        Returns:
            Number of messages (0 if error)
            
        Used for quick status checks without full summary.
        """
        try:
            summary = self.gmail_client.get_inbox_summary()
            return summary['message_count']
        
        except Exception as error:
            print(f"Error getting message count: {error}")
            return 0
