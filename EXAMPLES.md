# Examples & Usage Guide

## 🎯 Quick Start Examples

### Example 1: Scanning a Target with Hostname Support

**Before (IPv4 only):**
```
Enter target ip: scanme.nmap.org
✗ Invalid IPv4 address: 'scanme.nmap.org'. Expected format: xxx.xxx.xxx.xxx
```

**After (IPv4 + Hostnames):**
```
Enter target ip: scanme.nmap.org
✓ Command generated successfully!

╭─ Generated Command ──────────────────────────────────╮
│ nmap -T4 -F 'scanme.nmap.org'                        │
╰──────────────────────────────────────────────────────╯
```

**Valid inputs:**
- `192.168.1.1` (IPv4)
- `scanme.nmap.org` (hostname)
- `target.htb` (HTB machine)
- `internal.local` (local domain)
- `test-server.corp.example.com` (FQDN)

### Example 2: Web Scanning with URL Normalization

**Scenario: WhatWeb Scan**

**Input:** `example.com`
```
╭─ Generated Command ──────────────────────────────────╮
│ whatweb 'http://example.com'                         │
╰──────────────────────────────────────────────────────╯
```

**Input:** `http://example.com`
```
╭─ Generated Command ──────────────────────────────────╮
│ whatweb 'http://example.com'                         │
╰──────────────────────────────────────────────────────╯
```

**Input:** `http://http://example.com` (accidental duplicate)
```
╭─ Generated Command ──────────────────────────────────╮
│ whatweb 'http://example.com'                         │  ← Fixed automatically!
╰──────────────────────────────────────────────────────╯
```

**Input:** `https://secure.example.com/path`
```
╭─ Generated Command ──────────────────────────────────╮
│ whatweb 'https://secure.example.com/path'            │
╰──────────────────────────────────────────────────────╯
```

### Example 3: Configurable Wordlists

**Gobuster Directory Brute Force**

**Using Default:**
```
Enter target url: http://example.com
Enter wordlist (default: /usr/share/wordlists/dirb/common.txt): [Press Enter]

╭─ Generated Command ──────────────────────────────────────────────────╮
│ gobuster dir -u 'http://example.com' -w '/usr/share/wordlists/dirb/common.txt' │
╰──────────────────────────────────────────────────────────────────────╯
```

**Using Custom Wordlist:**
```
Enter target url: http://example.com
Enter wordlist (default: /usr/share/wordlists/dirb/common.txt): /opt/custom-wordlists/big.txt

╭─ Generated Command ──────────────────────────────────────────────────╮
│ gobuster dir -u 'http://example.com' -w '/opt/custom-wordlists/big.txt' │
╰──────────────────────────────────────────────────────────────────────╯
```

### Example 4: Command Injection Prevention

**Malicious Input Attempt:**
```
Enter search term: wordpress; rm -rf /

✗ Security Warning: Input contains potentially dangerous characters: 'wordpress; rm -rf /'
This could lead to command injection. Please use alphanumeric values.

Continue with this input anyway? [y/N]: n
```

**If User Confirms Anyway:**
```
Continue with this input anyway? [y/N]: y

╭─ Generated Command ──────────────────────────────────╮
│ searchsploit 'wordpress; rm -rf /'                   │  ← Safely quoted!
╰──────────────────────────────────────────────────────╯

Actual execution: searchsploit searches for "wordpress; rm -rf /" as a literal string
NOT: searchsploit wordpress THEN rm -rf /
```

**How it works:**
- `shlex.quote()` wraps the input in single quotes
- Shell treats the entire input as a single argument
- No command injection possible

### Example 5: SSH Brute Force with Configurable Wordlists

**Using Defaults:**
```
Enter target ip: 192.168.1.100
Enter users wordlist (default: /usr/share/wordlists/metasploit/unix_users.txt): [Press Enter]
Enter passwords wordlist (default: /usr/share/wordlists/rockyou.txt): [Press Enter]

╭─ Generated Command ──────────────────────────────────────────────────╮
│ hydra -L '/usr/share/wordlists/metasploit/unix_users.txt'           │
│       -P '/usr/share/wordlists/rockyou.txt'                          │
│       ssh://'192.168.1.100'                                          │
╰──────────────────────────────────────────────────────────────────────╯
```

**Using Custom Lists:**
```
Enter target ip: target.htb
Enter users wordlist (default: /usr/share/wordlists/metasploit/unix_users.txt): /tmp/custom-users.txt
Enter passwords wordlist (default: /usr/share/wordlists/rockyou.txt): /tmp/custom-passwords.txt

╭─ Generated Command ──────────────────────────────────────────────────╮
│ hydra -L '/tmp/custom-users.txt' -P '/tmp/custom-passwords.txt'     │
│       ssh://'target.htb'                                             │
╰──────────────────────────────────────────────────────────────────────╯
```

## 🔧 Advanced Usage

### Running Different Modules

**CTF Kit:**
```bash
python main.py --config configs/02_ctf_kit.yaml
```

**Web Bounty Hunting:**
```bash
python main.py --config configs/03_web_bounty.yaml
```

**Active Directory:**
```bash
python main.py --config configs/04_network_ad.yaml
```

**OSINT Detective:**
```bash
python main.py --config configs/07_osint_detective.yaml
```

### Custom Log Files

```bash
python main.py --log ~/pentests/project-alpha/session.log
```

### Combining Options

```bash
python main.py --config configs/03_web_bounty.yaml --log ~/logs/web-pentest.txt
```

## 📋 Common Workflows

### Workflow 1: Basic Network Reconnaissance

```
1. Launch: python main.py
2. Select: Reconnaissance
3. Choose: Nmap - Quick Scan
4. Enter target: 192.168.1.0/24
5. Review command
6. Execute
```

### Workflow 2: Web Application Testing

```
1. Launch: python main.py --config configs/03_web_bounty.yaml
2. Select: Web Attacks
3. Choose: Gobuster - Directory Brute Force
4. Enter target URL: https://example.com
5. Enter wordlist: [Use default or custom]
6. Review and execute
```

### Workflow 3: Exploit Research

```
1. Launch: python main.py
2. Select: Exploitation
3. Choose: SearchSploit - Exploit Search
4. Enter search term: apache 2.4.49
5. Review results
6. Return to menu for more searches
```

## 🛡️ Security Best Practices

### DO ✅

1. **Review Commands Before Execution**
   ```
   Always check the "Generated Command" panel
   Verify all parameters are correct
   Ensure target is authorized
   ```

2. **Use Proper Authorization**
   ```
   Only scan systems you have permission to test
   Keep authorization documentation handy
   Respect scope boundaries
   ```

3. **Verify File Paths**
   ```
   Check that wordlists exist before running
   Use absolute paths for clarity
   Test with small wordlists first
   ```

4. **Monitor Execution**
   ```
   Watch command output for errors
   Use Ctrl+C to stop if needed
   Check logs for audit trail
   ```

### DON'T ❌

1. **Don't Bypass Security Warnings Without Understanding**
   ```
   ✗ Enter search term: test; cat /etc/passwd
   ⚠ Security Warning: Input contains potentially dangerous characters
   Continue anyway? NO - unless you have a valid reason
   ```

2. **Don't Use Unauthorized Targets**
   ```
   ✗ Never scan systems without permission
   ✗ Respect rate limits and don't DOS
   ✗ Follow responsible disclosure
   ```

3. **Don't Trust Default Wordlists Blindly**
   ```
   ✗ Defaults are suggestions, not guarantees
   ✗ Verify paths exist on your system
   ✗ Use appropriate wordlists for the task
   ```

## 🎓 Tips & Tricks

### Tip 1: Quick Target Switching

Use hostnames in your `/etc/hosts`:
```bash
echo "192.168.1.100 target.local" | sudo tee -a /etc/hosts
```

Now you can use:
```
Enter target: target.local
```

### Tip 2: Custom Wordlist Collections

Organize your wordlists:
```bash
/opt/wordlists/
├── web/
│   ├── common.txt
│   ├── big.txt
│   └── raft-large.txt
├── passwords/
│   ├── rockyou.txt
│   ├── fasttrack.txt
│   └── custom.txt
└── users/
    ├── unix_users.txt
    └── windows_users.txt
```

### Tip 3: Session Logging

Keep organized logs:
```bash
mkdir -p ~/pentests/project-name/logs
python main.py --log ~/pentests/project-name/logs/session-$(date +%Y%m%d).txt
```

### Tip 4: Command Clipboard

Commands are automatically copied to clipboard:
```
1. Run a tool in Tajaa
2. Command is copied automatically
3. Paste into terminal, notes, or reports
```

### Tip 5: Multiple Terminals

For complex scenarios:
```
Terminal 1: python main.py                    # Main interface
Terminal 2: tail -f session_logs.txt          # Watch logs
Terminal 3: [Manual commands or monitoring]   # Additional work
```

## 🔍 Troubleshooting

### Issue: Wordlist Not Found

**Error:**
```
✗ File not found: '/usr/share/wordlists/dirb/common.txt'
```

**Solutions:**
1. Install wordlists: `sudo apt install wordlists`
2. Use custom path: `/opt/SecLists/Discovery/Web-Content/common.txt`
3. Find your wordlists: `locate common.txt`

### Issue: Tool Not Found

**Warning:**
```
⚠ Warning: Tool 'rustscan' not found in system PATH!
```

**Solutions:**
1. Install tool: `sudo apt install rustscan`
2. Check PATH: `which rustscan`
3. Install manually if needed

### Issue: Permission Denied

**Error:**
```
Error executing command: Permission denied
```

**Solutions:**
1. Run tool with sudo if needed (not the Python script)
2. Check file permissions on wordlists
3. Verify user has network access rights

### Issue: Command Fails to Execute

**Problem:** Command exits with non-zero code

**Solutions:**
1. Review the command for syntax errors
2. Test command manually in terminal
3. Check tool documentation
4. Verify all parameters are valid

## 📊 Input Validation Reference

| Parameter Type | Valid Examples | Invalid Examples |
|---------------|----------------|------------------|
| **IP Address** | `192.168.1.1`, `10.0.0.1` | `999.999.999.999`, `invalid` |
| **Hostname** | `example.com`, `target.htb`, `local.domain` | `exa mple.com`, `../../etc` |
| **URL** | `http://example.com`, `https://test.com/path` | `htp://wrong`, `not a url` |
| **Port** | `80`, `443`, `8080`, `65535` | `0`, `70000`, `abc` |
| **File Path** | `/usr/share/wordlists/common.txt` | `../../../etc/passwd` |
| **Search Term** | `wordpress`, `apache 2.4` | `test; rm -rf /` (warned) |

## 🚀 Performance Tips

1. **Start with Quick Scans**
   - Use Nmap Quick Scan before Full Scan
   - Test with small wordlists first
   - Verify connectivity before heavy scans

2. **Use Appropriate Tools**
   - RustScan for fast port discovery
   - Nmap for detailed analysis
   - Targeted tools for specific services

3. **Monitor Resource Usage**
   - Watch CPU and network during scans
   - Use Ctrl+C to interrupt if needed
   - Space out heavy scans

## 📝 Example Session

```
$ python main.py

 _____  _     _   _     _    
|_   _|/ \   | | / \   / \   
  | | / _ \  | |/ _ \ / _ \  
  | |/ ___ \ | / ___ / ___ \ 
  |_/_/   \_\___/   \_/   \_\

╭─────────────────────────────────────────╮
│ Modular Cyber Security Framework        │
│ Version 3.0.0 | 8 Specialized Domains   │
╰─────────────────────────────────────────╯

Available Categories
┏━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ # ┃ Category            ┃ Tools Count ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1 │ Reconnaissance      │ 5           │
│ 2 │ Web Attacks         │ 4           │
│ 3 │ Exploitation        │ 3           │
│ 4 │ Network Analysis    │ 3           │
│ 5 │ Service Enumeration │ 4           │
│ 6 │ Wireless Attacks    │ 3           │
└───┴─────────────────────┴─────────────┘

Select a category: Reconnaissance

Select a tool:
→ Nmap - Quick Scan
    └─ Fast port scan of the 1000 most common ports
  Nmap - Full Port Scan
    └─ Comprehensive scan of all 65535 ports
  ...

🔧 Preparing: Nmap - Quick Scan
Fast port scan of the 1000 most common ports

Enter target ip: scanme.nmap.org

╭─ Generated Command ──────────────────────╮
│ nmap -T4 -F 'scanme.nmap.org'            │
╰──────────────────────────────────────────╯

✓ Command copied to clipboard

Execute this command now? [Y/n]: y

⠋ Executing command...
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for scanme.nmap.org (45.33.32.156)
...

✓ Command executed successfully

Return to main menu? [Y/n]: 
```

---

**Happy Hacking! 🔒**

