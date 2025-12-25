"""
Tajaa Session Manager
Handles session persistence, state management, and graceful recovery.
Author: Tajaa
"""

import os
import json
import pickle
import atexit
import signal
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from rich.console import Console


@dataclass
class SessionState:
    """Complete session state."""
    id: int = 0
    name: str = ""
    created_at: str = ""
    last_active: str = ""

    # Active context
    active_target: str = ""
    active_target_id: int = 0
    current_category: str = ""
    current_tool: str = ""

    # History
    command_history: List[str] = field(default_factory=list)
    tool_history: List[str] = field(default_factory=list)
    target_history: List[str] = field(default_factory=list)

    # Findings cache
    discovered_ports: Dict[str, List[int]] = field(default_factory=dict)
    discovered_services: Dict[str, List[Dict]] = field(default_factory=dict)

    # UI state
    last_view: str = "categories"
    scroll_position: int = 0
    expanded_categories: List[str] = field(default_factory=list)

    # Background tasks
    running_tasks: List[str] = field(default_factory=list)

    # User preferences
    preferences: Dict[str, Any] = field(default_factory=dict)


class SessionManager:
    """
    Manages user sessions with automatic state persistence.
    Handles graceful shutdown and crash recovery.
    """

    def __init__(self, session_dir: Path = None, db_manager=None):
        self.session_dir = session_dir or Path("data/sessions")
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.db = db_manager
        self.console = Console()

        self._current_session: Optional[SessionState] = None
        self._session_file: Optional[Path] = None
        self._autosave_enabled = True

        # Register cleanup handlers
        atexit.register(self._cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, self._signal_handler)

    @property
    def current(self) -> Optional[SessionState]:
        """Get current session state."""
        return self._current_session

    def _generate_session_name(self) -> str:
        """Generate unique session name."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:6]
        return f"session_{timestamp}_{random_suffix}"

    async def create_session(self, name: str = None) -> SessionState:
        """Create a new session."""
        session_name = name or self._generate_session_name()
        now = datetime.now().isoformat()

        self._current_session = SessionState(
            name=session_name,
            created_at=now,
            last_active=now,
        )

        # Create session file
        self._session_file = self.session_dir / f"{session_name}.json"

        # Save to database if available
        if self.db:
            try:
                session_id = await self.db.create_session(
                    session_name,
                    asdict(self._current_session)
                )
                self._current_session.id = session_id
            except Exception:
                pass

        self._save_session()
        return self._current_session

    async def load_session(self, name: str) -> Optional[SessionState]:
        """Load an existing session."""
        session_file = self.session_dir / f"{name}.json"

        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._current_session = SessionState(**data)
            self._session_file = session_file
            self._current_session.last_active = datetime.now().isoformat()

            # Update database
            if self.db and self._current_session.id:
                await self.db.update_session(
                    self._current_session.id,
                    state=asdict(self._current_session)
                )

            return self._current_session

        except Exception as e:
            self.console.print(f"[yellow]Warning:[/yellow] Failed to load session: {e}")
            return None

    async def resume_latest(self) -> Optional[SessionState]:
        """Resume the most recent session."""
        sessions = self.list_sessions()
        if not sessions:
            return await self.create_session()

        # Find most recent
        latest = max(sessions, key=lambda s: s.get('last_active', ''))
        return await self.load_session(latest['name'])

    def list_sessions(self) -> List[Dict]:
        """List all available sessions."""
        sessions = []

        for session_file in self.session_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        'name': data.get('name', session_file.stem),
                        'created_at': data.get('created_at', ''),
                        'last_active': data.get('last_active', ''),
                        'target': data.get('active_target', ''),
                    })
            except Exception:
                continue

        return sorted(sessions, key=lambda s: s.get('last_active', ''), reverse=True)

    def _save_session(self) -> None:
        """Save current session to disk."""
        if not self._current_session or not self._session_file:
            return

        try:
            self._current_session.last_active = datetime.now().isoformat()

            with open(self._session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._current_session), f, indent=2, default=str)

        except Exception as e:
            self.console.print(f"[yellow]Warning:[/yellow] Failed to save session: {e}")

    def autosave(self) -> None:
        """Trigger autosave if enabled."""
        if self._autosave_enabled:
            self._save_session()

    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================

    def set_active_target(self, target: str, target_id: int = 0) -> None:
        """Set the active target."""
        if self._current_session:
            self._current_session.active_target = target
            self._current_session.active_target_id = target_id
            if target not in self._current_session.target_history:
                self._current_session.target_history.append(target)
            self.autosave()

    def add_command(self, command: str) -> None:
        """Add command to history."""
        if self._current_session:
            self._current_session.command_history.append(command)
            # Keep only last 500 commands
            self._current_session.command_history = self._current_session.command_history[-500:]
            self.autosave()

    def add_tool_usage(self, tool_name: str) -> None:
        """Track tool usage."""
        if self._current_session:
            self._current_session.tool_history.append(tool_name)
            self._current_session.tool_history = self._current_session.tool_history[-100:]
            self.autosave()

    def cache_ports(self, target: str, ports: List[int]) -> None:
        """Cache discovered ports for a target."""
        if self._current_session:
            existing = self._current_session.discovered_ports.get(target, [])
            combined = list(set(existing + ports))
            self._current_session.discovered_ports[target] = sorted(combined)
            self.autosave()

    def cache_services(self, target: str, services: List[Dict]) -> None:
        """Cache discovered services for a target."""
        if self._current_session:
            existing = self._current_session.discovered_services.get(target, [])
            # Deduplicate by port
            existing_ports = {s.get('port') for s in existing}
            for svc in services:
                if svc.get('port') not in existing_ports:
                    existing.append(svc)
            self._current_session.discovered_services[target] = existing
            self.autosave()

    def get_cached_ports(self, target: str = None) -> List[int]:
        """Get cached ports for target or current target."""
        if not self._current_session:
            return []
        target = target or self._current_session.active_target
        return self._current_session.discovered_ports.get(target, [])

    def get_cached_services(self, target: str = None) -> List[Dict]:
        """Get cached services for target or current target."""
        if not self._current_session:
            return []
        target = target or self._current_session.active_target
        return self._current_session.discovered_services.get(target, [])

    def set_preference(self, key: str, value: Any) -> None:
        """Set a user preference."""
        if self._current_session:
            self._current_session.preferences[key] = value
            self.autosave()

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        if self._current_session:
            return self._current_session.preferences.get(key, default)
        return default

    def set_ui_state(self, view: str = None, scroll: int = None) -> None:
        """Update UI state."""
        if self._current_session:
            if view:
                self._current_session.last_view = view
            if scroll is not None:
                self._current_session.scroll_position = scroll
            self.autosave()

    def add_running_task(self, task_id: str) -> None:
        """Track a running background task."""
        if self._current_session:
            if task_id not in self._current_session.running_tasks:
                self._current_session.running_tasks.append(task_id)
            self.autosave()

    def remove_running_task(self, task_id: str) -> None:
        """Remove a completed background task."""
        if self._current_session:
            if task_id in self._current_session.running_tasks:
                self._current_session.running_tasks.remove(task_id)
            self.autosave()

    # =========================================================================
    # SESSION LIFECYCLE
    # =========================================================================

    async def close_session(self) -> None:
        """Close and save the current session."""
        if self._current_session:
            self._save_session()

            # Update database
            if self.db and self._current_session.id:
                try:
                    await self.db.update_session(
                        self._current_session.id,
                        state=asdict(self._current_session)
                    )
                except Exception:
                    pass

            self._current_session = None
            self._session_file = None

    def delete_session(self, name: str) -> bool:
        """Delete a session."""
        session_file = self.session_dir / f"{name}.json"
        if session_file.exists():
            session_file.unlink()
            return True
        return False

    def export_session(self, output_path: Path) -> bool:
        """Export current session to file."""
        if not self._current_session:
            return False

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._current_session), f, indent=2, default=str)
            return True
        except Exception:
            return False

    def import_session(self, input_path: Path) -> Optional[SessionState]:
        """Import a session from file."""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Generate new name to avoid conflicts
            data['name'] = self._generate_session_name()
            data['last_active'] = datetime.now().isoformat()

            self._current_session = SessionState(**data)
            self._session_file = self.session_dir / f"{self._current_session.name}.json"
            self._save_session()

            return self._current_session
        except Exception:
            return None

    # =========================================================================
    # CLEANUP
    # =========================================================================

    def _cleanup(self) -> None:
        """Cleanup handler called on exit."""
        if self._current_session:
            self._save_session()

    def _signal_handler(self, signum, frame) -> None:
        """Handle signals gracefully."""
        self._cleanup()
        # Re-raise the signal after cleanup
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)


class WorkspaceManager:
    """
    Manages workspaces for organizing targets and findings.
    A workspace groups related targets, scans, and notes.
    """

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = workspace_dir or Path("data/workspaces")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self._current_workspace: Optional[str] = None

    def create_workspace(self, name: str, description: str = "") -> Path:
        """Create a new workspace."""
        workspace_path = self.workspace_dir / name
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Create workspace metadata
        metadata = {
            'name': name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'targets': [],
            'notes': '',
        }

        with open(workspace_path / 'workspace.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        # Create subdirectories
        (workspace_path / 'scans').mkdir(exist_ok=True)
        (workspace_path / 'notes').mkdir(exist_ok=True)
        (workspace_path / 'loot').mkdir(exist_ok=True)
        (workspace_path / 'reports').mkdir(exist_ok=True)

        return workspace_path

    def list_workspaces(self) -> List[Dict]:
        """List all workspaces."""
        workspaces = []

        for ws_dir in self.workspace_dir.iterdir():
            if ws_dir.is_dir():
                metadata_file = ws_dir / 'workspace.json'
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            metadata['path'] = str(ws_dir)
                            workspaces.append(metadata)
                    except Exception:
                        workspaces.append({
                            'name': ws_dir.name,
                            'path': str(ws_dir)
                        })

        return workspaces

    def set_current_workspace(self, name: str) -> bool:
        """Set the current workspace."""
        workspace_path = self.workspace_dir / name
        if workspace_path.exists():
            self._current_workspace = name
            return True
        return False

    def get_current_workspace(self) -> Optional[str]:
        """Get the current workspace name."""
        return self._current_workspace

    def add_target_to_workspace(self, workspace: str, target: str) -> None:
        """Add a target to a workspace."""
        workspace_path = self.workspace_dir / workspace
        metadata_file = workspace_path / 'workspace.json'

        if not metadata_file.exists():
            return

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        if target not in metadata.get('targets', []):
            metadata.setdefault('targets', []).append(target)

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

    def save_scan_output(self, workspace: str, target: str, tool: str,
                         output: str) -> Path:
        """Save scan output to workspace."""
        workspace_path = self.workspace_dir / workspace / 'scans'
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Create target directory
        target_dir = workspace_path / target.replace('/', '_').replace(':', '_')
        target_dir.mkdir(exist_ok=True)

        # Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = target_dir / f"{tool}_{timestamp}.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Tool: {tool}\n")
            f.write(f"# Target: {target}\n")
            f.write(f"# Timestamp: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            f.write(output)

        return output_file

