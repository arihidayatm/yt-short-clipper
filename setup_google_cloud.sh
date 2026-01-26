#!/bin/bash
# Quick Start Guide for Google Cloud Setup
# This script provides interactive guidance for setting up Google Cloud APIs

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  YT Short Clipper - Google Cloud API Quick Start          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "config.json" ]; then
    echo "⚠️  config.json not found!"
    echo "    Please run the application at least once first"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo ""
echo "📋 QUICK START CHECKLIST"
echo "════════════════════════════════════════════════════════════"
echo ""

echo "Step 1️⃣  Create Google Cloud Service Account"
echo "─────────────────────────────────────────────"
echo ""
echo "  a) Go to: https://console.cloud.google.com"
echo "  b) Create new project or select existing"
echo "  c) Go to: IAM & Admin > Service Accounts"
echo "  d) Click 'CREATE SERVICE ACCOUNT'"
echo "  e) Fill in details:"
echo "     • Service account name: yt-short-clipper-svc"
echo "     • Description: Service for YT Short Clipper"
echo "  f) Click 'CREATE AND CONTINUE'"
echo ""

read -p "Press Enter after creating service account..."

echo ""
echo "Step 2️⃣  Grant Required Roles"
echo "─────────────────────────────"
echo ""
echo "  a) On the service account page, go to 'ROLES' tab"
echo "  b) Click 'GRANT ROLE' and add:"
echo "     • Cloud Speech-to-Text API User"
echo "     • Cloud Text-to-Speech API User"
echo "  c) Click 'SAVE'"
echo ""

read -p "Press Enter after granting roles..."

echo ""
echo "Step 3️⃣  Create JSON Credentials"
echo "─────────────────────────────"
echo ""
echo "  a) Go to 'KEYS' tab"
echo "  b) Click 'ADD KEY' > 'Create new key'"
echo "  c) Select 'JSON' and click 'CREATE'"
echo "  d) A JSON file will download automatically"
echo ""

read -p "Press Enter after downloading the JSON file..."

echo ""
echo "Step 4️⃣  Move Credentials File"
echo "─────────────────────────────"
echo ""
echo "  Run this command:"
echo "  $ mv ~/Downloads/yt-short-clipper-svc-*.json google-cloud-credentials.json"
echo ""

read -p "Press Enter after moving the file (or after verifying it exists)..."

# Check if credentials file exists
if [ -f "google-cloud-credentials.json" ]; then
    echo "✓ Credentials file found!"
else
    echo "✗ Credentials file not found at: google-cloud-credentials.json"
    echo "  Please download and move it, then run this script again"
    exit 1
fi

echo ""
echo "Step 5️⃣  Update Application Configuration"
echo "──────────────────────────────────────"
echo ""
echo "  Running configuration update script..."
echo ""

# Run the config update script
./venv/bin/python3 update_google_cloud_config.py

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ✓ Setup Complete!                                        ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🚀 Ready to use Google Cloud APIs!"
    echo ""
    echo "Next steps:"
    echo "  1. Run the application: ./run.sh"
    echo "  2. Enter a YouTube URL"
    echo "  3. Enjoy using Google Cloud APIs!"
    echo ""
    echo "📚 For more info:"
    echo "  • GOOGLE_CLOUD_SETUP.md"
    echo "  • GOOGLE_CLOUD_INTEGRATION_SUMMARY.md"
else
    echo ""
    echo "✗ Configuration update failed"
    exit 1
fi
