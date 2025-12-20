# 🌍 Geo-SQL Agent

**AI-Powered Spatial Query Engine** - Transform natural language questions into PostGIS SQL queries and visualize results on an interactive map.

> "Who said you need to memorize all PostGIS syntax by heart?"

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.3-blue.svg)](https://postgis.net/)

---

## 📚 Documentation

**🚀 First time?** → Start here: **[START_HERE.md](START_HERE.md)** (עברית)

| Document | Description | Language | Time |
|----------|-------------|----------|------|
| **[START_HERE.md](START_HERE.md)** | Just want it running? 4 steps | 🇮🇱 עברית | 5 min |
| **[SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)** | Quick start with examples | 🇬🇧 English | 10 min |
| **[CHEAT_SHEET.md](CHEAT_SHEET.md)** | Quick reference card | 🇬🇧 English | 2 min |
| **[USAGE_GUIDE.md](USAGE_GUIDE.md)** | Complete usage guide | 🇮🇱 עברית | 20 min |
| **[WORKFLOW.md](WORKFLOW.md)** | Visual workflow diagram | 🇬🇧 English | 15 min |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Technical architecture | 🇬🇧 English | 30 min |
| **[QUERIES.md](QUERIES.md)** | Example queries library | 🇬🇧 English | 10 min |

---

## 🎯 The Problem

GIS developers know that spatial SQL is a **nightmare** for those who don't master it. Complex queries involving `ST_DWithin`, `ST_Intersects`, geography casts, and spatial joins can take hours to debug.

## ✨ The Solution

An AI agent that:
- 🧠 **Understands your database schema**
- 🗣️ **Accepts questions in natural language** (English/Hebrew)
- 🎯 **Generates valid PostGIS SQL queries**
- 🗺️ **Visualizes results on an interactive map**
- ⚡ **Returns results in real-time**

## 🏗️ Architecture

```
┌─────────────────┐
│    Frontend     │  Leaflet Map + Query Input
│  (Nginx/HTML)   │
└────────┬────────┘
         │
         │ HTTP/JSON
         │
┌────────▼────────┐
│     Backend     │  FastAPI + OpenAI API
│     (Python)    │  SQL Generation Engine
└────────┬────────┘
         │
         │ SQL Queries
         │
┌────────▼────────┐
│    PostGIS      │  Geospatial Database
│   (PostgreSQL)  │  Points, Polygons, Roads
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### Installation

1. **Clone and setup:**

```bash
git clone <your-repo>
cd MasterRepo
cp .env.example .env
```

2. **Add your OpenAI API key to `.env`:**

```bash
OPENAI_API_KEY=sk-your-actual-api-key
```

3. **Start all services:**

```bash
docker-compose up --build
```

4. **Access the application:**

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📊 Sample Data

The database comes pre-loaded with Tel Aviv data:

- **15 Cafes** - Popular coffee shops around the city
- **7 Parks** - Including Yarkon Park, Meir Park, Independence Park
- **6 Roads** - Main streets and boulevards

## 💡 Example Queries

Try these natural language questions:

1. **"Find all cafes within 200 meters of the largest park"**
   - Tests: Distance queries, aggregation, geography casting

2. **"Show all parks larger than 5000 square meters"**
   - Tests: Area calculations, simple filtering

3. **"What is the closest cafe to the smallest park?"**
   - Tests: Complex spatial joins, distance ordering

4. **"Find cafes near main roads"**
   - Tests: Line-point proximity, type filtering

5. **"Show all roads that intersect with parks"**
   - Tests: Geometric intersections

## 🎬 Demo Workflow

### Input:
```
"Find cafes within 200m of the largest park"
```

### Generated SQL:
```sql
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c, parks p
WHERE p.area = (SELECT MAX(area) FROM parks)
AND ST_DWithin(c.geom::geography, p.geom::geography, 200);
```

### Output:
- **Map:** Red markers showing matching cafes
- **SQL Console:** The generated query
- **Stats:** Result count + execution time

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI API** - GPT-4 for SQL generation
- **SQLAlchemy + GeoAlchemy2** - Database ORM
- **Pydantic** - Data validation

### Database
- **PostgreSQL 15** - Relational database
- **PostGIS 3.3** - Spatial extension

### Frontend
- **Leaflet** - Interactive maps
- **Vanilla JS** - No framework overhead
- **OpenStreetMap** - Base map tiles

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   └── index.html           # Single-page app
├── init-data/
│   ├── 01-init-schema.sql   # Database schema
│   └── 02-load-sample-data.sql  # Sample data
├── docker-compose.yml       # Orchestration
└── README.md
```

## 🔑 Key Features

### 1. Intelligent System Prompt
The AI knows your exact database schema and PostGIS functions:

```python
SYSTEM_PROMPT = """
You are a PostGIS SQL expert...
Table: cafes (id, name, geom, address)
Table: parks (id, name, geom, area)
...
Use ST_DWithin for distance queries
Use geography cast for meter-based calculations
"""
```

### 2. Spatial Indexing
All geometry columns use GIST indexes for fast queries:

```sql
CREATE INDEX idx_cafes_geom ON cafes USING GIST(geom);
```

### 3. Real-time Visualization
Results automatically display on the map with popups showing all attributes.

## 🎓 Educational Value

This project demonstrates:

✅ **Backend Development** - RESTful API design
✅ **AI Integration** - Prompt engineering for code generation
✅ **Geospatial Databases** - PostGIS spatial queries
✅ **Full-stack Integration** - Frontend ↔ Backend ↔ Database
✅ **Docker Orchestration** - Multi-container applications

## 🎥 Perfect for Social Media

### LinkedIn Post Template:

```
🌍 Who said you need to memorize PostGIS syntax?

I built an AI engine that translates natural language
into complex spatial SQL queries.

This isn't just GPT writing code – it's an agent that:
✅ Knows my database schema
✅ Performs spatial joins
✅ Returns geometric results to the map

GIS developers, how much time would this save you?

#GIS #AI #PostGIS #Python #FastAPI
```

### Video Demo (30 seconds):

Split-screen showing:
- **Left:** You typing questions in Hebrew/English
- **Right:** SQL appearing in console + points populating on map

## 🤝 Contributing

Want to extend this? Ideas:

- [ ] Add more spatial functions (buffers, unions, etc.)
- [ ] Support for raster data
- [ ] Multi-language support
- [ ] Query history and favorites
- [ ] Export results to GeoJSON/Shapefile

## 📝 License

MIT License - feel free to use this in your portfolio!

## 🙋‍♂️ Author

Built to showcase the power of AI + GIS integration.

**Questions?** Open an issue or reach out on LinkedIn.

---

⭐ If this helped you understand AI-powered spatial queries, give it a star!
