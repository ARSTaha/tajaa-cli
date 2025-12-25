# ⚔️ Tajaa CLI - The Ultimate Cyber Security Framework

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/ARSTaha/tajaa-cli)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux-557C94.svg)](https://www.kali.org/)
[![Tools](https://img.shields.io/badge/tools-500+-red.svg)](CONFIG_CATALOG.md)

**The most comprehensive pentesting framework ever created.** 500+ battle-tested security tools across 9 specialized domains, organized for real-world scenarios.

> *"One framework to rule them all."*

---

## Why Tajaa CLI?

Tajaa CLI transforms how security professionals work. No more searching through bookmarks, remembering complex syntax, or maintaining scattered scripts. Everything you need is organized, validated, and ready to execute.

### What Makes It Different

- **🎯 CTF-Optimized** - 150+ CTF-specific tools including the legendary `nmap -sC -sV -p-` and complete exploitation chains
- **🔒 Security-First** - All inputs sanitized with `shlex.quote()`, command injection protection built-in
- **⚡ Zero Friction** - Select tool, enter parameters, execute. Commands auto-copied to clipboard
- **📚 Self-Documenting** - Session logging with timestamps for writeups and reports
- **🧩 Modular Design** - 9 specialized configs that load instantly, switch contexts in seconds

### Core Features

- **500+ Pre-configured Tools** - Every tool you need, perfectly parameterized
- **Smart Input Validation** - IP addresses, domains, ports, file paths all validated
- **Dependency Checking** - Warns about missing tools before execution
- **Rich Terminal UI** - Beautiful interface powered by Rich library
- **Session Logging** - Every command logged with timestamps

---

## The 9 Modules

| Module | Config File | Tools | Primary Use Cases |
|--------|------------|-------|-------------------|
| **⚔️ General** | `01_commands.yaml` | 60+ | General pentesting commands |
| **🏆 CTF Kit** | `02_ctf_kit.yaml` | 150+ | **The ultimate CTF toolkit** - Nmap arsenal, stego, crypto, pwn, privesc |
| **🌐 Web Bounty** | `03_web_bounty.yaml` | 80+ | Subdomain enum, SQLi, XSS, API fuzzing, CMS exploitation |
| **🏢 Network AD** | `04_network_ad.yaml` | 65+ | SMB, Kerberos, LDAP, lateral movement, domain compromise |
| **📱 Mobile IoT** | `05_mobile_iot.yaml` | 60+ | APK analysis, iOS RE, firmware extraction, dynamic analysis |
| **☁️ Cloud Auditor** | `06_cloud_auditor.yaml` | 75+ | AWS/Azure/GCP enum, S3 testing, container security |
| **🕵️ OSINT Detective** | `07_osint_detective.yaml` | 60+ | Passive recon, social media OSINT, email intel |
| **📡 Wireless Radio** | `08_wireless_radio.yaml` | 45+ | WiFi cracking, Bluetooth, evil twin, SDR, NFC/RFID |
| **🔒 Post Exploit** | `09_post_exploit.yaml` | 75+ | Privilege escalation, persistence, data exfil |

**→ See [CONFIG_CATALOG.md](CONFIG_CATALOG.md) for complete tool listings and detailed documentation**

---

## 🚀 Quick Start Installation

> **📘 New to Kali Linux?** See [INSTALL_KALI.md](INSTALL_KALI.md) for a complete step-by-step guide with troubleshooting.

### Prerequisites

- **Operating System**: Kali Linux, Parrot OS, or any Linux distribution
- **Python**: 3.8 or higher
- **Security Tools** - Install as needed (nmap, metasploit, etc.)

### Installation

**Option 1: Automated Installation (Recommended)**

```bash
# Clone repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Run installer (handles virtual environment automatically)
chmod +x install.sh
./install.sh

# Activate virtual environment (REQUIRED)
source .venv/bin/activate

# Run the framework
python3 main.py
```

**Option 2: Manual Installation**

```bash
# Clone repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Create virtual environment (REQUIRED on modern Kali/Debian)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the framework
python3 main.py
```

**⚠️ IMPORTANT:** Modern Kali Linux (2023.1+) uses PEP 668 externally-managed Python environments. You **MUST** activate the virtual environment before running the framework:

```bash
source .venv/bin/activate
```

If you see `ModuleNotFoundError: No module named 'typer'`, you forgot to activate the virtual environment.

**Having installation issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common solutions.

### Optional: Create Aliases

Add to your `~/.bashrc` or `~/.zshrc` (replace `~/tajaa-cli` with your actual path):

```bash
# Tajaa CLI Aliases (automatically activates venv)
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

Then reload your shell: `source ~/.bashrc` or `source ~/.zshrc`

---

## Usage

**Always activate the virtual environment first:**

```bash
cd ~/tajaa-cli
source .venv/bin/activate
```

### Basic Usage

```bash
python3 main.py
```

### Load Specific Module

```bash
# CTF toolkit
python3 main.py --config configs/02_ctf_kit.yaml

# Web security
python3 main.py --config configs/03_web_bounty.yaml

# Cloud auditing
python3 main.py --config configs/06_cloud_auditor.yaml

# Post-exploitation
python3 main.py --config configs/09_post_exploit.yaml
```

### Using Aliases (if configured)

```bash
tajaa          # Default module (General pentesting)
tajaa-ctf      # CTF toolkit
tajaa-web      # Web security
tajaa-ad       # Active Directory
tajaa-mobile   # Mobile & IoT
tajaa-cloud    # Cloud auditing
tajaa-osint    # OSINT operations
tajaa-wireless # Wireless attacks
tajaa-post     # Post-exploitation
```

---

## 📂 Project Structure

```
tajaa-cli/
├── main.py                    # Main framework (OOP architecture)
├── requirements.txt           # Python dependencies
├── install.sh                 # Automated installer
├── install_arsenal.sh         # Optional tools installer (CyberChef, payloads)
│
├── configs/                   # Configuration modules
│   ├── 01_commands.yaml       # General pentesting (60+ tools)
│   ├── 02_ctf_kit.yaml        # CTF competitions (167 tools) ⭐
│   ├── 03_web_bounty.yaml     # Web security (80+ tools)
│   ├── 04_network_ad.yaml     # Active Directory (65+ tools)
│   ├── 05_mobile_iot.yaml     # Mobile & IoT (60+ tools)
│   ├── 06_cloud_auditor.yaml  # Cloud security (75+ tools)
│   ├── 07_osint_detective.yaml # OSINT (60+ tools)
│   ├── 08_wireless_radio.yaml # Wireless (45+ tools)
│   └── 09_post_exploit.yaml   # Post-exploitation (75+ tools)
│
├── README.md                  # Main documentation
├── INSTALL_KALI.md            # Step-by-step Kali installation guide
├── QUICKSTART.md              # Getting started guide
├── CONFIG_CATALOG.md          # Complete tool catalog
├── TROUBLESHOOTING.md         # Installation & usage issues
├── CHANGELOG.md               # Version history
├── ARCHITECTURE.md            # Technical architecture
├── EXAMPLES.md                # Usage examples
├── SECURITY.md                # Security features
├── QUICK_REFERENCE.md         # Command reference
├── LICENSE                    # MIT License
│
├── test_components.py         # Unit tests
├── test_security.py           # Security tests
└── verify_security.py         # Quick verification
```

---

## 🏗️ Architecture Overview

### Clean OOP Design

```
TajaaCLI (Main Orchestrator)
├── ConfigLoader (Module loading & parsing)
├── InputValidator (Parameter validation)
├── DependencyChecker (Tool availability)
├── SessionLogger (Audit trail logging)
├── CommandExecutor (Command execution)
└── UIManager (Rich terminal interface)
```

### Design Principles

- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: Components receive dependencies via constructor
- **Type Hinting**: Full typing coverage for IDE support
- **Modular Configuration**: Separate YAML files per domain
- **Error Handling**: Graceful errors at every level

---

## 📝 Configuration System

### Module Configuration Format

Each YAML module follows this structure:

```yaml
categories:
  category_name:
    name: "Display Name"
    tools:
      tool_key:
        name: "Tool Display Name"
        description: "What this tool does"
        command: "binary_name -flag {param1} {param2}"
        params:
          - param1
          - param2
```

### Adding Custom Tools

1. Edit any module YAML file
2. Follow the structure above
3. Reload Tajaa CLI
4. Your tool appears in the menu!

### Parameter Validation

- **`target_ip`**: Automatic IPv4 validation
- **`port`**: Validates 1-65535 range
- **`domain`**: Non-empty string validation
- **Custom params**: Define your own validators

---

## 🎯 Use Case Examples

### Scenario 1: Bug Bounty Hunt
```bash
# Load web bounty arsenal
tajaa-web

# Run subdomain enumeration
# → Select: Subdomain Discovery
# → Select: Amass - Advanced Subdomain Enum
# → Enter domain: example.com
# → 500+ subdomains discovered

# Run vulnerability scan
# → Select: Vulnerability Scanning
# → Select: Nuclei - Template-Based Scanner
# → Auto-scans all discovered subdomains
```

### Scenario 2: Corporate Pentest
```bash
# Load Active Directory module
tajaa-ad

# Enumerate SMB shares
# → Select: SMB Enumeration
# → Select: CrackMapExec - SMB Enumeration
# → Enter target IP: 10.10.10.100

# Kerberoast attack
# → Select: Active Directory Attacks
# → Select: GetUserSPNs.py - Kerberoasting
```

### Scenario 3: OSINT Investigation
```bash
# Load OSINT module
tajaa-osint

# Search for email leaks
# → Select: Email Intelligence
# → Select: Holehe - Email Account Finder
# → Enter email: target@company.com

# Find social media profiles
# → Select: Social Media OSINT
# → Select: Sherlock - Username Hunter
```

---

## 🛡️ Security & Legal Notice

⚠️ **WARNING**: This framework is for **authorized security testing ONLY**!

### Legal Requirements:
- ✅ Get written permission before testing
- ✅ Stay within authorized scope
- ✅ Follow responsible disclosure
- ✅ Respect privacy and legal boundaries
- ❌ Never attack systems without authorization

### Ethical Use:
- For security research and education
- Authorized penetration testing
- Bug bounty programs
- CTF competitions
- Academic purposes

**Misuse of this tool is illegal and unethical.**

---

## 📊 Example Session Log

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

## 🤝 Contributing

Contributions welcome! Help us expand the framework:

1. Fork: https://github.com/ARSTaha/tajaa-cli
2. Create feature branch: `git checkout -b feature/new-module`
3. Add your tools/modules following the YAML structure
4. Add tests and documentation
5. Submit pull request

**Ideas for Contributions:**
- New security tool integrations
- Additional specialized modules
- Enhanced validation logic
- Output parsing features
- Report generation capabilities

---

## 📚 Documentation

- **[CONFIG_CATALOG.md](CONFIG_CATALOG.md)** - Complete module and tool reference
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step getting started
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎓 Learning Path

### Beginner (Weeks 1-4)
1. Start with **CTF Kit** - Learn fundamental tools
2. Practice with **OSINT Detective** - Passive techniques

### Intermediate (Weeks 5-12)
3. Master **Web Bounty** - Web application security
4. Explore **Wireless Radio** - Wireless attack vectors

### Advanced (Weeks 13-24)
5. Study **Network AD** - Enterprise environments
6. Learn **Cloud Auditor** - Cloud security

### Expert (Weeks 25+)
7. Implement **Post Exploit** - Advanced persistence
8. Combine **Mobile IoT** - Embedded systems

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author

**Tajaa**
- GitHub: [@ARSTaha](https://github.com/ARSTaha)

---

## 🙏 Acknowledgments

- Kali Linux Team
- Python Rich Library
- InquirerPy Project
- The InfoSec Community
- All Open Source Security Tool Developers

---

## 📞 Support

- **Issues**: https://github.com/ARSTaha/tajaa-cli/issues
- **Discussions**: https://github.com/ARSTaha/tajaa-cli/discussions
- **Documentation**: See docs folder

---

## 🌟 Star History

If you find Tajaa CLI useful, please consider giving it a star ⭐!

---

**Built with ❤️ for the security community**

**Remember: With great power comes great responsibility. Use ethically! 🔒**

