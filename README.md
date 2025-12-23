# 🌍 Geo-SQL Agent

**AI-Powered Spatial Query Engine** - Transform natural language questions into PostGIS SQL queries and visualize results on an interactive map.

> "Who said you need to memorize all PostGIS syntax by heart?"

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6.svg)](https://www.typescriptlang.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.3-blue.svg)](https://postgis.net/)

[![Backend CI](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/frontend-ci.yml)
[![Docker Build](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/docker-build.yml/badge.svg)](https://github.com/YOUR_USERNAME/geo-sql-agent/actions/workflows/docker-build.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/geo-sql-agent/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/geo-sql-agent)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

</div>

---

## 📸 Screenshots

<!-- Add screenshots here -->
![Query Interface](docs/images/screenshot-query.png)
![Map Results](docs/images/screenshot-map.png)
![SQL Display](docs/images/screenshot-sql.png)

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
- 🔒 **Validates and sanitizes SQL** for security
- 📊 **Tracks query history**

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         Geo-SQL Agent                             │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────┐        ┌─────────────────────┐
│   React Frontend    │        │  FastAPI Backend    │
│   (TypeScript)      │◄──────►│    (Python 3.11)    │
│                     │  HTTP  │                     │
│  • Leaflet Maps     │  JSON  │  • OpenAI GPT-4     │
│  • Tailwind CSS     │        │  • SQL Generation   │
│  • Context API      │        │  • Validation       │
│  • Error Boundaries │        │  • Rate Limiting    │
└─────────────────────┘        └──────────┬──────────┘
                                          │
                                          │ SQL
                                          ▼
                               ┌─────────────────────┐
                               │  PostGIS Database   │
                               │  (PostgreSQL 15)    │
                               │                     │
                               │  • Spatial Queries  │
                               │  • GeoJSON Output   │
                               │  • GIST Indexes     │
                               └─────────────────────┘
```

### Technology Stack

#### Frontend
- **React 18** + **TypeScript** - Type-safe UI components
- **Tailwind CSS** - Utility-first styling
- **React-Leaflet** - Interactive maps
- **Axios** - HTTP client with interceptors
- **Context API** - State management

#### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and settings
- **SQLAlchemy** - Database ORM with connection pooling
- **OpenAI GPT-4** - SQL generation
- **Tenacity** - Retry logic for resilience
- **SlowAPI** - Rate limiting

#### Database
- **PostgreSQL 15** - Relational database
- **PostGIS 3.3** - Spatial extension

#### DevOps
- **Docker** + **Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipelines
- **Pre-commit** - Git hooks for code quality
- **pytest** + **Jest** - Testing frameworks

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation (3 Steps)

#### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/geo-sql-agent.git
cd geo-sql-agent
cp .env.example .env
```

#### 2. Add API Key
Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 3. Run with Docker

**Development Mode** (with hot reload):
```bash
docker-compose --profile development up --build
```
✅ React Dev: http://localhost:3000
✅ Backend API: http://localhost:8000
✅ API Docs: http://localhost:8000/docs

**Production Mode** (optimized):
```bash
docker-compose --profile production up --build
```
✅ React Prod: http://localhost:3010

---

## 💡 Example Queries

Try these natural language questions:

### Spatial Queries
- "Find all cafes within 200 meters of the largest park"
- "Show all parks larger than 5000 square meters"
- "What is the closest cafe to the smallest park?"

### Planning Data (Israeli)
- "Show me 5 approved planning areas"
- "הצג תכניות מאושרות" (Show approved plans)
- "מצא תכניות שמכילות בתי קפה" (Find plans containing cafes)

### Advanced
- "Show roads that intersect with parks"
- "Find planning areas within 500m of cafes"

---

## 📊 Sample Data

The database comes pre-loaded with:

| Table | Count | Type | Description |
|-------|-------|------|-------------|
| **cafes** | 15 | Points | Coffee shops around Tel Aviv |
| **parks** | 7 | Polygons | Parks and green spaces |
| **roads** | 6 | LineStrings | Main streets and boulevards |
| **plans** | 1000+ | Polygons | Israeli urban planning data |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICK_START.md](QUICK_START.md)** | Quick 3-step installation guide |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Detailed system architecture and design |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Guidelines for contributing to the project |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and release notes |
| **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** | Complete project overview and statistics |

---

## 🔧 Development

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

#### Frontend
```bash
cd frontend-react
npm install
npm start
npm test
```

### Code Quality

Run pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Run linters:
```bash
# Backend
cd backend
black app
isort app
flake8 app
mypy app

# Frontend
cd frontend-react
npm run lint
npm run format
```

### Testing

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend-react
npm test -- --coverage
```

---

## 🔒 Security

### Built-in Security Features

✅ **SQL Injection Prevention**
- Input validation with Pydantic
- SQL query validation (only SELECT allowed)
- Blocked keywords (DROP, DELETE, INSERT, etc.)
- Multiple statement prevention

✅ **Rate Limiting**
- 10 requests per minute (configurable)
- Per-IP tracking

✅ **Docker Security**
- Non-root user in containers
- Multi-stage builds
- Minimal attack surface

### Security Best Practices

- **NEVER** commit `.env` file
- Change database credentials in production
- Use HTTPS in production
- Configure CORS for your domain
- Rotate API keys regularly

See [SECURITY.md](.github/SECURITY.md) for reporting vulnerabilities.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Areas for Contribution

- [ ] Add more PostGIS functions
- [ ] Support for raster data
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Query history persistence
- [ ] Export to GeoJSON/Shapefile
- [ ] Dark mode toggle
- [ ] Additional map layers

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/geo-sql-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/geo-sql-agent/discussions)
- **Email**: your-email@example.com

---

## 📈 Project Stats

<!-- GitHub stats will be auto-generated -->
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/geo-sql-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/geo-sql-agent?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/geo-sql-agent?style=social)

---

## 🎓 Educational Value

This project demonstrates:
- ✅ **Backend Development** - RESTful API design with FastAPI
- ✅ **AI Integration** - Prompt engineering for SQL generation
- ✅ **Geospatial Databases** - PostGIS spatial queries
- ✅ **Full-stack Integration** - React + FastAPI + PostgreSQL
- ✅ **Docker Orchestration** - Multi-container applications
- ✅ **CI/CD Pipelines** - GitHub Actions workflows
- ✅ **Code Quality** - Testing, linting, type checking
- ✅ **Security Best Practices** - Input validation, rate limiting

Perfect for:
- Learning modern web development
- Understanding AI-powered applications
- GIS and spatial data processing
- Production-ready Docker deployments

---

## 🌟 Acknowledgments

- OpenAI for GPT-4 API
- PostGIS team for the amazing spatial extension
- FastAPI community
- React and TypeScript teams
- All contributors

---

## 📞 Contact

Built by [Your Name]

- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- GitHub: [@YourUsername](https://github.com/YourUsername)
- Email: your-email@example.com

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

Made with ❤️ and lots of ☕

</div>
