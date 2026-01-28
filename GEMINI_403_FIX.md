# Gemini API 403 Forbidden Error - Fix Guide

## Problem
```
Failed to call Gemini API: 403 Client Error: Forbidden for url: 
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyBDoBdpOEHoaKm6JxZI_vXy_KbT9QNb54c
```

Error occurs at: **Step [2/4] Finding highlights**

## Root Causes (Check in order)

### 1. **Invalid or Expired API Key**
Your current API key: `AIzaSyBDoBdpOEHoaKm6JxZI_vXy_KbT9QNb54c`

**Fix:**
- Go to https://console.cloud.google.com/
- Check if API key is valid and not revoked
- Generate new API key if needed

### 2. **Generative AI API Not Enabled**

**Fix:**
- Go to https://console.cloud.google.com/
- Select your project
- Search for "Generative Language API"
- Click ENABLE if not already enabled

### 3. **API Key Restrictions**

**Fix:**
- Go to https://console.cloud.google.com/apis/credentials
- Find your API key: `AIzaSyBDoBdpOEHoaKm6JxZI_vXy_KbT9QNb54c`
- Click it to open details
- Check "API restrictions"
  - If restricted, add "Generative Language API" to allowed APIs
  - If unrestricted, leave as is

### 4. **Wrong API Key Type**

**Correct Configuration:**
- Use: **API Key** (not Service Account)
- Type: Public
- Restrictions: Can be unrestricted

### 5. **API Quota Exceeded**

**Fix:**
- Check quota usage in Google Cloud Console
- May need to wait for quota reset (usually monthly)
- Or upgrade to paid plan

## Step-by-Step Fix

### Step 1: Get New API Key
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API key in new Google Cloud project"
3. Copy the generated API key
4. Keep it safe - never share it

### Step 2: Update Configuration
Open Settings in YT Short Clipper:
1. Go to Settings Tab
2. Find "Google Gemini" section
3. Enter your new API key
4. Click Save

Or manually edit config.json:
```json
{
  "ai_providers": {
    "google": {
      "api_key": "YOUR_NEW_API_KEY_HERE",
      "model": "gemini-2.5-flash"
    }
  }
}
```

### Step 3: Test the Fix
1. Restart YT Short Clipper
2. Process a test video
3. Watch for step [2/4] to complete without error

## Verify API Key Works

**Quick Test in Terminal:**
```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Hello"}]
    }]
  }'
```

Expected response: Contains "candidates" array with text response
Error response: Contains "error" object with 403/401/429 codes

## Common Errors & Meanings

| Error | Meaning | Solution |
|-------|---------|----------|
| 403 Forbidden | API disabled or key invalid | Get new key, enable API |
| 401 Unauthorized | Wrong/expired key | Get new key |
| 429 Too Many Requests | Quota exceeded | Wait or upgrade plan |
| 400 Bad Request | Invalid request format | Check API docs |

## Troubleshooting Checklist

- [ ] API key is not expired
- [ ] Generative Language API is enabled in Google Cloud
- [ ] API key has no API restrictions OR Generative Language API is in allowed list
- [ ] API quota not exceeded
- [ ] Using correct API key (not OAuth token)
- [ ] Configuration saved correctly in Settings
- [ ] Application restarted after config change

## Prevention Tips

1. **Store API key securely** - Use environment variables or config files
2. **Monitor API usage** - Check quota regularly in Google Cloud Console
3. **Refresh key periodically** - Generate new keys every 3-6 months
4. **Use least privilege** - Restrict API key to Generative Language API only

## Still Not Working?

1. Check error.log in app directory for more details
2. Try with fresh Google account and new project
3. Ensure you have billing enabled (even free tier needs it)
4. Contact Google Cloud Support if API issue persists
