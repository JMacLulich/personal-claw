#!/bin/bash
# Deploy Personal-Claw to N100 box
#
# Syncs code to remote server, excluding development/private files.
# Run from project root: ./scripts/deploy.sh

set -e

# Configuration
REMOTE_HOST="n100alerts"
REMOTE_PATH="~/personal-claw/"
LOCAL_PATH="."

echo "🚀 Deploying Personal-Claw to ${REMOTE_HOST}..."

# Rsync options:
# -a: archive mode (preserves permissions, timestamps)
# -v: verbose
# -z: compress during transfer
# --delete: remove files on remote that don't exist locally
# --exclude: skip these files/directories

rsync -avz --delete \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude '.env' \
  --exclude 'token.json' \
  --exclude 'credentials.json' \
  --exclude '*.pyc' \
  --exclude '.DS_Store' \
  "${LOCAL_PATH}/" \
  "${REMOTE_HOST}:${REMOTE_PATH}"

echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. SSH to server: ssh ${REMOTE_HOST}"
echo "2. Install service: cd ~/personal-claw && sudo ./scripts/service-install.sh"
echo "3. Check status: sudo systemctl status personal-claw"
