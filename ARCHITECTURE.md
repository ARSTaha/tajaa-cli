# Tajaa CLI - Architecture Documentation

## System Overview

Tajaa CLI is a production-grade penetration testing command manager built with object-oriented principles. The system provides a structured interface for executing security tools with intelligent input validation, dependency checking, and session logging.

### Core Design Philosophy

The architecture follows strict separation of concerns, where each component handles a specific aspect of the application lifecycle. This modular approach enables maintainability, testability, and extensibility while ensuring robust error handling at every layer.

### Technology Stack
- Python 3.8+: Modern Python with type hints
- Typer: Command-line interface framework
- Rich: Terminal formatting and UI
- InquirerPy: Interactive prompts
- PyYAML: Configuration parsing
- pyfiglet: ASCII art banners
- pyperclip: Clipboard integration

### System Flow Diagram

```
┌─────────────┐
│   Config    │  commands.yaml loaded and parsed
│   Loader    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     UI      │  Display categories and tools
│   Manager   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    User     │  Interactive tool selection
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Input     │  Validate IPv4, ports, parameters
│  Validator  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Dependency  │  Check if tool binary exists
│   Checker   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Command   │  Execute with progress feedback
│  Executor   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Session   │  Log command with timestamp
│   Logger    │
└─────────────┘
```

---

## Component Design

### ConfigLoader

**Responsibility:** Parse and validate YAML configuration files.

**Key Methods:**
- `load() -> Dict[str, CategoryConfig]`: Loads tool categories from YAML
- Validates configuration structure and converts to typed dataclasses

**Dependencies:** PyYAML, pathlib

**Error Handling:** Raises descriptive exceptions for malformed configuration

### InputValidator

**Responsibility:** Validate user input for security and correctness.

**Key Methods:**
- `validate_ipv4(ip_string: str) -> Tuple[bool, Optional[str]]`: IPv4 validation using ipaddress module
- `validate_port(port_string: str) -> Tuple[bool, Optional[str]]`: Port range validation (1-65535)
- `get_validated_input(param_name: str) -> str`: Interactive input with retry logic

**Validation Rules:**
- IPv4: Must be valid format (e.g., 192.168.1.1)
- Port: Integer between 1 and 65535
- Re-prompts on invalid input with clear error messages

### CommandExecutor

**Responsibility:** Execute pentesting commands with safety checks and feedback.

**Key Methods:**
- `execute(category: CategoryConfig, tool_name: str, tool: ToolConfig)`: Main execution flow
- `prepare_command(command_template: str, params: List[str]) -> str`: Build command from template
- `_execute_with_progress(command: str)`: Run command with visual progress indicator

**Safety Features:**
- Dependency checking before execution
- Command preview with user confirmation
- Clipboard auto-copy of generated commands
- Graceful KeyboardInterrupt handling

### SessionLogger

**Responsibility:** Maintain audit trail of executed commands.

**Key Methods:**
- `log_command(command: str, category: str, tool: str)`: Append to session log file

**Log Format:**
```
[2025-12-14 10:30:45] [Reconnaissance] [Nmap Quick Scan] nmap -T4 -F 192.168.1.1
```

**File Management:**
- Creates log file if not exists
- Appends with atomic writes
- Handles file permission errors gracefully

---

## Table of Contents
1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Class Hierarchy](#class-hierarchy)
4. [Component Details](#component-details)
5. [Data Flow](#data-flow)
6. [Extension Guide](#extension-guide)

---

## Overview

Tajaa CLI is built using **Object-Oriented Programming (OOP)** principles with a focus on:
- **Separation of Concerns**: Each class has a single, well-defined responsibility
- **Dependency Injection**: Components receive dependencies via constructors
- **Type Safety**: Comprehensive type hints using Python's `typing` module
- **Error Handling**: Graceful error handling at every level

### Technology Stack
- **Python 3.8+**: Modern Python with type hints
- **Typer**: Command-line interface framework
- **Rich**: Terminal formatting and UI
- **InquirerPy**: Interactive prompts
- **PyYAML**: Configuration parsing
- **pyfiglet**: ASCII art banners
- **pyperclip**: Clipboard integration

---

## Design Principles

### SOLID Principles Applied

#### 1. Single Responsibility Principle (SRP)
Each class has one reason to change:
- `ConfigLoader`: Only configuration loading
- `InputValidator`: Only input validation
- `CommandExecutor`: Only command execution
- `UIManager`: Only UI/UX concerns
- `DependencyChecker`: Only dependency checking
- `SessionLogger`: Only logging

#### 2. Open/Closed Principle (OCP)
- Easy to add new validators without modifying existing code
- Add new tools via YAML without touching Python code
- Extend categories without changing core logic

#### 3. Liskov Substitution Principle (LSP)
- All dataclasses (`ToolConfig`, `CategoryConfig`) can be used interchangeably
- Console interface is consistent across all classes

#### 4. Interface Segregation Principle (ISP)
- Each class exposes only the methods it needs
- No class is forced to implement unnecessary interfaces

#### 5. Dependency Inversion Principle (DIP)
- High-level `TajaaCLI` depends on abstractions (other classes)
- Dependencies are injected, not hard-coded

---

## Class Hierarchy

```
┌─────────────────────────────────────────────────────┐
│                    TajaaCLI                         │
│              (Main Orchestrator)                    │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Composes
        ┌──────────┴──────────┬──────────────────┬──────────────────┐
        │                     │                  │                  │
        ▼                     ▼                  ▼                  ▼
┌───────────────┐     ┌──────────────┐   ┌──────────────┐  ┌─────────────┐
│ ConfigLoader  │     │ UIManager    │   │ SessionLogger│  │CommandExec..│
└───────────────┘     └──────────────┘   └──────────────┘  └──────┬──────┘
        │                                                           │
        │ Loads                                          Composes   │
        ▼                                                           │
┌───────────────┐                                   ┌───────────────┴────┐
│CategoryConfig │                                   │ InputValidator     │
│               │                                   │ DependencyChecker  │
│   ├─ToolConfig│                                   └────────────────────┘
└───────────────┘
```

### Dataclasses (Value Objects)

```python
@dataclass
class ToolConfig:
    name: str              # Display name
    description: str       # Tool description
    command: str          # Command template
    params: List[str]     # Required parameters

@dataclass
class CategoryConfig:
    name: str                          # Category display name
    tools: Dict[str, ToolConfig]       # Tools in this category
```

---

## Component Details

### 1. ConfigLoader

**Responsibility**: Load and parse YAML configuration

```python
class ConfigLoader:
    def __init__(self, config_path: Path) -> None
    def load(self) -> Dict[str, CategoryConfig]
```

**Key Features**:
- Validates YAML structure
- Creates typed objects from raw data
- Provides helpful error messages
- Handles missing files gracefully

**Example Usage**:
```python
loader = ConfigLoader(Path("commands.yaml"))
categories = loader.load()
```

---

### 2. InputValidator

**Responsibility**: Validate user inputs based on parameter type

```python
class InputValidator:
    def __init__(self, console: Console) -> None
    def validate_ipv4(self, ip_string: str) -> Tuple[bool, Optional[str]]
    def validate_port(self, port_string: str) -> Tuple[bool, Optional[str], Optional[int]]
    def get_validated_input(self, param_name: str, prompt_text: Optional[str] = None) -> str
```

**Validation Rules**:
- **IPv4**: Uses `ipaddress.IPv4Address` for strict validation
- **Port**: Must be integer 1-65535
- **Others**: Non-empty string

**Example Usage**:
```python
validator = InputValidator(console)
is_valid, error = validator.validate_ipv4("192.168.1.1")
if is_valid:
    # Use the IP
else:
    # Show error
```

**Extending Validators**:
```python
def validate_url(self, url_string: str) -> Tuple[bool, Optional[str]]:
    """Add custom URL validation."""
    try:
        result = urlparse(url_string)
        if all([result.scheme, result.netloc]):
            return True, None
        return False, "Invalid URL format"
    except Exception as e:
        return False, str(e)
```

---

### 3. DependencyChecker

**Responsibility**: Verify system dependencies

```python
class DependencyChecker:
    def __init__(self, console: Console) -> None
    def check_tool_exists(self, tool_name: str) -> bool
    def warn_missing_tool(self, tool_name: str) -> bool
```

**How It Works**:
- Uses `shutil.which()` to check PATH
- Extracts binary name from command string
- Warns user with option to continue

**Example Usage**:
```python
checker = DependencyChecker(console)
if not checker.check_tool_exists("nmap"):
    if not checker.warn_missing_tool("nmap"):
        return  # User chose not to continue
```

---

### 4. SessionLogger

**Responsibility**: Log commands and sessions

```python
class SessionLogger:
    def __init__(self, log_file: Path) -> None
    def log_command(self, command: str, category: str, tool_name: str) -> None
    def log_session_start(self) -> None
```

**Log Format**:
```
================================================================================
SESSION START: 2025-12-13 14:30:00
================================================================================
[2025-12-13 14:31:15] Category: Reconnaissance | Tool: Nmap - Quick Scan
Command: nmap -T4 -F 192.168.1.1
--------------------------------------------------------------------------------
```

**Features**:
- Timestamps every entry
- Includes category and tool context
- Fails silently (doesn't interrupt UX)

---

### 5. CommandExecutor

**Responsibility**: Execute pentesting commands

```python
class CommandExecutor:
    def __init__(
        self,
        console: Console,
        validator: InputValidator,
        dependency_checker: DependencyChecker,
        logger: SessionLogger
    ) -> None
    
    def prepare_command(self, tool: ToolConfig) -> Optional[str]
    def execute(self, tool: ToolConfig, category_name: str, simulate: bool = False) -> None
    def _execute_with_progress(self, command: str) -> None
```

**Workflow**:
1. Check if tool exists (dependency)
2. Collect and validate parameters
3. Format command with parameters
4. Display command in panel
5. Copy to clipboard
6. Log to file
7. Execute with progress indicator

**Error Handling**:
- `KeyboardInterrupt`: Graceful cancellation
- Missing tool: Warning with option to continue
- Invalid params: Re-prompt until valid

---

### 6. UIManager

**Responsibility**: Manage user interface

```python
class UIManager:
    def __init__(self, console: Console) -> None
    def show_banner(self) -> None
    def show_categories_table(self, categories: Dict[str, CategoryConfig]) -> None
    def select_category(self, categories: Dict[str, CategoryConfig]) -> Optional[str]
    def select_tool(self, category: CategoryConfig) -> Optional[str]
```

**Features**:
- ASCII art banner (pyfiglet)
- Rich tables for categories
- Interactive menus (InquirerPy)
- Consistent styling

---

### 7. TajaaCLI (Main Application)

**Responsibility**: Orchestrate all components

```python
class TajaaCLI:
    def __init__(self, config_path: Path, log_path: Path) -> None
    def initialize(self) -> bool
    def run(self) -> None
```

**Main Loop**:
```
1. Show banner
2. Load configuration
3. Loop:
   a. Show categories
   b. User selects category
   c. User selects tool
   d. Execute tool
   e. Ask to continue
4. Exit gracefully
```

---

## Data Flow

### Command Execution Flow

```
User Input
    │
    ▼
┌─────────────────┐
│   UIManager     │ ← Show categories/tools
│  (select_tool)  │
└────────┬────────┘
         │ Selected tool
         ▼
┌─────────────────────┐
│  CommandExecutor    │
│  (execute)          │
└──────┬──────────────┘
       │
       ├─► DependencyChecker.check_tool_exists()
       │
       ├─► InputValidator.get_validated_input() ◄─┐
       │                                           │
       │   ┌───────────────────────────────────────┘
       │   │ Loop until valid
       │   │
       ├─► prepare_command() → format string
       │
       ├─► Display in Panel (Rich)
       │
       ├─► pyperclip.copy()
       │
       ├─► SessionLogger.log_command()
       │
       └─► subprocess.run() with Progress indicator
```

### Configuration Loading Flow

```
commands.yaml
    │
    ▼
┌──────────────┐
│ ConfigLoader │
│   (load)     │
└──────┬───────┘
       │
       ├─► yaml.safe_load()
       │
       ├─► Parse categories
       │
       ├─► Create ToolConfig objects
       │
       └─► Create CategoryConfig objects
           │
           ▼
       Dict[str, CategoryConfig]
           │
           ▼
       TajaaCLI.categories
```

---

## Extension Guide

### Adding a New Validator

**File**: `main.py`
**Class**: `InputValidator`

```python
def validate_mac_address(self, mac_string: str) -> Tuple[bool, Optional[str]]:
    """
    Validate MAC address format.
    
    Args:
        mac_string: String to validate as MAC address
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import re
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    
    if re.match(pattern, mac_string):
        return True, None
    else:
        return False, f"Invalid MAC address: '{mac_string}'"

# Update get_validated_input():
def get_validated_input(self, param_name: str, prompt_text: Optional[str] = None) -> str:
    # ...existing code...
    
    elif 'mac' in param_name.lower():
        is_valid, error_msg = self.validate_mac_address(user_input)
        if is_valid:
            return user_input
        else:
            self.console.print(f"[bold red]✗[/bold red] {error_msg}")
```

### Adding a New Category

**File**: `commands.yaml`

```yaml
categories:
  # ...existing categories...
  
  password_attacks:
    name: "Password Attacks"
    tools:
      john_the_ripper:
        name: "John the Ripper"
        description: "Crack password hashes"
        command: "john --wordlist=/usr/share/wordlists/rockyou.txt {hash_file}"
        params:
          - hash_file
      
      hashcat:
        name: "Hashcat - GPU Cracking"
        description: "GPU-accelerated password cracking"
        command: "hashcat -m {hash_type} -a 0 {hash_file} {wordlist}"
        params:
          - hash_type
          - hash_file
          - wordlist
```

### Adding a New Feature Class

Example: Add a **ReportGenerator** class

```python
class ReportGenerator:
    """Generates pentesting reports from session logs."""
    
    def __init__(self, console: Console, log_file: Path) -> None:
        """
        Initialize the report generator.
        
        Args:
            console: Rich console for output
            log_file: Path to session log file
        """
        self.console: Console = console
        self.log_file: Path = log_file
    
    def generate_markdown_report(self, output_path: Path) -> None:
        """
        Generate a Markdown report from session logs.
        
        Args:
            output_path: Where to save the report
        """
        # Implementation here
        pass
    
    def generate_html_report(self, output_path: Path) -> None:
        """
        Generate an HTML report from session logs.
        
        Args:
            output_path: Where to save the report
        """
        # Implementation here
        pass
```

Then integrate into `TajaaCLI`:

```python
class TajaaCLI:
    def __init__(self, config_path: Path, log_path: Path) -> None:
        # ...existing code...
        self.report_generator: ReportGenerator = ReportGenerator(
            self.console,
            log_path
        )
```

---

## Type Hints Reference

All functions use comprehensive type hints:

```python
# Simple types
def function_name(param: str) -> None:

# Optional types
def function_name(param: Optional[str] = None) -> bool:

# Complex types
def function_name(data: Dict[str, List[int]]) -> Tuple[bool, Optional[str]]:

# Path objects
def function_name(path: Path) -> None:

# Class instances
def function_name(console: Console) -> None:
```

---

## Best Practices

### When Adding New Features

1. **Follow SRP**: One class, one responsibility
2. **Use Type Hints**: Always annotate parameters and return types
3. **Add Docstrings**: Google-style docstrings for all public methods
4. **Handle Errors**: Try/except with user-friendly messages
5. **Test**: Write tests in `test_components.py`
6. **Document**: Update this file with your changes

### Code Style

```python
# Good
def validate_input(self, user_input: str) -> Tuple[bool, Optional[str]]:
    """
    Validate user input for security.
    
    Args:
        user_input: The input to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validation logic
        return True, None
    except ValueError as e:
        return False, str(e)

# Bad
def validate(input):  # No types, no docstring
    return input.strip() != ""
```

---

## Performance Considerations

- **YAML Loading**: Cached in memory after first load
- **Validation**: Minimal overhead, runs only on user input
- **Logging**: Asynchronous-friendly (doesn't block)
- **Progress Indicators**: Use Rich's async-aware Progress

---

## Security Considerations

### Input Validation
- Always validate before using in commands
- Prevent command injection
- Sanitize file paths

### Command Execution
- Use `subprocess.run()` with proper escaping
- Never use `os.system()` or `eval()`
- Validate tool existence before execution

### Logging
- Don't log sensitive data (passwords, API keys)
- Ensure log files have proper permissions
- Rotate logs regularly in production

---

## Testing Strategy

### Unit Tests
Test each class in isolation:
- ConfigLoader: Test YAML parsing
- InputValidator: Test validation logic
- DependencyChecker: Test tool detection

### Integration Tests
Test component interactions:
- TajaaCLI initialization
- Full command execution flow

### Manual Testing
- Test with invalid configs
- Test with missing dependencies
- Test keyboard interrupts
- Test edge cases

---

## Future Enhancements

### Planned Features
1. **Output Parsing**: Parse tool output and display summaries
2. **Report Generation**: Auto-generate pentest reports
3. **Tool Chaining**: Execute multiple tools in sequence
4. **Database Integration**: Store results in database
5. **Web UI**: Add optional web interface
6. **Plugin System**: Allow third-party plugins

### Extension Points
- Custom validators (URL, domain, etc.)
- Custom output parsers
- Custom report templates
- Custom tool integrations

---

**End of Architecture Documentation**

For questions or contributions, please open an issue on GitHub.

