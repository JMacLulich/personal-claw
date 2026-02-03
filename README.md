# Personal-Claw

**Anxiety-reduction system for financial communications**

Personal-Claw sits between you and financial email sources (accountant, bank, tax office), providing neutral defused summaries via Discord, and enforces mandatory human-in-the-loop approval for all replies. The goal is to break the catastrophizing → avoidance → anxiety → sleep disruption cycle by removing emotional charge from financial communications.

**Repository:** https://github.com/JMacLulich/personal-claw

## Core Features

- Monitor Gmail inbox for emails from allowlisted financial contacts
- Send neutral, defused summaries to Discord using supportive/coaching tone
- Accept input from single allowlisted Discord user ID only (security)
- Support both text and voice input (voice transcribed to text)
- Show draft replies in Discord for review/editing before sending
- Require explicit two-step approval ("send this" → confirm) before actually sending
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
# DISCORD_BOT_TOKEN=<your_token_here>
# DISCORD_ALLOWLISTED_USER_ID=<your_user_id_here>
```

### Required Secrets

You'll need to obtain these credentials:

**1. Discord Bot Token**
- Go to https://discord.com/developers/applications
- Create new application (or use existing one)
- Go to Bot section
- Copy token
- Add to `.env` as `DISCORD_BOT_TOKEN=MTcy4...your_actual_token_here`

**2. Your Discord User ID (Allowlist)**
- In Discord, go to User Settings → Advanced
- Enable Developer Mode
- Right-click your username → Copy ID
- Add to `.env` as `DISCORD_ALLOWLISTED_USER_ID=1234567890123456789`

**3. Gmail OAuth Credentials**
- Go to https://console.cloud.google.com
- Create a new project (or use existing one)
- Enable Gmail API (APIs & Services → Enable APIs)
- Create OAuth 2.0 credentials (Desktop app type)
- Download as `credentials.json` and save to project root
- The bot will automatically create `token.json` on first run

### 3. Run the Bot

```bash
source .venv/bin/activate
python src/main.py
```

First run opens your MacBook's browser for Google OAuth flow. The bot creates `token.json` automatically.

## Development

This project uses **OpenClaw CLI** to run the bot. You'll start Personal-Claw by running:

```bash
openclaw
```

**Project Structure:**

```
personal-claw/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── bot.py             # Discord bot
│   ├── auth.py            # User allowlist enforcement
│   ├── gmail_client.py     # Gmail API client
│   └── token_manager.py    # OAuth token management
├── .env                   # Your secrets (gitignored)
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

**Key Dependencies:**

- **py-cord** (2.6+) — Discord bot framework
- **google-api-python-client** — Gmail API integration
- **google-auth-oauthlib** — OAuth for Gmail
- **google-auth-httplib2** — HTTP transport for Gmail
- **python-dotenv** — Environment variable management

All secrets are excluded from git via `.gitignore` (`.env`, `token.json`, `credentials.json`).

## Architecture

- **Security:** Bot only responds to allowlisted user ID — rejects all other users
- **Privacy:** Financial emails never logged or stored beyond operational needs
- **Safety:** NO auto-send under any circumstances — explicit approval required
- **Interface:** Discord only — no web UI, no email client
- **Voice:** Supports voice input as first-class (for checking while driving/walking)
- **Tone:** Supportive/coaching (not clinical, not patronizing)

## Deployment Security

How to run OpenClaw safely on your MeLE N100 (headless system):

### Dedicated Sandbox (Rootless Container)

**Rootless Podman:**
- Run OpenClaw in a rootless container (not a root Docker daemon)
- `--cap-drop=ALL` — Drop all Linux capabilities
- `--security-opt=no-new-privileges` — No privilege escalation
- `--read-only` — Container filesystem is read-only (no writes except OpenClaw data volume)
- `--cap-drop ALL` — Drop all capabilities (no sudo, no raw sockets)

**Tight Network Rules:**
- No inbound ports exposed — OpenClaw connects outbound only (Discord, Gmail APIs)
- Outbound allow only: DNS (53) + HTTPS (443) for Gmail + Discord APIs

**Secrets Hygiene:**
- Keep tokens/API keys in chmod 600 env file owned by non-root user
- Never bake secrets into images or shell history
- Least-privilege app permissions:
  - Mail: start with read + draft only, no auto-send
  - OpenClaw: disable marketplace/community skills; disable any tools that run shell commands or browse filesystem
  - Control-plane safety: Discord DM-only (or one private channel) + allowlist your Discord user ID

### Risk Assessment

If N100 is compromised:
- **Containment:** Rootless container, no host filesystem access, tight network rules
- **Data Isolation:** OpenClaw data in dedicated volume, not on host
- **Least Privileges:** No sudo, no raw sockets, no capability escalation
- **Audit Trail:** All "draft created" and "sent" actions logged
- **No Inbound Services:** OpenClaw connects outbound only
- **No Arbitrary Code:** Security-opt prevents new privileges, no shell access to host

If an attacker gets code access:
- They still can't: Read-only filesystem, no tools inside container
- They're limited to: OpenClaw APIs only (Gmail read + Discord outbound)
- Host filesystem access: Read-only mount (no writes)
- Arbitrary network access: Outbound-only rules

What this protects against:
- Code execution on N100 (container doesn't have tools)
- Escalation beyond container (no sudo, no raw sockets)
- Access to your host system (no host mounts, outbound-only network)

### Quick Checklist

Before running `openclaw` on N100:
- [x] N100 host firewall configured (allow outbound, SSH locked down)
- [ ] SSH allow rules pinned to Tailscale interface (tailscale0) where possible
- [ ] Secrets in env file have correct permissions (chmod 600)
- [ ] OpenClaw marketplace skills disabled
- [ ] Secrets not hardcoded in any files
- [ ] Rootless container configured with tight security options

This setup creates a hardened sandbox for OpenClaw. Even if the container is compromised, attacker options are extremely limited.

