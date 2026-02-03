#!/bin/bash
# Install Personal-Claw as systemd service
#
# This script must be run ON THE N100 BOX (not locally).
# Run with sudo: sudo ./scripts/service-install.sh

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "❌ This script must be run with sudo"
   echo "Usage: sudo ./scripts/service-install.sh"
   exit 1
fi

# Configuration
SERVICE_FILE="personal-claw.service"
SYSTEMD_PATH="/etc/systemd/system/personal-claw.service"

echo "🔧 Installing Personal-Claw systemd service..."

# Check service file exists
if [ ! -f "${SERVICE_FILE}" ]; then
    echo "❌ Error: ${SERVICE_FILE} not found"
    echo "Make sure you're running this from the project root"
    exit 1
fi

# Copy service file to systemd directory
echo "📋 Copying service file to ${SYSTEMD_PATH}"
cp "${SERVICE_FILE}" "${SYSTEMD_PATH}"

# Reload systemd daemon to recognize new service
echo "🔄 Reloading systemd daemon"
systemctl daemon-reload

# Enable service (start on boot)
echo "✅ Enabling service to start on boot"
systemctl enable personal-claw

# Start service now
echo "▶️  Starting service"
systemctl start personal-claw

# Wait a moment for service to start
sleep 2

# Show status
echo ""
echo "✅ Installation complete!"
echo ""
echo "Service status:"
systemctl status personal-claw --no-pager

echo ""
echo "Useful commands:"
echo "  Check status:  sudo systemctl status personal-claw"
echo "  Stop service:  sudo systemctl stop personal-claw"
echo "  Start service: sudo systemctl start personal-claw"
echo "  View logs:     journalctl -u personal-claw -f"
echo "  Restart:       sudo systemctl restart personal-claw"
