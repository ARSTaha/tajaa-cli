# Quick Start Guide

Get started with Tajaa CLI in 5 minutes.

## Installation

```bash
# Clone repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 test_components.py
```

**Important:** Always activate the virtual environment before using Tajaa CLI:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

## Basic Usage

```bash
# Run with default config
python3 main.py

# Run with specific module
python3 main.py --config configs/02_ctf_kit.yaml
```

## Available Modules

| Config File | Domain | Tools |
|------------|--------|-------|
| `01_commands.yaml` | General Pentesting | 60+ |
| `02_ctf_kit.yaml` | CTF Competitions | 150+ |
| `03_web_bounty.yaml` | Web Security | 80+ |
| `04_network_ad.yaml` | Active Directory | 65+ |
| `05_mobile_iot.yaml` | Mobile & IoT | 60+ |
| `06_cloud_auditor.yaml` | Cloud Security | 75+ |
| `07_osint_detective.yaml` | OSINT | 60+ |
| `08_wireless_radio.yaml` | Wireless | 45+ |
| `09_post_exploit.yaml` | Post-Exploitation | 75+ |

## Quick Examples

### CTF Challenge
```bash
python3 main.py --config configs/02_ctf_kit.yaml
# Select: Steganography → Binwalk
# Enter file path
# Command auto-copied to clipboard
```

### Web Pentest
```bash
python3 main.py --config configs/03_web_bounty.yaml
# Select: Directory Enumeration → Gobuster
# Enter target URL
# Scan starts automatically
```

### Cloud Audit
```bash
python3 main.py --config configs/06_cloud_auditor.yaml
# First run: AWS CLI - Check Authentication
# Then: List S3 Buckets, EC2 Instances, etc.
```

## Optional Arsenal

Install CyberChef, payloads, and wordlists:

```bash
chmod +x install_arsenal.sh
sudo ./install_arsenal.sh
```

This installs:
- CyberChef (local HTML)
- LinPEAS, WinPEAS, pspy64
- SecLists wordlists

## Creating Aliases

Add to `~/.bashrc` or `~/.zshrc` (adjust path as needed):

```bash
# Tajaa CLI Aliases (with virtual environment)
alias tajaa='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py'
alias tajaa-ctf='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/02_ctf_kit.yaml'
alias tajaa-web='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/03_web_bounty.yaml'
alias tajaa-cloud='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/06_cloud_auditor.yaml'
```

Then reload: `source ~/.bashrc` or `source ~/.zshrc`

## Tips

- All commands are logged to `session_logs.txt`
- Commands auto-copy to clipboard
- Use Ctrl+C to cancel anytime
- Missing tools show warnings but continue

## Documentation

- **README.md** - Full documentation
- **SECURITY.md** - Security features
- **EXAMPLES.md** - Usage examples
- **ARCHITECTURE.md** - Technical details
- **CHANGELOG.md** - Version history

## Support

Report issues: https://github.com/ARSTaha/tajaa-cli/issues

---

**Author:** Tajaa  
**License:** MIT

