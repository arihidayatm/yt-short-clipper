#!/usr/bin/env python3
"""
Google Cloud Configuration Update Script
Automatically updates config.json to use Google Cloud APIs
"""

import json
import os
import sys
from pathlib import Path


def main():
    config_file = Path("config.json")
    credentials_file = Path("google-cloud-credentials.json")
    
    print("=" * 60)
    print("Google Cloud Configuration Update")
    print("=" * 60)
    
    # Check if config.json exists
    if not config_file.exists():
        print("\n✗ config.json not found in current directory")
        print("  Please run the application first to generate the config file")
        sys.exit(1)
    
    # Check if credentials file exists
    if not credentials_file.exists():
        print("\n✗ google-cloud-credentials.json not found")
        print("  Please place your Google Cloud credentials file in this directory")
        print("\n  Steps to get credentials:")
        print("  1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
        print("  2. Create a service account or select existing one")
        print("  3. Go to KEYS tab > ADD KEY > Create new key (JSON)")
        print("  4. Save the downloaded file as: google-cloud-credentials.json")
        sys.exit(1)
    
    # Load current config
    print("\n📖 Loading current configuration...")
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Get user input for which providers to update
    print("\n🔧 Which providers do you want to update?")
    print("   1. Caption Maker (Speech-to-Text)")
    print("   2. Hook Maker (Text-to-Speech)")
    print("   3. Both")
    
    choice = input("\nEnter choice (1-3) [default: 3]: ").strip() or "3"
    
    if choice not in ["1", "2", "3"]:
        print("✗ Invalid choice")
        sys.exit(1)
    
    # Update caption_maker (Speech-to-Text)
    if choice in ["1", "3"]:
        print("\n📝 Updating caption_maker (Speech-to-Text)...")
        config["ai_providers"]["caption_maker"] = {
            "provider": "google-cloud",
            "credentials_path": str(credentials_file),
            "model": "whisper-1"  # Keep for compatibility
        }
        print("   ✓ caption_maker will now use Google Cloud Speech-to-Text")
    
    # Update hook_maker (Text-to-Speech)
    if choice in ["2", "3"]:
        print("\n🔊 Updating hook_maker (Text-to-Speech)...")
        config["ai_providers"]["hook_maker"] = {
            "provider": "google-cloud",
            "credentials_path": str(credentials_file),
            "model": "tts-1"  # Keep for compatibility
        }
        print("   ✓ hook_maker will now use Google Cloud Text-to-Speech")
    
    # Save updated config
    print("\n💾 Saving updated configuration...")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Display summary
    print("\n" + "=" * 60)
    print("✓ Configuration Updated Successfully!")
    print("=" * 60)
    
    print("\n📋 Summary of changes:")
    print("-" * 60)
    
    if choice in ["1", "3"]:
        print("✓ caption_maker:")
        print(f"  Provider: {config['ai_providers']['caption_maker']['provider']}")
        print(f"  Credentials: {config['ai_providers']['caption_maker']['credentials_path']}")
    
    if choice in ["2", "3"]:
        print("✓ hook_maker:")
        print(f"  Provider: {config['ai_providers']['hook_maker']['provider']}")
        print(f"  Credentials: {config['ai_providers']['hook_maker']['credentials_path']}")
    
    print("\n" + "-" * 60)
    print("\n🚀 Next steps:")
    print("   1. Run the application: ./run.sh")
    print("   2. Enter a YouTube URL")
    print("   3. The app will use Google Cloud APIs for:")
    if choice in ["1", "3"]:
        print("      - Audio transcription (Speech-to-Text)")
    if choice in ["2", "3"]:
        print("      - Audio generation (Text-to-Speech)")
    
    print("\n📚 For more information:")
    print("   • See: GOOGLE_CLOUD_SETUP.md")
    print("   • Docs: https://cloud.google.com/docs")
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
"""
Google Cloud Configuration Update Script
Automatically updates config.json to use Google Cloud APIs
"""

import json
import os
import sys
from pathlib import Path


def main():
    config_file = Path("config.json")
    credentials_file = Path("google-cloud-credentials.json")
    
    print("=" * 60)
    print("Google Cloud Configuration Update")
    print("=" * 60)
    
    # Check if config.json exists
    if not config_file.exists():
        print("\n✗ config.json not found in current directory")
        print("  Please run the application first to generate the config file")
        sys.exit(1)
    
    # Check if credentials file exists
    if not credentials_file.exists():
        print("\n✗ google-cloud-credentials.json not found")
        print("  Please place your Google Cloud credentials file in this directory")
        print("\n  Steps to get credentials:")
        print("  1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
        print("  2. Create a service account or select existing one")
        print("  3. Go to KEYS tab > ADD KEY > Create new key (JSON)")
        print("  4. Save the downloaded file as: google-cloud-credentials.json")
        sys.exit(1)
    
    # Load current config
    print("\n📖 Loading current configuration...")
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Get user input for which providers to update
    print("\n🔧 Which providers do you want to update?")
    print("   1. Caption Maker (Speech-to-Text)")
    print("   2. Hook Maker (Text-to-Speech)")
    print("   3. Both")
    
    choice = input("\nEnter choice (1-3) [default: 3]: ").strip() or "3"
    
    if choice not in ["1", "2", "3"]:
        print("✗ Invalid choice")
        sys.exit(1)
    
    # Update caption_maker (Speech-to-Text)
    if choice in ["1", "3"]:
        print("\n📝 Updating caption_maker (Speech-to-Text)...")
        config["ai_providers"]["caption_maker"] = {
            "provider": "google-cloud",
            "credentials_path": str(credentials_file),
            "model": "whisper-1"  # Keep for compatibility
        }
        print("   ✓ caption_maker will now use Google Cloud Speech-to-Text")
    
    # Update hook_maker (Text-to-Speech)
    if choice in ["2", "3"]:
        print("\n🔊 Updating hook_maker (Text-to-Speech)...")
        config["ai_providers"]["hook_maker"] = {
            "provider": "google-cloud",
            "credentials_path": str(credentials_file),
            "model": "tts-1"  # Keep for compatibility
        }
        print("   ✓ hook_maker will now use Google Cloud Text-to-Speech")
    
    # Save updated config
    print("\n💾 Saving updated configuration...")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Display summary
    print("\n" + "=" * 60)
    print("✓ Configuration Updated Successfully!")
    print("=" * 60)
    
    print("\n📋 Summary of changes:")
    print("-" * 60)
    
    if choice in ["1", "3"]:
        print("✓ caption_maker:")
        print(f"  Provider: {config['ai_providers']['caption_maker']['provider']}")
        print(f"  Credentials: {config['ai_providers']['caption_maker']['credentials_path']}")
    
    if choice in ["2", "3"]:
        print("✓ hook_maker:")
        print(f"  Provider: {config['ai_providers']['hook_maker']['provider']}")
        print(f"  Credentials: {config['ai_providers']['hook_maker']['credentials_path']}")
    
    print("\n" + "-" * 60)
    print("\n🚀 Next steps:")
    print("   1. Run the application: ./run.sh")
    print("   2. Enter a YouTube URL")
    print("   3. The app will use Google Cloud APIs for:")
    if choice in ["1", "3"]:
        print("      - Audio transcription (Speech-to-Text)")
    if choice in ["2", "3"]:
        print("      - Audio generation (Text-to-Speech)")
    
    print("\n📚 For more information:")
    print("   • See: GOOGLE_CLOUD_SETUP.md")
    print("   • Docs: https://cloud.google.com/docs")
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
