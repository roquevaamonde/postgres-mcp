# VS Code Setup Guide

## Overview

This guide provides step-by-step instructions to configure the PostgreSQL MCP Server in VS Code across all operating systems.

## Prerequisites

- VS Code installed with MCP support
- PostgreSQL MCP Server installed and configured
- Virtual environment activated with dependencies installed

## Step-by-Step Setup

### Step 1: Locate Your MCP Configuration File

The location varies by operating system:

#### Linux
```
~/.config/Code/User/mcp.json
```

#### macOS
```
~/Library/Application\ Support/Code/User/mcp.json
```

#### Windows (Registry-based Path)
```
%APPDATA%\Code\User\mcp.json
```

Expand the path:
```cmd
echo %APPDATA%\Code\User\mcp.json
```

#### WSL (Windows Subsystem for Linux)
```
~/.config/Code\ -\ WSL/User/mcp.json
```

### Step 2: Copy Configuration Template

```bash
cp config/mcp.json.example mcp.json
```

This creates a local copy you can edit and test before applying to VS Code.

### Step 3: Determine Your Virtual Environment Path

The path to Python executable varies by OS:

#### Linux / macOS / WSL

Find the Python executable in your virtual environment:

```bash
which python3
# Output example: /home/username/projects/postgres_mcp/venv/bin/python3
```

Or from within the venv:

```bash
source venv/bin/activate
which python3
```

#### Windows (Command Prompt)

```cmd
where python.exe
```

If using venv:

```cmd
venv\Scripts\python.exe
```

Full path example:
```
C:\Users\username\projects\postgres_mcp\venv\Scripts\python.exe
```

### Step 4: Update the MCP Configuration

Edit your `mcp.json` with the paths and credentials:

#### For Linux / macOS / WSL

```json
{
  "servers": {
    "postgres": {
      "type": "stdio",
      "command": "/home/username/projects/postgres_mcp/venv/bin/python3",
      "args": ["/home/username/projects/postgres_mcp/postgres_mcp_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "CONNECTION_NAMES": "default",
        "DEFAULT_HOST": "localhost",
        "DEFAULT_PORT": "5432",
        "DEFAULT_USER": "database_user",
        "DEFAULT_PASSWORD": "database_password",
        "DEFAULT_DATABASE": "database_name"
      }
    }
  }
}
```

#### For Windows

```json
{
  "servers": {
    "postgres": {
      "type": "stdio",
      "command": "C:\\Users\\username\\projects\\postgres_mcp\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\username\\projects\\postgres_mcp\\postgres_mcp_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "CONNECTION_NAMES": "default",
        "DEFAULT_HOST": "localhost",
        "DEFAULT_PORT": "5432",
        "DEFAULT_USER": "database_user",
        "DEFAULT_PASSWORD": "database_password",
        "DEFAULT_DATABASE": "database_name"
      }
    }
  }
}
```

### Step 5: Apply to VS Code

#### Option A: Edit VS Code Configuration Directly

Open VS Code's MCP configuration file:

1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Preferences: Open User Settings (JSON)"
3. Or navigate to: `~/.config/Code/User/mcp.json` directly

Paste your configuration into the file.

#### Option B: Copy Configuration to VS Code

```bash
# Linux / macOS / WSL
cp mcp.json ~/.config/Code/User/mcp.json

# Windows (PowerShell)
Copy-Item -Path "mcp.json" -Destination "$env:APPDATA\Code\User\mcp.json"
```

### Step 6: Restart VS Code

1. Close VS Code completely
2. Reopen VS Code
3. Wait for VS Code to initialize extensions and servers

The MCP server should now start automatically.

### Step 7: Verify Installation

#### Check Server Status

1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Search for "MCP" or "Claude"
3. You should see "PostgreSQL MCP" listed as an available server
4. Click to see available tools

#### View Server Logs

For debugging, check the output:

1. View > Output
2. Select "PostgreSQL MCP" from the dropdown
3. Review initialization and any error messages

## Troubleshooting

### "Server Failed to Start"

**Check:**
- Virtual environment path is correct and uses absolute path
- Python executable exists at the specified path
- postgres_mcp_server.py file exists

**Verify paths:**
```bash
# Check if file exists
ls /path/to/postgres_mcp_server.py
ls /path/to/venv/bin/python3

# Test Python can run
/path/to/venv/bin/python3 --version
```

### "Module Not Found"

**Solutions:**
1. Ensure `psycopg2-binary` is installed in the venv
2. Verify venv path in mcp.json is correct
3. Reinstall dependencies:
   ```bash
   source venv/bin/activate
   pip install psycopg2-binary
   ```

### "Connection Refused"

**Check:**
- Database host is correct and accessible
- Database credentials are correct
- PostgreSQL server is running
- Firewall allows connection to database port

### "Invalid Configuration"

**Verify:**
- JSON syntax is valid (use online JSON validator)
- All required fields are present
- String values are properly quoted
- File encoding is UTF-8

## Tips and Tricks

### Using Absolute Paths

Always use absolute paths in `mcp.json`:

```json
{
  "command": "/absolute/path/to/python3",
  "args": ["/absolute/path/to/postgres_mcp_server.py"]
}
```

NOT relative paths:
```json
{
  "command": "venv/bin/python3",  // ❌ Won't work
  "args": ["postgres_mcp_server.py"]  // ❌ Won't work
}
```

### Testing Configuration Locally

Before committing to VS Code config, test locally:

```bash
# Activate venv
source venv/bin/activate

# Run server manually
python3 postgres_mcp_server.py

# In another terminal, test with a request
echo '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | python3 postgres_mcp_server.py
```

### Managing Multiple Environments

If you have multiple database environments:

```json
{
  "servers": {
    "postgres-dev": {
      "type": "stdio",
      "command": "/path/to/venv/bin/python3",
      "args": ["/path/to/postgres_mcp_server.py"],
      "env": {
        "CONNECTION_NAMES": "dev,prod",
        "DEFAULT_HOST": "localhost",
        ...
      }
    },
    "postgres-prod": {
      "type": "stdio",
      "command": "/path/to/venv/bin/python3",
      "args": ["/path/to/postgres_mcp_server.py"],
      "env": {
        "CONNECTION_NAMES": "production",
        "DEFAULT_HOST": "prod-db.example.com",
        ...
      }
    }
  }
}
```

## Persistence

The MCP configuration is stored in:

- **Linux/macOS/WSL:** `~/.config/Code/User/settings.json`
- **Windows:** `%APPDATA%\Code\User\settings.json`

VS Code syncs this across devices if you have sync enabled.

## Next Steps

1. Read the [Configuration Guide](CONFIGURATION.md) for detailed credential setup
2. Check the [Project Structure](STRUCTURE.md) to understand the codebase
3. Run tests to verify everything works: `pytest tests/ -v`
