# Implementation Plan: FinPilot MVP Core

**Branch**: `001-mvp-core` | **Date**: March 21, 2026 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mvp-core/spec.md`

**Tech Stack**: Next.js 14 (Frontend) | FastAPI (Backend) | PostgreSQL | Docker Compose

---

## Summary

FinPilot MVP is a goal-based financial planning web application for Vietnamese users. Users input basic financial data through a guided conversation, select a goal (house purchase primary), and receive deterministic projections + rule-based recommendations. Technical approach: Conversational React frontend (Next.js) with progressive state capture; RESTful FastAPI backend with stateless projection calculations; PostgreSQL for user plans and calculation audit trail; Docker Compose for local dev + staging.

---

## Technical Context

**Frontend Language/Version**: TypeScript, Next.js 14 (App Router)  
**Frontend Framework**: React 18.3+, TailwindCSS, Recharts (charting)  
**Frontend State**: Context API + localStorage (progressive capture); optional React Query post-MVP  
**Backend Language/Version**: Python 3.11+  
**Backend Framework**: FastAPI 0.104+  
**Backend ORM**: SQLAlchemy 2.x with async support  
**Database**: PostgreSQL 15+; connection pooling (PgBouncer or asyncpg)  
**Storage**: PostgreSQL (users, plans, calculations, audit logs); no file storage MVP  
**Authentication**: JWT tokens (Access + Refresh); secure httpOnly cookies  
**Testing Backend**: pytest + pytest-asyncio; fixtures for DB + calculation tests  
**Testing Frontend**: Jest + React Testing Library; Playwright for E2E  
**Target Platform**: Web browser (desktop-first, mobile responsive); no native apps  
**Containerization**: Docker Compose (local dev); Docker + nginx (staging/prod)  
**Project Type**: Full-stack web service  
**Performance Goals**: Projection calculation <100ms; API response <200ms p95; Dashboard render <300ms  
**Constraints**: No internet-dependent calculations; all logic self-contained; VND arithmetic without floats  
**Scale/Scope**: MVP targets 500-1000 active monthly users; ~10 core screens; 2 primary goal types

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

**Principle I: Goal-Based Financial Planning** ✓

- Architecture supports goal-centric data model (Goal entities with user links)
- Projection engine calculates goal-specific feasibility (not generic tracking)
- Recommendations tied to goal achievement, not product upsell
- **Status**: Compliant; design reflects goal-first thinking

**Principle II: Explainable Modeling** ✓

- Deterministic calculation engine with audit trail logging
- All assumptions stored and displayed to users
- Rule-based recommendations with plain-language explanations
- No black-box algorithms or randomness
- **Status**: Compliant; calculations fully auditable

**Principle III: Vietnam-First UX** ✓

- Frontend localizes to Vietnamese (language toggles are O2025 only)
- Currency formatted as VND with proper thousands separator
- Date format DD/MM/YYYY (Vietnamese convention)
- Default down payment % aligned with Vietnam real estate norms
- **Status**: Compliant; design considers Vietnamese context

**Principle IV: Deterministic Calculation Quality** ✓

- Linear projection math (no compounds, no randomness)
- All VND arithmetic as integers (no floating-point errors)
- Same inputs = identical outputs (reproducible in tests)
- **Status**: Compliant; calculation design is deterministic

**Principle V: Progressive Data Capture** ✓

- Onboarding asks one question per step; optional fields supported
- Defaults provided for skipped inputs
- Saved plan can be updated incrementally
- No forced upfront data entry
- **Status**: Compliant; UX supports progressive disclosure

**Principle VI: Trust-Centered Product Behavior** ✓

- No manipulative patterns (no fake urgency, dark patterns)
- Security-first: HTTPS, encrypted DB, JWT auth
- Transparent assumptions; no hidden logic
- GDPR-style data export capability
- **Status**: Compliant; architecture prioritizes trust

**Constitution Check Result**: ✅ **PASS** — All principles alignedafter implementation. No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-mvp-core/
├── spec.md              # Product specification (already complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 (technical research outcomes)
├── data-model.md        # Phase 1 (database schema + entities)
├── contracts/           # Phase 1 (API contracts)
│   ├── goals.md         # Goal creation/retrieval/update contracts
│   ├── projections.md   # Projection calculation contract
│   ├── users.md         # Auth + user contracts
│   └── health.md        # Health check contract
├── quickstart.md        # Phase 1 (setup & first run guide)
└── tasks.md             # Phase 2 (actionable implementation tasks)
```

### Source Code (repository root)

```text
finpilotv1/
├── docker-compose.yml               # Local dev stack (Next.js, FastAPI, Postgres)
├── .dockerignore
├── .env.example
│
├── backend/                         # FastAPI service
│   ├── Dockerfile
│   ├── requirements.txt              # Python dependencies
│   ├── pyproject.toml                # Project config
│   ├── .env.example
│   │
│   └── src/
│       ├── main.py                   # FastAPI app entrypoint
│       ├── config.py                 # Settings (env, DB URL, etc.)
│       ├── database.py               # SQLAlchemy setup + connection
│       │
│       ├── models/                   # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   ├── user.py               # User, authentication
│       │   ├── goal.py               # Goal, goal type enum
│       │   ├── plan.py               # Plan (collection of goals)
│       │   └── audit.py              # Calculation audit trail
│       │
│       ├── schemas/                  # Pydantic schemas (request/response)
│       │   ├── __init__.py
│       │   ├── user.py               # UserCreate, UserLogin, UserResponse
│       │   ├── goal.py               # GoalCreate, GoalUpdate, GoalResponse
│       │   ├── plan.py               # PlanResponse
│       │   ├── projection.py         # ProjectionInput, ProjectionOutput
│       │   └── recommendation.py     # RecommendationResponse
│       │
│       ├── calculations/             # Business logic (projection, rules)
│       │   ├── __init__.py
│       │   ├── projection.py         # Linear projection calculation
│       │   ├── rules.py              # Recommendation rule engine
│       │   └── validation.py         # Input validation logic
│       │
│       ├── services/                 # Higher-level logic
│       │   ├── __init__.py
│       │   ├── user_service.py       # User creation, retrieval
│       │   ├── goal_service.py       # Goal CRUD operations
│       │   ├── projection_service.py # Orchestrates projection + recommendations
│       │   └── plan_service.py       # Plan persistence and retrieval
│       │
│       ├── api/                      # FastAPI routes
│       │   ├── __init__.py
│       │   ├── dependencies.py       # FastAPI Depends utilities
│       │   ├── auth.py               # Auth endpoints (/auth/login, /auth/register)
│       │   ├── goals.py              # Goal endpoints (/goals)
│       │   ├── projections.py        # Projection endpoints (/projections/calculate)
│       │   ├── plans.py              # Plan endpoints (/plans)
│       │   ├── health.py             # /health endpoint
│       │   └── router.py             # Route aggregator
│       │
│       ├── middleware/               # FastAPI middleware
│       │   ├── __init__.py
│       │   └── cors.py               # CORS configuration
│       │
│       └── utils/                    # Utilities
│           ├── __init__.py
│           ├── logger.py             # Structured logging
│           ├── security.py           # JWT, password hashing
│           └── helpers.py            # Common utilities
│
│   └── tests/                        # Test suite
│       ├── conftest.py               # Fixtures (DB, client, user)
│       ├── test_api/
│       │   ├── test_auth.py
│       │   ├── test_goals.py
│       │   ├── test_projections.py
│       │   └── test_plans.py
│       ├── test_calculations/
│       │   ├── test_projection.py    # Unit tests for calculation logic
│       │   ├── test_rules.py         # Unit tests for recommendations
│       │   └── test_validation.py
│       ├── test_services/
│       │   ├── test_user_service.py
│       │   ├── test_goal_service.py
│       │   └── test_projection_service.py
│       ├── test_db/
│       │   └── test_models.py        # Model constraint tests
│       └── integration/
│           └── test_onboarding_flow.py  # End-to-end flow test
│
├── frontend/                        # Next.js application
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── .env.example
│   │
│   ├── public/                      # Static assets
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   └── ...
│   │
│   └── src/
│       ├── app/                     # Next.js 14 App Router
│       │   ├── layout.tsx           # Root layout
│       │   ├── page.tsx             # Home page (landing)
│       │   ├── plan/
│       │   │   ├── layout.tsx       # Planning flow wrapper
│       │   │   ├── page.tsx         # Start planning entry
│       │   │   ├── goal/
│       │   │   │   └── page.tsx     # Goal type selection
│       │   │   ├── timeline/
│       │   │   │   └── page.tsx     # Timeline picker
│       │   │   ├── amount/
│       │   │   │   └── page.tsx     # Goal amount input
│       │   │   ├── savings/
│       │   │   │   └── page.tsx     # Monthly savings input
│       │   │   ├── assets/
│       │   │   │   └── page.tsx     # Current savings input
│       │   │   ├── debt/
│       │   │   │   └── page.tsx     # Debt input (optional)
│       │   │   ├── review/
│       │   │   │   └── page.tsx     # Summary + confirmation
│       │   │   └── results/
│       │   │       └── page.tsx     # Dashboard + results
│       │   ├── dashboard/
│       │   │   ├── layout.tsx       # Dashboard layout (auth required)
│       │   │   ├── page.tsx         # Plan list/overview
│       │   │   ├── plan/
│       │   │   │   └── [id]/
│       │   │   │       └── page.tsx # Individual plan view
│       │   │   └── plan/
│       │   │       └── [id]/edit/
│       │   │           └── page.tsx # Edit saved plan
│       │   ├── auth/
│       │   │   ├── login/
│       │   │   │   └── page.tsx
│       │   │   ├── signup/
│       │   │   │   └── page.tsx
│       │   │   └── logout/
│       │   │       └── page.tsx
│       │   ├── api/                 # API routes (if using Next.js API)
│       │   │   └── [... proxy to backend OR client-side client-only]
│       │   └── globals.css          # Global styles
│       │
│       ├── components/              # Reusable React components
│       │   ├── common/
│       │   │   ├── Header.tsx
│       │   │   ├── Footer.tsx
│       │   │   ├── LoadingSpinner.tsx
│       │   │   └── ErrorBoundary.tsx
│       │   ├── planning/
│       │   │   ├── QuestionCard.tsx  # Single onboarding question
│       │   │   ├── ProgressBar.tsx   # Visual progress indicator
│       │   │   ├── InputFields.tsx   # Currency, date, number inputs
│       │   │   └── SkipOption.tsx    # Skip/optional field handler
│       │   ├── dashboard/
│       │   │   ├── GoalCard.tsx      # Goal summary card
│       │   │   ├── ProjectionChart.tsx  # Recharts chart
│       │   │   ├── FinancialSummary.tsx  # Net worth, liquid, debt
│       │   │   ├── RecommendationPanel.tsx  # List of recommendations
│       │   │   ├── AssumptionsSection.tsx  # Collapsible assumptions
│       │   │   └── SavePlanPrompt.tsx  # CTA for save
│       │   └── auth/
│       │       ├── LoginForm.tsx
│       │       └── SignupForm.tsx
│       │
│       ├── hooks/                   # Custom React hooks
│       │   ├── useAuth.ts           # Auth state + login/logout
│       │   ├── usePlan.ts           # Plan CRUD operations
│       │   ├── useProjection.ts     # Projection calculation
│       │   └── useLocalStorage.ts   # Progressive data persistence
│       │
│       ├── lib/                     # Utilities
│       │   ├── api.ts               # Axios/fetch client wrapper
│       │   ├── auth.ts              # JWT token management
│       │   ├── formatting.ts        # VND formatting, date formatting
│       │   └── constants.ts         # UI constants, API endpoints
│       │
│       ├── context/                 # React Context
│       │   ├── PlanContext.tsx      # Plan state (onboarding + results)
│       │   └── AuthContext.tsx      # Auth state
│       │
│       ├── types/                   # TypeScript types
│       │   └── index.ts             # Goal, Plan, User, Projection, etc.
│       │
│       └── styles/                  # TailwindCSS + additional styles
│           └── ...
│
│   └── __tests__/                   # Test suite (or __tests__ at root)
│       ├── components/
│       │   ├── QuestionCard.test.tsx
│       │   ├── ProjectionChart.test.tsx
│       │   └── ...
│       ├── hooks/
│       │   ├── useProject.test.ts
│       │   └── ...
│       ├── lib/
│       │   ├── formatting.test.ts   # VND, date formatting tests
│       │   └── ...
│       └── e2e/                     # Playwright tests
│           ├── onboarding.spec.ts   # Full onboarding flow
│           ├── auth.spec.ts         # Login/signup flow
│           └── dashboard.spec.ts    # Save + view plan flow
│
└── docs/                            # Project documentation
    ├── DEVELOPMENT.md               # Local dev setup
    ├── ARCHITECTURE.md              # System design docs
    ├── API_REFERENCE.md             # API endpoint docs
    └── DATABASE.md                  # Schema + migrations

```

**Structure Decision**: Selected "Web application (frontend + backend)" option. Reflects:

- Clean separation of concerns (Next.js SPA ↔ FastAPI REST API)
- Scalability (frontend can be deployed to CDN, backend separately)
- Technology alignment (JavaScript team ↔ Python team)
- Docker Compose enables local dev parity with production
- Progressive data capture: localStorage (frontend) ↔ DB (backend after save)

## Complexity Tracking

**Principle Alignment Checks**:

- ✅ No violations detected
- Constitution compliant: See Constitution Check above
- All design decisions logged below

---

## Phase 0: Outline & Research

**Objective**: Resolve technical unknowns; document best practices for Next.js + FastAPI integration; establish architectural patterns.

### Research Tasks

#### Research 1: Next.js 14 App Router × FastAPI Integration Pattern

**Unknown**: How to structure API calls from Next.js 14 to FastAPI without Next.js /api routes?
**Goals**: Determine fetch strategy; handle CORS; manage errors gracefully

**Outcomes** (to document in research.md):

- **Decision**: Use Client-side fetch to external FastAPI endpoint (CORS enabled)
- **Why**: Simpler, no need for Next.js API layer; keeps frontend stateless
- **Pattern**: Create `lib/api.ts` wrapper with axios/fetch client for all API calls
- **Error handling**: Global error boundary + useCallback hooks for 401/500 responses
- **Alternatives considered**: Next.js API routes (decided against: adds complexity, requires proxying)

#### Research 2: JWT Token Management in SPA Environment

**Unknown**: How to securely store JWT tokens in a browser? HttpOnly cookies vs localStorage?
**Goals**: Balance security (XSS protection) with UX (no refresh token complexity in MVP)

**Outcomes** (to document in research.md):

- **Decision**: Use httpOnly + Secure cookies for access token; refresh token also in httpOnly
- **Why**: Protects against XSS; standard SPA security pattern; no localStorage attack surface
- **Implementation**: FastAPI sets Set-Cookie headers; browser automatically includes in requests
- **Refresh logic**: Axios interceptor detects 401 → call /auth/refresh → retry original request
- **Trade-off**: Slightly more complex than localStorage, but critical for financial data security
- **XSRF**: Include CSRF token in non-httpOnly cookie; send in X-CSRF-Token header

#### Research 3: PostgreSQL Integer Arithmetic for VND

**Unknown**: How to handle VND calculations without floating-point errors?
**Goals**: Ensure all financial calculations are exact (no 0.1 cent rounding errors)

**Outcomes** (to document in research.md):

- **Decision**: All VND amounts stored as BIGINT (not DECIMAL); no cents
- **Why**: VND is not subdivided (1 VND is minimum); simplifies math; no float errors
- **Backend**: SQLAlchemy models use Integer type; calculations return integers
- **Frontend**: Format as integer with thousands separator (e.g., 5,000,000,000 ₫)
- **Validation**: Input accepts integers only; reject decimals with clear error
- **Audit**: All calculations logged as integers; 100% reproducible

#### Research 4: Docker Compose Setup for Development

**Unknown**: How to structure docker-compose.yml for local Next.js + FastAPI + PostgreSQL development?
**Goals**: Ensure local dev environment mirrors production; hot reload works; DB migrations smooth

**Outcomes** (to document in research.md):

- **Decision**: Three services: backend (FastAPI), frontend (Next.js), db (PostgreSQL); shared volumes
- **Services**:
  - `db`: PostgreSQL 15 with named volume (persists across container restarts)
  - `backend`: FastAPI on port 8000; mounts backend/ directory (hot reload via import replacement)
  - `frontend`: Next.js on port 3000; mounts frontend/ directory (hot reload via fast refresh)
  - `adminer` (optional): PostgreSQL admin tool on port 8080 (useful for debugging)
- **Networking**: Services on single network; internal DNS (e.g., `http://backend:8000` from frontend)
- **Environment**: .env files for DB credentials, API URL, JWT secret
- **Startup**: `docker-compose up -d`; migrations run on backend startup hook

#### Research 5: Deterministic Testing Strategy for Calculations

**Unknown**: How to ensure projection calculations are bulletproof + reproducible?
**Goals**: Build confidence in calculation correctness; prevent regressions

**Outcomes** (to document in research.md):

- **Decision**: Comprehensive unit tests with known inputs/outputs; comparison spreadsheet; golden files
- **Test pattern**:
  ```python
  def test_projection_on_track():
    # Arrange: Known inputs
    projection = ProjectionInput(
      current_savings=80_000_000,      # 80M VND
      monthly_contribution=15_000_000, # 15M VND
      goal_amount=960_000_000,         # 960M VND
      months_to_goal=24
    )
    # Act
    result = calculate_projection(projection)
    # Assert: Exact output
    assert result.projected_savings == 1_020_000_000  # 80M + (15M × 24)
    assert result.gap == -60_000_000   # Negative gap = surplus
    assert result.feasible == True
  ```
- **Comparison spreadsheet**: Maintain Excel with same test inputs; verify periodically
- **Audit trail**: Log all calculation steps to DB; enable reproduction

### Output Artifacts (Phase 0)

- ✅ `research.md` generated with decisions + rationales
- ✅ Example docker-compose.yml documented
- ✅ Calculation test patterns established

---

## Phase 1: Design & Contracts

### 1.1 Data Model Design (data-model.md)

**Entities**:

1. **User**
   - id (UUID primary key)
   - email (unique)
   - password_hash
   - created_at, updated_at
   - Relationships: → Plans (one-to-many)

2. **Plan**
   - id (UUID primary key)
   - user_id (foreign key → User)
   - name (e.g., "House Purchase 2027")
   - created_at, updated_at
   - Relationships: → Goals (one-to-many), → CalculationAudit (one-to-many)

3. **Goal**
   - id (UUID primary key)
   - plan_id (foreign key → Plan)
   - goal_type (enum: HOUSE_PURCHASE, EMERGENCY_FUND, OTHER)
   - target_completion_date (YYYY-MM-DD)
   - target_amount_vnd (BIGINT, no decimals)
   - primary (boolean: one goal per plan can be marked primary)
   - Relationships: → GoalAssumptions (one-to-one)

4. **GoalAssumptions**
   - id (UUID primary key)
   - goal_id (foreign key → Goal)
   - down_payment_percent (integer, e.g., 20)
   - closing_costs_percent (integer, e.g., 4)
   - inflation_assumption (integer, %, default 0)
   - investment_return_assumption (integer, %, default 0)

5. **FinancialSnapshot**
   - id (UUID primary key)
   - plan_id (foreign key → Plan)
   - current_liquid_savings_vnd (BIGINT)
   - current_total_debt_vnd (BIGINT)
   - monthly_surplus_vnd (BIGINT)
   - created_at

6. **ProjectionResult**
   - id (UUID primary key)
   - goal_id (foreign key → Goal)
   - projected_savings_vnd (BIGINT)
   - gap_vnd (BIGINT, can be negative)
   - feasible (boolean)
   - completion_date (YYYY-MM-DD, or null if not feasible)
   - recommendations (JSON array of recommendation objects)
   - calculated_at (timestamp)

7. **CalculationAudit**
   - id (UUID primary key)
   - plan_id (foreign key → Plan)
   - calculation_type (enum: PROJECTION, RECOMMENDATION)
   - input_json (JSON blob of all inputs)
   - output_json (JSON blob of all outputs)
   - created_at

**Constraints**:

- Email unique across users
- One primary goal per plan
- All VND amounts as BIGINT (no nulls in financial data)
- Dates as DATE or TIMESTAMP; UTC always
- Foreign key cascades: delete User → delete Plans + Goals

### 1.2 API Contracts (contracts/)

**contracts/auth.md**: Login, signup, logout, token refresh
**contracts/goals.md**: Create goal, list goals, get goal, update goal, delete goal
**contracts/projections.md**: Calculate projection (single goal))
**contracts/plans.md**: Create plan, get plan, list plans, update plan
**contracts/health.md**: Health check for k8s probes

Example contract structure:

````
## POST /auth/register

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
````

**Response** (201):

```json
{
  "id": "uuid...",
  "email": "user@example.com",
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Error** (409):

```json
{
  "detail": "Email already registered"
}
```

**Implementation Notes**:

- Password validated: 8+ chars, upper + lower + number
- Tokens created with 30-day expiry
- Refresh token stored in secure httpOnly cookie

````

### 1.3 Quickstart Guide (quickstart.md)

**Setup for Local Development** (Docker Compose):

1. **Clone + Configure**
   ```bash
   git clone ...
   cd finpilotv1
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
````

2. **Start Services**

   ```bash
   docker-compose up -d
   ```

   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - DB: localhost:5432 (credentials in .env)

3. **Run Migrations**

   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. **Seed Data** (optional)

   ```bash
   docker-compose exec backend python scripts/seed.py
   ```

5. **Access Application**
   - Open http://localhost:3000
   - See landing page + "Start Planning" button

6. **Running Tests**

   ```bash
   # Backend tests
   docker-compose exec backend pytest tests/

   # Frontend tests
   docker-compose exec frontend npm test

   # E2E tests
   docker-compose exec frontend npx playwright test
   ```

### 1.4 Agent Context Update

**Command**: `.specify/scripts/bash/update-agent-context.sh copilot`

Outputs: Updates `.vscode/copilot-instructions.md` with:

- Stack: Next.js 14 (TypeScript, React 18), FastAPI (Python 3.11), PostgreSQL 15
- Key architectural patterns: Progressive data capture, rule-based recommendations
- Testing strategy: Deterministic calculation tests, E2E flows
- Deployment: Docker Compose (dev), Docker + nginx (prod)

---

## Implementation Sequence (Ready for Phase 2 Tasks)

### Dependency Chain

1. **Foundation** (Week 1):
   - [ ] Database schema + models
   - [ ] Authentication service (login, signup, JWT)
   - [ ] Docker Compose setup

2. **Core Calculation** (Week 2):
   - [ ] Projection engine (core math)
   - [ ] Recommendation rule engine
   - [ ] Goal CRUD API endpoints

3. **Frontend Onboarding** (Week 2-3):
   - [ ] Landing page + start flow
   - [ ] Question-by-question UI
   - [ ] Local state management (Context + localStorage)

4. **Results Dashboard** (Week 3):
   - [ ] Results display
   - [ ] Charts + visualizations
   - [ ] Save plan flow

5. **Polish & Testing** (Week 4):
   - [ ] E2E testing
   - [ ] Localization (Vietnamese)
   - [ ] Performance optimization

---

## Key Decisions Documented

| Decision                   | Rationale                                           | Risk Mitigation                            |
| -------------------------- | --------------------------------------------------- | ------------------------------------------ |
| No Next.js API layer       | Simplifies architecture; FastAPI is source of truth | CORS must be configured correctly          |
| HttpOnly JWT cookies       | Security for financial data                         | Requires refresh token pattern             |
| Integer VND arithmetic     | No floating-point errors                            | All calculations must be tested rigorously |
| Docker Compose for dev     | Local-prod parity                                   | Requires team familiarity with Docker      |
| Progressive data capture   | Reduces user friction                               | DB schema must support optional fields     |
| Rule-based recommendations | Explainability + determinism                        | Rules engine must be thoroughly tested     |

---

## Success Criteria for Phase 1

- [ ] `data-model.md` complete with all entities, constraints, relationships
- [ ] 4+ API contracts defined in `contracts/` with request/response examples
- [ ] `quickstart.md` tested: newcomer can start dev environment with one command
- [ ] `research.md` documents all major technical decisions + alternatives
- [ ] Agent context updated with stack-specific guidance

---

**Phase 1 Status**: ✅ Ready to generate Phase 2 tasks via `/speckit.tasks`

**Next Step**: Run `/speckit.tasks` to generate actionable, dependency-ordered implementation tasks.

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
