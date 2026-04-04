# Local Development Setup - Database in Docker, Apps Locally

This guide explains how to run the database in Docker while running the backend and frontend applications locally.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Machine                          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Frontend (Next.js)          Backend (FastAPI)           │
│  http://localhost:3000       http://localhost:8000       │
│  npm run dev                 uvicorn ...                 │
│         │                          │                      │
│         └──────────┬───────────────┘                     │
│                    │                                      │
│              DATABASE_URL                                │
│         (localhost:5432)                                  │
│                    │                                      │
│         ┌──────────▼──────────┐                          │
│         │    Docker Desktop   │                          │
│         ├─────────────────────┤                          │
│         │ PostgreSQL:5432     │                          │
│         │ PgAdmin:8080        │                          │
│         └─────────────────────┘                          │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

- Docker and Docker Desktop installed
- Python 3.11+ installed locally
- Node.js 18+ installed locally
- Git

## Step 1: Start Docker Database

Start only the database services:

```bash
docker-compose up
```

You should see:

```
db_1   | database system is ready to accept connections
```

### Verify Database is Running

Check the health:

```bash
docker-compose exec db pg_isready -U finpilot_user -d finpilot
# Output: accepting connections
```

## Step 2: Set Up Backend

### Install Python Dependencies

```bash
cd backend

# Using pip (recommended for development)
pip install -r requirements.txt

# OR using conda
conda create -n finpilot python=3.11
conda activate finpilot
pip install -r requirements.txt
```

### Run Database Migrations

```bash
cd backend

# Apply all migrations to the Docker database
alembic upgrade head
```

Expected output:

```
INFO  [alembic.runtime.migration] Running upgrade 823108182c7d -> add_template_id_to_plans, Add template_id to plans table
INFO  [alembic.runtime.migration] Migration complete
```

### Start Backend Server

```bash
cd backend

# Run on default port 8000
uvicorn src.main:app --reload

# OR run on a different port
uvicorn src.main:app --reload --port 8001
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Test Backend

```bash
# In a new terminal
curl http://localhost:8000/api/v1/health

# Should return:
# {"status":"healthy"}

# Check templates endpoint
curl http://localhost:8000/api/v1/templates

# Should return templates list with home_purchase and emergency_fund
```

## Step 3: Set Up Frontend

### Install Node Dependencies

```bash
cd frontend

# Using npm (recommended)
npm install

# OR using yarn
yarn install

# OR using pnpm
pnpm install
```

### Update Frontend API Configuration

Edit [frontend/src/lib/api.ts](../frontend/src/lib/api.ts):

```typescript
// Make sure the API base URL points to local backend
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
```

Or set environment variable in [frontend/.env.local](../frontend/.env.local):

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Start Frontend Server

```bash
cd frontend

# Run on default port 3000
npm run dev

# Output should show:
# ▲ Next.js 14.x.x
# - ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Test Frontend

Open browser and navigate to:

```
http://localhost:3000
```

## Database Access

### PgAdmin Web Interface

- URL: [http://localhost:8080](http://localhost:8080)
- Email: `admin@finpilot.com`
- Password: `admin`

**Add Server**:

1. Right-click "Servers" → "Register" → "Server"
2. General tab:
   - Name: `Local Finpilot DB`
3. Connection tab:
   - Host name/address: `localhost`
   - Port: `5432`
   - Maintenance database: `finpilot`
   - Username: `finpilot_user`
   - Password: `finpilot_password`
   - Save password: ✓
4. Click "Save"

Then navigate to:

```
Servers → Local Finpilot DB → Databases → finpilot → Schemas → public → Tables → plans
```

Right-click `plans` → "Properties" to verify `template_id` column exists.

### Command Line Access

```bash
# Connect to PostgreSQL directly
docker-compose exec db psql -U finpilot_user -d finpilot

# Inside psql:
\dt                    # List all tables
\d plans              # Describe plans table
SELECT * FROM plans;  # Query plans table
\q                    # Exit
```

## Running Database Migrations Locally

When you modify the schema, generate and apply migrations:

### Create a New Migration

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "describe your change"

# You'll get a new file in alembic/versions/
```

### Review the Migration

```bash
# Edit the generated file in alembic/versions/
# Verify upgrade() and downgrade() functions
```

### Apply the Migration

```bash
cd backend

# Apply to the Docker database
alembic upgrade head

# OR upgrade one specific migration
alembic upgrade +1

# Check current migration status
alembic current

# View migration history
alembic history
```

### Rollback if Needed

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific migration
alembic downgrade 823108182c7d

# Rollback all (be careful!)
alembic downgrade base
```

## Environment Configuration

### Backend (.env)

Location: [backend/.env](../backend/.env)

```bash
# Database (localhost for local development)
DATABASE_URL=postgresql://finpilot_user:finpilot_password@localhost:5432/finpilot

# Security
SECRET_KEY=dev-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local)

Location: [frontend/.env.local](../frontend/.env.local)

```bash
# API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Useful Commands

### Check All Services Status

```bash
# Docker services
docker-compose ps

# Backend running?
lsof -i :8000

# Frontend running?
lsof -i :3000

# Database running?
lsof -i :5432
```

### Database Troubleshooting

```bash
# Check if database is healthy
docker-compose exec db pg_isready -U finpilot_user -d finpilot

# View database logs
docker-compose logs db

# Verify migrations are applied
docker-compose exec db psql -U finpilot_user -d finpilot -c "SELECT * FROM alembic_version;"

# Check template_id column exists
docker-compose exec db psql -U finpilot_user -d finpilot -c "\d plans"
```

### Reset Database (Warning: Destroys Data)

```bash
# Complete reset
docker-compose down -v

# Restart database
docker-compose up

# Re-apply migrations
cd backend
alembic upgrade head
```

## Common Issues

### Backend Can't Connect to Database

**Error**: `could not translate host name "db" to address`

**Solution**: Make sure `.env` has `localhost` not `db`:

```bash
# Check backend/.env
cat backend/.env | grep DATABASE_URL
# Should show: postgresql://...@localhost:5432/...
```

### Frontend Can't Reach Backend API

**Error**: `Failed to fetch from http://localhost:8000/api/v1`

**Solution**:

1. Verify backend is running: `curl http://localhost:8000/api/v1/health`
2. Check frontend environment: `echo $NEXT_PUBLIC_API_URL`
3. Verify CORS settings in backend `.env`:
   ```bash
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

### Alembic Can't Find Models

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Make sure you're in the backend directory:

```bash
cd backend
alembic upgrade head  # ✓ Correct
```

Not:

```bash
alembic upgrade head  # ✗ Wrong - not in backend directory
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # Database

# Kill process (replace PID)
kill -9 <PID>

# OR use different port
uvicorn src.main:app --reload --port 8001
npm run dev -- -p 3001
```

## Next Steps

1. ✅ Database running in Docker
2. ✅ Backend connected to Docker database
3. ✅ Frontend connected to backend API
4. → Start developing features!

## Switching Back to Docker-Only Setup

If you want to run all services in Docker again:

```bash
# Restore backend service in docker-compose.yml
# Then run:
docker-compose build
docker-compose up

# This is the deployment setup (all in Docker)
```

See [DOCKER_MIGRATION_FIX.md](DOCKER_MIGRATION_FIX.md) for full Docker setup details.
