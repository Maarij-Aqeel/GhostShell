"""Command execution utilities."""

import re
import subprocess
from typing import List, Tuple
from rich.console import Console
from .logger import CommandLogger


class CommandExecutor:
    """Handles extraction and execution of commands from AI responses."""
    
    def __init__(self, logger: CommandLogger):
        self.console = Console()
        self.logger = logger
    
    def extract_commands(self, text: str) -> List[str]:
        """
        Extract commands from markdown code blocks.
        
        Args:
            text: Text containing markdown code blocks
            
        Returns:
            List of extracted commands
        """
        # Pattern for inline code blocks
        inline_commands = re.findall(r'`([^`\n]+)`', text)
        
        # Pattern for multi-line code blocks
        block_commands = re.findall(r'```(?:bash|sh|shell)?\n?(.*?)\n?```', text, re.DOTALL)
        
        commands = []
        
        # Process inline commands
        for cmd in inline_commands:
            cmd = cmd.strip()
            if cmd and self._is_safe_command(cmd):
                commands.append(cmd)
        
        # Process block commands
        for block in block_commands:
            for line in block.split('\n'):
                cmd = line.strip()
                if cmd and not cmd.startswith('#') and self._is_safe_command(cmd):
                    commands.append(cmd)
        
        return commands
    
    def _is_safe_command(self, command: str) -> bool:
        """
        Basic safety check for commands.
        
        Args:
            command: Command to check
            
        Returns:
            True if command appears safe, False otherwise
        """
        dangerous_patterns = [
            r'rm\s+-rf\s+/',  # rm -rf /
            r'>\s*/dev/sd[a-z]',  # writing to disk devices
            r'dd\s+if=.*of=/dev/',  # dd to devices
            r'mkfs\.',  # filesystem creation
            r'fdisk',  # partition manipulation
            r'format\s+c:',  # Windows format
            r'del\s+/s\s+/q\s+c:\\',  # Windows delete
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False
        
        return True
    
    def execute_commands(self, markdown_text: str, auto_execute: bool = False) -> None:
        """
        Execute commands extracted from markdown text.
        
        Args:
            markdown_text: Text containing commands
            auto_execute: If True, execute without prompting
        """
        commands = self.extract_commands(markdown_text)
        
        if not commands:
            self.console.print("[yellow]No executable commands found.[/yellow]")
            return
        
        self.console.print(f"[cyan]Found {len(commands)} command(s):[/cyan]")
        for i, cmd in enumerate(commands, 1):
            self.console.print(f"[bold blue]{i}.[/bold blue] [green]{cmd}[/green]")
        
        if not auto_execute:
            response = input("\nExecute these commands? [y/N/s(elect)]: ").lower().strip()
            
            if response == 's':
                self._selective_execution(commands)
                return
            elif response != 'y':
                self.console.print("[yellow]Command execution cancelled.[/yellow]")
                return
        
        self._execute_command_list(commands)
    
    def _selective_execution(self, commands: List[str]) -> None:
        """Allow user to select which commands to execute."""
        for i, cmd in enumerate(commands, 1):
            self.console.print(f"\n[bold blue]{i}.[/bold blue] [green]{cmd}[/green]")
            response = input("Execute this command? [y/n/q(uit)]: ").lower().strip()
            
            if response == 'q':
                break
            elif response == 'y':
                self._execute_single_command(cmd)
    
    def _execute_command_list(self, commands: List[str]) -> None:
        """Execute a list of commands."""
        for cmd in commands:
            self._execute_single_command(cmd)
    
    def _execute_single_command(self, command: str) -> None:
        """
        Execute a single command.
        
        Args:
            command: Command to execute
        """
        self.console.print(f"\n[bold red]>[/bold red] [green]{command}[/green]")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if result.stdout:
                    self.console.print(result.stdout)
                self.logger.log_command(f"✓ {command}")
            else:
                self.console.print(f"[red]Error (exit code {result.returncode}):[/red]")
                if result.stderr:
                    self.console.print(f"[red]{result.stderr}[/red]")
                self.logger.log_command(f"✗ {command} (failed)")
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Command timed out (30s limit)[/red]")
            self.logger.log_command(f"✗ {command} (timeout)")
        except Exception as e:
            self.console.print(f"[red]Execution error: {e}[/red]")
            self.logger.log_command(f"✗ {command} (error: {e})")