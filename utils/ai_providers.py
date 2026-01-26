"""
AI Provider adapters for supporting multiple AI services
"""

import json
import re
import unicodedata
from typing import Optional, Any, List, Dict


def _sanitize_content(text: str) -> str:
    """Remove control characters while preserving newlines and valid Unicode"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove control characters except whitespace
    text = ''.join(
        ch if unicodedata.category(ch)[0] != 'C' or ch in '\t\n\r '
        else ' ' for ch in text
    )
    
    # Ensure valid UTF-8
    text = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    
    return text


class GoogleGeminiAdapter:
    """Adapter to make Google Gemini API compatible with OpenAI client interface"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initialize Google Gemini adapter
        
        Args:
            api_key: Google API key
            model: Model name (default: gemini-pro)
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Create nested structure to mimic OpenAI client
        self.chat = ChatCompletions(api_key, model)


class ChatCompletions:
    """Wrapper for chat completions adapter"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.completions = ChatCompletionsAdapter(api_key, model)


class ChatCompletionsAdapter:
    """Adapter for chat completions to mimic OpenAI interface"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def create(self, messages: List[Dict], **kwargs) -> Any:
        """
        Create a chat completion using Google Gemini API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters (temperature, max_tokens, etc)
        
        Returns:
            Response object with .choices[0].message.content
        """
        import requests
        
        # Convert OpenAI message format to Gemini format
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Ensure content is a string and handle special characters
            if not isinstance(content, str):
                content = str(content)
            
            # Sanitize content to remove control characters
            content = _sanitize_content(content)
            
            # Convert roles: "assistant" -> "model", "user" -> "user"
            if role == "assistant":
                role = "model"
            
            contents.append({
                "role": role,
                "parts": [{"text": content}]
            })
        
        # Build request
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": min(2.0, max(0.0, kwargs.get("temperature", 0.7))),
                "maxOutputTokens": kwargs.get("max_tokens", 2048),
                "topP": 0.95,
                "topK": 40
            }
        }
        
        # Add safety settings to allow more varied content
        payload["safetySettings"] = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        try:
            import sys
            import json as json_lib
            
            # Try to validate payload, but don't fail if validation itself has issues
            try:
                payload_json = json_lib.dumps(payload)
                # Payload is valid
            except (ValueError, TypeError) as validation_error:
                # Payload validation failed, but still try to send it
                # requests.post with json= parameter will handle serialization
                print(f"[DEBUG] Payload validation warning: {str(validation_error)}", file=sys.stderr)
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            # Get response text for debugging
            response_text = response.text
            
            # Try to parse JSON with better error handling
            try:
                data = response.json()
            except ValueError as json_error:
                # Log the problematic response for debugging
                print(f"[DEBUG] JSON parsing error: {str(json_error)}", file=sys.stderr)
                print(f"[DEBUG] Response status: {response.status_code}", file=sys.stderr)
                print(f"[DEBUG] Response length: {len(response_text)}", file=sys.stderr)
                
                # Try to extract partial response if available
                if response_text:
                    print(f"[DEBUG] Response (first 1000 chars):\n{response_text[:1000]}", file=sys.stderr)
                    print(f"[DEBUG] Response (last 500 chars):\n{response_text[-500:]}", file=sys.stderr)
                
                # Return a fallback response with error message
                error_msg = f"API response parsing failed: {str(json_error)}"
                print(f"[DEBUG] {error_msg}", file=sys.stderr)
                return GeminiResponse(error_msg)
            
            # Extract text from Gemini response
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                
                # Check for blocked content
                if "finishReason" in candidate and candidate["finishReason"] == "SAFETY":
                    print("[DEBUG] Response blocked by safety filters", file=sys.stderr)
                    return GeminiResponse("Content blocked by safety filters")
                
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        text = parts[0]["text"]
                        # Return object mimicking OpenAI response structure
                        return GeminiResponse(text)
            
            # Handle error responses
            if "error" in data:
                error_msg = f"Gemini API error: {data['error']}"
                print(f"[DEBUG] {error_msg}", file=sys.stderr)
                return GeminiResponse(error_msg)
            
            # No valid response structure found
            print("[DEBUG] No valid response structure from Gemini API", file=sys.stderr)
            return GeminiResponse("No valid response from API")
            
        except requests.exceptions.Timeout:
            error_msg = "Gemini API request timeout (60s)"
            print(f"[DEBUG] {error_msg}", file=sys.stderr)
            return GeminiResponse(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to call Gemini API: {str(e)}"
            print(f"[DEBUG] {error_msg}", file=sys.stderr)
            return GeminiResponse(error_msg)


class GeminiResponse:
    """Response object that mimics OpenAI response structure"""
    
    def __init__(self, text: str):
        self.choices = [GeminiChoice(text)]
        # Add usage tracking (mimics OpenAI usage format)
        self.usage = GeminiUsage(
            prompt_tokens=len(text.split()),
            completion_tokens=len(text.split()),
            total_tokens=len(text.split()) * 2
        )


class GeminiUsage:
    """Usage statistics that mimics OpenAI usage object"""
    
    def __init__(self, prompt_tokens: int, completion_tokens: int, total_tokens: int):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


class GeminiChoice:
    """Choice object that mimics OpenAI choice structure"""
    
    def __init__(self, text: str):
        self.message = GeminiMessage(text)
        self.finish_reason = "stop"


class GeminiMessage:
    """Message object that mimics OpenAI message structure"""
    
    def __init__(self, content: str):
        self.content = content
        self.role = "assistant"


def create_ai_client(provider_type: str, api_key: str = "", model: str = "", 
                     base_url: Optional[str] = None, service_type: Optional[str] = None,
                     credentials_path: Optional[str] = None):
    """
    Factory function to create appropriate AI client
    
    Args:
        provider_type: "openai", "google", or "google-cloud"
        api_key: API key for the provider (optional for google-cloud)
        model: Model name
        base_url: Optional base URL (for OpenAI)
        service_type: Type of service for google-cloud ("speech-to-text" or "text-to-speech")
        credentials_path: Path to Google Cloud credentials JSON (for google-cloud)
    
    Returns:
        AI client instance
    """
    if provider_type.lower() == "google":
        return GoogleGeminiAdapter(api_key, model)
    elif provider_type.lower() == "google-cloud":
        from utils.google_cloud_adapters import create_google_cloud_client
        if not credentials_path:
            credentials_path = "google-cloud-credentials.json"
        return create_google_cloud_client(service_type or "text-to-speech", credentials_path)
    elif provider_type.lower() == "openai":
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url=base_url or "https://api.openai.com/v1")
    else:
        raise ValueError(f"Unknown AI provider: {provider_type}")
