# 🔄 Geo-SQL Agent - Visual Workflow

> **See exactly what happens when you ask a question**

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         👤 USER                                     │
│                   (Web Browser)                                     │
│                                                                     │
│  Types: "Find cafes within 200m of the largest park"               │
│  Clicks: [Execute Query] button                                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP POST Request
                             │ {question: "Find cafes..."}
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🌐 FRONTEND LAYER                                │
│                 (Nginx serving index.html)                          │
│                   Port: http://localhost:3010                       │
│                                                                     │
│  📝 Step 1: Validate input                                          │
│     - Check question is not empty                                  │
│     - Show loading spinner                                         │
│     - Clear previous results from map                              │
│                                                                     │
│  🔄 Step 2: Send to backend                                         │
│     fetch('http://localhost:8000/query', {                         │
│       method: 'POST',                                              │
│       body: JSON.stringify({question: "Find cafes..."})           │
│     })                                                             │
│                                                                     │
│  Console Log:                                                       │
│  🔵 FRONTEND: New Query Request                                    │
│  📝 Question: "Find cafes within 200m..."                          │
│  🌐 STEP 1: Sending POST request                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ POST /query
                             │ Content-Type: application/json
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 BACKEND LAYER                                 │
│                   (FastAPI Python Server)                           │
│                   Port: http://localhost:8000                       │
│                                                                     │
│  📥 Step 1: Receive request                                         │
│     @app.post("/query")                                            │
│     async def execute_query(request: QueryRequest)                 │
│                                                                     │
│  Console Log:                                                       │
│  ════════════════════════════════════════════                      │
│  🔵 NEW QUERY REQUEST                                              │
│  📝 Question: Find cafes within 200m of the largest park           │
│  ════════════════════════════════════════════                      │
│                                                                     │
│  🤖 Step 2: Prepare AI prompt                                       │
│     System Prompt:                                                 │
│     "You are a PostGIS SQL expert.                                 │
│      Database Schema:                                              │
│      - cafes (id, name, geom, address)                            │
│      - parks (id, name, geom, area)                               │
│      - roads (id, name, geom, road_type)                          │
│                                                                     │
│      PostGIS Functions:                                            │
│      - ST_DWithin(geom1, geom2, distance)                         │
│      - ST_AsGeoJSON(geom)                                         │
│      - Geography cast: geom::geography"                           │
│                                                                     │
│  Console Log:                                                       │
│  🤖 STEP 1: Sending question to OpenAI GPT-4...                    │
│     Model: gpt-4                                                   │
│     Temperature: 0                                                 │
│     Max Tokens: 500                                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ API Call
                             │ POST https://api.openai.com/v1/chat/completions
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🧠 OPENAI GPT-4                                  │
│                   (Cloud AI Service)                                │
│                                                                     │
│  🧪 AI Processing:                                                  │
│     1. Analyzes system prompt (database schema)                    │
│     2. Understands user question                                   │
│     3. Maps "cafes" → cafes table                                 │
│     4. Maps "200m" → ST_DWithin with 200 parameter                │
│     5. Maps "largest park" → MAX(area) subquery                   │
│     6. Generates PostGIS SQL query                                 │
│                                                                     │
│  ⏱️ Processing time: ~1-2 seconds                                   │
│  💰 Cost: ~$0.01                                                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Returns SQL Query
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 BACKEND LAYER (continued)                     │
│                                                                     │
│  ✅ Step 3: Receive SQL from OpenAI                                 │
│                                                                     │
│  Console Log:                                                       │
│  ✅ Received response from OpenAI                                  │
│  📄 Raw SQL Response:                                              │
│  ```sql                                                            │
│  SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson             │
│  FROM cafes c, parks p                                             │
│  WHERE p.area = (SELECT MAX(area) FROM parks)                     │
│  AND ST_DWithin(c.geom::geography, p.geom::geography, 200)        │
│  ```                                                               │
│                                                                     │
│  🔧 Step 4: Clean SQL                                               │
│     - Remove markdown code blocks (```)                            │
│     - Trim whitespace                                              │
│                                                                     │
│  Console Log:                                                       │
│  🔧 Cleaning SQL: Removing ```sql markdown blocks                  │
│  ✨ Final SQL Query:                                               │
│  SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson...          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Execute SQL
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🗄️ DATABASE LAYER                                │
│              (PostgreSQL 15 + PostGIS 3.3)                          │
│                   Port: localhost:5433                              │
│                                                                     │
│  Console Log (Backend):                                             │
│  🗄️  STEP 2: Executing SQL query on PostGIS database...            │
│                                                                     │
│  🔍 Step 1: Parse SQL                                               │
│     PostgreSQL query planner analyzes the SQL                      │
│                                                                     │
│  📊 Step 2: Execute subquery                                        │
│     SELECT MAX(area) FROM parks;                                   │
│     → Returns: 350000 (Yarkon Park is largest)                     │
│                                                                     │
│  🗺️ Step 3: Spatial query                                           │
│     Uses GIST spatial index on cafes.geom                          │
│     Uses GIST spatial index on parks.geom                          │
│                                                                     │
│     For each cafe:                                                 │
│       - Check if distance to Yarkon Park ≤ 200m                   │
│       - Use geography cast for meter-based calculation            │
│       - ST_DWithin returns TRUE/FALSE                             │
│                                                                     │
│  📦 Step 4: Generate GeoJSON                                        │
│     ST_AsGeoJSON converts geometry to:                             │
│     {"type":"Point","coordinates":[34.7818,32.0853]}              │
│                                                                     │
│  ✅ Results:                                                         │
│     Row 1: {id: 3, name: "Aroma Yarkon", geojson: {...}}          │
│     Row 2: {id: 7, name: "Cofix Park", geojson: {...}}            │
│     Row 3: {id: 12, name: "Landwer", geojson: {...}}              │
│                                                                     │
│  ⏱️ Execution time: ~50ms                                           │
│                                                                     │
│  Console Log (Backend):                                             │
│  ✅ Query executed successfully                                    │
│  📊 Columns: ['id', 'name', 'geojson']                             │
│  📈 Rows returned: 3                                               │
│     🗺️  Parsed GeoJSON for row 1                                   │
│     🗺️  Parsed GeoJSON for row 2                                   │
│     🗺️  Parsed GeoJSON for row 3                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Return results
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 BACKEND LAYER (final step)                    │
│                                                                     │
│  📦 Step 5: Format response                                         │
│                                                                     │
│  JSON Response:                                                     │
│  {                                                                 │
│    "sql": "SELECT c.id, c.name...",                               │
│    "results": [                                                    │
│      {                                                             │
│        "id": 3,                                                    │
│        "name": "Aroma Yarkon",                                     │
│        "geojson": {                                                │
│          "type": "Point",                                          │
│          "coordinates": [34.7818, 32.0853]                        │
│        }                                                           │
│      },                                                            │
│      ... (2 more)                                                  │
│    ],                                                              │
│    "execution_time": 1.234                                         │
│  }                                                                 │
│                                                                     │
│  Console Log:                                                       │
│  ════════════════════════════════════════════                      │
│  🟢 QUERY COMPLETED SUCCESSFULLY                                   │
│  ⏱️  Total Execution Time: 1.234s                                  │
│  📊 Total Results: 3                                               │
│  ════════════════════════════════════════════                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP 200 OK
                             │ Content-Type: application/json
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🌐 FRONTEND LAYER (rendering)                    │
│                                                                     │
│  Console Log:                                                       │
│  ✅ STEP 2: Received response from backend                         │
│  📄 Generated SQL: SELECT c.id, c.name...                          │
│  📊 Results count: 3                                               │
│  ⏱️  Execution time: 1.234s                                         │
│                                                                     │
│  🖥️ Step 3: Display SQL                                             │
│     sqlOutput.textContent = data.sql;                              │
│     → Shows SQL in the SQL Console panel                           │
│                                                                     │
│  Console Log:                                                       │
│  🗺️  STEP 3: Rendering results on map...                           │
│                                                                     │
│  🗺️ Step 4: Render on Leaflet map                                  │
│                                                                     │
│     For each result:                                               │
│       Console Log:                                                 │
│       Adding feature 1/3 to map                                    │
│       Type: Point, Coordinates: [34.7818, 32.0853]                │
│                                                                     │
│       1. Parse GeoJSON                                             │
│          {type: "Point", coordinates: [lng, lat]}                 │
│                                                                     │
│       2. Create Leaflet marker                                     │
│          L.circleMarker([lat, lng], {                             │
│            radius: 8,                                              │
│            fillColor: "#667eea",                                  │
│            color: "#fff"                                           │
│          })                                                        │
│                                                                     │
│       3. Add popup                                                 │
│          Popup content:                                            │
│          "<strong>id:</strong> 3<br>                              │
│           <strong>name:</strong> Aroma Yarkon"                    │
│                                                                     │
│       4. Add to map                                                │
│          layer.addTo(resultsLayer);                               │
│                                                                     │
│  🎯 Step 5: Fit map bounds                                          │
│                                                                     │
│     Console Log:                                                   │
│     🎯 STEP 4: Fitting map bounds to results                       │
│        Bounds: LatLngBounds(...)                                   │
│                                                                     │
│     const bounds = resultsLayer.getBounds();                       │
│     map.fitBounds(bounds, {padding: [50, 50]});                   │
│     → Map zooms to show all 3 markers                              │
│                                                                     │
│  📊 Step 6: Update statistics                                       │
│     resultCount.textContent = "3";                                 │
│     execTime.textContent = "1234ms";                               │
│                                                                     │
│  Console Log:                                                       │
│  ════════════════════════════════════════════                      │
│  🟢 FRONTEND: Query Completed Successfully                         │
│  ════════════════════════════════════════════                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         👤 USER (Result)                            │
│                                                                     │
│  🗺️ Map Display:                                                    │
│     ┌────────────────────────────────────┐                         │
│     │  📍 Aroma Yarkon                   │                         │
│     │  📍 Cofix Park                     │                         │
│     │  📍 Landwer                        │                         │
│     │                                    │                         │
│     │  [OpenStreetMap background]        │                         │
│     └────────────────────────────────────┘                         │
│                                                                     │
│  📄 SQL Console:                                                    │
│     SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson          │
│     FROM cafes c, parks p                                          │
│     WHERE p.area = (SELECT MAX(area) FROM parks)                  │
│     AND ST_DWithin(c.geom::geography, p.geom::geography, 200)     │
│                                                                     │
│  📊 Statistics:                                                     │
│     Results: 3 cafes                                               │
│     Time: 1234ms                                                   │
│                                                                     │
│  ✨ User can now:                                                   │
│     - Click markers to see details                                 │
│     - Zoom/pan the map                                             │
│     - Try another query                                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Time Breakdown

| Step | Component | Time | % of Total |
|------|-----------|------|------------|
| 1. Frontend validation | Browser | ~5ms | 0.4% |
| 2. HTTP request | Network | ~10ms | 0.8% |
| 3. Backend receives | FastAPI | ~5ms | 0.4% |
| **4. OpenAI API call** | **GPT-4** | **~1000ms** | **81%** |
| 5. SQL execution | PostGIS | ~50ms | 4% |
| 6. JSON formatting | Backend | ~5ms | 0.4% |
| 7. HTTP response | Network | ~10ms | 0.8% |
| 8. Map rendering | Leaflet.js | ~150ms | 12% |
| **Total** | **End-to-end** | **~1234ms** | **100%** |

**Bottleneck:** OpenAI API call (80% of time)

---

## 🔍 Detailed Component Interactions

### 1. Frontend → Backend Communication

```javascript
// frontend/index.html
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: "Find cafes within 200m of the largest park"
  })
});

const data = await response.json();
// data = {
//   sql: "SELECT...",
//   results: [...],
//   execution_time: 1.234
// }
```

### 2. Backend → OpenAI Communication

```python
# backend/main.py
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT  # Database schema + PostGIS functions
        },
        {
            "role": "user",
            "content": "Find cafes within 200m of the largest park"
        }
    ],
    temperature=0,  # Deterministic output
    max_tokens=500
)

sql_query = response.choices[0].message.content.strip()
```

### 3. Backend → PostGIS Communication

```python
# backend/main.py
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://geouser:geopass@postgis:5432/geospatial"
)

with engine.connect() as conn:
    result = conn.execute(text(sql_query))
    rows = result.fetchall()
```

### 4. Frontend Map Rendering

```javascript
// frontend/index.html
data.results.forEach(result => {
  const geojson = result.geojson; // {type: "Point", coordinates: [lng, lat]}

  const layer = L.geoJSON(geojson, {
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, {
        radius: 8,
        fillColor: "#667eea"
      });
    }
  });

  layer.bindPopup(`<strong>id:</strong> ${result.id}<br>
                   <strong>name:</strong> ${result.name}`);

  layer.addTo(resultsLayer);
});

map.fitBounds(resultsLayer.getBounds());
```

---

## 🎓 Key Technologies Explained

| Technology | Role | Why This Choice |
|------------|------|-----------------|
| **Leaflet.js** | Map rendering | Lightweight, open-source, no API keys |
| **FastAPI** | Web framework | Async support, auto API docs, type safety |
| **OpenAI GPT-4** | SQL generation | Best accuracy for complex queries |
| **PostGIS** | Spatial database | Industry standard, 300+ GIS functions |
| **SQLAlchemy** | Database ORM | Handles connections, SQL execution |
| **Docker Compose** | Orchestration | Run all 3 services with one command |
| **Nginx** | Static file server | Serve frontend HTML/JS/CSS |

---

## 🔄 Error Flow

What happens when something goes wrong:

```
User asks: "Find airports"  (not in database)
  ↓
Frontend sends to Backend
  ↓
Backend sends to OpenAI
  ↓
GPT-4 responds: "Sorry, database doesn't contain airports table"
  ↓
Backend tries to execute this as SQL
  ↓
PostgreSQL ERROR: syntax error at or near "Sorry"
  ↓
Backend catches exception:
  Console Log:
  🔴 QUERY FAILED
  ❌ Error Type: SyntaxError
  ❌ Error Message: syntax error at or near "Sorry"
  ↓
Backend returns HTTP 500:
  {
    "detail": "Query execution failed: syntax error..."
  }
  ↓
Frontend catches error:
  Console Log:
  🔴 FRONTEND: Query Failed
  ❌ Error: Query execution failed...
  ↓
User sees:
  - Alert popup with error message
  - Red text in SQL console
  - No changes to map
```

---

## 📊 Data Flow Example

**Question:** "Show all parks larger than 5000 square meters"

### Input Data:
```
User input: "Show all parks larger than 5000 square meters"
```

### Transformation 1 (OpenAI):
```sql
SELECT id, name, area, ST_AsGeoJSON(geom) as geojson
FROM parks
WHERE area > 5000;
```

### Transformation 2 (PostGIS):
```
Database returns:
Row 1: id=1, name="Yarkon Park", area=350000, geom=POLYGON(...)
Row 2: id=2, name="Meir Garden", area=45000, geom=POLYGON(...)
Row 3: id=4, name="Independence Park", area=75000, geom=POLYGON(...)
```

### Transformation 3 (ST_AsGeoJSON):
```json
[
  {
    "id": 1,
    "name": "Yarkon Park",
    "area": 350000,
    "geojson": {
      "type": "Polygon",
      "coordinates": [[[34.78, 32.09], [34.82, 32.09], ...]]
    }
  },
  ...
]
```

### Transformation 4 (Frontend):
```
Leaflet map with 3 polygon overlays,
each clickable to show park details
```

---

## 🎯 Summary

**5 Main Steps:**
1. 🌐 **Frontend** validates and sends question
2. 🤖 **Backend** calls OpenAI to generate SQL
3. 🧠 **OpenAI** returns PostGIS SQL query
4. 🗄️ **PostGIS** executes query and returns GeoJSON
5. 🗺️ **Frontend** renders results on Leaflet map

**Total Time:** ~1-2 seconds (mostly OpenAI API)

**Total Cost:** ~$0.01 per query

**Key Feature:** Natural language → Visual map in 2 seconds! 🚀
