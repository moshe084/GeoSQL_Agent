# 🏗️ Architecture Documentation - Geo-SQL Agent

## 📐 System Overview

The Geo-SQL Agent is a modern three-tier application that uses AI to bridge natural language and spatial databases. Built with production-grade architecture, modular services, and comprehensive error handling.

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
│  │  React-Leaflet Map (Interactive Visualization)      │   │
│  │  - OpenStreetMap base layer                         │   │
│  │  - GeoJSON overlay for results                      │   │
│  │  - Popup interactions                               │   │
│  │  - Marker clustering                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Query Interface Components                         │   │
│  │  - QueryInput: Natural language input               │   │
│  │  - SQLDisplay: SQL visualization                    │   │
│  │  - LoadingSpinner: Async state management           │   │
│  │  - ErrorBoundary: Error handling                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology: React 18 + TypeScript + Tailwind CSS          │
│  State: Context API + Custom Hooks                         │
│  Map Library: React-Leaflet 4.x                            │
│  Testing: Jest + React Testing Library                     │
│  Deployment: Nginx (Docker - Production build)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ POST /query (Natural Language)
                     │ Response: { sql, results, execution_time, result_count }
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  BACKEND TIER                               │
│                    (Modular Architecture)                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FastAPI Application (app/main.py)                  │   │
│  │                                                      │   │
│  │  - Lifespan event handlers (startup/shutdown)       │   │
│  │  - Global exception handling                        │   │
│  │  - OpenAPI documentation (/docs, /redoc)            │   │
│  │  - Pydantic-based configuration                     │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │  Middleware Layer (app/api/middleware.py)           │   │
│  │  - CORS configuration                               │   │
│  │  - Request/Response logging                         │   │
│  │  - Rate limiting (SlowAPI)                          │   │
│  │  - Request ID tracking                              │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │  API Routes (app/api/routes.py)                     │   │
│  │                                                      │   │
│  │  Endpoints:                                         │   │
│  │  - GET  /          → API information                │   │
│  │  - GET  /health    → Health check + DB status       │   │
│  │  - GET  /schema    → Database schema info           │   │
│  │  - POST /query     → Execute NL query (rate limited)│   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼────────────────────────────────────┐   │
│  │  Service Layer (Singleton Pattern)                  │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ QueryService (app/services/query_service.py) │  │   │
│  │  │ - Orchestrates query flow                    │  │   │
│  │  │ - Coordinates OpenAI + Database              │  │   │
│  │  │ - Formats results                            │  │   │
│  │  │ - Logging & monitoring                       │  │   │
│  │  └──────────┬───────────────┬───────────────────┘  │   │
│  │             │               │                       │   │
│  │  ┌──────────▼──────┐  ┌────▼────────────────────┐ │   │
│  │  │ OpenAIService   │  │ DatabaseService         │ │   │
│  │  │ - SQL generation│  │ - Connection pooling    │ │   │
│  │  │ - GPT-4 client  │  │ - Query execution       │ │   │
│  │  │ - Prompt mgmt   │  │ - SQL validation        │ │   │
│  │  │ - Retry logic   │  │ - Schema introspection  │ │   │
│  │  └─────────────────┘  │ - Health checks         │ │   │
│  │                       └─────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Configuration (app/config.py)                      │   │
│  │  - Pydantic Settings with validation                │   │
│  │  - Environment variable loading                     │   │
│  │  - Type-safe configuration                          │   │
│  │  - Default values + overrides                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Data Models (app/models/schemas.py)                │   │
│  │  - QueryRequest, QueryResponse                      │   │
│  │  - HealthResponse, SchemaResponse                   │   │
│  │  - ErrorResponse, TableInfo                         │   │
│  │  - Full Pydantic validation                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology: Python 3.11, FastAPI, OpenAI SDK, SlowAPI     │
│  Testing: pytest, pytest-asyncio, pytest-cov               │
│  Deployment: Docker (Uvicorn server with hot-reload)       │
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
│  │  Tables (4 spatial tables):                         │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ cafes (Points)                        │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - address: TEXT                       │          │   │
│  │  │ - geom: GEOMETRY(Point, 4326)         │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  │ ~ 15 cafes in Tel Aviv                │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ parks (Polygons)                      │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - area: FLOAT                         │          │   │
│  │  │ - geom: GEOMETRY(Polygon, 4326)       │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  │ ~ 7 major parks                       │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ roads (LineStrings)                   │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - name: TEXT                          │          │   │
│  │  │ - road_type: TEXT                     │          │   │
│  │  │ - geom: GEOMETRY(LineString, 4326)    │          │   │
│  │  │ - INDEX: GIST(geom)                   │          │   │
│  │  │ ~ 6 main streets                      │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────┐          │   │
│  │  │ plans (Polygons) 🆕                   │          │   │
│  │  │ Israeli urban planning data           │          │   │
│  │  │ - id: SERIAL PRIMARY KEY              │          │   │
│  │  │ - pl_number: VARCHAR(78)              │          │   │
│  │  │ - pl_name: TEXT                       │          │   │
│  │  │ - pl_url: TEXT                        │          │   │
│  │  │ - pl_area_dunam: DOUBLE PRECISION     │          │   │
│  │  │ - quantity_delta_120: DOUBLE PRECISION│          │   │
│  │  │ - station_desc: VARCHAR(100)          │          │   │
│  │  │ - internet_short_status: VARCHAR(100) │          │   │
│  │  │ - pl_date_advertise: DATE             │          │   │
│  │  │ - pl_date_8: DATE                     │          │   │
│  │  │ - plan_county_name: VARCHAR(100)      │          │   │
│  │  │ - pl_landuse_string: TEXT             │          │   │
│  │  │ - geom: GEOMETRY(Polygon, 4326)       │          │   │
│  │  │ - INDEXES: GIST(geom), pl_number,     │          │   │
│  │  │   station_desc, plan_county_name,     │          │   │
│  │  │   pl_landuse_string                   │          │   │
│  │  │ ~ Thousands of planning areas         │          │   │
│  │  └──────────────────────────────────────┘          │   │
│  │                                                      │   │
│  │  Spatial Functions Used:                            │   │
│  │  - ST_DWithin()      - Distance queries             │   │
│  │  - ST_Intersects()   - Intersection tests           │   │
│  │  - ST_Contains()     - Containment checks           │   │
│  │  - ST_Within()       - Reverse containment          │   │
│  │  - ST_Distance()     - Distance calculations        │   │
│  │  - ST_Area()         - Area calculations            │   │
│  │  - ST_AsGeoJSON()    - GeoJSON export              │   │
│  │  - ::geography       - Meter-based operations       │   │
│  │                                                      │   │
│  │  Initialization Scripts:                            │   │
│  │  1. 01-init-schema.sql    - Create tables & indexes │   │
│  │  2. 02-load-sample-data.sql - Load sample data     │   │
│  │  3. 03-create-plans-table.sql - Create plans table │   │
│  │  4. 04-import-plans-data.py - Import planning data │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology: PostgreSQL 15, PostGIS 3.3                    │
│  Deployment: Docker (postgis/postgis:15-3.3 image)         │
│  Health Checks: pg_isready + connection tests              │
│  Resource Limits: 2 CPUs, 1GB RAM                          │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Query Execution Flow (Detailed)

```
1. USER INPUT
   └─→ User types: "Find cafes within 200m of the largest park"
       React component: <QueryInput />

2. FRONTEND - React App
   └─→ useQuery() hook triggered
   └─→ API call via Axios:
       POST http://localhost:8000/query
       Headers: { Content-Type: application/json }
       Body: { "question": "Find cafes within 200m of..." }
   └─→ Loading state managed by AppContext

3. BACKEND - Middleware Layer (app/api/middleware.py)
   └─→ Request intercepted by:
       - CORS middleware (validates origin)
       - Rate limiter (checks: 10 requests/60 seconds)
       - Request logger (logs IP, timestamp, endpoint)
   └─→ Request ID assigned for tracking

4. BACKEND - API Route (app/api/routes.py)
   └─→ POST /query endpoint handler
   └─→ Pydantic validation:
       - Question length check (max 500 chars)
       - Type validation (must be string)
   └─→ Calls QueryService.process_query()

5. SERVICE LAYER - QueryService (app/services/query_service.py)
   └─→ STEP 1: Generate SQL
       - Calls OpenAIService.generate_sql(question)
       - Logs: "Generating SQL using OpenAI..."

6. SERVICE LAYER - OpenAIService (app/services/openai_service.py)
   └─→ Constructs prompt:
       System: "You are a PostGIS SQL expert. Database schema:
                - cafes (id, name, address, geom POINT)
                - parks (id, name, area, geom POLYGON)
                - roads (id, name, road_type, geom LINESTRING)
                - plans (id, pl_number, pl_name, ..., geom POLYGON)
                Use ST_DWithin for distances, ::geography for meters..."
       User: "Find cafes within 200m of the largest park"
   └─→ Calls OpenAI API:
       Model: gpt-4
       Temperature: 0 (deterministic)
       Max tokens: 500
       Timeout: 30 seconds
   └─→ Receives SQL:
       "SELECT c.id, c.name, c.address, ST_AsGeoJSON(c.geom) as geojson
        FROM cafes c, parks p
        WHERE p.area = (SELECT MAX(area) FROM parks)
        AND ST_DWithin(c.geom::geography, p.geom::geography, 200);"

7. SERVICE LAYER - QueryService (Validation)
   └─→ STEP 2: Validate SQL
       - Calls DatabaseService.validate_sql(sql)
       - Checks for blocked keywords: DROP, DELETE, UPDATE, INSERT, etc.
       - Verifies allowed keywords only: SELECT, FROM, WHERE, etc.
       - Logs: "SQL validation passed"

8. SERVICE LAYER - DatabaseService (app/services/database.py)
   └─→ STEP 3: Execute SQL
       - Gets connection from pool (SQLAlchemy)
       - Executes query with text() wrapper
       - Fetches all rows
       - Returns: (columns, rows)

9. SERVICE LAYER - QueryService (Formatting)
   └─→ STEP 4: Format Results
       - Converts rows to list of dictionaries
       - Parses GeoJSON strings to JSON objects
       - Calculates execution time
       - Logs: "Query completed: 0.143s, 3 results"

10. BACKEND RESPONSE
    └─→ Returns QueryResponse (Pydantic model):
        {
          "sql": "SELECT c.id, c.name...",
          "results": [
            { "id": 3, "name": "Aroma", "address": "...", "geojson": {...} },
            { "id": 5, "name": "Landwer", "address": "...", "geojson": {...} },
            { "id": 8, "name": "Cofix", "address": "...", "geojson": {...} }
          ],
          "execution_time": 0.143,
          "result_count": 3
        }

11. FRONTEND - React Components
    └─→ <SQLDisplay /> shows SQL query + execution time
    └─→ <Map /> component:
        - Parses GeoJSON from results
        - Adds markers to Leaflet map
        - Creates popups with cafe details
        - Fits map bounds to show all results
    └─→ Stats display: "📊 Found 3 results"
```

### Error Handling Flow

```
Error Scenario 1: Invalid Input
  User → Frontend → Backend → Rate Limiter
  └─→ 429 Too Many Requests (>10 requests/minute)
  └─→ Frontend displays error banner

Error Scenario 2: SQL Validation Failure
  User → Frontend → Backend → QueryService → DatabaseService
  └─→ Detects "DROP TABLE" in SQL
  └─→ Raises ValueError("Invalid SQL: Blocked keyword")
  └─→ 400 Bad Request
  └─→ Frontend displays error message

Error Scenario 3: Database Connection Failure
  Backend → DatabaseService → PostgreSQL
  └─→ Connection timeout
  └─→ Health check fails
  └─→ 503 Service Unavailable
  └─→ Frontend displays: "Database connection failed"

Error Scenario 4: OpenAI API Failure
  Backend → OpenAIService → OpenAI API
  └─→ API key invalid / Rate limit / Timeout
  └─→ Retry logic (3 attempts)
  └─→ If all fail: 500 Internal Server Error
  └─→ Frontend displays generic error
```

## 🧩 Component Details

### Frontend (React + TypeScript Application)

**Directory Structure:**
```
frontend-react/
├── src/
│   ├── App.tsx                      # Main application component
│   ├── index.tsx                    # Entry point
│   ├── components/
│   │   ├── Map.tsx                  # Leaflet map with markers
│   │   ├── QueryInput.tsx           # Input form with validation
│   │   ├── SQLDisplay.tsx           # SQL syntax highlighting
│   │   ├── LoadingSpinner.tsx       # Loading state indicator
│   │   └── ErrorBoundary.tsx        # React error boundary
│   ├── context/
│   │   └── AppContext.tsx           # Global state management
│   ├── hooks/
│   │   ├── useQuery.ts              # Custom hook for API calls
│   │   └── index.ts                 # Hook exports
│   ├── services/
│   │   └── api.ts                   # Axios API client
│   ├── types/
│   │   └── index.ts                 # TypeScript type definitions
│   └── __tests__/
│       ├── components/              # Component tests
│       └── hooks/                   # Hook tests
├── Dockerfile.dev                   # Development Docker image
├── Dockerfile.prod                  # Production Docker image
└── package.json
```

**Technology Stack:**
- **React 18.2** with TypeScript 5.x
- **Tailwind CSS 3.x** for utility-first styling
- **Context API** for global state management
- **React-Leaflet 4.x** for map visualization
- **Axios** for HTTP requests with interceptors
- **Jest + React Testing Library** for testing

**Key Components:**

1. **App.tsx** - Main application wrapper
   - Provides AppContext to all children
   - Wraps in ErrorBoundary for error handling
   - Coordinates QueryInput, Map, and SQLDisplay

2. **QueryInput.tsx** - User input interface
   - Controlled textarea component
   - Client-side validation (max 500 chars)
   - Submit on Enter (Shift+Enter for newline)
   - Loading state disables input

3. **Map.tsx** - Interactive Leaflet map
   - OpenStreetMap base tiles
   - Dynamic marker generation from GeoJSON
   - Popup windows with result details
   - Auto-fit bounds to show all markers
   - Support for Points, Polygons, LineStrings

4. **SQLDisplay.tsx** - SQL visualization
   - Syntax highlighting (basic)
   - Copy-to-clipboard button
   - Execution time display
   - Collapsible panel

5. **AppContext.tsx** - Global state
   ```typescript
   interface AppState {
     currentQuery: QueryResult | null;
     queryHistory: QueryResult[];
     isLoading: boolean;
     error: string | null;
   }
   ```

**Custom Hooks:**

```typescript
// useQuery.ts
export const useQuery = () => {
  const { dispatch } = useAppContext();

  const executeQuery = async (question: string) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const response = await api.post('/query', { question });
      dispatch({ type: 'SET_QUERY_RESULT', payload: response.data });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  return { executeQuery, isLoading, error };
};
```

**API Integration:**
```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor (logging)
api.interceptors.request.use(config => {
  console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
  return config;
});

// Response interceptor (error handling)
api.interceptors.response.use(
  response => response,
  error => {
    const message = error.response?.data?.detail || error.message;
    console.error('API Error:', message);
    return Promise.reject(new Error(message));
  }
);
```

**Deployment:**
- **Development:** Vite dev server with hot reload (port 3000)
- **Production:** Optimized build served by Nginx (port 3010)
- **Docker profiles:** development / production

### Backend (FastAPI Application - Modular Architecture)

**Directory Structure:**
```
backend/
├── app/
│   ├── __init__.py                  # Package metadata
│   ├── main.py                      # FastAPI app + lifespan
│   ├── config.py                    # Pydantic settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py                # API endpoints
│   │   └── middleware.py            # CORS, logging, rate limiting
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── query_service.py         # Query orchestration
│   │   ├── openai_service.py        # OpenAI integration
│   │   └── database.py              # Database operations
│   └── tests/
│       ├── conftest.py              # pytest fixtures
│       ├── test_api.py              # API endpoint tests
│       ├── test_database.py         # Database tests
│       └── test_schemas.py          # Pydantic validation tests
├── main.py                          # Backward compatibility shim
├── requirements.txt
├── requirements-dev.txt
└── Dockerfile
```

**API Endpoints:**

| Endpoint | Method | Purpose | Request | Response | Rate Limit |
|----------|--------|---------|---------|----------|------------|
| `/` | GET | API info | - | API metadata + endpoints | No |
| `/health` | GET | Health check | - | `{ status, database, version, environment }` | No |
| `/schema` | GET | DB schema | - | `{ tables: {...}, total_records }` | No |
| `/query` | POST | Execute NL query | `{ question: str }` | `{ sql, results, execution_time, result_count }` | Yes (10/min) |

**Pydantic Models:**

```python
# Request Models
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

# Response Models
class QueryResponse(BaseModel):
    sql: str
    results: List[Dict[str, Any]]
    execution_time: float
    result_count: int

class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
    environment: str

class TableInfo(BaseModel):
    columns: List[str]
    count: int
    geometry_type: Optional[str]

class SchemaResponse(BaseModel):
    tables: Dict[str, TableInfo]
    total_records: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    detail: Optional[str]
```

**Service Layer Architecture:**

1. **QueryService** (app/services/query_service.py)
   - Orchestrates the entire query flow
   - Coordinates OpenAI + Database services
   - Handles logging and monitoring
   - Formats results for frontend

2. **OpenAIService** (app/services/openai_service.py)
   ```python
   class OpenAIService:
       def generate_sql(self, question: str) -> str:
           """Generate SQL from natural language"""
           response = self.client.chat.completions.create(
               model=self.settings.openai_model,
               messages=[
                   {"role": "system", "content": self._get_system_prompt()},
                   {"role": "user", "content": question}
               ],
               temperature=0.0,
               max_tokens=500,
               timeout=30
           )
           return response.choices[0].message.content
   ```

3. **DatabaseService** (app/services/database.py)
   ```python
   class DatabaseService:
       def __init__(self):
           """Initialize with connection pooling"""
           self.engine = create_engine(
               DATABASE_URL,
               pool_size=5,
               max_overflow=10,
               pool_timeout=30
           )

       def validate_sql(self, sql: str) -> Tuple[bool, Optional[str]]:
           """Validate SQL for security"""
           # Check for blocked keywords
           for keyword in BLOCKED_KEYWORDS:
               if keyword in sql.upper():
                   return False, f"Blocked keyword: {keyword}"
           return True, None

       def execute_query(self, sql: str) -> Tuple[List[str], List[tuple]]:
           """Execute SQL and return columns + rows"""
           with self.engine.connect() as conn:
               result = conn.execute(text(sql))
               columns = list(result.keys())
               rows = result.fetchall()
           return columns, rows
   ```

**Configuration Management:**

```python
# app/config.py
class Settings(BaseSettings):
    # Application
    app_name: str = "Geo-SQL Agent"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.0

    # CORS
    cors_origins: List[str] = ["http://localhost:3010"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 10
    rate_limit_period: int = 60

    # Validation
    blocked_sql_keywords: List[str] = ["DROP", "DELETE", "UPDATE", "INSERT"]

    class Config:
        env_file = ".env"
```

**Middleware Stack:**

```python
# app/api/middleware.py
def setup_middleware(app: FastAPI):
    """Configure all middleware"""

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"]
    )

    # Request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        return response

    # Rate limiting (SlowAPI)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**Testing:**
- Unit tests with pytest
- Integration tests for API endpoints
- Database fixture with rollback
- Mock OpenAI responses
- Coverage reporting with pytest-cov

### Database (PostGIS)

**Container:** `postgis/postgis:15-3.3`

**Initialization Scripts (executed in order):**
1. `01-init-schema.sql` - Creates tables (cafes, parks, roads) and spatial indexes
2. `02-load-sample-data.sql` - Loads sample data (Tel Aviv locations)
3. `03-create-plans-table.sql` - Creates plans table for Israeli planning data
4. `04-import-plans-data.py` - Python script to import planning data from JSON

**Coordinate System:**
- **SRID 4326** (WGS84) - Standard GPS coordinates
- Longitude/Latitude pairs
- Example: `(34.7818, 32.0853)` = Tel Aviv
- All geometries use this projection for consistency

**Spatial Indexes:**
```sql
-- Cafes spatial index
CREATE INDEX idx_cafes_geom ON cafes USING GIST(geom);

-- Parks spatial index
CREATE INDEX idx_parks_geom ON parks USING GIST(geom);

-- Roads spatial index
CREATE INDEX idx_roads_geom ON roads USING GIST(geom);

-- Plans spatial index + attribute indexes
CREATE INDEX idx_plans_geom ON plans USING GIST(geom);
CREATE INDEX idx_plans_number ON plans(pl_number);
CREATE INDEX idx_plans_status ON plans(station_desc);
CREATE INDEX idx_plans_county ON plans(plan_county_name);
CREATE INDEX idx_plans_landuse ON plans(pl_landuse_string);
```
- **GIST:** Generalized Search Tree - optimized for spatial data
- Speeds up spatial queries by 10-100x
- Enables efficient bounding box queries
- Critical for ST_DWithin, ST_Intersects, ST_Contains

**Geography Casting:**
```sql
-- Accurate distance in meters (slower, uses spherical calculation)
ST_DWithin(geom::geography, geom::geography, 200)

-- Planar distance (faster, less accurate for large distances)
ST_DWithin(geom, geom, 0.002)  -- ~200m in degrees
```
- `geometry` type: planar (fast, inaccurate for distance)
- `geography` type: spherical (accurate, meters)
- Use geography for meter-based calculations
- Automatically accounts for Earth's curvature

**Connection Pooling:**
```python
# SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # Keep 5 connections open
    max_overflow=10,      # Allow 10 additional connections when needed
    pool_timeout=30,      # Wait 30s for connection
    pool_recycle=3600     # Recycle connections after 1 hour
)
```

**Health Check:**
```bash
pg_isready -U geouser -d geospatial
# Runs every 10 seconds
# 5 retries before marking unhealthy
# 30 second startup period
```

## 🎯 Design Decisions

### Architecture Patterns

**1. Service Layer Pattern**
- Separates business logic from API routes
- Enables easier testing with mocked services
- Allows service reuse across different endpoints
- Implements singleton pattern for service instances

**2. Dependency Injection**
- Settings injected via Pydantic
- Services accessed via getter functions
- Enables easy mocking in tests
- Cleaner code with explicit dependencies

**3. Modular Frontend**
- Component-based architecture (React)
- Separation of concerns (components/hooks/services)
- Context API for global state
- Custom hooks for reusable logic

### Technology Choices

**Why React + TypeScript over Vanilla JS?**
- **Type Safety** - Catch errors at compile time
- **Better DX** - Autocomplete, refactoring support
- **Component Reusability** - Modular architecture
- **State Management** - Built-in Context API
- **Testing** - Easier to test components
- **Ecosystem** - Rich library ecosystem

**Trade-off:** Larger bundle size, build complexity

**Why GPT-4 over GPT-3.5?**
- **Better SQL accuracy** - Fewer syntax errors (~90% vs ~70%)
- **Complex query understanding** - Handles ambiguous questions
- **Schema reasoning** - Better understanding of table relationships
- **PostGIS functions** - More accurate spatial query generation

**Trade-off:** Cost (~10x more) but worth it for production quality

**Why FastAPI over Flask/Django?**
- **Async support** - Native async/await for I/O-bound tasks
- **Auto API docs** - Swagger UI + ReDoc out of the box
- **Type safety** - Pydantic validation with type hints
- **Modern Python** - Uses latest Python features (3.11+)
- **Performance** - Comparable to Node.js/Go
- **Developer experience** - Fast development with auto-reload

**Trade-off:** Less mature ecosystem than Django

**Why React-Leaflet over Mapbox/Google Maps?**
- **Open source** - No API keys or billing required
- **Lightweight** - Smaller bundle size (~40KB vs ~200KB)
- **Flexible** - Full control over map behavior
- **Free tiles** - OpenStreetMap tiles are free
- **Privacy** - No tracking or data collection
- **React integration** - First-class React components

**Trade-off:** Less features (no 3D, limited styling), but sufficient for POC

**Why Docker Compose over Kubernetes?**
- **Simplicity** - Single YAML file for all services
- **Local development** - Easy to run locally
- **Reproducible** - Same environment everywhere
- **No orchestration overhead** - For 3 services, K8s is overkill
- **Fast iteration** - Quick rebuild and restart

**Trade-off:** Not suitable for large-scale production (use K8s for that)

**Why PostGIS over MongoDB Geo or MySQL Spatial?**
- **Industry standard** - Used by OpenStreetMap, ESRI, etc.
- **Powerful** - 300+ spatial functions vs ~20 in MySQL
- **Performant** - Optimized R-Tree indexes
- **SQL** - Familiar query language
- **Mature** - 20+ years of development
- **Documentation** - Extensive docs and community

**Trade-off:** More complex setup than MongoDB, but much more powerful

**Why SlowAPI for Rate Limiting?**
- **Simple** - Decorator-based API
- **Flexible** - Per-endpoint configuration
- **Storage** - In-memory or Redis
- **Compatible** - Works seamlessly with FastAPI

**Why Pydantic Settings?**
- **Type validation** - Automatic type checking
- **Environment variables** - Auto-loading from .env
- **Default values** - Fallback configuration
- **IDE support** - Autocomplete for settings
- **Documentation** - Settings are self-documenting

## 🔐 Security Considerations

### Current Implementation (Production-Ready Features)

✅ **Security features implemented:**
- ✅ **SQL validation** - Blocks DROP, DELETE, UPDATE, INSERT, etc.
- ✅ **Rate limiting** - 10 requests per 60 seconds per IP
- ✅ **Input validation** - Pydantic models with constraints
- ✅ **CORS configuration** - Configurable allowed origins
- ✅ **Request logging** - All requests logged with IP and timestamp
- ✅ **Error handling** - No stack traces in production
- ✅ **Health checks** - Database connection validation

### Security Layers

**1. SQL Validation (app/services/database.py)**
```python
BLOCKED_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
                    "CREATE", "TRUNCATE", "GRANT", "REVOKE"]

def validate_sql(self, sql: str) -> Tuple[bool, Optional[str]]:
    """Prevent destructive SQL commands"""
    sql_upper = sql.upper()
    for keyword in self.settings.blocked_sql_keywords:
        if keyword in sql_upper:
            return False, f"Blocked keyword: {keyword}"
    return True, None
```

**2. Rate Limiting (SlowAPI)**
```python
@router.post("/query")
@limiter.limit("10/60second")  # 10 requests per minute
async def execute_query(request: Request, query_request: QueryRequest):
    ...
```

**3. Input Validation (Pydantic)**
```python
class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Natural language question"
    )
```

**4. CORS Configuration**
```python
# Configurable via environment variable
CORS_ORIGINS=http://localhost:3000,http://localhost:3010,https://yourdomain.com

# In middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limited methods
    allow_headers=["*"]
)
```

**5. Secrets Management**
- Environment variables via .env file
- .env file in .gitignore (never committed)
- OpenAI API key never exposed to frontend
- Database credentials in environment only

### Remaining Vulnerabilities (⚠️ For Production)

**Authentication/Authorization:**
- ❌ No user authentication
- ❌ No API key validation
- ❌ No role-based access control (RBAC)

**Recommended implementation:**
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@router.post("/query", dependencies=[Depends(verify_api_key)])
async def execute_query(...):
    ...
```

**Advanced SQL Injection:**
- ✅ Blocked keywords implemented
- ⚠️ Could still have complex injection patterns
- 📝 Recommendation: Use SQL parser (sqlparse) for deeper validation

**DDoS Protection:**
- ✅ Basic rate limiting (10 req/min)
- ⚠️ No distributed rate limiting
- 📝 Recommendation: Use Redis for distributed rate limiting

**Secret Rotation:**
- ⚠️ No automatic secret rotation
- 📝 Recommendation: AWS Secrets Manager or HashiCorp Vault

**Logging & Monitoring:**
- ✅ Request logging implemented
- ⚠️ No centralized log aggregation
- 📝 Recommendation: ELK stack or CloudWatch for production

## 🐳 Docker Compose Architecture

### Service Configuration

**1. PostGIS Database Service**
```yaml
postgis:
  image: postgis/postgis:15-3.3
  container_name: geo-sql-postgis
  restart: unless-stopped

  environment:
    POSTGRES_DB: geospatial
    POSTGRES_USER: geouser
    POSTGRES_PASSWORD: geopass
    POSTGRES_SHARED_BUFFERS: 256MB
    POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB

  ports:
    - "5433:5432"  # External:Internal

  volumes:
    - postgis_data:/var/lib/postgresql/data  # Persistent storage
    - ./init-data:/docker-entrypoint-initdb.d:ro  # Init scripts

  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U geouser -d geospatial"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 30s

  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 1G
      reservations:
        cpus: '0.5'
        memory: 512M

  networks:
    - geosql-network
```

**2. FastAPI Backend Service**
```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: geo-sql-backend
  restart: unless-stopped

  ports:
    - "8000:8000"

  environment:
    DATABASE_URL: postgresql://geouser:geopass@postgis:5432/geospatial
    OPENAI_API_KEY: ${OPENAI_API_KEY}
    ENVIRONMENT: ${ENVIRONMENT:-production}
    DEBUG: ${DEBUG:-false}

  depends_on:
    postgis:
      condition: service_healthy  # Wait for DB to be ready

  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3

  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 512M

  networks:
    - geosql-network
```

**3. React Frontend Services (Profiles)**

**Development Profile:**
```yaml
frontend-dev:
  build:
    context: ./frontend-react
    dockerfile: Dockerfile.dev
  ports:
    - "3000:3000"
  environment:
    - REACT_APP_API_URL=http://localhost:8000
    - CHOKIDAR_USEPOLLING=true  # Hot reload in Docker
  volumes:
    - ./frontend-react:/app
    - /app/node_modules  # Anonymous volume for node_modules
  profiles:
    - development  # Only starts with --profile development
```

**Production Profile:**
```yaml
frontend-prod:
  build:
    context: ./frontend-react
    dockerfile: Dockerfile.prod  # Multi-stage build
  ports:
    - "3010:80"
  profiles:
    - production  # Only starts with --profile production
```

### Docker Profiles Usage

```bash
# Development mode (hot reload, source maps)
docker-compose --profile development up -d

# Production mode (optimized build, Nginx)
docker-compose --profile production up -d

# Without frontend (API only)
docker-compose up -d postgis backend
```

### Networking

```yaml
networks:
  geosql-network:
    driver: bridge
    name: geosql-network
```

**Benefits:**
- Service isolation
- Internal DNS (services can communicate by name)
- No port conflicts with host
- Easy to add services (e.g., Redis for caching)

### Volumes

```yaml
volumes:
  postgis_data:
    name: geosql_postgis_data
```

**Persistence:**
- Database data survives container restarts
- Can be backed up: `docker run --rm -v geosql_postgis_data:/data -v $(pwd):/backup ubuntu tar czf /backup/db-backup.tar.gz /data`

### Health Checks & Dependencies

**Service Startup Order:**
```
1. PostGIS starts
   └─→ Health check: pg_isready
       └─→ Becomes healthy after ~30s

2. Backend starts (waits for PostGIS)
   └─→ depends_on: postgis (condition: service_healthy)
   └─→ Health check: curl /health
       └─→ Becomes healthy after ~10s

3. Frontend starts (waits for Backend)
   └─→ depends_on: backend (condition: service_healthy)
   └─→ No health check needed (static files)
```

**Benefits:**
- No "connection refused" errors
- Clean startup sequence
- Automatic retries on failure

### Resource Limits

**Why set resource limits?**
- Prevent one service from consuming all resources
- Predictable performance
- Better for running on shared infrastructure
- Easier to plan capacity

**Current limits:**
- **PostGIS:** 2 CPUs, 1GB RAM (database needs more memory)
- **Backend:** 1 CPU, 512MB RAM (Python + FastAPI)
- **Frontend:** 0.5 CPU, 128MB RAM (just Nginx serving static files)

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

### Current (Development + Production)

**Local Development:**
```
┌────────────────────────────────────────────────────┐
│              Docker Host (localhost)               │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │ Frontend-Dev │  │   Backend    │  │ PostGIS │ │
│  │ React + Vite │  │   FastAPI    │  │ 15-3.3  │ │
│  │ :3000        │  │   :8000      │  │ :5433   │ │
│  │ Hot Reload   │  │              │  │         │ │
│  └──────┬───────┘  └──────┬───────┘  └────┬────┘ │
│         │                 │                │      │
│         └────────┬────────┴────────────────┘      │
│                  │                                 │
│            geosql-network                          │
│         (Docker Bridge Network)                    │
└────────────────────────────────────────────────────┘
```

**Production (Docker Compose):**
```
┌────────────────────────────────────────────────────┐
│              Docker Host (Server)                  │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │Frontend-Prod │  │   Backend    │  │ PostGIS │ │
│  │ Nginx        │  │   FastAPI    │  │ 15-3.3  │ │
│  │ Optimized    │  │   Uvicorn    │  │         │ │
│  │ :3010        │  │   :8000      │  │ :5433   │ │
│  └──────┬───────┘  └──────┬───────┘  └────┬────┘ │
│         │                 │                │      │
│         └────────┬────────┴────────────────┘      │
│                  │                                 │
│   Health Checks + Resource Limits + Restart       │
│            geosql-network                          │
└────────────────────────────────────────────────────┘
```

### Cloud Production (Suggested for Scale)

**AWS Architecture:**
```
┌─────────────────────────────────────────────────────┐
│                  CloudFront CDN                     │
│           (Static Assets + Caching)                 │
└────────────┬────────────────────────────────────────┘
             │
        ┌────▼────┐
        │   S3    │ (React Build - Static Files)
        └─────────┘

┌─────────────────────────────────────────────────────┐
│              Application Load Balancer              │
│                (HTTPS Termination)                  │
└───────┬─────────────────────────────────────────────┘
        │
   ┌────▼────┐
   │   API   │
   │ Gateway │ (Rate Limiting, API Keys)
   └────┬────┘
        │
┌───────▼──────────────────────────────────────────────┐
│                    ECS Fargate                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Backend  │  │ Backend  │  │ Backend  │          │
│  │ Task 1   │  │ Task 2   │  │ Task 3   │          │
│  │ (FastAPI)│  │ (FastAPI)│  │ (FastAPI)│          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       └─────────────┼─────────────┘                 │
│                     │                                │
│           Auto Scaling Group                         │
└─────────────────────┬────────────────────────────────┘
                      │
            ┌─────────▼─────────┐
            │   RDS PostGIS     │
            │   Multi-AZ        │
            │   Read Replicas   │
            └───────────────────┘

┌─────────────────────────────────────────────────────┐
│              Supporting Services                    │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ ElastiCache  │  │  Secrets     │               │
│  │ (Redis)      │  │  Manager     │               │
│  │ Rate Limit   │  │  API Keys    │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ CloudWatch   │  │    WAF       │               │
│  │ Logs/Metrics │  │  DDoS Protect│               │
│  └──────────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────┘
```

**Cost Estimates (AWS us-east-1):**

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| ECS Fargate (3 tasks) | 0.5 vCPU, 1GB RAM each | ~$30 |
| RDS PostgreSQL + PostGIS | db.t3.medium, Multi-AZ | ~$120 |
| ElastiCache (Redis) | cache.t3.micro | ~$15 |
| S3 + CloudFront | Static hosting + CDN | ~$10 |
| Application Load Balancer | - | ~$20 |
| Secrets Manager | 3 secrets | ~$1 |
| CloudWatch | Logs + Metrics | ~$10 |
| **Total** | | **~$206/month** |

**OpenAI API Costs (separate):**
- GPT-4: ~$0.01-0.03 per query
- 1000 queries/month: ~$20/month

**Total Monthly Cost:** ~$230/month for production-ready infrastructure

---

## 📝 Architecture Evolution Summary

### Major Improvements from v1.0 → v2.0

**Frontend:**
- ✅ Migrated from Vanilla JS → React 18 + TypeScript
- ✅ Added Context API for state management
- ✅ Implemented custom hooks (useQuery)
- ✅ Added Tailwind CSS for styling
- ✅ Created ErrorBoundary for error handling
- ✅ Added component testing with Jest + RTL
- ✅ Separated dev/prod Docker builds

**Backend:**
- ✅ Restructured to modular architecture (services/api/models)
- ✅ Implemented Service Layer pattern (QueryService, OpenAIService, DatabaseService)
- ✅ Added Pydantic Settings for configuration
- ✅ Implemented rate limiting with SlowAPI
- ✅ Added SQL validation (blocked keywords)
- ✅ Comprehensive error handling
- ✅ Health checks for all services
- ✅ Added pytest test suite
- ✅ Logging & monitoring improvements

**Database:**
- ✅ Added plans table (Israeli urban planning data)
- ✅ Multiple indexes for performance (spatial + attribute)
- ✅ Health checks with pg_isready
- ✅ Connection pooling configuration
- ✅ Resource limits in Docker

**Infrastructure:**
- ✅ Docker Compose with profiles (dev/prod)
- ✅ Health check dependencies
- ✅ Resource limits for all services
- ✅ Dedicated network (geosql-network)
- ✅ Persistent volumes for database
- ✅ Environment-based configuration

**Security:**
- ✅ SQL injection prevention (keyword blocking)
- ✅ Rate limiting (10 req/min)
- ✅ Input validation (Pydantic)
- ✅ Configurable CORS
- ✅ Request logging
- ✅ Secret management via .env

### Key Architecture Patterns

1. **Three-Tier Architecture**: Clear separation between Frontend, Backend, Database
2. **Service Layer Pattern**: Business logic separated from API routes
3. **Singleton Pattern**: Service instances shared across requests
4. **Dependency Injection**: Settings and services injected via getters
5. **Container Orchestration**: Docker Compose with health checks
6. **Type Safety**: TypeScript (frontend) + Pydantic (backend)

### Performance Optimizations

- Connection pooling (5 base + 10 overflow)
- Spatial indexes (GIST) on all geometry columns
- Attribute indexes on commonly queried fields
- Resource limits prevent service starvation
- Geography casting for accurate distance calculations

### Current Capabilities

✅ **Natural Language to SQL**: GPT-4 powered query generation
✅ **Four Spatial Layers**: cafes, parks, roads, plans
✅ **Hebrew + English Support**: Bilingual query interface
✅ **Interactive Map**: Real-time visualization with Leaflet
✅ **Production Ready**: Health checks, logging, error handling
✅ **Docker Deployment**: One command to start all services
✅ **API Documentation**: Auto-generated Swagger UI
✅ **Testing**: Unit + integration tests

### Future Enhancements

**Planned Features:**
- [ ] User authentication (OAuth2/JWT)
- [ ] Query history and favorites
- [ ] Export results (GeoJSON, Shapefile, CSV)
- [ ] Advanced spatial operations (buffers, unions)
- [ ] Raster data support
- [ ] Multi-user collaboration
- [ ] Query caching with Redis
- [ ] WebSocket for real-time updates
- [ ] Mobile responsive design improvements
- [ ] Internationalization (i18n) for more languages

**Infrastructure:**
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Terraform for AWS deployment
- [ ] Monitoring dashboards (Grafana)
- [ ] Log aggregation (ELK stack)
- [ ] Performance benchmarking suite

---

## 📚 Further Reading

### Documentation
- [PostGIS Documentation](https://postgis.net/documentation/) - Spatial database extension
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React TypeScript Docs](https://react-typescript-cheatsheet.netlify.app/) - React + TS guide
- [Leaflet Tutorials](https://leafletjs.com/examples.html) - Interactive maps
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - GPT-4 API
- [Docker Compose Docs](https://docs.docker.com/compose/) - Container orchestration
- [Pydantic Docs](https://docs.pydantic.dev/) - Data validation

### Related Projects
- [OpenStreetMap](https://www.openstreetmap.org/) - Free map data source
- [Israeli Planning Administration](https://www.gov.il/he/departments/planning_administration) - Planning data source
- [GeoServer](http://geoserver.org/) - Open source geospatial server
- [QGIS](https://qgis.org/) - Desktop GIS application

### Architecture References
- [The Twelve-Factor App](https://12factor.net/) - Modern app architecture
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [API Design Patterns](https://cloud.google.com/apis/design) - Google Cloud

---

## 🙋‍♂️ Support & Contact

**Questions about the architecture?**
- 📖 Check the [README.md](README.md) for quick start
- 🐛 Found a bug? Open an [issue](https://github.com/yourusername/geo-sql-agent/issues)
- 💡 Have suggestions? Start a [discussion](https://github.com/yourusername/geo-sql-agent/discussions)
- 📧 Contact: your.email@example.com

**Built with ❤️ to showcase the power of AI + GIS integration**

---

*Last Updated: 2024-01*
*Architecture Version: 2.0*
*Document Maintainer: Your Name*
