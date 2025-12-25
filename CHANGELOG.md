# Changelog

All notable changes to Tajaa CLI will be documented in this file.

---

## [4.0.0] - 2025-12-25

### The Ultimate CTF Toolkit Release

This release transforms Tajaa CLI into the most comprehensive CTF toolkit ever created.

### New Features

- **167 CTF Tools** - Massive expansion of the CTF Kit module
- **15 Essential Nmap Scans** - Including the legendary `nmap -sC -sV -p- -oN scan.txt`
- **Complete Hash Cracking Arsenal** - John + Hashcat for all common hash types
- **Comprehensive Steganography Suite** - 16 tools for image, audio, and binary analysis
- **Binary Exploitation Tools** - Pattern generation, ROP gadgets, pwntools integration
- **Privilege Escalation Helpers** - LinPEAS/WinPEAS hosting with download command generators
- **18 Specialized Categories** - Organized workflow from recon to post-exploitation

### CTF Kit Categories

1. Nmap Arsenal (15 scans)
2. Lightning Fast Scanners (RustScan, Masscan)
3. Service-Specific Enumeration (SMB, SNMP, LDAP, NFS)
4. Web Directory & Content Discovery
5. Web Technology Analysis
6. Web Vulnerability Exploitation (SQLi, XSS, LFI, SSRF)
7. CMS Exploitation (WordPress, Drupal, Joomla)
8. Hash Identification & Cracking
9. Online Brute Force Attacks
10. Steganography Analysis
11. Audio Steganography
12. Cryptography Tools
13. Binary Analysis
14. Binary Exploitation
15. Privilege Escalation Enumeration
16. Reverse Shells & Listeners
17. OSINT & Information Gathering
18. Quick CTF Utilities

### Changed

- Version bumped to 4.0.0
- Rebranded as "The Ultimate Cyber Security Framework"
- Tool count increased from 480+ to 500+
- Updated documentation and CONFIG_CATALOG.md

---

## [3.1.0] - 2025-12-19

### Security Fixes

- **Fixed command injection vulnerability** - All user inputs now sanitized with `shlex.quote()`
- **Added dangerous input detection** - Pattern matching for shell metacharacters
- **Enhanced URL validation** - Prevents protocol duplication (http://http://...)
- **Improved file path security** - Blocks directory traversal attempts

### Features

- **Hostname support** - Accept both IPs and hostnames (scanme.nmap.org, target.htb)
- **Smart dependency checker** - Skips wrapper commands (sudo, proxychains) for accurate tool detection
- **Wordlist path aliases** - Multi-path fallback for different Linux distros
- **Arsenal installer** - New `install_arsenal.sh` for CyberChef, payloads, and wordlists
- **Payload delivery mode** - Post-exploitation tools now generate download commands

### Changed

- Updated configs to use payload server approach for exploit tools
- Replaced broken CyberChef CLI with local HTML version
- Added AWS authentication check in cloud auditor module

---

## [3.0.0] - 2025-12-14

### Added

- 8 specialized configuration modules (CTF, Web, AD, Mobile, Cloud, OSINT, Wireless, Post-Exploit)
- 480+ total security tools across 66 categories
- Module-based architecture with `--config` flag
- Cloud security domain (AWS/Azure/GCP)
- OSINT capabilities
- Mobile & IoT security tools
- Wireless & RF security tools
- Post-exploitation toolkit

### Changed

- **BREAKING**: Configuration files moved to `configs/` directory
- Rebranded as "Modular Cyber Security Framework"
- Updated banner and version to 3.0.0
- Enhanced documentation for modular workflow

---

## [2.0.0] - 2025-12-14

### Added

- Complete OOP refactor with SOLID principles
- ConfigLoader, InputValidator, DependencyChecker classes
- SessionLogger for automatic command logging
- Rich terminal UI with progress bars
- Clipboard integration
- Type hints and comprehensive docstrings
- 22+ pre-configured tools across 6 categories

### Changed

- Migrated from procedural to object-oriented architecture
- Enhanced YAML configuration format
- Improved error handling and user experience

---

## [1.0.0] - Initial Release

- Basic command-line tool with simple tool execution

---

**Author:** Tajaa  
**License:** MIT
