"""
Google Cloud Speech-to-Text and Text-to-Speech adapters
"""

import json
from typing import Optional, List, Dict, Any
from pathlib import Path


class GoogleCloudSpeechToTextAdapter:
    """Adapter for Google Cloud Speech-to-Text API"""
    
    def __init__(self, credentials_path: str):
        """
        Initialize Google Cloud Speech-to-Text adapter
        
        Args:
            credentials_path: Path to Google Cloud service account JSON key
        """
        try:
            from google.cloud import speech
            from google.oauth2 import service_account
        except ImportError:
            raise ImportError("Please install: pip install google-cloud-speech")
        
        self.credentials_path = credentials_path
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = speech.SpeechClient(credentials=credentials)
    
    def transcribe(self, audio_file_path: str, language_code: str = "id-ID") -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file (WAV, MP3, OGG, FLAC)
            language_code: Language code (default: Indonesian)
        
        Returns:
            Transcribed text
        """
        from google.cloud import speech
        
        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        
        response = self.client.recognize(config=config, audio=audio)
        
        transcript = ""
        for result in response.results:
            if result.alternatives:
                transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()


class GoogleCloudTextToSpeechAdapter:
    """Adapter for Google Cloud Text-to-Speech API"""
    
    def __init__(self, credentials_path: str):
        """
        Initialize Google Cloud Text-to-Speech adapter
        
        Args:
            credentials_path: Path to Google Cloud service account JSON key
        """
        try:
            from google.cloud import texttospeech
            from google.oauth2 import service_account
        except ImportError:
            raise ImportError("Please install: pip install google-cloud-texttospeech")
        
        self.credentials_path = credentials_path
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    def synthesize(self, text: str, output_file: str, language_code: str = "id-ID", 
                   voice_name: str = "id-ID-Neural2-A") -> str:
        """
        Synthesize text to speech
        
        Args:
            text: Text to synthesize
            output_file: Output audio file path (MP3)
            language_code: Language code (default: Indonesian)
            voice_name: Voice name (default: Indonesian female neural voice)
        
        Returns:
            Path to output file
        """
        from google.cloud import texttospeech
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        
        # Write audio to file
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        return output_file


class GoogleCloudWhisperAdapter:
    """
    Adapter that mimics OpenAI Whisper interface using Google Cloud Speech-to-Text
    """
    
    def __init__(self, credentials_path: str):
        self.speech_client = GoogleCloudSpeechToTextAdapter(credentials_path)
    
    def transcriptions(self):
        """Return object with create method to mimic OpenAI interface"""
        return GoogleCloudTranscriptionsAPI(self.speech_client)


class GoogleCloudTranscriptionsAPI:
    """Mimic OpenAI transcriptions.create() interface"""
    
    def __init__(self, speech_client):
        self.speech_client = speech_client
    
    def create(self, file: Any = None, model: str = "whisper-1", **kwargs) -> Any:
        """
        Create transcription using Google Cloud Speech-to-Text
        
        Args:
            file: File object or file path
            model: Model name (ignored, for compatibility)
            **kwargs: Additional parameters
        
        Returns:
            Response object with .text property
        """
        # Handle file parameter
        if hasattr(file, 'read'):
            # File-like object
            file_path = file.name if hasattr(file, 'name') else "temp_audio.wav"
        else:
            # String file path
            file_path = str(file)
        
        # Get language from kwargs
        language_code = kwargs.get("language", "id-ID")
        
        # Transcribe
        text = self.speech_client.transcribe(file_path, language_code)
        
        # Return object mimicking OpenAI response
        return GoogleCloudTranscriptionResponse(text)


class GoogleCloudTranscriptionResponse:
    """Response object that mimics OpenAI transcription response"""
    
    def __init__(self, text: str):
        self.text = text
        # Add usage tracking (mimics OpenAI usage format)
        self.usage = GoogleCloudUsage(
            prompt_tokens=len(text.split()),
            completion_tokens=len(text.split()),
            total_tokens=len(text.split()) * 2
        )


class GoogleCloudUsage:
    """Usage statistics that mimics OpenAI usage object"""
    
    def __init__(self, prompt_tokens: int, completion_tokens: int, total_tokens: int):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


class GoogleCloudTextToSpeechAPI:
    """Mimic OpenAI TTS interface using Google Cloud Text-to-Speech"""
    
    def __init__(self, credentials_path: str):
        self.tts_client = GoogleCloudTextToSpeechAdapter(credentials_path)
    
    def speech(self):
        """Return object with create method to mimic OpenAI interface"""
        return GoogleCloudSpeechAPI(self.tts_client)


class GoogleCloudSpeechAPI:
    """Mimic OpenAI audio.speech.create() interface"""
    
    def __init__(self, tts_client):
        self.tts_client = tts_client
    
    def create(self, model: str = "tts-1", voice: str = "nova", 
               input: str = "", **kwargs) -> Any:
        """
        Create speech using Google Cloud Text-to-Speech
        
        Args:
            model: Model name (ignored, for compatibility)
            voice: Voice name mapping
            input: Text to synthesize
            **kwargs: Additional parameters (output_file, language_code)
        
        Returns:
            Response object with .iter_bytes() method
        """
        # Map OpenAI voice names to Google Cloud voice names
        voice_mapping = {
            "alloy": "en-US-Neural2-A",
            "echo": "en-US-Neural2-C",
            "fable": "en-US-Neural2-D",
            "onyx": "en-US-Neural2-E",
            "nova": "en-US-Neural2-F",
            "shimmer": "en-US-Neural2-G",
        }
        
        # Get Google Cloud voice name
        google_voice = voice_mapping.get(voice, "id-ID-Neural2-A")
        language_code = "id-ID" if "id-ID" in google_voice else "en-US"
        
        # Output file
        output_file = kwargs.get("output_file", "/tmp/tts_output.mp3")
        
        # Synthesize
        self.tts_client.synthesize(
            text=input,
            output_file=output_file,
            language_code=language_code,
            voice_name=google_voice
        )
        
        # Return response object
        return GoogleCloudAudioResponse(output_file)


class GoogleCloudAudioResponse:
    """Response object that mimics OpenAI audio response"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Add usage tracking (mimics OpenAI usage format)
        self.usage = GoogleCloudUsage(
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0
        )
    
    def iter_bytes(self, chunk_size: int = 1024):
        """Iterate over audio bytes"""
        with open(self.file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    def write_to_file(self, file_path: str):
        """Write audio to file"""
        with open(self.file_path, "rb") as src:
            with open(file_path, "wb") as dst:
                dst.write(src.read())


def create_google_cloud_client(service_type: str, credentials_path: str):
    """
    Factory function to create Google Cloud client
    
    Args:
        service_type: "speech-to-text", "text-to-speech", or "whisper"
        credentials_path: Path to Google Cloud service account JSON key
    
    Returns:
        Client instance
    """
    if service_type == "speech-to-text":
        client = GoogleCloudSpeechToTextAdapter(credentials_path)
        # Return object with transcriptions attribute to mimic OpenAI
        class SpeechWrapper:
            def __init__(self, speech_client):
                self.audio = type('obj', (object,), {
                    'transcriptions': GoogleCloudTranscriptionsAPI(speech_client)
                })()
        return SpeechWrapper(client)
    
    elif service_type == "text-to-speech":
        client = GoogleCloudTextToSpeechAdapter(credentials_path)
        # Return object with audio attribute to mimic OpenAI
        class TTSWrapper:
            def __init__(self, tts_client):
                self.audio = type('obj', (object,), {
                    'speech': GoogleCloudSpeechAPI(tts_client)
                })()
        return TTSWrapper(client)
    
    else:
        raise ValueError(f"Unknown service type: {service_type}")
