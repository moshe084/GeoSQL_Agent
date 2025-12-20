# 🤝 Contributing to Geo-SQL Agent

Thank you for your interest in contributing! This project is designed to showcase AI + GIS integration, and we welcome improvements.

## 🎯 Project Goals

1. **Educational:** Demonstrate LLM integration with spatial databases
2. **Practical:** Solve real GIS developer pain points
3. **Portfolio-worthy:** Showcase full-stack development skills
4. **Open Source:** Help the GIS community

## 🚀 How to Contribute

### 1. Report Issues

Found a bug or have a feature idea?

- Check existing issues first
- Use issue templates
- Include:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment (OS, Docker version, etc.)
  - Screenshots/logs if applicable

### 2. Suggest Features

Have an idea for improvement?

**Before opening an issue:**
- Is it aligned with project goals?
- Would it help GIS developers?
- Is it technically feasible?

**Good feature requests include:**
- Clear use case description
- Example queries or scenarios
- Potential implementation approach

### 3. Submit Pull Requests

**Process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and open a PR

**PR Guidelines:**
- Link to related issue
- Describe what changed and why
- Include screenshots for UI changes
- Add tests if applicable
- Update documentation

## 🏗️ Development Setup

### Prerequisites

```bash
# Install dependencies
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js (optional, for frontend tooling)
- OpenAI API key
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run locally (without Docker)
export DATABASE_URL=postgresql://geouser:geopass@localhost:5432/geospatial
export OPENAI_API_KEY=sk-your-key
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend

# Serve locally
python -m http.server 3010
# Or use Live Server extension in VS Code
```

**Database:**
```bash
# Start only PostGIS
docker-compose up postgis
```

### Testing

**Manual Testing:**
1. Start all services: `./run.sh`
2. Open http://localhost:3010
3. Try queries from `QUERIES.md`
4. Check logs: `docker-compose logs -f`

**Automated Testing (TODO):**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📋 Contribution Ideas

### 🟢 Beginner-Friendly

- [ ] Add more example queries to `QUERIES.md`
- [ ] Improve error messages
- [ ] Add loading animations
- [ ] Create additional sample datasets (other cities)
- [ ] Write blog post about using the tool
- [ ] Fix typos in documentation
- [ ] Add comments to code
- [ ] Create video tutorial

### 🟡 Intermediate

- [ ] Add query history (localStorage)
- [ ] Implement query favorites
- [ ] Add export to GeoJSON/CSV
- [ ] Support for additional PostGIS functions:
  - [ ] ST_Buffer
  - [ ] ST_Union
  - [ ] ST_ConvexHull
  - [ ] ST_Centroid
- [ ] Dark mode toggle
- [ ] Responsive mobile layout
- [ ] Add map layer controls (toggle cafes/parks/roads)
- [ ] Implement query auto-complete
- [ ] Add unit tests for backend
- [ ] Create Docker development compose file
- [ ] Add GitHub Actions CI/CD

### 🔴 Advanced

- [ ] Multi-language support (i18n)
- [ ] Voice input for queries
- [ ] Query result comparison (A/B testing)
- [ ] Advanced visualizations:
  - [ ] Heatmaps
  - [ ] Clustering
  - [ ] 3D buildings
- [ ] Raster data support
- [ ] Real-time collaboration (WebSockets)
- [ ] Query performance optimization
- [ ] Caching layer (Redis)
- [ ] LLM fine-tuning for better SQL
- [ ] Support for other databases (MongoDB, MySQL)
- [ ] Plugin system for custom functions
- [ ] Admin panel for data management

## 🛠️ Code Style

### Python (Backend)

**Follow PEP 8:**
```python
# Good
def execute_query(request: QueryRequest) -> QueryResponse:
    """Execute natural language query and return results."""
    sql_query = generate_sql(request.question)
    results = run_query(sql_query)
    return QueryResponse(sql=sql_query, results=results)

# Bad
def exec_q(req):
    sql=gen_sql(req.q)
    return run(sql)
```

**Type hints everywhere:**
```python
from typing import List, Dict, Any

def parse_results(rows: List[tuple]) -> List[Dict[str, Any]]:
    ...
```

**Docstrings for public functions:**
```python
def generate_sql(question: str) -> str:
    """
    Generate PostGIS SQL query from natural language.

    Args:
        question: User's question in natural language

    Returns:
        Valid PostGIS SQL query as string

    Raises:
        ValueError: If question is empty or invalid
    """
    ...
```

### JavaScript (Frontend)

**Use modern ES6+:**
```javascript
// Good
const executeQuery = async (question) => {
    const response = await fetch(API_URL, {
        method: 'POST',
        body: JSON.stringify({ question })
    });
    return await response.json();
};

// Bad
function executeQuery(question) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', API_URL);
    ...
}
```

**Comments for complex logic:**
```javascript
// Parse GeoJSON from string or object
const geojson = typeof result.geojson === 'string'
    ? JSON.parse(result.geojson)  // From database
    : result.geojson;              // Already parsed
```

### SQL

**Consistent formatting:**
```sql
-- Good
SELECT
    c.id,
    c.name,
    ST_AsGeoJSON(c.geom) as geojson
FROM cafes c
WHERE c.name LIKE '%Coffee%'
ORDER BY c.id;

-- Bad
select c.id,c.name,ST_AsGeoJSON(c.geom) as geojson from cafes c where c.name like '%Coffee%' order by c.id;
```

## 🧪 Testing Checklist

Before submitting a PR, verify:

- [ ] All services start: `./run.sh`
- [ ] Frontend loads at http://localhost:3010
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Basic query works: "Show me all cafes"
- [ ] Spatial query works: "Find cafes within 200m of largest park"
- [ ] Map displays results correctly
- [ ] SQL appears in console
- [ ] No console errors in browser
- [ ] No errors in backend logs
- [ ] Database has expected data counts
- [ ] Works on clean Docker environment
- [ ] Documentation updated if needed
- [ ] Code follows style guidelines

## 📝 Commit Message Format

Use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**

```
feat(backend): add query caching with Redis

Implemented LRU cache for generated SQL queries to reduce
OpenAI API calls and improve response times.

- Added Redis dependency
- Created cache decorator
- Set TTL to 1 hour
- Updated documentation

Closes #42
```

```
fix(frontend): handle empty query results gracefully

Previously, empty results caused map.fitBounds() to error.
Now shows user-friendly message when no results found.

Fixes #38
```

```
docs(readme): add troubleshooting section

Added common issues and solutions for:
- Database connection failures
- OpenAI API errors
- Port conflicts
```

## 🏆 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in blog posts/videos
- Given contributor badge

## 📚 Resources

### Learning Materials

**PostGIS:**
- [PostGIS Official Docs](https://postgis.net/documentation/)
- [PostGIS Workshop](https://postgis.net/workshops/postgis-intro/)
- [Spatial SQL Cookbook](https://postgis.net/docs/PostGIS_Special_Functions_Index.html)

**FastAPI:**
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Leaflet:**
- [Leaflet Quick Start](https://leafletjs.com/examples/quick-start/)
- [Leaflet Plugins](https://leafletjs.com/plugins.html)

**OpenAI:**
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### Inspiration Projects

- [pgvector](https://github.com/pgvector/pgvector) - Postgres vector similarity search
- [LangChain](https://github.com/langchain-ai/langchain) - LLM application framework
- [GeoServer](https://github.com/geoserver/geoserver) - OGC standard server
- [Mapbox GL JS](https://github.com/mapbox/mapbox-gl-js) - Vector tile mapping

## ❓ Questions?

- Open a [Discussion](https://github.com/your-repo/discussions)
- Ask in issues with `question` label
- Check existing docs first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Geo-SQL Agent better!** 🌍🚀

---

## 🎯 Current Priority Areas

*Updated: December 2024*

1. **Testing:** Add comprehensive test coverage
2. **Performance:** Implement query caching
3. **Documentation:** Create video tutorials
4. **Features:** Add more PostGIS functions
5. **UX:** Improve error handling and feedback

Check the [Issues](https://github.com/your-repo/issues) page for specific tasks!
