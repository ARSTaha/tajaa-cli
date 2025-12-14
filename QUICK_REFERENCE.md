# ⚡ Tajaa CLI - Quick Reference Cheat Sheet

**Version 3.0.0** | The Ultimate Modular Cyber Security Framework

---

## 🚀 Installation One-Liner

```bash
git clone https://github.com/ARSTaha/tajaa-cli.git && cd tajaa-cli && pip install -r requirements.txt && python3 main.py --help
```

---

## 📦 The 8 Specialized Modules

| Module | Config File | Use Case | Tool Count |
|--------|------------|----------|-----------|
| 🏆 **CTF Kit** | `configs/02_ctf_kit.yaml` | Competitions, challenges, rapid assessments | 50+ |
| 🌐 **Web Bounty** | `configs/03_web_bounty.yaml` | Bug bounty hunting, web app pentesting | 70+ |
| 🏢 **Network AD** | `configs/04_network_ad.yaml` | Corporate networks, Active Directory attacks | 55+ |
| 📱 **Mobile IoT** | `configs/05_mobile_iot.yaml` | Mobile apps, firmware reverse engineering | 60+ |
| ☁️ **Cloud Auditor** | `configs/06_cloud_auditor.yaml` | AWS/Azure/GCP security audits | 50+ |
| 🕵️ **OSINT Detective** | `configs/07_osint_detective.yaml` | Intelligence gathering, passive recon | 65+ |
| 📡 **Wireless Radio** | `configs/08_wireless_radio.yaml` | WiFi/Bluetooth/SDR/RFID security | 75+ |
| 🔒 **Post Exploit** | `configs/09_post_exploit.yaml` | Post-compromise, persistence, lateral movement | 55+ |

**Total: 480+ tools across 8 domains**

---

## 🎯 Command Patterns

### Basic Usage
```bash
# Default configuration
python3 main.py

# Specific module
python3 main.py --config <module_file>

# With custom logs
python3 main.py --config <module_file> --log <log_file>
```

### Module Launch Commands

```bash
# CTF & Speed Hacking
python3 main.py --config configs/02_ctf_kit.yaml

# Web Application Security
python3 main.py --config configs/03_web_bounty.yaml

# Active Directory Pentesting
python3 main.py --config configs/04_network_ad.yaml

# Mobile & IoT Security
python3 main.py --config configs/05_mobile_iot.yaml

# Cloud Security Auditing
python3 main.py --config configs/06_cloud_auditor.yaml

# OSINT & Intelligence
python3 main.py --config configs/07_osint_detective.yaml

# Wireless & Radio Hacking
python3 main.py --config configs/08_wireless_radio.yaml

# Post-Exploitation
python3 main.py --config configs/09_post_exploit.yaml
```

---

## ⚡ Quick Aliases Setup

```bash
# Add to ~/.bashrc or ~/.zshrc
alias tajaa="python3 ~/tajaa-cli/main.py"
alias tajaa-ctf="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/02_ctf_kit.yaml"
alias tajaa-web="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/03_web_bounty.yaml"
alias tajaa-ad="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/04_network_ad.yaml"
alias tajaa-mobile="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/05_mobile_iot.yaml"
alias tajaa-cloud="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/06_cloud_auditor.yaml"
alias tajaa-osint="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/07_osint_detective.yaml"
alias tajaa-wireless="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/08_wireless_radio.yaml"
alias tajaa-post="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/09_post_exploit.yaml"

# Reload shell
source ~/.bashrc
```

### Usage After Aliases
```bash
tajaa-ctf        # Launch CTF module
tajaa-web        # Launch web bounty module
tajaa-ad         # Launch AD pentesting module
tajaa-mobile     # Launch mobile/IoT module
tajaa-cloud      # Launch cloud auditing module
tajaa-osint      # Launch OSINT module
tajaa-wireless   # Launch wireless hacking module
tajaa-post       # Launch post-exploitation module
```

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Navigate menu | `↑` `↓` Arrow keys |
| Select option | `Enter` |
| Go back | Select `[← Back]` option |
| Cancel/Exit | `Ctrl+C` (graceful exit) |
| Confirm execution | `y` + `Enter` |
| Skip execution (copy only) | `n` + `Enter` |

---

## 🔍 Parameter Validation

### IP Address Format
- **Valid**: `192.168.1.1`, `10.0.0.1`, `172.16.0.1`
- **Invalid**: `999.999.999.999`, `localhost`, `192.168.1.1/24`

### Port Numbers
- **Range**: `1-65535`
- **Common Ports**: 
  - `21` (FTP)
  - `22` (SSH)
  - `80` (HTTP)
  - `443` (HTTPS)
  - `3306` (MySQL)
  - `3389` (RDP)
  - `8080` (HTTP-Alt)

### Domain Format
- **Valid**: `example.com`, `subdomain.example.com`, `test.example.co.uk`
- **Invalid**: Empty string, `http://example.com` (remove protocol)

---

## 📝 Session Logs

### Default Location
```
./session_logs.txt
```

### Custom Log File
```bash
# Date-stamped logs
python3 main.py --config web_bounty.yaml --log ./engagement_$(date +%Y%m%d).log

# Project-specific logs
python3 main.py --config osint_detective.yaml --log ./client_osint.log
```

### Log Format
```
================================================================================
SESSION START: 2025-12-14 10:30:00
MODULE: web_bounty.yaml
================================================================================
[2025-12-14 10:31:15] Subdomain Discovery | Amass - Advanced Subdomain Enum
Command: amass enum -d example.com -o subdomains.txt
--------------------------------------------------------------------------------
[2025-12-14 10:45:22] Vulnerability Scanning | Nuclei - Template-Based Scanner
Command: nuclei -l subdomains.txt -severity critical,high,medium
--------------------------------------------------------------------------------
```

---

## 🎯 Quick Scenario Guide

### Scenario 1: Starting a Bug Bounty Hunt
```bash
tajaa-web
# → Select: Subdomain Discovery
# → Select: Amass - Advanced Subdomain Enum
# → Enter domain: target.com
# → Execute

# → Select: Vulnerability Scanning
# → Select: Nuclei - Template-Based Scanner
# → Execute on discovered subdomains
```

### Scenario 2: CTF Competition
```bash
tajaa-ctf
# → Select: Network Reconnaissance
# → Select: RustScan - Ultra Fast Port Scanner
# → Enter target_ip: 10.10.10.100
# → Execute

# → Select: Steganography & Forensics
# → Select: Binwalk - Extract Hidden Files
# → Enter file_path: ./image.png
# → Execute
```

### Scenario 3: Corporate Pentest
```bash
tajaa-ad
# → Select: SMB Enumeration
# → Select: CrackMapExec - SMB Enumeration
# → Enter credentials
# → Execute

# → Select: Active Directory Attacks
# → Select: BloodHound.py - AD Collector
# → Execute data collection
```

### Scenario 4: OSINT Investigation
```bash
tajaa-osint
# → Select: Email Intelligence
# → Select: Holehe - Email Account Finder
# → Enter email: target@company.com
# → Execute

# → Select: Social Media OSINT
# → Select: Sherlock - Username Hunter
# → Enter username: target_user
# → Execute
```

### Scenario 5: Cloud Security Audit
```bash
tajaa-cloud
# → Select: AWS Enumeration
# → Select: AWS CLI - List S3 Buckets
# → Execute (uses configured AWS credentials)

# → Select: AWS Security Audit
# → Select: Prowler - Full AWS Audit
# → Execute comprehensive scan
```

---

## 🔧 Configuration Management

### Adding a Custom Tool

Edit any module YAML file (e.g., `ctf_kit.yaml`):

```yaml
categories:
  custom_category:
    name: "My Custom Tools"
    tools:
      my_tool:
        name: "Custom Tool Name"
        description: "What this tool does"
        command: "binary_name -flag {param1} {param2}"
        params:
          - param1
          - param2
```

### Reload and Use
```bash
python3 main.py --config ctf_kit.yaml
# Your custom tool now appears in the menu!
```

---

## 🛠️ Common Tool Installation

### Kali Linux (Most tools pre-installed)
```bash
sudo apt update
sudo apt install nmap rustscan masscan gobuster nikto sqlmap metasploit-framework
```

### Additional Tools
```bash
# Web tools
sudo apt install amass subfinder nuclei wfuzz ffuf

# AD tools
sudo apt install crackmapexec bloodhound impacket-scripts

# Wireless tools
sudo apt install aircrack-ng wifite reaver

# OSINT tools
pip install sherlock-project holehe theHarvester
```

---

## 📊 Module Selection Guide

| If you need to... | Use this module |
|-------------------|-----------------|
| Scan networks quickly | 🏆 CTF Kit |
| Find subdomains | 🌐 Web Bounty |
| Test for XSS/SQLi | 🌐 Web Bounty |
| Attack Active Directory | 🏢 Network AD |
| Analyze Android APK | 📱 Mobile IoT |
| Audit AWS S3 buckets | ☁️ Cloud Auditor |
| Find email addresses | 🕵️ OSINT Detective |
| Search social media | 🕵️ OSINT Detective |
| Crack WiFi password | 📡 Wireless Radio |
| Attack Bluetooth devices | 📡 Wireless Radio |
| Escalate Linux privileges | 🔒 Post Exploit |
| Exfiltrate data | 🔒 Post Exploit |

---

## 🆘 Troubleshooting Quick Fixes

### Problem: Tool Not Found
```
⚠ Warning: 'nmap' not found
```
**Fix**: `sudo apt install nmap`

### Problem: Invalid IP Address
```
⚠ Invalid IPv4 address
```
**Fix**: Use format `192.168.1.1` (not `localhost` or `192.168.1.1/24`)

### Problem: YAML Parse Error
```
Error loading configuration
```
**Fix**: Check YAML syntax:
```bash
python3 -c "import yaml; yaml.safe_load(open('ctf_kit.yaml'))"
```

### Problem: Permission Denied
```
Permission denied
```
**Fix**: Some tools require sudo:
```bash
sudo python3 main.py --config wireless_radio.yaml
```

---

## 📚 Documentation Links

- **[README.md](README.md)** - Complete project overview
- **[CONFIG_CATALOG.md](CONFIG_CATALOG.md)** - Detailed module documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎓 Pro Tips

### Tip 1: Use Tab Completion
If you're writing a lot of commands, consider enabling shell completion for faster typing.

### Tip 2: Review Session Logs
```bash
# View today's commands
grep "$(date +%Y-%m-%d)" session_logs.txt

# View specific tool usage
grep "Nmap" session_logs.txt
```

### Tip 3: Chain Multiple Modules
```bash
# OSINT first
tajaa-osint
# Then web testing
tajaa-web
# Then exploitation
tajaa-ad
```

### Tip 4: Organize by Project
```bash
# Create project-specific log files
tajaa-web --log ./projects/company_a/web_audit.log
tajaa-osint --log ./projects/company_a/osint.log
```

### Tip 5: Customize Your Workflow
Create your own YAML module with your favorite tools!

---

## 🔒 Legal Reminder

⚠️ **Always get written authorization before security testing!**

- ✅ Legal penetration tests
- ✅ Authorized bug bounty programs  
- ✅ CTF competitions
- ✅ Your own systems
- ❌ Unauthorized hacking (ILLEGAL)

---

## 🌟 Quick Win Commands

```bash
# Test installation
python3 main.py --help

# Launch CTF module
tajaa-ctf

# Launch web bounty module with custom log
tajaa-web --log ./bug_bounty_$(date +%Y%m%d).log

# Launch OSINT with custom config location
python3 main.py --config ./configs/osint_detective.yaml

# View session history
tail -f session_logs.txt
```

---

**Happy Ethical Hacking! 🔒**

For more help, see [QUICKSTART.md](QUICKSTART.md) or open an issue on GitHub.

