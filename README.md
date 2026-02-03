# Personal-Claw

**Anxiety-reduction system for financial communications**

Personal-Claw sits between you and financial email sources (accountant, bank, tax office), providing neutral defused summaries via Discord with mandatory human-in-the-loop approval for all replies. The goal is to break the catastrophizing → avoidance → anxiety cycle by removing emotional charge from financial communications.

## Core Features

- Monitor Gmail inbox for emails from allowlisted financial contacts
- Send neutral, defused summaries to Discord using supportive/coaching tone
- Accept input from single allowlisted Discord user ID only (security)
- Support both text and voice input (voice transcribed to text)
- Show draft replies in Discord for review/editing before sending
- Require explicit two-step approval before actually sending any reply
- Never auto-send under any circumstances

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and fill in required values
```

### Required Secrets

You'll need to obtain these credentials:

1. **Discord Bot Token** - Get from [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application → Bot → Copy token
   - Add to `.env` as `DISCORD_BOT_TOKEN`

2. **Discord User ID** - Your allowlisted user ID (Jason only)
   - Enable Developer Mode in Discord settings
   - Right-click your username → Copy ID
   - Add to `.env` as `DISCORD_ALLOWLISTED_USER_ID`

3. **Gmail credentials.json** - Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Enable Gmail API for your project
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` in project root

### 3. Run the Bot

```bash
source .venv/bin/activate
python src/main.py
```

## Architecture

- **Security**: Bot only responds to allowlisted user ID - rejects all other users
- **Privacy**: Financial emails never logged or stored beyond operational needs
- **Safety**: NO auto-send under any circumstances - explicit approval required
- **Interface**: Discord only - no web UI, no email client
- **Voice**: Supports voice input as first-class (for checking while driving/walking)
- **Tone**: Supportive/coaching (not clinical, not patronizing)

## Project Structure

```
personal-claw/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   └── main.py            # (Coming soon)
├── .env.example           # Environment variable template
├── .env                   # Your secrets (gitignored)
├── requirements.txt       # Python dependencies
└── README.md
```

## Development

This project uses:
- **py-cord** (2.6+) - Discord bot framework
- **google-api-python-client** - Gmail API integration
- **python-dotenv** - Environment variable management

All secrets are excluded from git via `.gitignore` (`.env`, `token.json`, `credentials.json`).
