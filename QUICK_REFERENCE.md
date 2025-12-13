# Tajaa CLI - Quick Reference

## Installation

```bash
# Clone the repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

## Basic Usage

### Start the Application
```bash
python main.py
```

### With Custom Configuration
```bash
python main.py --config custom_commands.yaml
```

### Direct Execution Flow
1. Application displays ASCII banner and categories table
2. Select a category using arrow keys
3. Choose a tool from the category
4. Enter required parameters (IP addresses, ports, etc.)
5. Review generated command
6. Confirm execution or copy to clipboard

## Key Shortcuts

| Action | Shortcut |
|--------|----------|
| Navigate menu | `↑` `↓` Arrow keys |
| Select option | `Enter` |
| Cancel/Back | `Ctrl+C` |
| Confirm execution | `y` + `Enter` |
| Skip execution | `n` + `Enter` |

## Common Parameters

### IP Address Format
- Must be valid IPv4: `192.168.1.1`
- Invalid examples: `999.999.999.999`, `localhost`

### Port Numbers
- Range: `1-65535`
- Common ports: `21` (FTP), `22` (SSH), `80` (HTTP), `443` (HTTPS)

## Session Logs

All executed commands are logged to:
```
./session_logs.txt
```

Log format:
```
[YYYY-MM-DD HH:MM:SS] [Category] [Tool] command
```

## Tool Categories

1. **Reconnaissance** - Network scanning and enumeration
2. **Web Application Attacks** - Web vulnerability testing
3. **Exploitation** - Exploit frameworks and tools
4. **Network Analysis** - Traffic analysis and sniffing
5. **Service Enumeration** - Service-specific enumeration
6. **Wireless Attacks** - WiFi security testing

## Example Workflow

```bash
$ python main.py

# Select: Reconnaissance
# Select: Nmap - Quick Scan
# Enter target ip: 192.168.1.1
# Review: nmap -T4 -F 192.168.1.1
# Confirm: y

# Command executes and logs to session_logs.txt
```

## Configuration

Edit `commands.yaml` to add custom tools:

```yaml
categories:
  custom_category:
    name: "My Custom Tools"
    tools:
      my_tool:
        name: "Custom Tool Name"
        description: "What this tool does"
        command: "tool_binary {param1} {param2}"
        params:
          - param1
          - param2
```

## Troubleshooting

### Tool Not Found
If you see "Tool 'toolname' not found", install the required tool:
```bash
sudo apt-get install toolname  # Debian/Ubuntu
```

### Permission Denied
Some tools require root privileges:
```bash
sudo python main.py
```

### Invalid IP Address
Ensure IPv4 format: `xxx.xxx.xxx.xxx` where each octet is 0-255

## Author

Tajaa

## License

MIT License - See LICENSE file for details

