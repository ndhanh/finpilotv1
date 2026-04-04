# Docker Migration Fix - Complete Guide

## Problem Summary

The original Docker setup was unable to run database migrations when the backend container started. This caused schema mismatches since the `template_id` column wasn't being added to the `plans` table.

## Root Causes Fixed

### 1. **Missing Backend Service in docker-compose.yml**

The backend container wasn't defined in the docker-compose configuration, meaning there was no service to run migrations or the FastAPI app.

**Solution**: Added backend service with:

- Build configuration pointing to ./backend/Dockerfile
- Proper health check dependency on database
- Environment variables for configuration
- Volume mount for live code reloading
- Startup command to run migrations then start app

### 2. **Missing Migration Step in Startup**

The Dockerfile CMD was only running `uvicorn` without first executing `alembic upgrade head`.

**Solution**: Updated docker-compose backend command:

```sh
sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
```

This ensures:

- Migrations run first
- Application starts after migrations complete
- Both commands share the same shell context

### 3. **Database URL Configuration**

The Alembic env.py has a hardcoded Docker-specific database URL, and the FastAPI app reads from environment variables.

**Solution**: Set `DATABASE_URL` environment variable in docker-compose to match both systems:

```yaml
DATABASE_URL: postgresql://finpilot_user:finpilot_password@db:5432/finpilot
```

## Files Modified

### [docker-compose.yml](../docker-compose.yml)

**Changes**:

- Added `backend` service section
- Set `depends_on` with `service_healthy` condition to wait for database
- Added environment variables for FastAPI configuration
- Set startup command with migration + app launch

**Key Configuration**:

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    DATABASE_URL: postgresql://finpilot_user:finpilot_password@db:5432/finpilot
    SECRET_KEY: dev-secret-key-change-in-production
    CORS_ORIGINS: http://localhost:3000,http://localhost:3001
    PYTHONUNBUFFERED: "1"
  depends_on:
    db:
      condition: service_healthy
  volumes:
    - ./backend:/app
  command: sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
```

### [backend/alembic/versions/add_template_id_to_plans.py](../backend/alembic/versions/add_template_id_to_plans.py)

**Changes**:

- Fixed SQL execution to use `sa.text()` wrapper for raw SQL
- Added `existing_nullable=True` parameter for proper state tracking
- Ensured proper null handling in backfill operation

**Key Migration Steps**:

1. Add `template_id` column as nullable (with server default)
2. Backfill existing records with `'home_purchase'`
3. Make column non-nullable
4. Create index for query performance

## How the Fix Works

### Pre-Migration Checks

1. **Database Health Check** (docker-compose)
   - Waits for PostgreSQL to be ready before starting backend
   - Uses `pg_isready` health check on db service
   - Backend service waits for healthy database

2. **Configuration Loading**
   - FastAPI reads environment variables set in docker-compose
   - Alembic reads hardcoded URL in env.py (pointing to Docker service `db`)
   - Both use same credentials: `finpilot_user:finpilot_password`

### Migration Execution

1. **Container Startup**
   - Backend container starts and executes: `alembic upgrade head`
   - Alembic connects to PostgreSQL using Docker service hostname `db`
   - Migration file executes upgrade() function

2. **Migration Steps**

   ```python
   # 1. Add nullable column
   op.add_column("plans", sa.Column("template_id", sa.String(50), nullable=True))

   # 2. Backfill with default
   op.execute(sa.text("UPDATE plans SET template_id = 'home_purchase'..."))

   # 3. Make non-nullable
   op.alter_column("plans", "template_id", nullable=False, existing_nullable=True)

   # 4. Add index
   op.create_index("ix_plans_template_id", "plans", ["template_id"])
   ```

3. **Application Startup**
   - After migrations complete, FastAPI starts with `uvicorn`
   - Database schema is ready
   - API endpoints can query the database

## Testing the Fix

### Quick Test

Start Docker services:

```bash
docker-compose up
```

Expected output in logs:

```
backend_1  | INFO: Alembic version table created...
backend_1  | INFO: Running migration add_template_id_to_plans...
backend_1  | INFO: Done
backend_1  | INFO: Uvicorn running on 0.0.0.0:8000
```

### Verification Tests

1. **Check API is Running**

   ```bash
   curl http://localhost:8000/api/v1/health
   ```

   Expected response:

   ```json
   { "status": "healthy" }
   ```

2. **Check Templates Endpoint**

   ```bash
   curl http://localhost:8000/api/v1/templates
   ```

   Expected response with 2 templates:

   ```json
   {
     "templates": [
       {
         "id": "home_purchase",
         "name_vi": "Lập kế hoạch mua nhà",
         "status": "available",
         ...
       }
     ]
   }
   ```

3. **Verify Database Schema**

   Using pgAdmin (port 8080):
   - Login: admin@finpilot.com / admin
   - Navigate to: Servers > finpilot > Databases > finpilot > Schemas > public > Tables > plans
   - Right-click on `plans` table and select "Properties"
   - Verify `template_id` column exists with:
     - Type: character varying(50)
     - Nullable: NO
     - Default: None (was filled during migration)

   Or using psql:

   ```bash
   docker-compose exec db psql -U finpilot_user -d finpilot -c "\d plans"
   ```

4. **Check Migration History**

   ```bash
   docker-compose exec backend alembic history
   ```

   Should show both existing migrations and the new one:

   ```
   822108182c7d -> add_template_id_to_plans (head), Add template_id to plans table
   ```

### Debugging Issues

If migrations fail:

1. **Check logs**

   ```bash
   docker-compose logs backend
   docker-compose logs db
   ```

2. **Verify database is healthy**

   ```bash
   docker-compose exec db pg_isready -U finpilot_user -d finpilot
   ```

   Should return: `accepting connections`

3. **Check Alembic directly**

   ```bash
   docker-compose exec backend sh
   cd /app
   alembic current
   alembic update head
   ```

4. **Reset if needed** (WARNING: destroys data)
   ```bash
   docker-compose down -v
   docker-compose up
   ```

## Environment Variables Reference

| Variable           | Value                                                           | Purpose                           |
| ------------------ | --------------------------------------------------------------- | --------------------------------- |
| `DATABASE_URL`     | `postgresql://finpilot_user:finpilot_password@db:5432/finpilot` | FastAPI database connection       |
| `SECRET_KEY`       | `dev-secret-key-change-in-production`                           | JWT token signing (dev only)      |
| `CORS_ORIGINS`     | `http://localhost:3000,http://localhost:3001`                   | Frontend origins allowed          |
| `PYTHONUNBUFFERED` | `1`                                                             | Unbuffered Python output for logs |

## Production Considerations

### Security

- [ ] Change `SECRET_KEY` to a strong random string
- [ ] Use database credentials from secrets management
- [ ] Remove `--reload` flag from uvicorn command
- [ ] Set `echo=False` in database.py

### Configuration

- [ ] Use `.env` file or environment variables for credentials
- [ ] Set `CORS_ORIGINS` to actual frontend domains
- [ ] Update database URL to production server address
- [ ] Configure logging levels appropriately

### Database

- [ ] Use managed PostgreSQL (RDS, Cloud SQL, etc.)
- [ ] Enable automated backups
- [ ] Set up connection pooling
- [ ] Monitor migration execution

## Next Steps

1. **Test the Fix**: Run `docker-compose up` and verify endpoints
2. **Continue Phase 3**: Implement frontend template selection component
3. **Add Frontend Service**: Include frontend in docker-compose
4. **Integration Testing**: Test full flow from frontend through API to database
