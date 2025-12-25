"""
Tajaa UI Module
Hyper-modern cyberpunk user interface with cinematic effects.
Author: Tajaa
"""

import asyncio
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.align import Align
from rich.style import Style
from rich.box import DOUBLE, HEAVY, ROUNDED, MINIMAL
from rich import box


# =============================================================================
# CYBERPUNK COLOR SCHEME
# =============================================================================

class CyberpunkTheme:
    """Cyberpunk color palette."""
    # Primary colors
    NEON_CYAN = "#00FFFF"
    NEON_MAGENTA = "#FF00FF"
    NEON_GREEN = "#00FF00"
    NEON_YELLOW = "#FFFF00"
    NEON_RED = "#FF0044"
    NEON_BLUE = "#0088FF"
    NEON_PURPLE = "#AA00FF"
    NEON_ORANGE = "#FF8800"

    # Background/accent
    DARK_BG = "#0a0a0f"
    DARK_PANEL = "#111122"
    GRID_LINE = "#333355"

    # Status colors
    SUCCESS = "#00FF88"
    WARNING = "#FFAA00"
    ERROR = "#FF3366"
    INFO = "#00CCFF"

    # Gradients (for text effects)
    GRADIENT_1 = ["#FF0080", "#FF00FF", "#8000FF", "#0080FF", "#00FFFF"]
    GRADIENT_2 = ["#00FFFF", "#00FF80", "#80FF00", "#FFFF00", "#FF8000"]


# =============================================================================
# ASCII ART BANNERS
# =============================================================================

# 3D Neon ASCII Art Banner - Massive and cinematic
BANNER_3D = """
[bold cyan]████████████████████████████████████████████████████████████████████████████████[/bold cyan]
[bold cyan]██                                                                            ██[/bold cyan]
[bold cyan]██    ██████████╗  ███████╗      ██╗  ███████╗  ███████╗                      ██[/bold cyan]
[bold cyan]██    ╚══██╔═══╝  ██╔═══██║      ██║  ██╔═══██║ ██╔═══██║                     ██[/bold cyan]
[bold cyan]██       ██║      ████████║      ██║  ████████║ ████████║                     ██[/bold cyan]
[bold cyan]██       ██║      ██╔═══██║ ██   ██║  ██╔═══██║ ██╔═══██║                     ██[/bold cyan]
[bold cyan]██       ██║      ██║   ██║ ╚█████╔╝  ██║   ██║ ██║   ██║                     ██[/bold cyan]
[bold cyan]██       ╚═╝      ╚═╝   ╚═╝  ╚════╝   ╚═╝   ╚═╝ ╚═╝   ╚═╝                     ██[/bold cyan]
[bold cyan]██                                                                            ██[/bold cyan]
[bold cyan]██[/bold cyan][magenta]    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      [/magenta][bold cyan]██[/bold cyan]
[bold green]██              ╔═══════════════════════════════════════════════╗              ██[/bold green]
[bold green]██              ║[/bold green][yellow]  ⚡ CYBER SECURITY FRAMEWORK v5.0 ⚡  [/yellow][bold green]║              ██[/bold green]
[bold green]██              ╚═══════════════════════════════════════════════╝              ██[/bold green]
[bold cyan]██                                                                            ██[/bold cyan]
[bold cyan]████████████████████████████████████████████████████████████████████████████████[/bold cyan]
"""

# Compact banner for after initialization
BANNER_COMPACT = """
[bold cyan]╔══════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]████████╗[/bold magenta]  __ _   (_)  __ _    __ _   [green]⚡ v5.0[/green]  [bold yellow]💀[/bold yellow]            [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]╚══██╔══╝[/bold magenta] / _` |  | | / _` |  / _` |   [dim]Cyber Security Framework[/dim]   [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]   ██║   [/bold magenta]| (_| |  | || (_| | | (_| |   [dim]────────────────────────[/dim]   [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]   ╚═╝   [/bold magenta] \\__,_| _/ | \\__,_|  \\__,_|   [dim]By Tajaa[/dim]                    [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                  |__/                                                  [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════════╝[/bold cyan]
"""


# =============================================================================
# CINEMATIC INTRO
# =============================================================================

class CinematicIntro:
    """Creates stunning startup sequences."""

    def __init__(self, console: Console = None):
        self.console = console or Console()

    async def play(self, skip: bool = False) -> None:
        """Play the cinematic intro sequence."""
        if skip:
            self.console.print(BANNER_COMPACT)
            return

        self.console.clear()

        # Phase 1: Matrix-style startup text
        await self._matrix_boot()

        # Phase 2: Main banner reveal
        await self._reveal_banner()

        # Phase 3: System initialization
        await self._system_init()

        # Phase 4: Ready state
        await self._ready_state()

    async def _matrix_boot(self) -> None:
        """Matrix-style boot sequence."""
        boot_messages = [
            ("[green]█[/green] Initializing neural network...", 0.03),
            ("[green]█[/green] Loading cryptographic modules...", 0.02),
            ("[green]█[/green] Establishing secure channels...", 0.02),
            ("[green]█[/green] Calibrating attack vectors...", 0.03),
            ("[green]█[/green] Synchronizing with C2 servers...", 0.02),
            ("[green]█[/green] Bypassing detection systems...", 0.03),
            ("[green]█[/green] [bold]SYSTEM READY[/bold]", 0.05),
        ]

        for msg, delay in boot_messages:
            # Typing effect
            full_msg = ""
            for char in msg:
                full_msg += char
                self.console.print(full_msg, end="\r")
                await asyncio.sleep(0.01)
            self.console.print(msg)
            await asyncio.sleep(delay)

        await asyncio.sleep(0.5)
        self.console.clear()

    async def _reveal_banner(self) -> None:
        """Reveal the main banner with animation."""
        lines = BANNER_3D.strip().split('\n')

        # Reveal line by line
        for i, line in enumerate(lines):
            self.console.print(line)
            await asyncio.sleep(0.02)

        await asyncio.sleep(0.3)

    async def _system_init(self) -> None:
        """System initialization progress bar."""
        init_tasks = [
            ("Loading 480+ tools", 15),
            ("Initializing database", 10),
            ("Setting up plugins", 20),
            ("Configuring AI engine", 15),
            ("Preparing attack chains", 10),
            ("Securing communications", 10),
            ("Final checks", 20),
        ]

        self.console.print()
        self.console.print("[bold cyan]  ╔═══════════════════════════════════════════════════════════╗[/bold cyan]")
        self.console.print("[bold cyan]  ║[/bold cyan]            [bold magenta]⚡ SYSTEM INITIALIZATION ⚡[/bold magenta]            [bold cyan]║[/bold cyan]")
        self.console.print("[bold cyan]  ╚═══════════════════════════════════════════════════════════╝[/bold cyan]")
        self.console.print()

        with Progress(
            SpinnerColumn("dots", style="cyan"),
            TextColumn("[bold magenta]{task.description}[/bold magenta]"),
            BarColumn(bar_width=40, style="dim", complete_style="green", finished_style="green"),
            TaskProgressColumn(),
            console=self.console,
            transient=True,
        ) as progress:
            for task_name, weight in init_tasks:
                task = progress.add_task(f"  {task_name}...", total=100)
                for i in range(100):
                    await asyncio.sleep(0.005 * (weight / 15))
                    progress.update(task, advance=1)

        self.console.print("  [bold green]✓ All systems operational[/bold green]")
        await asyncio.sleep(0.3)

    async def _ready_state(self) -> None:
        """Show ready state."""
        self.console.print()
        ready_text = Text()
        ready_text.append("  ◈ ", style="bold magenta")
        ready_text.append("TAJAA ", style="bold cyan")
        ready_text.append("READY ", style="bold green")
        ready_text.append("◈", style="bold magenta")
        self.console.print(ready_text)
        self.console.print()
        await asyncio.sleep(0.5)


# =============================================================================
# SPLIT-SCREEN DASHBOARD
# =============================================================================

class DashboardLayout:
    """Split-screen dashboard layout manager."""

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self._layout = Layout()
        self._setup_layout()

        # Content stores
        self._logs: List[str] = []
        self._status: Dict[str, Any] = {}
        self._active_target: str = ""
        self._running_tasks: List[Dict] = []

    def _setup_layout(self) -> None:
        """Setup the dashboard layout structure."""
        self._layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )

        self._layout["main"].split_row(
            Layout(name="sidebar", ratio=1),
            Layout(name="content", ratio=3),
        )

        self._layout["sidebar"].split(
            Layout(name="target_info", size=8),
            Layout(name="tasks", ratio=1),
        )

    def _make_header(self) -> Panel:
        """Generate header panel."""
        header_text = Text()
        header_text.append(" 💀 ", style="bold magenta")
        header_text.append("TAJAA", style="bold cyan")
        header_text.append(" │ ", style="dim")
        header_text.append("Cyber Security Framework", style="dim green")
        header_text.append(" │ ", style="dim")
        header_text.append(datetime.now().strftime("%H:%M:%S"), style="yellow")

        return Panel(
            Align.center(header_text),
            style="bold cyan",
            box=box.MINIMAL,
        )

    def _make_target_panel(self) -> Panel:
        """Generate target info panel."""
        content = []

        if self._active_target:
            content.append(f"[bold cyan]🎯 Target:[/bold cyan]")
            content.append(f"   [green]{self._active_target}[/green]")
        else:
            content.append("[dim]No active target[/dim]")

        ports = self._status.get('ports', [])
        if ports:
            content.append(f"\n[bold magenta]🔓 Open Ports:[/bold magenta]")
            content.append(f"   [yellow]{', '.join(map(str, ports[:10]))}[/yellow]")
            if len(ports) > 10:
                content.append(f"   [dim]+{len(ports) - 10} more[/dim]")

        return Panel(
            "\n".join(content),
            title="[bold cyan]Target Info[/bold cyan]",
            border_style="dim",
            box=box.ROUNDED,
        )

    def _make_tasks_panel(self) -> Panel:
        """Generate running tasks panel."""
        if not self._running_tasks:
            content = "[dim]No background tasks[/dim]"
        else:
            table = Table(box=None, show_header=False, padding=(0, 1))
            table.add_column("Status", width=2)
            table.add_column("Task")

            for task in self._running_tasks[-5:]:
                status_icon = "🔄" if task.get('status') == 'running' else "✓"
                table.add_row(status_icon, task.get('name', '')[:20])

            content = table

        return Panel(
            content,
            title="[bold #FF00FF]Background Tasks[/bold #FF00FF]",
            border_style="#333355",
            box=box.ROUNDED,
        )

    def _make_content_panel(self, content: Any = None) -> Panel:
        """Generate main content panel."""
        return Panel(
            content or "[dim]Select a tool to begin[/dim]",
            title="[bold #00FF00]⚡ Active Terminal[/bold #00FF00]",
            border_style="#00FF00",
            box=box.DOUBLE,
        )

    def _make_logs_panel(self) -> Panel:
        """Generate logs panel."""
        if not self._logs:
            content = "[dim]No recent activity[/dim]"
        else:
            content = "\n".join(self._logs[-20:])

        return Panel(
            content,
            title="[bold #FFFF00]📋 Activity Log[/bold #FFFF00]",
            border_style="#333355",
            box=box.ROUNDED,
        )

    def _make_footer(self) -> Panel:
        """Generate footer panel."""
        footer_text = Text()
        footer_text.append(" [", style="dim")
        footer_text.append("q", style="bold #FF00FF")
        footer_text.append("] Quit  ", style="dim")
        footer_text.append("[", style="dim")
        footer_text.append("s", style="bold #FF00FF")
        footer_text.append("] Search  ", style="dim")
        footer_text.append("[", style="dim")
        footer_text.append("b", style="bold #FF00FF")
        footer_text.append("] Back  ", style="dim")
        footer_text.append("[", style="dim")
        footer_text.append("t", style="bold #FF00FF")
        footer_text.append("] Tasks  ", style="dim")
        footer_text.append("[", style="dim")
        footer_text.append("?", style="bold #FF00FF")
        footer_text.append("] Help", style="dim")

        return Panel(
            Align.center(footer_text),
            style="on #0a0a0f",
            box=box.MINIMAL,
        )

    def update(self, target: str = None, ports: List[int] = None,
               tasks: List[Dict] = None, log: str = None) -> None:
        """Update dashboard state."""
        if target is not None:
            self._active_target = target
        if ports is not None:
            self._status['ports'] = ports
        if tasks is not None:
            self._running_tasks = tasks
        if log:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self._logs.append(f"[dim]{timestamp}[/dim] {log}")

    def render(self, main_content: Any = None) -> Layout:
        """Render the complete dashboard."""
        self._layout["header"].update(self._make_header())
        self._layout["target_info"].update(self._make_target_panel())
        self._layout["tasks"].update(self._make_tasks_panel())
        self._layout["content"].update(self._make_content_panel(main_content))
        self._layout["footer"].update(self._make_footer())

        return self._layout


# =============================================================================
# UI COMPONENTS
# =============================================================================

class UIComponents:
    """Reusable UI components."""

    @staticmethod
    def category_card(name: str, tool_count: int, icon: str = "📁") -> Panel:
        """Create a category card."""
        return Panel(
            f"[bold #00FFFF]{icon} {name}[/bold #00FFFF]\n[dim]{tool_count} tools[/dim]",
            border_style="#333355",
            box=box.ROUNDED,
            padding=(0, 2),
        )

    @staticmethod
    def tool_card(name: str, description: str, tags: List[str] = None) -> Panel:
        """Create a tool card."""
        content = Text()
        content.append(f"🔧 {name}\n", style="bold #00FF00")
        content.append(f"{description}\n", style="dim")
        if tags:
            content.append("Tags: ", style="dim #FF00FF")
            content.append(", ".join(tags[:3]), style="#FF00FF")

        return Panel(
            content,
            border_style="#333355",
            box=box.ROUNDED,
        )

    @staticmethod
    def suggestion_card(suggestions: List[Dict]) -> Panel:
        """Create a suggestions card."""
        table = Table(box=None, show_header=False)
        table.add_column("Icon", width=3)
        table.add_column("Tool")
        table.add_column("Reason")

        for sugg in suggestions[:5]:
            table.add_row(
                "💡",
                f"[bold #00FF00]{sugg.get('tool', '')}[/bold #00FF00]",
                f"[dim]{sugg.get('reason', '')}[/dim]"
            )

        return Panel(
            table,
            title="[bold #FFFF00]⚡ Recommended[/bold #FFFF00]",
            border_style="#FFFF00",
            box=box.ROUNDED,
        )

    @staticmethod
    def command_box(command: str) -> Panel:
        """Create a styled command display box."""
        return Panel(
            f"[bold green]$ {command}[/bold green]",
            title="[bold cyan]Command[/bold cyan]",
            border_style="green",
            box=box.HEAVY,
        )

    @staticmethod
    def status_indicator(status: str) -> Text:
        """Create a status indicator."""
        indicators = {
            'success': ("✓", "green"),
            'error': ("✗", "red"),
            'warning': ("⚠", "yellow"),
            'info': ("ℹ", "cyan"),
            'running': ("●", "cyan"),
            'pending': ("○", "dim"),
        }

        icon, color = indicators.get(status, ("?", "white"))
        text = Text()
        text.append(f" {icon} ", style=f"bold {color}")
        return text

    @staticmethod
    def progress_bar(progress: float, width: int = 30) -> Text:
        """Create a neon progress bar."""
        filled = int(progress * width)
        empty = width - filled

        bar = Text()
        bar.append("█" * filled, style="green")
        bar.append("░" * empty, style="dim")
        bar.append(f" {progress * 100:.0f}%", style="bold cyan")
        return bar


class TajaaUI:
    """Main UI manager for Tajaa."""

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.intro = CinematicIntro(self.console)
        self.dashboard = DashboardLayout(self.console)
        self.components = UIComponents()
        self._use_dashboard = False

    async def show_intro(self, skip: bool = False) -> None:
        """Show the intro sequence."""
        await self.intro.play(skip=skip)

    def show_banner(self) -> None:
        """Show the compact banner."""
        self.console.print(BANNER_COMPACT)

    def show_categories(self, categories: Dict[str, Any]) -> None:
        """Display categories in a grid."""
        self.console.print()
        self.console.print("[bold cyan]  ╔═══ CATEGORIES ═══════════════════════════════════════════╗[/bold cyan]")
        self.console.print()

        for idx, (cat_id, cat_data) in enumerate(categories.items(), 1):
            name = cat_data.get('name', cat_id)
            count = len(cat_data.get('tools', {}))

            # Add emoji based on category
            emoji = self._get_category_emoji(cat_id)

            self.console.print(
                f"  [dim]{idx:2}.[/dim]  {emoji}  [bold cyan]{name}[/bold cyan]  "
                f"[dim]─────[/dim] [magenta]{count} tools[/magenta]"
            )

        self.console.print()
        self.console.print("[bold cyan]  ╚═══════════════════════════════════════════════════════════╝[/bold cyan]")
        self.console.print()

    def _get_category_emoji(self, cat_id: str) -> str:
        """Get emoji for category."""
        emoji_map = {
            'reconnaissance': '🔍',
            'recon': '🔍',
            'web': '🌐',
            'web_apps': '🌐',
            'web_bounty': '🎯',
            'wireless': '📡',
            'wireless_radio': '📡',
            'sniffing': '🎭',
            'exploitation': '💀',
            'post_exploitation': '🔓',
            'post_exploit': '🔓',
            'osint': '🕵️',
            'osint_detective': '🕵️',
            'mobile': '📱',
            'mobile_iot': '📱',
            'cloud': '☁️',
            'cloud_auditor': '☁️',
            'network': '🔗',
            'network_ad': '🔗',
            'ctf': '🏁',
            'ctf_kit': '🏁',
            'commands': '⚡',
        }
        return emoji_map.get(cat_id.lower(), '📦')

    def show_tools(self, category_name: str, tools: Dict[str, Any]) -> None:
        """Display tools in a category."""
        self.console.print()
        self.console.print(f"[bold magenta]  ╔═══ {category_name.upper()} ═══[/bold magenta]")
        self.console.print()

        for idx, (tool_id, tool_data) in enumerate(tools.items(), 1):
            name = tool_data.get('name', tool_id)
            desc = tool_data.get('description', '')[:50]

            self.console.print(
                f"  [dim]{idx:2}.[/dim]  🔧  [bold green]{name}[/bold green]"
            )
            if desc:
                self.console.print(f"        [dim]{desc}...[/dim]")

        self.console.print()
        self.console.print(f"[bold magenta]  ╚{'═' * 50}[/bold magenta]")
        self.console.print()

    def show_suggestions(self, suggestions: List[Dict]) -> None:
        """Display tool suggestions."""
        if not suggestions:
            return

        self.console.print()
        self.console.print("[bold yellow]  💡 RECOMMENDED TOOLS[/bold yellow]")
        self.console.print("  [dim]─────────────────────────────────────────[/dim]")

        for sugg in suggestions[:5]:
            self.console.print(
                f"  [green]▸[/green] [bold]{sugg.get('tool_name', '')}[/bold]"
            )
            self.console.print(f"    [dim]{sugg.get('reason', '')}[/dim]")

        self.console.print()

    def show_command(self, tool_name: str, command: str, description: str = "") -> None:
        """Display a command in styled format."""
        self.console.print()
        self.console.print(f"[bold cyan]  ┌─ 🔧 {tool_name}[/bold cyan]")
        if description:
            self.console.print(f"[dim]  │  {description}[/dim]")
        self.console.print(f"[dim]  └{'─' * 55}[/dim]")
        self.console.print()
        self.console.print("[bold]  Command:[/bold]")
        self.console.print()

        # Format long commands
        if len(command) > 70:
            parts = command.split(' ')
            current = "    "
            for part in parts:
                if len(current) + len(part) > 70:
                    self.console.print(f"[green]{current} \\[/green]")
                    current = "      " + part
                else:
                    current += " " + part if current.strip() else "    " + part
            if current.strip():
                self.console.print(f"[green]{current}[/green]")
        else:
            self.console.print(f"    [green]{command}[/green]")

        self.console.print()

    def show_result(self, success: bool, message: str = "") -> None:
        """Display execution result."""
        if success:
            self.console.print(f"  [bold green]✓ {message or 'Completed successfully'}[/bold green]")
        else:
            self.console.print(f"  [bold red]✗ {message or 'Execution failed'}[/bold red]")

    def show_search_results(self, results: List[tuple], query: str) -> None:
        """Display search results."""
        self.console.print()
        self.console.print(f"[bold cyan]  🔍 Search Results for '{query}'[/bold cyan]")
        self.console.print("  [dim]─────────────────────────────────────────[/dim]")

        if not results:
            self.console.print("  [dim]No results found[/dim]")
        else:
            for idx, (tool, score) in enumerate(results[:15], 1):
                # Convert score to int for string multiplication
                score_int = int(score) if isinstance(score, float) else score
                filled = min(5, max(0, score_int // 20))
                confidence_bar = "█" * filled + "░" * (5 - filled)

                # Handle both ToolInfo objects and objects with metadata attribute
                if hasattr(tool, 'metadata'):
                    name = tool.metadata.name
                    desc = tool.metadata.description[:60] if tool.metadata.description else ''
                elif hasattr(tool, 'name'):
                    name = tool.name
                    desc = (tool.description[:60] if hasattr(tool, 'description') and tool.description else '')
                else:
                    name = str(tool)
                    desc = ''

                self.console.print(
                    f"  [dim]{idx:2}.[/dim] [bold green]{name}[/bold green] "
                    f"[dim]│[/dim] [yellow]{confidence_bar}[/yellow]"
                )
                if desc:
                    self.console.print(f"      [dim]{desc}...[/dim]")

        self.console.print()

    def confirm(self, message: str, default: bool = True) -> bool:
        """Show styled confirmation prompt."""
        from rich.prompt import Confirm
        return Confirm.ask(f"  [bold cyan]{message}[/bold cyan]", default=default)

    def prompt(self, message: str, default: str = "") -> str:
        """Show styled input prompt."""
        from rich.prompt import Prompt
        display = f"  [cyan]›[/cyan] {message}"
        if default:
            display += f" [dim]({default})[/dim]"
        return Prompt.ask(display, default=default)

