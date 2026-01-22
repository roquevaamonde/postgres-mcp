# Configuration Guide

## Overview

The PostgreSQL MCP Server supports two configuration methods:
1. **Local configuration file** (`settings.json`) - Best for development
2. **Environment variables** - Best for production and security-sensitive environments

## Local Configuration: `settings.json`

### Setup

Copy the example configuration:

```bash
cp config/settings.json.example settings.json
```

Edit the file with your database credentials:

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
      },
      {
        "name": "production",
        "host": "prod-db.example.com",
        "port": 5432,
        "user": "prod_user",
        "password": "prod_password",
        "database": "prod_database"
      }
    ]
  }
}
```

### Configuration Options

- **defaultConnection** (string): Name of the default connection to use
- **queryTimeout** (integer): Query execution timeout in seconds (default: 30)
- **logLevel** (string): Logging level - "debug", "info", "warning", "error" (default: "info")
- **enableSSL** (boolean): Enable SSL/TLS for database connections (default: false)
- **connections** (array): Array of database connection configurations

### Connection Options

Each connection requires:

- **name** (string, required): Unique identifier for the connection
- **host** (string, required): Database host address
- **port** (integer, optional): Database port (default: 5432)
- **user** (string, required): Database username
- **password** (string, required): Database password
- **database** (string, required): Database name

## Environment Variables (Recommended for Production)

For security-sensitive environments, configure connections using environment variables instead of storing credentials in files.

### Format

Environment variables follow a naming pattern:

```
[CONNECTION_NAME]_HOST
[CONNECTION_NAME]_PORT
[CONNECTION_NAME]_USER
[CONNECTION_NAME]_PASSWORD
[CONNECTION_NAME]_DATABASE
```

### Example Configuration

For a "default" connection:

```bash
export CONNECTION_NAMES="default"
export DEFAULT_HOST="localhost"
export DEFAULT_PORT="5432"
export DEFAULT_USER="db_user"
export DEFAULT_PASSWORD="db_password"
export DEFAULT_DATABASE="db_name"
```

For multiple connections:

```bash
export CONNECTION_NAMES="default,production,development"

# Default connection
export DEFAULT_HOST="localhost"
export DEFAULT_PORT="5432"
export DEFAULT_USER="dev_user"
export DEFAULT_PASSWORD="dev_password"
export DEFAULT_DATABASE="dev_db"

# Production connection
export PRODUCTION_HOST="prod-db.example.com"
export PRODUCTION_PORT="5432"
export PRODUCTION_USER="prod_user"
export PRODUCTION_PASSWORD="prod_password"
export PRODUCTION_DATABASE="prod_db"

# Development connection
export DEVELOPMENT_HOST="localhost"
export DEVELOPMENT_PORT="5432"
export DEVELOPMENT_USER="dev_user"
export DEVELOPMENT_PASSWORD="dev_password"
export DEVELOPMENT_DATABASE="dev_db"
```

### Setting Environment Variables Persistently

#### Linux/macOS

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
export DEFAULT_HOST="localhost"
export DEFAULT_USER="db_user"
# ... other variables
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

#### Windows (PowerShell)

Set user environment variables:

```powershell
[Environment]::SetEnvironmentVariable("DEFAULT_HOST", "localhost", "User")
[Environment]::SetEnvironmentVariable("DEFAULT_USER", "db_user", "User")
# ... other variables
```

Or set for current session only:

```powershell
$env:DEFAULT_HOST = "localhost"
$env:DEFAULT_USER = "db_user"
```

## Configuration Priority

The server loads configuration in this order:

1. **Default fallback values**
2. **settings.json file** (if it exists)
3. **Environment variables** (override file settings)

This means environment variables take precedence over the configuration file, allowing flexible override scenarios.

## Validation

The server validates configuration on startup:

- Ensures at least one database connection is configured
- Verifies all required connection parameters are present
- Reports errors with descriptive messages

If configuration fails to load, the server will:
1. Attempt to use fallback environment variables
2. Use default values for optional parameters
3. Exit with an error if no valid configuration can be established

## Troubleshooting Configuration Issues

### "Connection not found"
- Verify the connection name matches exactly (case-sensitive)
- Check that the connection is defined in either `settings.json` or environment variables

### "Could not load settings.json"
- Ensure the file is valid JSON
- Check file permissions (must be readable)
- Verify the file path is correct relative to the script location

### "Configuration error: Key 'X' not found"
- Ensure all required connection parameters are provided
- Required fields: host, port, user, password, database

## Security Best Practices

1. **Never commit `settings.json` with credentials**
   ```bash
   # Add to .gitignore
   settings.json
   ```

2. **Use environment variables in production**
   - More secure than storing in files
   - Can be managed by container/deployment systems

3. **Restrict file permissions**
   ```bash
   chmod 600 settings.json
   ```

4. **Use strong passwords**
   - Generate secure database passwords
   - Rotate credentials regularly

5. **Use SSL/TLS in production**
   ```json
   {
     "postgres": {
       "enableSSL": true,
       ...
     }
   }
   ```
