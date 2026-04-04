# Quick Start - Local Development with Docker Database

## 📋 Setup Summary

You now have a setup where:
- **Database**: PostgreSQL 15 running in Docker
- **Backend**: FastAPI running locally (Python)
- **Frontend**: Next.js running locally (Node.js)

All three connect to each other on localhost.

## 🚀 Quick Start (5 minutes)

### Terminal 1: Start Database

```bash
# In root directory
docker-compose up
```

Wait for output: `database system is ready to accept connections`

### Terminal 2: Setup & Run Backend

```bash
cd backend

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Run database migrations to Docker
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 3: Setup & Run Frontend

```bash
cd frontend

# Install Node dependencies (first time only)
npm install

# Start frontend development server
npm run dev
```

Expected output:
```
▲ Next.js 14.x.x
- ready started server on 0.0.0.0:3000
```

## ✅ Verify Everything Works

### Test Backend

```bash
curl http://localhost:8000/api/v1/health
# Returns: {"status":"healthy"}

curl http://localhost:8000/api/v1/templates
# Returns: {"templates": [...]}
```

### Test Frontend

Open in browser:
```
http://localhost:3000
```

### Test Database

Access PgAdmin:
```
http://localhost:8080
Email: admin@finpilot.com
Password: admin
```

## 🔧 Common Commands

### Apply New Migrations

After creating a new migration file:
```bash
cd backend
alembic upgrade head
```

### Rollback One Migration

```bash
cd backend
alembic downgrade -1
```

### Check Migration Status

```bash
cd backend
alembic current
alembic history
```

### Reset Everything (⚠️ Deletes data)

```bash
docker-compose down -v
docker-compose up
cd backend
alembic upgrade head
```

## 🐛 Troubleshooting

### "Connection refused" from backend

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Fix**: 
```bash
# Check .env has localhost (not 'db')
cat backend/.env | grep DATABASE_URL
# Should show: postgresql://...@localhost:5432/...

# Verify Docker database is running
docker-compose ps
```

### Frontend can't reach backend

**Problem**: `Failed to fetch from http://localhost:8000`

**Fix**:
1. Verify backend is running: `lsof -i :8000`
2. Check frontend `.env.local` file exists and has correct API URL
3. Backend CORS must allow frontend origin: Check backend `.env`

### Port already in use

**Problem**: `Address already in use :8000`

**Fix**:
```bash
# Find what's using the port
lsof -i :8000

# Kill it (replace <PID>)
kill -9 <PID>
```

## 📚 Full Documentation

For detailed setup, troubleshooting, and workflow:
- [LOCAL_DEVELOPMENT_SETUP.md](docs/LOCAL_DEVELOPMENT_SETUP.md) - Complete guide

## 🎯 Next Steps

1. ✅ Database running in Docker
2. ✅ Backend connected to Docker database
3. ✅ Frontend connected to backend
4. → Start implementing features!

See [../../tasks.md](specs/001-mvp-core/tasks.md) for Phase 3 (Frontend template selection).
