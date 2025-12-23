"""
Database service tests
"""

import pytest
from app.services.database import DatabaseService


class TestSQLValidation:
    """Test SQL validation logic"""

    def test_valid_select_query(self):
        """Test valid SELECT query passes validation"""
        db = DatabaseService()
        sql = "SELECT id, name FROM cafes WHERE id = 1"
        is_valid, error = db.validate_sql(sql)

        assert is_valid is True
        assert error == ""

    def test_query_must_start_with_select(self):
        """Test query must start with SELECT"""
        db = DatabaseService()
        sql = "UPDATE cafes SET name = 'test'"
        is_valid, error = db.validate_sql(sql)

        assert is_valid is False
        assert "SELECT" in error

    def test_blocked_keywords_detected(self):
        """Test blocked SQL keywords are detected"""
        db = DatabaseService()
        blocked_queries = [
            "SELECT * FROM cafes; DROP TABLE cafes",
            "SELECT * FROM cafes WHERE id = 1 DELETE FROM parks",
            "SELECT * FROM (INSERT INTO cafes VALUES (1, 'test'))",
            "SELECT * FROM cafes; ALTER TABLE cafes",
            "SELECT * FROM cafes; CREATE TABLE test",
            "SELECT * FROM cafes; TRUNCATE TABLE parks",
        ]

        for sql in blocked_queries:
            is_valid, error = db.validate_sql(sql)
            assert is_valid is False
            assert error != ""

    def test_multiple_statements_blocked(self):
        """Test multiple statements are blocked"""
        db = DatabaseService()
        sql = "SELECT * FROM cafes; SELECT * FROM parks"
        is_valid, error = db.validate_sql(sql)

        assert is_valid is False
        assert "Multiple" in error or "statements" in error.lower()

    def test_trailing_semicolon_allowed(self):
        """Test trailing semicolon is allowed"""
        db = DatabaseService()
        sql = "SELECT * FROM cafes;"
        is_valid, error = db.validate_sql(sql)

        assert is_valid is True

    def test_case_insensitive_validation(self):
        """Test validation is case insensitive"""
        db = DatabaseService()

        # Valid in different cases
        assert db.validate_sql("select * from cafes")[0] is True
        assert db.validate_sql("SELECT * FROM cafes")[0] is True
        assert db.validate_sql("SeLeCt * FrOm cafes")[0] is True

        # Invalid in different cases
        assert db.validate_sql("select * from cafes; drop table cafes")[0] is False
        assert db.validate_sql("SELECT * FROM cafes; DROP TABLE cafes")[0] is False


class TestDatabaseConnection:
    """Test database connection handling"""

    def test_database_service_initializes(self):
        """Test DatabaseService can be initialized"""
        db = DatabaseService()
        assert db is not None
        assert db.engine is not None

    def test_get_schema_info_structure(self):
        """Test get_schema_info returns correct structure"""
        db = DatabaseService()
        schema = db.get_schema_info()

        assert isinstance(schema, dict)
        assert "cafes" in schema
        assert "parks" in schema
        assert "roads" in schema
        assert "plans" in schema

        for table_name, table_info in schema.items():
            assert "columns" in table_info
            assert "geometry_type" in table_info
            assert "description" in table_info
            assert "count" in table_info

    def test_get_table_count(self):
        """Test get_table_count returns integer"""
        db = DatabaseService()
        count = db.get_table_count("cafes")

        assert isinstance(count, int)
        assert count >= 0
