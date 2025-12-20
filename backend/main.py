from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from sqlalchemy import create_engine, text
from openai import OpenAI
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Geo-SQL Agent")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://geouser:geopass@localhost:5432/geospatial")
engine = create_engine(DATABASE_URL)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for SQL generation
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

Important PostGIS functions to use:
- ST_DWithin(geom1, geom2, distance) - finds geometries within distance (in meters when using geography cast)
- ST_Distance(geom1, geom2) - calculates distance between geometries
- ST_Intersects(geom1, geom2) - checks if geometries intersect
- ST_Contains(geom1, geom2) - checks if geom1 contains geom2
- ST_Area(geom) - calculates area
- ST_AsGeoJSON(geom) - converts geometry to GeoJSON
- Geography cast: geom::geography for meter-based calculations

Rules:
1. ALWAYS use ST_AsGeoJSON() to return geometry columns
2. For distance queries, use geography cast: geom::geography
3. Return ONLY the SQL query, no explanations
4. Use proper spatial indexes when possible
5. Include necessary columns: id, name, and geometry as geojson

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

Now, convert the user's question into a PostGIS SQL query."""


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    sql: str
    results: List[Dict[str, Any]]
    execution_time: float


@app.get("/")
async def root():
    return {
        "message": "Geo-SQL Agent API",
        "endpoints": {
            "/query": "POST - Execute natural language query",
            "/schema": "GET - Get database schema",
            "/health": "GET - Check service health"
        }
    }


@app.get("/health")
async def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    try:
        with engine.connect() as conn:
            # Get table counts
            cafes_count = conn.execute(text("SELECT COUNT(*) FROM cafes")).scalar()
            parks_count = conn.execute(text("SELECT COUNT(*) FROM parks")).scalar()
            roads_count = conn.execute(text("SELECT COUNT(*) FROM roads")).scalar()

        return {
            "tables": {
                "cafes": {
                    "count": cafes_count,
                    "columns": ["id", "name", "geom", "address"]
                },
                "parks": {
                    "count": parks_count,
                    "columns": ["id", "name", "geom", "area"]
                },
                "roads": {
                    "count": roads_count,
                    "columns": ["id", "name", "geom", "road_type"]
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute natural language query"""
    import time

    logger.info("="*80)
    logger.info("🔵 NEW QUERY REQUEST")
    logger.info(f"📝 Question: {request.question}")
    logger.info("="*80)

    try:
        # Step 1: Generate SQL using OpenAI
        start_time = time.time()

        logger.info("🤖 STEP 1: Sending question to OpenAI GPT-4...")
        logger.info(f"   Model: gpt-4")
        logger.info(f"   Temperature: 0")
        logger.info(f"   Max Tokens: 500")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.question}
            ],
            temperature=0,
            max_tokens=500
        )

        sql_query = response.choices[0].message.content.strip()
        logger.info("✅ Received response from OpenAI")
        logger.info(f"📄 Raw SQL Response:\n{sql_query}")

        # Remove markdown code blocks if present
        if sql_query.startswith("```sql"):
            logger.info("🔧 Cleaning SQL: Removing ```sql markdown blocks")
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            logger.info("🔧 Cleaning SQL: Removing ``` markdown blocks")
            sql_query = sql_query.replace("```", "").strip()

        logger.info(f"✨ Final SQL Query:\n{sql_query}")

        # Step 2: Execute SQL query
        logger.info("🗄️  STEP 2: Executing SQL query on PostGIS database...")

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = result.keys()
            rows = result.fetchall()

            logger.info(f"✅ Query executed successfully")
            logger.info(f"📊 Columns: {list(columns)}")
            logger.info(f"📈 Rows returned: {len(rows)}")

            # Convert to list of dicts
            results = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    # Parse GeoJSON strings
                    if col == 'geojson' and isinstance(value, str):
                        try:
                            value = json.loads(value)
                            logger.info(f"   🗺️  Parsed GeoJSON for row {len(results) + 1}")
                        except:
                            pass
                    row_dict[col] = value
                results.append(row_dict)

        execution_time = time.time() - start_time

        logger.info("="*80)
        logger.info("🟢 QUERY COMPLETED SUCCESSFULLY")
        logger.info(f"⏱️  Total Execution Time: {execution_time:.3f}s")
        logger.info(f"📊 Total Results: {len(results)}")
        logger.info("="*80)

        return QueryResponse(
            sql=sql_query,
            results=results,
            execution_time=execution_time
        )

    except Exception as e:
        logger.error("="*80)
        logger.error("🔴 QUERY FAILED")
        logger.error(f"❌ Error Type: {type(e).__name__}")
        logger.error(f"❌ Error Message: {str(e)}")
        logger.error("="*80)
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
