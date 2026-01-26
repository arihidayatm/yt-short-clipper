"""
Status pages for API and Library checking
"""

import threading
import subprocess
import customtkinter as ctk
from tkinter import messagebox

from utils.helpers import get_ffmpeg_path, get_ytdlp_path


class APIStatusPage(ctk.CTkFrame):
    """API Status page - check OpenAI and YouTube API status"""
    
    def __init__(self, parent, get_client_callback, get_config_callback, get_youtube_status_callback, on_back_callback, refresh_icon=None):
        super().__init__(parent)
        self.get_client = get_client_callback
        self.get_config = get_config_callback
        self.get_youtube_status = get_youtube_status_callback
        self.on_back = on_back_callback
        self.refresh_icon = refresh_icon
        
        self.create_ui()
    
    def create_ui(self):
        """Create the API status page UI"""
        # Import header and footer components
        from components.page_layout import PageHeader, PageFooter
        
        # Set background color to match home page
        self.configure(fg_color=("#1a1a1a", "#0a0a0a"))
        
        # Header with back button
        header = PageHeader(self, self, show_nav_buttons=False, show_back_button=True, page_title="API Status")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        # Main content
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Status summary card
        summary_frame = ctk.CTkFrame(main, fg_color=("gray88", "gray18"), corner_radius=12)
        summary_frame.pack(fill="x", pady=(0, 15))
        
        summary_content = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_content.pack(fill="x", padx=15, pady=12)
        
        summary_title = ctk.CTkLabel(summary_content, text="System Status Overview", 
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        summary_title.pack(fill="x", pady=(0, 8))
        
        # Status indicators row
        indicators_frame = ctk.CTkFrame(summary_content, fg_color="transparent")
        indicators_frame.pack(fill="x")
        
        self.summary_status_label = ctk.CTkLabel(indicators_frame, text="Scanning...", 
            font=ctk.CTkFont(size=12), text_color="gray")
        self.summary_status_label.pack(side="left", fill="x", expand=True)
        
        # AI API Status (parent card)
        ai_frame = ctk.CTkFrame(main, fg_color=("gray90", "gray17"), corner_radius=12)
        ai_frame.pack(fill="x", pady=(0, 15))
        
        ai_header = ctk.CTkFrame(ai_frame, fg_color="transparent")
        ai_header.pack(fill="x", padx=15, pady=(15, 5))
        
        ai_title_frame = ctk.CTkFrame(ai_header, fg_color="transparent")
        ai_title_frame.pack(side="left")
        
        ctk.CTkLabel(ai_title_frame, text="🤖", font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(ai_title_frame, text="AI API Services", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        # Sub-providers with better spacing
        providers_frame = ctk.CTkFrame(ai_frame, fg_color="transparent")
        providers_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        # Highlight Finder
        self._create_provider_card(providers_frame, "🎯", "Highlight Finder", 
            "Finds engaging segments using AI analysis", "hf")
        
        # Caption Maker
        self._create_provider_card(providers_frame, "📝", "Caption Maker", 
            "Generates captions for video segments", "cm")
        
        # Hook Maker
        self._create_provider_card(providers_frame, "🎤", "Hook Maker", 
            "Creates engaging audio hooks", "hm")
        
        # YouTube Title Maker
        self._create_provider_card(providers_frame, "📺", "YouTube Title Maker", 
            "Generates optimized YouTube titles", "yt_maker")
        
        # YouTube API Status
        yt_frame = ctk.CTkFrame(main, fg_color=("gray90", "gray17"), corner_radius=12)
        yt_frame.pack(fill="x", pady=(0, 15))
        
        yt_header = ctk.CTkFrame(yt_frame, fg_color="transparent")
        yt_header.pack(fill="x", padx=15, pady=(15, 10))
        
        yt_title_frame = ctk.CTkFrame(yt_header, fg_color="transparent")
        yt_title_frame.pack(side="left")
        
        ctk.CTkLabel(yt_title_frame, text="📱", font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(yt_title_frame, text="YouTube API", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        self.yt_status_badge = ctk.CTkLabel(yt_header, text="Checking...", 
            font=ctk.CTkFont(size=11, weight="bold"), text_color="gray", 
            bg_color=("gray80", "gray30"), fg_color=("gray80", "gray30"), 
            corner_radius=6)
        self.yt_status_badge.pack(side="right", padx=8, pady=0)
        
        self.yt_info_label = ctk.CTkLabel(yt_frame, text="", font=ctk.CTkFont(size=11), 
            text_color="gray", anchor="w")
        self.yt_info_label.pack(fill="x", padx=15, pady=(0, 15))
        
        # Action buttons frame
        actions_frame = ctk.CTkFrame(main, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(15, 0))
        
        # Refresh button with better styling
        ctk.CTkButton(actions_frame, text="🔄 Refresh All Status", image=self.refresh_icon, 
            compound="left", height=45, font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#36719F", "#144870"),
            corner_radius=10,
            command=self.refresh_status).pack(fill="x", pady=(0, 5))
        
        # Help text
        help_text = ctk.CTkLabel(actions_frame, 
            text="💡 Tip: If you see errors, check your API keys in Settings. All services must be configured for the application to work properly.",
            font=ctk.CTkFont(size=10), text_color="gray", anchor="w", wraplength=500)
        help_text.pack(fill="x", pady=(5, 0))
        
        # Footer
        footer = PageFooter(self, self)
        footer.pack(fill="x", padx=20, pady=(15, 0), side="bottom")
    
    def _create_provider_card(self, parent, emoji, name, description, provider_key):
        """Create a provider status card"""
        card_frame = ctk.CTkFrame(parent, fg_color=("gray85", "gray20"), corner_radius=10)
        card_frame.pack(fill="x", pady=(0, 10))
        
        # Header with emoji and title
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10, 0))
        
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True)
        
        ctk.CTkLabel(title_frame, text=emoji, font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_frame, text=name, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(side="left")
        
        # Status badge
        status_label = ctk.CTkLabel(header_frame, text="Checking...", 
            font=ctk.CTkFont(size=10, weight="bold"), text_color="gray",
            bg_color=("gray75", "gray35"), fg_color=("gray75", "gray35"),
            corner_radius=5, padx=8, pady=2)
        status_label.pack(side="right", padx=0, pady=0)
        
        # Description
        ctk.CTkLabel(card_frame, text=description, font=ctk.CTkFont(size=10), 
            text_color="gray", anchor="w").pack(fill="x", padx=12, pady=(5, 0))
        
        # Info label
        info_label = ctk.CTkLabel(card_frame, text="", font=ctk.CTkFont(size=10), 
            text_color="gray", anchor="w")
        info_label.pack(fill="x", padx=12, pady=(3, 10))
        
        # Store references
        if provider_key == "hf":
            self.hf_status_label = status_label
            self.hf_info_label = info_label
        elif provider_key == "cm":
            self.cm_status_label = status_label
            self.cm_info_label = info_label
        elif provider_key == "hm":
            self.hm_status_label = status_label
            self.hm_info_label = info_label
        elif provider_key == "yt_maker":
            self.yt_maker_status_label = status_label
            self.yt_maker_info_label = info_label
    
    def update_status(self, youtube_connected, youtube_channel):
        """Update YouTube connection status (deprecated - now uses callback)"""
        pass
    
    def refresh_status(self):
        """Refresh API status"""
        # Reset to checking state
        self.hf_status_label.configure(text="⏳ Checking...", text_color="gray", bg_color=("gray75", "gray35"))
        self.hf_info_label.configure(text="")
        self.cm_status_label.configure(text="⏳ Checking...", text_color="gray", bg_color=("gray75", "gray35"))
        self.cm_info_label.configure(text="")
        self.hm_status_label.configure(text="⏳ Checking...", text_color="gray", bg_color=("gray75", "gray35"))
        self.hm_info_label.configure(text="")
        self.yt_maker_status_label.configure(text="⏳ Checking...", text_color="gray", bg_color=("gray75", "gray35"))
        self.yt_maker_info_label.configure(text="")
        self.yt_status_badge.configure(text="⏳ Checking...", text_color="gray", bg_color=("gray80", "gray30"))
        self.yt_info_label.configure(text="")
        self.summary_status_label.configure(text="Checking all services...")
        
        def check_status():
            from openai import OpenAI
            
            # Get config
            config = self.get_config()
            ai_providers = config.get("ai_providers", {})
            
            # Check each AI provider
            providers_to_check = [
                ("highlight_finder", "🎯 Highlight Finder", self.hf_status_label, self.hf_info_label, "chat"),
                ("caption_maker", "📝 Caption Maker", self.cm_status_label, self.cm_info_label, "whisper"),
                ("hook_maker", "🎤 Hook Maker", self.hm_status_label, self.hm_info_label, "tts"),
                ("youtube_title_maker", "📺 YouTube Title Maker", self.yt_maker_status_label, self.yt_maker_info_label, "chat")
            ]
            
            for provider_key, provider_name, status_label, info_label, provider_type in providers_to_check:
                provider_config = ai_providers.get(provider_key, {})
                api_key = provider_config.get("api_key", "")
                base_url = provider_config.get("base_url", "https://api.openai.com/v1")
                model = provider_config.get("model", "N/A")
                
                if not api_key:
                    self.after(0, lambda sl=status_label, il=info_label: (
                        sl.configure(text="⚙️ Not configured", text_color="gray", bg_color=("gray75", "gray35")),
                        il.configure(text="Configure API key in Settings")
                    ))
                    continue
                
                try:
                    client = OpenAI(api_key=api_key, base_url=base_url)
                    
                    # Try to list models to verify API key and model availability
                    try:
                        models_response = client.models.list()
                        available_models = [m.id for m in models_response.data]
                        
                        # Check if configured model is available
                        if model in available_models:
                            self.after(0, lambda sl=status_label, il=info_label, m=model: (
                                sl.configure(text="✓ Connected", text_color="white", bg_color=("green", "#2E7D32")),
                                il.configure(text=f"Model: {m}")
                            ))
                        else:
                            self.after(0, lambda sl=status_label, il=info_label, m=model: (
                                sl.configure(text="⚠️ Model not found", text_color="white", bg_color=("orange", "#F57C00")),
                                il.configure(text=f"Model '{m}' not available")
                            ))
                    except Exception as list_error:
                        # Check if it's a connection/authentication error
                        error_str = str(list_error).lower()
                        if any(x in error_str for x in ['connection', 'timeout', 'unreachable', 'invalid', 'unauthorized', 'authentication', 'api key', 'not found', '404', '401', '403', '500', '502', '503', 'error code']):
                            # Real error - connection or auth failed
                            raise list_error
                        else:
                            # Provider might not support models.list(), show configured status
                            self.after(0, lambda sl=status_label, il=info_label, m=model: (
                                sl.configure(text="✓ Configured", text_color="white", bg_color=("green", "#2E7D32")),
                                il.configure(text=f"Model: {m}")
                            ))
                    
                except Exception as e:
                    error_msg = str(e)[:60]
                    self.after(0, lambda sl=status_label, il=info_label, err=error_msg: (
                        sl.configure(text="✗ Error", text_color="white", bg_color=("red", "#C62828")),
                        il.configure(text=f"Error: {err}")
                    ))
            
            # Check YouTube status
            youtube_connected, youtube_channel = self.get_youtube_status()
            
            if youtube_connected and youtube_channel:
                self.after(0, lambda: self.yt_status_badge.configure(text="✓ Connected", text_color="white", bg_color=("green", "#2E7D32")))
                self.after(0, lambda: self.yt_info_label.configure(text=f"Channel: {youtube_channel['title']}"))
            else:
                try:
                    from youtube_uploader import YouTubeUploader
                    uploader = YouTubeUploader()
                    if not uploader.is_configured():
                        self.after(0, lambda: self.yt_status_badge.configure(text="⚙️ Not configured", text_color="gray", bg_color=("gray80", "gray30")))
                        self.after(0, lambda: self.yt_info_label.configure(text="client_secret.json not found"))
                    else:
                        self.after(0, lambda: self.yt_status_badge.configure(text="⚠️ Not connected", text_color="white", bg_color=("orange", "#F57C00")))
                        self.after(0, lambda: self.yt_info_label.configure(text="Connect your channel in Settings"))
                except Exception as e:
                    self.after(0, lambda: self.yt_status_badge.configure(text="✗ Error", text_color="white", bg_color=("red", "#C62828")))
                    self.after(0, lambda: self.yt_info_label.configure(text=f"Error: {str(e)[:60]}"))
        
        threading.Thread(target=check_status, daemon=True).start()
    
    def open_github(self):
        """Open GitHub repository"""
        import webbrowser
        webbrowser.open("https://github.com/jipraks/yt-short-clipper")
    
    def open_discord(self):
        """Open Discord server invite link"""
        import webbrowser
        webbrowser.open("https://s.id/ytsdiscord")
    
    def show_page(self, page_name):
        """Delegate to parent app's show_page method"""
        try:
            parent = self.master
            while parent and not hasattr(parent, 'show_page'):
                parent = parent.master
            if parent and hasattr(parent, 'show_page'):
                parent.show_page(page_name)
        except:
            pass


class LibStatusPage(ctk.CTkFrame):
    """Library Status page - check FFmpeg and yt-dlp"""
    
    def __init__(self, parent, on_back_callback, refresh_icon=None):
        super().__init__(parent)
        self.on_back = on_back_callback
        self.refresh_icon = refresh_icon
        
        self.create_ui()
    
    def create_ui(self):
        """Create the library status page UI"""
        # Import header and footer components
        from components.page_layout import PageHeader, PageFooter
        
        # Set background color to match home page
        self.configure(fg_color=("#1a1a1a", "#0a0a0a"))
        
        # Header with back button
        header = PageHeader(self, self, show_nav_buttons=False, show_back_button=True, page_title="Library Status")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        # Main content
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # yt-dlp Status
        ytdlp_frame = ctk.CTkFrame(main, fg_color=("gray90", "gray17"))
        ytdlp_frame.pack(fill="x", pady=(15, 10))
        
        ytdlp_header = ctk.CTkFrame(ytdlp_frame, fg_color="transparent")
        ytdlp_header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(ytdlp_header, text="yt-dlp", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        self.ytdlp_status_label = ctk.CTkLabel(ytdlp_header, text="Checking...", font=ctk.CTkFont(size=13), text_color="gray")
        self.ytdlp_status_label.pack(side="right")
        
        self.ytdlp_info_label = ctk.CTkLabel(ytdlp_frame, text="", font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        self.ytdlp_info_label.pack(fill="x", padx=15, pady=(0, 15))
        
        # FFmpeg Status
        ffmpeg_frame = ctk.CTkFrame(main, fg_color=("gray90", "gray17"))
        ffmpeg_frame.pack(fill="x", pady=(0, 10))
        
        ffmpeg_header = ctk.CTkFrame(ffmpeg_frame, fg_color="transparent")
        ffmpeg_header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(ffmpeg_header, text="FFmpeg", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        self.ffmpeg_status_label = ctk.CTkLabel(ffmpeg_header, text="Checking...", font=ctk.CTkFont(size=13), text_color="gray")
        self.ffmpeg_status_label.pack(side="right")
        
        self.ffmpeg_info_label = ctk.CTkLabel(ffmpeg_frame, text="", font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        self.ffmpeg_info_label.pack(fill="x", padx=15, pady=(0, 15))
        
        # Refresh button
        ctk.CTkButton(main, text="Check Libraries", image=self.refresh_icon, compound="left",
            height=45, command=self.refresh_status).pack(fill="x", pady=(10, 0))
        
        # Footer
        footer = PageFooter(self, self)
        footer.pack(fill="x", padx=20, pady=(0, 15), side="bottom")
    
    def refresh_status(self):
        """Refresh library status"""
        # Reset to checking state
        self.ytdlp_status_label.configure(text="Checking...", text_color="gray")
        self.ytdlp_info_label.configure(text="")
        self.ffmpeg_status_label.configure(text="Checking...", text_color="gray")
        self.ffmpeg_info_label.configure(text="")
        
        def check_libs():
            # Check yt-dlp
            ytdlp_path = get_ytdlp_path()
            try:
                result = subprocess.run([ytdlp_path, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.after(0, lambda: self.ytdlp_status_label.configure(text="✓ Installed", text_color="green"))
                    self.after(0, lambda: self.ytdlp_info_label.configure(text=f"Version: {version}"))
                else:
                    self.after(0, lambda: self.ytdlp_status_label.configure(text="✗ Error", text_color="red"))
                    self.after(0, lambda: self.ytdlp_info_label.configure(text="Failed to get version"))
            except FileNotFoundError:
                self.after(0, lambda: self.ytdlp_status_label.configure(text="✗ Not found", text_color="red"))
                self.after(0, lambda: self.ytdlp_info_label.configure(text="yt-dlp not installed or not in PATH"))
            except Exception as e:
                self.after(0, lambda: self.ytdlp_status_label.configure(text="✗ Error", text_color="red"))
                self.after(0, lambda: self.ytdlp_info_label.configure(text=f"Error: {str(e)[:50]}"))
            
            # Check FFmpeg
            ffmpeg_path = get_ffmpeg_path()
            try:
                result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Extract version from first line
                    version_line = result.stdout.split('\n')[0]
                    version = version_line.split('version')[1].split()[0] if 'version' in version_line else "Unknown"
                    self.after(0, lambda: self.ffmpeg_status_label.configure(text="✓ Installed", text_color="green"))
                    self.after(0, lambda: self.ffmpeg_info_label.configure(text=f"Version: {version}"))
                else:
                    self.after(0, lambda: self.ffmpeg_status_label.configure(text="✗ Error", text_color="red"))
                    self.after(0, lambda: self.ffmpeg_info_label.configure(text="Failed to get version"))
            except FileNotFoundError:
                self.after(0, lambda: self.ffmpeg_status_label.configure(text="✗ Not found", text_color="red"))
                self.after(0, lambda: self.ffmpeg_info_label.configure(text="FFmpeg not installed or not in PATH"))
            except Exception as e:
                self.after(0, lambda: self.ffmpeg_status_label.configure(text="✗ Error", text_color="red"))
                self.after(0, lambda: self.ffmpeg_info_label.configure(text=f"Error: {str(e)[:50]}"))
        
        threading.Thread(target=check_libs, daemon=True).start()
    
    def open_github(self):
        """Open GitHub repository"""
        import webbrowser
        webbrowser.open("https://github.com/jipraks/yt-short-clipper")
    
    def open_discord(self):
        """Open Discord server invite link"""
        import webbrowser
        webbrowser.open("https://s.id/ytsdiscord")
    
    def show_page(self, page_name):
        """Delegate to parent app's show_page method"""
        try:
            parent = self.master
            while parent and not hasattr(parent, 'show_page'):
                parent = parent.master
            if parent and hasattr(parent, 'show_page'):
                parent.show_page(page_name)
        except:
            pass
