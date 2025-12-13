# 🚀 Tajaa CLI - Quick Start Guide

## Installation (5 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd /opt/tajaa-cli
# or wherever you cloned/downloaded the project
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python3 test_components.py
```

You should see:
```
Total: 4/4 tests passed
```

## 🎮 Running the Application

### Basic Run
```bash
python3 main.py
```

### With Options
```bash
# Custom config file
python3 main.py --config /path/to/commands.yaml

# Custom log file
python3 main.py --log /path/to/session.log

# Both
python3 main.py --config ./commands.yaml --log ./my_logs.txt
```

## 🎯 Usage Flow

### 1. Start the Application
```bash
python3 main.py
```

### 2. You'll See the Banner
```
  _______ ___    ___ ___    ___ 
 |_   _  |   |  |   |   |  |   |
   | | | |   |  |   |   |  |   |
   | | | |   |  |   |   |  |   |
   | | | |   |_ |   |   |_ |   |
   |_| |_|\____|/    \____||___|

Professional Penetration Testing Command Manager
Version 2.0.0 | Ethical Hacking & Security Research
```

### 3. Select a Category
Use arrow keys to navigate:
- Reconnaissance (5 tools)
- Web Application Attacks (4 tools)
- Exploitation (3 tools)
- Network Analysis (3 tools)
- Service Enumeration (4 tools)
- Wireless Attacks (3 tools)
- [Exit]

### 4. Select a Tool
Example: Selecting "Reconnaissance" shows:
```
Nmap - Quick Scan
  └─ Fast port scan of the 1000 most common ports

Nmap - Full Port Scan
  └─ Comprehensive scan of all 65535 ports with service detection

...
[← Back to Categories]
```

### 5. Enter Parameters
The tool will ask for required inputs with validation:

```
Enter target ip: 192.168.1.1  ✓
```

If you enter invalid input:
```
Enter target ip: 999.999.999.999
✗ Invalid IPv4 address: '999.999.999.999'. Expected format: xxx.xxx.xxx.xxx
Enter target ip:
```

### 6. Review & Execute
```
╭─ Generated Command ─────────────────────╮
│ nmap -T4 -F 192.168.1.1                 │
╰─────────────────────────────────────────╯
✓ Command copied to clipboard

Execute this command now? [Y/n]:
```

### 7. Command Execution
Press `Y` to run or `n` to skip:
```
⠋ Executing command...
✓ Command executed successfully

Return to main menu? [Y/n]:
```

## 🔍 Input Validation Examples

### Valid IPv4 Addresses ✓
- `192.168.1.1`
- `10.0.0.1`
- `172.16.0.1`

### Invalid IPv4 Addresses ✗
- `999.999.999.999` (out of range)
- `192.168.1` (incomplete)
- `192.168.1.1.1` (too many octets)
- `example.com` (not an IP)

### Valid Ports ✓
- `80` (HTTP)
- `443` (HTTPS)
- `22` (SSH)
- `3389` (RDP)

### Invalid Ports ✗
- `0` (below range)
- `99999` (above 65535)
- `abc` (not a number)

## 🎨 Keyboard Shortcuts

- **↑/↓ Arrow Keys**: Navigate menus
- **Enter**: Select option
- **Ctrl+C**: Cancel current operation / Return to previous menu
- **Y/N**: Confirm/Decline prompts

## 📝 Viewing Logs

All executed commands are logged automatically:

```bash
cat session_logs.txt
```

Output:
```
================================================================================
SESSION START: 2025-12-13 14:30:00
================================================================================
[2025-12-13 14:31:15] Category: Reconnaissance | Tool: Nmap - Quick Scan
Command: nmap -T4 -F 192.168.1.1
--------------------------------------------------------------------------------
```

## ⚙️ Customizing Commands

Edit `commands.yaml`:

```yaml
categories:
  reconnaissance:
    name: "Reconnaissance"
    tools:
      my_custom_scan:
        name: "My Custom Scan"
        description: "What my scan does"
        command: "nmap -sS -p {port} {target_ip}"
        params:
          - target_ip
          - port
```

Restart the application to see your changes.

## 🛠️ Troubleshooting

### "Tool 'nmap' not found!"
Install the missing tool:
```bash
sudo apt update
sudo apt install nmap
```

### "Configuration file not found"
Ensure `commands.yaml` is in the same directory as `main.py`:
```bash
ls -la
# You should see both main.py and commands.yaml
```

### Import Errors
Reinstall dependencies:
```bash
pip install --force-reinstall -r requirements.txt
```

### Permission Denied
Make the script executable:
```bash
chmod +x main.py
```

## 🎓 Pro Tips

1. **Clipboard Auto-Copy**: Every generated command is automatically copied to your clipboard - just paste it anywhere!

2. **Test Before Execute**: Choose "n" when asked to execute, test the command manually first

3. **Log Review**: Regularly check `session_logs.txt` to track your testing activities

4. **Custom Wordlists**: Modify paths in `commands.yaml` to use your preferred wordlists

5. **Graceful Exit**: Press Ctrl+C at any time to safely return to the previous menu

## 📚 Next Steps

1. **Explore All Categories**: Check out all 6 categories and 22+ tools
2. **Add Your Tools**: Customize `commands.yaml` with your favorite tools
3. **Create Aliases**: Add a shell alias for quick access
4. **Integrate**: Use in your penetration testing workflow

## 💡 Example Workflow

```bash
# 1. Start Tajaa
python3 main.py

# 2. Run Reconnaissance
Select: Reconnaissance → Nmap - Quick Scan
Enter: 192.168.1.100
Execute: Yes

# 3. Run Web Scanning
Select: Web Application Attacks → Gobuster
Enter: 192.168.1.100
Execute: Yes

# 4. Review Logs
# Exit application (Ctrl+C)
cat session_logs.txt

# 5. Continue Testing
# All commands are in clipboard and logs!
```

## 🔒 Security Reminder

⚠️ **ALWAYS GET AUTHORIZATION BEFORE TESTING!**

This tool is for:
- ✓ Your own systems
- ✓ Authorized penetration tests
- ✓ Educational labs
- ✓ CTF competitions

NOT for:
- ✗ Unauthorized scanning
- ✗ Illegal activities
- ✗ Violating terms of service

---

**Happy Ethical Hacking! 🔒**

