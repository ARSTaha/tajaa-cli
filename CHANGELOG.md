# Changelog

All notable changes to Tajaa CLI will be documented in this file.

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
