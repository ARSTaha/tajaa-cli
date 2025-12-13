#!/usr/bin/env python3
"""
Example usage and testing script for Tajaa CLI
This demonstrates programmatic usage of the classes
"""

from pathlib import Path
from main import (
    ConfigLoader,
    InputValidator,
    DependencyChecker,
    SessionLogger
)
from rich.console import Console


def test_config_loader():
    """Test configuration loading."""
    print("Testing ConfigLoader...")
    console = Console()
    loader = ConfigLoader(Path("commands.yaml"))
    
    try:
        categories = loader.load()
        console.print(f"[green]✓ Loaded {len(categories)} categories[/green]")
        
        for cat_id, cat_config in categories.items():
            console.print(f"  - {cat_config.name}: {len(cat_config.tools)} tools")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Config loading failed: {e}[/red]")
        return False


def test_input_validator():
    """Test input validation."""
    print("\nTesting InputValidator...")
    console = Console()
    validator = InputValidator(console)
    
    # Test valid IPv4
    is_valid, error = validator.validate_ipv4("192.168.1.1")
    assert is_valid, "Valid IP should pass"
    console.print("[green]✓ Valid IPv4 accepted[/green]")
    
    # Test invalid IPv4
    is_valid, error = validator.validate_ipv4("999.999.999.999")
    assert not is_valid, "Invalid IP should fail"
    console.print("[green]✓ Invalid IPv4 rejected[/green]")
    
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

