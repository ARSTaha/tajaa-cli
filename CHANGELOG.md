# Changelog

All notable changes to the Tajaa CLI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2025-12-14

### 🎉 MAJOR RELEASE - Complete Framework Transformation

**Tajaa CLI is now "The Ultimate Modular Cyber Security Framework"** - no longer just a penetration testing tool, but a comprehensive security framework covering 8 specialized domains.

### Added

#### **Modular Architecture System**
- **8 Specialized Configuration Modules**: Complete domain-specific tool arsenals
  - `ctf_kit.yaml` - CTF & Speed Hacking (50+ tools)
  - `web_bounty.yaml` - Web Application Security (70+ tools)
  - `network_ad.yaml` - Active Directory & Windows (55+ tools)
  - `mobile_iot.yaml` - Mobile & IoT Security (60+ tools)
  - `cloud_auditor.yaml` - AWS/Azure/GCP Auditing (50+ tools)
  - `osint_detective.yaml` - OSINT & Intelligence (65+ tools)
  - `wireless_radio.yaml` - Wireless/SDR/RFID (75+ tools)
  - `post_exploit.yaml` - Post-Exploitation (55+ tools)

#### **New Security Domains**
- **Cloud Security**: AWS, Azure, GCP enumeration and auditing tools
- **OSINT Capabilities**: Passive reconnaissance, social media intel, email intelligence
- **Mobile Security**: Android APK analysis, iOS reverse engineering, firmware extraction
- **Wireless Security**: WiFi cracking, Bluetooth attacks, SDR, RFID/NFC
- **Post-Exploitation**: Privilege escalation, data exfiltration, persistence mechanisms

#### **Documentation**
- **CONFIG_CATALOG.md**: Complete reference for all 8 modules and 480+ tools
- **DELIVERY_SUMMARY.md**: Comprehensive delivery documentation
- **Updated README.md**: Reflects modular framework architecture
- **Updated QUICKSTART.md**: Module selection guide and workflow
- **Updated QUICK_REFERENCE.md**: Module-based command patterns

#### **Tools Coverage**
- **480+ Total Tools**: Expanded from 22 to 480+ security tools
- **66 Categories**: Organized across 8 specialized domains
- **Complete Tool Chains**: Full workflow support for each security domain

### Changed

#### **Rebranding**
- **From**: "Professional Penetration Testing Command Manager"
- **To**: "The Ultimate Modular Cyber Security Framework"

#### **Configuration Architecture**
- **BREAKING CHANGE**: All YAML configuration files moved to `configs/` directory
- **Numbered Prefixes**: Config files now use numbered prefixes (01-09) for logical ordering
  - `01_commands.yaml` - Default/General Pentest (replaces `commands.yaml`)
  - `02_ctf_kit.yaml` - CTF & Competitions
  - `03_web_bounty.yaml` - Web Application Security
  - `04_network_ad.yaml` - Active Directory & Corporate
  - `05_mobile_iot.yaml` - Mobile & IoT Security
  - `06_cloud_auditor.yaml` - Cloud Security Auditing
  - `07_osint_detective.yaml` - OSINT & Intelligence
  - `08_wireless_radio.yaml` - Wireless & RF Security
  - `09_post_exploit.yaml` - Post-Exploitation
- **Default Config Path**: Now points to `configs/01_commands.yaml`
- **See MIGRATION.md**: Complete migration guide for upgrading from v2.x

#### **Documentation Updates**
- All documentation updated to reference `configs/` directory structure
- Updated README.md, QUICKSTART.md, QUICK_REFERENCE.md with new paths
- Added `configs/README.md` with module descriptions and usage guide
- Added `MIGRATION.md` with upgrade instructions
- **To**: "The Ultimate Modular Cyber Security Framework"
- **Positioning**: Multi-domain security platform vs. single-purpose pentesting tool

#### **Architecture**
- **Modular Configuration**: `--config` flag now loads specialized modules
- **Module-Based Workflow**: Users select domain-specific toolsets
- **Scalable Design**: Easy to add new domains and tools

#### **User Experience**
- **Banner Updated**: Now shows "Modular Cyber Security Framework" and "8 Specialized Domains | 480+ Tools"
- **Help Text**: Updated CLI help to reflect modular nature
- **Config Option**: Enhanced help text mentions specific module examples
- **Version**: Updated from 2.0.0 to 3.0.0

#### **Documentation**
- **README.md**: Complete rewrite emphasizing modularity
- **QUICKSTART.md**: Added module selection guide
- **QUICK_REFERENCE.md**: Module-based command patterns and scenario guide

### Improved

#### **Flexibility**
- Users can now switch between specialized domains instantly
- Each module optimized for specific use cases
- No more bloated single configuration

#### **Organization**
- Tools grouped by security domain and use case
- Clear separation: CTF vs. Corporate vs. Cloud vs. OSINT
- Easy to find the right tool for the right job

#### **Scalability**
- Framework can easily accommodate new security domains
- Simple YAML-based module addition
- Community can contribute domain-specific modules

### Technical Details

#### **Module Structure**
```
Each module contains:
- 5-12 specialized categories
- 50-75 curated security tools
- Domain-specific workflows
- Optimized for specific scenarios
```

#### **Command Patterns**
```bash
# Old (2.0.0)
python3 main.py --config commands.yaml

# New (3.0.0)
python3 main.py --config ctf_kit.yaml
python3 main.py --config web_bounty.yaml
python3 main.py --config osint_detective.yaml
```

---

## [2.0.0] - 2025-12-14

### Added
- **Complete OOP Refactor**: Migrated from procedural to object-oriented architecture
- **ConfigLoader Class**: YAML configuration loading with validation
- **InputValidator Class**: Smart validation for IPv4 addresses and port numbers
- **DependencyChecker Class**: Automatic tool availability checking
- **SessionLogger Class**: Automatic command logging with timestamps
- **CommandExecutor Class**: Robust command execution with progress indicators
- **UIManager Class**: Centralized UI management
- **TajaaCLI Class**: Main orchestrator class
- **Type Hints**: Full typing coverage across all functions and methods
- **Google-Style Docstrings**: Comprehensive documentation for all classes and methods
- **Rich Progress Bars**: Visual feedback during command execution
- **Clipboard Integration**: Auto-copy generated commands
- **Graceful Error Handling**: KeyboardInterrupt handling throughout
- **SOLID Principles**: Clean architecture following best practices

### Changed
- **Configuration Format**: Enhanced YAML with description fields for each tool
- **User Experience**: Improved UI with Rich tables and panels
- **Error Messages**: More descriptive and user-friendly error reporting
- **Menu System**: Switched to InquirerPy for better interactive experience

### Features
- 6 pentesting categories
- 22+ pre-configured tools
- IPv4 address validation
- Port number validation (1-65535)
- Automatic session logging
- Tool dependency warnings
- Command history tracking
- Beautiful ASCII art banner
- Interactive menu navigation

### Technical Improvements
- Separation of concerns with dedicated classes
- Dependency injection pattern
- Comprehensive type hints
- Error handling at every level
- Modular, extensible design
- Production-ready code quality

### Documentation
- README.md: Comprehensive project overview
- QUICKSTART.md: Step-by-step getting started guide
- ARCHITECTURE.md: Detailed architecture documentation
- LICENSE: MIT license with security disclaimer
- requirements.txt: All Python dependencies
- .gitignore: Proper Git ignore configuration

### Testing
- test_components.py: Automated component tests
- 4/4 passing tests for all core components

### Categories & Tools

#### Reconnaissance (5 tools)
- Nmap Quick Scan
- Nmap Full Port Scan
- Nmap Vulnerability Scan
- RustScan
- WhatWeb

#### Web Application Attacks (4 tools)
- Gobuster Directory Brute Force
- Nikto Web Scanner
- SQLMap SQL Injection
- Wfuzz Web Fuzzer

#### Exploitation (3 tools)
- Metasploit DB Nmap
- SearchSploit
- Hydra SSH Brute Force

#### Network Analysis (3 tools)
- NetDiscover
- ARP-Scan
- TCPDump

#### Service Enumeration (4 tools)
- Enum4Linux
- SMBClient
- LDAP Search
- SNMP Walk

#### Wireless Attacks (3 tools)
- Airmon-ng Monitor Mode
- Airodump-ng Wireless Capture
- Wash WPS Detection

---

## [1.0.0] - Initial Release

### Initial Release
- Basic command-line tool
- Simple tool execution
- Basic configuration
- Limited tool coverage
- Procedural code structure

---

## Release Notes

### Version 3.0.0 - The Modular Revolution

This is a **transformational release** that redefines what Tajaa CLI is:

**For Security Professionals:**
- No more one-size-fits-all approach
- 8 specialized domains covering your entire workflow
- CTF to corporate, cloud to wireless, OSINT to post-exploitation
- 480+ tools at your fingertips
- Switch contexts instantly with module-based architecture

**For Bug Bounty Hunters:**
- Dedicated `web_bounty.yaml` module with 70+ web testing tools
- Complete workflow: subdomain enum → vulnerability scanning → exploitation
- Integrated API testing, XSS detection, SQL injection, CMS exploitation

**For Red Team Operators:**
- `network_ad.yaml` for Active Directory attacks
- `post_exploit.yaml` for persistence and lateral movement
- Complete enterprise penetration testing toolkit

**For Cloud Security Engineers:**
- `cloud_auditor.yaml` for AWS/Azure/GCP auditing
- S3 bucket testing, IAM analysis, container security
- Compliance and security audit automation

**For OSINT Investigators:**
- `osint_detective.yaml` with 65+ intelligence tools
- Email intel, social media OSINT, domain intelligence
- Completely passive reconnaissance capabilities

**For Wireless Security Researchers:**
- `wireless_radio.yaml` with 75+ wireless tools
- WiFi, Bluetooth, SDR, RFID/NFC coverage
- Evil twin attacks, packet analysis, radio frequency hacking

**For Mobile Security Analysts:**
- `mobile_iot.yaml` for Android/iOS and firmware analysis
- APK decompilation, dynamic analysis, hardware interfacing
- Complete mobile security testing workflow

**For CTF Players:**
- `ctf_kit.yaml` optimized for speed and competitions
- Steganography, crypto, binary analysis, password cracking
- Everything you need for rapid-fire CTF challenges

**Migration from 2.x:**
- Your existing `commands.yaml` still works (backward compatible)
- Explore new modules with `--config <module_file>`
- Update aliases to use module-specific configurations

**Known Issues:**
- None reported

**Future Roadmap:**
- Plugin system for community modules
- Output parsing and correlation
- Automated report generation
- Integration with vulnerability databases
- Multi-target campaign management

---

## Version Comparison

| Feature | v1.0.0 | v2.0.0 | v3.0.0 |
|---------|--------|--------|--------|
| Architecture | Procedural | OOP | Modular OOP |
| Tool Count | ~15 | 22 | 480+ |
| Domains | 1 (Pentesting) | 1 (Pentesting) | 8 (Multi-domain) |
| Modules | 0 | 0 | 8 |
| Configuration | Basic | Enhanced YAML | Modular YAML |
| Use Cases | Generic | Pentesting | CTF, Web, AD, Mobile, Cloud, OSINT, Wireless, Post-Exploit |

---

## Contributing

See README.md for contribution guidelines.

Want to add a new security domain? Create a new YAML module and submit a PR!

---

## Support

- **Issues**: https://github.com/ARSTaha/tajaa-cli/issues
- **Discussions**: https://github.com/ARSTaha/tajaa-cli/discussions
- **Documentation**: [CONFIG_CATALOG.md](CONFIG_CATALOG.md)

---

**Built with ❤️ for the security community**

