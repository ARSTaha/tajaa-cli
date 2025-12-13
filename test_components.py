#!/usr/bin/env python3
"""
Unit tests for Tajaa CLI components
Author: Tajaa
"""

import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from io import StringIO

from main import (
    ConfigLoader,
    InputValidator,
    SessionLogger,
    ToolConfig,
    CategoryConfig
)
from rich.console import Console


class TestConfigLoader(unittest.TestCase):
    """Test cases for ConfigLoader class"""

    def setUp(self):
        """Create a temporary YAML config for testing"""
        self.temp_yaml = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.temp_yaml.write("""
categories:
  recon:
    name: "Reconnaissance"
    tools:
      test_tool:
        name: "Test Tool"
        description: "A test tool"
        command: "echo {target}"
        params:
          - target
""")
        self.temp_yaml.close()
        self.config_path = Path(self.temp_yaml.name)

    def tearDown(self):
        """Clean up temporary file"""
        if self.config_path.exists():
            self.config_path.unlink()

    def test_load_valid_config(self):
        """Test loading a valid configuration file"""
        loader = ConfigLoader(self.config_path)
        categories = loader.load()

        self.assertIn('recon', categories)
        self.assertEqual(categories['recon'].name, "Reconnaissance")
        self.assertIn('test_tool', categories['recon'].tools)
        self.assertEqual(categories['recon'].tools['test_tool'].name, "Test Tool")

    def test_load_nonexistent_file(self):
        """Test loading a non-existent configuration file"""
        loader = ConfigLoader(Path("nonexistent.yaml"))
        with self.assertRaises(FileNotFoundError):
            loader.load()


class TestInputValidator(unittest.TestCase):
    """Test cases for InputValidator class"""

    def setUp(self):
        """Create a mock console for testing"""
        self.console = Console(file=StringIO(), legacy_windows=False)
        self.validator = InputValidator(self.console)

    def test_validate_ipv4_valid(self):
        """Test validation of valid IPv4 addresses"""
        valid_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8"]

        for ip in valid_ips:
            is_valid, error = self.validator.validate_ipv4(ip)
            self.assertTrue(is_valid, f"IP {ip} should be valid")
            self.assertIsNone(error)

    def test_validate_ipv4_invalid(self):
        """Test validation of invalid IPv4 addresses"""
        invalid_ips = [
            "999.999.999.999",
            "192.168.1",
            "192.168.1.1.1",
            "abc.def.ghi.jkl",
            "192.168.-1.1",
            ""
        ]

        for ip in invalid_ips:
            is_valid, error = self.validator.validate_ipv4(ip)
            self.assertFalse(is_valid, f"IP {ip} should be invalid")
            self.assertIsNotNone(error)

    def test_validate_port_valid(self):
        """Test validation of valid port numbers"""
        valid_ports = ["1", "80", "443", "8080", "65535"]

        for port in valid_ports:
            is_valid, error = self.validator.validate_port(port)
            self.assertTrue(is_valid, f"Port {port} should be valid")
            self.assertIsNone(error)

    def test_validate_port_invalid(self):
        """Test validation of invalid port numbers"""
        invalid_ports = [
            "0",           # Too low
            "65536",       # Too high
            "-1",          # Negative
            "abc",         # Not a number
            "80.5",        # Decimal
            ""             # Empty
        ]

        for port in invalid_ports:
            is_valid, error = self.validator.validate_port(port)
            self.assertFalse(is_valid, f"Port {port} should be invalid")
            self.assertIsNotNone(error)

    def test_validate_port_boundary(self):
        """Test port validation at boundaries"""
        # Test minimum valid port
        is_valid, error = self.validator.validate_port("1")
        self.assertTrue(is_valid)

        # Test maximum valid port
        is_valid, error = self.validator.validate_port("65535")
        self.assertTrue(is_valid)

        # Test just below minimum
        is_valid, error = self.validator.validate_port("0")
        self.assertFalse(is_valid)

        # Test just above maximum
        is_valid, error = self.validator.validate_port("65536")
        self.assertFalse(is_valid)


class TestSessionLogger(unittest.TestCase):
    """Test cases for SessionLogger class"""

    def setUp(self):
        """Create a temporary log file for testing"""
        self.temp_log = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        self.temp_log.close()
        self.log_path = Path(self.temp_log.name)
        self.logger = SessionLogger(self.log_path)

    def tearDown(self):
        """Clean up temporary log file"""
        if self.log_path.exists():
            self.log_path.unlink()

    def test_log_command(self):
        """Test logging a command to file"""
        command = "nmap -sV 192.168.1.1"
        category = "Reconnaissance"
        tool = "Nmap"

        self.logger.log_command(command, category, tool)

        # Read the log file
        with open(self.log_path, 'r') as f:
            log_content = f.read()

        self.assertIn(command, log_content)
        self.assertIn(category, log_content)
        self.assertIn(tool, log_content)

    def test_multiple_logs(self):
        """Test logging multiple commands"""
        commands = [
            ("nmap -sV 192.168.1.1", "Recon", "Nmap"),
            ("nikto -h http://target.com", "Web", "Nikto"),
            ("hydra -L users.txt ssh://target", "Exploit", "Hydra")
        ]

        for cmd, cat, tool in commands:
            self.logger.log_command(cmd, cat, tool)

        # Read the log file
        with open(self.log_path, 'r') as f:
            log_lines = f.readlines()

        self.assertEqual(len(log_lines), 3)

        for i, (cmd, _, _) in enumerate(commands):
            self.assertIn(cmd, log_lines[i])


class TestDataClasses(unittest.TestCase):
    """Test cases for data classes"""

    def test_tool_config_creation(self):
        """Test ToolConfig dataclass creation"""
        tool = ToolConfig(
            name="Test Tool",
            description="A test description",
            command="test {param}",
            params=["param"]
        )

        self.assertEqual(tool.name, "Test Tool")
        self.assertEqual(tool.description, "A test description")
        self.assertEqual(tool.command, "test {param}")
        self.assertListEqual(tool.params, ["param"])

    def test_category_config_creation(self):
        """Test CategoryConfig dataclass creation"""
        tool = ToolConfig(
            name="Tool",
            description="Desc",
            command="cmd",
            params=[]
        )

        category = CategoryConfig(
            name="Test Category",
            tools={"tool1": tool}
        )

        self.assertEqual(category.name, "Test Category")
        self.assertIn("tool1", category.tools)
        self.assertEqual(category.tools["tool1"].name, "Tool")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
    # Test valid port
    is_valid, error, port = validator.validate_port("443")
    assert is_valid and port == 443, "Valid port should pass"
    console.print("[green]✓ Valid port accepted[/green]")

    # Test invalid port
    is_valid, error, port = validator.validate_port("99999")
    assert not is_valid, "Invalid port should fail"
    console.print("[green]✓ Invalid port rejected[/green]")

    return True


def test_dependency_checker():
    """Test dependency checking."""
    print("\nTesting DependencyChecker...")
    console = Console()
    checker = DependencyChecker(console)

    # Test common tool
    exists = checker.check_tool_exists("python")
    console.print(f"[green]✓ Python exists: {exists}[/green]")

    # Test non-existent tool
    exists = checker.check_tool_exists("nonexistent_tool_xyz123")
    console.print(f"[green]✓ Non-existent tool detected: {not exists}[/green]")

    return True


def test_session_logger():
    """Test session logging."""
    print("\nTesting SessionLogger...")
    console = Console()
    test_log = Path("test_session.log")
    logger = SessionLogger(test_log)

    logger.log_session_start()
    logger.log_command(
        "nmap -T4 192.168.1.1",
        "Reconnaissance",
        "Nmap Quick Scan"
    )

    if test_log.exists():
        console.print("[green]✓ Log file created successfully[/green]")
        # Clean up
        test_log.unlink()
        return True
    else:
        console.print("[red]✗ Log file not created[/red]")
        return False


def main():
    """Run all tests."""
    console = Console()
    console.print("\n[bold cyan]Tajaa CLI - Component Tests[/bold cyan]\n")

    tests = [
        ("Configuration Loader", test_config_loader),
        ("Input Validator", test_input_validator),
        ("Dependency Checker", test_dependency_checker),
        ("Session Logger", test_session_logger),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            console.print(f"[red]✗ {name} failed with exception: {e}[/red]")
            results.append((name, False))

    # Summary
    console.print("\n[bold]Test Summary:[/bold]")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[green]PASS[/green]" if result else "[red]FAIL[/red]"
        console.print(f"  {status} - {name}")

    console.print(f"\n[bold]Total: {passed}/{total} tests passed[/bold]\n")


if __name__ == "__main__":
    main()

