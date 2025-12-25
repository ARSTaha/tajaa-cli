# Tajaa CLI - Tool Catalog

Complete reference for all security modules in Tajaa CLI.

---

## Modules Overview

| # | Module | File | Tools | Description |
|---|--------|------|-------|-------------|
| 1 | General | `01_commands.yaml` | 60+ | General pentesting |
| 2 | CTF Kit | `02_ctf_kit.yaml` | 150+ | CTF competitions |
| 3 | Web Bounty | `03_web_bounty.yaml` | 80+ | Bug bounty hunting |
| 4 | Network AD | `04_network_ad.yaml` | 65+ | Active Directory |
| 5 | Mobile IoT | `05_mobile_iot.yaml` | 60+ | Mobile & IoT |
| 6 | Cloud | `06_cloud_auditor.yaml` | 75+ | Cloud security |
| 7 | OSINT | `07_osint_detective.yaml` | 60+ | Intelligence gathering |
| 8 | Wireless | `08_wireless_radio.yaml` | 45+ | WiFi & RF |
| 9 | Post Exploit | `09_post_exploit.yaml` | 75+ | Post-exploitation |

---

## CTF Kit Details

The flagship module with 150+ tools for CTF competitions.

### Categories

| Category | Tools | Use Case |
|----------|-------|----------|
| 🎯 Nmap Arsenal | 15 | Port scanning & enumeration |
| ⚡ Fast Scanners | 3 | Quick reconnaissance |
| 🔍 Service Enum | 11 | SMB, SNMP, LDAP, NFS |
| 🌐 Web Discovery | 8 | Directory brute forcing |
| 🔎 Web Analysis | 6 | Technology fingerprinting |
| 💉 Web Exploitation | 9 | SQLi, XSS, LFI, SSRF |
| 📦 CMS Attacks | 5 | WordPress, Drupal, Joomla |
| 🔓 Hash Cracking | 13 | John, Hashcat |
| 🔐 Brute Force | 9 | Hydra, Medusa |
| 🖼️ Steganography | 13 | Image & file forensics |
| 🔊 Audio Analysis | 3 | Audio steganography |
| 🔐 Cryptography | 11 | Encoding & decryption |
| ⚙️ Binary Analysis | 12 | Reverse engineering |
| 💀 Binary Exploit | 5 | Buffer overflow tools |
| 📈 Privilege Escalation | 10 | LinPEAS, WinPEAS |
| 🐚 Reverse Shells | 14 | Shell generation |
| 🕵️ OSINT | 7 | Passive recon |
| ⚡ Utilities | 13 | File servers, search |

### Popular Commands

**Nmap - Full TCP Scan (CTF Standard)**
```bash
nmap -sC -sV -p- -oN scan.txt <TARGET>
```

**Gobuster - Directory Brute**
```bash
gobuster dir -u http://<TARGET> -w /usr/share/wordlists/dirb/common.txt -t 50
```

**John the Ripper**
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt <HASH_FILE>
```

**Hydra - SSH Brute**
```bash
hydra -l <USER> -P /usr/share/wordlists/rockyou.txt ssh://<TARGET>
```

**Netcat Listener**
```bash
nc -lvnp <PORT>
```

---

## Hash Modes Reference

| Hash Type | John | Hashcat Mode |
|-----------|------|--------------|
| MD5 | auto | 0 |
| SHA1 | auto | 100 |
| SHA256 | auto | 1400 |
| SHA512 | auto | 1700 |
| NTLM | auto | 1000 |
| bcrypt | auto | 3200 |
| WordPress | auto | 400 |
| Linux Shadow | auto | 1800 |

---

## Usage

```bash
# Activate environment
source .venv/bin/activate

# Run CTF Kit
python3 main.py --config configs/02_ctf_kit.yaml

# Run Web Bounty
python3 main.py --config configs/03_web_bounty.yaml

# Run OSINT
python3 main.py --config configs/07_osint_detective.yaml
```

---

## Custom Configuration

Create your own YAML config:

```yaml
categories:
  my_tools:
    name: "My Tools"
    tools:
      my_scan:
        name: "My Custom Scan"
        description: "Custom nmap scan"
        command: "nmap -sC -sV {target_ip}"
        params:
          - target_ip
```

---

## Dependencies

Most tools come pre-installed on Kali. Install missing tools:

```bash
sudo apt update
sudo apt install nmap masscan gobuster feroxbuster ffuf
sudo apt install john hashcat hydra medusa
sudo apt install sqlmap nikto wpscan
sudo apt install binwalk foremost steghide exiftool
```

Run `install_arsenal.sh` for extras:

```bash
chmod +x install_arsenal.sh
sudo ./install_arsenal.sh
```

---

**Author**: Tajaa  
**Version**: 4.0.0

