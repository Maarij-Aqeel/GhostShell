# 👻 GhostShell

**AI-powered terminal assistant** for intelligent command generation, code creation, technical explanations, and content summarization — powered by **Google Gemini AI**.

> Think of it as your AI-powered shell companion — command smarter, not harder.

---

## Features

- **LLM Integration**: Uses Gemini AI to understand and generate terminal tasks  
- **Code Generation**: Quickly scaffold code in Python, Bash, etc.  
- **Explain Anything**: Get clear explanations of code, tools, or concepts  
- **Summarization**: Compress large files or documentation into digestible insights  
- **Rich Terminal Output**: Beautiful formatting with `rich` (colors, markdown, etc.)  
- **Command History**: Log and reuse previously generated commands  
- **Safety Checks**: Warns before executing potentially dangerous commands  

---

## Installation


### From Source

```bash
git clone https://github.com/Maarij-Aqeel/GhostShell.git
cd GhostShell
pip install -e .
```

### Development Mode

```bash
pip install -e ".[dev]"
```

---

## Setup

1. Get your **Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)  
2. Create a `.env` file in the project root or export as an environment variable:

```bash
# .env file
GEMINI_API=your_gemini_api_key
```

Or:

```bash
export GEMINI_API=your_gemini_api_key
```

---

## Usage

GhostShell installs 3 command aliases:

- `ghostshell` (main)  
- `gshell` (short)  
- `gsh` (tiny)

### 🔹 Basic Examples

```bash
ghostshell "command to list files by size"

ghostshell /code "create a Flask login system"

ghostshell /explain "difference between Docker and Podman"

ghostshell /summarize -f long_document.txt

ghostshell /command "install Docker on Ubuntu" -o setup.sh
```

### 🔸 Task Prefixes

| Prefix        | Purpose                            |
|---------------|-------------------------------------|
| `/command`    | Generate terminal commands          |
| `/code`       | Generate code snippets              |
| `/explain`    | Explain commands or code            |
| `/summarize`  | Summarize large input files         |
| _No Prefix_   | General AI assistance               |

---

## Advanced Usage

```bash
# Analyze and modify file content
ghostshell /code "optimize this Python script" -f script.py

# Auto-execute suggested commands (⚠️ use with caution)
ghostshell /command "install dependencies" --auto-execute

# Save output to a specific file
ghostshell /code "generate hello world in Go" -o hello.go

# Show last 10 generated commands
ghostshell --history 10

# Clear all history
ghostshell --clear-history

# Use a different Gemini model
ghostshell -m gemini-1.5-pro "build a web crawler"
```

---

## Safety First

GhostShell is designed with safety in mind:

-  Dangerous command detection  
-  Manual confirmation for critical actions  
-  Timeout fallback (default 30s)  
-  No command is auto-executed without permission  

---

## Development

### Environment Setup

```bash
git clone https://github.com/Maarij-Aqeel/GhostShell.git
cd GhostShell
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=Ghost_shell
```

### Code Quality

```bash
black Ghost_shell/
flake8 Ghost_shell/
mypy Ghost_shell/
```

---

## Contributing

Contributions are welcome!

1. Fork this repo  
2. Create a branch (`git checkout -b feature-xyz`)  
3. Commit your changes  
4. Push and open a pull request  
5. Add a meaningful description 

---

### .env.example

```env
# Rename this file to `.env` and add your API key
GEMINI_API=your_gemini_api_key_here
```

---

