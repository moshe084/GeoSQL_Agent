"""
Pydantic schema validation tests
"""

import pytest
from pydantic import ValidationError
from app.models.schemas import QueryRequest, QueryResponse


class TestQueryRequest:
    """Test QueryRequest validation"""

    def test_valid_query_request(self):
        """Test valid query request"""
        request = QueryRequest(question="Show all cafes")
        assert request.question == "Show all cafes"

    def test_question_too_short(self):
        """Test question must be at least 3 characters"""
        with pytest.raises(ValidationError):
            QueryRequest(question="ab")

    def test_question_too_long(self):
        """Test question cannot exceed 500 characters"""
        long_question = "a" * 501
        with pytest.raises(ValidationError):
            QueryRequest(question=long_question)

    def test_question_required(self):
        """Test question field is required"""
        with pytest.raises(ValidationError):
            QueryRequest()

    def test_empty_question_rejected(self):
        """Test empty question is rejected"""
        with pytest.raises(ValidationError):
            QueryRequest(question="")

    def test_whitespace_only_question_rejected(self):
        """Test whitespace-only question is rejected"""
        with pytest.raises(ValidationError):
            QueryRequest(question="   ")

    def test_suspicious_patterns_detected(self):
        """Test suspicious SQL patterns are detected"""
        suspicious_questions = [
            "Show cafes -- comment",
            "Find parks /* comment */",
            "List roads xp_cmdshell",
            "Get data sp_executesql",
            "Query exec('test')",
            "Search execute('test')",
        ]

        for question in suspicious_questions:
            with pytest.raises(ValidationError) as exc_info:
                QueryRequest(question=question)
            assert "suspicious" in str(exc_info.value).lower()

    def test_question_strips_whitespace(self):
        """Test question whitespace is stripped"""
        request = QueryRequest(question="  Show all cafes  ")
        assert request.question == "Show all cafes"


class TestQueryResponse:
    """Test QueryResponse model"""

    def test_valid_query_response(self):
        """Test valid query response"""
        response = QueryResponse(
            sql="SELECT * FROM cafes",
            results=[{"id": 1, "name": "Test"}],
            execution_time=1.5,
            result_count=1
        )

        assert response.sql == "SELECT * FROM cafes"
        assert len(response.results) == 1
        assert response.execution_time == 1.5
        assert response.result_count == 1
        assert response.timestamp is not None

    def test_all_fields_required(self):
        """Test all required fields must be present"""
        with pytest.raises(ValidationError):
            QueryResponse(sql="SELECT * FROM cafes")

    def test_results_must_be_list(self):
        """Test results must be a list"""
        with pytest.raises(ValidationError):
            QueryResponse(
                sql="SELECT * FROM cafes",
                results="not a list",
                execution_time=1.0,
                result_count=0
            )

    def test_execution_time_must_be_number(self):
        """Test execution_time must be a number"""
        with pytest.raises(ValidationError):
            QueryResponse(
                sql="SELECT * FROM cafes",
                results=[],
                execution_time="not a number",
                result_count=0
            )
