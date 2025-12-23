"""Query service orchestrating SQL generation and execution"""

import logging
import json
import time
from typing import Dict, Any, List

from app.services.database import get_db_service
from app.services.openai_service import get_openai_service
from app.models.schemas import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)


class QueryService:
    """Service for handling end-to-end query processing"""

    def __init__(self):
        """Initialize query service with database and OpenAI services"""
        self.db_service = get_db_service()
        self.openai_service = get_openai_service()
        logger.info("Query service initialized")

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process natural language query and return results

        Args:
            request: Query request with natural language question

        Returns:
            Query response with SQL, results, and metadata

        Raises:
            ValueError: If SQL validation fails
            Exception: If query execution fails
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info("NEW QUERY REQUEST")
        logger.info(f"Question: {request.question}")
        logger.info("=" * 80)

        try:
            # Step 1: Generate SQL using OpenAI
            logger.info("STEP 1: Generating SQL using OpenAI...")
            sql_query = self.openai_service.generate_sql(request.question)
            logger.info(f"Generated SQL:\n{sql_query}")

            # Step 2: Validate SQL
            logger.info("STEP 2: Validating SQL...")
            is_valid, error_message = self.db_service.validate_sql(sql_query)
            if not is_valid:
                logger.error(f"SQL validation failed: {error_message}")
                raise ValueError(f"Invalid SQL: {error_message}")
            logger.info("SQL validation passed")

            # Step 3: Execute SQL query
            logger.info("STEP 3: Executing SQL query...")
            columns, rows = self.db_service.execute_query(sql_query)

            # Step 4: Format results
            logger.info("STEP 4: Formatting results...")
            results = self._format_results(columns, rows)

            execution_time = time.time() - start_time

            logger.info("=" * 80)
            logger.info("QUERY COMPLETED SUCCESSFULLY")
            logger.info(f"Execution time: {execution_time:.3f}s")
            logger.info(f"Results: {len(results)} rows")
            logger.info("=" * 80)

            return QueryResponse(
                sql=sql_query,
                results=results,
                execution_time=execution_time,
                result_count=len(results)
            )

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            raise

    @staticmethod
    def _format_results(columns: List[str], rows: List[tuple]) -> List[Dict[str, Any]]:
        """
        Format database rows into list of dictionaries

        Args:
            columns: Column names
            rows: Database rows

        Returns:
            List of dictionaries with column names as keys
        """
        results = []

        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]

                # Parse GeoJSON strings
                if col == 'geojson' and isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse GeoJSON for row")
                        pass

                row_dict[col] = value

            results.append(row_dict)

        return results


# Singleton instance
_query_service = None


def get_query_service() -> QueryService:
    """Get singleton query service instance"""
    global _query_service
    if _query_service is None:
        _query_service = QueryService()
    return _query_service
