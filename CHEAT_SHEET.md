# 📋 Geo-SQL Agent - Cheat Sheet

> **Quick reference for common tasks**

---

## 🚀 Getting Started

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

---

## 🌐 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3010 | Ask questions here |
| Backend API | http://localhost:8000 | API endpoint |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| Health Check | http://localhost:8000/health | Check if running |

---

## 💬 Example Questions

### 🟢 Simple (Copy & Paste)

```
Show me all cafes
```

```
Show all parks
```

```
Show all roads
```

### 🟡 Spatial Queries

```
Find cafes within 200 meters of the largest park
```

```
What is the closest cafe to the smallest park?
```

```
Find cafes within 50 meters of main roads
```

```
Show roads that intersect with parks
```

### 🔴 Advanced Analysis

```
Which park has the most cafes within 300 meters?
```

```
Count how many cafes are within 500m of each park
```

```
Find cafes that are near parks but not near roads
```

### 🇮🇱 Hebrew

```
הצג את כל בתי הקפה
```

```
מצא בתי קפה במרחק 200 מטר מהפארק הגדול ביותר
```

```
איזה פארק יש הכי הרבה בתי קפה בקרבתו?
```

---

## 🗄️ Database Schema

### Tables

| Table | Columns | Count | Geometry Type |
|-------|---------|-------|---------------|
| **cafes** | id, name, address, geom | ~15 | Point |
| **parks** | id, name, area, geom | ~7 | Polygon |
| **roads** | id, name, road_type, geom | ~6 | LineString |

### PostGIS Functions (Auto-used by AI)

| Function | Purpose | Example |
|----------|---------|---------|
| `ST_DWithin(a, b, dist)` | Find within distance | Cafes within 200m of parks |
| `ST_Distance(a, b)` | Calculate distance | Distance from cafe to park |
| `ST_Intersects(a, b)` | Check intersection | Roads crossing parks |
| `ST_AsGeoJSON(geom)` | Convert to GeoJSON | For map rendering |
| `geom::geography` | Meter-based calculations | Accurate distances |

---

## 🐛 Troubleshooting

### Problem: "Port already allocated"
```bash
# Edit docker-compose.yml, change:
ports:
  - "5433:5432"  # instead of 5432:5432
```

### Problem: "OpenAI API key not found"
```bash
# Create .env file:
echo "OPENAI_API_KEY=sk-your-key" > .env

# Restart:
docker-compose restart backend
```

### Problem: "Query failed: Sorry, database doesn't..."
**Solution:** Only ask about: cafes, parks, roads

❌ Won't work: hospitals, airports, beaches
✅ Will work: cafes, parks, roads

### Problem: Map not loading
```bash
# Hard refresh browser:
Ctrl + Shift + R  (Windows/Linux)
Cmd + Shift + R   (Mac)
```

### Problem: Want to see what's happening
```bash
# Terminal: Backend logs
docker-compose logs -f backend

# Browser: Frontend logs
F12 → Console tab
```

---

## 🔧 Docker Commands

### Start/Stop
```bash
docker-compose up -d              # Start (detached)
docker-compose down               # Stop
docker-compose restart            # Restart all
docker-compose restart backend    # Restart backend only
```

### Logs
```bash
docker-compose logs -f            # All services
docker-compose logs -f backend    # Backend only
docker-compose logs -f postgis    # Database only
docker-compose logs --tail=50     # Last 50 lines
```

### Status & Debugging
```bash
docker-compose ps                 # Check status
docker exec -it geo-sql-backend bash     # Enter backend container
docker exec -it geo-sql-postgis psql -U geouser -d geospatial  # Enter database
```

### Clean Restart
```bash
docker-compose down -v            # Stop + remove volumes
docker-compose up --build -d      # Rebuild + start
```

---

## 📁 Key Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `.env` | OpenAI API key | First setup |
| `docker-compose.yml` | Service config | Change ports |
| `backend/main.py` | Backend logic | Add features |
| `backend/requirements.txt` | Python packages | Add dependencies |
| `frontend/index.html` | User interface | Change UI |
| `init-data/02-load-sample-data.sql` | Sample data | Add more data |

---

## 🔍 How to Check if Everything Works

### 1. Check Docker containers
```bash
docker-compose ps
```
Expected: All 3 containers "Up"

### 2. Check backend health
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy","database":"connected"}`

### 3. Check frontend
Open: http://localhost:3010
Expected: Map loads

### 4. Try a query
Type: `Show me all cafes`
Expected: See results on map

---

## ⚙️ Configuration

### Change Frontend Port
```yaml
# docker-compose.yml
frontend:
  ports:
    - "3000:80"  # Change 3010 to 3000
```

### Change Backend Port
```yaml
# docker-compose.yml
backend:
  ports:
    - "8001:8000"  # Change 8000 to 8001
```

### Change Database Port
```yaml
# docker-compose.yml
postgis:
  ports:
    - "5433:5432"  # External port (already changed)
```

---

## 📊 Response Format

Every query returns:

```json
{
  "sql": "SELECT id, name, ST_AsGeoJSON(geom)...",
  "results": [
    {
      "id": 1,
      "name": "Aroma",
      "geojson": {
        "type": "Point",
        "coordinates": [34.7818, 32.0853]
      }
    }
  ],
  "execution_time": 1.234
}
```

---

## 💰 Costs

| Service | Cost |
|---------|------|
| Docker | Free |
| Frontend | Free |
| Backend | Free |
| PostGIS | Free |
| OpenAI GPT-4 | ~$0.01/query |

**Total per query:** ~$0.01

---

## 🎯 Quick Debugging Steps

1. **Check logs:**
   ```bash
   docker-compose logs -f backend
   ```

2. **Check browser console:**
   F12 → Console

3. **Test backend directly:**
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"question":"Show me all cafes"}'
   ```

4. **Check database:**
   ```bash
   docker exec -it geo-sql-postgis psql -U geouser -d geospatial -c "SELECT COUNT(*) FROM cafes;"
   ```

5. **Full restart:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

## 📝 SQL Examples (What AI Generates)

### Simple List
```sql
-- "Show me all cafes"
SELECT id, name, address, ST_AsGeoJSON(geom) as geojson
FROM cafes;
```

### Distance Query
```sql
-- "Find cafes within 200m of largest park"
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c, parks p
WHERE p.area = (SELECT MAX(area) FROM parks)
AND ST_DWithin(c.geom::geography, p.geom::geography, 200);
```

### Aggregation
```sql
-- "Count cafes near each park"
SELECT p.id, p.name, COUNT(c.id) as cafe_count
FROM parks p
LEFT JOIN cafes c ON ST_DWithin(p.geom::geography, c.geom::geography, 500)
GROUP BY p.id, p.name;
```

---

## 🔗 Quick Links

- [Simple Guide (English)](SIMPLE_GUIDE.md)
- [Full Guide (Hebrew)](USAGE_GUIDE.md)
- [Visual Workflow](WORKFLOW.md)
- [Architecture](ARCHITECTURE.md)
- [Example Queries](QUERIES.md)
- [PostGIS Docs](https://postgis.net/docs/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Leaflet Docs](https://leafletjs.com/)

---

## 🎓 Learning Path

1. **Day 1:** Follow [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md) - Get it running
2. **Day 2:** Try queries from [QUERIES.md](QUERIES.md)
3. **Day 3:** Read [WORKFLOW.md](WORKFLOW.md) - Understand how it works
4. **Day 4:** Explore [ARCHITECTURE.md](ARCHITECTURE.md) - Deep dive
5. **Day 5:** Add your own data to `init-data/02-load-sample-data.sql`

---

## 🚨 Emergency Commands

### System won't start?
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```

### Database corrupted?
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recreate from scratch
```

### Logs too much?
```bash
# Reduce log verbosity in backend/main.py:
logging.basicConfig(level=logging.WARNING)  # instead of INFO
```

---

**Print this page and keep it next to your keyboard!** 📄
