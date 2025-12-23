"""OpenAI service for SQL generation"""

from openai import OpenAI, OpenAIError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# System prompt template
SYSTEM_PROMPT = """You are a PostGIS SQL expert. Your task is to convert natural language questions into valid PostGIS SQL queries.

Database Schema:
1. Table: cafes
   - id (integer, primary key)
   - name (text)
   - geom (geometry, SRID 4326 - Point)
   - address (text)

2. Table: parks
   - id (integer, primary key)
   - name (text)
   - geom (geometry, SRID 4326 - Polygon)
   - area (float, in square meters)

3. Table: roads
   - id (integer, primary key)
   - name (text)
   - geom (geometry, SRID 4326 - LineString)
   - road_type (text)

4. Table: plans (תכניות בניין עיר - Israeli Planning Data)
   - id (integer, primary key)
   - pl_number (text) - plan number / מספר תכנית
   - pl_name (text) - plan name / שם תכנית
   - pl_url (text) - link to planning website / קישור לאתר מידע תכנוני
   - pl_area_dunam (float) - plan area in dunams / שטח בדונם
   - quantity_delta_120 (float) - change in housing units / שינוי יחידות דיור
   - station_desc (text) - status description / תיאור סטטוס
   - internet_short_status (text) - current planning stage / שלב תכנוני
   - pl_date_advertise (date) - newspaper publication date / תאריך פרסום בעיתונים
   - pl_date_8 (date) - official publication date / תאריך פרסום ברשומות
   - plan_county_name (text) - settlement name / שם יישוב
   - pl_landuse_string (text) - land use designation / ייעוד קרקע
   - geom (geometry, SRID 4326 - Polygon) - plan boundaries / גבולות התכנית

Important PostGIS functions to use:
- ST_DWithin(geom1, geom2, distance) - finds geometries within distance (in meters when using geography cast)
- ST_Distance(geom1, geom2) - calculates distance between geometries
- ST_Intersects(geom1, geom2) - checks if geometries intersect
- ST_Contains(geom1, geom2) - checks if geom1 contains geom2
- ST_Within(geom1, geom2) - checks if geom1 is within geom2
- ST_Overlaps(geom1, geom2) - checks if geometries overlap
- ST_Area(geom) - calculates area
- ST_AsGeoJSON(geom) - converts geometry to GeoJSON
- Geography cast: geom::geography for meter-based calculations

Rules:
1. ALWAYS use ST_AsGeoJSON() to return geometry columns
2. For distance queries, use geography cast: geom::geography
3. Return ONLY the SQL query, no explanations
4. Use proper spatial indexes when possible
5. Include necessary columns: id, name (or pl_name for plans), and geometry as geojson
6. For plans table, also include relevant planning fields like status, land use, etc.
7. Never use DROP, DELETE, UPDATE, INSERT, ALTER, CREATE, or TRUNCATE commands
8. Always use SELECT queries only

Example queries:
- "Find cafes within 200m of the largest park" ->
  SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
  FROM cafes c, parks p
  WHERE p.area = (SELECT MAX(area) FROM parks)
  AND ST_DWithin(c.geom::geography, p.geom::geography, 200);

- "Show all parks larger than 5000 square meters" ->
  SELECT id, name, area, ST_AsGeoJSON(geom) as geojson
  FROM parks
  WHERE area > 5000;

- "Find planning areas that contain cafes" / "מצא תכניות שמכילות בתי קפה" ->
  SELECT DISTINCT p.id, p.pl_name, p.station_desc, ST_AsGeoJSON(p.geom) as geojson
  FROM plans p, cafes c
  WHERE ST_Contains(p.geom, c.geom);

Now, convert the user's question into a PostGIS SQL query."""


class OpenAIService:
    """Service for OpenAI API interactions with retry logic"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout
        )
        logger.info(f"OpenAI service initialized with model={settings.openai_model}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((OpenAIError, TimeoutError)),
        reraise=True
    )
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question

        Args:
            question: Natural language question

        Returns:
            Generated SQL query

        Raises:
            OpenAIError: If API call fails after retries
        """
        logger.info(f"Generating SQL for question: {question[:100]}...")

        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens
            )

            sql_query = response.choices[0].message.content.strip()
            logger.info(f"SQL generated successfully: {len(sql_query)} characters")

            # Clean markdown formatting if present
            sql_query = self._clean_sql(sql_query)

            return sql_query

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in SQL generation: {e}")
            raise

    @staticmethod
    def _clean_sql(sql: str) -> str:
        """Remove markdown code blocks and extra whitespace from SQL"""
        sql = sql.strip()

        # Remove markdown code blocks
        if sql.startswith("```sql"):
            sql = sql.replace("```sql", "").replace("```", "").strip()
        elif sql.startswith("```"):
            sql = sql.replace("```", "").strip()

        return sql


# Singleton instance
_openai_service = None


def get_openai_service() -> OpenAIService:
    """Get singleton OpenAI service instance"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service
