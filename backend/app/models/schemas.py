"""Pydantic models for request/response validation"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for natural language queries"""

    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Natural language question to convert to SQL",
        example="Find all cafes within 200 meters of parks"
    )

    @validator('question')
    def validate_question(cls, v):
        """Validate question is not empty and doesn't contain suspicious patterns"""
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty")

        # Check for suspicious SQL injection patterns
        suspicious_patterns = ['--', '/*', '*/', 'xp_', 'sp_', 'exec(', 'execute(']
        for pattern in suspicious_patterns:
            if pattern.lower() in v.lower():
                raise ValueError(f"Question contains suspicious pattern: {pattern}")

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Show me all parks larger than 5000 square meters"
            }
        }


class QueryResponse(BaseModel):
    """Response model for query execution"""

    sql: str = Field(..., description="Generated SQL query")
    results: List[Dict[str, Any]] = Field(..., description="Query results")
    execution_time: float = Field(..., description="Execution time in seconds")
    result_count: int = Field(..., description="Number of results returned")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "sql": "SELECT id, name, ST_AsGeoJSON(geom) as geojson FROM parks WHERE area > 5000",
                "results": [
                    {"id": 1, "name": "Yarkon Park", "area": 15000, "geojson": {"type": "Polygon"}}
                ],
                "execution_time": 1.234,
                "result_count": 1,
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    database: str = Field(..., description="Database connection status")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TableInfo(BaseModel):
    """Information about a database table"""

    count: int = Field(..., description="Number of records")
    columns: List[str] = Field(..., description="Table columns")
    geometry_type: str = Field(..., description="Geometry type")
    description: Optional[str] = Field(None, description="Table description")


class SchemaResponse(BaseModel):
    """Database schema information"""

    tables: Dict[str, TableInfo] = Field(..., description="Database tables")
    total_records: int = Field(..., description="Total records across all tables")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "detail": "Question cannot be empty",
                "timestamp": "2024-01-01T12:00:00"
            }
        }
