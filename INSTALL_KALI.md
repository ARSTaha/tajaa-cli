# Tajaa CLI - Kali Linux Installation Guide

Complete step-by-step installation guide for Kali Linux users.

---

## Prerequisites

Before you begin, ensure you have:

- **Kali Linux** (2023.1 or newer recommended)
- **Python 3.8+** (pre-installed on Kali)
- **Git** (pre-installed on Kali)
- **Internet connection** for downloading dependencies

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
cd ~
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli
```

**What this does:**
- Downloads the Tajaa CLI framework to your home directory
- Creates a folder called `tajaa-cli`
- Navigates into that folder

---

## Step 2: Run the Automated Installer

Make the installer executable and run it:

```bash
chmod +x install.sh
./install.sh
```

**What this does:**
- Checks your Python version (must be 3.8+)
- Installs `python3-venv` if not present
- Creates a virtual environment in `.venv/`
- Installs all required Python packages

**Expected output:**
```
================================
  Tajaa CLI Installer
================================

[1/4] Checking Python version...
✓ Python 3.11.9 detected

[2/4] Checking python3-venv...
✓ python3-venv available

[3/4] Creating virtual environment...
✓ Virtual environment created

[4/4] Installing dependencies...
✓ Dependencies installed

================================
  Installation Complete!
================================
```

---

## Step 3: Activate the Virtual Environment

**IMPORTANT:** You must activate the virtual environment every time you use Tajaa CLI.

```bash
source .venv/bin/activate
```

**How to tell it's active:**
- Your terminal prompt will show `(.venv)` at the beginning
- Example: `(.venv) ┌──(kali㉿kali)-[~/tajaa-cli]`

---

## Step 4: Run Tajaa CLI

Now you can run the framework:

```bash
python3 main.py
```

**To load a specific module:**

```bash
# CTF toolkit
python3 main.py --config configs/02_ctf_kit.yaml

# Web security
python3 main.py --config configs/03_web_bounty.yaml

# Cloud auditing
python3 main.py --config configs/06_cloud_auditor.yaml
```

---

## Step 5: Create Quick Aliases (Optional but Recommended)

To save time, create shell aliases:

### For Bash (Kali default):

```bash
nano ~/.bashrc
```

Add these lines at the end:

```bash
# Tajaa CLI Aliases
alias tajaa='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py'
alias tajaa-ctf='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/02_ctf_kit.yaml'
alias tajaa-web='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/03_web_bounty.yaml'
alias tajaa-ad='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/04_network_ad.yaml'
alias tajaa-mobile='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/05_mobile_iot.yaml'
alias tajaa-cloud='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/06_cloud_auditor.yaml'
alias tajaa-osint='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/07_osint_detective.yaml'
alias tajaa-wireless='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/08_wireless_radio.yaml'
alias tajaa-post='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py --config configs/09_post_exploit.yaml'
```

Save and exit (Ctrl+X, then Y, then Enter), then reload:

```bash
source ~/.bashrc
```

### For Zsh:

```bash
nano ~/.zshrc
```

Add the same aliases, save, and reload:

```bash
source ~/.zshrc
```

**Now you can use:**

```bash
tajaa          # Launch default module
tajaa-ctf      # Launch CTF toolkit
tajaa-web      # Launch web security module
tajaa-cloud    # Launch cloud auditing module
```

---

## Step 6: Install Optional Arsenal (Recommended)

This installs additional tools like CyberChef, LinPEAS, and SecLists wordlists:

```bash
# Make sure you're still in the tajaa-cli directory
cd ~/tajaa-cli

# Run the arsenal installer with sudo (it installs system-wide tools)
sudo bash install_arsenal.sh
```

**What this installs:**
- CyberChef (local HTML version) → `/opt/tajaa-tools/cyberchef/`
- LinPEAS, WinPEAS, pspy64 → `/opt/tajaa-tools/payloads/`
- SecLists wordlists → `/opt/wordlists/`

---

## Quick Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'typer'`

**Solution:**
You forgot to activate the virtual environment. Run:

```bash
cd ~/tajaa-cli
source .venv/bin/activate
```

### Problem: `externally-managed-environment` error during install

**Solution:**
The installer handles this automatically by creating a virtual environment. If you see this error, it means you tried to install packages system-wide. Always use the virtual environment.

### Problem: Alias doesn't work

**Solution:**
1. Check that you added the aliases to the correct file (`~/.bashrc` or `~/.zshrc`)
2. Make sure you reloaded the shell: `source ~/.bashrc`
3. Verify the path in the alias matches where you cloned the repo

### Problem: Permission denied on `install.sh`

**Solution:**
```bash
chmod +x install.sh
./install.sh
```

---

## Uninstallation

If you want to remove Tajaa CLI:

```bash
# Remove the main directory
rm -rf ~/tajaa-cli

# Remove optional arsenal tools (if installed)
sudo rm -rf /opt/tajaa-tools
sudo rm -rf /opt/wordlists

# Remove aliases from ~/.bashrc or ~/.zshrc
nano ~/.bashrc  # or ~/.zshrc
# Delete the Tajaa CLI alias lines, save, and reload
source ~/.bashrc
```

---

## Daily Usage Workflow

Every time you want to use Tajaa CLI:

### Method 1: Manual Activation

```bash
cd ~/tajaa-cli
source .venv/bin/activate
python3 main.py --config configs/02_ctf_kit.yaml
```

### Method 2: Using Aliases (Recommended)

```bash
tajaa-ctf
```

That's it! The alias handles everything automatically.

---

## Next Steps

- Read the [README.md](README.md) for feature overview
- Check [CONFIG_CATALOG.md](CONFIG_CATALOG.md) for complete tool listings
- See [EXAMPLES.md](EXAMPLES.md) for usage examples
- Review [SECURITY.md](SECURITY.md) for security features
- Visit [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

**Author:** Tajaa  
**GitHub:** https://github.com/ARSTaha/tajaa-cli  
**License:** MIT

Happy hacking! 🎯

