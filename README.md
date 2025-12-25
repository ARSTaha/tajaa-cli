<p align="center">
  <img src="https://img.shields.io/badge/Version-5.0.0-00FFFF?style=for-the-badge&logo=hackthebox&logoColor=white" alt="Version"/>
  <img src="https://img.shields.io/badge/Tools-480+-FF00FF?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Tools"/>
  <img src="https://img.shields.io/badge/Python-3.12+-00FF00?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-FFFF00?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=30&duration=3000&pause=1000&color=00FFFF&center=true&vCenter=true&width=600&lines=TAJAA+CLI;The+Ultimate+Cyber+Security+Framework;480%2B+Tools.+One+Interface.;From+the+Future.+For+the+Elite." alt="Typing SVG" />
</p>

```
████████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██    ██████████╗  ███████╗      ██╗  ███████╗  ███████╗                      ██
██    ╚══██╔═══╝  ██╔═══██║      ██║  ██╔═══██║ ██╔═══██║                     ██
██       ██║      ████████║      ██║  ████████║ ████████║                     ██
██       ██║      ██╔═══██║ ██   ██║  ██╔═══██║ ██╔═══██║                     ██
██       ██║      ██║   ██║ ╚█████╔╝  ██║   ██║ ██║   ██║                     ██
██       ╚═╝      ╚═╝   ╚═╝  ╚════╝   ╚═╝   ╚═╝ ╚═╝   ╚═╝                     ██
██                                                                            ██
██              ⚡ CYBER SECURITY FRAMEWORK v5.0 ⚡                            ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████
```

---

## 🌟 The Manifesto

> *"In the digital battlefield, the tools you wield define your legacy. Tajaa doesn't just run commands—it orchestrates digital warfare."*

**Tajaa CLI** isn't another hacking framework. It's a revolution.

While others give you a list of tools, Tajaa gives you **intelligence**. While others make you type commands, Tajaa **thinks ahead**. While others look like they're from 2010, Tajaa **looks like 2030**.

This is the framework that makes Metasploit look like a calculator.

---

## 🚀 Features That Redefine Possible

### 🧠 **The Tajaa Brain** — Intelligence Over Raw Power

```
┌─────────────────────────────────────────────────────────────────┐
│  💡 RECOMMENDED TOOLS                                           │
│  ─────────────────────────────────────────                      │
│  ▸ nikto      HTTP service detected - web vulnerability scanner │
│  ▸ gobuster   HTTP service - fast directory scanner             │
│  ▸ sqlmap     HTTP service - SQL injection testing              │
│  ▸ sslscan    HTTPS service - SSL/TLS scanner                   │
└─────────────────────────────────────────────────────────────────┘
```

- **Context-Aware Suggestions**: Scan a target, find Port 80 open? Tajaa automatically queues Nikto, Dirb, and SQLMap. It thinks so you don't have to.
  
- **Fuzzy Search**: 480+ tools at your fingertips. Type "sql" and watch magic happen with rapidfuzz-powered instant matching.

- **Attack Chain Automation**: Why run tools one by one when you can orchestrate entire attack workflows?
  ```
  🔗 Web Recon Chain
  ├── Step 1: Port Scan (nmap)
  ├── Step 2: Technology Detection (whatweb)
  ├── Step 3: Directory Bruteforce (gobuster)
  └── Step 4: Vulnerability Scan (nikto)
  ```

### 💾 **Database Integration** — Memory That Persists

- **SQLite-powered persistence**: Every scan, every finding, every target—stored and indexed.
- **Cross-tool data sharing**: Nmap finds ports → automatically fed to service-specific tools.
- **Session continuity**: Close your terminal. Come back tomorrow. Pick up exactly where you left off.

### ⚡ **Asynchronous Core** — Speed Redefined

- **Non-blocking execution**: Run a background port scan while configuring your next attack.
- **Parallel tool execution**: Launch multiple tools simultaneously without freezing.
- **Real-time output streaming**: Watch results flow in live.

### 🎨 **Hyper-Modern UI** — The "Wow" Factor

```
╔══════════════════════════════════════════════════════════════════╗
║  ████████╗  __ _   (_)  __ _    __ _   ⚡ v5.0  💀               ║
║  ╚══██╔══╝ / _` |  | | / _` |  / _` |   Cyber Security Framework ║
║     ██║   | (_| |  | || (_| | | (_| |   ─────────────────────── ║
║     ╚═╝    \__,_| _/ | \__,_|  \__,_|   By Tajaa                 ║
║                  |__/                                            ║
╚══════════════════════════════════════════════════════════════════╝
```

- **Cinematic Intro**: Matrix-style boot sequence that makes every session feel legendary.
- **Cyberpunk Aesthetic**: Neon cyan, magenta, and green. Dark backgrounds. Clean tables.
- **Status Emojis**: 💀🔒🚀🎯 — Because elite hackers deserve elite visuals.

---

## 📦 Installation

### One-Line Install (Kali Linux)

```bash
git clone https://github.com/ARSTaha/tajaa-cli.git && cd tajaa-cli && chmod +x install.sh && ./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Launch
python main.py
```

### Requirements

- Python 3.12+
- Kali Linux (recommended) or any Linux distribution
- 480+ security tools (install with `chmod +x install_arsenal.sh && sudo ./install_arsenal.sh`)

---

## 🎮 Usage

### Launch

```bash
# Standard launch with cinematic intro
python main.py

# Quick launch (skip intro)
python main.py --skip-intro

# Show version
python main.py --version
```

### Navigation

```
🔍 Search Tools    — Fuzzy search across 480+ tools
🔗 Attack Chains   — Execute multi-step workflows
🎯 Set Target      — Define your target for smart suggestions
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Navigate |
| `Enter` | Select |
| `q` | Quit |
| `b` | Back |
| `Ctrl+C` | Cancel operation |

---

## 🏗️ Architecture

```
tajaa-cli/
├── main.py              # Entry point & orchestrator
├── core/
│   ├── database.py      # SQLite async database layer
│   ├── engine.py        # Async execution engine
│   ├── intelligence.py  # AI-like suggestion system
│   ├── plugin.py        # Dynamic plugin architecture
│   ├── session.py       # Session & state management
│   └── ui.py            # Cyberpunk UI components
├── configs/
│   ├── 01_commands.yaml
│   ├── 02_ctf_kit.yaml
│   ├── 03_web_bounty.yaml
│   ├── 04_network_ad.yaml
│   ├── 05_mobile_iot.yaml
│   ├── 06_cloud_auditor.yaml
│   ├── 07_osint_detective.yaml
│   ├── 08_wireless_radio.yaml
│   └── 09_post_exploit.yaml
├── modules/
│   ├── recon/
│   ├── web/
│   ├── wireless/
│   ├── exploitation/
│   ├── post_exploitation/
│   └── ...
├── data/                # SQLite database & sessions
├── logs/                # Execution logs
└── utils/               # Helper utilities
```

---

## 🔧 Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| 🔍 Reconnaissance | 50+ | Network scanning, enumeration, OSINT |
| 🌐 Web Applications | 80+ | Web vulnerability scanning, exploitation |
| 📡 Wireless | 40+ | WiFi cracking, Bluetooth, radio |
| 🎭 Sniffing | 30+ | Packet capture, analysis, MITM |
| 💀 Exploitation | 60+ | Exploit frameworks, payloads |
| 🔓 Post-Exploitation | 50+ | Privilege escalation, persistence |
| 🕵️ OSINT | 40+ | Open source intelligence gathering |
| 📱 Mobile/IoT | 30+ | Android, iOS, embedded systems |
| ☁️ Cloud | 25+ | AWS, Azure, GCP security |
| 🏁 CTF Kit | 45+ | CTF-specific tools and utilities |

---

## 🔗 Attack Chains

Pre-built attack workflows that automate the entire pentesting process:

### Web Recon
```
Port Scan → Technology Detection → Directory Bruteforce → Vulnerability Scan
```

### Network Enumeration
```
Host Discovery → Full Port Scan → Service Detection → Vulnerability Scripts
```

### SMB Enumeration
```
SMB Version → Enum4linux → Share Enumeration → Null Session Test
```

### SQL Injection
```
Parameter Discovery → SQLi Detection → Database Enumeration → Data Dump
```

### Linux PrivEsc
```
System Info → LinPEAS → SUID Check → Sudo Permissions
```

---

## 🎯 Smart Suggestions

Tajaa learns from your scans and suggests the next logical tools:

| Discovery | Suggested Tools |
|-----------|----------------|
| Port 80/443 | nikto, dirb, gobuster, sqlmap |
| Port 22 | ssh-audit, hydra |
| Port 445 | enum4linux, smbclient, crackmapexec |
| Port 3306 | mysql, hydra |
| Port 88 | kerbrute, GetNPUsers.py |
| Port 3389 | xfreerdp, crowbar |

---

## 📊 Database Schema

Tajaa stores everything for cross-tool intelligence:

- **Targets**: IP addresses, domains, URLs
- **Scans**: Tool executions with full output
- **Findings**: Ports, services, vulnerabilities, credentials
- **Sessions**: State persistence and history
- **Attack Chains**: Custom workflows

---

## 🛡️ Security Considerations

- **Input Validation**: All user inputs are sanitized against injection attacks
- **No External Connections**: Tajaa runs entirely locally
- **Secure Storage**: Sensitive findings are stored in local SQLite
- **Sudo Handling**: Graceful privilege escalation requests

---

## 🤝 Contributing

Tajaa is built for the community. Contributions welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Tajaa**

*"Building tools that make the impossible feel inevitable."*

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-00FFFF?style=flat-square&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Built%20for-Kali%20Linux-FF00FF?style=flat-square&logo=kalilinux" alt="Kali"/>
  <img src="https://img.shields.io/badge/Status-Elite-00FF00?style=flat-square" alt="Status"/>
</p>

<p align="center">
  <b>💀 Stay Elite. Stay Tajaa. 💀</b>
</p>

