"""Configuration management for PostgreSQL MCP Server"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any


class ConfigurationManager:
    """Manages configuration loading from files and environment variables"""

    DEFAULT_CONFIG = {
        "connections": {},
        "defaultConnection": "default",
        "queryTimeout": 30,
        "logLevel": "info",
        "enableSSL": False
    }

    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()

    def load_from_file(self) -> None:
        """Load configuration from settings.json"""
        script_dir = Path(__file__).parent.parent
        settings_file = script_dir / "settings.json"

        if not settings_file.exists():
            return

        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                postgres_config = file_config.get("postgres", {})
                self._update_config_from_dict(postgres_config)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not load settings.json: {e}", file=sys.stderr)

    def load_from_environment(self) -> None:
        """Load configuration from environment variables"""
        connection_names = os.getenv("CONNECTION_NAMES", "default").split(",")
        for conn_name in connection_names:
            conn_name = conn_name.strip()
            if conn_name:
                self._load_connection_from_env(conn_name)

    def _update_config_from_dict(self, postgres_config: Dict[str, Any]) -> None:
        """Update configuration from a dictionary"""
        self.config["queryTimeout"] = postgres_config.get("queryTimeout", 30)
        self.config["logLevel"] = postgres_config.get("logLevel", "info")
        self.config["defaultConnection"] = postgres_config.get("defaultConnection", "default")
        self.config["enableSSL"] = postgres_config.get("enableSSL", False)

        for conn in postgres_config.get("connections", []):
            conn_name = conn.get("name", "default")
            self.config["connections"][conn_name] = {
                "host": conn.get("host", "localhost"),
                "port": str(conn.get("port", "5432")),
                "user": conn.get("user"),
                "password": conn.get("password"),
                "database": conn.get("database"),
            }

    def _load_connection_from_env(self, conn_name: str) -> None:
        """Load a single connection from environment variables"""
        prefix = conn_name.upper()
        host = os.getenv(f"{prefix}_HOST")
        user = os.getenv(f"{prefix}_USER")
        password = os.getenv(f"{prefix}_PASSWORD")
        database = os.getenv(f"{prefix}_DATABASE")
        port = os.getenv(f"{prefix}_PORT", "5432")

        if all([host, user, password, database]):
            self.config["connections"][conn_name] = {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database": database,
            }

    def _ensure_default_connection(self) -> None:
        """Ensure default connection exists"""
        if not self.config["connections"]:
            self.config["connections"]["default"] = {
                "host": os.getenv("DEFAULT_HOST", "localhost"),
                "port": os.getenv("DEFAULT_PORT", "5432"),
                "user": os.getenv("DEFAULT_USER", "learning_user"),
                "password": os.getenv("DEFAULT_PASSWORD", "django123"),
                "database": os.getenv("DEFAULT_DATABASE", "learning_db"),
            }

    def load(self) -> Dict[str, Any]:
        """Load all configuration and return the config dictionary"""
        self.load_from_file()
        self.load_from_environment()
        self._ensure_default_connection()
        return self.config
