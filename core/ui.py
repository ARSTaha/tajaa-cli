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
[bold #00FFFF]
████████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██    ██████████╗  ███████╗      ██╗  ███████╗  ███████╗                      ██
██    ╚══██╔═══╝  ██╔═══██║      ██║  ██╔═══██║ ██╔═══██║                     ██
██       ██║      ████████║      ██║  ████████║ ████████║                     ██
██       ██║      ██╔═══██║ ██   ██║  ██╔═══██║ ██╔═══██║                     ██
██       ██║      ██║   ██║ ╚█████╔╝  ██║   ██║ ██║   ██║                     ██
██       ╚═╝      ╚═╝   ╚═╝  ╚════╝   ╚═╝   ╚═╝ ╚═╝   ╚═╝                     ██
██                                                                            ██
██[/bold #00FFFF][#FF00FF]    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      [/#FF00FF]██
██[bold #00FF00]              ╔═══════════════════════════════════════════════╗              [/bold #00FF00]██
██[bold #00FF00]              ║[/bold #00FF00][#FFFF00]  ⚡ CYBER SECURITY FRAMEWORK v5.0 ⚡  [/#FFFF00][bold #00FF00]║              [/bold #00FF00]██
██[bold #00FF00]              ╚═══════════════════════════════════════════════╝              [/bold #00FF00]██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████
[/bold #00FFFF]"""

# Compact banner for after initialization
BANNER_COMPACT = """[bold #00FFFF]
╔══════════════════════════════════════════════════════════════════╗
║  [bold #FF00FF]████████╗[/bold #FF00FF][bold #00FFFF]  __ _   (_)  __ _    __ _   [/bold #00FFFF][#00FF00]⚡ v5.0[/#00FF00]  [bold #FFFF00]💀[/bold #FFFF00]            ║
║  [bold #FF00FF]╚══██╔══╝[/bold #FF00FF][bold #00FFFF] / _` |  | | / _` |  / _` |[/bold #00FFFF]   [dim]Cyber Security Framework[/dim]   ║
║  [bold #FF00FF]   ██║   [/bold #FF00FF][bold #00FFFF]| (_| |  | || (_| | | (_| |[/bold #00FFFF]   [dim]────────────────────────[/dim]   ║
║  [bold #FF00FF]   ╚═╝   [/bold #FF00FF][bold #00FFFF] \\__,_| _/ | \\__,_|  \\__,_|[/bold #00FFFF]   [dim]By Tajaa[/dim]                    ║
║                  [bold #00FFFF]|__/[/bold #00FFFF]                                                  ║
╚══════════════════════════════════════════════════════════════════╝
[/bold #00FFFF]"""


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
            ("[#00FF00]█[/#00FF00] Initializing neural network...", 0.03),
            ("[#00FF00]█[/#00FF00] Loading cryptographic modules...", 0.02),
            ("[#00FF00]█[/#00FF00] Establishing secure channels...", 0.02),
            ("[#00FF00]█[/#00FF00] Calibrating attack vectors...", 0.03),
            ("[#00FF00]█[/#00FF00] Synchronizing with C2 servers...", 0.02),
            ("[#00FF00]█[/#00FF00] Bypassing detection systems...", 0.03),
            ("[#00FF00]█[/#00FF00] [bold]SYSTEM READY[/bold]", 0.05),
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
        self.console.print("[bold #00FFFF]  ╔═══════════════════════════════════════════════════════════╗[/bold #00FFFF]")
        self.console.print("[bold #00FFFF]  ║[/bold #00FFFF]            [bold #FF00FF]⚡ SYSTEM INITIALIZATION ⚡[/bold #FF00FF]            [bold #00FFFF]║[/bold #00FFFF]")
        self.console.print("[bold #00FFFF]  ╚═══════════════════════════════════════════════════════════╝[/bold #00FFFF]")
        self.console.print()

        with Progress(
            SpinnerColumn("dots", style="#00FFFF"),
            TextColumn("[bold #FF00FF]{task.description}[/bold #FF00FF]"),
            BarColumn(bar_width=40, style="#333355", complete_style="#00FF00", finished_style="#00FF00"),
            TaskProgressColumn(),
            console=self.console,
            transient=True,
        ) as progress:
            for task_name, weight in init_tasks:
                task = progress.add_task(f"  {task_name}...", total=100)
                for i in range(100):
                    await asyncio.sleep(0.005 * (weight / 15))
                    progress.update(task, advance=1)

        self.console.print("  [bold #00FF00]✓ All systems operational[/bold #00FF00]")
        await asyncio.sleep(0.3)

    async def _ready_state(self) -> None:
        """Show ready state."""
        self.console.print()
        ready_text = Text()
        ready_text.append("  ◈ ", style="bold #FF00FF")
        ready_text.append("TAJAA ", style="bold #00FFFF")
        ready_text.append("READY ", style="bold #00FF00")
        ready_text.append("◈", style="bold #FF00FF")
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
        header_text.append(" 💀 ", style="bold #FF00FF")
        header_text.append("TAJAA", style="bold #00FFFF")
        header_text.append(" │ ", style="dim")
        header_text.append("Cyber Security Framework", style="dim #00FF00")
        header_text.append(" │ ", style="dim")
        header_text.append(datetime.now().strftime("%H:%M:%S"), style="#FFFF00")

        return Panel(
            Align.center(header_text),
            style="bold #00FFFF on #0a0a0f",
            box=box.MINIMAL,
        )

    def _make_target_panel(self) -> Panel:
        """Generate target info panel."""
        content = []

        if self._active_target:
            content.append(f"[bold #00FFFF]🎯 Target:[/bold #00FFFF]")
            content.append(f"   [#00FF00]{self._active_target}[/#00FF00]")
        else:
            content.append("[dim]No active target[/dim]")

        ports = self._status.get('ports', [])
        if ports:
            content.append(f"\n[bold #FF00FF]🔓 Open Ports:[/bold #FF00FF]")
            content.append(f"   [#FFFF00]{', '.join(map(str, ports[:10]))}[/#FFFF00]")
            if len(ports) > 10:
                content.append(f"   [dim]+{len(ports) - 10} more[/dim]")

        return Panel(
            "\n".join(content),
            title="[bold #00FFFF]Target Info[/bold #00FFFF]",
            border_style="#333355",
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
            f"[bold #00FF00]$ {command}[/bold #00FF00]",
            title="[bold #00FFFF]Command[/bold #00FFFF]",
            border_style="#00FF00",
            box=box.HEAVY,
        )

    @staticmethod
    def status_indicator(status: str) -> Text:
        """Create a status indicator."""
        indicators = {
            'success': ("✓", "#00FF00"),
            'error': ("✗", "#FF3366"),
            'warning': ("⚠", "#FFAA00"),
            'info': ("ℹ", "#00CCFF"),
            'running': ("●", "#00FFFF"),
            'pending': ("○", "#666666"),
        }

        icon, color = indicators.get(status, ("?", "#FFFFFF"))
        text = Text()
        text.append(f" {icon} ", style=f"bold {color}")
        return text

    @staticmethod
    def progress_bar(progress: float, width: int = 30) -> Text:
        """Create a neon progress bar."""
        filled = int(progress * width)
        empty = width - filled

        bar = Text()
        bar.append("█" * filled, style="#00FF00")
        bar.append("░" * empty, style="#333355")
        bar.append(f" {progress * 100:.0f}%", style="bold #00FFFF")
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
        self.console.print("[bold #00FFFF]  ╔═══ CATEGORIES ═══════════════════════════════════════════╗[/bold #00FFFF]")
        self.console.print()

        for idx, (cat_id, cat_data) in enumerate(categories.items(), 1):
            name = cat_data.get('name', cat_id)
            count = len(cat_data.get('tools', {}))

            # Add emoji based on category
            emoji = self._get_category_emoji(cat_id)

            self.console.print(
                f"  [dim]{idx:2}.[/dim]  {emoji}  [bold #00FFFF]{name}[/bold #00FFFF]  "
                f"[dim]─────[/dim] [#FF00FF]{count} tools[/#FF00FF]"
            )

        self.console.print()
        self.console.print("[bold #00FFFF]  ╚═══════════════════════════════════════════════════════════╝[/bold #00FFFF]")
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
        self.console.print(f"[bold #FF00FF]  ╔═══ {category_name.upper()} ═══[/bold #FF00FF]")
        self.console.print()

        for idx, (tool_id, tool_data) in enumerate(tools.items(), 1):
            name = tool_data.get('name', tool_id)
            desc = tool_data.get('description', '')[:50]

            self.console.print(
                f"  [dim]{idx:2}.[/dim]  🔧  [bold #00FF00]{name}[/bold #00FF00]"
            )
            if desc:
                self.console.print(f"        [dim]{desc}...[/dim]")

        self.console.print()
        self.console.print(f"[bold #FF00FF]  ╚{'═' * 50}[/bold #FF00FF]")
        self.console.print()

    def show_suggestions(self, suggestions: List[Dict]) -> None:
        """Display tool suggestions."""
        if not suggestions:
            return

        self.console.print()
        self.console.print("[bold #FFFF00]  💡 RECOMMENDED TOOLS[/bold #FFFF00]")
        self.console.print("  [dim]─────────────────────────────────────────[/dim]")

        for sugg in suggestions[:5]:
            self.console.print(
                f"  [#00FF00]▸[/#00FF00] [bold]{sugg.get('tool_name', '')}[/bold]"
            )
            self.console.print(f"    [dim]{sugg.get('reason', '')}[/dim]")

        self.console.print()

    def show_command(self, tool_name: str, command: str, description: str = "") -> None:
        """Display a command in styled format."""
        self.console.print()
        self.console.print(f"[bold #00FFFF]  ┌─ 🔧 {tool_name}[/bold #00FFFF]")
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
                    self.console.print(f"[#00FF00]{current} \\[/#00FF00]")
                    current = "      " + part
                else:
                    current += " " + part if current.strip() else "    " + part
            if current.strip():
                self.console.print(f"[#00FF00]{current}[/#00FF00]")
        else:
            self.console.print(f"    [#00FF00]{command}[/#00FF00]")

        self.console.print()

    def show_result(self, success: bool, message: str = "") -> None:
        """Display execution result."""
        if success:
            self.console.print(f"  [bold #00FF00]✓ {message or 'Completed successfully'}[/bold #00FF00]")
        else:
            self.console.print(f"  [bold #FF3366]✗ {message or 'Execution failed'}[/bold #FF3366]")

    def show_search_results(self, results: List[tuple], query: str) -> None:
        """Display search results."""
        self.console.print()
        self.console.print(f"[bold #00FFFF]  🔍 Search Results for '{query}'[/bold #00FFFF]")
        self.console.print("  [dim]─────────────────────────────────────────[/dim]")

        if not results:
            self.console.print("  [dim]No results found[/dim]")
        else:
            for idx, (tool, score) in enumerate(results[:15], 1):
                confidence_bar = "█" * (score // 20) + "░" * (5 - score // 20)
                self.console.print(
                    f"  [dim]{idx:2}.[/dim] [bold #00FF00]{tool.metadata.name}[/bold #00FF00] "
                    f"[dim]│[/dim] [{CyberpunkTheme.NEON_YELLOW}]{confidence_bar}[/{CyberpunkTheme.NEON_YELLOW}]"
                )
                self.console.print(f"      [dim]{tool.metadata.description[:60]}...[/dim]")

        self.console.print()

    def confirm(self, message: str, default: bool = True) -> bool:
        """Show styled confirmation prompt."""
        from rich.prompt import Confirm
        return Confirm.ask(f"  [bold #00FFFF]{message}[/bold #00FFFF]", default=default)

    def prompt(self, message: str, default: str = "") -> str:
        """Show styled input prompt."""
        from rich.prompt import Prompt
        display = f"  [cyan]›[/cyan] {message}"
        if default:
            display += f" [dim]({default})[/dim]"
        return Prompt.ask(display, default=default)

