# FinPilot Backend - Run and Test Guide

## Overview

FinPilot backend is a FastAPI application providing financial planning APIs for Vietnamese users. It includes deterministic financial projections, user authentication, and goal planning features.

**Current Status**: Phase 2 (Foundational Infrastructure) is complete. The backend has:

- ✅ PostgreSQL database with migrations
- ✅ JWT authentication system
- ✅ FastAPI routing and CORS
- ✅ Base SQLAlchemy models
- ✅ Comprehensive error handling and logging
- ✅ **Deterministic financial projection engine**

**Next Phase**: Phase 3 (User Stories) - API endpoints, schemas, and testing framework.

## Prerequisites

- **Python 3.11+**
- **PostgreSQL 15+** (or Docker)
- **Poetry** (recommended) or **pip**
- **Docker & Docker Compose** (for full stack development)

## Quick Start with Docker Compose (Recommended)

### 1. Clone and Setup Environment

```bash
cd /Users/ndhanh/projects/finpilotv1
cp backend/.env.example backend/.env
```

### 2. Start All Services

```bash
docker-compose up --build
```

This starts:

- **PostgreSQL** on `localhost:5432`
- **Backend API** on `localhost:8000`
- **Frontend** on `localhost:3000`

### 3. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 4. Test the API

```bash
curl http://localhost:8000/api/v1/health/
# Expected: {"status": "healthy", "service": "finpilot-api"}
```

### 5. Quick Calculation Test

Test the core calculation engine without starting the full server:

```bash
cd backend
python -c "
import sys
sys.path.insert(0, '.')
from src.calculations.projection import ProjectionCalculator, ProjectionInputs

inputs = ProjectionInputs(
    target_amount=100_000_000,  # 100M VND
    timeline_years=5,
    monthly_savings=2_000_000,  # 2M VND/month
    current_savings=10_000_000,  # 10M VND
    expected_return_rate=0.07
)

result = ProjectionCalculator.calculate_projection(inputs)
print(f'✅ Calculation engine working!')
print(f'Achievable: {result.is_achievable}')
print(f'Final net worth: {result.final_net_worth:,} VND')
"
```

## Local Development Setup

### Option 1: Using Poetry (Recommended)

```bash
cd backend

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Copy environment file
cp .env.example .env

# Edit .env with your local database URL
# DATABASE_URL=postgresql://finpilot_user:finpilot_password@localhost:5432/finpilot
```

### Option 2: Using pip and venv

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### Database Setup (Local PostgreSQL)

```bash
# Create database
createdb finpilot

# Create user (optional, adjust .env accordingly)
createuser finpilot_user
psql -c "ALTER USER finpilot_user PASSWORD 'finpilot_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE finpilot TO finpilot_user;"
```

### Run Database Migrations

```bash
# Using Poetry
poetry run alembic upgrade head

# Or using pip
alembic upgrade head
```

### Start the Development Server

```bash
# Using Poetry
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using pip
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

**Note**: Test directories are set up but most test files are currently empty. The framework is ready for comprehensive testing.

### Run All Tests

```bash
# Using Poetry
poetry run pytest

# Or using pip
pytest
```

### Run Specific Test Categories

```bash
# Unit tests for calculations
pytest tests/test_calculations/

# API tests
pytest tests/test_api/

# Database tests
pytest tests/test_db/

# Integration tests
pytest tests/integration/
```

### Test Coverage

```bash
# With coverage report
pytest --cov=src --cov-report=html

# View coverage report in browser
open htmlcov/index.html
```

### Manual Testing with HTTP Requests

#### Health Check

```bash
curl http://localhost:8000/api/v1/health/
```

#### Test Calculation Engine

```bash
python -c "
from src.calculations.projection import ProjectionCalculator, ProjectionInputs

inputs = ProjectionInputs(
    target_amount=100_000_000,  # 100M VND
    timeline_years=5,
    monthly_savings=2_000_000,  # 2M VND/month
    current_savings=10_000_000,  # 10M VND
    expected_return_rate=0.07
)

result = ProjectionCalculator.calculate_projection(inputs)
print(f'Achievable: {result.is_achievable}')
print(f'Final net worth: {result.final_net_worth:,} VND')
print(f'Break-even month: {result.break_even_month}')
"
```

## API Documentation

### Interactive API Docs (Swagger UI)

Visit: `http://localhost:8000/docs`

### Alternative API Docs (ReDoc)

Visit: `http://localhost:8000/redoc`

## Code Quality

### Linting and Formatting

```bash
# Format code with Black
black src/

# Sort imports with isort
isort src/

# Check for linting issues (if flake8 is installed)
flake8 src/
```

### Type Checking (if mypy is configured)

```bash
mypy src/
```

## Environment Variables

Key environment variables in `.env`:

```bash
# Database connection
DATABASE_URL=postgresql://finpilot_user:finpilot_password@localhost:5432/finpilot

# Security (change in production!)
SECRET_KEY=your-secret-key-here-change-in-production

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432 -U finpilot_user -d finpilot

# Reset database (WARNING: destroys data)
docker-compose down -v
docker-compose up -d db
docker-compose exec backend alembic upgrade head
```

### Port Conflicts

```bash
# Check what's using ports
lsof -i :8000  # Backend
lsof -i :5432  # Database
lsof -i :3000  # Frontend
```

### Import Errors

```bash
# Ensure you're in the correct directory
cd backend

# Activate virtual environment
source venv/bin/activate  # or poetry shell

# Install dependencies
pip install -r requirements.txt  # or poetry install
```

### Migration Issues

```bash
# Check migration status
alembic current

# Reset migrations (WARNING: destroys data)
alembic downgrade base
alembic upgrade head
```

### Docker Issues

```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View container logs
docker-compose logs backend
docker-compose logs db
```

## Development Workflow

1. **Start services**: `docker-compose up -d`
2. **Run migrations**: `docker-compose exec backend alembic upgrade head`
3. **Make code changes** in `src/`
4. **Run tests**: `docker-compose exec backend pytest`
5. **Check API**: Visit `http://localhost:8000/docs`
6. **Format code**: `docker-compose exec backend black src/`

## Production Deployment

For production deployment:

1. Use environment-specific `.env` files
2. Set strong `SECRET_KEY`
3. Configure proper CORS origins
4. Use managed PostgreSQL database
5. Enable HTTPS
6. Set up proper logging and monitoring

## Architecture Overview

```
src/
├── main.py              # FastAPI application
├── config.py            # Settings and configuration
├── database.py          # SQLAlchemy setup
├── models/              # Database models
├── schemas/             # Pydantic schemas
├── api/                 # API routes
├── services/            # Business logic
├── calculations/        # Financial calculations
├── auth/                # Authentication utilities
└── utils/               # Utilities (logging, errors)
```
