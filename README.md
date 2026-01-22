# 🐘 PostgreSQL MCP Server

A Model Context Protocol (MCP) server for PostgreSQL that enables executing SQL queries directly from VS Code without requiring external database tools.

## Overview

This MCP server provides a clean, JSON-based interface to PostgreSQL databases through VS Code. It supports multiple database connections, type-safe operations, and comprehensive error handling.

## ✨ Features

- **Multiple Database Connections**: Manage development, staging, and production databases
- **Structured JSON Responses**: Clean, validated response format
- **Type Hints**: Full type annotation for IDE support and error prevention
- **Comprehensive Testing**: Unit tests ensuring reliability
- **Object-Oriented Design**: Well-structured, maintainable codebase

## 📋 Requirements

- Python 3.8 or higher
- Access to PostgreSQL database(s)
- VS Code with MCP support
- `psycopg2-binary` Python package

## 🚀 Installation

### Quick Setup

```bash
# 1. Copy the configuration example
cp config/settings.json.example settings.json

# 2. Edit settings.json with your database credentials
nano settings.json

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install psycopg2-binary

# 5. Ready to use in VS Code
```

## ⚙️ Configuration

For detailed configuration instructions, see [Configuration Guide](docs/CONFIGURATION.md)

### Local Configuration: `settings.json`

```json
{
  "postgres": {
    "defaultConnection": "default",
    "queryTimeout": 30,
    "logLevel": "info",
    "enableSSL": false,
    "connections": [
      {
        "name": "default",
        "host": "localhost",
        "port": 5432,
        "user": "database_user",
        "password": "database_password",
        "database": "database_name"
      }
    ]
  }
}
```

## 🔧 VS Code Configuration

For detailed setup instructions by operating system, see [VS Code Setup Guide](docs/VSCODE_SETUP.md)

## 📖 Usage

### Executing Queries

Access the PostgreSQL MCP tools through VS Code's MCP interface:

**List Available Connections**
```
Tool: list_connections
Returns: JSON array of configured database connections
```

**Execute Query**
```
Tool: query
Parameters:
  - sql (string, required): SQL query to execute
  - connection (string, optional): Connection name (default: "default")
Returns: JSON array for SELECT queries, affected rows count for INSERT/UPDATE/DELETE
```

### Example

```sql
SELECT COUNT(*) as total FROM users WHERE active = true;
```

Response:
```json
[
  {
    "total": 42
  }
]
```

## 🧪 Testing

Run the comprehensive test suite to verify functionality:

```bash
# Activate virtual environment
source venv/bin/activate

# Execute tests
pytest tests/ -v
```

Expected output:
```
tests/test_postgres_mcp.py::TestConfigurationManager::test_default_config_structure PASSED
tests/test_postgres_mcp.py::TestDatabaseManager::test_connection_validation PASSED
tests/test_postgres_mcp.py::TestMCPServer::test_initialize_response PASSED
...
===== 9 passed in 0.07s =====
```

## 🏗️ Architecture

For detailed architecture documentation, see [Project Structure](docs/STRUCTURE.md)

The server is implemented with a clean, object-oriented design:

```
┌─────────────────────────┐
│ ConfigurationManager    │ ← Loads and validates configuration
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│  DatabaseManager        │ ← Manages connections and queries
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│  MCPServer              │ ← Handles MCP protocol requests
└────────────┬────────────┘
             │
        VS Code
```

## 📁 Project Structure

```
postgres_mcp/
├── postgres_mcp/              # Main package
│   ├── configuration.py       # Configuration management
│   ├── database.py            # Database operations
│   ├── server.py              # MCP server implementation
│   └── __init__.py            # Package initialization
├── config/                    # Configuration examples
│   ├── settings.json.example
│   └── mcp.json.example
├── docs/                      # Documentation
│   ├── CONFIGURATION.md
│   ├── VSCODE_SETUP.md
│   ├── STRUCTURE.md
│   └── REFACTORING.md
├── tests/                     # Unit tests
│   └── test_postgres_mcp.py
├── postgres_mcp_server.py     # Entry point
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🔍 Troubleshooting

### Connection Error: "Connection not found"
Verify that:
- The connection name exists in your configuration
- The name matches exactly (case-sensitive)
- The configuration file is properly formatted JSON

### Authentication Error: "Password authentication failed"
Check:
- Database user credentials are correct
- The user has appropriate permissions
- The database host is accessible
- Firewall rules allow the connection

### Database Error: "relation does not exist"
The specified table does not exist. Verify:
- Table name is correct and exists in the database
- You are connected to the correct database
- Table is in the public schema or schema path is specified

### Server Not Starting
- Verify Python version is 3.8+
- Ensure `psycopg2-binary` is installed in the virtual environment
- Check that paths in `mcp.json` are absolute and correct
- Review VS Code output console for error messages

## 📝 Recent Updates

- Modular package structure with organized directories
- Refactored to comprehensive object-oriented design
- Implemented robust JSON response handling
- Added comprehensive unit test suite
- Added full type hints throughout
- Improved error handling and reporting

## 🤝 Contributing

Contributions are welcome. Please ensure:
- Code follows existing patterns
- All tests pass before submitting
- New features include appropriate tests
- Documentation is updated accordingly

## 📄 License

This project is provided as-is for use in your projects.

---

**Professional PostgreSQL integration for VS Code**

For issues or questions, please refer to the troubleshooting section or review the test cases for usage examples.

