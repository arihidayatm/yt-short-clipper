# Google Cloud APIs Integration Guide

## Overview

YT Short Clipper now supports **Google Cloud APIs** as an alternative to OpenAI for Speech-to-Text (Whisper) and Text-to-Speech services.

## What This Means

Instead of using OpenAI's APIs, you can now:
- **Transcribe videos** using Google Cloud Speech-to-Text
- **Generate audio** using Google Cloud Text-to-Speech

This is useful if:
- Your OpenAI account has API quota limits
- You want to use Google Cloud services
- You need support for additional languages/voices

## Quick Start (5 minutes)

### 1. Create Google Cloud Service Account

Visit: https://console.cloud.google.com/iam-admin/serviceaccounts

1. Click "CREATE SERVICE ACCOUNT"
2. Fill in details and create
3. Go to "ROLES" and add these permissions:
   - Cloud Speech-to-Text API User
   - Cloud Text-to-Speech API User

### 2. Download Credentials

1. Go to "KEYS" tab
2. Click "ADD KEY" > "Create new key"
3. Select "JSON" and download

### 3. Place Credentials File

Save the downloaded JSON file as:
```bash
google-cloud-credentials.json
```

in your YT Short Clipper directory

### 4. Run Setup Script

```bash
cd ~/yt-short-clipper
./setup_google_cloud.sh
```

### 5. Start Using!

```bash
./run.sh
```

## File Structure After Setup

```
yt-short-clipper/
├── google-cloud-credentials.json      ← Your Google Cloud credentials
├── config.json                        ← Updated with Google Cloud providers
├── setup_google_cloud.sh              ← Interactive setup script
├── update_google_cloud_config.py      ← Config updater
├── GOOGLE_CLOUD_SETUP.md              ← Detailed guide
├── GOOGLE_CLOUD_INTEGRATION_SUMMARY.md← Complete summary
└── ... other files
```

## Configuration Example

After setup, your `config.json` will include:

```json
{
  "ai_providers": {
    "caption_maker": {
      "provider": "google-cloud",
      "credentials_path": "google-cloud-credentials.json"
    },
    "hook_maker": {
      "provider": "google-cloud", 
      "credentials_path": "google-cloud-credentials.json"
    }
  }
}
```

## Pricing

| Service | Free Tier | Paid |
|---------|-----------|------|
| Speech-to-Text | 60 min/month | $0.024 per 15 sec |
| Text-to-Speech | 1M chars/month | $0.016 per 1K chars |

## Troubleshooting

| Error | Solution |
|-------|----------|
| Credentials file not found | Run: `ls google-cloud-credentials.json` |
| Permission denied | Add roles to service account, wait 1-2 min |
| API not enabled | Go to https://console.cloud.google.com/apis/library and enable APIs |

## Reverting to OpenAI

If you want to switch back, edit `config.json`:

```json
{
  "ai_providers": {
    "caption_maker": {
      "provider": "openai",
      "api_key": "sk-your-key"
    },
    "hook_maker": {
      "provider": "openai",
      "api_key": "sk-your-key"
    }
  }
}
```

## Additional Resources

- [Complete Setup Guide](GOOGLE_CLOUD_SETUP.md)
- [Integration Summary](GOOGLE_CLOUD_INTEGRATION_SUMMARY.md)
- [Google Cloud Speech-to-Text Docs](https://cloud.google.com/speech-to-text/docs)
- [Google Cloud Text-to-Speech Docs](https://cloud.google.com/text-to-speech/docs)

## Support

For help:
1. Check the detailed guides listed above
2. Review console error messages
3. Check Google Cloud quotas and permissions
4. See troubleshooting section above

---

**Selesai!** Anda siap menggunakan Google Cloud APIs! 🎉
