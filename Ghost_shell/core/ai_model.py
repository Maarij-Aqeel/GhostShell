"""AI model interface for Gemini."""

import sys
from typing import Optional, List
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown

from ..utils import FileHandler, CommandExecutor, CommandLogger
from ..prompts import PROMPT_TEMPLATES
from .config import Config


class GeminiModel:
    """Handles interaction with the Gemini AI model."""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = genai.Client(api_key=config.api_key)
        self.history: List[types.Content] = []
        self.console = Console()
        self.file_handler = FileHandler()
        self.logger = CommandLogger(config.log_file)
        self.executor = CommandExecutor(self.logger)
    
    def generate_response(
        self, 
        content: str, 
        task_type: str = "default",
        input_file: Optional[str] = None,
        output_file: Optional[str] = None,
        auto_execute: bool = False
    ) -> str:
        """
        Generate a response from the AI model.
        
        Args:
            content: The user's input/prompt
            task_type: Type of task (command, code, explain, summarize, default)
            input_file: Optional file to include in the prompt
            output_file: Optional file to save the response
            auto_execute: Whether to auto-execute commands
            
        Returns:
            The AI's response text
        """
        try:
            # Prepare the full content
            full_content = content
            if input_file:
                try:
                    file_content = self.file_handler.read_file(input_file)
                    full_content += f"\n\n--- File Content ({input_file}) ---\n{file_content}"
                except Exception as e:
                    self.console.print(f"[red]Warning: Could not read file {input_file}: {e}[/red]")
            
            # Get the appropriate prompt
            prompt = PROMPT_TEMPLATES.get(task_type, PROMPT_TEMPLATES["default"])
            
            # Create chat session
            chat = self.client.chats.create(
                model=self.config.model_name,
                config=types.GenerateContentConfig(system_instruction=prompt),
                history=self.history
            )
            
            # Generate response with streaming
            full_response = ""
            with self.console.status("[bold green]Thinking...[/]", spinner="dots"):
                for chunk in chat.send_message_stream(full_content):
                    if chunk.text:
                        self.console.print(Markdown(chunk.text), end="")
                        full_response += chunk.text
            
            self.console.print()  # New line after response
            
            # Update history
            self.history = chat.get_history()
            
            # Save to output file if specified
            if output_file:
                try:
                    self.file_handler.write_file(output_file, full_response)
                except Exception as e:
                    self.console.print(f"[red]Warning: Could not save to {output_file}: {e}[/red]")
            
            # Handle command execution
            if task_type == "command":
                self.executor.execute_commands(full_response, auto_execute)
            
            return full_response
            
        except Exception as e:
            self.console.print(f"[red]Error generating response: {e}[/red]")
            return ""
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.history = []
        self.console.print("[green]✓ Conversation history cleared.[/green]")
    
    def show_history(self, limit: Optional[int] = None) -> None:
        """Show command execution history."""
        history = self.logger.get_history(limit)
        if not history:
            self.console.print("[yellow]No command history found.[/yellow]")
            return
        
        self.console.print(f"[cyan]Command History (last {len(history)} entries):[/cyan]")
        for entry in history:
            self.console.print(f"  {entry}")