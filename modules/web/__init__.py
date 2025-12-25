"""Tajaa Web Application Plugins"""

from core.plugin import PluginBase, PluginMetadata, PluginCategory
from typing import Dict, List, Any
import re


class NiktoScanner(PluginBase):
    """Nikto web vulnerability scanner."""

    metadata = PluginMetadata(
        name="Nikto",
        description="Web server vulnerability scanner",
        category=PluginCategory.WEB,
        tags=['web', 'vulnerability', 'scanner'],
        dependencies=['nikto']
    )

    @property
    def command_template(self) -> str:
        return "nikto -h {url} -o {output} -Format txt"

    @property
    def required_params(self) -> List[str]:
        return ['url']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {'output': 'nikto_results.txt'}

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Nikto output."""
        results = {
            'vulnerabilities': [],
            'info': [],
            'server': ''
        }

        # Extract server info
        server_match = re.search(r'Server: (.+)', output)
        if server_match:
            results['server'] = server_match.group(1)

        # Extract vulnerabilities
        vuln_pattern = r'\+ (OSVDB-\d+|[A-Z]{3,}:.*?): (.+)'
        for match in re.finditer(vuln_pattern, output):
            results['vulnerabilities'].append({
                'id': match.group(1),
                'description': match.group(2)
            })

        return results

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """Suggest tools based on findings."""
        suggestions = []
        vulns = findings.get('vulnerabilities', [])

        for vuln in vulns:
            desc = vuln.get('description', '').lower()
            if 'sql' in desc:
                suggestions.append('sqlmap')
            if 'xss' in desc:
                suggestions.append('xsstrike')
            if 'directory' in desc or 'listing' in desc:
                suggestions.append('gobuster')

        return list(set(suggestions))


class GobusterDir(PluginBase):
    """Gobuster directory brute-forcing."""

    metadata = PluginMetadata(
        name="Gobuster Dir",
        description="Directory/file enumeration with Gobuster",
        category=PluginCategory.WEB,
        tags=['web', 'directory', 'bruteforce', 'enumeration'],
        dependencies=['gobuster']
    )

    @property
    def command_template(self) -> str:
        return "gobuster dir -u {url} -w {wordlist} -t {threads} -x {extensions} -o {output}"

    @property
    def required_params(self) -> List[str]:
        return ['url']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'wordlist': '/usr/share/wordlists/dirb/common.txt',
            'threads': '50',
            'extensions': 'php,html,txt,js',
            'output': 'gobuster_results.txt'
        }

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Gobuster output."""
        results = {
            'directories': [],
            'files': [],
            'status_codes': {}
        }

        pattern = r'/(\S+)\s+\(Status: (\d+)\)'
        for match in re.finditer(pattern, output):
            path = '/' + match.group(1)
            status = int(match.group(2))

            entry = {'path': path, 'status': status}

            if '.' in path.split('/')[-1]:
                results['files'].append(entry)
            else:
                results['directories'].append(entry)

            # Track status codes
            results['status_codes'][status] = results['status_codes'].get(status, 0) + 1

        return results

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """Suggest tools based on discovered paths."""
        suggestions = []
        dirs = findings.get('directories', [])
        files = findings.get('files', [])

        for d in dirs:
            path = d.get('path', '').lower()
            if 'admin' in path or 'login' in path:
                suggestions.append('hydra')
            if 'api' in path:
                suggestions.extend(['ffuf', 'postman'])
            if 'upload' in path:
                suggestions.append('upload-scanner')

        for f in files:
            path = f.get('path', '').lower()
            if path.endswith('.php'):
                suggestions.append('sqlmap')
            if '.git' in path:
                suggestions.append('git-dumper')
            if 'config' in path:
                suggestions.append('curl')

        return list(set(suggestions))


class SQLMapAuto(PluginBase):
    """SQLMap SQL injection tool."""

    metadata = PluginMetadata(
        name="SQLMap",
        description="Automatic SQL injection and database takeover tool",
        category=PluginCategory.WEB,
        tags=['web', 'sqli', 'database', 'exploitation'],
        dependencies=['sqlmap']
    )

    @property
    def command_template(self) -> str:
        return "sqlmap -u '{url}' --batch --random-agent {options}"

    @property
    def required_params(self) -> List[str]:
        return ['url']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'options': '--dbs'
        }

    @property
    def param_descriptions(self) -> Dict[str, str]:
        return {
            'url': 'Target URL with parameter (e.g., http://site.com/page?id=1)',
            'options': 'SQLMap options (--dbs, --tables, --dump, etc.)'
        }


class WhatWebScan(PluginBase):
    """WhatWeb technology fingerprinting."""

    metadata = PluginMetadata(
        name="WhatWeb",
        description="Web technology fingerprinting and identification",
        category=PluginCategory.WEB,
        tags=['web', 'fingerprint', 'technology', 'recon'],
        dependencies=['whatweb']
    )

    @property
    def command_template(self) -> str:
        return "whatweb -a {aggression} {url}"

    @property
    def required_params(self) -> List[str]:
        return ['url']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {'aggression': '3'}

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse WhatWeb output."""
        results = {
            'technologies': [],
            'cms': '',
            'server': '',
            'frameworks': []
        }

        # Common patterns
        tech_patterns = {
            'WordPress': 'wordpress',
            'Drupal': 'drupal',
            'Joomla': 'joomla',
            'Apache': 'apache',
            'Nginx': 'nginx',
            'PHP': 'php',
            'jQuery': 'jquery',
            'Bootstrap': 'bootstrap'
        }

        for tech, keyword in tech_patterns.items():
            if keyword.lower() in output.lower():
                results['technologies'].append(tech)

        return results

