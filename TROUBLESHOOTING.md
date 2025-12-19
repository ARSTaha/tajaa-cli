# Installation Troubleshooting Guide

Common installation issues and solutions for Tajaa CLI.

---

## Error: externally-managed-environment

### Problem
```
error: externally-managed-environment
× This environment is externally managed
```

### Cause
Modern Python installations (Kali Linux 2023+, Ubuntu 23.04+, Debian 12+) use PEP 668 to prevent system-wide package installations that could break the OS.

### Solution (Recommended)

Use a virtual environment:

```bash
# Navigate to project directory
cd tajaa-cli

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Tajaa CLI
python3 main.py
```

### Alternative Solutions

#### Option 2: Using pipx (for single application)
```bash
# Install pipx
sudo apt install pipx

# Not recommended for Tajaa CLI (designed for single-file apps)
```

#### Option 3: System packages (limited)
```bash
# Install available system packages
sudo apt install python3-yaml python3-typer python3-rich

# Note: Not all dependencies may be available
```

#### Option 4: Override (NOT RECOMMENDED)
```bash
# This can break your system - use virtual environment instead
pip install -r requirements.txt --break-system-packages
```

---

## Error: Module Not Found

### Problem
```
ModuleNotFoundError: No module named 'typer'
```

### Solution
Ensure virtual environment is activated:

```bash
# Check if virtual environment is active
which python3
# Should show: /path/to/tajaa-cli/.venv/bin/python3

# If not active, activate it
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Error: Permission Denied

### Problem
```
PermissionError: [Errno 13] Permission denied
```

### Solution 1: Don't use sudo with pip in venv
```bash
# Wrong
sudo pip install -r requirements.txt

# Correct
source .venv/bin/activate
pip install -r requirements.txt
```

### Solution 2: Fix virtual environment permissions
```bash
# Fix ownership
sudo chown -R $USER:$USER .venv

# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Error: python3-venv not installed

### Problem
```
The virtual environment was not created successfully because ensurepip is not available.
```

### Solution
Install venv package:

```bash
# Debian/Ubuntu/Kali
sudo apt update
sudo apt install python3-venv

# Fedora/RHEL
sudo dnf install python3-virtualenv

# Arch Linux
sudo pacman -S python-virtualenv
```

---

## Error: Outdated pip/setuptools

### Problem
```
WARNING: pip is being invoked by an old script wrapper.
```

### Solution
```bash
# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Error: SSL Certificate Verification Failed

### Problem
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

### Solution
```bash
# Update CA certificates
sudo apt update
sudo apt install ca-certificates

# Or install with --trusted-host (temporary fix)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## Virtual Environment Best Practices

### Always Activate Before Use

```bash
# Add to ~/.bashrc or ~/.zshrc for convenience
alias tajaa='cd ~/tajaa-cli && source .venv/bin/activate && python3 main.py'
```

### Check Active Environment

```bash
# Method 1: Check prompt
# Should show: (.venv) user@host:~/tajaa-cli$

# Method 2: Check Python path
which python3
# Should show: /home/user/tajaa-cli/.venv/bin/python3

# Method 3: Check pip location
which pip
# Should show: /home/user/tajaa-cli/.venv/bin/pip
```

### Deactivate When Done

```bash
deactivate
```

---

## Kali Linux Specific Issues

### Issue: Python version mismatch

```bash
# Check Python version
python3 --version

# Ensure 3.8+
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Issue: Missing development headers

```bash
# Install build essentials
sudo apt install build-essential python3-dev
```

---

## Ubuntu/Debian Specific Issues

### Issue: deadsnakes PPA needed for newer Python

```bash
# Add PPA for newer Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv
```

---

## Testing Installation

```bash
# Activate environment
source .venv/bin/activate

# Test imports
python3 -c "import typer, yaml, rich; print('All imports successful')"

# Run tests
python3 test_components.py
python3 verify_security.py

# Run application
python3 main.py --help
```

---

## Clean Reinstall

If all else fails, start fresh:

```bash
# Remove virtual environment
rm -rf .venv

# Create new virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify
python3 test_components.py
```

---

## Still Having Issues?

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8 or higher
   ```

2. **Check virtual environment:**
   ```bash
   which python3  # Should point to .venv/bin/python3
   ```

3. **Check requirements.txt:**
   ```bash
   cat requirements.txt  # Verify file exists and is readable
   ```

4. **Report issue:**
   - GitHub Issues: https://github.com/ARSTaha/tajaa-cli/issues
   - Include: OS version, Python version, error message

---

## Quick Reference

```bash
# Complete installation workflow
git clone https://github.com/ARSTaha/tajaa-cli.git
cd tajaa-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py

# Daily usage
cd tajaa-cli
source .venv/bin/activate
python3 main.py

# When finished
deactivate
```

---

**Author:** Tajaa  
**Last Updated:** December 19, 2025

