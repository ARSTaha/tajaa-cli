"""
Tajaa Async Engine
High-performance asynchronous command execution engine.
Author: Tajaa
"""

import asyncio
import shlex
import sys
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any, Coroutine
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn


class TaskStatus(Enum):
    """Background task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BackgroundTask:
    """Represents a background task."""
    id: str
    name: str
    command: str
    status: TaskStatus = TaskStatus.PENDING
    process: Optional[asyncio.subprocess.Process] = None
    output_buffer: deque = field(default_factory=lambda: deque(maxlen=1000))
    error_buffer: deque = field(default_factory=lambda: deque(maxlen=500))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    exit_code: Optional[int] = None
    callback: Optional[Callable] = None


class BackgroundTaskManager:
    """
    Manages background tasks for concurrent execution.
    Allows running multiple scans simultaneously without blocking the UI.
    """

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.tasks: Dict[str, BackgroundTask] = {}
        self._task_counter = 0
        self._lock = asyncio.Lock()
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self.console = Console()

    def _generate_task_id(self) -> str:
        """Generate unique task ID."""
        self._task_counter += 1
        return f"task_{self._task_counter:04d}"

    async def submit(self, name: str, command: str,
                     callback: Callable = None) -> str:
        """Submit a new background task."""
        async with self._lock:
            task_id = self._generate_task_id()
            task = BackgroundTask(
                id=task_id,
                name=name,
                command=command,
                callback=callback
            )
            self.tasks[task_id] = task

            # Check if we can run immediately
            running_count = sum(1 for t in self.tasks.values()
                               if t.status == TaskStatus.RUNNING)

            if running_count < self.max_concurrent:
                asyncio_task = asyncio.create_task(self._execute_task(task_id))
                self._running_tasks[task_id] = asyncio_task

            return task_id

    async def _execute_task(self, task_id: str) -> None:
        """Execute a background task."""
        task = self.tasks.get(task_id)
        if not task:
            return

        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

        try:
            # Parse command
            if sys.platform == 'win32':
                process = await asyncio.create_subprocess_shell(
                    task.command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            else:
                args = shlex.split(task.command)
                process = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

            task.process = process

            # Stream output
            async def read_stream(stream, buffer):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded = line.decode('utf-8', errors='replace').rstrip()
                    buffer.append(decoded)

            await asyncio.gather(
                read_stream(process.stdout, task.output_buffer),
                read_stream(process.stderr, task.error_buffer),
            )

            await process.wait()
            task.exit_code = process.returncode
            task.status = TaskStatus.COMPLETED if task.exit_code == 0 else TaskStatus.FAILED
            task.completed_at = datetime.now()

            # Execute callback if provided
            if task.callback:
                if asyncio.iscoroutinefunction(task.callback):
                    await task.callback(task)
                else:
                    task.callback(task)

        except asyncio.CancelledError:
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            if task.process:
                task.process.terminate()
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error_buffer.append(str(e))

        # Start next pending task
        await self._start_next_pending()

    async def _start_next_pending(self) -> None:
        """Start the next pending task if capacity allows."""
        async with self._lock:
            running_count = sum(1 for t in self.tasks.values()
                               if t.status == TaskStatus.RUNNING)

            if running_count < self.max_concurrent:
                for task_id, task in self.tasks.items():
                    if task.status == TaskStatus.PENDING:
                        asyncio_task = asyncio.create_task(self._execute_task(task_id))
                        self._running_tasks[task_id] = asyncio_task
                        break

    async def cancel(self, task_id: str) -> bool:
        """Cancel a running task."""
        task = self.tasks.get(task_id)
        if not task:
            return False

        if task.status == TaskStatus.RUNNING:
            if task_id in self._running_tasks:
                self._running_tasks[task_id].cancel()
            if task.process:
                task.process.terminate()
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            return True
        elif task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True

        return False

    async def cancel_all(self) -> None:
        """Cancel all running and pending tasks."""
        for task_id in list(self.tasks.keys()):
            await self.cancel(task_id)

    def get_task(self, task_id: str) -> Optional[BackgroundTask]:
        """Get task by ID."""
        return self.tasks.get(task_id)

    def get_running_tasks(self) -> List[BackgroundTask]:
        """Get all running tasks."""
        return [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]

    def get_task_output(self, task_id: str) -> str:
        """Get full output for a task."""
        task = self.tasks.get(task_id)
        if task:
            return '\n'.join(task.output_buffer)
        return ""

    def get_task_status_table(self) -> Table:
        """Generate a rich table of task statuses."""
        table = Table(title="Background Tasks", box=None)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Status", style="bold")
        table.add_column("Duration", style="dim")

        status_colors = {
            TaskStatus.PENDING: "yellow",
            TaskStatus.RUNNING: "blue",
            TaskStatus.COMPLETED: "green",
            TaskStatus.FAILED: "red",
            TaskStatus.CANCELLED: "dim",
        }

        for task in self.tasks.values():
            duration = ""
            if task.started_at:
                end = task.completed_at or datetime.now()
                delta = end - task.started_at
                duration = f"{delta.total_seconds():.1f}s"

            status_style = status_colors.get(task.status, "white")
            table.add_row(
                task.id,
                task.name[:30],
                f"[{status_style}]{task.status.value}[/{status_style}]",
                duration
            )

        return table


class AsyncEngine:
    """
    Core async execution engine for Tajaa.
    Handles command execution, output streaming, and process management.
    """

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.task_manager = BackgroundTaskManager()
        self._output_callbacks: List[Callable] = []

    def add_output_callback(self, callback: Callable[[str], None]) -> None:
        """Add callback for real-time output streaming."""
        self._output_callbacks.append(callback)

    def remove_output_callback(self, callback: Callable) -> None:
        """Remove output callback."""
        if callback in self._output_callbacks:
            self._output_callbacks.remove(callback)

    async def execute(self, command: str, stream_output: bool = True,
                      timeout: int = None) -> Dict[str, Any]:
        """
        Execute a command asynchronously.

        Args:
            command: The command to execute
            stream_output: Whether to stream output in real-time
            timeout: Optional timeout in seconds

        Returns:
            Dict with 'output', 'errors', 'exit_code', 'success'
        """
        result = {
            'output': '',
            'errors': '',
            'exit_code': -1,
            'success': False,
            'timed_out': False,
        }

        try:
            # Create process
            if sys.platform == 'win32':
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            else:
                args = shlex.split(command)
                process = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

            output_lines = []
            error_lines = []

            async def stream_stdout():
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    decoded = line.decode('utf-8', errors='replace').rstrip()
                    output_lines.append(decoded)
                    if stream_output:
                        self.console.print(f"  [dim]│[/dim] {decoded}")
                        for callback in self._output_callbacks:
                            callback(decoded)

            async def stream_stderr():
                while True:
                    line = await process.stderr.readline()
                    if not line:
                        break
                    decoded = line.decode('utf-8', errors='replace').rstrip()
                    error_lines.append(decoded)
                    if stream_output:
                        self.console.print(f"  [dim]│[/dim] [yellow]{decoded}[/yellow]")

            try:
                if timeout:
                    await asyncio.wait_for(
                        asyncio.gather(stream_stdout(), stream_stderr(), process.wait()),
                        timeout=timeout
                    )
                else:
                    await asyncio.gather(stream_stdout(), stream_stderr())
                    await process.wait()

            except asyncio.TimeoutError:
                process.terminate()
                await process.wait()
                result['timed_out'] = True

            result['output'] = '\n'.join(output_lines)
            result['errors'] = '\n'.join(error_lines)
            result['exit_code'] = process.returncode
            result['success'] = process.returncode == 0

        except FileNotFoundError:
            result['errors'] = f"Command not found: {command.split()[0]}"
        except Exception as e:
            result['errors'] = str(e)

        return result

    async def execute_background(self, name: str, command: str,
                                  callback: Callable = None) -> str:
        """Execute command in background, returns task ID."""
        return await self.task_manager.submit(name, command, callback)

    async def execute_chain(self, commands: List[Dict[str, str]],
                            stop_on_failure: bool = True) -> List[Dict[str, Any]]:
        """
        Execute a chain of commands sequentially.

        Args:
            commands: List of {'name': str, 'command': str}
            stop_on_failure: Stop execution if a command fails

        Returns:
            List of execution results
        """
        results = []

        for cmd in commands:
            self.console.print(f"\n  [cyan]▶[/cyan] {cmd.get('name', 'Command')}")
            result = await self.execute(cmd['command'])
            result['name'] = cmd.get('name', '')
            results.append(result)

            if stop_on_failure and not result['success']:
                self.console.print(f"  [red]✗[/red] Chain stopped due to failure")
                break

        return results

    async def execute_parallel(self, commands: List[Dict[str, str]],
                                max_concurrent: int = 3) -> List[Dict[str, Any]]:
        """
        Execute multiple commands in parallel.

        Args:
            commands: List of {'name': str, 'command': str}
            max_concurrent: Maximum concurrent executions

        Returns:
            List of execution results
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        results = []

        async def execute_with_semaphore(cmd: Dict) -> Dict:
            async with semaphore:
                result = await self.execute(cmd['command'], stream_output=False)
                result['name'] = cmd.get('name', '')
                return result

        tasks = [execute_with_semaphore(cmd) for cmd in commands]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [r if isinstance(r, dict) else {'errors': str(r), 'success': False}
                for r in results]

    def get_background_tasks(self) -> List[BackgroundTask]:
        """Get all background tasks."""
        return list(self.task_manager.tasks.values())

    async def cancel_background_task(self, task_id: str) -> bool:
        """Cancel a background task."""
        return await self.task_manager.cancel(task_id)

    async def wait_for_task(self, task_id: str, timeout: int = None) -> Optional[BackgroundTask]:
        """Wait for a background task to complete."""
        start = datetime.now()
        while True:
            task = self.task_manager.get_task(task_id)
            if not task:
                return None

            if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
                return task

            if timeout:
                elapsed = (datetime.now() - start).total_seconds()
                if elapsed >= timeout:
                    return task

            await asyncio.sleep(0.1)


class OutputParser:
    """
    Parses command output to extract structured data.
    Used for cross-tool data sharing.
    """

    @staticmethod
    def parse_nmap_output(output: str) -> Dict[str, Any]:
        """Parse Nmap output to extract ports and services."""
        import re

        result = {
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
            result['ports'].append(port_info)
            result['services'].append(port_info)

        # Extract hosts
        host_pattern = r'Nmap scan report for (\S+)'
        for match in re.finditer(host_pattern, output):
            result['hosts'].append(match.group(1))

        return result

    @staticmethod
    def parse_nikto_output(output: str) -> Dict[str, Any]:
        """Parse Nikto output to extract vulnerabilities."""
        import re

        result = {
            'vulnerabilities': [],
            'info': [],
        }

        vuln_pattern = r'\+ (OSVDB-\d+|[A-Z]{3,}:.*?): (.+)'
        for match in re.finditer(vuln_pattern, output):
            result['vulnerabilities'].append({
                'id': match.group(1),
                'description': match.group(2)
            })

        return result

    @staticmethod
    def parse_gobuster_output(output: str) -> Dict[str, Any]:
        """Parse Gobuster output to extract directories."""
        import re

        result = {
            'directories': [],
            'files': [],
        }

        dir_pattern = r'/(\S+)\s+\(Status: (\d+)\)'
        for match in re.finditer(dir_pattern, output):
            entry = {
                'path': match.group(1),
                'status': int(match.group(2))
            }
            if '.' in entry['path']:
                result['files'].append(entry)
            else:
                result['directories'].append(entry)

        return result

