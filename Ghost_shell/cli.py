"""Main entry point for the GhostShell tool."""

import argparse
import sys
from typing import Optional

from .core import GeminiModel, Config
from .utils import FileHandler


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='gshell',
        description="GhostShell - AI-powered command and code generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "list all files in current directory"
  %(prog)s /code "create a python script to sort a list"
  %(prog)s /explain "how does git rebase work"
  %(prog)s /summarize -f document.txt
  %(prog)s /command "install nodejs on ubuntu" -o install_commands.txt
        """
    )
    
    parser.add_argument(
        "task",
        nargs="?",
        help="Task type: /command, /code, /explain, /summarize, or direct prompt"
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Description or prompt for the AI"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Input file to include in the prompt"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file to save the response"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="gemini-2.5-flash",
        help="AI model to use (default: gemini-2.5-flash)"
    )
    
    parser.add_argument(
        "--auto-execute",
        action="store_true",
        help="Auto-execute commands without prompting (use with caution)"
    )
    
    parser.add_argument(
        "--history",
        type=int,
        metavar="N",
        help="Show last N command history entries"
    )
    
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Clear command history"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="GhostShell {__import__('Ghost_shell').__version__}"
    )
    
    return parser


def determine_task_type(task_arg: Optional[str]) -> tuple[str, Optional[str]]:
    """
    Determine the task type and remaining prompt.
    
    Args:
        task_arg: The task argument from command line
        
    Returns:
        Tuple of (task_type, remaining_prompt)
    """
    if not task_arg:
        return "default", None
    
    if task_arg.startswith("/"):
        task_type = task_arg[1:]  # Remove the leading slash
        if task_type in ["command", "code", "explain", "summarize"]:
            return task_type, None
        else:
            # Unknown task type, treat as regular prompt
            return "default", task_arg
    else:
        # No slash, treat as regular prompt
        return "default", task_arg


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config = Config()
        if args.model:
            config.set_model(args.model)
        
        # Initialize the AI model
        model = GeminiModel(config)
        
        # Handle special commands
        if args.clear_history:
            model.logger.clear_history()
            return
        
        if args.history is not None:
            model.show_history(args.history)
            return
        
        # Validate input file if provided
        if args.file and not FileHandler.validate_file_exists(args.file):
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Determine task type and prompt
        task_type, remaining_prompt = determine_task_type(args.task)
        
        # Build the full prompt
        prompt_parts = []
        if remaining_prompt:
            prompt_parts.append(remaining_prompt)
        if args.prompt:
            prompt_parts.append(args.prompt)
        
        if not prompt_parts:
            print("Error: No prompt provided", file=sys.stderr)
            parser.print_help()
            sys.exit(1)
        
        full_prompt = " ".join(prompt_parts)
        
        # Generate response
        model.generate_response(
            content=full_prompt,
            task_type=task_type,
            input_file=args.file,
            output_file=args.output,
            auto_execute=args.auto_execute
        )
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()