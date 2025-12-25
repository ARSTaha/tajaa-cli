"""
Tajaa Intelligence Module
AI-like recommendation system, fuzzy search, and attack chain orchestration.
Author: Tajaa
"""

import re
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict

try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


@dataclass
class ToolInfo:
    """Tool information for search and suggestions."""
    id: str
    name: str
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    port_relevance: List[int] = field(default_factory=list)  # Relevant ports
    service_relevance: List[str] = field(default_factory=list)  # Relevant services
    follows: List[str] = field(default_factory=list)  # Tools this naturally follows
    provides: List[str] = field(default_factory=list)  # What this tool provides
    requires: List[str] = field(default_factory=list)  # What this tool needs


@dataclass
class Suggestion:
    """A tool suggestion with reasoning."""
    tool_id: str
    tool_name: str
    category: str
    reason: str
    confidence: float  # 0.0 to 1.0
    priority: int = 0  # Higher = more important


class FuzzySearchEngine:
    """
    Fuzzy search engine for finding tools by name, description, or tags.
    Uses rapidfuzz for high-performance fuzzy matching.
    """

    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}
        self._search_index: Dict[str, List[str]] = defaultdict(list)

    def register_tool(self, tool: ToolInfo) -> None:
        """Register a tool for searching."""
        self.tools[tool.id] = tool

        # Build search index
        search_terms = [
            tool.name.lower(),
            tool.description.lower(),
            *[tag.lower() for tag in tool.tags],
            tool.category.lower(),
        ]

        for term in search_terms:
            words = re.split(r'\W+', term)
            for word in words:
                if word:
                    self._search_index[word].append(tool.id)

    def search(self, query: str, limit: int = 10, threshold: int = 60) -> List[Tuple[ToolInfo, int]]:
        """
        Search for tools matching the query.

        Args:
            query: Search query
            limit: Maximum results
            threshold: Minimum match score (0-100)

        Returns:
            List of (ToolInfo, score) tuples
        """
        if not query:
            return []

        query = query.lower().strip()
        results = []

        if RAPIDFUZZ_AVAILABLE:
            # Use rapidfuzz for fuzzy matching
            tool_names = {tid: t.name for tid, t in self.tools.items()}
            tool_descs = {tid: t.description for tid, t in self.tools.items()}

            # Search by name
            name_matches = process.extract(
                query,
                tool_names,
                scorer=fuzz.WRatio,
                limit=limit * 2
            )

            # Search by description
            desc_matches = process.extract(
                query,
                tool_descs,
                scorer=fuzz.partial_ratio,
                limit=limit
            )

            # Combine and deduplicate
            seen = set()
            combined = []

            for match_name, score, tool_id in name_matches:
                if score >= threshold and tool_id not in seen:
                    seen.add(tool_id)
                    combined.append((self.tools[tool_id], score))

            for match_desc, score, tool_id in desc_matches:
                if score >= threshold and tool_id not in seen:
                    seen.add(tool_id)
                    # Lower score for description matches
                    combined.append((self.tools[tool_id], int(score * 0.8)))

            results = sorted(combined, key=lambda x: x[1], reverse=True)[:limit]

        else:
            # Fallback to simple substring matching
            for tool_id, tool in self.tools.items():
                score = 0
                if query in tool.name.lower():
                    score = 90
                elif query in tool.description.lower():
                    score = 70
                elif any(query in tag.lower() for tag in tool.tags):
                    score = 60

                if score >= threshold:
                    results.append((tool, score))

            results = sorted(results, key=lambda x: x[1], reverse=True)[:limit]

        return results

    def search_by_tags(self, tags: List[str], limit: int = 20) -> List[ToolInfo]:
        """Search tools by tags."""
        results = []
        tag_set = set(t.lower() for t in tags)

        for tool in self.tools.values():
            tool_tags = set(t.lower() for t in tool.tags)
            if tag_set & tool_tags:  # Intersection
                results.append(tool)

        return results[:limit]


class ContextSuggestionEngine:
    """
    Context-aware suggestion engine that recommends tools based on findings.
    """

    def __init__(self, search_engine: FuzzySearchEngine = None):
        self.search_engine = search_engine or FuzzySearchEngine()
        self.console = Console()

        # Port to tool mappings
        self._port_tool_map: Dict[int, List[Dict]] = {
            # Web ports
            80: [
                {'tool': 'nikto', 'reason': 'HTTP service detected - web vulnerability scanner', 'priority': 10},
                {'tool': 'dirb', 'reason': 'HTTP service - directory bruteforce', 'priority': 9},
                {'tool': 'gobuster', 'reason': 'HTTP service - fast directory scanner', 'priority': 9},
                {'tool': 'sqlmap', 'reason': 'HTTP service - SQL injection testing', 'priority': 8},
                {'tool': 'wfuzz', 'reason': 'HTTP service - web fuzzer', 'priority': 7},
                {'tool': 'whatweb', 'reason': 'HTTP service - technology fingerprinting', 'priority': 8},
            ],
            443: [
                {'tool': 'sslscan', 'reason': 'HTTPS service - SSL/TLS scanner', 'priority': 10},
                {'tool': 'testssl', 'reason': 'HTTPS service - SSL testing', 'priority': 9},
                {'tool': 'nikto', 'reason': 'HTTPS service - web vulnerability scanner', 'priority': 9},
                {'tool': 'dirb', 'reason': 'HTTPS service - directory bruteforce', 'priority': 8},
                {'tool': 'gobuster', 'reason': 'HTTPS service - fast directory scanner', 'priority': 8},
            ],
            8080: [
                {'tool': 'nikto', 'reason': 'Alternate HTTP port - web scanner', 'priority': 9},
                {'tool': 'dirb', 'reason': 'Alternate HTTP - directory scan', 'priority': 8},
            ],
            8443: [
                {'tool': 'sslscan', 'reason': 'Alternate HTTPS - SSL scanner', 'priority': 9},
                {'tool': 'nikto', 'reason': 'Alternate HTTPS - web scanner', 'priority': 8},
            ],
            # SSH
            22: [
                {'tool': 'ssh-audit', 'reason': 'SSH service - configuration audit', 'priority': 10},
                {'tool': 'hydra', 'reason': 'SSH service - brute force credentials', 'priority': 7},
                {'tool': 'medusa', 'reason': 'SSH service - password cracker', 'priority': 6},
            ],
            # FTP
            21: [
                {'tool': 'ftp-anon', 'reason': 'FTP service - anonymous access check', 'priority': 10},
                {'tool': 'hydra', 'reason': 'FTP service - brute force credentials', 'priority': 8},
                {'tool': 'nmap', 'reason': 'FTP service - run FTP scripts', 'priority': 7, 'args': '--script ftp-*'},
            ],
            # SMB
            445: [
                {'tool': 'smbclient', 'reason': 'SMB service - enumerate shares', 'priority': 10},
                {'tool': 'enum4linux', 'reason': 'SMB service - full enumeration', 'priority': 10},
                {'tool': 'crackmapexec', 'reason': 'SMB service - swiss army knife', 'priority': 9},
                {'tool': 'smbmap', 'reason': 'SMB service - share permissions', 'priority': 9},
            ],
            139: [
                {'tool': 'enum4linux', 'reason': 'NetBIOS - enumeration', 'priority': 10},
                {'tool': 'nbtscan', 'reason': 'NetBIOS - name scan', 'priority': 8},
            ],
            # DNS
            53: [
                {'tool': 'dig', 'reason': 'DNS service - zone transfer attempt', 'priority': 10},
                {'tool': 'dnsrecon', 'reason': 'DNS service - enumeration', 'priority': 9},
                {'tool': 'fierce', 'reason': 'DNS service - domain scanner', 'priority': 8},
            ],
            # SMTP
            25: [
                {'tool': 'smtp-user-enum', 'reason': 'SMTP service - user enumeration', 'priority': 10},
                {'tool': 'nmap', 'reason': 'SMTP service - vulnerability scripts', 'priority': 8, 'args': '--script smtp-*'},
            ],
            # MySQL
            3306: [
                {'tool': 'mysql', 'reason': 'MySQL service - connect and enumerate', 'priority': 10},
                {'tool': 'hydra', 'reason': 'MySQL service - brute force', 'priority': 7},
                {'tool': 'nmap', 'reason': 'MySQL service - run scripts', 'priority': 8, 'args': '--script mysql-*'},
            ],
            # PostgreSQL
            5432: [
                {'tool': 'psql', 'reason': 'PostgreSQL service - connect and enumerate', 'priority': 10},
                {'tool': 'hydra', 'reason': 'PostgreSQL service - brute force', 'priority': 7},
            ],
            # Redis
            6379: [
                {'tool': 'redis-cli', 'reason': 'Redis service - direct connection', 'priority': 10},
                {'tool': 'nmap', 'reason': 'Redis service - info gathering', 'priority': 8, 'args': '--script redis-*'},
            ],
            # LDAP
            389: [
                {'tool': 'ldapsearch', 'reason': 'LDAP service - enumeration', 'priority': 10},
                {'tool': 'nmap', 'reason': 'LDAP service - scripts', 'priority': 8, 'args': '--script ldap-*'},
            ],
            636: [
                {'tool': 'ldapsearch', 'reason': 'LDAPS service - secure enumeration', 'priority': 10},
            ],
            # RDP
            3389: [
                {'tool': 'xfreerdp', 'reason': 'RDP service - remote desktop', 'priority': 10},
                {'tool': 'ncrack', 'reason': 'RDP service - brute force', 'priority': 7},
                {'tool': 'crowbar', 'reason': 'RDP service - password spray', 'priority': 7},
            ],
            # WinRM
            5985: [
                {'tool': 'evil-winrm', 'reason': 'WinRM service - remote shell', 'priority': 10},
                {'tool': 'crackmapexec', 'reason': 'WinRM service - enumeration', 'priority': 9, 'args': '-u user -p pass winrm'},
            ],
            5986: [
                {'tool': 'evil-winrm', 'reason': 'WinRM HTTPS - remote shell', 'priority': 10},
            ],
            # Kerberos
            88: [
                {'tool': 'kerbrute', 'reason': 'Kerberos - user enumeration', 'priority': 10},
                {'tool': 'GetNPUsers.py', 'reason': 'Kerberos - AS-REP roasting', 'priority': 9},
                {'tool': 'GetUserSPNs.py', 'reason': 'Kerberos - Kerberoasting', 'priority': 9},
            ],
            # MongoDB
            27017: [
                {'tool': 'mongosh', 'reason': 'MongoDB service - connect', 'priority': 10},
                {'tool': 'nmap', 'reason': 'MongoDB service - scripts', 'priority': 8, 'args': '--script mongodb-*'},
            ],
            # Elasticsearch
            9200: [
                {'tool': 'curl', 'reason': 'Elasticsearch - API enumeration', 'priority': 10},
            ],
            # Docker
            2375: [
                {'tool': 'docker', 'reason': 'Docker API - remote access', 'priority': 10},
            ],
            2376: [
                {'tool': 'docker', 'reason': 'Docker TLS API - remote access', 'priority': 10},
            ],
            # VNC
            5900: [
                {'tool': 'vncviewer', 'reason': 'VNC service - connect', 'priority': 10},
                {'tool': 'hydra', 'reason': 'VNC service - brute force', 'priority': 7},
            ],
            # SNMP
            161: [
                {'tool': 'snmpwalk', 'reason': 'SNMP service - enumeration', 'priority': 10},
                {'tool': 'onesixtyone', 'reason': 'SNMP service - community scanner', 'priority': 9},
            ],
        }

        # Service to tool mappings
        self._service_tool_map: Dict[str, List[Dict]] = {
            'http': [
                {'tool': 'nikto', 'reason': 'Web service - vulnerability scanner', 'priority': 10},
                {'tool': 'dirb', 'reason': 'Web service - directory bruteforce', 'priority': 9},
                {'tool': 'sqlmap', 'reason': 'Web service - SQL injection', 'priority': 8},
            ],
            'https': [
                {'tool': 'sslscan', 'reason': 'HTTPS - SSL/TLS analysis', 'priority': 10},
                {'tool': 'nikto', 'reason': 'HTTPS - web scanner', 'priority': 9},
            ],
            'ssh': [
                {'tool': 'ssh-audit', 'reason': 'SSH - configuration audit', 'priority': 10},
            ],
            'ftp': [
                {'tool': 'ftp', 'reason': 'FTP - anonymous login check', 'priority': 10},
            ],
            'smb': [
                {'tool': 'enum4linux', 'reason': 'SMB - enumeration', 'priority': 10},
                {'tool': 'crackmapexec', 'reason': 'SMB - swiss army knife', 'priority': 9},
            ],
            'mysql': [
                {'tool': 'mysql', 'reason': 'MySQL - connect and enumerate', 'priority': 10},
            ],
            'mssql': [
                {'tool': 'mssqlclient.py', 'reason': 'MSSQL - connect via impacket', 'priority': 10},
            ],
            'rdp': [
                {'tool': 'xfreerdp', 'reason': 'RDP - remote desktop client', 'priority': 10},
            ],
            'ldap': [
                {'tool': 'ldapsearch', 'reason': 'LDAP - enumeration', 'priority': 10},
            ],
            'dns': [
                {'tool': 'dnsrecon', 'reason': 'DNS - enumeration', 'priority': 10},
            ],
            'kerberos': [
                {'tool': 'kerbrute', 'reason': 'Kerberos - user enumeration', 'priority': 10},
            ],
        }

        # Attack phase workflow
        self._workflow_suggestions: Dict[str, List[Dict]] = {
            'recon': [
                {'next_phase': 'enumeration', 'tools': ['nmap', 'masscan', 'rustscan'], 'reason': 'Initial port discovery'},
            ],
            'enumeration': [
                {'next_phase': 'vulnerability', 'tools': ['nikto', 'nuclei', 'nessus'], 'reason': 'Service-specific enumeration complete'},
            ],
            'vulnerability': [
                {'next_phase': 'exploitation', 'tools': ['metasploit', 'searchsploit'], 'reason': 'Vulnerabilities identified'},
            ],
            'exploitation': [
                {'next_phase': 'post_exploitation', 'tools': ['linpeas', 'winpeas', 'bloodhound'], 'reason': 'Initial access obtained'},
            ],
            'post_exploitation': [
                {'next_phase': 'persistence', 'tools': ['mimikatz', 'secretsdump'], 'reason': 'Privilege escalation needed'},
            ],
        }

    def suggest_from_ports(self, open_ports: List[int], limit: int = 10) -> List[Suggestion]:
        """
        Suggest tools based on discovered open ports.

        Args:
            open_ports: List of open port numbers
            limit: Maximum suggestions

        Returns:
            List of tool suggestions
        """
        suggestions = []
        seen_tools = set()

        for port in open_ports:
            if port in self._port_tool_map:
                for tool_info in self._port_tool_map[port]:
                    tool_name = tool_info['tool']
                    if tool_name not in seen_tools:
                        seen_tools.add(tool_name)
                        suggestions.append(Suggestion(
                            tool_id=tool_name,
                            tool_name=tool_name,
                            category='recommended',
                            reason=tool_info['reason'],
                            confidence=0.9,
                            priority=tool_info['priority']
                        ))

        # Sort by priority
        suggestions.sort(key=lambda x: x.priority, reverse=True)
        return suggestions[:limit]

    def suggest_from_services(self, services: List[str], limit: int = 10) -> List[Suggestion]:
        """
        Suggest tools based on discovered services.

        Args:
            services: List of service names
            limit: Maximum suggestions

        Returns:
            List of tool suggestions
        """
        suggestions = []
        seen_tools = set()

        for service in services:
            service_lower = service.lower()
            for key, tool_list in self._service_tool_map.items():
                if key in service_lower or service_lower in key:
                    for tool_info in tool_list:
                        tool_name = tool_info['tool']
                        if tool_name not in seen_tools:
                            seen_tools.add(tool_name)
                            suggestions.append(Suggestion(
                                tool_id=tool_name,
                                tool_name=tool_name,
                                category='recommended',
                                reason=tool_info['reason'],
                                confidence=0.85,
                                priority=tool_info['priority']
                            ))

        suggestions.sort(key=lambda x: x.priority, reverse=True)
        return suggestions[:limit]

    def suggest_next_phase(self, current_phase: str) -> List[Suggestion]:
        """
        Suggest tools for the next attack phase.

        Args:
            current_phase: Current phase (recon, enumeration, etc.)

        Returns:
            List of tool suggestions for next phase
        """
        suggestions = []

        if current_phase in self._workflow_suggestions:
            for workflow in self._workflow_suggestions[current_phase]:
                for tool_name in workflow['tools']:
                    suggestions.append(Suggestion(
                        tool_id=tool_name,
                        tool_name=tool_name,
                        category=workflow['next_phase'],
                        reason=workflow['reason'],
                        confidence=0.8,
                        priority=5
                    ))

        return suggestions

    def render_suggestions(self, suggestions: List[Suggestion]) -> Panel:
        """Render suggestions as a rich panel."""
        table = Table(box=None, show_header=True, header_style="bold cyan")
        table.add_column("Tool", style="green")
        table.add_column("Reason", style="white")
        table.add_column("Confidence", style="yellow")

        for sugg in suggestions[:10]:
            confidence_bar = "█" * int(sugg.confidence * 5) + "░" * (5 - int(sugg.confidence * 5))
            table.add_row(
                f"🔧 {sugg.tool_name}",
                sugg.reason,
                f"{confidence_bar} {sugg.confidence:.0%}"
            )

        return Panel(table, title="[bold cyan]💡 Recommended Tools[/bold cyan]", border_style="cyan")


@dataclass
class AttackChainStep:
    """A single step in an attack chain."""
    name: str
    tool: str
    command_template: str
    description: str
    required_params: List[str] = field(default_factory=list)
    optional_params: List[str] = field(default_factory=list)
    success_indicators: List[str] = field(default_factory=list)
    fail_conditions: List[str] = field(default_factory=list)


@dataclass
class AttackChain:
    """A complete attack chain workflow."""
    name: str
    description: str
    steps: List[AttackChainStep]
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard, expert


class AttackChainOrchestrator:
    """
    Orchestrates multi-step attack chains.
    Manages workflow automation from recon to reporting.
    """

    def __init__(self):
        self.chains: Dict[str, AttackChain] = {}
        self.console = Console()
        self._register_default_chains()

    def _register_default_chains(self) -> None:
        """Register built-in attack chains."""

        # Web Application Recon Chain
        self.register_chain(AttackChain(
            name="Web Recon",
            description="Full web application reconnaissance workflow",
            tags=['web', 'recon', 'enumeration'],
            difficulty="easy",
            steps=[
                AttackChainStep(
                    name="Port Scan",
                    tool="nmap",
                    command_template="nmap -sC -sV -p 80,443,8080,8443 {target}",
                    description="Scan common web ports",
                    required_params=['target'],
                    success_indicators=['open'],
                ),
                AttackChainStep(
                    name="Technology Detection",
                    tool="whatweb",
                    command_template="whatweb -a 3 {url}",
                    description="Identify web technologies",
                    required_params=['url'],
                    success_indicators=['Detected'],
                ),
                AttackChainStep(
                    name="Directory Bruteforce",
                    tool="gobuster",
                    command_template="gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -t 50",
                    description="Find hidden directories",
                    required_params=['url'],
                    success_indicators=['Status: 200', 'Status: 301'],
                ),
                AttackChainStep(
                    name="Vulnerability Scan",
                    tool="nikto",
                    command_template="nikto -h {url}",
                    description="Scan for web vulnerabilities",
                    required_params=['url'],
                    success_indicators=['OSVDB'],
                ),
            ]
        ))

        # Network Enumeration Chain
        self.register_chain(AttackChain(
            name="Network Enum",
            description="Complete network enumeration workflow",
            tags=['network', 'recon', 'internal'],
            difficulty="medium",
            steps=[
                AttackChainStep(
                    name="Host Discovery",
                    tool="nmap",
                    command_template="nmap -sn {network}",
                    description="Discover live hosts",
                    required_params=['network'],
                    success_indicators=['Host is up'],
                ),
                AttackChainStep(
                    name="Full Port Scan",
                    tool="nmap",
                    command_template="nmap -sS -p- --min-rate 5000 {target}",
                    description="Full TCP port scan",
                    required_params=['target'],
                    success_indicators=['open'],
                ),
                AttackChainStep(
                    name="Service Detection",
                    tool="nmap",
                    command_template="nmap -sC -sV -p {ports} {target}",
                    description="Detailed service enumeration",
                    required_params=['target', 'ports'],
                    success_indicators=['VERSION'],
                ),
                AttackChainStep(
                    name="Vulnerability Scripts",
                    tool="nmap",
                    command_template="nmap --script vuln -p {ports} {target}",
                    description="Run vulnerability scripts",
                    required_params=['target', 'ports'],
                    success_indicators=['VULNERABLE'],
                ),
            ]
        ))

        # SMB Enumeration Chain
        self.register_chain(AttackChain(
            name="SMB Enum",
            description="Complete SMB enumeration for Active Directory",
            tags=['smb', 'windows', 'ad', 'enumeration'],
            difficulty="medium",
            steps=[
                AttackChainStep(
                    name="SMB Version",
                    tool="crackmapexec",
                    command_template="crackmapexec smb {target}",
                    description="Get SMB version and OS info",
                    required_params=['target'],
                    success_indicators=['SMBv'],
                ),
                AttackChainStep(
                    name="Enum4linux",
                    tool="enum4linux",
                    command_template="enum4linux -a {target}",
                    description="Full SMB enumeration",
                    required_params=['target'],
                    success_indicators=['Domain:', 'Users:'],
                ),
                AttackChainStep(
                    name="Share Enumeration",
                    tool="smbmap",
                    command_template="smbmap -H {target}",
                    description="Enumerate SMB shares",
                    required_params=['target'],
                    success_indicators=['READ', 'WRITE'],
                ),
                AttackChainStep(
                    name="Null Session",
                    tool="rpcclient",
                    command_template="rpcclient -U '' -N {target}",
                    description="Test null session access",
                    required_params=['target'],
                    success_indicators=['rpcclient $>'],
                ),
            ]
        ))

        # SQL Injection Chain
        self.register_chain(AttackChain(
            name="SQLi Attack",
            description="SQL injection detection and exploitation",
            tags=['web', 'sqli', 'exploitation'],
            difficulty="medium",
            steps=[
                AttackChainStep(
                    name="Parameter Discovery",
                    tool="gobuster",
                    command_template="gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -x php,asp,aspx",
                    description="Find potential injectable endpoints",
                    required_params=['url'],
                    success_indicators=['Status: 200'],
                ),
                AttackChainStep(
                    name="SQLi Detection",
                    tool="sqlmap",
                    command_template="sqlmap -u '{url}' --batch --random-agent",
                    description="Test for SQL injection",
                    required_params=['url'],
                    success_indicators=['injectable', 'vulnerable'],
                ),
                AttackChainStep(
                    name="Database Enumeration",
                    tool="sqlmap",
                    command_template="sqlmap -u '{url}' --batch --dbs",
                    description="Enumerate databases",
                    required_params=['url'],
                    success_indicators=['available databases'],
                ),
                AttackChainStep(
                    name="Dump Data",
                    tool="sqlmap",
                    command_template="sqlmap -u '{url}' --batch -D {database} --dump",
                    description="Dump database contents",
                    required_params=['url', 'database'],
                    success_indicators=['Table:', 'dumped'],
                ),
            ]
        ))

        # Post-Exploitation Linux Chain
        self.register_chain(AttackChain(
            name="Linux PrivEsc",
            description="Linux privilege escalation workflow",
            tags=['linux', 'privesc', 'post-exploitation'],
            difficulty="hard",
            steps=[
                AttackChainStep(
                    name="System Info",
                    tool="uname",
                    command_template="uname -a && cat /etc/*release",
                    description="Get system information",
                    required_params=[],
                    success_indicators=['Linux'],
                ),
                AttackChainStep(
                    name="LinPEAS",
                    tool="linpeas",
                    command_template="curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh",
                    description="Run LinPEAS enumeration",
                    required_params=[],
                    success_indicators=['[+]', 'Vulnerable'],
                ),
                AttackChainStep(
                    name="SUID Check",
                    tool="find",
                    command_template="find / -perm -4000 2>/dev/null",
                    description="Find SUID binaries",
                    required_params=[],
                    success_indicators=['/usr/bin'],
                ),
                AttackChainStep(
                    name="Sudo Permissions",
                    tool="sudo",
                    command_template="sudo -l",
                    description="Check sudo permissions",
                    required_params=[],
                    success_indicators=['NOPASSWD', 'may run'],
                ),
            ]
        ))

    def register_chain(self, chain: AttackChain) -> None:
        """Register an attack chain."""
        self.chains[chain.name.lower().replace(' ', '_')] = chain

    def get_chain(self, name: str) -> Optional[AttackChain]:
        """Get attack chain by name."""
        return self.chains.get(name.lower().replace(' ', '_'))

    def list_chains(self) -> List[AttackChain]:
        """List all available attack chains."""
        return list(self.chains.values())

    def get_chains_by_tag(self, tag: str) -> List[AttackChain]:
        """Get chains matching a tag."""
        return [c for c in self.chains.values() if tag.lower() in [t.lower() for t in c.tags]]

    def render_chain_overview(self, chain: AttackChain) -> Panel:
        """Render attack chain as a visual diagram."""
        from rich.tree import Tree

        tree = Tree(f"[bold cyan]🔗 {chain.name}[/bold cyan]")

        for i, step in enumerate(chain.steps, 1):
            step_node = tree.add(f"[green]Step {i}:[/green] {step.name}")
            step_node.add(f"[dim]Tool:[/dim] {step.tool}")
            step_node.add(f"[dim]Command:[/dim] [yellow]{step.command_template}[/yellow]")

        return Panel(
            tree,
            title=f"[bold white]{chain.description}[/bold white]",
            subtitle=f"[dim]Difficulty: {chain.difficulty} | Tags: {', '.join(chain.tags)}[/dim]",
            border_style="cyan"
        )

