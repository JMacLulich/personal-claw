"""Discord bot for Personal-Claw with single-user authorization.

This module creates the Discord bot with global allowlist enforcement via
@bot.check decorator. All commands require authorization - there is no way
to bypass this check.

Security approach:
- @bot.check runs before ALL commands automatically
- Fails closed: default deny for unauthorized users
- Single point of enforcement: impossible to forget on new commands
"""

import discord
from discord.ext import commands

from src.auth import check_allowlisted_user
from src.config import load_config


def create_bot() -> discord.Bot:
    """
    Create and configure the Discord bot instance.
    
    Returns bot with global allowlist check and commands registered.
    """
    bot = discord.Bot()
    
    # Global check: enforce allowlist for ALL commands
    @bot.check
    def global_allowlist_check(ctx: commands.Context) -> bool:
        """
        Global check that runs before every command.
        
        This ensures only the allowlisted user can execute any bot command.
        Security-first: impossible to bypass, runs automatically for all commands.
        """
        return check_allowlisted_user(ctx)
    
    @bot.event
    async def on_ready():
        """Log when bot successfully connects to Discord."""
        print(f"Bot connected as {bot.user}")
        print(f"Bot ID: {bot.user.id}")
        print("Ready to receive commands from allowlisted user")
    
    @bot.event
    async def on_application_command_error(ctx: commands.Context, error: Exception):
        """
        Handle errors during command execution.
        
        Specifically handles CheckFailure errors to provide user-friendly feedback
        when unauthorized users attempt to use the bot.
        """
        if isinstance(error, commands.CheckFailure):
            # User failed allowlist check - send private rejection message
            try:
                await ctx.respond(
                    "Sorry, this bot is private and only responds to its owner.",
                    ephemeral=True  # Only visible to user who tried the command
                )
            except Exception as e:
                # If we can't respond (e.g., no permission), log it
                print(f"Could not send rejection message: {e}")
        else:
            # Other errors - log and notify user
            print(f"Command error: {error}")
            try:
                await ctx.respond(
                    "An error occurred while processing your command.",
                    ephemeral=True
                )
            except Exception:
                pass
    
    @bot.command(name="ping", description="Test if bot is responding")
    async def ping(ctx: commands.Context):
        """
        Test command to verify bot is working and user is authorized.
        
        This command will only execute if the user passes the global allowlist check.
        """
        await ctx.respond("Pong! You're authorized. 🎯")
    
    return bot


def main():
    """Main entry point: load config and start bot."""
    config = load_config()
    print(f"Starting bot with allowlisted user ID: {config.discord_allowlisted_user_id}")
    
    # Create bot instance when running (not at import time)
    bot = create_bot()
    bot.run(config.discord_bot_token)


if __name__ == "__main__":
    main()
