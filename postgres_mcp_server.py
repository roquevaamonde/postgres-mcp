#!/usr/bin/env python3
"""
PostgreSQL MCP Server for VS Code
Communicates via stdio with JSON-RPC protocol
Supports multiple database connections
Configuration can be loaded from settings.json or environment variables
"""
import json
import sys

from postgres_mcp import ConfigurationManager, MCPServer


def main():
    """Main server loop"""
    config_manager = ConfigurationManager()
    config = config_manager.load()
    server = MCPServer(config)

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = server.process_request(request)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                pass
            except (KeyError, ValueError, TypeError, OSError) as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -1,
                        "message": str(e)
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
