# Tajaa CLI Architecture

> Version 5.0.0 - The Universe-Class Cyber Security Framework

## Overview

Tajaa CLI is built on a modular, async-first architecture designed for maximum performance, extensibility, and user experience. This document describes the internal architecture and how components interact.

## Directory Structure

```
tajaa-cli/
├── main.py                  # Entry point & application orchestrator
├── requirements.txt         # Python dependencies
├── core/                    # Core framework modules
│   ├── __init__.py
│   ├── database.py          # SQLite async database layer
│   ├── engine.py            # Async command execution engine
│   ├── intelligence.py      # AI-like suggestion system
│   ├── plugin.py            # Dynamic plugin architecture
│   ├── session.py           # Session & state management
│   └── ui.py                # Cyberpunk UI components
├── configs/                 # YAML tool configurations
│   ├── 01_commands.yaml
│   ├── 02_ctf_kit.yaml
│   ├── 03_web_bounty.yaml
│   ├── 04_network_ad.yaml
│   ├── 05_mobile_iot.yaml
│   ├── 06_cloud_auditor.yaml
│   ├── 07_osint_detective.yaml
│   ├── 08_wireless_radio.yaml
│   └── 09_post_exploit.yaml
├── modules/                 # Python plugin modules
│   ├── recon/              # Reconnaissance tools
│   ├── web/                # Web application tools
│   ├── wireless/           # Wireless/radio tools
│   ├── sniffing/           # Network sniffing tools
│   ├── exploitation/       # Exploitation tools
│   ├── post_exploitation/  # Post-exploitation tools
│   ├── osint/              # OSINT tools
│   ├── mobile/             # Mobile/IoT tools
│   └── cloud/              # Cloud security tools
├── data/                    # Runtime data
│   ├── tajaa.db            # SQLite database
│   └── sessions/           # Session state files
├── logs/                    # Execution logs
└── utils/                   # Helper utilities
    └── helpers.py          # Common utility functions
```

## Core Components

### 1. Database Layer (`core/database.py`)

The `DatabaseManager` class provides async SQLite persistence:

```python
class DatabaseManager:
    """Async SQLite database for cross-tool data sharing."""
    
    # Tables:
    # - targets: Scan targets (IP, hostname, URL)
    # - scans: Tool executions with output
    # - findings: Discovered ports, services, vulnerabilities
    # - sessions: User session state
    # - attack_chains: Saved workflows
    # - command_history: Command audit log
```

**Key Features:**
- Async operations with `aiosqlite`
- Connection pooling with locks
- Foreign key constraints for data integrity
- Indexed queries for performance

### 2. Async Engine (`core/engine.py`)

The `AsyncEngine` handles command execution:

```python
class AsyncEngine:
    """Non-blocking command execution with streaming output."""
    
    async def execute(command, stream_output=True, timeout=None)
    async def execute_background(name, command, callback)
    async def execute_chain(commands, stop_on_failure=True)
    async def execute_parallel(commands, max_concurrent=3)
```

The `BackgroundTaskManager` enables concurrent operations:

```python
class BackgroundTaskManager:
    """Manages background tasks for parallel execution."""
    
    async def submit(name, command, callback) -> task_id
    async def cancel(task_id)
    def get_running_tasks() -> List[BackgroundTask]
```

### 3. Intelligence Module (`core/intelligence.py`)

#### FuzzySearchEngine
```python
class FuzzySearchEngine:
    """RapidFuzz-powered tool search."""
    
    def search(query, limit=10, threshold=60) -> List[ToolInfo]
    def search_by_tags(tags) -> List[ToolInfo]
```

#### ContextSuggestionEngine
```python
class ContextSuggestionEngine:
    """AI-like tool recommendations based on findings."""
    
    # Port → Tool mappings
    # Port 80 → nikto, dirb, gobuster, sqlmap
    # Port 445 → enum4linux, smbclient, crackmapexec
    # Port 22 → ssh-audit, hydra
    
    def suggest_from_ports(ports) -> List[Suggestion]
    def suggest_from_services(services) -> List[Suggestion]
    def suggest_next_phase(current_phase) -> List[Suggestion]
```

#### AttackChainOrchestrator
```python
class AttackChainOrchestrator:
    """Multi-step attack workflow automation."""
    
    # Built-in chains:
    # - Web Recon: nmap → whatweb → gobuster → nikto
    # - Network Enum: discovery → port scan → service detection
    # - SMB Enum: crackmapexec → enum4linux → smbmap
    # - SQLi Attack: discovery → detection → enumeration → dump
```

### 4. Plugin System (`core/plugin.py`)

```python
class PluginBase(ABC):
    """Base class for all plugins."""
    
    metadata: PluginMetadata
    command_template: str
    required_params: List[str]
    optional_params: Dict[str, str]
    
    def build_command() -> str
    def parse_output(output) -> Dict
    def get_suggestions(findings) -> List[str]
```

**Plugin Loading:**
- YAML plugins: Load from `configs/*.yaml`
- Python plugins: Load from `modules/{category}/*.py`
- Lazy loading for instant startup

### 5. Session Manager (`core/session.py`)

```python
class SessionManager:
    """Persistent session state with auto-save."""
    
    # Session State:
    # - Active target
    # - Command history
    # - Discovered ports/services cache
    # - Background tasks
    # - UI preferences
    
    async def create_session(name)
    async def load_session(name)
    async def resume_latest()
    def autosave()
```

### 6. UI System (`core/ui.py`)

```python
class TajaaUI:
    """Cyberpunk-themed user interface."""
    
    intro: CinematicIntro      # Matrix-style boot sequence
    dashboard: DashboardLayout  # Split-screen layout
    components: UIComponents    # Reusable UI elements
```

**Theme Colors:**
- Neon Cyan: `#00FFFF`
- Neon Magenta: `#FF00FF`
- Neon Green: `#00FF00`
- Neon Yellow: `#FFFF00`

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│  TajaaCLI   │────▶│ CommandMgr  │
│  Input      │     │ (main.py)   │     │  (Brain)    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
        ┌──────────────────────────────────────┼──────────────────┐
        │                                      │                  │
        ▼                                      ▼                  ▼
┌─────────────┐                       ┌─────────────┐    ┌─────────────┐
│FuzzySearch  │                       │AsyncEngine  │    │PluginReg   │
│  Engine     │                       │(Execution)  │    │ (Tools)    │
└─────────────┘                       └─────────────┘    └─────────────┘
        │                                      │                  │
        │                                      ▼                  │
        │                             ┌─────────────┐             │
        │                             │OutputParser │             │
        │                             │(Extraction) │             │
        │                             └─────────────┘             │
        │                                      │                  │
        ▼                                      ▼                  │
┌─────────────┐                       ┌─────────────┐             │
│Suggestion   │◀──────────────────────│ Database   │◀────────────┘
│  Engine     │                       │(Findings)  │
└─────────────┘                       └─────────────┘
        │
        ▼
┌─────────────┐
│   User      │
│(Suggestions)│
└─────────────┘
```

## Extension Points

### Adding a New Tool (YAML)

Add to any config file in `configs/`:

```yaml
categories:
  web_apps:
    tools:
      my_new_tool:
        name: "My Tool"
        description: "Tool description"
        command: "mytool -u {url} -o {output}"
        params: ["url"]
        defaults:
          output: "results.txt"
```

### Adding a Plugin (Python)

Create in `modules/{category}/`:

```python
from core.plugin import PluginBase, PluginMetadata, PluginCategory

class MyTool(PluginBase):
    metadata = PluginMetadata(
        name="My Tool",
        description="Description",
        category=PluginCategory.WEB,
        tags=['web', 'scanner']
    )
    
    @property
    def command_template(self) -> str:
        return "mytool -u {url}"
    
    @property
    def required_params(self) -> List[str]:
        return ['url']
    
    def parse_output(self, output: str) -> Dict:
        # Extract structured data
        return {'findings': [...]}
    
    def get_suggestions(self, findings: Dict) -> List[str]:
        # Suggest next tools
        return ['tool1', 'tool2']
```

### Adding an Attack Chain

Register in `core/intelligence.py`:

```python
orchestrator.register_chain(AttackChain(
    name="My Chain",
    description="Custom attack workflow",
    steps=[
        AttackChainStep(
            name="Step 1",
            tool="nmap",
            command_template="nmap {target}",
            required_params=['target']
        ),
        # ... more steps
    ]
))
```

## Performance Optimizations

1. **Lazy Loading**: Plugins loaded on-demand
2. **Async I/O**: Non-blocking database and subprocess operations
3. **Connection Pooling**: Single database connection with locks
4. **Index Optimization**: Database indexes on frequently queried columns
5. **Output Streaming**: Real-time output display without buffering
6. **Background Tasks**: Concurrent scan execution

## Security Considerations

1. **Input Validation**: All user inputs sanitized against injection
2. **Command Escaping**: `shlex.quote()` for shell arguments
3. **Path Validation**: No path traversal allowed
4. **Privilege Handling**: Graceful sudo requests
5. **Local Storage**: All data stored locally, no external connections

## Testing

Run the test suite:

```bash
python test_imports.py      # Test all imports
python test_components.py   # Test individual components
python test_security.py     # Security validation
```

## Author

**Tajaa** - Building tools that make the impossible feel inevitable.

