"""
Discord Bot for Personal-Claw

This bot provides:
- User allowlist enforcement via global @bot.check decorator
- Commands for inbox checking and status
- Integration with PersonalClaw orchestrator (when available)
- Gmail client integration

All commands protected by single-user allowlist check.
"""

import discord
from discord.ext import commands
from src.auth import check_allowlisted_user
from src.config import load_config
from src.gmail_client import GmailClient
from src.token_manager import TokenManager

# Load configuration
config = load_config()

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Create Gmail client instance
token_manager = TokenManager(
    credentials_path=config.gmail_credentials_path,
    token_path=config.gmail_token_path
)
gmail_client = GmailClient(token_manager)


@bot.event
async def on_ready():
    """Bot startup - loaded config, ready to serve."""
    print(f"✅ Bot connected as {bot.user.name}")
    print("✅ Gmail connected")
    print("🎯 Bot is online and ready!")
    print(f"📬 Status: Responding to commands from {bot.user.name} only")


@bot.check(check_allowlisted_user)
async def ping(ctx):
    """Ping command - bot health check with allowlist enforcement."""
    await ctx.send("Pong! You're authorized. 🎯")


@bot.check(check_allowlisted_user)
async def status(ctx):
    """Get bot status - check Gmail connection, inbox count."""
    # Try to get message count (may fail if Gmail not configured yet)
    try:
        count = await gmail_client.get_message_count()
    except Exception:
        count = 0
    
    # Format response
    response = "📬 Status:\n"
    response += f"📬 Messages: {count}\n"
    
    # Connection status
    if gmail_client.is_connected():
        response += f"📬 Gmail: {'✅ Connected'}\n"
    else:
        response += f"📬 Gmail: {'❌ Disconnected'}\n"
    
    # Bot status
    if bot.is_ready():
        response += f"📬 Discord: {'✅ Connected'}\n"
    else:
        response += f"📬 Discord: {'❌ Disconnected'}\n"
    
    response += "📬 All systems operational"
    
    await ctx.send(response)


@bot.check(check_allowlisted_user)
async def check_inbox(ctx):
    """Check inbox - fetch Gmail summary."""
    # Get inbox summary from Gmail client
    summary = await gmail_client.get_inbox_summary()
    
    # Send summary
    await ctx.send(f"📬 Inbox Summary:\n{summary}")


@bot.command(name="status", description="Check bot and inbox status")
async def cmd_status(ctx):
    """Command: /status - Get bot and Gmail status."""
    # Get message count
    try:
        count = await gmail_client.get_message_count()
    except Exception:
        count = 0
    
    # Format response
    response = "📬 Status:\n"
    response += f"📬 Messages: {count}\n"
    
    # Connection status
    if gmail_client.is_connected():
        response += f"📬 Gmail: {'✅ Connected'}\n"
    else:
        response += f"📬 Gmail: {'❌ Disconnected'}\n"
    
    # Bot status
    if bot.is_ready():
        response += f"📬 Discord: {'✅ Connected'}\n"
    else:
        response += f"📬 Discord: {'❌ Disconnected'}\n"
    
    response += "📬 All systems operational"
    
    await ctx.send(response)


@bot.command(name="check-inbox", description="Check your Gmail inbox")
async def cmd_check_inbox(ctx):
    """Command: /check-inbox - Fetch Gmail summary."""
    # Get inbox summary
    summary = await gmail_client.get_inbox_summary()
    
    # Send summary
    await ctx.send(f"📬 Inbox Summary:\n{summary}")


def main():
    """Main entry point: load config, create bot, start it."""
    print(f"Starting bot with allowlisted user ID: {config.discord_allowlisted_user_id}")
    
    bot.run(config.discord_bot_token)


if __name__ == "__main__":
    main()
