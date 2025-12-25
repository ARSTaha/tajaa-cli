"""
Tajaa Utility Functions
Common helpers for the Tajaa CLI framework.
Author: Tajaa
"""

import os
import re
import socket
import ipaddress
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple


def is_valid_ip(ip: str) -> bool:
    """Check if string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_cidr(cidr: str) -> bool:
    """Check if string is a valid CIDR notation."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def is_valid_hostname(hostname: str) -> bool:
    """Check if string is a valid hostname."""
    if len(hostname) > 255:
        return False
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, hostname))


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL."""
    pattern = r'^https?://[^\s<>\"\']+$'
    return bool(re.match(pattern, url))


def is_valid_port(port: Any) -> bool:
    """Check if value is a valid port number."""
    try:
        p = int(port)
        return 1 <= p <= 65535
    except (ValueError, TypeError):
        return False


def resolve_hostname(hostname: str) -> Optional[str]:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def parse_ports(port_string: str) -> List[int]:
    """
    Parse port string into list of ports.
    Supports: single (80), range (1-100), comma-separated (22,80,443)
    """
    ports = set()

    for part in port_string.split(','):
        part = part.strip()
        if '-' in part:
            try:
                start, end = part.split('-')
                for p in range(int(start), int(end) + 1):
                    if is_valid_port(p):
                        ports.add(p)
            except ValueError:
                continue
        else:
            try:
                p = int(part)
                if is_valid_port(p):
                    ports.add(p)
            except ValueError:
                continue

    return sorted(ports)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing dangerous characters."""
    # Remove path separators and null bytes
    filename = filename.replace('/', '_').replace('\\', '_').replace('\x00', '')
    # Remove other dangerous characters
    filename = re.sub(r'[<>:"|?*]', '_', filename)
    # Limit length
    return filename[:200]


def generate_timestamp_filename(prefix: str, extension: str = 'txt') -> str:
    """Generate a timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def calculate_file_hash(filepath: Path, algorithm: str = 'md5') -> str:
    """Calculate hash of a file."""
    hash_func = getattr(hashlib, algorithm)()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def get_service_by_port(port: int) -> str:
    """Get common service name for a port."""
    services = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        111: 'RPC',
        135: 'MSRPC',
        139: 'NetBIOS',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        993: 'IMAPS',
        995: 'POP3S',
        1433: 'MSSQL',
        1521: 'Oracle',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        6379: 'Redis',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt',
        27017: 'MongoDB',
    }
    return services.get(port, 'Unknown')


def extract_ips_from_text(text: str) -> List[str]:
    """Extract all valid IP addresses from text."""
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    matches = re.findall(pattern, text)
    return [ip for ip in matches if is_valid_ip(ip)]


def extract_urls_from_text(text: str) -> List[str]:
    """Extract all URLs from text."""
    pattern = r'https?://[^\s<>\"\']+(?<![\.,;:!?\)\]\}])'
    return re.findall(pattern, text)


def extract_emails_from_text(text: str) -> List[str]:
    """Extract all email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def is_root() -> bool:
    """Check if running as root/admin."""
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else os.getuid() == 0


def detect_os() -> str:
    """Detect operating system."""
    import platform
    system = platform.system().lower()
    if system == 'linux':
        # Try to detect distro
        try:
            with open('/etc/os-release') as f:
                content = f.read()
                if 'kali' in content.lower():
                    return 'kali'
                if 'ubuntu' in content.lower():
                    return 'ubuntu'
                if 'debian' in content.lower():
                    return 'debian'
                if 'arch' in content.lower():
                    return 'arch'
        except FileNotFoundError:
            pass
        return 'linux'
    return system


def format_duration(seconds: float) -> str:
    """Format duration in human readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


class ProgressTracker:
    """Simple progress tracking utility."""

    def __init__(self, total: int, description: str = "Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()

    def update(self, amount: int = 1) -> None:
        """Update progress by amount."""
        self.current = min(self.current + amount, self.total)

    @property
    def percentage(self) -> float:
        """Get current percentage."""
        return (self.current / self.total) * 100 if self.total > 0 else 0

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        return (datetime.now() - self.start_time).total_seconds()

    @property
    def eta(self) -> Optional[float]:
        """Estimate time to completion."""
        if self.current == 0:
            return None
        rate = self.current / self.elapsed
        remaining = self.total - self.current
        return remaining / rate if rate > 0 else None

    def __str__(self) -> str:
        eta_str = format_duration(self.eta) if self.eta else "N/A"
        return f"{self.description}: {self.percentage:.1f}% ({self.current}/{self.total}) - ETA: {eta_str}"

