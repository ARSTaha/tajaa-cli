# Tajaa CLI - Configuration Modules

This directory contains modular YAML configuration files for different cyber security domains.

## 📁 Module Organization

The configurations are numbered for logical progression and ease of use:

### **01_commands.yaml** - Default Configuration
- **Purpose:** General-purpose penetration testing toolkit
- **Use Case:** Standard security assessments and quick tasks
- **Usage:** `tajaa --config configs/01_commands.yaml`
- **Domain:** General Pentest

### **02_ctf_kit.yaml** - CTF & Competition Tools
- **Purpose:** Speed-focused tools for Capture The Flag competitions
- **Use Case:** CTF events, puzzle solving, forensics challenges
- **Usage:** `tajaa --config configs/02_ctf_kit.yaml`
- **Domain:** Competitive Security
- **Key Tools:** Nmap (fast), Rustscan, Binwalk, Steghide, John, Hashcat

### **03_web_bounty.yaml** - Web Application Security
- **Purpose:** Deep web analysis and bug bounty hunting
- **Use Case:** Web application penetration testing, API security
- **Usage:** `tajaa --config configs/03_web_bounty.yaml`
- **Domain:** Web Security
- **Key Tools:** Sublist3r, Nuclei, Sqlmap, WPScan, Dalfox, Nikto

### **04_network_ad.yaml** - Active Directory & Corporate Networks
- **Purpose:** Enterprise network security and Active Directory exploitation
- **Use Case:** Corporate internal assessments, Windows environments
- **Usage:** `tajaa --config configs/04_network_ad.yaml`
- **Domain:** Corporate Security
- **Key Tools:** Evil-WinRM, CrackMapExec, Impacket, Bloodhound, Responder

### **05_mobile_iot.yaml** - Mobile & IoT Security
- **Purpose:** Android/iOS application analysis and firmware hacking
- **Use Case:** Mobile app pentesting, IoT device security
- **Usage:** `tajaa --config configs/05_mobile_iot.yaml`
- **Domain:** Mobile Security
- **Key Tools:** Apktool, Jadx, ADB, Binwalk, Objection

### **06_cloud_auditor.yaml** - Cloud Security Assessment
- **Purpose:** Multi-cloud security auditing (AWS, Azure, GCP)
- **Use Case:** Cloud infrastructure security reviews
- **Usage:** `tajaa --config configs/06_cloud_auditor.yaml`
- **Domain:** Cloud Security
- **Key Tools:** AWS CLI, ScoutSuite, Prowler, CloudSplaining

### **07_osint_detective.yaml** - OSINT & Reconnaissance
- **Purpose:** Passive intelligence gathering and reconnaissance
- **Use Case:** Pre-engagement research, social engineering prep
- **Usage:** `tajaa --config configs/07_osint_detective.yaml`
- **Domain:** Intelligence Gathering
- **Key Tools:** TheHarvester, Sherlock, SpiderFoot, DNSRecon, WHOIS

### **08_wireless_radio.yaml** - Wireless & Signal Intelligence
- **Purpose:** WiFi, Bluetooth, and Software-Defined Radio (SDR) attacks
- **Use Case:** Wireless network assessments, RF signal analysis
- **Usage:** `tajaa --config configs/08_wireless_radio.yaml`
- **Domain:** Wireless Security
- **Key Tools:** Aircrack-ng suite, Wifite, Bettercap, HackRF tools

### **09_post_exploit.yaml** - Post-Exploitation Framework
- **Purpose:** Activities after initial compromise
- **Use Case:** Privilege escalation, persistence, lateral movement
- **Usage:** `tajaa --config configs/09_post_exploit.yaml`
- **Domain:** Advanced Exploitation
- **Key Tools:** Metasploit modules, privilege escalation scripts, persistence tools

---

## 🎯 Quick Selection Guide

**Choose your module based on your target:**

| Target Type | Recommended Module |
|-------------|-------------------|
| General Pentest | `01_commands.yaml` |
| CTF Competition | `02_ctf_kit.yaml` |
| Web Application | `03_web_bounty.yaml` |
| Windows Domain | `04_network_ad.yaml` |
| Mobile App | `05_mobile_iot.yaml` |
| AWS/Azure/GCP | `06_cloud_auditor.yaml` |
| Person/Company Research | `07_osint_detective.yaml` |
| WiFi Network | `08_wireless_radio.yaml` |
| Compromised System | `09_post_exploit.yaml` |

---

## 🔧 YAML Structure Reference

Each configuration file follows this schema:

```yaml
categories:
  category_key:
    name: "Category Display Name"
    tools:
      tool_key:
        name: "Tool Display Name"
        description: "Professional description of the tool"
        command: "binary_name -flag {param1} {param2}"
        params:
          - param1
          - param2
```

---

## 💡 Usage Examples

### Single Module Execution
```bash
# Run CTF-focused tools
tajaa --config configs/02_ctf_kit.yaml

# Run OSINT tools
tajaa --config configs/07_osint_detective.yaml
```

### Default Behavior
If no `--config` flag is provided, Tajaa CLI defaults to `configs/01_commands.yaml`.

---

## 📝 Adding Custom Modules

1. Create a new YAML file following the numbering convention: `10_your_module.yaml`
2. Follow the schema structure shown above
3. Reference it using: `tajaa --config configs/10_your_module.yaml`

---

**Maintained by:** Tajaa Team  
**Version:** 3.0.0  
**Last Updated:** December 14, 2025

