# Tajaa CLI - Quick Reference Guide

Fast command reference for Tajaa CLI operations.

**Author:** Tajaa  
**Version:** 3.1.0

---

## Installation Commands

```bash
# Clone repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Run installer
chmod +x install.sh
./install.sh

# Activate virtual environment (REQUIRED)
source .venv/bin/activate

# Run Tajaa CLI
python3 main.py
```

---

## Daily Usage

### Starting Tajaa CLI

```bash
# Always activate venv first
cd ~/tajaa-cli
source .venv/bin/activate

# Launch framework
python3 main.py
```

### Load Specific Modules

```bash
# CTF toolkit
python3 main.py --config configs/02_ctf_kit.yaml

# Web security
python3 main.py --config configs/03_web_bounty.yaml

# Active Directory
python3 main.py --config configs/04_network_ad.yaml

# Mobile & IoT
python3 main.py --config configs/05_mobile_iot.yaml

# Cloud security
python3 main.py --config configs/06_cloud_auditor.yaml

# OSINT
python3 main.py --config configs/07_osint_detective.yaml

# Wireless
python3 main.py --config configs/08_wireless_radio.yaml

# Post-exploitation
python3 main.py --config configs/09_post_exploit.yaml
```

---

## Bash Aliases (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Tajaa CLI shortcuts
alias tajaa='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py'
alias tajaa-ctf='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/02_ctf_kit.yaml'
alias tajaa-web='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/03_web_bounty.yaml'
alias tajaa-ad='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/04_network_ad.yaml'
alias tajaa-mobile='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/05_mobile_iot.yaml'
alias tajaa-cloud='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/06_cloud_auditor.yaml'
alias tajaa-osint='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/07_osint_detective.yaml'
alias tajaa-wireless='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/08_wireless_radio.yaml'
alias tajaa-post='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/09_post_exploit.yaml'
```

Then reload:
```bash
source ~/.bashrc
```

---

## Common Workflows

### Web Application Testing

```bash
# 1. Launch web module
tajaa-web

# 2. Subdomain enumeration
# → Select: Subdomain Discovery
# → Select: Subfinder / Amass / Assetfinder

# 3. Directory brute forcing
# → Select: Directory Brute Forcing
# → Select: Gobuster / Ffuf / Feroxbuster

# 4. Vulnerability scanning
# → Select: Vulnerability Scanning
# → Select: Nuclei / Nikto
```

### Active Directory Pentest

```bash
# 1. Launch AD module
tajaa-ad

# 2. Network enumeration
# → Select: Network Discovery
# → Select: Nmap / CrackMapExec

# 3. SMB enumeration
# → Select: SMB Enumeration
# → Select: Enum4Linux-ng / SMBMap

# 4. Active Directory attacks
# → Select: Active Directory Attacks
# → Select: Kerberoasting / AS-REP Roasting
```

### CTF Challenge

```bash
# 1. Launch CTF module
tajaa-ctf

# 2. Port scan target
# → Select: Network Reconnaissance
# → Select: RustScan / Nmap

# 3. Check for steganography
# → Select: Steganography & Forensics
# → Select: Steghide / Binwalk / ExifTool

# 4. Crack passwords
# → Select: Password Cracking
# → Select: John the Ripper / Hashcat
```

---

## Session Management

### Session Logs

All commands are automatically logged to `session_logs.txt`:

```bash
# View current session log
cat session_logs.txt

# View last 20 commands
tail -n 20 session_logs.txt

# Search for specific commands
grep "nmap" session_logs.txt
```

### Custom Log File

```bash
# Use custom log file
python3 main.py --log pentest_client_2025.txt
```

---

## Virtual Environment Tips

### Activation

```bash
# Activate
source .venv/bin/activate

# Check if activated (you'll see .venv in prompt)
(.venv) kali@kali:~/tajaa-cli$

# Deactivate when done
deactivate
```

### Troubleshooting

```bash
# If venv is corrupted, recreate it
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration Customization

### Add Custom Tool

Edit any YAML config file (e.g., `configs/03_web_bounty.yaml`):

```yaml
categories:
  custom_category:
    name: "🔥 My Custom Tools"
    tools:
      my_tool:
        name: "My Custom Scanner"
        description: "Does awesome security testing"
        command: "mytool -target {target} -port {port}"
        params:
          - target
          - port
        defaults:
          port: "80"
```

Save and reload Tajaa CLI - your tool appears in the menu!

---

## Clipboard Integration

All generated commands are automatically copied to clipboard:

```bash
# After selecting a tool and entering parameters
# The command is copied - just paste with Ctrl+Shift+V

# In terminal
Ctrl+Shift+V  # Paste the command
```

---

## Installing Additional Tools

### Install Arsenal (Optional)

```bash
# Install CyberChef, payloads, wordlists
sudo chmod +x install_arsenal.sh
sudo ./install_arsenal.sh

# This installs:
# - CyberChef (Local HTML)
# - LinPEAS, WinPEAS, pspy
# - SecLists, RockYou wordlist
```

### Manual Tool Installation

```bash
# Install common pentesting tools
sudo apt update
sudo apt install -y nmap gobuster nikto sqlmap hydra metasploit-framework

# Install specialized tools
sudo apt install -y amass subfinder nuclei feroxbuster

# For wireless testing
sudo apt install -y aircrack-ng reaver wifite hashcat

# For Active Directory
sudo apt install -y crackmapexec impacket-scripts bloodhound
```

---

## Performance Tips

### Fast Scanning

Use RustScan for initial port discovery:
```bash
# Scan all ports in seconds, then feed to nmap
rustscan -a 10.10.10.10 -- -A -sC
```

### Background Execution

For long-running scans:
```bash
# Execute command in background
nmap -p- 10.10.10.10 -oA fullscan &

# Monitor progress
tail -f fullscan.gnmap
```

---

## Security Reminders

⚠️ **Always remember:**

- Get written authorization before testing
- Stay within authorized scope
- Document everything
- Follow responsible disclosure
- Respect privacy and legal boundaries

---

## Getting Help

### Documentation

- **[README.md](README.md)** - Main documentation
- **[CONFIG_CATALOG.md](CONFIG_CATALOG.md)** - All tools reference
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples

### Support

- **GitHub Issues:** https://github.com/ARSTaha/tajaa-cli/issues
- **Discussions:** https://github.com/ARSTaha/tajaa-cli/discussions

---

## Keyboard Shortcuts

### In Tajaa CLI

- **Arrow Keys** - Navigate menus
- **Enter** - Select option
- **Ctrl+C** - Cancel current operation / Go back
- **Ctrl+D** - Exit program

### In Terminal

- **Ctrl+Shift+C** - Copy
- **Ctrl+Shift+V** - Paste
- **Ctrl+L** - Clear screen
- **Ctrl+R** - Search command history

---

**Quick Start:**
```bash
cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py
```

**Remember:** Always activate the virtual environment first!

---

**Built with ❤️ for the security community by Tajaa**

