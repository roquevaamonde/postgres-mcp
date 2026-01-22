"""Model Context Protocol server implementation"""
import json
from typing import Dict, Any

try:
    from .database import DatabaseManager
except ImportError:
    from database import DatabaseManager


class MCPServer:
    """Model Context Protocol server for PostgreSQL"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_manager = DatabaseManager(
            config["connections"],
            config["queryTimeout"]
        )
        self.default_connection = config["defaultConnection"]

    def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize message"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "postgres-mcp",
                    "version": "1.0.0"
                }
            }
        }

    def handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """List available tools"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "list_connections",
                        "description": "List all available database connections",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "query",
                        "description": "Execute a SQL query against PostgreSQL",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sql": {
                                    "type": "string",
                                    "description": "The SQL query to execute"
                                },
                                "connection": {
                                    "type": "string",
                                    "description": f"Connection name (default: {self.default_connection})"
                                }
                            },
                            "required": ["sql"]
                        }
                    }
                ]
            }
        }

    def handle_list_connections(self) -> str:
        """List all available connections"""
        connections_info = [
            {
                "name": conn_name,
                "host": config["host"],
                "port": config["port"],
                "database": config["database"],
                "user": config["user"]
            }
            for conn_name, config in self.config["connections"].items()
        ]
        return json.dumps(connections_info, indent=2)

    def handle_query(self, sql: str, connection_name: str) -> str:
        """Execute a query and return results as JSON"""
        result = self.db_manager.execute_query(sql, connection_name)

        # Always return structured JSON, whether success or error
        if result.get("success"):
            result_data = result.get("result")
        else:
            result_data = {"error": result.get("error", "Unknown error")}

        if isinstance(result_data, (list, dict)):
            return json.dumps(result_data, indent=2, ensure_ascii=False)
        return json.dumps({"result": str(result_data)}, ensure_ascii=False)

    def handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool calls"""
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})
        connection = arguments.get("connection", self.default_connection)

        if tool_name == "list_connections":
            text = self.handle_list_connections()
        elif tool_name == "query":
            sql = arguments.get("sql", "")
            text = self.handle_query(sql, connection)
        else:
            text = f"Unknown tool: {tool_name}"

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "content": [{"type": "text", "text": text}]
            }
        }

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming MCP request"""
        method = request.get("method")

        if method == "initialize":
            return self.handle_initialize(request)
        elif method == "tools/list":
            return self.handle_list_tools(request)
        elif method == "tools/call":
            return self.handle_call_tool(request)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
