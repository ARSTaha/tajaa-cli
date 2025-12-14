# 📚 Tajaa CLI - Configuration Catalog

> **Complete reference guide for all available security modules**

---

## 📖 Overview

Tajaa CLI uses a modular architecture with specialized YAML configuration files. Each module is designed for a specific cyber security domain, containing carefully curated tools and commands.

**Location:** `configs/`  
**Total Modules:** 9  
**Naming Convention:** `[number]_[domain].yaml`

---

## 🗂️ Module Index

| # | Module | Domain | Primary Use Case |
|---|--------|--------|------------------|
| **01** | `commands.yaml` | General Pentest | Standard security assessments |
| **02** | `ctf_kit.yaml` | CTF & Competition | Speed-focused competitive hacking |
| **03** | `web_bounty.yaml` | Web Application | Bug bounties & web app testing |
| **04** | `network_ad.yaml` | Enterprise Networks | Active Directory exploitation |
| **05** | `mobile_iot.yaml` | Mobile & Firmware | App analysis & IoT security |
| **06** | `cloud_auditor.yaml` | Cloud Security | AWS/Azure/GCP assessments |
| **07** | `osint_detective.yaml` | Intelligence | Passive recon & OSINT |
| **08** | `wireless_radio.yaml` | Wireless & SDR | WiFi, Bluetooth, radio signals |
| **09** | `post_exploit.yaml` | Post-Exploitation | Persistence, privilege escalation |

---

## 📋 Detailed Module Descriptions

### **01 - General Commands** (`01_commands.yaml`)
**Target Audience:** Security professionals, pentesters  
**Scenario:** General-purpose security assessments

**Tool Categories:**
- Network Discovery (Nmap, Netcat, Ping)
- Web Analysis (cURL, Wget, Gobuster)
- Enumeration (DNS, SMB, SNMP)
- Exploitation (Metasploit, Searchsploit)

**Usage:**
```bash
tajaa --config configs/01_commands.yaml
```

**Key Feature:** Essential toolkit for standard penetration testing workflows

---

### **02 - CTF Kit** (`02_ctf_kit.yaml`)
**Target Audience:** CTF players, competitive hackers  
**Scenario:** Capture The Flag events, time-critical challenges

**Tool Categories:**
- Ultra-fast network scanning (RustScan, Masscan)
- Forensics (Exiftool, Binwalk, Strings)
- Steganography (Steghide, Zsteg, Stegseek)
- Password cracking (John, Hashcat)
- Quick exploitation (Python reverse shells)

**Usage:**
```bash
tajaa --config configs/02_ctf_kit.yaml
```

**Key Feature:** Optimized for speed and efficiency

---

### **03 - Web Bounty Hunter** (`03_web_bounty.yaml`)
**Target Audience:** Bug bounty hunters, web pentesters  
**Scenario:** Deep web application security testing

**Tool Categories & Complete Tool List:**

**🔎 Subdomain Discovery (5 tools)**
- `Sublist3r` - Fast passive subdomain finder using search engines
- `Amass Enum` - OWASP Amass active and passive subdomain enumeration
- `Amass Passive` - Passive-only reconnaissance mode
- `Subfinder` - Lightning-fast passive subdomain discovery
- `Assetfinder` - Domain asset discovery tool

**🌐 Web Service Probing (4 tools)**
- `Httprobe` - Live host detection for HTTP/HTTPS
- `Httpx` - Advanced HTTP toolkit with tech detection
- `Waybackurls` - Historical endpoint discovery from Wayback Machine
- `GAU (Get All URLs)` - Fetch URLs from AlienVault, Wayback, Common Crawl

**🎯 Vulnerability Scanners (4 tools)**
- `Nuclei Basic` - Template-based scanner with 5000+ templates
- `Nuclei List` - Scan multiple URLs with severity filtering
- `Nikto` - Classic web server vulnerability scanner
- `Wapiti` - Black-box web application auditor

**🔥 XSS Detection & Exploitation (4 tools)**
- `Dalfox (Pipe)` - Fast XSS scanner with parameter analysis
- `Dalfox (File)` - Scan multiple URLs from file
- `XSStrike` - Intelligent XSS scanner with crawling
- `XSSer` - Automated XSS exploitation framework

**💉 SQL Injection (5 tools)**
- `SQLmap Auto` - Automatic SQL injection detection
- `SQLmap Enumerate DBs` - List all databases
- `SQLmap Dump` - Extract entire database contents
- `SQLmap OS Shell` - Attempt to get operating system shell
- `NoSQLMap` - NoSQL injection scanner (MongoDB, CouchDB)

**📦 CMS-Specific Scanners (4 tools)**
- `WPScan` - WordPress security scanner
- `WPScan Aggressive` - Aggressive plugin detection mode
- `Droopescan` - Drupal/Joomla/Moodle scanner
- `Joomscan` - Dedicated Joomla vulnerability scanner

**🔌 API Security Testing (4 tools)**
- `Arjun` - HTTP parameter discovery
- `Kiterunner` - Fast API endpoint and route discovery
- `Ffuf Param` - Parameter fuzzing for APIs
- `Newman` - Postman CLI runner for API testing

**🎲 Web Fuzzing (4 tools)**
- `Wfuzz Basic` - General purpose HTTP fuzzer
- `Wfuzz POST` - POST parameter fuzzing
- `Ffuf Subdomain` - Fast subdomain discovery via DNS
- `Ffuf Extension` - File extension discovery

**⚡ Command Injection Testing (3 tools)**
- `Commix Auto` - Automatic command injection detection
- `Commix OS Shell` - Exploit to spawn shell
- `Tplmap` - Server-Side Template Injection (SSTI) detection

**🔒 SSL/TLS Analysis (3 tools)**
- `SSLscan` - SSL/TLS cipher suite scanner
- `Testssl.sh` - Comprehensive SSL vulnerability testing
- `SSLyze` - Fast SSL configuration scanner

**Total Tools: 40** | **Categories: 10**

**Usage:**
```bash
tajaa --config configs/03_web_bounty.yaml
```

**Key Feature:** Comprehensive web attack surface coverage from recon to exploitation

---

### **04 - Network & Active Directory** (`04_network_ad.yaml`)
**Target Audience:** Corporate pentesters, red teamers  
**Scenario:** Internal network assessments, Windows environments

**Tool Categories:**
- Windows exploitation (Evil-WinRM, Impacket-PsExec)
- SMB attacks (CrackMapExec, SMBClient)
- Credential harvesting (Responder, Mimikatz)
- Kerberos attacks (Kerbrute, GetNPUsers)
- Domain enumeration (Bloodhound, Enum4Linux-ng)

**Usage:**
```bash
tajaa --config configs/04_network_ad.yaml
```

**Key Feature:** Enterprise-grade Active Directory toolkit

---

### **05 - Mobile & IoT** (`05_mobile_iot.yaml`)
**Target Audience:** Mobile security researchers, IoT testers  
**Scenario:** Android/iOS app analysis, firmware reverse engineering

**Tool Categories & Complete Tool List:**

**🤖 Android APK Analysis (7 tools)**
- `Apktool Decompile` - Decompile APK to smali code and resources
- `Apktool Recompile` - Rebuild modified APK
- `JADX Decompile` - Decompile APK to readable Java source
- `JADX-GUI` - Interactive decompiler with GUI
- `AAPT Manifest` - Extract AndroidManifest.xml
- `AAPT Permissions` - List app permissions
- `MobSF` - Mobile Security Framework automated analysis

**📱 Android Device Interaction (7+ tools)**
- `ADB Devices` - List connected Android devices
- `ADB Shell` - Interactive device shell
- `ADB Install` - Install APK to device
- `ADB Pull` - Extract files from device
- `ADB Push` - Upload files to device
- `ADB Logcat` - Real-time system logs
- `ADB Backup` - Create device backup

**🍎 iOS Security Testing (5 tools)**
- `Objection` - Runtime mobile exploration toolkit
- `Frida` - Dynamic instrumentation framework
- `Frida-Trace` - Function call tracing
- `Frida-PS` - List running processes
- `iOS Binary Analysis` - Static analysis tools

**📡 Firmware Analysis (6 tools)**
- `Binwalk Extract` - Extract embedded files from firmware
- `Binwalk Entropy` - Analyze encryption/compression in firmware
- `Firmware-mod-kit Extract` - Unpack firmware images
- `Firmware-mod-kit Build` - Rebuild modified firmware
- `Strings Analysis` - Extract readable strings
- `Hexdump` - Binary file examination

**🔬 Dynamic Analysis (4 tools)**
- `Frida Instrumentation` - Runtime manipulation
- `Drozer` - Android security assessment framework
- `Scrcpy` - Android device screen mirroring and control
- `MobSF Dynamic` - Dynamic application testing

**Total Tools: 29+** | **Categories: 5**

**Usage:**
```bash
tajaa --config configs/05_mobile_iot.yaml
```

**Key Feature:** Complete mobile and IoT security testing - from APK analysis to firmware reverse engineering

---

### **06 - Cloud Auditor** (`06_cloud_auditor.yaml`)
**Target Audience:** Cloud security engineers, DevSecOps  
**Scenario:** Multi-cloud infrastructure security assessments

**Tool Categories & Complete Tool List:**

**☁️ AWS Reconnaissance (9 tools)**
- `AWS Whoami` - Check current AWS credentials and permissions
- `AWS S3 List` - Enumerate all S3 buckets
- `AWS S3 Bucket Contents` - List objects in specific bucket
- `AWS EC2 Instances` - Enumerate EC2 instances in region
- `AWS IAM Users` - List all IAM users
- `AWS IAM Policies` - List custom IAM policies
- `AWS Lambda Functions` - Enumerate Lambda functions
- `AWS RDS Instances` - List RDS databases
- `AWS Secrets Manager` - Enumerate stored secrets

**🔍 AWS Security Auditing (6 tools)**
- `Prowler Full` - Comprehensive AWS security audit (200+ checks)
- `Prowler CIS` - CIS AWS Foundations Benchmark
- `Prowler Region` - Audit specific AWS region
- `ScoutSuite AWS` - Multi-cloud security auditing
- `ScoutSuite Report` - Generate detailed HTML report
- `Cloudsplaining` - IAM risk and privilege escalation analysis

**🔷 Azure Security Testing (7 tools)**
- `Azure Login` - Authenticate to Azure
- `Azure List Resources` - Enumerate all resources
- `Azure VM List` - List virtual machines
- `Azure Storage Accounts` - Enumerate storage accounts
- `Azure Key Vault List` - List key vaults and secrets
- `ScoutSuite Azure` - Azure security audit
- `Azure AD Enumeration` - Active Directory reconnaissance

**🟢 Google Cloud Platform (6 tools)**
- `GCloud Projects` - List GCP projects
- `GCloud Compute Instances` - Enumerate VM instances
- `GCloud Storage Buckets` - List Cloud Storage buckets
- `GCloud IAM Policies` - Enumerate IAM policies
- `GCloud Service Accounts` - List service accounts
- `ScoutSuite GCP` - GCP security audit

**🔧 Container & Kubernetes Security (4 tools)**
- `Kubectl Get Pods` - List Kubernetes pods
- `Kubectl Get Secrets` - Extract secrets from K8s
- `Docker Image Scan` - Scan Docker images for vulnerabilities
- `Trivy` - Container vulnerability scanner

**Total Tools: 32+** | **Categories: 5**

**Usage:**
```bash
tajaa --config configs/06_cloud_auditor.yaml
```

**Key Feature:** Complete multi-cloud security coverage (AWS, Azure, GCP) with automated compliance auditing

---

### **07 - OSINT Detective** (`07_osint_detective.yaml`)
**Target Audience:** Threat intelligence analysts, social engineers  
**Scenario:** Passive reconnaissance without touching the target

**Tool Categories:**
- Email/domain harvesting (TheHarvester)
- Username hunting (Sherlock, WhatsMyName)
- Domain intelligence (Whois, DNSRecon)
- Social media OSINT (Twint, Holehe)
- Automation frameworks (SpiderFoot, Recon-ng)

**Usage:**
```bash
tajaa --config configs/07_osint_detective.yaml
```

**Key Feature:** 100% passive, no target interaction

---

### **08 - Wireless & Radio** (`08_wireless_radio.yaml`)
**Target Audience:** Wireless security specialists, SDR enthusiasts  
**Scenario:** WiFi/Bluetooth/RF signal security testing

**Tool Categories:**
- WiFi (Aircrack-ng suite, Wifite, Bettercap)
- Bluetooth (Bluesnarfer, Bettercap)
- SDR (HackRF, RTL-SDR)
- Network interception (Bettercap, Ettercap)

**Usage:**
```bash
tajaa --config configs/08_wireless_radio.yaml
```

**Key Feature:** Signals intelligence and wireless exploitation

---

### **09 - Post-Exploitation** (`09_post_exploit.yaml`)
**Target Audience:** Red teamers, advanced pentesters  
**Scenario:** Post-compromise operations, lateral movement

**Tool Categories & Complete Tool List:**

**🐧 Linux Post-Exploitation Enumeration (8 tools)**
- `LinPEAS` - Automated Linux privilege escalation enumeration
- `LinEnum` - Comprehensive system enumeration script
- `Linux Smart Enumeration` - Smart enumeration with verbosity levels
- `Pspy` - Monitor Linux processes without root (cron jobs)
- `Sudo Version Check` - Check for vulnerable sudo versions
- `Find SUID Binaries` - Locate SUID binaries for privilege escalation
- `GetCap` - List files with special Linux capabilities
- `Find World Writable` - Locate world-writable files and directories

**📤 Data Exfiltration (8 tools)**
- `Netcat Send` - Send file via netcat to listening server
- `Netcat Receive` - Listen and receive file via netcat
- `Curl Upload` - Upload file via HTTP POST
- `Wget Download` - Download file from attacker server
- `Base64 Encode` - Encode file to base64 for manual exfil
- `SCP Transfer` - Secure copy via SSH
- `Python HTTP Server` - Simple HTTP server for file transfer
- `Updog Server` - HTTP server with upload capability

**🔒 Persistence Mechanisms (6+ tools)**
- `Crontab Add` - Add reverse shell to crontab
- `Systemd Service` - Create systemd service (requires root)
- `Bashrc Backdoor` - Add reverse shell to .bashrc
- `SSH Authorized Keys` - Add attacker SSH public key
- `Startup Scripts` - Modify system startup scripts
- `Init.d Persistence` - Create init.d service

**💻 Windows Post-Exploitation (6+ tools)**
- `WinPEAS` - Windows privilege escalation enumeration
- `PowerSploit` - PowerShell post-exploitation framework
- `Mimikatz` - Credential dumping and manipulation
- `LaZagne` - Multi-platform password recovery
- `Rubeus` - Kerberos abuse toolkit
- `SharpHound` - BloodHound data collector for Windows

**🔄 Lateral Movement (5+ tools)**
- `SSH Tunneling` - Create SSH tunnels for pivoting
- `Chisel` - Fast TCP/UDP tunnel over HTTP
- `Ligolo` - Reverse tunneling tool
- `Proxychains` - Force connections through proxy
- `Socat` - Multipurpose relay tool

**🗑️ Covering Tracks (5+ tools)**
- `Log Deletion` - Remove entries from system logs
- `Timestomping` - Modify file timestamps
- `Clear Bash History` - Remove command history
- `Clear Event Logs` - Windows event log deletion
- `Disable Logging` - Temporarily disable system logging

**Total Tools: 38+** | **Categories: 6**

**Usage:**
```bash
tajaa --config configs/09_post_exploit.yaml
```

**Key Feature:** Complete post-compromise toolkit - from enumeration to persistence to exfiltration

---

## 🎯 How to Choose a Module

| Your Goal | Recommended Module |
|-----------|-------------------|
| I'm playing a CTF competition | `02_ctf_kit.yaml` |
| I need to test a web application | `03_web_bounty.yaml` |
| I'm on a corporate internal pentest | `04_network_ad.yaml` |
| I need to analyze a mobile app | `05_mobile_iot.yaml` |
| I'm auditing AWS/Azure infrastructure | `06_cloud_auditor.yaml` |
| I need to gather intelligence passively | `07_osint_detective.yaml` |
| I'm testing WiFi security | `08_wireless_radio.yaml` |
| I've already compromised a system | `09_post_exploit.yaml` |
| I need general-purpose tools | `01_commands.yaml` |

---

## 🔧 Configuration File Structure

All modules follow this standardized YAML schema:

```yaml
categories:
  category_key:
    name: "Display Name for Category"
    tools:
      tool_key:
        name: "Tool Display Name"
        description: "What this tool does"
        command: "binary_name --flag {param1} {param2}"
        params:
          - param1
          - param2
```

**Key Elements:**
- **categories:** Logical grouping of related tools
- **tools:** Individual security tools with metadata
- **command:** Actual command template with placeholders
- **params:** Required user inputs (e.g., target_ip, domain)

---

## 🚀 Quick Start Examples

### Example 1: Run a Fast Port Scan (CTF Mode)
```bash
# Launch Tajaa with CTF configuration
tajaa --config configs/02_ctf_kit.yaml

# Select: Network Reconnaissance > RustScan
# Input: 192.168.1.100
```

### Example 2: Find Subdomains (Bug Bounty Mode)
```bash
# Launch Tajaa with Web Bounty configuration
tajaa --config configs/03_web_bounty.yaml

# Select: Subdomain Enumeration > Sublist3r
# Input: example.com
```

### Example 3: Enumerate Active Directory (Corporate Mode)
```bash
# Launch Tajaa with Network/AD configuration
tajaa --config configs/04_network_ad.yaml

# Select: Domain Enumeration > Enum4Linux-ng
# Input: 10.10.10.100
```

---

## 📝 Creating Custom Modules

You can create your own configurations following these guidelines:

### Naming Convention
- Use numbered prefixes for ordering: `10_custom_module.yaml`
- Use lowercase with underscores: `my_custom_tools.yaml`
- Place in `configs/` directory

### Minimum Required Structure
```yaml
categories:
  my_category:
    name: "My Category"
    tools:
      my_tool:
        name: "My Tool"
        description: "What it does"
        command: "tool-binary {param}"
        params:
          - param
```

### Best Practices
1. **Use descriptive tool names** - Include the tool's purpose
2. **Write clear descriptions** - Explain what the tool does and when to use it
3. **Use parameter placeholders** - Wrap variables in curly braces: `{target_ip}`
4. **Group logically** - Organize tools into meaningful categories
5. **Test commands** - Ensure all commands work on Kali Linux

---

## 🔐 Security Notes

- **All configurations assume Kali Linux environment**
- Some tools require `sudo` privileges (clearly marked in descriptions)
- Always ensure you have proper authorization before using these tools
- Logs are stored in `session_logs.txt` (automatically created)

---

## 📄 Version Information

- **Catalog Version:** 3.0.0
- **Last Updated:** December 14, 2025
- **Total Tools:** 270+ across all modules
- **Supported Domains:** 9
- **Total Categories:** 50+

### Tool Count by Module:
| Module | Tools | Categories |
|--------|-------|------------|
| 01 - General Commands | 19 | 5 |
| 02 - CTF Kit | 34 | 7 |
| 03 - Web Bounty Hunter | 40 | 10 |
| 04 - Network & AD | 28+ | 5 |
| 05 - Mobile & IoT | 29+ | 5 |
| 06 - Cloud Auditor | 32+ | 5 |
| 07 - OSINT Detective | 37+ | 6 |
| 08 - Wireless & Radio | 40+ | 7 |
| 09 - Post-Exploitation | 38+ | 6 |
| **TOTAL** | **270+** | **50+** |

---

## 🤝 Contributing

To add new tools to existing modules or create new modules:

1. Follow the YAML schema outlined above
2. Ensure tool is available in Kali Linux repositories
3. Test the command template with real parameters
4. Add clear, professional descriptions
5. Update this catalog if adding new modules

---

## 📚 Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Architecture Guide:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Quick Start Guide:** [QUICKSTART.md](QUICKSTART.md)
- **Change History:** [CHANGELOG.md](CHANGELOG.md)

---

**Tajaa CLI v3.0.0** - The Ultimate Modular Cyber Security Framework  
*Built for professionals, designed for speed, optimized for results.*

