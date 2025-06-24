"""Logging utilities for command history."""

import logging
from pathlib import Path
from typing import List, Optional


class CommandLogger:
    """Handles logging and retrieval of command history."""
    
    def __init__(self, log_file: str = "commands_history.log"):
        self.log_file = Path(log_file)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logging configuration."""
        self.logger = logging.getLogger("command_logger")
        self.logger.setLevel(logging.INFO)
        
        # Create log directory if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_command(self, command: str) -> None:
        """
        Log a command to the history file.
        
        Args:
            command: The command to log
        """
        try:
            self.logger.info(command.strip())
        except Exception as e:
            print(f"Warning: Failed to log command: {e}")
    
    def get_history(self, limit: Optional[int] = None) -> List[str]:
        """
        Retrieve command history.
        
        Args:
            limit: Maximum number of commands to retrieve
            
        Returns:
            List of command history entries
        """
        try:
            if not self.log_file.exists():
                return []
            
            with self.log_file.open('r', encoding='utf-8') as file:
                lines = file.readlines()
            
            if limit:
                lines = lines[-limit:]
            
            return [line.strip() for line in lines if line.strip()]
            
        except Exception as e:
            print(f"Warning: Failed to retrieve command history: {e}")
            return []
    
    def clear_history(self) -> None:
        """Clear the command history file."""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
            print("✓ Command history cleared")
        except Exception as e:
            print(f"Error clearing history: {e}")