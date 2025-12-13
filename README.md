# 🔒 Tajaa CLI - Professional Penetration Testing Command Manager

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/ARSTaha/tajaa-cli)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.kali.org/)
[![GitHub](https://img.shields.io/badge/GitHub-ARSTaha-181717?logo=github)](https://github.com/ARSTaha)

A production-grade, object-oriented CLI tool for ethical hacking and penetration testing on Kali Linux. Built with clean architecture, SOLID principles, and comprehensive input validation.

## ✨ Features

- **🏗️ Clean OOP Architecture**: Modular design with clear separation of concerns
- **🔍 Smart Input Validation**: Validates IPv4 addresses and port numbers automatically
- **📦 Dependency Checking**: Warns if required tools are not installed
- **📝 Session Logging**: Auto-logs all commands to `session_logs.txt` with timestamps
- **🎨 Rich UI/UX**: Beautiful terminal interface with progress indicators
- **⌨️ Graceful Error Handling**: Handles Ctrl+C and errors without ugly tracebacks
- **📋 Clipboard Integration**: Auto-copies generated commands to clipboard
- **🔧 Extensible Configuration**: Easy to add new tools via YAML

## 📋 Prerequisites

- **Operating System**: Kali Linux (or any Linux distribution)
- **Python**: 3.8 or higher
- **Pentesting Tools**: nmap, gobuster, nikto, etc. (install as needed)

## 🚀 Installation

### 1. Clone or Download

```bash
# Clone from GitHub
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Make Executable

```bash
chmod +x main.py
```

## 📖 Usage

### Basic Usage

```bash
python3 main.py
```

### With Custom Config

```bash
python3 main.py --config /path/to/custom_commands.yaml
```

### With Custom Log File

```bash
python3 main.py --log /path/to/custom_logs.txt
```

### Both Options

```bash
python3 main.py --config ./commands.yaml --log ./my_session.log
```

## 🎯 Workflow

1. **Select Category**: Choose from Reconnaissance, Web Attacks, Exploitation, etc.
2. **Select Tool**: Pick a specific tool from the category
3. **Input Parameters**: Enter validated inputs (IP addresses, ports, etc.)
4. **Review Command**: See the generated command before execution
5. **Execute**: Run the command or just copy it to clipboard

## 🏗️ Architecture

### Class Structure

```
TajaaCLI (Main Orchestrator)
├── ConfigLoader (YAML parsing)
├── InputValidator (IPv4, Port validation)
├── DependencyChecker (Tool availability)
├── SessionLogger (Command logging)
├── CommandExecutor (Command execution)
└── UIManager (User interface)
```

### Design Principles

- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: Components receive dependencies via constructor
- **Type Hinting**: Full typing coverage for better IDE support
- **Error Handling**: Graceful error handling at every level

## 📝 Configuration

### Adding a New Tool

Edit `commands.yaml`:

```yaml
categories:
  your_category:
    name: "Your Category Name"
    tools:
      your_tool:
        name: "Tool Display Name"
        description: "What this tool does"
        command: "tool_binary {param1} {param2}"
        params:
          - param1
          - param2
```

### Parameter Validation

- **`target_ip`**: Automatically validates IPv4 format
- **`port`**: Validates integer in range 1-65535
- **Other params**: Ensures non-empty input

## 📂 Project Structure

```
tajaa-cli/
├── main.py              # Main application (all classes)
├── commands.yaml        # Tool configurations
├── requirements.txt     # Python dependencies
├── session_logs.txt     # Auto-generated command logs
└── README.md           # This file
```

## 🔧 Development

### Adding a New Validator

```python
class InputValidator:
    def validate_custom(self, input_str: str) -> Tuple[bool, Optional[str]]:
        """Add your custom validation logic."""
        # Your validation code
        pass
```

### Adding a New Category Class

```python
@dataclass
class NewConfig:
    """Your new configuration class."""
    field1: str
    field2: List[str]
```

## 🛡️ Security Considerations

⚠️ **WARNING**: This tool is for **authorized penetration testing only**!

- Always get written permission before testing
- Never use against systems you don't own or have permission to test
- Follow responsible disclosure practices
- Respect privacy and legal boundaries

## 📊 Example Session Log

```
================================================================================
SESSION START: 2025-12-13 14:30:00
================================================================================
[2025-12-13 14:31:15] Category: Reconnaissance | Tool: Nmap - Quick Scan
Command: nmap -T4 -F 192.168.1.1
--------------------------------------------------------------------------------
[2025-12-13 14:33:22] Category: Web Application Attacks | Tool: Gobuster
Command: gobuster dir -u http://192.168.1.1 -w /usr/share/wordlists/dirb/common.txt
--------------------------------------------------------------------------------
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository: https://github.com/ARSTaha/tajaa-cli
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the existing OOP structure
4. Add type hints and docstrings
5. Test thoroughly
6. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Tajaa

## 🙏 Acknowledgments

- Kali Linux Team
- Python Rich library
- InquirerPy project
- The InfoSec Community

## 📞 Support

For issues, questions, or feature requests, please open an issue on GitHub:
https://github.com/ARSTaha/tajaa-cli/issues

---

**Remember**: With great power comes great responsibility. Use ethically! 🔒

