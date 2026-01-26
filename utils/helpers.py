"""
Helper utility functions for YT Short Clipper
"""

import sys
import re
import os
import shutil
from pathlib import Path


def get_app_dir():
    """Get application directory"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def get_bundle_dir():
    """Get bundled resources directory"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else get_app_dir()
    return get_app_dir()


def get_ffmpeg_path():
    """Get FFmpeg executable path, handling virtual environments"""
    if getattr(sys, 'frozen', False):
        # For bundled executables
        bundled = get_app_dir() / "ffmpeg" / "ffmpeg.exe"
        if bundled.exists():
            return str(bundled)
    
    # Try to find ffmpeg in PATH
    found = shutil.which("ffmpeg")
    if found:
        return found
    
    # Try with .exe on Windows
    if sys.platform == "win32":
        found = shutil.which("ffmpeg.exe")
        if found:
            return found
    
    # Fallback to default
    return "ffmpeg"


def get_ytdlp_path():
    """Get yt-dlp executable path, handling virtual environments"""
    if getattr(sys, 'frozen', False):
        # For bundled executables
        bundled = get_app_dir() / "yt-dlp.exe"
        if bundled.exists():
            return str(bundled)
    
    # Try to find yt-dlp in PATH
    found = shutil.which("yt-dlp")
    if found:
        return found
    
    # Try with .exe on Windows
    if sys.platform == "win32":
        found = shutil.which("yt-dlp.exe")
        if found:
            return found
    
    # Try in the current Python's scripts directory (for virtual environments)
    scripts_dir = os.path.dirname(sys.executable)
    yt_dlp_path = os.path.join(scripts_dir, "yt-dlp")
    if os.path.exists(yt_dlp_path):
        return yt_dlp_path
    
    # Also try with .exe extension on Windows
    if sys.platform == "win32":
        yt_dlp_exe = os.path.join(scripts_dir, "yt-dlp.exe")
        if os.path.exists(yt_dlp_exe):
            return yt_dlp_exe
    
    # Fallback to default
    return "yt-dlp"


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
