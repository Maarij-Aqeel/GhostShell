"""File handling utilities."""

import os
from pathlib import Path
from typing import Optional


class FileHandler:
    """Handles file operations for the GhostShell tool."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with path.open("r", encoding="utf-8") as file:
                return file.read()
                
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}")
    
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file to write
            content: Content to write
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with path.open("w", encoding="utf-8") as file:
                file.write(content)
                
            print(f"✓ Successfully saved to {file_path}")
            
        except Exception as e:
            raise IOError(f"Error writing file {file_path}: {e}")
    
    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return Path(file_path).exists()