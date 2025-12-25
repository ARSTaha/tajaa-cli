"""Tajaa Recon Plugins"""

from core.plugin import PluginBase, PluginMetadata, PluginCategory
from typing import Dict, List, Any


class NmapAdvanced(PluginBase):
    """Advanced Nmap scanner with result parsing."""

    metadata = PluginMetadata(
        name="Nmap Advanced",
        description="Advanced port scanner with service detection and scripting",
        category=PluginCategory.RECON,
        tags=['network', 'ports', 'scanner', 'enumeration', 'nse'],
        dependencies=['nmap']
    )

    @property
    def command_template(self) -> str:
        return "nmap {options} -p {ports} -oN {output} {target}"

    @property
    def required_params(self) -> List[str]:
        return ['target']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'ports': '-',
            'options': '-sC -sV -A',
            'output': 'nmap_scan.txt'
        }

    @property
    def param_descriptions(self) -> Dict[str, str]:
        return {
            'target': 'Target IP, hostname, or CIDR range',
            'ports': 'Ports to scan (default: all, or specify like 22,80,443)',
            'options': 'Nmap options (default: -sC -sV -A for comprehensive scan)',
            'output': 'Output filename for results'
        }

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Nmap output into structured data."""
        import re

        results = {
            'hosts': [],
            'ports': [],
            'services': [],
            'os_detection': [],
            'scripts': []
        }

        # Extract open ports
        port_pattern = r'(\d+)/(tcp|udp)\s+open\s+(\S+)(?:\s+(.*))?'
        for match in re.finditer(port_pattern, output):
            port_info = {
                'port': int(match.group(1)),
                'protocol': match.group(2),
                'service': match.group(3),
                'version': match.group(4) or ''
            }
            results['ports'].append(port_info['port'])
            results['services'].append(port_info)

        # Extract hosts
        host_pattern = r'Nmap scan report for (\S+)'
        for match in re.finditer(host_pattern, output):
            results['hosts'].append(match.group(1))

        # Extract OS detection
        os_pattern = r'OS details: (.+)'
        for match in re.finditer(os_pattern, output):
            results['os_detection'].append(match.group(1))

        return results

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """Suggest tools based on discovered services."""
        suggestions = []
        ports = findings.get('ports', [])
        services = findings.get('services', [])

        # Web services
        if 80 in ports or 443 in ports or 8080 in ports:
            suggestions.extend(['nikto', 'gobuster', 'dirb', 'whatweb'])

        # SSH
        if 22 in ports:
            suggestions.extend(['ssh-audit', 'hydra'])

        # SMB
        if 445 in ports or 139 in ports:
            suggestions.extend(['enum4linux', 'smbclient', 'crackmapexec'])

        # FTP
        if 21 in ports:
            suggestions.extend(['ftp-anon', 'hydra'])

        # MySQL
        if 3306 in ports:
            suggestions.extend(['mysql', 'hydra'])

        # Check for specific services
        for svc in services:
            service_name = svc.get('service', '').lower()
            if 'http' in service_name:
                suggestions.extend(['nikto', 'gobuster'])
            if 'ssh' in service_name:
                suggestions.append('ssh-audit')

        return list(set(suggestions))


class MasscanFast(PluginBase):
    """Masscan ultra-fast port scanner."""

    metadata = PluginMetadata(
        name="Masscan",
        description="Ultra-fast port scanner for large networks",
        category=PluginCategory.RECON,
        tags=['network', 'ports', 'fast', 'mass-scan'],
        dependencies=['masscan']
    )

    @property
    def command_template(self) -> str:
        return "sudo masscan {target} -p {ports} --rate {rate}"

    @property
    def required_params(self) -> List[str]:
        return ['target']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'ports': '1-65535',
            'rate': '10000'
        }

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Masscan output."""
        import re

        results = {'ports': [], 'hosts': []}
        pattern = r'Discovered open port (\d+)/(tcp|udp) on (\S+)'
        for match in re.finditer(pattern, output):
            results['ports'].append(int(match.group(1)))
            if match.group(3) not in results['hosts']:
                results['hosts'].append(match.group(3))

        return results


class RustScan(PluginBase):
    """RustScan - Modern fast port scanner."""

    metadata = PluginMetadata(
        name="RustScan",
        description="Fast port scanner written in Rust, pipes to Nmap",
        category=PluginCategory.RECON,
        tags=['network', 'ports', 'fast', 'rust'],
        dependencies=['rustscan']
    )

    @property
    def command_template(self) -> str:
        return "rustscan -a {target} --ulimit 5000 -- -sC -sV"

    @property
    def required_params(self) -> List[str]:
        return ['target']

