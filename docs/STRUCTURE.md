# Project Structure

## Overview

The PostgreSQL MCP Server is organized into a clean, modular package structure following Python naming conventions and best practices.

## Directory Layout

```
postgres_mcp/
├── postgres_mcp/                    # Main package (importable module)
│   ├── __init__.py                  # Package initialization and public API
│   ├── configuration.py             # Configuration management
│   ├── database.py                  # Database operations
│   └── server.py                    # MCP server implementation
├── config/                          # Configuration files and examples
│   ├── settings.json.example        # settings.json template
│   └── mcp.json.example             # VS Code MCP configuration template
├── docs/                            # Documentation
│   ├── CONFIGURATION.md             # Configuration guide
│   ├── VSCODE_SETUP.md              # VS Code setup instructions
│   ├── STRUCTURE.md                 # This file
│   └── REFACTORING.md               # Refactoring notes
├── tests/                           # Unit tests
│   ├── __init__.py                  # Tests package
│   └── test_postgres_mcp.py         # Main test file
├── postgres_mcp_server.py           # Entry point (main server script)
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
└── venv/                            # Virtual environment (not committed)
```

## Module Description

### `postgres_mcp/__init__.py`
**Responsibility**: Package initialization and public API export

Exports:
- `ConfigurationManager`
- `DatabaseManager`
- `MCPServer`

Provides version information and ensures clean imports throughout the project.

### `postgres_mcp/configuration.py`
**Responsibility**: Configuration management

Contains the `ConfigurationManager` class which:
- Loads configuration from `settings.json`
- Loads configuration from environment variables
- Validates configuration structure
- Provides fallback defaults
- Ensures at least one database connection is available

**Key Methods:**
- `load()` - Load all configuration sources
- `load_from_file()` - Load from settings.json
- `load_from_environment()` - Load from env vars

### `postgres_mcp/database.py`
**Responsibility**: Database connectivity and query execution

Contains the `DatabaseManager` class which:
- Manages PostgreSQL connections
- Executes SQL queries safely
- Handles database errors gracefully
- Formats query results as Python dictionaries
- Implements proper connection lifecycle

**Key Methods:**
- `execute_query()` - Execute SQL against a specific connection
- `_fetch_results()` - Format query results as dictionaries

### `postgres_mcp/server.py`
**Responsibility**: MCP protocol implementation

Contains the `MCPServer` class which:
- Implements Model Context Protocol handlers
- Manages tool registration and discovery
- Handles JSON-RPC requests and responses
- Orchestrates configuration and database managers

**Key Methods:**
- `handle_initialize()` - MCP initialization
- `handle_list_tools()` - Return available tools
- `handle_call_tool()` - Execute a tool
- `process_request()` - Route incoming requests

### `postgres_mcp_server.py`
**Responsibility**: Application entry point

The main script that:
- Initializes the configuration manager
- Creates the MCP server instance
- Runs the main event loop
- Handles stdin/stdout communication with VS Code
- Manages exceptions and graceful shutdown

## Naming Conventions

Following Python PEP 8:

- **Package directory**: `postgres_mcp` (lowercase with underscore)
- **Module files**: `configuration.py`, `database.py`, `server.py` (lowercase with underscore)
- **Classes**: `ConfigurationManager`, `DatabaseManager`, `MCPServer` (CamelCase)
- **Methods**: `load_from_file()`, `execute_query()` (snake_case)
- **Constants**: `DEFAULT_CONFIG` (UPPERCASE with underscore)
- **Private methods**: `_fetch_results()`, `_update_config_from_dict()` (leading underscore)

## Dependencies

**Runtime:**
- `psycopg2-binary` (>=2.9.0) - PostgreSQL database adapter for Python

**Development:**
- `pytest` (>=6.0.0) - Testing framework

Install with:
```bash
pip install -r requirements.txt  # Production
pip install -r requirements-dev.txt  # Development (if available)
```

## Import Examples

### From the package:
```python
from postgres_mcp import ConfigurationManager, DatabaseManager, MCPServer
```

### From specific modules:
```python
from postgres_mcp.configuration import ConfigurationManager
from postgres_mcp.database import DatabaseManager
from postgres_mcp.server import MCPServer
```

## Testing Structure

Tests are located in the `tests/` directory:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_postgres_mcp.py -v

# Run specific test class
pytest tests/test_postgres_mcp.py::TestConfigurationManager -v

# Run specific test
pytest tests/test_postgres_mcp.py::TestDatabaseManager::test_connection_validation -v
```

Test coverage includes:
- Configuration loading and validation
- Database connection management
- Query execution and error handling
- MCP protocol implementation
- Error response formatting

## Extensibility

The modular structure makes it easy to extend:

### Adding New Database Backends

Create `postgres_mcp/mysql.py`:
```python
class MySQLManager:
    """MySQL implementation similar to DatabaseManager"""
    pass
```

### Adding Custom Tools

Extend `MCPServer` in `postgres_mcp/server.py`:
```python
def handle_custom_tool(self):
    # Your custom implementation
    pass
```

### Adding Configuration Providers

Extend `ConfigurationManager`:
```python
def load_from_vault(self):
    # Load from HashiCorp Vault, AWS Secrets Manager, etc.
    pass
```

## Code Quality Standards

- **Type Hints**: Full type annotations across all modules
- **Docstrings**: Module, class, and method-level documentation
- **Error Handling**: Comprehensive exception handling with informative messages
- **Testing**: 9 unit tests covering all major components
- **PEP 8**: Code follows Python style guidelines (checked with pylint/flake8)
- **Security**: Proper credential handling and SQL injection prevention

## Performance Considerations

- **Connection Management**: Connections are created per query and closed after use
- **Query Timeout**: Configurable query timeout prevents long-running queries
- **Error Recovery**: Graceful error handling prevents server crashes
- **JSON Serialization**: Efficient JSON encoding for response formatting

## Security Best Practices

1. **Credential Storage**
   - Use environment variables in production
   - Never commit `settings.json` with credentials

2. **SQL Injection Prevention**
   - Queries are executed directly (user responsibility)
   - Parameter binding recommended in client code

3. **Connection Security**
   - SSL/TLS support available
   - Configurable connection timeouts

4. **Error Information**
   - Error messages are logged but not exposed to clients
   - Database errors are sanitized in responses


