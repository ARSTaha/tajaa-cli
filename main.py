#!/usr/bin/env python3
"""
████████╗  ███████╗      ██╗  ███████╗  ███████╗
╚══██╔══╝  ██╔═══██║     ██║  ██╔═══██║ ██╔═══██║
   ██║     ████████║     ██║  ████████║ ████████║
   ██║     ██╔═══██║ ██  ██║  ██╔═══██║ ██╔═══██║
   ██║     ██║   ██║ ╚████╔╝  ██║   ██║ ██║   ██║
   ╚═╝     ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═╝   ╚═╝

Tajaa CLI - The Ultimate Cyber Security Framework
Author: Tajaa
Version: 5.0.0
License: MIT

The most advanced, aesthetically stunning, and powerful CLI framework.
480+ tools. AI-powered suggestions. Attack chain automation.
"""

import asyncio
import sys
import shutil
import shlex
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

import typer
import yaml
import pyperclip
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# Core imports
from core.database import DatabaseManager, FindingType, ScanStatus
from core.engine import AsyncEngine, OutputParser
from core.intelligence import (
    FuzzySearchEngine,
    ContextSuggestionEngine,
    AttackChainOrchestrator,
    ToolInfo,
    Suggestion
)
from core.plugin import PluginLoader, PluginRegistry, YAMLPlugin
from core.session import SessionManager, WorkspaceManager
from core.ui import TajaaUI, CinematicIntro, CyberpunkTheme


# =============================================================================
# CONSTANTS
# =============================================================================

VERSION = "5.0.0"
AUTHOR = "Tajaa"

# Tool count placeholder - will be updated dynamically
TOOL_COUNT = 480


# =============================================================================
# INPUT VALIDATION (Enhanced)
# =============================================================================

class InputValidator:
    """Enhanced input validation with security checks."""

    def __init__(self, console: Console):
        self.console = console
        self.dangerous_patterns = [
            r'[;&|`$<>]',
            r'\$\(',
            r'`',
            r'\.\./',
            r'\n',
            r'\r',
        ]

    def validate_target(self, value: str) -> tuple[bool, str]:
        """Validate target (IP/hostname/URL)."""
        import ipaddress

        value = value.strip()

        # Check for dangerous characters
        for pattern in self.dangerous_patterns:
            if re.search(pattern, value):
                return False, "Dangerous characters detected"

        # Try IP address
        try:
            ipaddress.ip_address(value)
            return True, ""
        except ValueError:
            pass

        # Try hostname
        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?)*$'
        if re.match(hostname_pattern, value):
            return True, ""

        # Try URL
        url_pattern = r'^https?://[^\s]+$'
        if re.match(url_pattern, value):
            return True, ""

        return False, f"Invalid target: {value}"

    def validate_port(self, value: str) -> tuple[bool, str, int]:
        """Validate port number."""
        try:
            port = int(value)
            if 1 <= port <= 65535:
                return True, "", port
            return False, "Port out of range (1-65535)", 0
        except ValueError:
            return False, f"Invalid port: {value}", 0

    def validate_path(self, value: str) -> tuple[bool, str]:
        """Validate file path."""
        if '..' in value:
            return False, "Path traversal not allowed"
        return True, ""

    def get_validated_input(self, param_name: str, default: str = None) -> str:
        """Get and validate user input."""
        prompt_text = param_name.replace('_', ' ').title()
        display = f"  [cyan]›[/cyan] {prompt_text}"
        if default:
            display += f" [dim]({default})[/dim]"

        while True:
            try:
                value = Prompt.ask(display, default=default or "")

                if not value.strip() and default:
                    value = default

                if not value.strip():
                    self.console.print("    [red]✗[/red] Cannot be empty")
                    continue

                # Validate based on param type
                param_lower = param_name.lower()

                if any(x in param_lower for x in ['ip', 'target', 'host', 'rhost', 'lhost', 'url']):
                    is_valid, err = self.validate_target(value)
                    if not is_valid:
                        self.console.print(f"    [red]✗[/red] {err}")
                        continue

                elif 'port' in param_lower:
                    is_valid, err, _ = self.validate_port(value)
                    if not is_valid:
                        self.console.print(f"    [red]✗[/red] {err}")
                        continue

                elif any(x in param_lower for x in ['file', 'path', 'wordlist']):
                    is_valid, err = self.validate_path(value)
                    if not is_valid:
                        self.console.print(f"    [red]✗[/red] {err}")
                        continue

                return value.strip()

            except KeyboardInterrupt:
                raise


# =============================================================================
# COMMAND MANAGER (The Brain)
# =============================================================================

class CommandManager:
    """
    Intelligent command manager - The brain of Tajaa.
    Handles 480+ tools with AI-like recommendations and workflow automation.
    """

    def __init__(
        self,
        console: Console,
        db: DatabaseManager,
        engine: AsyncEngine,
        plugin_registry: PluginRegistry,
        session: SessionManager,
        ui: TajaaUI
    ):
        self.console = console
        self.db = db
        self.engine = engine
        self.plugins = plugin_registry
        self.session = session
        self.ui = ui
        self.validator = InputValidator(console)

        # Intelligence modules
        self.fuzzy_search = FuzzySearchEngine()
        self.suggestion_engine = ContextSuggestionEngine(self.fuzzy_search)
        self.attack_chains = AttackChainOrchestrator()

        # Register all tools for search
        self._index_tools()

    def _index_tools(self) -> None:
        """Index all tools for fuzzy search."""
        for plugin in self.plugins.list_all():
            tool_info = ToolInfo(
                id=plugin.metadata.name.lower().replace(' ', '_'),
                name=plugin.metadata.name,
                description=plugin.metadata.description,
                category=plugin.metadata.category.value,
                tags=plugin.metadata.tags,
            )
            self.fuzzy_search.register_tool(tool_info)

    async def search_tools(self, query: str) -> List[tuple]:
        """Search for tools using fuzzy matching."""
        return self.fuzzy_search.search(query, limit=15)

    async def get_suggestions(self, target: str = None) -> List[Suggestion]:
        """Get AI-powered tool suggestions based on context."""
        suggestions = []

        # Get suggestions from session cache
        if self.session.current:
            ports = self.session.get_cached_ports(target)
            if ports:
                suggestions.extend(self.suggestion_engine.suggest_from_ports(ports))

            services = self.session.get_cached_services(target)
            if services:
                service_names = [s.get('service', '') for s in services]
                suggestions.extend(self.suggestion_engine.suggest_from_services(service_names))

        # Get from database
        if target and self.db:
            try:
                db_target = await self.db.get_target_by_value(target)
                if db_target:
                    db_ports = await self.db.get_open_ports(db_target.id)
                    if db_ports:
                        suggestions.extend(self.suggestion_engine.suggest_from_ports(db_ports))
            except Exception:
                pass

        # Deduplicate
        seen = set()
        unique = []
        for s in suggestions:
            if s.tool_id not in seen:
                seen.add(s.tool_id)
                unique.append(s)

        return sorted(unique, key=lambda x: x.priority, reverse=True)[:10]

    async def execute_tool(self, plugin: YAMLPlugin, category_name: str) -> Optional[Dict]:
        """Execute a tool and process results."""
        # Check if tool exists
        tool_binary = plugin.command_template.split()[0]
        if not shutil.which(tool_binary):
            self.console.print(f"\n  [yellow]⚠[/yellow] Tool not found: [white]{tool_binary}[/white]")
            if not Confirm.ask("  Continue anyway?", default=False):
                return None

        # Show tool header
        self.ui.show_command(
            plugin.metadata.name,
            plugin.command_template,
            plugin.metadata.description
        )

        # Get parameters
        params = {}
        if plugin.required_params:
            self.console.print("  [dim]Parameters:[/dim]\n")

        for param in plugin.required_params:
            default = plugin.optional_params.get(param, '')
            value = self.validator.get_validated_input(param, default=default)
            params[param] = shlex.quote(value)
            plugin.set_param(param, value)

        # Build command
        try:
            command = plugin.build_command()
        except Exception as e:
            self.console.print(f"\n  [red]✗[/red] Error building command: {e}")
            return None

        # Display final command
        self.console.print()
        self.console.print("  [bold]Final Command:[/bold]")
        self.console.print()
        self._display_command(command)
        self.console.print()

        # Copy to clipboard
        try:
            pyperclip.copy(command)
            self.console.print("  [dim]✓ Copied to clipboard[/dim]")
        except Exception:
            pass

        # Log to session
        if self.session.current:
            self.session.add_command(command)
            self.session.add_tool_usage(plugin.metadata.name)

        # Execute
        self.console.print()
        if not Confirm.ask("  [cyan]Execute now?[/cyan]", default=True):
            return None

        self.console.print()
        self.console.print("  [dim]Running...[/dim]\n")
        self.console.print("  [dim]─" * 35 + "[/dim]\n")

        # Execute with async engine
        result = await self.engine.execute(command, stream_output=True)

        self.console.print("\n  [dim]─" * 35 + "[/dim]")

        if result['success']:
            self.console.print("\n  [bold #00FF00]✓ Completed successfully[/bold #00FF00]")
        else:
            self.console.print(f"\n  [yellow]⚠ Exit code: {result['exit_code']}[/yellow]")

        # Parse output and cache findings
        await self._process_output(plugin, result, params)

        return result

    async def _process_output(self, plugin: YAMLPlugin, result: Dict, params: Dict) -> None:
        """Process tool output and extract findings."""
        output = result.get('output', '')
        if not output:
            return

        # Get target from params
        target = None
        for key in ['target', 'ip', 'host', 'url', 'rhost']:
            if key in params:
                target = params[key].strip("'\"")
                break

        if not target:
            return

        # Parse output based on tool type
        findings = plugin.parse_output(output)

        # Cache ports
        ports = findings.get('ports', [])
        if ports and self.session.current:
            self.session.cache_ports(target, ports)

        # Cache services
        services = findings.get('services', [])
        if services and self.session.current:
            self.session.cache_services(target, services)

        # Store in database
        if self.db and target:
            try:
                target_id = await self.db.add_target(target)

                # Create scan record
                scan_id = await self.db.create_scan(
                    target_id,
                    plugin.metadata.name,
                    plugin.build_command()
                )

                # Store findings
                for port in ports:
                    await self.db.add_finding(
                        scan_id, target_id,
                        FindingType.PORT,
                        str(port),
                        port=port
                    )

                for svc in services:
                    await self.db.add_finding(
                        scan_id, target_id,
                        FindingType.SERVICE,
                        svc.get('service', ''),
                        port=svc.get('port'),
                        service=svc.get('service', ''),
                        version=svc.get('version', '')
                    )

                await self.db.update_scan(scan_id, ScanStatus.COMPLETED, output)

            except Exception:
                pass

        # Show suggestions
        suggestions = await self.get_suggestions(target)
        if suggestions:
            self.console.print()
            self.ui.show_suggestions([{
                'tool_name': s.tool_name,
                'reason': s.reason
            } for s in suggestions[:5]])

    def _display_command(self, command: str) -> None:
        """Display command with formatting."""
        if len(command) <= 70:
            self.console.print(f"    [#00FF00]{command}[/#00FF00]")
        else:
            parts = []
            current = ""
            for word in command.split():
                if len(current) + len(word) > 65 and current:
                    parts.append(current)
                    current = "    " + word
                else:
                    current = current + " " + word if current else word
            if current:
                parts.append(current)

            for i, part in enumerate(parts):
                suffix = " \\" if i < len(parts) - 1 else ""
                self.console.print(f"    [#00FF00]{part}{suffix}[/#00FF00]")

    async def execute_attack_chain(self, chain_name: str, target: str) -> None:
        """Execute a predefined attack chain."""
        chain = self.attack_chains.get_chain(chain_name)
        if not chain:
            self.console.print(f"  [red]✗[/red] Chain not found: {chain_name}")
            return

        self.console.print()
        self.console.print(self.attack_chains.render_chain_overview(chain))
        self.console.print()

        if not Confirm.ask("  [cyan]Execute this chain?[/cyan]", default=True):
            return

        # Execute each step
        for i, step in enumerate(chain.steps, 1):
            self.console.print()
            self.console.print(f"  [bold #00FFFF]━━━ Step {i}/{len(chain.steps)}: {step.name} ━━━[/bold #00FFFF]")

            # Build command with target
            command = step.command_template.replace('{target}', shlex.quote(target))
            command = command.replace('{url}', shlex.quote(target))

            self.console.print(f"  [dim]Tool: {step.tool}[/dim]")
            self.console.print(f"  [dim]Command: {command}[/dim]")
            self.console.print()

            result = await self.engine.execute(command, stream_output=True)

            if result['success']:
                self.console.print(f"\n  [#00FF00]✓ Step {i} completed[/#00FF00]")
            else:
                self.console.print(f"\n  [yellow]⚠ Step {i} failed[/yellow]")
                if not Confirm.ask("  Continue chain?", default=False):
                    break

        self.console.print()
        self.console.print("  [bold #00FF00]━━━ Chain Complete ━━━[/bold #00FF00]")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class TajaaCLI:
    """
    Tajaa CLI - The Ultimate Cyber Security Framework
    Main application orchestrator.
    """

    def __init__(
        self,
        config_dir: Path = Path("configs"),
        db_path: Path = Path("data/tajaa.db"),
        skip_intro: bool = False
    ):
        self.console = Console()
        self.config_dir = config_dir
        self.db_path = db_path
        self.skip_intro = skip_intro

        # Core components (initialized in setup)
        self.db: Optional[DatabaseManager] = None
        self.engine: Optional[AsyncEngine] = None
        self.plugins: Optional[PluginRegistry] = None
        self.session: Optional[SessionManager] = None
        self.ui: Optional[TajaaUI] = None
        self.command_manager: Optional[CommandManager] = None

        # State
        self._categories: Dict[str, Dict] = {}
        self._running = False

    async def setup(self) -> bool:
        """Initialize all components."""
        try:
            # Initialize UI
            self.ui = TajaaUI(self.console)

            # Show intro
            await self.ui.show_intro(skip=self.skip_intro)

            # Initialize database
            self.db = DatabaseManager(self.db_path)
            await self.db.connect()

            # Initialize async engine
            self.engine = AsyncEngine(self.console)

            # Initialize session manager
            self.session = SessionManager(db_manager=self.db)
            await self.session.create_session()

            # Load plugins
            loader = PluginLoader(configs_path=self.config_dir)
            self.plugins = loader.load_all(lazy=True)

            # Initialize command manager
            self.command_manager = CommandManager(
                self.console,
                self.db,
                self.engine,
                self.plugins,
                self.session,
                self.ui
            )

            # Load categories from YAML
            self._load_categories()

            return True

        except Exception as e:
            self.console.print(f"\n  [red]✗ Initialization failed: {e}[/red]\n")
            return False

    def _load_categories(self) -> None:
        """Load categories from YAML configs."""
        self._categories = {}

        for yaml_file in sorted(self.config_dir.glob("*.yaml")):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if data and 'categories' in data:
                    self._categories.update(data['categories'])

            except Exception:
                continue

    async def run(self) -> None:
        """Main application loop."""
        self._running = True

        try:
            self.console.clear()
            self.ui.show_banner()

            while self._running:
                try:
                    # Show categories
                    self.ui.show_categories(self._categories)

                    # Show suggestions if target is set
                    if self.session.current and self.session.current.active_target:
                        suggestions = await self.command_manager.get_suggestions(
                            self.session.current.active_target
                        )
                        if suggestions:
                            self.ui.show_suggestions([{
                                'tool_name': s.tool_name,
                                'reason': s.reason
                            } for s in suggestions[:3]])

                    # Category selection
                    cat_id = await self._select_category()
                    if cat_id is None:
                        break

                    if cat_id == "__search__":
                        await self._handle_search()
                        continue

                    if cat_id == "__chains__":
                        await self._handle_attack_chains()
                        continue

                    if cat_id == "__target__":
                        await self._set_target()
                        continue

                    # Tool selection
                    category = self._categories[cat_id]
                    tool_id = await self._select_tool(category)

                    if tool_id is None:
                        self.console.clear()
                        self.ui.show_banner()
                        continue

                    # Execute tool
                    plugin = self.plugins.get(f"{cat_id}.{tool_id}")
                    if plugin:
                        await self.command_manager.execute_tool(plugin, category.get('name', cat_id))

                    # Continue prompt
                    self.console.print()
                    if not Confirm.ask("  [cyan]Continue?[/cyan]", default=True):
                        break

                    self.console.clear()
                    self.ui.show_banner()

                except KeyboardInterrupt:
                    self.console.print()
                    self.console.clear()
                    self.ui.show_banner()
                    continue

        except KeyboardInterrupt:
            pass
        finally:
            await self._cleanup()

    async def _select_category(self) -> Optional[str]:
        """Select a category."""
        try:
            choices = []

            # Add special options at top
            choices.append(Choice(value="__search__", name="🔍  Search Tools"))
            choices.append(Choice(value="__chains__", name="🔗  Attack Chains"))
            choices.append(Choice(value="__target__", name="🎯  Set Target"))
            choices.append(Choice(value="", name="─" * 40))

            # Add categories
            for cat_id, cat_data in self._categories.items():
                name = cat_data.get('name', cat_id)
                count = len(cat_data.get('tools', {}))
                emoji = self.ui._get_category_emoji(cat_id)
                choices.append(Choice(value=cat_id, name=f"{emoji}  {name} ({count})"))

            choices.append(Choice(value="", name="─" * 40))
            choices.append(Choice(value="__exit__", name="🚪  Exit"))

            self.console.print()
            result = inquirer.select(
                message="Select option:",
                choices=[c for c in choices if c.value != ""],
                pointer="❯",
                qmark="",
                amark="",
                instruction="",
            ).execute()

            return None if result == "__exit__" else result

        except KeyboardInterrupt:
            return None

    async def _select_tool(self, category: Dict) -> Optional[str]:
        """Select a tool from category."""
        try:
            tools = category.get('tools', {})
            name = category.get('name', 'Tools')

            self.console.print()
            self.console.print(f"[bold #FF00FF]  ╔═══ {name.upper()} ═══[/bold #FF00FF]")
            self.console.print()

            choices = []
            for tool_id, tool_data in tools.items():
                tool_name = tool_data.get('name', tool_id)
                choices.append(Choice(value=tool_id, name=f"🔧  {tool_name}"))

            choices.append(Choice(value="__back__", name="← Back"))

            result = inquirer.select(
                message="Select tool:",
                choices=choices,
                pointer="❯",
                qmark="",
                amark="",
            ).execute()

            return None if result == "__back__" else result

        except KeyboardInterrupt:
            return None

    async def _handle_search(self) -> None:
        """Handle fuzzy search."""
        self.console.print()
        query = Prompt.ask("  [cyan]🔍 Search[/cyan]")

        if not query.strip():
            return

        results = await self.command_manager.search_tools(query)
        self.ui.show_search_results(results, query)

        if results:
            self.console.print()
            if Confirm.ask("  Select a tool from results?", default=True):
                choices = [
                    Choice(value=tool.id, name=f"🔧  {tool.name}")
                    for tool, _ in results[:10]
                ]
                choices.append(Choice(value="__back__", name="← Back"))

                result = inquirer.select(
                    message="Select tool:",
                    choices=choices,
                    pointer="❯",
                    qmark="",
                    amark="",
                ).execute()

                if result != "__back__":
                    # Find and execute the plugin
                    for cat_id, cat_data in self._categories.items():
                        for tool_id, tool_data in cat_data.get('tools', {}).items():
                            if tool_data.get('name', '').lower().replace(' ', '_') == result:
                                plugin = self.plugins.get(f"{cat_id}.{tool_id}")
                                if plugin:
                                    await self.command_manager.execute_tool(plugin, cat_data.get('name', ''))
                                return

    async def _handle_attack_chains(self) -> None:
        """Handle attack chain selection and execution."""
        chains = self.command_manager.attack_chains.list_chains()

        if not chains:
            self.console.print("  [dim]No attack chains available[/dim]")
            return

        choices = [
            Choice(value=c.name.lower().replace(' ', '_'), name=f"🔗  {c.name} - {c.description}")
            for c in chains
        ]
        choices.append(Choice(value="__back__", name="← Back"))

        self.console.print()
        result = inquirer.select(
            message="Select attack chain:",
            choices=choices,
            pointer="❯",
            qmark="",
            amark="",
        ).execute()

        if result == "__back__":
            return

        # Get target
        target = self.session.current.active_target if self.session.current else ""
        if not target:
            target = Prompt.ask("  [cyan]Target[/cyan]")

        if target:
            await self.command_manager.execute_attack_chain(result, target)

    async def _set_target(self) -> None:
        """Set the active target."""
        self.console.print()
        target = Prompt.ask("  [cyan]🎯 Enter target (IP/hostname/URL)[/cyan]")

        if target.strip():
            is_valid, err = self.command_manager.validator.validate_target(target)
            if is_valid:
                self.session.set_active_target(target)
                self.console.print(f"  [#00FF00]✓ Target set: {target}[/#00FF00]")

                # Store in database
                if self.db:
                    target_id = await self.db.add_target(target)
                    if self.session.current:
                        self.session.current.active_target_id = target_id
            else:
                self.console.print(f"  [red]✗ {err}[/red]")

    async def _cleanup(self) -> None:
        """Cleanup resources."""
        if self.session:
            await self.session.close_session()

        if self.db:
            await self.db.close()

        self.console.print()
        self.console.print("  [dim]Thanks for using Tajaa CLI - Stay Elite 💀[/dim]")
        self.console.print()


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

app = typer.Typer(
    name="tajaa",
    help="Tajaa CLI - The Ultimate Cyber Security Framework",
    add_completion=False
)


@app.command()
def main(
    config: Path = typer.Option(
        Path("configs"),
        "--config", "-c",
        help="Config directory path"
    ),
    db: Path = typer.Option(
        Path("data/tajaa.db"),
        "--db", "-d",
        help="Database file path"
    ),
    skip_intro: bool = typer.Option(
        False,
        "--skip-intro", "-s",
        help="Skip cinematic intro"
    ),
    version: bool = typer.Option(
        False,
        "--version", "-v",
        help="Show version"
    )
) -> None:
    """Launch Tajaa CLI - The Ultimate Cyber Security Framework."""
    if version:
        console = Console()
        console.print(f"\n  [bold #00FFFF]Tajaa CLI[/bold #00FFFF] v{VERSION}")
        console.print(f"  [dim]Author: {AUTHOR}[/dim]")
        console.print(f"  [dim]Tools: {TOOL_COUNT}+[/dim]\n")
        return

    # Run the async application
    tajaa = TajaaCLI(config_dir=config, db_path=db, skip_intro=skip_intro)

    async def run_app():
        if await tajaa.setup():
            await tajaa.run()

    asyncio.run(run_app())


if __name__ == "__main__":
    app()

