# 🏗️ Architecture Documentation - Geo-SQL Agent

## 📐 System Overview

The Geo-SQL Agent is a three-tier application that uses AI to bridge natural language and spatial databases.

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Web Browser)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP Requests (JSON)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FRONTEND TIER                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Leaflet Map (Interactive Visualization)            │   │
│  │  - OpenStreetMap base layer                         │   │
│  │  - GeoJSON overlay for results                      │   │
│  │  - Popup interactions                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Query Interface                                    │   │
│  │  - Text input for natural language                  │   │
│  │  - SQL display console                              │   │
│  │  - Result statistics                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology: HTML5 + JavaScript + Leaflet.js               │
│  Deployment: Nginx (Docker)                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ POST /query (Natural Language)
                     │ Response: { sql, results, execution_time }
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  BACKEND TIER                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FastAPI Application                                │   │
│  │                                                      │   │
│  │  Routes:                                            │   │
│  │  - POST /query → Execute NL query                   │   │
│  │  - GET /schema → Get DB schema                      │   │
│  │  - GET /health → Health check                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                     │                                       │
│                     │                                       │
│  ┌─────────────────▼───────────────┐                       │
│  │  AI Agent (SQL Generator)        │                       │
│  │                                  │                       │
│  │  ┌────────────────────────────┐ │                       │
│  │  │ System Prompt:             │ │                       │
│  │  │ - Database schema          │ │                       │
│  │  │ - PostGIS functions        │ │                       │
│  │  │ - Query examples           │ │                       │
│  │  └────────────────────────────┘ │                       │
│  │            │                     │                       │
│  │            ▼                     │                       │
│  │  ┌────────────────────────────┐ │                       │
│  │  │ OpenAI GPT-4 API           │ │                       │
│  │  │ - Model: gpt-4             │ │                       │
│  │  │ - Temperature: 0           │ │                       │
│  │  │ - Max tokens: 500          │ │                       │
│  │  └────────────────────────────┘ │                       │
│  │            │                     │                       │
│  │            ▼                     │                       │
│  │  ┌────────────────────────────┐ │                       │
│  │  │ Generated SQL Query        │ │                       │
│  │  │ (PostGIS-compatible)       │ │                       │
│  │  └────────────────────────────┘ │                       │
│  └──────────────────────────────────┘                       │
│                     │                                       │
│                     │                                       │
│  ┌─────────────────▼───────────────┐                       │
│  │  SQL Executor                    │                       │
│  │  - SQLAlchemy engine             │                       │
│  │  - GeoAlchemy2 for geometries    │                       │
│  │  - Result parsing                │                       │
│  └──────────────────────────────────┘                       │
│                                                             │
│  Technology: Python 3.11, FastAPI, OpenAI SDK              │
│  Deployment: Docker (Uvicorn server)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ SQL Queries
                     │ Results: { id, name, geojson, ... }
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 DATABASE TIER                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PostgreSQL 15 + PostGIS 3.3                        │   │
│  │                                                      │   │
│  │  Tables:                                            │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ cafes                                 │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - address: TEXT                       │          │   │
│  │  │ - geom: GEOMETRY(Point, 4326)         │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ parks                                 │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - area: FLOAT                         │          │   │
│  │  │ - geom: GEOMETRY(Polygon, 4326)       │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ roads                                 │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - road_type: TEXT                     │          │   │
│  │  │ - geom: GEOMETRY(LineString, 4326)    │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  Spatial Functions Used:                            │   │
│  │  - ST_DWithin()      - Distance queries             │   │
│  │  - ST_Intersects()   - Intersection tests           │   │
│  │  - ST_Distance()     - Distance calculations        │   │
│  │  - ST_Area()         - Area calculations            │   │
│  │  - ST_AsGeoJSON()    - GeoJSON export              │   │
│  │  - ::geography       - Meter-based operations       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology: PostgreSQL 15, PostGIS 3.3                    │
│  Deployment: Docker (Official PostGIS image)               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Query Execution Flow

```
1. USER INPUT
   └─→ "Find cafes within 200m of the largest park"

2. FRONTEND
   └─→ POST /query
       Headers: { Content-Type: application/json }
       Body: { "question": "Find cafes within 200m of..." }

3. BACKEND - FastAPI Endpoint
   └─→ Receives request
       Validates input with Pydantic
       └─→ Calls AI Agent

4. AI AGENT - SQL Generation
   └─→ Constructs prompt:
       System: "You are a PostGIS expert..."
       User: "Find cafes within 200m..."
   └─→ Calls OpenAI API
       Model: gpt-4
       Temperature: 0 (deterministic)
   └─→ Receives SQL:
       "SELECT c.id, c.name, ST_AsGeoJSON(c.geom)
        FROM cafes c, parks p
        WHERE p.area = (SELECT MAX(area) FROM parks)
        AND ST_DWithin(c.geom::geography, p.geom::geography, 200)"

5. SQL EXECUTOR
   └─→ Validates SQL (basic checks)
   └─→ Executes on PostGIS database
   └─→ Parses results:
       - Converts ST_AsGeoJSON() strings to JSON
       - Formats as list of dicts

6. BACKEND RESPONSE
   └─→ Returns JSON:
       {
         "sql": "SELECT c.id, c.name...",
         "results": [
           { "id": 3, "name": "Aroma", "geojson": {...} },
           { "id": 5, "name": "Landwer", "geojson": {...} }
         ],
         "execution_time": 0.143
       }

7. FRONTEND
   └─→ Displays SQL in console
   └─→ Renders GeoJSON on map
   └─→ Shows statistics
```

## 🧩 Component Details

### Frontend (Single-Page Application)

**File:** `frontend/index.html`

**Responsibilities:**
- User interface for query input
- Map visualization
- API communication
- Result display

**Key Libraries:**
- **Leaflet 1.9.4:** Map rendering
- **OpenStreetMap:** Base map tiles
- **Vanilla JavaScript:** No framework overhead

**API Integration:**
```javascript
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: userInput })
});

const data = await response.json();
// data = { sql, results, execution_time }
```

### Backend (FastAPI Application)

**File:** `backend/main.py`

**Endpoints:**

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/` | GET | API info | - | Welcome message + endpoints |
| `/health` | GET | Health check | - | `{ status, database }` |
| `/schema` | GET | DB schema | - | `{ tables: { cafes, parks, roads } }` |
| `/query` | POST | Execute NL query | `{ question: str }` | `{ sql, results, execution_time }` |

**Request/Response Models (Pydantic):**

```python
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    results: List[Dict[str, Any]]
    execution_time: float
```

**AI Integration:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.question}
    ],
    temperature=0,
    max_tokens=500
)
```

**Database Connection:**
```python
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://geouser:geopass@postgis:5432/geospatial"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text(sql_query))
```

### Database (PostGIS)

**Container:** `postgis/postgis:15-3.3`

**Initialization:**
1. `01-init-schema.sql` - Creates tables and indexes
2. `02-load-sample-data.sql` - Loads Tel Aviv data

**Coordinate System:**
- **SRID 4326** (WGS84) - Standard GPS coordinates
- Longitude/Latitude pairs
- Example: `(34.7818, 32.0853)` = Tel Aviv

**Spatial Indexes:**
```sql
CREATE INDEX idx_cafes_geom ON cafes USING GIST(geom);
```
- **GIST:** Generalized Search Tree
- Speeds up spatial queries by 10-100x

**Geography Casting:**
```sql
ST_DWithin(geom::geography, geom::geography, 200)
```
- `geometry` type: planar (fast, inaccurate for distance)
- `geography` type: spherical (accurate, meters)

## 🎯 Design Decisions

### Why GPT-4 over GPT-3.5?
- **Better SQL accuracy** - Fewer syntax errors
- **Complex query understanding** - Handles ambiguous questions
- **Schema reasoning** - Understands table relationships

**Trade-off:** Cost (~10x more) but worth it for demo quality

### Why FastAPI over Flask/Django?
- **Async support** - Better performance for I/O-bound tasks
- **Auto API docs** - Swagger UI at `/docs`
- **Type safety** - Pydantic validation
- **Modern Python** - Uses type hints

### Why Leaflet over Mapbox/Google Maps?
- **Open source** - No API keys needed
- **Lightweight** - Small bundle size
- **Flexible** - Easy to customize
- **Free** - OpenStreetMap tiles

**Trade-off:** Less features than Mapbox, but sufficient for POC

### Why Docker Compose?
- **Reproducible** - Same environment everywhere
- **Isolated** - No conflicts with local Postgres
- **Simple** - One command to start all services
- **Portable** - Works on any platform

### Why PostGIS over MongoDB/GeoJSON files?
- **Industry standard** - Used by OpenStreetMap, GIS professionals
- **Powerful** - 300+ spatial functions
- **Performant** - Optimized spatial indexes
- **SQL** - Familiar query language

## 🔐 Security Considerations

### Current Implementation (POC)

⚠️ **Not production-ready!** This is a demo project.

**Current vulnerabilities:**
- No SQL injection protection
- No authentication/authorization
- CORS allows all origins
- API keys in environment variables
- No rate limiting
- No input validation on SQL output

### Production Recommendations

1. **SQL Injection Prevention:**
   ```python
   # Add SQL validation before execution
   # Whitelist allowed tables
   # Use parameterized queries where possible
   ```

2. **Authentication:**
   ```python
   from fastapi import Depends, HTTPException
   from fastapi.security import APIKeyHeader

   api_key_header = APIKeyHeader(name="X-API-Key")

   async def verify_api_key(api_key: str = Depends(api_key_header)):
       if api_key != VALID_API_KEY:
           raise HTTPException(status_code=403, detail="Invalid API key")
   ```

3. **Rate Limiting:**
   ```python
   from slowapi import Limiter

   limiter = Limiter(key_func=get_remote_address)

   @app.post("/query")
   @limiter.limit("5/minute")
   async def execute_query(...):
       ...
   ```

4. **CORS:**
   ```python
   allow_origins=["https://yourdomain.com"]  # Not "*"
   ```

5. **Secrets Management:**
   - Use AWS Secrets Manager / Azure Key Vault
   - Never commit `.env` to git
   - Rotate API keys regularly

## 📊 Performance Characteristics

### Expected Latency

| Component | Operation | Typical Time |
|-----------|-----------|--------------|
| Frontend | User input → API call | < 10ms |
| Backend | Request parsing | < 5ms |
| OpenAI API | SQL generation | 500-2000ms |
| Backend | SQL execution | 10-100ms |
| Backend | Result formatting | < 10ms |
| Frontend | Map rendering | 50-200ms |
| **Total** | **End-to-end** | **~1-2 seconds** |

**Bottleneck:** OpenAI API call (70-80% of total time)

### Optimization Opportunities

1. **Caching common queries:**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def generate_sql(question: str) -> str:
       # Cache LLM responses
   ```

2. **Streaming SQL execution:**
   - Show SQL immediately
   - Execute while user reads it

3. **Database query optimization:**
   - Use EXPLAIN ANALYZE
   - Add more indexes if needed

4. **Frontend optimization:**
   - Debounce query input
   - Show loading states

## 🔍 Monitoring & Debugging

### Useful Docker Commands

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# Check container status
docker ps

# Inspect database
docker exec -it geo-sql-postgis psql -U geouser -d geospatial
```

### Backend Logging

The FastAPI app includes automatic logging:
- Request/response logging
- SQL query logging
- Error stack traces

### Database Debugging

```sql
-- Check table contents
SELECT COUNT(*) FROM cafes;
SELECT COUNT(*) FROM parks;

-- Test spatial query manually
SELECT ST_AsGeoJSON(geom) FROM cafes LIMIT 1;

-- Check indexes
SELECT tablename, indexname FROM pg_indexes WHERE tablename IN ('cafes', 'parks', 'roads');

-- Analyze query performance
EXPLAIN ANALYZE
SELECT c.id FROM cafes c, parks p
WHERE ST_DWithin(c.geom::geography, p.geom::geography, 200);
```

## 🚀 Deployment Architecture

### Current (Development)

```
┌──────────────────────────────────┐
│       Docker Host                │
│                                  │
│  ┌──────────┐  ┌──────────┐     │
│  │ Frontend │  │ Backend  │     │
│  │ :3010    │  │ :8000    │     │
│  └──────────┘  └──────────┘     │
│       │              │           │
│       └──────┬───────┘           │
│              │                   │
│        ┌─────▼─────┐             │
│        │ PostGIS   │             │
│        │ :5432     │             │
│        └───────────┘             │
└──────────────────────────────────┘
```

### Production (Suggested)

```
┌─────────────────────────────────────────────┐
│              Load Balancer                  │
│           (Nginx / CloudFlare)              │
└──────┬──────────────────────┬───────────────┘
       │                      │
       │                      │
┌──────▼──────┐        ┌──────▼──────┐
│  Frontend   │        │   Backend   │
│  (Static)   │        │  (FastAPI)  │
│  CDN / S3   │        │  ECS / K8s  │
└─────────────┘        └──────┬──────┘
                              │
                       ┌──────▼──────┐
                       │   PostGIS   │
                       │   RDS / DO  │
                       └─────────────┘
```

## 📚 Further Reading

- [PostGIS Documentation](https://postgis.net/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Leaflet Tutorials](https://leafletjs.com/examples.html)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Questions about the architecture?** Open an issue or discussion!
