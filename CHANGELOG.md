# Changelog

All notable changes to the Geo-SQL Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Query history persistence (LocalStorage)
- Export results to GeoJSON/CSV/Shapefile
- Dark mode toggle for frontend
- Additional PostGIS functions (ST_Buffer, ST_Union, etc.)
- Multi-language support (Spanish, French, Arabic)
- WebSocket support for real-time updates
- Query templates and favorites

---

## [1.0.2] - 2024-12-24

### 🎨 Frontend UX Improvements & Data Import

### Fixed
- **Frontend Layout:** Complete redesign to match original split-view layout
  - Left sidebar (40%) with Query Input, SQL Display, and Example Queries
  - Right map (60%) with full-screen view - no scrolling required
  - Removed redundant wrapper components for cleaner UI
- **Leaflet Markers:** Fixed broken marker icons using CDN
  - Added proper icon URLs from `cdnjs.cloudflare.com`
  - Markers now display correctly with blue pins and shadows
- **Map Bounds:** Fixed map auto-focus for all geometry types
  - Added `extractBounds()` function to handle Points, LineStrings, Polygons
  - Recursive coordinate extraction for Multi* geometries
  - Map now centers correctly on Polygons/LineStrings, not just Points
- **Geometry Display:** Added support for all PostGIS geometry types
  - Points displayed as Markers with popups
  - LineStrings displayed as blue lines (roads)
  - Polygons displayed as blue shapes with semi-transparent fill (plans, parks)
  - Added custom `geoJsonStyle()` function for consistent styling
- **Popup Content:** Fixed empty popups by extracting properties correctly
  - Properties now shown for all geometry types
  - Displays id, name, area, distance, and all custom attributes

### Added
- **Plans Data:** Imported 1,000 Israeli planning records (תכניות בניין עיר)
  - Ran `04-import-plans-data.py` to populate plans table
  - Plans include: pl_name, pl_area_dunam, station_desc, geometry
  - Enables queries like "Find me the smallest plan" and "Show biggest approved plans"
  - Full support for plan-cafe/plan-park spatial joins
- **SQL Display Component:** Re-added to sidebar
  - Shows generated SQL query after execution
  - Displays execution time
  - Copy-to-clipboard functionality
  - Better user understanding of what queries are being executed

### Changed
- **TypeScript Version:** Downgraded from 5.3 to 4.9.5
  - Fixed compatibility with react-scripts@5.0.1
  - Resolved build errors without `--legacy-peer-deps`
- **Frontend Dependencies:** Cleaned up unused imports and configs
  - Removed `.eslintrc.json` (conflicted with react-scripts)
  - Removed unused `EXAMPLE_QUERIES` constant
  - Fixed all TypeScript strict mode warnings

### Data
- **Database Records:**
  - Cafes: 15 locations
  - Parks: 7 green spaces
  - Roads: 6 streets
  - Plans: 1,000 planning records ✨ NEW

---

## [1.0.1] - 2024-12-23

### 🧹 Project Cleanup & Security Fixes

### Fixed
- **CRITICAL:** SQL injection vulnerability in `database.py:get_table_count()`
  - Added whitelist validation for table names
  - Prevented potential SQL injection attack vector
- **Build Issue:** Fixed `Dockerfile.prod` npm install command
  - Changed from `npm ci --only=production` to `npm ci` to include devDependencies for build
  - Ensures TypeScript and build tools are available during Docker build

### Removed
- **Legacy Frontend:** Removed `frontend/` directory (legacy HTML version)
  - Modern React frontend (`frontend-react/`) is now the only frontend
  - Removed `frontend-legacy` service from `docker-compose.yml`
  - Updated README to remove legacy mode instructions
- **Redundant Documentation:** Cleaned up duplicate and session-specific MD files
  - Removed `AUDIT_REPORT.md` (session report)
  - Removed `DEPLOYMENT_CHECKLIST.md` (redundant with README)
  - Removed `QUICK_START.md` (duplicate of README Quick Start section)
  - Removed `PROJECT_COMPLETE.md` (internal session report)
  - Removed `MD_FILES_ANALYSIS.md` (temporary analysis file)
  - **Result:** 50% reduction in documentation files (8 → 4 core files)

### Changed
- **Documentation Structure:** Now maintains only 4 essential MD files:
  - `README.md` - Main project documentation
  - `ARCHITECTURE.md` - Technical architecture details
  - `CHANGELOG.md` - Version history (this file)
  - `CONTRIBUTING.md` - Contribution guidelines
- Updated `README.md` deployment section to remove legacy mode
- Streamlined docker-compose.yml (2 profiles: development, production)

### Added
- `frontend-react/.env.example` - Environment variables template
- `frontend-react/.eslintignore` - ESLint exclusions
- `frontend-react/.prettierignore` - Prettier exclusions

### Security
- ✅ SQL injection vulnerability patched
- ✅ Table name whitelist validation enforced
- ✅ All security best practices verified

---

## [1.0.0] - 2024-12-23

### 🎉 Major Release - Production Ready

This release marks the complete transformation from MVP to production-ready application.

### Added

#### Backend
- **Complete Backend Refactoring** with best practices architecture
  - Modular structure (app/models, services, api)
  - Pydantic Settings for configuration management
  - Connection pooling with SQLAlchemy
  - SQL validation (prevents DROP, DELETE, INSERT commands)
  - Rate limiting with SlowAPI (10 requests/minute default)
  - Retry logic for OpenAI with Tenacity
  - Comprehensive error handling and logging
  - Health check endpoint (`/health`)
  - OpenAPI documentation (`/docs`, `/redoc`)

#### Frontend
- **Modern React 18 Frontend** with TypeScript
  - React-Leaflet for interactive maps
  - Tailwind CSS for responsive design
  - Context API for state management
  - Error boundaries for error handling
  - Loading states and spinners
  - Example queries quick-select
  - Copy SQL to clipboard functionality
  - Auto-fit map to results

#### DevOps & Quality
- **GitHub Actions CI/CD**
  - Backend CI workflow (pytest, flake8, mypy)
  - Frontend CI workflow (Jest, ESLint, TypeScript checks)
  - Docker build and push workflow
  - Code coverage reporting with Codecov

- **Pre-commit Hooks**
  - Black (Python formatting)
  - isort (import sorting)
  - flake8 (Python linting)
  - mypy (type checking)
  - Prettier (TypeScript/JavaScript formatting)
  - ESLint (TypeScript linting)
  - Markdown linting
  - Secrets detection

- **Testing Infrastructure**
  - pytest suite for backend (API, database, schemas)
  - Jest + React Testing Library for frontend
  - Test coverage reporting
  - Integration tests

- **Code Quality Tools**
  - .flake8 configuration
  - pyproject.toml for Black, isort, mypy
  - .eslintrc.json for TypeScript
  - .prettierrc.json for code formatting

#### Docker
- **Production-ready Docker setup**
  - Multi-stage Dockerfile (builder + runtime)
  - Non-root user for security
  - Health checks for all services
  - Resource limits (CPU, memory)
  - Docker Compose profiles (development/production/legacy)
  - Three frontend options: React dev, React prod, HTML legacy

#### Documentation
- **Comprehensive Documentation**
  - QUICK_START.md - 3-step installation guide
  - UPGRADE_SUMMARY.md - Detailed upgrade notes
  - Updated README.md with badges and architecture
  - GitHub templates (bug reports, feature requests, PRs)
  - SECURITY.md - Security policy and best practices
  - Updated all existing documentation

#### Israeli Planning Data
- Plans table schema and import scripts
- 1000+ Israeli urban planning areas (תכניות בניין עיר)
- PLANS_IMPORT.md guide
- PLANS_QUERIES.md with 20+ example queries
- Hebrew language support for planning queries

### Changed

- **Port Configuration**: PostGIS now uses port 5433 (was 5432)
- **Frontend Architecture**: Migrated from vanilla HTML to React + TypeScript
- **Backend Structure**: Refactored monolithic main.py into modular architecture
- **Environment Variables**: Expanded .env.example with comprehensive settings
- **Dependencies**: Updated to latest stable versions
  - FastAPI 0.104.1
  - React 18.2.0
  - TypeScript 5.3.3
  - Added: slowapi, tenacity, pydantic-settings

### Improved

- **Security**
  - SQL injection prevention with validation
  - Input sanitization with Pydantic
  - Rate limiting per IP
  - Non-root Docker users
  - Secrets detection in pre-commit hooks

- **Performance**
  - Connection pooling for database
  - Multi-stage Docker builds (smaller images)
  - React production builds with optimization
  - Database indexes (GIST for spatial data)

- **Developer Experience**
  - Type safety with TypeScript and Pydantic
  - Auto-formatting with Black and Prettier
  - Pre-commit hooks for code quality
  - Comprehensive error messages
  - API documentation with OpenAPI/Swagger

### Fixed

- OpenAI version conflict (requires >= 1.6.1)
- Frontend map bounds error (layerGroup vs featureGroup)
- Docker port conflicts with local PostgreSQL
- Unicode encoding issues in import scripts
- ESRI JSON geometry conversion

### Security

- SQL validation prevents destructive queries
- Rate limiting prevents abuse
- Input validation prevents injections
- Secrets detection in commits
- Security policy documented

---

## [0.2.0] - 2024-12-21

### Added

- Comprehensive logging system (backend + frontend)
- Documentation suite (7 core docs + planning docs)
- Plans table for Israeli urban planning data
- Import scripts for Plans.json (8.9MB)
- Hebrew language support

### Changed

- Enhanced frontend logging with console.log tracking
- Updated system prompt to include plans table schema

### Fixed

- OpenAI version compatibility
- Port conflict (5432 → 5433)
- Frontend map rendering bug

---

## [0.1.0] - 2024-12-20

### Added

- Initial project structure
- FastAPI backend with OpenAI integration
- HTML frontend with Leaflet maps
- PostGIS database with sample data (cafes, parks, roads)
- Docker Compose orchestration
- Basic documentation (README, ARCHITECTURE)
- Sample SQL queries

### Features

- Natural language to SQL conversion
- Real-time query execution
- Interactive map visualization
- Support for Points, Polygons, and LineStrings
- English and Hebrew query support

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

---

## Links

- [GitHub Repository](https://github.com/YOUR_USERNAME/geo-sql-agent)
- [Issue Tracker](https://github.com/YOUR_USERNAME/geo-sql-agent/issues)
- [Documentation](https://github.com/YOUR_USERNAME/geo-sql-agent/tree/main/docs)

---

## Contributors

Thank you to all contributors who have helped improve this project!

<!-- Contributors will be listed here -->

---

**For upgrade instructions, see [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)**
