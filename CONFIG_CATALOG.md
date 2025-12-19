# Configuration Catalog - Tajaa CLI

Complete reference for all 9 configuration modules and 480+ security tools.

**Author:** Tajaa  
**Version:** 3.1.0  
**Last Updated:** December 19, 2025

---

## Table of Contents

1. [01_commands.yaml](#1-01_commandsyaml---general-pentesting) - General Pentesting (60+ tools)
2. [02_ctf_kit.yaml](#2-02_ctf_kityaml---ctf-competitions) - CTF Competitions (70+ tools)
3. [03_web_bounty.yaml](#3-03_web_bountyyaml---web-security) - Web Security (80+ tools)
4. [04_network_ad.yaml](#4-04_network_adyaml---active-directory) - Active Directory (65+ tools)
5. [05_mobile_iot.yaml](#5-05_mobile_iotyaml---mobile--iot) - Mobile & IoT (60+ tools)
6. [06_cloud_auditor.yaml](#6-06_cloud_auditoryaml---cloud-security) - Cloud Security (75+ tools)
7. [07_osint_detective.yaml](#7-07_osint_detectiveyaml---osint) - OSINT (60+ tools)
8. [08_wireless_radio.yaml](#8-08_wireless_radioyaml---wireless) - Wireless (45+ tools)
9. [09_post_exploit.yaml](#9-09_post_exploityaml---post-exploitation) - Post-Exploitation (75+ tools)

---

## 1. 01_commands.yaml - General Pentesting

**Use Case:** Standard penetration testing engagements  
**Total Tools:** 60+  
**Categories:** 6

### Categories

#### 🔍 Reconnaissance
- **Nmap Quick Scan** - Fast port scan (top 1000 ports)
- **Nmap Full Scan** - Comprehensive all-port scan with service detection
- **Nmap Vulnerability Scan** - NSE vulnerability scripts
- **RustScan** - Ultra-fast port scanner
- **WhatWeb** - Web technology fingerprinting

#### 🌐 Web Application Attacks
- **Gobuster** - Directory/file brute forcing
- **Nikto** - Web server vulnerability scanner
- **SQLMap** - Automated SQL injection testing
- **Wfuzz** - Web application fuzzer

#### 💥 Exploitation
- **Metasploit DB** - Import Nmap results into Metasploit
- **SearchSploit** - Local exploit database search
- **Hydra SSH** - SSH credential brute forcing

#### 📡 Network Analysis
- **NetDiscover** - Active/passive network reconnaissance
- **ARP-Scan** - ARP-based host discovery
- **TCPDump** - Network packet capture

#### 🔎 Service Enumeration
- **Enum4Linux** - Windows/Samba enumeration
- **SMBClient** - SMB share enumeration
- **LDAP Search** - LDAP directory enumeration
- **SNMP Walk** - SNMP information gathering

#### 📶 Wireless Attacks
- **Airmon-ng** - Enable monitor mode
- **Airodump-ng** - Wireless packet capture
- **Wash** - WPS detection

**Usage:**
```bash
python3 main.py --config configs/01_commands.yaml
```

---

## 2. 02_ctf_kit.yaml - CTF Competitions

**Use Case:** Capture The Flag competitions and speed hacking  
**Total Tools:** 70+  
**Categories:** 7

### Categories

#### 🔍 Network Reconnaissance
- **RustScan** - Ultra-fast port scanner
- **Nmap Fast** - Quick 1000-port scan
- **Nmap Vuln** - Vulnerability detection
- **Masscan** - Mass IP scanning

#### 🖼️ Steganography & Forensics
- **ExifTool** - EXIF metadata extraction
- **Binwalk** - Firmware/file carving
- **Steghide** - Extract hidden data from images
- **Zsteg** - PNG/BMP LSB analysis
- **Strings** - Extract readable strings
- **Foremost** - File recovery by headers/footers

#### 🔓 Password Cracking
- **John the Ripper** - Password hash cracking
- **Hashcat MD5** - GPU-accelerated MD5 cracking
- **Hashcat NTLM** - Windows NTLM cracking
- **Hashcat SHA256** - SHA256 hash cracking
- **Hydra SSH** - SSH brute forcing

#### 🔐 Cryptography Tools
- **Hash Identifier** - Detect hash types
- **Base64 Decode** - Base64 decoding
- **OpenSSL AES Decrypt** - AES decryption
- **CyberChef Local** - Local HTML crypto tool

#### 🐚 Reverse Shells & Payloads
- **Python Reverse Shell** - Python-based reverse shell
- **Bash Reverse Shell** - Bash TCP reverse shell
- **Netcat Reverse** - Traditional netcat shell
- **Msfvenom Linux** - Linux ELF payload generation
- **Msfvenom Windows** - Windows EXE payload generation

#### 🌐 Quick Web Enumeration
- **Gobuster** - Directory brute forcing
- **Ffuf Vhost** - Virtual host discovery
- **WhatWeb** - Technology fingerprinting
- **Curl Headers** - HTTP header analysis

#### ⚙️ Binary & Reverse Engineering
- **File Identify** - File type detection
- **Ltrace** - Library call tracing
- **Strace** - System call tracing
- **Radare2** - Binary analysis
- **Objdump** - Binary disassembly

**Usage:**
```bash
python3 main.py --config configs/02_ctf_kit.yaml
```

---

## 3. 03_web_bounty.yaml - Web Security

**Use Case:** Bug bounty hunting and web application testing  
**Total Tools:** 80+  
**Categories:** 8

### Key Categories

#### Directory & Subdomain Enumeration
- Gobuster, Dirb, Ffuf, Feroxbuster
- Sublist3r, Amass, Assetfinder

#### Vulnerability Scanning
- Nikto, Nuclei, WPScan, Joomscan
- Wapiti, XSStrike, SQLMap

#### API & GraphQL Testing
- Postman, Arjun, GraphQL Voyager
- JWT Tool, API Fuzzer

#### CMS Exploitation
- WordPress, Joomla, Drupal scanners
- CMS-specific exploit tools

#### SSL/TLS Analysis
- SSLScan, TestSSL, SSL Labs

#### JavaScript Analysis
- JSParser, LinkFinder, Retire.js

**Usage:**
```bash
python3 main.py --config configs/03_web_bounty.yaml
```

---

## 4. 04_network_ad.yaml - Active Directory

**Use Case:** Windows networks and Active Directory penetration testing  
**Total Tools:** 65+  
**Categories:** 7

### Key Categories

#### AD Enumeration
- BloodHound, SharpHound, PowerView
- ADExplorer, Enum4Linux

#### Kerberos Attacks
- Rubeus, Kerberoasting
- AS-REP Roasting, Golden/Silver Tickets

#### Credential Dumping
- Mimikatz, LaZagne, Pypykatz
- SAM/LSA dumping

#### SMB Exploitation
- SMBClient, CrackMapExec, PSExec
- EternalBlue, SMBGhost

#### LDAP & Domain Services
- LDAP enumeration, DCSync
- Group Policy exploitation

#### Windows Privilege Escalation
- PowerUp, WinPEAS, Watson
- Token manipulation

**Usage:**
```bash
python3 main.py --config configs/04_network_ad.yaml
```

---

## 5. 05_mobile_iot.yaml - Mobile & IoT

**Use Case:** Mobile app and IoT device security testing  
**Total Tools:** 60+  
**Categories:** 6

### Key Categories

#### Android Analysis
- APKTool, Jadx, MobSF
- Frida, Objection, Drozer

#### iOS Security
- iProxy, iFunBox, Class-dump-z
- Clutch, Bagbak

#### Firmware Analysis
- Binwalk, Firmware-mod-kit
- QEMU emulation

#### Hardware Hacking
- UART, JTAG, SPI tools
- Logic analyzers, Bus Pirate

#### Network Analysis
- Wireshark, tcpdump
- BLE sniffing, Zigbee analysis

**Usage:**
```bash
python3 main.py --config configs/05_mobile_iot.yaml
```

---

## 6. 06_cloud_auditor.yaml - Cloud Security

**Use Case:** AWS, Azure, and GCP security auditing  
**Total Tools:** 75+  
**Categories:** 8

### Key Categories

#### ☁️ AWS Reconnaissance
- **Check Auth** - Verify AWS authentication
- **Get Caller Identity** - Check current credentials
- **List S3 Buckets** - Enumerate S3 buckets
- **List EC2 Instances** - Discover EC2 resources
- **List IAM Users** - IAM enumeration
- **List Lambda Functions** - Serverless discovery

#### 🔍 AWS Security Auditing
- **Prowler** - Comprehensive AWS security audit
- **ScoutSuite** - Multi-cloud security tool
- **Cloudsplaining** - IAM risk analysis
- **Pacu** - AWS exploitation framework

#### 🔷 Azure Reconnaissance
- Azure CLI enumeration tools
- VM, storage, web app discovery
- Key Vault enumeration

#### 🌐 GCP Reconnaissance
- GCloud project enumeration
- Compute instance discovery
- Storage bucket listing

#### 🪣 S3 Bucket Exploitation
- Bucket ACL checking
- Public access testing
- Bucket content downloading

#### 🐳 Container & Kubernetes Security
- kubectl commands
- Trivy scanning
- Docker inspection

#### 🔐 Cloud Metadata Exploitation
- AWS EC2 metadata
- Azure VM metadata
- GCP service account tokens

#### ⚡ Serverless Security
- Lambda function testing
- Serverless framework tools

**Usage:**
```bash
python3 main.py --config configs/06_cloud_auditor.yaml
```

---

## 7. 07_osint_detective.yaml - OSINT

**Use Case:** Open-source intelligence gathering  
**Total Tools:** 60+  
**Categories:** 6

### Key Categories

#### Email Intelligence
- Hunter.io, TheHarvester
- Email verification, breach checking

#### Domain & Subdomain Intel
- Whois, DNS enumeration
- Certificate transparency logs

#### Social Media OSINT
- Sherlock, Twint, InstagramOSINT
- Username enumeration

#### People Search
- Spokeo, Pipl alternatives
- Social network discovery

#### Image & Metadata Analysis
- Exiftool, reverse image search
- Geolocation extraction

#### Dark Web & Breach Data
- Have I Been Pwned
- Breach database searching

**Usage:**
```bash
python3 main.py --config configs/07_osint_detective.yaml
```

---

## 8. 08_wireless_radio.yaml - Wireless

**Use Case:** WiFi, Bluetooth, SDR, and RF security  
**Total Tools:** 45+  
**Categories:** 5

### Key Categories

#### WiFi Hacking
- Aircrack-ng suite
- WPA/WPA2 cracking
- Evil twin attacks

#### Bluetooth Attacks
- Bluesniff, Btlejack
- BLE exploitation

#### SDR & Radio Frequency
- GNU Radio, HackRF
- RTL-SDR tools

#### RFID/NFC
- Proxmark3, Chameleon
- Card cloning

#### Jamming & Analysis
- Signal jammers
- Spectrum analysis

**Usage:**
```bash
python3 main.py --config configs/08_wireless_radio.yaml
```

---

## 9. 09_post_exploit.yaml - Post-Exploitation

**Use Case:** Post-compromise activities and persistence  
**Total Tools:** 75+  
**Categories:** 10

### Key Categories

#### 🐧 Linux Enumeration
- **Payload Server** - HTTP server for hosting payloads
- **LinPEAS Command** - Generate download command
- **pspy Command** - Process monitoring download
- **SUID Find** - Find SUID binaries
- **Capabilities Check** - Linux capabilities enumeration

#### 📤 Data Exfiltration
- Netcat file transfer
- Curl upload
- Base64 encoding
- SCP transfer
- Python HTTP server

#### 🔒 Persistence Mechanisms
- Crontab backdoors
- Systemd services
- SSH key injection
- Bashrc backdoors

#### ↔️ Lateral Movement
- SSH tunneling
- SOCKS proxies
- Chisel tunneling
- Proxychains

#### 🔑 Credential Harvesting
- Mimikatz (Windows)
- LaZagne password recovery
- Browser password extraction
- /etc/shadow dumping

#### 🗺️ Internal Network Discovery
- ARP scanning
- Ping sweeps
- NetBIOS scanning
- Network range discovery

#### ⬆️ Privilege Escalation Exploits
- PwnKit (CVE-2021-4034)
- Dirty Pipe (CVE-2022-0847)
- DirtyCOW (CVE-2016-5195)
- GTFOBins exploitation

#### 🧹 Anti-Forensics & Cleanup
- Clear command history
- Secure file deletion
- Log wiping
- Timestamp modification

#### 🌐 Web Shell Deployment
- PHP web shells
- ASP shells
- JSP shells
- Weevely backdoors

#### 🐳 Container Escape Techniques
- Docker socket exploitation
- Privileged container checks
- CGroup escapes

**Usage:**
```bash
python3 main.py --config configs/09_post_exploit.yaml
```

---

## Usage Guide

### Basic Usage

```bash
# Launch specific module
python3 main.py --config configs/02_ctf_kit.yaml

# Or use aliases (if configured)
alias tajaa-ctf="python3 ~/tajaa-cli/main.py --config configs/02_ctf_kit.yaml"
tajaa-ctf
```

### Module Selection Guide

| Scenario | Recommended Module |
|----------|-------------------|
| General pentest | 01_commands.yaml |
| CTF competition | 02_ctf_kit.yaml |
| Bug bounty hunting | 03_web_bounty.yaml |
| Corporate network | 04_network_ad.yaml |
| Mobile app test | 05_mobile_iot.yaml |
| Cloud audit | 06_cloud_auditor.yaml |
| OSINT investigation | 07_osint_detective.yaml |
| WiFi assessment | 08_wireless_radio.yaml |
| Post-compromise | 09_post_exploit.yaml |

---

## Adding Custom Tools

Edit any YAML file to add your own tools:

```yaml
categories:
  your_category:
    name: "Your Category Name"
    tools:
      your_tool:
        name: "Your Tool Name"
        description: "What it does"
        command: "your_command {param1} {param2}"
        params:
          - param1
          - param2
        defaults:
          param1: "default_value"
```

---

## Tool Statistics

| Module | Categories | Tools | Primary Focus |
|--------|-----------|-------|---------------|
| 01_commands.yaml | 6 | 60+ | General pentesting |
| 02_ctf_kit.yaml | 7 | 70+ | CTF & speed hacking |
| 03_web_bounty.yaml | 8 | 80+ | Web application security |
| 04_network_ad.yaml | 7 | 65+ | Active Directory |
| 05_mobile_iot.yaml | 6 | 60+ | Mobile & IoT |
| 06_cloud_auditor.yaml | 8 | 75+ | Cloud security |
| 07_osint_detective.yaml | 6 | 60+ | Intelligence gathering |
| 08_wireless_radio.yaml | 5 | 45+ | Wireless security |
| 09_post_exploit.yaml | 10 | 75+ | Post-exploitation |
| **TOTAL** | **66** | **480+** | **Multi-domain** |

---

## Parameter Types

Tajaa CLI automatically validates these parameter types:

- **target_ip** - IPv4 address or hostname
- **target_url** - URL (auto-normalized)
- **lhost/lport** - Local host/port
- **file_path** - File system paths
- **wordlist** - Wordlist paths (multi-location support)
- **username/password** - Authentication credentials
- **domain** - Domain names
- **hash_file** - Hash files for cracking

---

## Security Features

All tools in this catalog benefit from:

✅ **Command Injection Protection** - All inputs sanitized with `shlex.quote()`  
✅ **Input Validation** - Automatic parameter validation  
✅ **Dangerous Input Detection** - Pattern matching for shell metacharacters  
✅ **Session Logging** - Every command logged with timestamp  
✅ **Dependency Checking** - Pre-execution tool availability warnings  

---

## Contributing

To add a new module:

1. Create `configs/10_your_module.yaml`
2. Follow the existing YAML structure
3. Test with `python3 main.py --config configs/10_your_module.yaml`
4. Submit pull request

---

## Support

- **Issues:** https://github.com/ARSTaha/tajaa-cli/issues
- **Documentation:** See README.md
- **Examples:** See EXAMPLES.md

---

**Author:** Tajaa  
**License:** MIT  
**Version:** 3.1.0

