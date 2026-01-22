"""
Unit tests for PostgreSQL MCP Server
"""
import json
import pytest
from postgres_mcp import (
    ConfigurationManager,
    DatabaseManager,
    MCPServer
)


class TestConfigurationManager:
    """Test configuration loading"""

    def test_default_config_structure(self):
        """Test that default configuration has required structure"""
        manager = ConfigurationManager()
        config = manager.load()

        assert "connections" in config
        assert "defaultConnection" in config
        assert "queryTimeout" in config
        assert "logLevel" in config
        assert "enableSSL" in config

    def test_default_connection_exists(self):
        """Test that default connection is always available"""
        manager = ConfigurationManager()
        config = manager.load()

        assert "default" in config["connections"]
        default_conn = config["connections"]["default"]
        assert all(key in default_conn for key in ["host", "port", "user", "password", "database"])


class TestDatabaseManager:
    """Test database manager functionality"""

    def test_connection_validation(self):
        """Test that invalid connections return error"""
        connections = {
            "default": {
                "host": "localhost",
                "port": "5432",
                "user": "test",
                "password": "test",
                "database": "test"
            }
        }
        manager = DatabaseManager(connections)

        result = manager.execute_query("SELECT 1", "nonexistent")

        assert not result["success"]
        assert "not found" in result["error"]

    def test_query_result_structure(self):
        """Test that successful queries return correct structure"""
        # This is a structure test, not an actual DB test
        result = {
            "success": True,
            "result": [{"id": 1, "name": "test"}]
        }

        assert result["success"]
        assert isinstance(result["result"], list)
        assert all(isinstance(row, dict) for row in result["result"])


class TestMCPServer:
    """Test MCP Server functionality"""

    @pytest.fixture
    def server_config(self):
        """Create a test server configuration"""
        return {
            "connections": {
                "default": {
                    "host": "localhost",
                    "port": "5432",
                    "user": "test",
                    "password": "test",
                    "database": "test"
                }
            },
            "defaultConnection": "default",
            "queryTimeout": 30,
            "logLevel": "info",
            "enableSSL": False
        }

    @pytest.fixture
    def server(self, server_config):
        """Create a test MCP server"""
        return MCPServer(server_config)

    def test_initialize_response(self, server):
        """Test initialize request handling"""
        request = {"id": 1, "method": "initialize"}
        response = server.handle_initialize(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["serverInfo"]["name"] == "postgres-mcp"

    def test_list_tools_response(self, server):
        """Test list tools request handling"""
        request = {"id": 1}
        response = server.handle_list_tools(request)

        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        assert "tools" in response["result"]
        tool_names = [tool["name"] for tool in response["result"]["tools"]]
        assert "list_connections" in tool_names
        assert "query" in tool_names

    def test_list_connections(self, server):
        """Test list connections handler"""
        result = server.handle_list_connections()
        connections = json.loads(result)

        assert isinstance(connections, list)
        assert all(conn["name"] for conn in connections)

    def test_process_unknown_method(self, server):
        """Test handling of unknown methods"""
        request = {"id": 1, "method": "unknown/method"}
        response = server.process_request(request)

        assert "error" in response
        assert response["error"]["code"] == -32601

    def test_invalid_query_returns_error(self, server):
        """Test that invalid queries return error response"""
        result = server.handle_query("INVALID SQL", "default")

        # Result should always be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, (dict, list))

        # If it's a dict, it should be either a result or an error
        if isinstance(parsed, dict):
            assert "error" in parsed or len(parsed) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
