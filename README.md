# ⚔️ Tajaa CLI - Modular Cyber Security Framework

[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)](https://github.com/ARSTaha/tajaa-cli)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.kali.org/)

A modular framework for penetration testing and security assessments. Combines 480+ security tools across 8 specialized domains in a single CLI interface.

---

## What is Tajaa CLI?

Tajaa CLI is a modular penetration testing framework with clean OOP architecture. Instead of maintaining multiple scattered scripts, you get organized tool configurations that adapt to your workflow - whether you're doing CTF competitions, web pentesting, or cloud audits.

### Key Features

- **Modular Configuration** - 8 specialized YAML configs for different security domains
- **Input Validation** - Automatic validation for IPs, ports, domains, and file paths
- **Command Injection Protection** - All inputs sanitized with `shlex.quote()`
- **Session Logging** - Every command timestamped for documentation
- **Smart Dependency Checking** - Pre-execution warnings for missing tools
- **Rich Terminal UI** - Clean interface with syntax highlighting
- **Clipboard Integration** - Auto-copy commands for quick execution

---

## The 8 Modules

| Module | Config File | Tools | Primary Use Cases |
|--------|------------|-------|-------------------|
| **🏆 CTF Kit** | `ctf_kit.yaml` | 50+ | Port scanning, steganography, password cracking, binary analysis, crypto |
| **🌐 Web Bounty** | `web_bounty.yaml` | 70+ | Subdomain enum, vuln scanning, XSS/SQLi, API fuzzing, CMS exploitation |
| **🏢 Network AD** | `network_ad.yaml` | 55+ | SMB enum, Kerberos attacks, lateral movement, domain compromise |
| **📱 Mobile IoT** | `mobile_iot.yaml` | 60+ | APK analysis, iOS reverse engineering, firmware extraction, dynamic analysis |
| **☁️ Cloud Auditor** | `cloud_auditor.yaml` | 50+ | Cloud enum, S3 testing, IAM auditing, container security, metadata exploitation |
| **🕵️ OSINT Detective** | `osint_detective.yaml` | 65+ | Passive recon, social media OSINT, email intel, cert transparency |
| **📡 Wireless Radio** | `wireless_radio.yaml` | 75+ | WiFi cracking, Bluetooth attacks, evil twin, SDR, NFC/RFID |
| **🔒 Post Exploit** | `post_exploit.yaml` | 55+ | Privilege escalation, data exfil, persistence, anti-forensics |

**→ See [CONFIG_CATALOG.md](CONFIG_CATALOG.md) for complete tool listings and detailed documentation**

---

## 🚀 Quick Start Installation

### Prerequisites

- **Operating System**: Kali Linux, Parrot OS, or any Linux distribution
- **Python**: 3.8 or higher
### Requirements

- **Python 3.8+**
- **Linux** (tested on Kali Linux, Ubuntu, Parrot OS)
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

# Activate and run
source .venv/bin/activate
python3 main.py
```

**Option 2: Manual Installation**

```bash
# Clone repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Create virtual environment (required on Kali Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the framework
python3 main.py
```

**Note for Kali Linux users:** Modern Kali uses externally-managed Python environments. Always use a virtual environment as shown above to avoid system conflicts.

**Having installation issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common solutions.

### Optional: Create Aliases

Add to your `~/.bashrc`:

```bash
alias tajaa="python3 ~/tajaa-cli/main.py"
alias tajaa-ctf="tajaa --config configs/02_ctf_kit.yaml"
alias tajaa-web="tajaa --config configs/03_web_bounty.yaml"
alias tajaa-cloud="tajaa --config configs/06_cloud_auditor.yaml"
```

---

## Usage

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
tajaa-ctf      # CTF toolkit
tajaa-web      # Web security
tajaa-cloud    # Cloud auditing
tajaa-post     # Post-exploitation
```

---

## 📂 Project Structure

```
tajaa-cli/
├── main.py                    # Main framework (OOP architecture)
├── requirements.txt           # Python dependencies
├── install.sh                 # Automated installer
├── install_arsenal.sh         # Optional tools installer
│
├── configs/                   # Configuration modules
│   ├── 01_commands.yaml       # General pentesting (60+ tools)
│   ├── 02_ctf_kit.yaml        # CTF competitions (70+ tools)
│   ├── 03_web_bounty.yaml     # Web security (80+ tools)
│   ├── 04_network_ad.yaml     # Active Directory (65+ tools)
│   ├── 05_mobile_iot.yaml     # Mobile & IoT (60+ tools)
│   ├── 06_cloud_auditor.yaml  # Cloud security (75+ tools)
│   ├── 07_osint_detective.yaml # OSINT (60+ tools)
│   ├── 08_wireless_radio.yaml # Wireless (45+ tools)
│   └── 09_post_exploit.yaml   # Post-exploitation (75+ tools)
│
├── README.md                  # Main documentation
├── QUICKSTART.md              # Getting started guide
├── CONFIG_CATALOG.md          # Complete tool catalog
├── TROUBLESHOOTING.md         # Installation & usage issues
├── CHANGELOG.md               # Version history
├── ARCHITECTURE.md            # Technical architecture
├── EXAMPLES.md                # Usage examples
├── SECURITY.md                # Security features
├── LICENSE                    # MIT License
│
└── tests/
    ├── test_components.py     # Unit tests
    ├── test_security.py       # Security tests
    └── verify_security.py     # Quick verification
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

