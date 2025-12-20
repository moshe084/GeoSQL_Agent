# 🚀 Quick Start Guide - Geo-SQL Agent

> **Turn natural language into SQL queries in 3 steps**

---

## What does it do?

Ask questions in plain English (or Hebrew) → Get SQL queries + Map visualizations

**Example:**
- You ask: *"Find cafes near parks"*
- AI generates: `SELECT c.id, c.name FROM cafes c, parks p WHERE ST_DWithin(...)`
- You see: Results on a map 🗺️

---

## 1️⃣ Install (5 minutes)

### Requirements:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [OpenAI API Key](https://platform.openai.com/api-keys) (~$0.01/query)

### Steps:

```bash
# Clone the repo
git clone https://github.com/moshe084/MasterRepo.git
cd MasterRepo

# Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Start everything
docker-compose up -d
```

**That's it!** Open http://localhost:3010

---

## 2️⃣ Use It

### Try these queries:

| Query | What happens |
|-------|--------------|
| `Show me all cafes` | Lists all cafes on map |
| `Find cafes within 200m of the largest park` | Spatial search |
| `Which park has the most cafes nearby?` | Analysis query |
| `הצג את כל בתי הקפה` | Works in Hebrew too! |

---

## 3️⃣ See What's Happening

### Backend logs (Terminal):
```bash
docker-compose logs -f backend
```

You'll see:
```
🔵 NEW QUERY REQUEST
📝 Question: Show me all cafes
🤖 Sending to OpenAI GPT-4...
✅ Generated SQL: SELECT id, name...
🗄️ Executing on PostGIS database...
🟢 COMPLETED - 15 results in 1.2s
```

### Frontend logs (Browser):
1. Press **F12** (Developer Tools)
2. Go to **Console** tab
3. See real-time logs

---

## 🛠️ Common Commands

| Command | What it does |
|---------|--------------|
| `docker-compose up -d` | Start the system |
| `docker-compose down` | Stop the system |
| `docker-compose ps` | Check status |
| `docker-compose logs -f backend` | View backend logs |
| `docker-compose restart` | Restart everything |

---

## 🐛 Troubleshooting

### ❌ "Port 5432 already allocated"
**Fix:** Change port in `docker-compose.yml` to `5433:5432`

### ❌ "OpenAI API key not found"
**Fix:** Create `.env` file with `OPENAI_API_KEY=sk-...` and restart:
```bash
docker-compose restart backend
```

### ❌ "Query failed: Sorry, database doesn't contain..."
**Fix:** You asked about data that doesn't exist. Only available:
- ✅ `cafes` (coffee shops)
- ✅ `parks` (parks)
- ✅ `roads` (streets)

### ❌ Map doesn't load
**Fix:** Hard refresh browser (Ctrl+Shift+R)

---

## 📊 What's in the Database?

**Tel Aviv sample data:**
- 15 cafes (Aroma, Landwer, etc.)
- 7 parks (Yarkon Park, Meir Garden, etc.)
- 6 roads (Dizengoff, Rothschild, etc.)

---

## 🎯 How It Works

```
You: "Find cafes near parks"
  ↓
Frontend sends to Backend (http://localhost:8000/query)
  ↓
Backend sends to OpenAI GPT-4:
  "Convert this to PostGIS SQL using tables: cafes, parks, roads"
  ↓
GPT-4 returns:
  "SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
   FROM cafes c, parks p
   WHERE ST_DWithin(c.geom::geography, p.geom::geography, 200)"
  ↓
Backend executes SQL on PostGIS database
  ↓
Results returned to Frontend
  ↓
Frontend draws points on Leaflet map
  ↓
You see: Map + SQL + Statistics
```

---

## 📚 Architecture

| Component | Technology | Port | Purpose |
|-----------|------------|------|---------|
| Frontend | HTML + Leaflet.js | 3010 | User interface + map |
| Backend | FastAPI + Python | 8000 | AI integration + SQL execution |
| Database | PostgreSQL + PostGIS | 5433 | Spatial data storage |

---

## 🔐 Security Warning

⚠️ **This is a POC (Proof of Concept) - NOT production-ready!**

**Issues:**
- No authentication
- No SQL injection protection
- CORS wide open
- API keys in plain text

**Before production:**
- Add JWT authentication
- Add rate limiting
- Validate SQL queries
- Use secrets manager

---

## 💡 Example Questions to Try

### 🟢 Simple
- Show me all cafes
- Show all parks
- List all roads

### 🟡 Spatial
- Find cafes within 200 meters of the largest park
- What is the closest cafe to the smallest park?
- Show roads that intersect with parks

### 🔴 Advanced
- Which park has the most cafes within 300 meters?
- Count how many cafes are within 500m of each park
- Find cafes that are near parks but not near roads

### 🇮🇱 Hebrew
- הצג את כל בתי הקפה
- מצא פארקים גדולים מ-5000 מטר רבוע
- איזה פארק יש הכי הרבה בתי קפה בקרבתו

---

## 🎓 Learn More

- **Full Documentation:** See [USAGE_GUIDE.md](USAGE_GUIDE.md) (Hebrew)
- **Architecture Details:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Example Queries:** See [QUERIES.md](QUERIES.md)
- **PostGIS Functions:** https://postgis.net/docs/reference.html
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

## 📝 Quick Reference Card

### URLs
- Frontend: http://localhost:3010
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Key Files
- `backend/main.py` - Backend logic + AI integration
- `frontend/index.html` - User interface
- `docker-compose.yml` - Service orchestration
- `.env` - OpenAI API key (create this!)

### Useful Docker Commands
```bash
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose ps             # Status
docker-compose logs -f        # All logs
docker-compose logs -f backend # Backend only
docker-compose restart        # Restart all
docker-compose down -v        # Full reset
```

---

## ✅ Checklist - Is Everything Working?

- [ ] Docker Desktop is running
- [ ] Created `.env` file with OpenAI API key
- [ ] Ran `docker-compose up -d`
- [ ] All 3 containers show "Up" in `docker-compose ps`
- [ ] http://localhost:3010 loads in browser
- [ ] http://localhost:8000/health returns `{"status":"healthy"}`
- [ ] Can execute query "Show me all cafes"
- [ ] See results on map
- [ ] Logs show in terminal and browser console

**If all ✅ → You're ready!**

---

## 🆘 Need Help?

1. **Check logs:** `docker-compose logs -f backend`
2. **Check health:** `curl http://localhost:8000/health`
3. **Browser console:** Press F12, check Console tab
4. **Full restart:** `docker-compose down && docker-compose up -d`
5. **Still stuck?** Open an issue: https://github.com/moshe084/MasterRepo/issues

---

## 🎉 Success Example

**Input:**
```
Find cafes within 200 meters of the largest park
```

**Output:**

**Generated SQL:**
```sql
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c, parks p
WHERE p.area = (SELECT MAX(area) FROM parks)
AND ST_DWithin(c.geom::geography, p.geom::geography, 200);
```

**Results:** 3 cafes found in 1.2 seconds

**Map:** Shows 3 blue markers on Tel Aviv map

---

**That's it! Start asking questions and watch the magic happen! ✨**
