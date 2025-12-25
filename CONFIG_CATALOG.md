# Tajaa CLI - Configuration Catalog

Complete reference for all tools and configurations available in the Tajaa CLI framework.

---

## Overview

Tajaa CLI provides **8 specialized security modules** with **480+ pre-configured tools**. Each module is stored as a YAML configuration file in the `configs/` directory.

| Module | File | Tools | Description |
|--------|------|-------|-------------|
| General Commands | `01_commands.yaml` | 60+ | General pentesting and recon |
| CTF Kit | `02_ctf_kit.yaml` | 150+ | Complete CTF competition toolkit |
| Web Bounty | `03_web_bounty.yaml` | 80+ | Bug bounty and web security |
| Network AD | `04_network_ad.yaml` | 65+ | Active Directory attacks |
| Mobile IoT | `05_mobile_iot.yaml` | 60+ | Mobile and IoT testing |
| Cloud Auditor | `06_cloud_auditor.yaml` | 75+ | Cloud security auditing |
| OSINT Detective | `07_osint_detective.yaml` | 60+ | Open source intelligence |
| Wireless Radio | `08_wireless_radio.yaml` | 45+ | Wireless and RF attacks |
| Post Exploit | `09_post_exploit.yaml` | 75+ | Post-exploitation techniques |

---

## Module Details

### CTF Kit (`02_ctf_kit.yaml`)

The ultimate CTF competition toolkit with 150+ tools organized into 15 categories.

#### Categories

| Category | Tools | Description |
|----------|-------|-------------|
| 🎯 Nmap Arsenal | 15 | Essential Nmap scans for every scenario |
| ⚡ Lightning Fast Scanners | 3 | RustScan, Masscan for quick enumeration |
| 🔍 Service Enumeration | 12 | SMB, SNMP, LDAP, NFS enumeration |
| 🌐 Web Discovery | 8 | Directory and content discovery |
| 🔎 Web Analysis | 6 | Technology fingerprinting |
| 💉 Web Vulnerabilities | 9 | SQLi, XSS, LFI, SSRF exploitation |
| 📦 CMS Attacks | 5 | WordPress, Drupal, Joomla scanners |
| 🔓 Hash Cracking | 13 | John, Hashcat for all hash types |
| 🔐 Brute Force | 9 | Hydra, Medusa for online attacks |
| 🖼️ Steganography | 13 | Image and file forensics |
| 🔊 Audio Stego | 3 | Audio analysis tools |
| 🔐 Cryptography | 12 | Encoding, decryption, RSA attacks |
| ⚙️ Binary Analysis | 12 | Reverse engineering tools |
| 💀 Binary Exploitation | 5 | ROP gadgets, pattern generation |
| 📈 Privilege Escalation | 10 | LinPEAS, WinPEAS, enumeration |
| 🐚 Shells & Listeners | 14 | Reverse shell generators |
| 🕵️ OSINT | 7 | Passive reconnaissance |
| ⚡ Quick Utilities | 13 | HTTP servers, searchsploit, tunnels |

#### Nmap Arsenal (15 Essential Scans)

```
nmap_full_tcp      - Full TCP scan with scripts: nmap -sC -sV -p- -oN scan.txt
nmap_quick_initial - Quick initial recon: nmap -sC -sV -oN initial_scan.txt
nmap_udp_top100    - UDP top 100: sudo nmap -sU --top-ports 100 -sV
nmap_all_scripts   - Full script scan: nmap -sC -sV -A -T4 -p-
nmap_vuln_scan     - Vulnerability detection: nmap --script vuln -p-
nmap_smb_enum      - SMB enumeration: nmap -p 139,445 --script=smb-*
nmap_http_enum     - HTTP enumeration: nmap -p 80,443 --script=http-*
nmap_ftp_anon      - FTP anonymous check: nmap -p 21 --script=ftp-*
nmap_ssh_enum      - SSH enumeration: nmap -p 22 --script=ssh-*
nmap_ldap_enum     - LDAP/AD enumeration: nmap -p 389,636 --script=ldap-*
nmap_mysql_enum    - MySQL enumeration: nmap -p 3306 --script=mysql-*
nmap_snmp_enum     - SNMP enumeration: sudo nmap -sU -p 161 --script=snmp-*
nmap_dns_enum      - DNS enumeration: nmap -p 53 --script=dns-*
nmap_rdp_check     - RDP security check: nmap -p 3389 --script=rdp-*
nmap_stealth_syn   - Stealth SYN scan: sudo nmap -sS -T2 -f
```

#### Hash Cracking Reference

| Hash Type | John Mode | Hashcat Mode |
|-----------|-----------|--------------|
| MD5 | auto | 0 |
| SHA1 | auto | 100 |
| SHA256 | auto | 1400 |
| SHA512 | auto | 1700 |
| NTLM | auto | 1000 |
| bcrypt | auto | 3200 |
| WordPress | auto | 400 |
| Linux Shadow | auto | 1800 |

---

### Web Bounty (`03_web_bounty.yaml`)

Bug bounty hunting and web application security testing.

#### Categories

| Category | Description |
|----------|-------------|
| Subdomain Discovery | Sublist3r, Amass, Subfinder |
| Web Probing | Httprobe, Httpx, Wayback |
| Vulnerability Scanners | Nuclei, Nikto, Wapiti |
| XSS Detection | Dalfox, XSStrike, XSSer |
| SQL Injection | SQLmap (all modes) |
| CMS Scanning | WPScan, Joomscan, Droopescan |
| API Testing | Arjun, Kiterunner, Ffuf |
| Fuzzing | Wfuzz, Ffuf, custom payloads |
| Command Injection | Commix, Tplmap |
| SSL/TLS Analysis | SSLyze, Testssl.sh |

---

### Network AD (`04_network_ad.yaml`)

Active Directory and network penetration testing.

#### Categories

| Category | Description |
|----------|-------------|
| SMB Enumeration | Enum4linux, SMBClient, CrackMapExec |
| Kerberos Attacks | Kerbrute, GetNPUsers, GetUserSPNs |
| LDAP Enumeration | LDAPSearch, BloodHound |
| Credential Attacks | Responder, NTLMRelayx |
| Lateral Movement | PsExec, WMIExec, EvilWinRM |
| Domain Compromise | Secretsdump, DCSync |

---

### Cloud Auditor (`06_cloud_auditor.yaml`)

Cloud infrastructure security assessment.

#### Categories

| Category | Description |
|----------|-------------|
| AWS Enumeration | aws-cli, Pacu, ScoutSuite |
| Azure Auditing | Az PowerShell, ROADtools |
| GCP Testing | gcloud, GCPBucketBrute |
| S3 Bucket Testing | S3Scanner, Bucket Finder |
| Container Security | Docker Bench, Trivy |
| Kubernetes | kubectl, Kubeaudit |

---

## Usage Examples

### Loading a Specific Module

```bash
# Activate virtual environment first
source .venv/bin/activate

# Load CTF Kit
python3 main.py --config configs/02_ctf_kit.yaml

# Load Web Bounty
python3 main.py --config configs/03_web_bounty.yaml

# Load Cloud Auditor
python3 main.py --config configs/06_cloud_auditor.yaml
```

### CTF Workflow Example

1. **Start with Fast Scan**
   - Select "Nmap Arsenal" → "Full TCP Scan with Scripts"
   - This runs: `nmap -sC -sV -p- -oN scan.txt <target>`

2. **Enumerate Services**
   - Based on open ports, select appropriate enumeration tools
   - SMB on 445? Use "Service Enumeration" → "Enum4Linux"
   - Web on 80? Use "Web Discovery" → "Gobuster"

3. **Find Vulnerabilities**
   - Use "Web Vulnerabilities" category for SQLi, XSS testing
   - Use "Hash Cracking" if you find password hashes

4. **Get Shell**
   - Use "Shells & Listeners" to generate reverse shells
   - Start listener with "Netcat - Start Listener"

5. **Privilege Escalation**
   - Use "Privilege Escalation" → "LinPEAS - Host for Download"
   - Transfer to target and run enumeration

---

## Creating Custom Configurations

You can create your own YAML configurations. Here's the structure:

```yaml
categories:
  category_name:
    name: "Category Display Name"
    tools:
      tool_id:
        name: "Tool Display Name"
        description: "What this tool does"
        command: "actual command with {parameters}"
        params:
          - parameter1
          - parameter2
        defaults:
          parameter1: "default_value"
```

### Example Custom Tool

```yaml
categories:
  my_tools:
    name: "My Custom Tools"
    tools:
      my_scanner:
        name: "My Port Scanner"
        description: "Custom nmap scan with my preferred options"
        command: "nmap -sC -sV -A -T4 --open -oA myscan {target_ip}"
        params:
          - target_ip
```

---

## Tool Dependencies

Most tools are pre-installed on Kali Linux. For missing tools:

```bash
# Update package lists
sudo apt update

# Install common tools
sudo apt install nmap masscan rustscan gobuster feroxbuster ffuf
sudo apt install john hashcat hydra medusa crackmapexec
sudo apt install sqlmap nikto wpscan whatweb
sudo apt install binwalk foremost steghide exiftool
sudo apt install radare2 gdb ltrace strace
```

### Optional Installations

Run `install_arsenal.sh` for additional tools:

```bash
sudo ./install_arsenal.sh
```

This installs:
- CyberChef (Local HTML version)
- LinPEAS / WinPEAS
- pspy64
- Common wordlists (SecLists, rockyou.txt)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/ARSTaha/tajaa-cli/issues)
- **Documentation**: See other .md files in the repository
- **Troubleshooting**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Author**: Tajaa  
**License**: MIT  
**Version**: 4.0.0

