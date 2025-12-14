# 🚀 Tajaa CLI - Quick Start Guide

**Welcome to Tajaa CLI v3.0.0 - The Ultimate Modular Cyber Security Framework!**

This guide will get you up and running in under 5 minutes.

---

## 📦 Installation (5 Minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli
```

### Step 2: Create Virtual Environment (Recommended)
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
Total: 4/4 tests passed ✓
```

### Step 5: Test the Framework
```bash
python3 main.py --help
```

---

## 🎯 Choosing Your Module

**This is the power of Tajaa CLI 3.0!** Instead of one generic pentesting tool, you now have **8 specialized modules** for different scenarios.

### Available Modules

| Module | Config File | When to Use |
|--------|------------|-------------|
| 🏆 **CTF Kit** | `configs/02_ctf_kit.yaml` | Competitions, challenges, rapid assessments |
| 🌐 **Web Bounty** | `configs/03_web_bounty.yaml` | Bug bounty hunting, web app pentesting |
| 🏢 **Network AD** | `configs/04_network_ad.yaml` | Corporate networks, Active Directory |
| 📱 **Mobile IoT** | `configs/05_mobile_iot.yaml` | Mobile apps, firmware reverse engineering |
| ☁️ **Cloud Auditor** | `configs/06_cloud_auditor.yaml` | AWS/Azure/GCP security audits |
| 🕵️ **OSINT Detective** | `configs/07_osint_detective.yaml` | Intelligence gathering, reconnaissance |
| 📡 **Wireless Radio** | `configs/08_wireless_radio.yaml` | WiFi/Bluetooth/SDR/RFID security |
| 🔒 **Post Exploit** | `configs/09_post_exploit.yaml` | After initial access, persistence |

---

## 🎮 Running the Framework

### Method 1: Default Configuration
```bash
python3 main.py
```

### Method 2: Specific Module (Recommended)
```bash
# CTF Competition Mode
python3 main.py --config configs/02_ctf_kit.yaml

# Bug Bounty Mode
python3 main.py --config configs/03_web_bounty.yaml

# OSINT Investigation Mode
python3 main.py --config configs/07_osint_detective.yaml

# Cloud Security Audit Mode
python3 main.py --config configs/06_cloud_auditor.yaml
```

### Method 3: With Custom Logs
```bash
# Date-stamped engagement logs
python3 main.py --config configs/04_network_ad.yaml --log ./pentest_$(date +%Y%m%d).log
```

---

## 🎯 Quick Examples by Scenario

### Scenario 1: You're in a CTF Competition
```bash
# Load CTF arsenal
python3 main.py --config configs/02_ctf_kit.yaml

# You get instant access to:
# - Fast port scanners (RustScan, Masscan)
# - Steganography tools (Binwalk, Steghide, Zsteg)
# - Password crackers (John, Hashcat)
# - Binary analysis (Radare2, Ghidra)
# - Crypto tools
```

### Scenario 2: You're Doing Bug Bounty
```bash
# Load web bounty tools
python3 main.py --config configs/03_web_bounty.yaml

# You get instant access to:
# - Subdomain enumeration (Amass, Subfinder)
# - Vulnerability scanners (Nuclei, Nikto)
# - XSS testing (Dalfox, XSStrike)
# - SQL injection (SQLmap)
# - API fuzzing (Arjun, Ffuf)
```

### Scenario 3: Corporate Pentest
```bash
# Load AD pentesting tools
python3 main.py --config configs/04_network_ad.yaml

# You get instant access to:
# - SMB enumeration (CrackMapExec, Enum4Linux-ng)
# - Kerberos attacks (Kerbrute, Rubeus)
# - Lateral movement (Impacket suite)
# - Credential harvesting
```

### Scenario 4: OSINT Investigation
```bash
# Load OSINT tools
python3 main.py --config configs/07_osint_detective.yaml

# You get instant access to:
# - Email intelligence (Holehe, h8mail)
# - Social media OSINT (Sherlock)
# - Domain intelligence (TheHarvester)
# - Shodan searches
```

---

## 📖 Usage Flow (Your First Run)

### 1. Start the Application
```bash
python3 main.py --config ctf_kit.yaml
```

### 2. You'll See the Banner
```
  _______ ___    ___ ___    ___ 
 |_   _  |   |  |   |   |  |   |
   | | | |   |  |   |   |  |   |
   | | | |   |  |   |   |  |   |
   | | | |   |_ |   |   |_ |   |
   |_| |_|\____|/    \____||___|

╔══════════════════════════════════════════════════╗
║  Modular Cyber Security Framework                ║
║  Version 3.0.0 | 8 Specialized Domains | 480+ Tools ║
╚══════════════════════════════════════════════════╝
```

### 3. Select a Category
Use arrow keys to navigate:
```
Available Categories
┌─────┬────────────────────────────┬─────────────┐
│  #  │ Category                   │ Tools Count │
├─────┼────────────────────────────┼─────────────┤
│  1  │ Network Reconnaissance     │      4      │
│  2  │ Steganography & Forensics  │      6      │
│  3  │ Password Cracking          │      6      │
│  4  │ Cryptography Tools         │      4      │
│  5  │ Reverse Shells & Payloads  │      5      │
│  6  │ Quick Web Enumeration      │      4      │
│  7  │ Binary & Reverse Engineering│     5      │
└─────┴────────────────────────────┴─────────────┘

? Select a category: [Use arrows]
❯ Network Reconnaissance
  Steganography & Forensics
  Password Cracking
  [Exit]
```

### 4. Select a Tool
Example: Selecting "Network Reconnaissance" shows:
```
Network Reconnaissance Tools
? Select a tool: [Use arrows]

❯ RustScan - Ultra Fast Port Scanner
  └─ Modern port scanner that feeds results to Nmap. Scans all 65k ports in seconds.

  Nmap - Fast Scan (Top 1000)
  └─ Quick scan of most common 1000 ports with service detection

  Nmap - Vulnerability Scan
  └─ Deep vulnerability detection using NSE scripts

  Masscan - Mass IP Scanner
  └─ Fastest port scanner for entire networks (requires sudo)

  [← Back to Categories]
```

### 5. Enter Parameters
The framework validates your input automatically:

**Valid Input:**
```
? Enter target_ip: 192.168.1.1 ✓
```

**Invalid Input:**
```
? Enter target_ip: 999.999.999.999 ✗
⚠ Invalid IPv4 address. Please use format: xxx.xxx.xxx.xxx
? Enter target_ip: 
```

### 6. Review Generated Command
```
╔══════════════════════════════════════════════════╗
║  Generated Command                                ║
╚══════════════════════════════════════════════════╝

rustscan -a 192.168.1.1 -- -A -sC

? Do you want to execute this command? (y/n): 
```

### 7. Execute or Copy
- **Press `y`**: Command executes with live progress indicator
- **Press `n`**: Command is copied to clipboard for manual execution

### 8. Check Session Log
All commands are logged:
```bash
cat session_logs.txt
```

Output:
```
================================================================================
SESSION START: 2025-12-14 10:30:00
MODULE: ctf_kit.yaml
================================================================================
[2025-12-14 10:31:15] Network Reconnaissance | RustScan - Ultra Fast Port Scanner
Command: rustscan -a 192.168.1.1 -- -A -sC
--------------------------------------------------------------------------------
```

---

## ⚡ Quick Copy-Paste Commands

### Set Up Aliases (One-Time Setup)
```bash
# Add to ~/.bashrc or ~/.zshrc
cat >> ~/.bashrc << 'EOF'
# Tajaa CLI Aliases
alias tajaa="python3 ~/tajaa-cli/main.py"
alias tajaa-ctf="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/ctf_kit.yaml"
alias tajaa-web="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/web_bounty.yaml"
alias tajaa-ad="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/network_ad.yaml"
alias tajaa-mobile="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/mobile_iot.yaml"
alias tajaa-cloud="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/cloud_auditor.yaml"
alias tajaa-osint="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/osint_detective.yaml"
alias tajaa-wireless="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/wireless_radio.yaml"
alias tajaa-post="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/post_exploit.yaml"
EOF

# Reload shell
source ~/.bashrc
```

### Now Use Short Commands
```bash
# Instead of: python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/ctf_kit.yaml
# Just type:
tajaa-ctf

# Instead of: python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/web_bounty.yaml
# Just type:
tajaa-web
```

---

## 🔧 Directory Organization (Recommended)

### Option 1: Keep YAMLs in Root (Default)
```
tajaa-cli/
├── main.py
├── ctf_kit.yaml
├── web_bounty.yaml
└── ...
```

Run with:
```bash
python3 main.py --config ctf_kit.yaml
```

### Option 2: Organize in configs/ Folder
```bash
# Create configs directory
mkdir -p configs

# Move all module YAMLs
mv *.yaml configs/
mv configs/commands.yaml ./  # Keep default in root

# Your structure:
tajaa-cli/
├── main.py
├── commands.yaml
└── configs/
    ├── ctf_kit.yaml
    ├── web_bounty.yaml
    ├── network_ad.yaml
    └── ...
```

Run with:
```bash
python3 main.py --config configs/ctf_kit.yaml
```

Update aliases:
```bash
alias tajaa-ctf="python3 ~/tajaa-cli/main.py --config ~/tajaa-cli/configs/ctf_kit.yaml"
```

---

## 🎓 Learning Tips

### Tip 1: Start with Your Use Case
- **Learning?** → Start with CTF Kit
- **Bug bounty?** → Start with Web Bounty
- **Corporate pentest?** → Start with Network AD
- **OSINT project?** → Start with OSINT Detective

### Tip 2: Explore One Module at a Time
Don't try to learn all 480+ tools at once. Master one module first.

### Tip 3: Read Tool Descriptions
Each tool has a description. Read them to understand when to use what.

### Tip 4: Check Session Logs
Review your logs to build muscle memory for command syntax.

### Tip 5: Customize Your Modules
Add your favorite tools to the YAML files!

---

## 🆘 Troubleshooting

### Issue: "Tool not found" Warning
```
⚠ Warning: 'nmap' not found. Please install: sudo apt install nmap
```

**Solution**: Install the required tool:
```bash
sudo apt update
sudo apt install nmap rustscan masscan
```

### Issue: Invalid IP Address
```
⚠ Invalid IPv4 address
```

**Solution**: Use correct format: `192.168.1.1` (not `192.168.1.1/24` or `localhost`)

### Issue: YAML Parsing Error
```
Error loading configuration file
```

**Solution**: Check YAML syntax with:
```bash
python3 -c "import yaml; yaml.safe_load(open('ctf_kit.yaml'))"
```

---

## 📚 Next Steps

1. **Read the Full README**: [`README.md`](README.md)
2. **Explore All Modules**: [`CONFIG_CATALOG.md`](CONFIG_CATALOG.md)
3. **Quick Reference**: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
4. **Architecture Details**: [`ARCHITECTURE.md`](ARCHITECTURE.md)

---

## 🎯 Quick Win Challenge

**Your First 5 Minutes with Tajaa CLI:**

1. Run: `tajaa-ctf` (or `python3 main.py --config ctf_kit.yaml`)
2. Navigate to: **Network Reconnaissance**
3. Select: **RustScan - Ultra Fast Port Scanner**
4. Enter target: `scanme.nmap.org` (official test target)
5. Execute and watch the magic! ✨

---

**You're ready to hack ethically! 🔒**

Need help? Check [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) or open an issue on GitHub.

