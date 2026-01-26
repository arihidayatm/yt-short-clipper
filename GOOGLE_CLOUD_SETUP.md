# Google Cloud Speech-to-Text & Text-to-Speech Setup

## Prerequisites

1. **Google Cloud Account** - https://console.cloud.google.com/
2. **Google Cloud Project** - Create a new project or use existing one

## Step-by-Step Setup

### Step 1: Enable APIs

1. Go to https://console.cloud.google.com/apis/library
2. Search for and enable these APIs:
   - **Cloud Speech-to-Text API**
   - **Cloud Text-to-Speech API**

### Step 2: Create Service Account

1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts/
2. Click "Create Service Account"
3. Fill in details:
   - **Service account name**: `yt-clipper-service`
   - Click "Create and Continue"

### Step 3: Grant Roles

1. In the "Grant this service account access to project" section:
2. Add these roles:
   - ✅ Cloud Speech-to-Text API User
   - ✅ Cloud Text-to-Speech API User
3. Click "Continue"

### Step 4: Create Key

1. Click "Create Key" button
2. Choose **JSON** format
3. Click "Create"
4. A JSON file will download automatically
5. **Save this file** - you'll need it for the app

### Step 5: Copy Credentials to App

1. Rename the downloaded JSON file to `google-cloud-credentials.json`
2. Place it in the app directory:
   ```
   /home/mahdev/Automation/yt-short-clipper/google-cloud-credentials.json
   ```

### Step 6: Update Config

Run this to update configuration:

```bash
cd /home/mahdev/Automation/yt-short-clipper
./venv/bin/python << 'EOF'
import json
from config.config_manager import ConfigManager
from pathlib import Path

app_dir = Path.cwd()
config_file = app_dir / "config.json"
output_dir = app_dir / "output"

config_mgr = ConfigManager(config_file, output_dir)
config = config_mgr.config

# Update providers to use Google Cloud
creds_path = str(app_dir / "google-cloud-credentials.json")

config["ai_providers"]["caption_maker"] = {
    "provider": "google-cloud",
    "credentials_path": creds_path,
    "model": "whisper-1"
}

config["ai_providers"]["hook_maker"] = {
    "provider": "google-cloud",
    "credentials_path": creds_path,
    "model": "tts-1"
}

config_mgr.save_config(config)
print("✓ Config updated to use Google Cloud APIs")
EOF
```

## Configuration

The app will use:

| Component | Provider | Status |
|-----------|----------|--------|
| Highlight Detection | Google Gemini | ✅ |
| Speech-to-Text | Google Cloud | ✅ |
| Text-to-Speech | Google Cloud | ✅ |

## Cost Estimates (Monthly Free Tier)

- **Speech-to-Text**: 60 minutes free per month
  - Then $0.024 per 15 seconds
- **Text-to-Speech**: 0 free tier, then $0.016 per 1K characters
  - ~$0.50 for 1 hour of spoken content

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution:** Make sure `google-cloud-credentials.json` is in the app directory with correct path in config.

### Error: "Permission denied"

**Solution:** Check service account has these roles:
- Cloud Speech-to-Text API User
- Cloud Text-to-Speech API User

### Error: Module not found

**Solution:** Install Google Cloud libraries:
```bash
./venv/bin/pip install -r requirements.txt
```

## Testing

Test Google Cloud setup:

```bash
cd /home/mahdev/Automation/yt-short-clipper
./venv/bin/python << 'EOF'
from utils.google_cloud_adapters import GoogleCloudSpeechToTextAdapter
from pathlib import Path

creds_path = Path.cwd() / "google-cloud-credentials.json"

# Test Speech-to-Text
print("Testing Google Cloud Speech-to-Text...")
client = GoogleCloudSpeechToTextAdapter(str(creds_path))
print("✓ Connected to Google Cloud Speech-to-Text API")
EOF
```

## Usage

1. Start the app:
   ```bash
   ./run.sh
   ```

2. Enter YouTube URL
3. App will:
   - ✅ Download video using yt-dlp
   - ✅ Extract audio and convert to mono
   - ✅ Transcribe using Google Cloud Speech-to-Text
   - ✅ Analyze highlights using Google Gemini
   - ✅ Generate TTS using Google Cloud Text-to-Speech

## Language Support

### Speech-to-Text
- Indonesian: `id-ID` (default)
- English: `en-US`
- Other: Check [supported languages](https://cloud.google.com/speech-to-text/docs/languages)

### Text-to-Speech
- Indonesian: `id-ID` with voice `id-ID-Neural2-A` or `id-ID-Neural2-B`
- English: `en-US` with multiple voice options
- Other: Check [supported languages](https://cloud.google.com/text-to-speech/docs/voices)

## Support

For issues with Google Cloud APIs:
- Speech-to-Text: https://cloud.google.com/speech-to-text/docs
- Text-to-Speech: https://cloud.google.com/text-to-speech/docs
