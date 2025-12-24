#!/usr/bin/env python3
"""
Tajaa CLI - Modular Cyber Security Framework

A modular framework for penetration testing and security assessments.
Supports CTF, Web Security, Active Directory, Mobile/IoT, Cloud, OSINT,
Wireless, and Post-Exploitation.

Author: Tajaa
Version: 3.1.0
License: MIT
"""

import subprocess
import shutil
import ipaddress
import shlex
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import typer
import yaml
import pyperclip
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


# Configuration Classes

@dataclass
class ToolConfig:
    """Configuration for a single security tool."""
    name: str
    description: str
    command: str
    params: List[str]
    defaults: Optional[Dict[str, str]] = None


@dataclass
class CategoryConfig:
    """Configuration for a category of tools."""
    name: str
    tools: Dict[str, ToolConfig]


class ConfigLoader:
    """Loads and parses YAML configuration files."""

    def __init__(self, config_path: Path) -> None:
        self.config_path: Path = config_path
        self.console: Console = Console()
        self.categories: Dict[str, CategoryConfig] = {}

    def load(self) -> Dict[str, CategoryConfig]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            self.console.print(f"[bold red]Error:[/bold red] Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            categories_data = data.get('categories', {})

            for category_id, category_data in categories_data.items():
                tools = {}

                for tool_id, tool_data in category_data.get('tools', {}).items():
                    tools[tool_id] = ToolConfig(
                        name=tool_data.get('name', tool_id),
                        description=tool_data.get('description', 'No description available'),
                        command=tool_data.get('command', ''),
                        params=tool_data.get('params', []),
                        defaults=tool_data.get('defaults', {})
                    )

                self.categories[category_id] = CategoryConfig(
                    name=category_data.get('name', category_id),
                    tools=tools
                )

            return self.categories

        except yaml.YAMLError as e:
            self.console.print(f"[bold red]Error:[/bold red] Invalid YAML configuration: {e}")
            raise
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to load configuration: {e}")
            raise


# ============================================================================
# Input Validation Classes
# ============================================================================

class InputValidator:
    """Handles validation of user inputs for security and correctness."""

    def __init__(self, console: Console) -> None:
        """
        Initialize the input validator.

        Args:
            console: Rich console for output
        """
        self.console: Console = console

        # Patterns for dangerous shell metacharacters
        self.dangerous_patterns = [
            r'[;&|`$<>]',     # Shell metacharacters
            r'\$\(',          # Command substitution
            r'`',             # Backticks
            r'\.\./',         # Directory traversal
            r'\n',            # Newline injection
            r'\r',            # Carriage return
        ]

    def validate_ipv4(self, ip_string: str) -> Tuple[bool, Optional[str]]:
        """Validate IPv4 address format."""
        try:
            ipaddress.IPv4Address(ip_string)
            return True, None
        except ValueError:
            return False, f"Invalid IPv4 address: '{ip_string}'. Expected format: xxx.xxx.xxx.xxx"

    def validate_hostname(self, hostname: str) -> Tuple[bool, Optional[str]]:
        """Validate hostname or FQDN format."""
        # Remove protocol if present
        hostname_clean = re.sub(r'^https?://', '', hostname)
        hostname_clean = hostname_clean.split('/')[0]
        hostname_clean = hostname_clean.split(':')[0]

        if len(hostname_clean) > 253:
            return False, "Hostname too long (max 253 characters)"

        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?)*$'

        if re.match(hostname_pattern, hostname_clean):
            return True, None

        return False, f"Invalid hostname format: '{hostname}'"

    def validate_ip_or_hostname(self, value: str) -> Tuple[bool, Optional[str]]:
        """Validate either IPv4 address or hostname."""
        is_valid_ipv4, _ = self.validate_ipv4(value)
        if is_valid_ipv4:
            return True, None

        is_valid_hostname, error_msg = self.validate_hostname(value)
        if is_valid_hostname:
            return True, None

        return False, f"Invalid target: '{value}'. Must be an IPv4 address (e.g., 192.168.1.1) or hostname (e.g., example.com)"

    def validate_port(self, port_string: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """Validate port number (1-65535)."""
        try:
            port = int(port_string)
            if 1 <= port <= 65535:
                return True, None, port
            else:
                return False, f"Port {port} out of range. Must be between 1-65535.", None
        except ValueError:
            return False, f"Invalid port: '{port_string}'. Must be an integer.", None

    def validate_url(self, url: str) -> Tuple[bool, Optional[str], str]:
        """
        Validate and normalize a URL input.
        Prevents protocol duplication (e.g., http://http://example.com)

        Args:
            url: URL string to validate

        Returns:
            Tuple of (is_valid, error_message, normalized_url)
        """
        url = url.strip()

        # Remove duplicate protocols (e.g., http://http://example.com -> http://example.com)
        url = re.sub(r'^(https?://)+', r'\1', url)

        # Remove trailing protocol without domain (cleanup edge case)
        url = re.sub(r'(https?://)$', '', url)

        # Add protocol if missing
        if url and not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        # Enhanced URL validation supporting:
        # - Hostnames and IP addresses
        # - Optional port numbers
        # - Optional paths
        url_pattern = r'^https?://([a-zA-Z0-9]([a-zA-Z0-9-_.]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-_.]{0,61}[a-zA-Z0-9])?)*|(\d{1,3}\.){3}\d{1,3})(:\d{1,5})?(/.*)?$'

        if re.match(url_pattern, url):
            return True, None, url

        return False, f"Invalid URL format: '{url}'", url

    def check_dangerous_input(self, value: str, param_name: str) -> Tuple[bool, Optional[str]]:
        """
        Check if input contains potentially dangerous shell metacharacters.

        Args:
            value: Input value to check
            param_name: Parameter name for context

        Returns:
            Tuple of (is_safe, warning_message)
        """
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, value):
                return False, (
                    f"Input contains potentially dangerous characters: '{value}'\n"
                    f"This could lead to command injection. Please use alphanumeric values."
                )

        return True, None

    def sanitize_input(self, value: str) -> str:
        """Sanitize user input to prevent command injection."""
        return value.strip()

    def validate_file_path(self, path_string: str, allow_missing: bool = False) -> Tuple[bool, Optional[str]]:
        """Validate file path with support for common wordlist aliases."""
        path_string = path_string.strip()

        if '..' in path_string:
            return False, "Directory traversal (..) not allowed for security"

        # Common wordlist aliases
        wordlist_aliases = {
            'rockyou': [
                '/usr/share/wordlists/rockyou.txt',
                '/usr/share/wordlists/rockyou.txt.gz',
            ],
            'dirb-common': [
                '/usr/share/wordlists/dirb/common.txt',
                '/usr/share/dirb/wordlists/common.txt',
            ],
            'dirbuster-medium': [
                '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
                '/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt',
            ],
        }

        for alias, paths in wordlist_aliases.items():
            if alias in path_string.lower():
                for alt_path in paths:
                    if Path(alt_path).exists():
                        return True, None
                if not allow_missing:
                    return False, f"Wordlist not found. Tried: {', '.join(paths)}"

        path = Path(path_string)
        if not path.exists():
            if allow_missing:
                return True, None
            return False, f"File not found: '{path_string}'"

        if not path.is_file():
            return False, f"Path is not a file: '{path_string}'"

        return True, None

    def get_validated_input(self, param_name: str, prompt_text: Optional[str] = None, default: Optional[str] = None) -> str:
        """
        Get and validate user input based on parameter type.

        Args:
            param_name: Name of the parameter (e.g., 'target_ip', 'port')
            prompt_text: Optional custom prompt text
            default: Optional default value

        Returns:
            Validated input string
        """
        if prompt_text is None:
            prompt_text = f"Enter {param_name.replace('_', ' ')}"

        # Add default to prompt if provided
        if default:
            prompt_text = f"{prompt_text} (default: {default})"

        while True:
            try:
                user_input = Prompt.ask(f"[cyan]{prompt_text}[/cyan]", default=default if default else "")

                # Use default if no input provided
                if not user_input.strip() and default:
                    user_input = default

                # Validate based on parameter name and type
                if 'ip' in param_name.lower() or 'target' in param_name.lower() or 'host' in param_name.lower():
                    # Support both IP and hostname
                    is_valid, error_msg = self.validate_ip_or_hostname(user_input)
                    if is_valid:
                        return self.sanitize_input(user_input)
                    else:
                        self.console.print(f"[bold red]✗[/bold red] {error_msg}")

                elif 'url' in param_name.lower():
                    # Validate and normalize URL
                    is_valid, error_msg, normalized_url = self.validate_url(user_input)
                    if is_valid:
                        return normalized_url
                    else:
                        self.console.print(f"[bold red]✗[/bold red] {error_msg}")

                elif 'port' in param_name.lower():
                    is_valid, error_msg, port_num = self.validate_port(user_input)
                    if is_valid:
                        return user_input
                    else:
                        self.console.print(f"[bold red]✗[/bold red] {error_msg}")

                elif 'wordlist' in param_name.lower() or 'file' in param_name.lower() or 'path' in param_name.lower():
                    # Validate file paths
                    is_valid, error_msg = self.validate_file_path(user_input)
                    if is_valid:
                        return self.sanitize_input(user_input)
                    else:
                        self.console.print(f"[bold red]✗[/bold red] {error_msg}")

                else:
                    # For other parameters, check for dangerous input
                    if user_input.strip():
                        is_safe, warning = self.check_dangerous_input(user_input, param_name)
                        if not is_safe:
                            self.console.print(f"[bold red]✗ Security Warning:[/bold red] {warning}")
                            if not Confirm.ask("[yellow]Continue with this input anyway?[/yellow]", default=False):
                                continue
                        return self.sanitize_input(user_input)
                    else:
                        self.console.print("[bold red]✗[/bold red] Input cannot be empty")

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Input cancelled by user[/yellow]")
                raise


# ============================================================================
# Dependency & System Checks
# ============================================================================

class DependencyChecker:
    """Checks for required system dependencies and tools."""

    def __init__(self, console: Console) -> None:
        """
        Initialize the dependency checker.

        Args:
            console: Rich console for output
        """
        self.console: Console = console

    def check_tool_exists(self, tool_name: str) -> bool:
        """
        Check if a tool/binary exists in the system PATH.
        Intelligently skips common wrapper commands (sudo, proxychains, etc.)

        Args:
            tool_name: Name of the tool to check

        Returns:
            True if tool exists, False otherwise
        """
        wrapper_commands = ['sudo', 'proxychains', 'proxychains4', 'timeout', 'nohup', 'nice', 'ionice']
        tokens = tool_name.split()

        actual_binary = None
        for token in tokens:
            if token not in wrapper_commands and not token.startswith('-'):
                actual_binary = token
                break

        if actual_binary:
            return shutil.which(actual_binary) is not None

        return shutil.which(tokens[0]) is not None if tokens else False

    def warn_missing_tool(self, tool_name: str) -> bool:
        """Warn user about missing tool and ask to continue."""
        self.console.print(
            Panel(
                f"[bold yellow]⚠ Warning:[/bold yellow] Tool '{tool_name}' not found in system PATH!\n\n"
                f"The command may fail to execute. Please ensure '{tool_name}' is installed.",
                title="Dependency Warning",
                border_style="yellow"
            )
        )

        return Confirm.ask("[yellow]Continue anyway?[/yellow]", default=False)


# Command Execution & Logging

class SessionLogger:
    """Handles logging of commands to file."""

    def __init__(self, log_file: Path) -> None:
        self.log_file: Path = log_file

    def log_command(self, command: str, category: str, tool_name: str) -> None:
        """Log executed command with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[{timestamp}] Category: {category} | Tool: {tool_name}\n"
            f"Command: {command}\n"
            f"{'-' * 80}\n"
        )

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # Silently fail to not interrupt the user experience
            pass

    def log_session_start(self) -> None:
        """Log the start of a new session."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"\n{'=' * 80}\n"
            f"SESSION START: {timestamp}\n"
            f"{'=' * 80}\n"
        )

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass


class CommandExecutor:
    """Handles execution of pentesting commands."""

    def __init__(
        self,
        console: Console,
        validator: InputValidator,
        dependency_checker: DependencyChecker,
        logger: SessionLogger
    ) -> None:
        """
        Initialize the command executor.

        Args:
            console: Rich console for output
            validator: Input validator instance
            dependency_checker: Dependency checker instance
            logger: Session logger instance
        """
        self.console: Console = console
        self.validator: InputValidator = validator
        self.dependency_checker: DependencyChecker = dependency_checker
        self.logger: SessionLogger = logger

    def prepare_command(self, tool: ToolConfig) -> Optional[str]:
        """Collect parameters and prepare command with shell-safe quoting."""
        command = tool.command
        params_dict = {}

        try:
            for param in tool.params:
                default_value = None
                if tool.defaults and param in tool.defaults:
                    default_value = tool.defaults[param]

                value = self.validator.get_validated_input(param, default=default_value)
                params_dict[param] = shlex.quote(value)

            prepared_command = command.format(**params_dict)
            return prepared_command

        except KeyboardInterrupt:
            return None
        except Exception as e:
            self.console.print(f"[bold red]Error preparing command:[/bold red] {e}")
            return None

    def execute(self, tool: ToolConfig, category_name: str, simulate: bool = False) -> None:
        """Execute a tool command or show it in simulation mode."""
        tool_binary = tool.command.split()[0]
        if not self.dependency_checker.check_tool_exists(tool_binary):
            if not self.dependency_checker.warn_missing_tool(tool_binary):
                return

        self.console.print(f"\n[bold cyan]🔧 Preparing:[/bold cyan] {tool.name}")
        self.console.print(f"[dim]{tool.description}[/dim]\n")

        prepared_command = self.prepare_command(tool)

        if prepared_command is None:
            self.console.print("[yellow]Command preparation cancelled[/yellow]")
            return

        self.console.print(
            Panel(
                f"[bold green]{prepared_command}[/bold green]",
                title="Generated Command",
                border_style="green"
            )
        )

        # Copy to clipboard
        try:
            pyperclip.copy(prepared_command)
            self.console.print("[dim]✓ Command copied to clipboard[/dim]\n")
        except Exception:
            pass

        # Log the command
        self.logger.log_command(prepared_command, category_name, tool.name)

        # Execute or simulate
        if not simulate:
            if Confirm.ask("[cyan]Execute this command now?[/cyan]", default=True):
                self._execute_with_progress(prepared_command)
        else:
            self.console.print("[yellow]Simulation mode - command not executed[/yellow]")

    def _execute_with_progress(self, command: str) -> None:
        """
        Execute command with a progress indicator.
        Uses safer subprocess execution with shell=False when possible.

        Args:
            command: Command to execute
        """
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Executing command...", total=None)

                # Try to execute without shell=True for better security
                # Fall back to shell=True for complex commands with pipes, etc.
                try:
                    # Parse command into arguments
                    args = shlex.split(command)
                    result = subprocess.run(
                        args,
                        shell=False,
                        capture_output=False,
                        text=True
                    )
                except (ValueError, FileNotFoundError):
                    # Fallback to shell=True for complex commands
                    # (e.g., commands with pipes, redirects)
                    self.console.print("[dim]Using shell mode for complex command...[/dim]")
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=False,
                        text=True
                    )

                progress.stop()

                if result.returncode == 0:
                    self.console.print("[bold green]✓ Command executed successfully[/bold green]")
                else:
                    self.console.print(f"[bold yellow]⚠ Command exited with code {result.returncode}[/bold yellow]")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Command execution interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"[bold red]Error executing command:[/bold red] {e}")


# ============================================================================
# User Interface Management
# ============================================================================

class UIManager:
    """Manages the user interface and menu interactions."""

    def __init__(self, console: Console) -> None:
        """
        Initialize the UI manager.

        Args:
            console: Rich console for output
        """
        self.console: Console = console

    def show_banner(self) -> None:
        """Display the application banner."""
        try:
            banner_text = pyfiglet.figlet_format("TAJAA", font="slant")
            self.console.print(f"[bold cyan]{banner_text}[/bold cyan]")
        except Exception:
            self.console.print("[bold cyan]TAJAA CLI[/bold cyan]\n")

        self.console.print(
            Panel(
                "[bold]Modular Cyber Security Framework[/bold]\n"
                "[dim]Version 3.1.0 | 8 Specialized Domains | 480+ Tools[/dim]",
                border_style="cyan"
            )
        )
        self.console.print()

    def show_categories_table(self, categories: Dict[str, CategoryConfig]) -> None:
        """
        Display available categories in a table.

        Args:
            categories: Dictionary of category configurations
        """
        table = Table(title="Available Categories", border_style="cyan")
        table.add_column("#", style="cyan", justify="center")
        table.add_column("Category", style="bold green")
        table.add_column("Tools Count", justify="center")

        for idx, (cat_id, cat_config) in enumerate(categories.items(), 1):
            table.add_row(str(idx), cat_config.name, str(len(cat_config.tools)))

        self.console.print(table)
        self.console.print()

    def select_category(self, categories: Dict[str, CategoryConfig]) -> Optional[str]:
        """
        Prompt user to select a category.

        Args:
            categories: Dictionary of category configurations

        Returns:
            Selected category ID or None if cancelled
        """
        try:
            choices = [
                Choice(value=cat_id, name=f"{cat_config.name} ({len(cat_config.tools)} tools)")
                for cat_id, cat_config in categories.items()
            ]
            choices.append(Choice(value="exit", name="[Exit]"))

            selected = inquirer.select(
                message="Select a category:",
                choices=choices,
                default=choices[0].value if choices else None
            ).execute()

            return None if selected == "exit" else selected

        except KeyboardInterrupt:
            return None

    def select_tool(self, category: CategoryConfig) -> Optional[str]:
        """
        Prompt user to select a tool from a category.

        Args:
            category: Category configuration

        Returns:
            Selected tool ID or None if cancelled
        """
        try:
            choices = [
                Choice(
                    value=tool_id,
                    name=f"{tool_config.name}\n  └─ {tool_config.description}"
                )
                for tool_id, tool_config in category.tools.items()
            ]
            choices.append(Choice(value="back", name="[← Back to Categories]"))

            selected = inquirer.select(
                message=f"Select a tool from {category.name}:",
                choices=choices,
                default=choices[0].value if choices else None
            ).execute()

            return None if selected == "back" else selected

        except KeyboardInterrupt:
            return None


# ============================================================================
# Main Application Class
# ============================================================================

class TajaaCLI:
    """Main application class orchestrating all components."""

    def __init__(self, config_path: Path, log_path: Path) -> None:
        """
        Initialize the Tajaa CLI application.

        Args:
            config_path: Path to module configuration file (e.g., configs/01_commands.yaml)
            log_path: Path to session log file
        """
        self.console: Console = Console()
        self.config_loader: ConfigLoader = ConfigLoader(config_path)
        self.validator: InputValidator = InputValidator(self.console)
        self.dependency_checker: DependencyChecker = DependencyChecker(self.console)
        self.logger: SessionLogger = SessionLogger(log_path)
        self.executor: CommandExecutor = CommandExecutor(
            self.console,
            self.validator,
            self.dependency_checker,
            self.logger
        )
        self.ui_manager: UIManager = UIManager(self.console)
        self.categories: Dict[str, CategoryConfig] = {}

    def initialize(self) -> bool:
        """
        Initialize the application by loading configuration.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.categories = self.config_loader.load()
            self.logger.log_session_start()
            return True
        except Exception as e:
            self.console.print(f"[bold red]Initialization failed:[/bold red] {e}")
            return False

    def run(self) -> None:
        """Main application loop."""
        try:
            self.ui_manager.show_banner()

            if not self.initialize():
                return

            while True:
                try:
                    # Show categories
                    self.ui_manager.show_categories_table(self.categories)

                    # Select category
                    selected_category_id = self.ui_manager.select_category(self.categories)

                    if selected_category_id is None:
                        break

                    category = self.categories[selected_category_id]

                    # Select tool
                    selected_tool_id = self.ui_manager.select_tool(category)

                    if selected_tool_id is None:
                        continue

                    tool = category.tools[selected_tool_id]

                    # Execute tool
                    self.executor.execute(tool, category.name)

                    # Ask if user wants to continue
                    self.console.print()
                    if not Confirm.ask("[cyan]Return to main menu?[/cyan]", default=True):
                        break

                    self.console.clear()
                    self.ui_manager.show_banner()

                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Returning to main menu...[/yellow]\n")
                    continue

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Exiting Tajaa CLI...[/yellow]")
        except Exception as e:
            self.console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        finally:
            self.console.print("\n[bold cyan]Thank you for using Tajaa CLI![/bold cyan]")
            self.console.print("[dim]Stay ethical. Happy hacking! 🔒[/dim]\n")


# ============================================================================
# CLI Entry Point
# ============================================================================

app = typer.Typer(
    name="tajaa",
    help="Tajaa CLI - The Ultimate Modular Cyber Security Framework with 8 specialized domains",
    add_completion=False
)


@app.command()
def main(
    config: Path = typer.Option(
        Path("configs/01_commands.yaml"),
        "--config",
        "-c",
        help="Path to specific module config (e.g., configs/02_ctf_kit.yaml, configs/07_osint_detective.yaml)"
    ),
    log: Path = typer.Option(
        Path("session_logs.txt"),
        "--log",
        "-l",
        help="Path to session log file"
    )
) -> None:
    """
    Launch the Tajaa CLI interactive interface.

    A production-grade modular cyber security framework for Kali Linux.
    Choose from 8 specialized domains: CTF, Web Bounty, Active Directory,
    Mobile/IoT, Cloud Security, OSINT, Wireless, and Post-Exploitation.
    """
    tajaa = TajaaCLI(config_path=config, log_path=log)
    tajaa.run()


if __name__ == "__main__":
    app()
