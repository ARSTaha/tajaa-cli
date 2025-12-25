"""
Tajaa Plugin System
Dynamic plugin architecture for modular tool management.
Author: Tajaa
"""

import importlib
import importlib.util
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Type, Callable
from dataclasses import dataclass, field
from enum import Enum

import yaml
from rich.console import Console


class PluginCategory(Enum):
    """Plugin categories."""
    RECON = "recon"
    WEB = "web"
    WIRELESS = "wireless"
    SNIFFING = "sniffing"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    OSINT = "osint"
    MOBILE = "mobile"
    CLOUD = "cloud"
    MISC = "misc"


@dataclass
class PluginMetadata:
    """Plugin metadata."""
    name: str
    description: str
    author: str = "Tajaa"
    version: str = "1.0.0"
    category: PluginCategory = PluginCategory.MISC
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    platform: str = "all"  # all, linux, windows, macos


class PluginBase(ABC):
    """
    Base class for all Tajaa plugins.
    Extend this class to create new tool plugins.
    """

    metadata: PluginMetadata = PluginMetadata(
        name="Base Plugin",
        description="Base plugin class"
    )

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self._params: Dict[str, Any] = {}

    @property
    @abstractmethod
    def command_template(self) -> str:
        """Return the command template with {param} placeholders."""
        pass

    @property
    def required_params(self) -> List[str]:
        """Return list of required parameters."""
        return []

    @property
    def optional_params(self) -> Dict[str, str]:
        """Return dict of optional params with defaults."""
        return {}

    @property
    def param_descriptions(self) -> Dict[str, str]:
        """Return descriptions for each parameter."""
        return {}

    def set_param(self, name: str, value: Any) -> None:
        """Set a parameter value."""
        self._params[name] = value

    def get_param(self, name: str, default: Any = None) -> Any:
        """Get a parameter value."""
        return self._params.get(name, default)

    def build_command(self) -> str:
        """Build the final command with all parameters."""
        cmd = self.command_template

        # Apply required params
        for param in self.required_params:
            value = self._params.get(param, '')
            cmd = cmd.replace(f'{{{param}}}', str(value))

        # Apply optional params with defaults
        for param, default in self.optional_params.items():
            value = self._params.get(param, default)
            cmd = cmd.replace(f'{{{param}}}', str(value))

        return cmd

    def validate_params(self) -> tuple[bool, str]:
        """Validate all required parameters are set."""
        missing = []
        for param in self.required_params:
            if param not in self._params or not self._params[param]:
                missing.append(param)

        if missing:
            return False, f"Missing required parameters: {', '.join(missing)}"
        return True, ""

    def pre_execute(self) -> bool:
        """Called before command execution. Return False to cancel."""
        return True

    def post_execute(self, output: str, exit_code: int) -> None:
        """Called after command execution with results."""
        pass

    def parse_output(self, output: str) -> Dict[str, Any]:
        """
        Parse command output into structured data.
        Override this to extract findings from tool output.
        """
        return {'raw_output': output}

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """
        Return suggested next tools based on findings.
        Override this to provide context-aware suggestions.
        """
        return []


class YAMLPlugin(PluginBase):
    """
    Plugin created from YAML configuration.
    Allows tools to be defined in YAML without writing Python code.
    """

    def __init__(self, config: Dict[str, Any], console: Console = None):
        super().__init__(console)
        self._config = config
        self.metadata = PluginMetadata(
            name=config.get('name', 'Unknown'),
            description=config.get('description', ''),
            category=PluginCategory(config.get('category', 'misc')),
            tags=config.get('tags', []),
            dependencies=config.get('dependencies', []),
        )
        self._command_template = config.get('command', '')
        self._required_params = config.get('params', [])
        self._optional_params = config.get('defaults', {})
        self._param_descriptions = config.get('param_descriptions', {})

    @property
    def command_template(self) -> str:
        return self._command_template

    @property
    def required_params(self) -> List[str]:
        return self._required_params

    @property
    def optional_params(self) -> Dict[str, str]:
        return self._optional_params

    @property
    def param_descriptions(self) -> Dict[str, str]:
        return self._param_descriptions


class PluginRegistry:
    """
    Central registry for all plugins.
    Handles plugin registration, lookup, and categorization.
    """

    def __init__(self):
        self._plugins: Dict[str, PluginBase] = {}
        self._by_category: Dict[PluginCategory, List[str]] = {cat: [] for cat in PluginCategory}
        self._by_tag: Dict[str, List[str]] = {}
        self._console = Console()

    def register(self, plugin_id: str, plugin: PluginBase) -> None:
        """Register a plugin."""
        self._plugins[plugin_id] = plugin

        # Index by category
        category = plugin.metadata.category
        if plugin_id not in self._by_category[category]:
            self._by_category[category].append(plugin_id)

        # Index by tags
        for tag in plugin.metadata.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = []
            if plugin_id not in self._by_tag[tag]:
                self._by_tag[tag].append(plugin_id)

    def get(self, plugin_id: str) -> Optional[PluginBase]:
        """Get plugin by ID."""
        return self._plugins.get(plugin_id)

    def get_by_category(self, category: PluginCategory) -> List[PluginBase]:
        """Get all plugins in a category."""
        return [self._plugins[pid] for pid in self._by_category.get(category, [])]

    def get_by_tag(self, tag: str) -> List[PluginBase]:
        """Get all plugins with a tag."""
        return [self._plugins[pid] for pid in self._by_tag.get(tag, [])]

    def list_all(self) -> List[PluginBase]:
        """List all registered plugins."""
        return list(self._plugins.values())

    def list_categories(self) -> Dict[str, int]:
        """List categories with plugin counts."""
        return {cat.value: len(plugins) for cat, plugins in self._by_category.items() if plugins}

    def search(self, query: str) -> List[PluginBase]:
        """Simple search by name or description."""
        query = query.lower()
        results = []
        for plugin in self._plugins.values():
            if (query in plugin.metadata.name.lower() or
                query in plugin.metadata.description.lower() or
                any(query in tag.lower() for tag in plugin.metadata.tags)):
                results.append(plugin)
        return results

    @property
    def count(self) -> int:
        """Total number of registered plugins."""
        return len(self._plugins)


class PluginLoader:
    """
    Loads plugins from various sources:
    - Python modules in /modules directory
    - YAML configuration files in /configs directory
    """

    def __init__(self, modules_path: Path = None, configs_path: Path = None):
        self.modules_path = modules_path or Path("modules")
        self.configs_path = configs_path or Path("configs")
        self.registry = PluginRegistry()
        self._console = Console()
        self._loaded = False

    def load_all(self, lazy: bool = True) -> PluginRegistry:
        """
        Load all plugins.

        Args:
            lazy: If True, only register plugins without fully loading

        Returns:
            PluginRegistry with all loaded plugins
        """
        if self._loaded:
            return self.registry

        # Load YAML-based plugins
        self._load_yaml_plugins()

        # Load Python module plugins
        if not lazy:
            self._load_module_plugins()

        self._loaded = True
        return self.registry

    def _load_yaml_plugins(self) -> None:
        """Load plugins from YAML config files."""
        if not self.configs_path.exists():
            return

        for yaml_file in sorted(self.configs_path.glob("*.yaml")):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if not data:
                    continue

                categories = data.get('categories', {})
                for cat_id, cat_data in categories.items():
                    tools = cat_data.get('tools', {})
                    if not tools:
                        continue

                    for tool_id, tool_data in tools.items():
                        if not tool_data:
                            continue

                        # Determine category from parent or default
                        tool_data['category'] = self._map_category(cat_id)

                        plugin = YAMLPlugin(tool_data)
                        plugin_id = f"{cat_id}.{tool_id}"
                        self.registry.register(plugin_id, plugin)

            except Exception as e:
                self._console.print(f"[yellow]Warning:[/yellow] Failed to load {yaml_file}: {e}")

    def _load_module_plugins(self) -> None:
        """Load plugins from Python modules."""
        if not self.modules_path.exists():
            return

        for category_dir in self.modules_path.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('_'):
                continue

            for py_file in category_dir.glob("*.py"):
                if py_file.name.startswith('_'):
                    continue

                try:
                    self._load_module_file(py_file, category_dir.name)
                except Exception as e:
                    self._console.print(f"[yellow]Warning:[/yellow] Failed to load {py_file}: {e}")

    def _load_module_file(self, file_path: Path, category: str) -> None:
        """Load plugins from a Python file."""
        module_name = f"modules.{category}.{file_path.stem}"

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            return

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Find plugin classes
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and
                issubclass(attr, PluginBase) and
                attr is not PluginBase and
                attr is not YAMLPlugin):
                plugin = attr()
                plugin_id = f"{category}.{attr_name.lower()}"
                self.registry.register(plugin_id, plugin)

    def _map_category(self, category_id: str) -> str:
        """Map category ID to PluginCategory value."""
        mappings = {
            'reconnaissance': 'recon',
            'web_apps': 'web',
            'web_bounty': 'web',
            'network_ad': 'recon',
            'wireless_radio': 'wireless',
            'post_exploit': 'post_exploitation',
            'osint_detective': 'osint',
            'mobile_iot': 'mobile',
            'cloud_auditor': 'cloud',
            'ctf_kit': 'misc',
            'commands': 'misc',
        }
        return mappings.get(category_id, 'misc')

    def reload(self) -> PluginRegistry:
        """Force reload all plugins."""
        self._loaded = False
        self.registry = PluginRegistry()
        return self.load_all(lazy=False)


# =============================================================================
# Example Plugin Implementations
# =============================================================================

class NmapPlugin(PluginBase):
    """Nmap port scanner plugin."""

    metadata = PluginMetadata(
        name="Nmap",
        description="Network mapper and port scanner",
        category=PluginCategory.RECON,
        tags=['network', 'ports', 'scanner', 'enumeration'],
        dependencies=['nmap']
    )

    @property
    def command_template(self) -> str:
        return "nmap {options} -p {ports} {target}"

    @property
    def required_params(self) -> List[str]:
        return ['target']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'ports': '-',
            'options': '-sC -sV'
        }

    @property
    def param_descriptions(self) -> Dict[str, str]:
        return {
            'target': 'Target IP or hostname',
            'ports': 'Ports to scan (default: all)',
            'options': 'Nmap options (default: -sC -sV)'
        }

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Nmap output into structured data."""
        import re

        results = {
            'hosts': [],
            'ports': [],
            'services': [],
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

        return results

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """Suggest tools based on discovered services."""
        suggestions = []
        ports = findings.get('ports', [])

        if 80 in ports or 443 in ports or 8080 in ports:
            suggestions.extend(['nikto', 'gobuster', 'dirb'])
        if 22 in ports:
            suggestions.append('ssh-audit')
        if 21 in ports:
            suggestions.append('ftp-anon')
        if 445 in ports:
            suggestions.extend(['enum4linux', 'smbclient'])
        if 3306 in ports:
            suggestions.append('mysql')

        return suggestions


class GobusterPlugin(PluginBase):
    """Gobuster directory scanner plugin."""

    metadata = PluginMetadata(
        name="Gobuster",
        description="Directory/file & DNS busting tool",
        category=PluginCategory.WEB,
        tags=['web', 'directory', 'bruteforce', 'enumeration'],
        dependencies=['gobuster']
    )

    @property
    def command_template(self) -> str:
        return "gobuster dir -u {url} -w {wordlist} -t {threads} {options}"

    @property
    def required_params(self) -> List[str]:
        return ['url']

    @property
    def optional_params(self) -> Dict[str, str]:
        return {
            'wordlist': '/usr/share/wordlists/dirb/common.txt',
            'threads': '50',
            'options': ''
        }

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse Gobuster output."""
        import re

        results = {
            'directories': [],
            'files': []
        }

        pattern = r'/(\S+)\s+\(Status: (\d+)\)'
        for match in re.finditer(pattern, output):
            entry = {
                'path': '/' + match.group(1),
                'status': int(match.group(2))
            }
            if '.' in entry['path'].split('/')[-1]:
                results['files'].append(entry)
            else:
                results['directories'].append(entry)

        return results

    def get_suggestions(self, findings: Dict[str, Any]) -> List[str]:
        """Suggest tools based on discovered paths."""
        suggestions = []
        dirs = findings.get('directories', [])
        files = findings.get('files', [])

        # Check for interesting paths
        for d in dirs:
            path = d.get('path', '').lower()
            if 'admin' in path or 'login' in path:
                suggestions.append('hydra')
            if 'api' in path:
                suggestions.append('ffuf')

        for f in files:
            path = f.get('path', '').lower()
            if path.endswith('.php'):
                suggestions.append('sqlmap')
            if path.endswith('.git'):
                suggestions.append('git-dumper')

        return list(set(suggestions))

