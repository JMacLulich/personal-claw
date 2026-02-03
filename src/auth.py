"""User authentication and authorization for Personal-Claw.

This module enforces single-user access control by validating Discord user IDs
against the allowlisted user ID from configuration. The allowlist check is
designed to be used as a global bot check decorator, ensuring all commands
require authorization.
"""

from discord.ext import commands

from src.config import load_config


def check_allowlisted_user(ctx: commands.Context) -> bool:
    """
    Global check: only allowlisted user can use bot commands.
    
    This function is designed to be used with @bot.check decorator to enforce
    authorization at the bot level, preventing any command execution from
    non-allowlisted users.
    
    Args:
        ctx: Discord command context containing author information
        
    Returns:
        True if ctx.author.id matches allowlisted user ID, False otherwise
    """
    config = load_config()
    
    # Check if user ID matches allowlisted user
    if ctx.author.id != config.discord_allowlisted_user_id:
        # Log rejection (user attempted to use bot but not authorized)
        print(f"Rejected command from unauthorized user: {ctx.author.id}")
        return False
    
    return True
