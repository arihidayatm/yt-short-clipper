# Google Cloud APIs Integration - Complete Summary

## ✅ What's Been Completed

Your YT Short Clipper application is now fully configured to use **Google Cloud APIs** for Speech-to-Text and Text-to-Speech, replacing OpenAI's services.

### 1. **Code Updates** ✓

#### Updated Files:
- **`clipper_core.py`**: Modified to detect provider type for caption_maker and hook_maker, with fallback logic to use Google Cloud when configured
- **`utils/ai_providers.py`**: Enhanced factory function to support google-cloud provider with service_type parameter
- **`config/config_manager.py`**: Added credentials_path field to default AI provider configuration
- **`utils/google_cloud_adapters.py`**: Complete implementation of Google Cloud adapters with OpenAI-compatible interface

#### New Files:
- **`update_google_cloud_config.py`**: Interactive configuration script to update config.json for Google Cloud providers

### 2. **Libraries Installed** ✓

```
✓ google-cloud-speech>=2.36.0
✓ google-cloud-texttospeech>=2.34.0
✓ google-auth (and supporting libraries)
```

All dependencies installed successfully in your virtual environment.

### 3. **Application Architecture** ✓

The application now supports multiple AI providers:

```
┌─────────────────────────────────────────────────────────────┐
│                    YT Short Clipper                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  highlight_finder (Google Gemini ✓)                         │
│        ↓                                                      │
│  caption_maker (OpenAI or Google Cloud)                      │
│        ↓                                                      │
│  hook_maker (OpenAI or Google Cloud)                         │
│        ↓                                                      │
│  youtube_title_maker (OpenAI)                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Next Steps (What You Need To Do)

### Step 1: Get Google Cloud Credentials

You need to download a **service account JSON file** from Google Cloud. Here's how:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. If you don't have a service account yet:
   - Click "CREATE SERVICE ACCOUNT"
   - Name: `yt-short-clipper-svc`
   - Click "CREATE AND CONTINUE"
3. Grant these roles to the service account:
   - ✓ Cloud Speech-to-Text API User
   - ✓ Cloud Text-to-Speech API User
4. Go to the "KEYS" tab
5. Click "ADD KEY" → "Create new key"
6. Select "JSON"
7. Click "CREATE"
8. A JSON file will download automatically

### Step 2: Place Credentials File

Save the downloaded JSON file in your project directory as `google-cloud-credentials.json`:

```bash
# From the downloads folder
mv ~/Downloads/yt-short-clipper-svc-*.json ~/yt-short-clipper/google-cloud-credentials.json

# Verify it exists
ls ~/yt-short-clipper/google-cloud-credentials.json
```

### Step 3: Update Application Configuration

Run the interactive configuration script:

```bash
cd ~/yt-short-clipper
./venv/bin/python3 update_google_cloud_config.py
```

This will:
- Verify your credentials file exists
- Ask which providers to update (caption_maker, hook_maker, or both)
- Update your config.json automatically
- Show a summary of changes

### Step 4: Test the Application

```bash
cd ~/yt-short-clipper
./run.sh
```

1. Enter a YouTube URL
2. The app will process video using:
   - Google Gemini for highlight detection
   - Google Cloud STT for transcription
   - Google Cloud TTS for audio generation

## 📊 Cost Information

### Speech-to-Text
- **Free tier**: 60 minutes/month
- **Paid**: $0.024 per 15 seconds (~$0.096/minute)
- Example: 30-min video = ~$2.88

### Text-to-Speech
- **Free tier**: 1 million characters/month  
- **Paid**: $0.016 per 1,000 characters
- Example: 100KB text = ~$1.60

**Total for 1 video**: ~$4-5 (mostly speech-to-text)

## 🔧 Configuration Files

### Current Config Structure

Your `config.json` will look like this after setup:

```json
{
  "ai_providers": {
    "highlight_finder": {
      "provider": "google",
      "model": "gemini-2.5-flash",
      "api_key": "AIzaSy..."
    },
    "caption_maker": {
      "provider": "google-cloud",
      "credentials_path": "google-cloud-credentials.json"
    },
    "hook_maker": {
      "provider": "google-cloud",
      "credentials_path": "google-cloud-credentials.json"
    },
    "youtube_title_maker": {
      "provider": "openai",
      "api_key": "sk-..."
    }
  }
}
```

## ❌ Troubleshooting

### Error: "google-cloud-credentials.json not found"
**Solution**: Make sure the JSON file is in the correct location:
```bash
ls -la ~/yt-short-clipper/google-cloud-credentials.json
```

### Error: "Permission denied" / "Not authorized"
**Solution**: Check that your service account has the required roles:
1. Go to: https://console.cloud.google.com/iam-admin/iam
2. Find your service account in the list
3. Edit it and add these roles:
   - Cloud Speech-to-Text API User
   - Cloud Text-to-Speech API User
4. Wait 1-2 minutes for permissions to propagate

### Error: "API is not enabled"
**Solution**: Enable the required APIs:
1. Go to: https://console.cloud.google.com/apis/library
2. Search for and enable:
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API

### Error: "Quota exceeded"
**Solution**: Check your usage and request increase if needed:
1. Go to: https://console.cloud.google.com/iam-admin/quotas
2. Review current usage
3. Request quota increase if needed

## 📚 Supported Languages

### Speech-to-Text
- English (US): en-US
- Indonesian: id-ID
- [Full list of 200+ languages](https://cloud.google.com/speech-to-text/docs/languages)

### Text-to-Speech
- English: en-US-Neural2-A through en-US-Neural2-H (8 voices)
- Indonesian: id-ID-Neural2-A, id-ID-Neural2-B, id-ID-Neural2-C (3 voices)
- [Full list of 600+ voices](https://cloud.google.com/text-to-speech/docs/voices)

## 🔄 How It All Works Together

When you run the application with a YouTube URL:

```
1. Download video
   ↓ (yt-dlp)
2. Extract audio from video
   ↓ (ffmpeg)
3. Transcribe audio to text
   ↓ (Google Cloud Speech-to-Text)
4. Find interesting highlights
   ↓ (Google Gemini)
5. Generate hook text
   ↓ (LLM - Google Gemini or OpenAI)
6. Generate hook audio
   ↓ (Google Cloud Text-to-Speech)
7. Combine clips with audio
   ↓ (ffmpeg)
8. Upload to social media
   ↓ (YouTube, TikTok)
```

## 🛡️ Security Notes

⚠️ **Important**: Your `google-cloud-credentials.json` contains sensitive credentials!

1. **Never commit to git**: Add to `.gitignore`
   ```bash
   echo "google-cloud-credentials.json" >> .gitignore
   ```

2. **Never share**: Keep the credentials file private

3. **Rotate periodically**: 
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Create new key if compromised
   - Delete old key

4. **Limit permissions**: Service account only has speech/TTS permissions

## 📖 Additional Resources

- [Google Cloud Speech-to-Text Docs](https://cloud.google.com/speech-to-text/docs)
- [Google Cloud Text-to-Speech Docs](https://cloud.google.com/text-to-speech/docs)
- [Service Account Authentication](https://cloud.google.com/docs/authentication/getting-started)
- [Complete Setup Guide](./GOOGLE_CLOUD_SETUP.md)

## ✨ What's Different From OpenAI?

| Feature | OpenAI | Google Cloud |
|---------|--------|--------------|
| Speech-to-Text | Whisper | Cloud Speech-to-Text |
| Text-to-Speech | TTS | Cloud Text-to-Speech |
| Free Tier | 3 months trial | 60 min/month STT, 1M chars/month TTS |
| Cost Model | Per-request | Per-minute/character |
| Languages | 99 languages | 200+ for STT, 600+ voices for TTS |
| Accuracy | Very good | Very good |

---

## 🎯 Ready to Go!

Once you complete the 4 steps above, your application will be fully set up to use Google Cloud APIs!

**Questions?** Check:
1. `./GOOGLE_CLOUD_SETUP.md` - Detailed setup guide
2. `./update_google_cloud_config.py --help` - Config script help
3. Console logs during application run
