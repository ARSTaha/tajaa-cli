"""
Tajaa Database Layer
SQLite-based persistence for scan results, sessions, and cross-tool data sharing.
Author: Tajaa
"""

import asyncio
import aiosqlite
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum


class ScanStatus(Enum):
    """Scan execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FindingType(Enum):
    """Types of security findings."""
    PORT = "port"
    SERVICE = "service"
    VULNERABILITY = "vulnerability"
    CREDENTIAL = "credential"
    HOST = "host"
    DOMAIN = "domain"
    URL = "url"
    FILE = "file"
    SUBDOMAIN = "subdomain"
    TECHNOLOGY = "technology"
    CERTIFICATE = "certificate"
    DNS_RECORD = "dns_record"


@dataclass
class Target:
    """Represents a scan target."""
    id: Optional[int] = None
    value: str = ""
    target_type: str = "host"  # host, network, url, domain
    created_at: str = ""
    metadata: Dict = None


@dataclass
class Scan:
    """Represents a security scan."""
    id: Optional[int] = None
    target_id: int = 0
    tool_name: str = ""
    command: str = ""
    status: str = ScanStatus.PENDING.value
    started_at: str = ""
    completed_at: str = ""
    output: str = ""
    exit_code: int = 0
    metadata: Dict = None


@dataclass
class Finding:
    """Represents a security finding."""
    id: Optional[int] = None
    scan_id: int = 0
    target_id: int = 0
    finding_type: str = ""
    value: str = ""
    port: Optional[int] = None
    protocol: str = ""
    service: str = ""
    version: str = ""
    severity: str = "info"  # info, low, medium, high, critical
    confidence: float = 1.0
    raw_data: str = ""
    created_at: str = ""


@dataclass
class Session:
    """Represents a user session."""
    id: Optional[int] = None
    name: str = ""
    created_at: str = ""
    last_active: str = ""
    state: Dict = None
    active_target_id: Optional[int] = None


class DatabaseManager:
    """
    Async SQLite database manager for Tajaa.
    Handles all persistence operations with connection pooling.
    """

    def __init__(self, db_path: Union[str, Path] = "data/tajaa.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        """Establish database connection."""
        if self._connection is None:
            self._connection = await aiosqlite.connect(str(self.db_path))
            self._connection.row_factory = aiosqlite.Row
            await self._connection.execute("PRAGMA foreign_keys = ON")
            await self._connection.execute("PRAGMA journal_mode = WAL")
            await self._init_schema()

    async def close(self) -> None:
        """Close database connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def _init_schema(self) -> None:
        """Initialize database schema."""
        schema = """
        -- Targets table
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL UNIQUE,
            target_type TEXT DEFAULT 'host',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT DEFAULT '{}'
        );

        -- Scans table
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER NOT NULL,
            tool_name TEXT NOT NULL,
            command TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            started_at TEXT,
            completed_at TEXT,
            output TEXT DEFAULT '',
            exit_code INTEGER DEFAULT 0,
            metadata TEXT DEFAULT '{}',
            FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
        );

        -- Findings table
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            finding_type TEXT NOT NULL,
            value TEXT NOT NULL,
            port INTEGER,
            protocol TEXT DEFAULT '',
            service TEXT DEFAULT '',
            version TEXT DEFAULT '',
            severity TEXT DEFAULT 'info',
            confidence REAL DEFAULT 1.0,
            raw_data TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE,
            FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
        );

        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP,
            state TEXT DEFAULT '{}',
            active_target_id INTEGER,
            FOREIGN KEY (active_target_id) REFERENCES targets(id) ON DELETE SET NULL
        );

        -- Attack chains table
        CREATE TABLE IF NOT EXISTS attack_chains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            steps TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        -- Command history table
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            command TEXT NOT NULL,
            executed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_scans_target ON scans(target_id);
        CREATE INDEX IF NOT EXISTS idx_scans_status ON scans(status);
        CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
        CREATE INDEX IF NOT EXISTS idx_findings_target ON findings(target_id);
        CREATE INDEX IF NOT EXISTS idx_findings_type ON findings(finding_type);
        CREATE INDEX IF NOT EXISTS idx_findings_port ON findings(port);
        """
        await self._connection.executescript(schema)
        await self._connection.commit()

    # =========================================================================
    # TARGET OPERATIONS
    # =========================================================================

    async def add_target(self, value: str, target_type: str = "host",
                         metadata: Dict = None) -> int:
        """Add a new target."""
        async with self._lock:
            try:
                cursor = await self._connection.execute(
                    """INSERT INTO targets (value, target_type, metadata)
                       VALUES (?, ?, ?)
                       ON CONFLICT(value) DO UPDATE SET target_type = excluded.target_type
                       RETURNING id""",
                    (value, target_type, json.dumps(metadata or {}))
                )
                row = await cursor.fetchone()
                await self._connection.commit()
                return row[0]
            except Exception:
                cursor = await self._connection.execute(
                    "SELECT id FROM targets WHERE value = ?", (value,)
                )
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def get_target(self, target_id: int) -> Optional[Target]:
        """Get target by ID."""
        cursor = await self._connection.execute(
            "SELECT * FROM targets WHERE id = ?", (target_id,)
        )
        row = await cursor.fetchone()
        if row:
            return Target(
                id=row['id'],
                value=row['value'],
                target_type=row['target_type'],
                created_at=row['created_at'],
                metadata=json.loads(row['metadata'])
            )
        return None

    async def get_target_by_value(self, value: str) -> Optional[Target]:
        """Get target by value."""
        cursor = await self._connection.execute(
            "SELECT * FROM targets WHERE value = ?", (value,)
        )
        row = await cursor.fetchone()
        if row:
            return Target(
                id=row['id'],
                value=row['value'],
                target_type=row['target_type'],
                created_at=row['created_at'],
                metadata=json.loads(row['metadata'])
            )
        return None

    async def get_all_targets(self, limit: int = 100) -> List[Target]:
        """Get all targets."""
        cursor = await self._connection.execute(
            "SELECT * FROM targets ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [Target(
            id=row['id'],
            value=row['value'],
            target_type=row['target_type'],
            created_at=row['created_at'],
            metadata=json.loads(row['metadata'])
        ) for row in rows]

    # =========================================================================
    # SCAN OPERATIONS
    # =========================================================================

    async def create_scan(self, target_id: int, tool_name: str, command: str,
                          metadata: Dict = None) -> int:
        """Create a new scan record."""
        async with self._lock:
            cursor = await self._connection.execute(
                """INSERT INTO scans (target_id, tool_name, command, status, started_at, metadata)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (target_id, tool_name, command, ScanStatus.RUNNING.value,
                 datetime.now().isoformat(), json.dumps(metadata or {}))
            )
            await self._connection.commit()
            return cursor.lastrowid

    async def update_scan(self, scan_id: int, status: ScanStatus = None,
                          output: str = None, exit_code: int = None) -> None:
        """Update scan record."""
        async with self._lock:
            updates = []
            values = []

            if status:
                updates.append("status = ?")
                values.append(status.value)
                if status in (ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED):
                    updates.append("completed_at = ?")
                    values.append(datetime.now().isoformat())

            if output is not None:
                updates.append("output = ?")
                values.append(output)

            if exit_code is not None:
                updates.append("exit_code = ?")
                values.append(exit_code)

            if updates:
                values.append(scan_id)
                await self._connection.execute(
                    f"UPDATE scans SET {', '.join(updates)} WHERE id = ?",
                    tuple(values)
                )
                await self._connection.commit()

    async def get_scan(self, scan_id: int) -> Optional[Scan]:
        """Get scan by ID."""
        cursor = await self._connection.execute(
            "SELECT * FROM scans WHERE id = ?", (scan_id,)
        )
        row = await cursor.fetchone()
        if row:
            return Scan(
                id=row['id'],
                target_id=row['target_id'],
                tool_name=row['tool_name'],
                command=row['command'],
                status=row['status'],
                started_at=row['started_at'],
                completed_at=row['completed_at'],
                output=row['output'],
                exit_code=row['exit_code'],
                metadata=json.loads(row['metadata'])
            )
        return None

    async def get_scans_for_target(self, target_id: int, limit: int = 50) -> List[Scan]:
        """Get all scans for a target."""
        cursor = await self._connection.execute(
            """SELECT * FROM scans WHERE target_id = ?
               ORDER BY started_at DESC LIMIT ?""",
            (target_id, limit)
        )
        rows = await cursor.fetchall()
        return [Scan(
            id=row['id'],
            target_id=row['target_id'],
            tool_name=row['tool_name'],
            command=row['command'],
            status=row['status'],
            started_at=row['started_at'],
            completed_at=row['completed_at'],
            output=row['output'],
            exit_code=row['exit_code'],
            metadata=json.loads(row['metadata'])
        ) for row in rows]

    async def get_running_scans(self) -> List[Scan]:
        """Get all currently running scans."""
        cursor = await self._connection.execute(
            "SELECT * FROM scans WHERE status = ?",
            (ScanStatus.RUNNING.value,)
        )
        rows = await cursor.fetchall()
        return [Scan(
            id=row['id'],
            target_id=row['target_id'],
            tool_name=row['tool_name'],
            command=row['command'],
            status=row['status'],
            started_at=row['started_at'],
            completed_at=row['completed_at'],
            output=row['output'],
            exit_code=row['exit_code'],
            metadata=json.loads(row['metadata'])
        ) for row in rows]

    # =========================================================================
    # FINDING OPERATIONS
    # =========================================================================

    async def add_finding(self, scan_id: int, target_id: int, finding_type: FindingType,
                          value: str, port: int = None, protocol: str = "",
                          service: str = "", version: str = "", severity: str = "info",
                          confidence: float = 1.0, raw_data: str = "") -> int:
        """Add a security finding."""
        async with self._lock:
            cursor = await self._connection.execute(
                """INSERT INTO findings
                   (scan_id, target_id, finding_type, value, port, protocol,
                    service, version, severity, confidence, raw_data)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (scan_id, target_id, finding_type.value, value, port, protocol,
                 service, version, severity, confidence, raw_data)
            )
            await self._connection.commit()
            return cursor.lastrowid

    async def add_findings_bulk(self, findings: List[Finding]) -> None:
        """Add multiple findings efficiently."""
        async with self._lock:
            await self._connection.executemany(
                """INSERT INTO findings
                   (scan_id, target_id, finding_type, value, port, protocol,
                    service, version, severity, confidence, raw_data)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [(f.scan_id, f.target_id, f.finding_type, f.value, f.port,
                  f.protocol, f.service, f.version, f.severity, f.confidence,
                  f.raw_data) for f in findings]
            )
            await self._connection.commit()

    async def get_findings_for_target(self, target_id: int,
                                       finding_type: FindingType = None) -> List[Finding]:
        """Get all findings for a target."""
        if finding_type:
            cursor = await self._connection.execute(
                """SELECT * FROM findings WHERE target_id = ? AND finding_type = ?
                   ORDER BY created_at DESC""",
                (target_id, finding_type.value)
            )
        else:
            cursor = await self._connection.execute(
                """SELECT * FROM findings WHERE target_id = ?
                   ORDER BY created_at DESC""",
                (target_id,)
            )

        rows = await cursor.fetchall()
        return [Finding(
            id=row['id'],
            scan_id=row['scan_id'],
            target_id=row['target_id'],
            finding_type=row['finding_type'],
            value=row['value'],
            port=row['port'],
            protocol=row['protocol'],
            service=row['service'],
            version=row['version'],
            severity=row['severity'],
            confidence=row['confidence'],
            raw_data=row['raw_data'],
            created_at=row['created_at']
        ) for row in rows]

    async def get_open_ports(self, target_id: int) -> List[int]:
        """Get all open ports for a target."""
        cursor = await self._connection.execute(
            """SELECT DISTINCT port FROM findings
               WHERE target_id = ? AND finding_type = 'port' AND port IS NOT NULL
               ORDER BY port""",
            (target_id,)
        )
        rows = await cursor.fetchall()
        return [row['port'] for row in rows]

    async def get_services(self, target_id: int) -> List[Dict]:
        """Get all discovered services for a target."""
        cursor = await self._connection.execute(
            """SELECT DISTINCT port, protocol, service, version FROM findings
               WHERE target_id = ? AND finding_type = 'service'
               ORDER BY port""",
            (target_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    # =========================================================================
    # SESSION OPERATIONS
    # =========================================================================

    async def create_session(self, name: str, state: Dict = None) -> int:
        """Create a new session."""
        async with self._lock:
            cursor = await self._connection.execute(
                """INSERT INTO sessions (name, state)
                   VALUES (?, ?)
                   ON CONFLICT(name) DO UPDATE SET last_active = CURRENT_TIMESTAMP
                   RETURNING id""",
                (name, json.dumps(state or {}))
            )
            row = await cursor.fetchone()
            await self._connection.commit()
            return row[0]

    async def get_session(self, session_id: int) -> Optional[Session]:
        """Get session by ID."""
        cursor = await self._connection.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        )
        row = await cursor.fetchone()
        if row:
            return Session(
                id=row['id'],
                name=row['name'],
                created_at=row['created_at'],
                last_active=row['last_active'],
                state=json.loads(row['state']),
                active_target_id=row['active_target_id']
            )
        return None

    async def get_session_by_name(self, name: str) -> Optional[Session]:
        """Get session by name."""
        cursor = await self._connection.execute(
            "SELECT * FROM sessions WHERE name = ?", (name,)
        )
        row = await cursor.fetchone()
        if row:
            return Session(
                id=row['id'],
                name=row['name'],
                created_at=row['created_at'],
                last_active=row['last_active'],
                state=json.loads(row['state']),
                active_target_id=row['active_target_id']
            )
        return None

    async def update_session(self, session_id: int, state: Dict = None,
                              active_target_id: int = None) -> None:
        """Update session state."""
        async with self._lock:
            updates = ["last_active = CURRENT_TIMESTAMP"]
            values = []

            if state is not None:
                updates.append("state = ?")
                values.append(json.dumps(state))

            if active_target_id is not None:
                updates.append("active_target_id = ?")
                values.append(active_target_id)

            values.append(session_id)
            await self._connection.execute(
                f"UPDATE sessions SET {', '.join(updates)} WHERE id = ?",
                tuple(values)
            )
            await self._connection.commit()

    async def get_recent_sessions(self, limit: int = 10) -> List[Session]:
        """Get recent sessions."""
        cursor = await self._connection.execute(
            "SELECT * FROM sessions ORDER BY last_active DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [Session(
            id=row['id'],
            name=row['name'],
            created_at=row['created_at'],
            last_active=row['last_active'],
            state=json.loads(row['state']),
            active_target_id=row['active_target_id']
        ) for row in rows]

    # =========================================================================
    # COMMAND HISTORY
    # =========================================================================

    async def add_command_history(self, session_id: int, command: str) -> None:
        """Add command to history."""
        async with self._lock:
            await self._connection.execute(
                "INSERT INTO command_history (session_id, command) VALUES (?, ?)",
                (session_id, command)
            )
            await self._connection.commit()

    async def get_command_history(self, session_id: int, limit: int = 100) -> List[str]:
        """Get command history for session."""
        cursor = await self._connection.execute(
            """SELECT command FROM command_history
               WHERE session_id = ?
               ORDER BY executed_at DESC LIMIT ?""",
            (session_id, limit)
        )
        rows = await cursor.fetchall()
        return [row['command'] for row in rows]

    # =========================================================================
    # ATTACK CHAINS
    # =========================================================================

    async def save_attack_chain(self, name: str, description: str,
                                 steps: List[Dict]) -> int:
        """Save an attack chain."""
        async with self._lock:
            cursor = await self._connection.execute(
                """INSERT INTO attack_chains (name, description, steps)
                   VALUES (?, ?, ?)""",
                (name, description, json.dumps(steps))
            )
            await self._connection.commit()
            return cursor.lastrowid

    async def get_attack_chains(self) -> List[Dict]:
        """Get all attack chains."""
        cursor = await self._connection.execute(
            "SELECT * FROM attack_chains ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [{
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'steps': json.loads(row['steps']),
            'created_at': row['created_at']
        } for row in rows]

    # =========================================================================
    # ANALYTICS & REPORTING
    # =========================================================================

    async def get_target_summary(self, target_id: int) -> Dict:
        """Get comprehensive summary for a target."""
        target = await self.get_target(target_id)
        if not target:
            return {}

        ports = await self.get_open_ports(target_id)
        services = await self.get_services(target_id)
        findings = await self.get_findings_for_target(target_id)

        # Count findings by severity
        severity_counts = {}
        for f in findings:
            severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

        # Count findings by type
        type_counts = {}
        for f in findings:
            type_counts[f.finding_type] = type_counts.get(f.finding_type, 0) + 1

        scans = await self.get_scans_for_target(target_id)

        return {
            'target': asdict(target),
            'open_ports': ports,
            'services': services,
            'total_findings': len(findings),
            'severity_breakdown': severity_counts,
            'type_breakdown': type_counts,
            'total_scans': len(scans),
            'completed_scans': len([s for s in scans if s.status == 'completed']),
        }

