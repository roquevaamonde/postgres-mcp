"""Database connection and query execution management"""
import psycopg2
from typing import Dict, Any, List


class DatabaseManager:
    """Manages database connections and query execution"""

    def __init__(self, connections: Dict[str, Dict[str, str]], timeout: int = 30):
        self.connections = connections
        self.timeout = timeout

    def execute_query(self, sql: str, connection_name: str = "default") -> Dict[str, Any]:
        """Execute a SQL query against PostgreSQL"""
        if connection_name not in self.connections:
            return {"success": False, "error": f"Connection '{connection_name}' not found"}

        try:
            conn_config = self.connections[connection_name]
            conn = psycopg2.connect(
                host=conn_config["host"],
                port=int(conn_config["port"]),
                user=conn_config["user"],
                password=conn_config["password"],
                database=conn_config["database"],
                connect_timeout=self.timeout
            )

            cursor = conn.cursor()
            cursor.execute(sql)

            if cursor.description:
                results = self._fetch_results(cursor)
                conn.commit()
                cursor.close()
                conn.close()
                return {"success": True, "result": results}
            else:
                rows_affected = cursor.rowcount
                conn.commit()
                cursor.close()
                conn.close()
                return {"success": True, "result": f"Query executed. Rows affected: {rows_affected}"}

        except psycopg2.OperationalError as e:
            return {"success": False, "error": f"Database connection error: {str(e)}"}
        except psycopg2.ProgrammingError as e:
            return {"success": False, "error": f"SQL syntax error: {str(e)}"}
        except psycopg2.Error as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except (KeyError, ValueError, TypeError) as e:
            return {"success": False, "error": f"Configuration error: {str(e)}"}

    @staticmethod
    def _fetch_results(cursor) -> List[Dict[str, Any]]:
        """Fetch query results and convert to list of dictionaries"""
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in results]
