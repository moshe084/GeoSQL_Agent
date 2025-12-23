"""Database service for PostGIS operations"""

from sqlalchemy import create_engine, text, exc
from sqlalchemy.pool import QueuePool
from typing import List, Dict, Any, Tuple
import logging
from contextlib import contextmanager

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DatabaseService:
    """Service for database operations with connection pooling and error handling"""

    def __init__(self):
        """Initialize database engine with connection pooling"""
        self.engine = create_engine(
            settings.database_url,
            poolclass=QueuePool,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_pre_ping=True,  # Verify connections before using
            echo=settings.debug
        )
        logger.info(f"Database engine initialized with pool_size={settings.db_pool_size}")

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = self.engine.connect()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def health_check(self) -> bool:
        """Check database connection health"""
        try:
            with self.get_connection() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def execute_query(self, sql: str) -> Tuple[List[str], List[Tuple]]:
        """
        Execute SQL query safely and return columns and rows

        Args:
            sql: SQL query string

        Returns:
            Tuple of (column_names, rows)

        Raises:
            exc.SQLAlchemyError: If query execution fails
        """
        logger.info(f"Executing SQL query: {sql[:100]}...")

        try:
            with self.get_connection() as conn:
                result = conn.execute(text(sql))
                columns = list(result.keys())
                rows = result.fetchall()

                logger.info(f"Query successful: {len(rows)} rows, {len(columns)} columns")
                return columns, rows

        except exc.SQLAlchemyError as e:
            logger.error(f"SQL execution error: {e}")
            raise

    def get_table_count(self, table_name: str) -> int:
        """
        Get count of records in a table

        Note: table_name is validated against known tables in get_schema_info()
        to prevent SQL injection
        """
        # Whitelist of allowed tables
        allowed_tables = ["cafes", "parks", "roads", "plans"]
        if table_name not in allowed_tables:
            logger.warning(f"Invalid table name requested: {table_name}")
            return 0

        try:
            with self.get_connection() as conn:
                # Safe to use here as table_name is whitelisted
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                return result.scalar()
        except exc.SQLAlchemyError as e:
            logger.warning(f"Failed to get count for table {table_name}: {e}")
            return 0

    def get_schema_info(self) -> Dict[str, Any]:
        """Get database schema information"""
        tables_info = {
            "cafes": {
                "columns": ["id", "name", "geom", "address"],
                "geometry_type": "Point",
                "description": "Coffee shops and cafes"
            },
            "parks": {
                "columns": ["id", "name", "geom", "area"],
                "geometry_type": "Polygon",
                "description": "Parks and green spaces"
            },
            "roads": {
                "columns": ["id", "name", "geom", "road_type"],
                "geometry_type": "LineString",
                "description": "Roads and streets"
            },
            "plans": {
                "columns": [
                    "id", "pl_number", "pl_name", "pl_url", "pl_area_dunam",
                    "quantity_delta_120", "station_desc", "internet_short_status",
                    "pl_date_advertise", "pl_date_8", "plan_county_name",
                    "pl_landuse_string", "geom"
                ],
                "geometry_type": "Polygon",
                "description": "תכניות בניין עיר - Israeli Planning Data"
            }
        }

        # Add counts
        for table_name in tables_info.keys():
            tables_info[table_name]["count"] = self.get_table_count(table_name)

        return tables_info

    def validate_sql(self, sql: str) -> Tuple[bool, str]:
        """
        Validate SQL query for safety

        Args:
            sql: SQL query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        sql_upper = sql.upper().strip()

        # Must start with SELECT
        if not sql_upper.startswith("SELECT"):
            return False, "Only SELECT queries are allowed"

        # Check for blocked keywords
        for keyword in settings.blocked_sql_keywords:
            if keyword.upper() in sql_upper:
                return False, f"Blocked SQL keyword detected: {keyword}"

        # Check for multiple statements
        if ";" in sql[:-1]:  # Allow trailing semicolon
            return False, "Multiple SQL statements are not allowed"

        return True, ""

    def close(self):
        """Close database engine and connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database engine closed")


# Singleton instance
_db_service = None


def get_db_service() -> DatabaseService:
    """Get singleton database service instance"""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service
