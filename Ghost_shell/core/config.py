"""Configuration management for the Terminal LLM tool."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for the application."""
    
    def __init__(self):
        load_dotenv()
        self._api_key: Optional[str] = None
        self._model_name: str = "gemini-2.5-flash"
        self._log_file: str = "commands_history.log"
    
    @property
    def api_key(self) -> str:
        """Get Gemini API key from environment variables."""
        if not self._api_key:
            self._api_key = os.getenv("GEMINI_API")
            if not self._api_key:
                raise ValueError("GEMINI_API environment variable is required")
        return self._api_key
    
    @property
    def model_name(self) -> str:
        """Get the model name."""
        return self._model_name
    
    @property
    def log_file(self) -> str:
        """Get the log file path."""
        return self._log_file
    
    def set_model(self, model_name: str) -> None:
        """Set the model name."""
        self._model_name = model_name