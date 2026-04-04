# Implementation Plan: Plan Template Selection & Navigation

**Branch**: `002-plan-template-selection` | **Date**: April 4, 2026 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-plan-template-selection/spec.md`

## Summary

Refactor the home planning user journey to support multiple planning templates (home purchase, emergency fund). Users will navigate from the marketing landing page through a template selection page to reach the appropriate planning wizard. The existing database schema will be preserved by adding a `template_id` field to the Plan model and creating a PlanTemplate configuration system.

**User Flow**: Marketing Landing Page → Plan Template Selection Page → Plan Wizard (Home Purchase)

## Technical Context

**Language/Version**:

- Backend: Python 3.11 (FastAPI)
- Frontend: TypeScript 5+ (Next.js 14+ App Router, React 18+)
- Marketing: TypeScript 5+ (Next.js 14+ App Router, React 18+)

**Primary Dependencies**:

- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic
- Frontend: React, Next.js, Tailwind CSS, TypeScript
- Marketing: React, Next.js, Tailwind CSS, TypeScript

**Storage**: PostgreSQL (existing async SQLAlchemy setup)

**Testing**: pytest (backend), Jest/React Testing Library (frontend)

**Target Platform**: Web (responsive mobile-first design)

**Project Type**: Full-stack web application (distributed Next.js multi-app monorepo with FastAPI backend)

**Performance Goals**:

- Template selection page load: <2 seconds (Lighthouse target: 90+ performance)
- Navigation transitions: <300ms

**Constraints**:

- Maintain backward compatibility with existing plan model
- No breaking changes to existing API contracts
- Preserve user plan draft data during navigation
- Support anonymous users (no authentication required for template selection)

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

✅ **No constitution violations identified for this feature.**

This feature:

- Uses existing tech stack (FastAPI, Next.js, React, PostgreSQL, Tailwind)
- Follows established patterns (component-based UI, service layer in backend)
- Maintains backward compatibility with existing Plan model
- Does not require new external dependencies
- Aligns with multi-app monorepo structure (marketing + frontend + backend)

## Project Structure

### Documentation (this feature)

```text
specs/002-plan-template-selection/
├── spec.md              # Feature specification (DONE)
├── plan.md              # This file (current output)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output - API contracts
│   ├── template-selection-api.md
│   └── plan-creation-api.md
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository)

```text
marketing/                          # Marketing/landing page app
├── src/
│   └── app/
│       ├── page.tsx               # Landing page (DONE - has CTA button)
│       └── plan-templates/
│           └── page.tsx           # NEW: Template selection page
├── package.json
└── tsconfig.json

frontend/                           # Plan wizard app
├── src/
│   ├── app/
│   │   ├── plan-templates/
│   │   │   └── page.tsx          # NEW: Alt template selection (fallback route)
│   │   └── plan/
│   │       ├── page.tsx          # REFACTOR: Remove hardcoded options, add template logic
│   │       ├── goal/
│   │       ├── amount/
│   │       ├── assets/
│   │       ├── debt/
│   │       ├── savings/
│   │       ├── timeline/
│   │       ├── results/
│   │       └── review/
│   ├── components/
│   │   ├── planning/
│   │   │   ├── TemplateSelectionCard.tsx    # NEW
│   │   │   ├── TemplateSelectionPage.tsx    # NEW
│   │   │   └── [existing components]
│   │   └── [existing components]
│   ├── lib/
│   │   ├── templates.ts           # NEW: Template definitions & logic
│   │   ├── constants.ts           # MODIFY: Add plan template routes
│   │   ├── api.ts                 # MODIFY: Add template endpoints
│   │   └── [existing utilities]
│   ├── context/
│   │   ├── PlanContext.tsx        # MODIFY: Add templateId field
│   │   └── [existing context]
│   ├── hooks/
│   │   ├── usePlan.ts             # MODIFY: Add template tracking
│   │   ├── useTemplateSelection.ts # NEW: Template selection logic
│   │   └── [existing hooks]
│   ├── types/
│   │   ├── template.ts            # NEW: Template TS types
│   │   └── [existing types]
│   └── tests/
│       └── components/
│           └── TemplateSelection.test.tsx  # NEW

backend/
├── src/
│   ├── models/
│   │   ├── plan.py               # MODIFY: Add template_id foreign key
│   │   └── [existing models]
│   ├── schemas/
│   │   ├── plan.py               # MODIFY: Add templateId to PlanCreate/Response
│   │   ├── template.py           # NEW: Template schemas (TemplateResponse, etc)
│   │   └── [existing schemas]
│   ├── api/
│   │   ├── plans.py              # MODIFY: Accept templateId in create_plan
│   │   ├── templates.py          # NEW: GET /api/templates, GET /api/templates/{id}
│   │   ├── router.py             # MODIFY: Register template routes
│   │   └── [existing endpoints]
│   ├── services/
│   │   ├── plan_service.py       # MODIFY: Handle templateId
│   │   ├── template_service.py   # NEW: Manage template config
│   │   └── [existing services]
│   ├── config/
│   │   └── templates.py          # NEW: Template configurations (home_purchase, emergency_fund)
│   ├── alembic/
│   │   └── versions/
│   │       └── [new_migration].py # NEW: Add template_id to plans table
│   └── tests/
│       ├── test_api/
│       │   ├── test_templates.py      # NEW
│       │   └── [existing tests]
│       └── test_services/
│           ├── test_template_service.py # NEW
│           └── [existing tests]

docs/
├── TEMPLATE_SELECTION_FLOW.md    # NEW: UX flow documentation
└── [existing docs]
```

**Structure Decision**:

This feature uses Option 2 (Web application with frontend + backend):

- **Marketing app** (`/marketing/`): Hosts landing page with CTA button pointing to template selection
- **Frontend app** (`/frontend/`): Hosts template selection page and plan wizard with template-aware logic
- **Backend app** (`/backend/`): Provides template API endpoints and enhanced plan creation with template tracking

**Key Architectural Decisions**:

1. Template selection page lives in both marketing (primary) and frontend (fallback) for routing flexibility
2. Database schema extended minimally: add `template_id` FK to existing Plan table
3. Template configurations stored as Python constants (no DB config needed for MVP)
4. Context and hooks enhanced to track selected template throughout wizard flow

---

## Phase 0: Research & Clarification

### Research Tasks

1. **Template Configuration Pattern**
   - Research appropriate patterns for storing template metadata (home purchase vs emergency fund)
   - Determine if Python config constants are sufficient or if DB storage needed for future extensibility
   - Review best practices for multi-template form wizards

2. **Existing Plan Wizard Integration**
   - Analyze current `/plan` page structure and wizard flow
   - Map existing form steps to template concept
   - Identify where template_id needs to flow through context

3. **Multi-App Navigation**
   - Research Next.js linking strategy across isolated apps (marketing → frontend)
   - Determine best approach for passing template context between apps
   - Evaluate direct URL navigation vs API coordination

4. **Responsive Design Patterns**
   - Research Tailwind CSS patterns for template selection card grids (1 col mobile, 2 col desktop)
   - Determine skeleton loading pattern compatibility

### Deliverable

**research.md** containing:

- Selected template configuration approach (config constants + schema design)
- Integration points in existing plan wizard
- Navigation pattern decision (URL params, context, API)
- Responsive design reference implementation

---

## Phase 1: Design & Contracts

### 1.1 Data Model (`data-model.md`)

**New/Modified Entities**:

- **PlanTemplate** (Configuration, not DB table for MVP)
  - id: string (e.g., "home_purchase", "emergency_fund")
  - name_vi: string
  - description_vi: string
  - icon: string (emoji or icon name)
  - status: enum ("available", "coming_soon")
  - wizard_steps: List[string] - e.g., ["goal", "amount", "assets", "debt", "savings", "timeline"]

- **Plan** (Existing - to be modified)
  - +template_id: string (FK to PlanTemplate.id) - NEW FIELD
  - user_id: int
  - name: string
  - description: optional string
  - created_at: datetime
  - updated_at: datetime

- **PlanContext** (Frontend state model)
  - selectedTemplate: PlanTemplate | null
  - planId: number | null
  - currentStep: string
  - draftData: Record<string, any>

### 1.2 Contracts (`contracts/` directory)

**contracts/template-selection-api.md**:

- `GET /api/templates` → List[TemplateResponse]
- `GET /api/templates/{template_id}` → TemplateResponse

**contracts/plan-creation-api.md**:

- `POST /api/plans` → Accept templateId in request body
- Response includes template_id field

### 1.3 Quickstart (`quickstart.md`)

**Frontend Developer Quickstart**:

1. Component: TemplateSelectionPage renders TemplateSelectionCard for each template
2. Hook: useTemplateSelection() manages template selection state
3. Navigation: On select, navigate to /plan with template in URL or context
4. Context: PlanContext stores selectedTemplate through wizard steps

**Backend Developer Quickstart**:

1. Config: Define templates in backend/src/config/templates.py
2. API: TemplateService queries config and returns Template responses
3. Schema: PlanCreate accepts optional template_id parameter
4. Migration: Add template_id column to plans table

### 1.4 Agent Context Update

After this phase, run:

```bash
./.specify/scripts/bash/update-agent-context.sh copilot
```

This updates GitHub Copilot context with:

- Template configuration patterns
- Multi-app routing decisions
- Modified Plan model structure
- New API contracts

---

## Phase 2: Task Generation

After Phase 1 design is complete, run:

```bash
/speckit.tasks
```

This generates `tasks.md` with actionable, dependency-ordered tasks covering:

1. **Database Migration** (Backend)
   - Create Alembic migration to add template_id to plans table
   - Set default template_id="home_purchase" for backward compatibility

2. **Backend API & Config** (Backend)
   - Implement PlanTemplate config in backend/src/config/templates.py
   - Create TemplateService in backend/src/services/template_service.py
   - Add GET /api/templates endpoints
   - Modify PlanCreate schema and create_plan() endpoint to accept template_id

3. **Frontend Components** (Frontend)
   - Create TemplateSelectionCard component
   - Create TemplateSelectionPage component
   - Add plan-templates route at /plan-templates

4. **Frontend Navigation & State** (Frontend)
   - Create lib/templates.ts with template definitions mirror
   - Create useTemplateSelection hook
   - Modify PlanContext to include selectedTemplate
   - Modify usePlan to preserve template through wizard steps
   - Update /plan/page.tsx to respect selected template
   - Update routing logic to require template selection before wizard

5. **Marketing CTA Integration** (Marketing)
   - Verify landing page CTA button exists
   - Point CTA to /plan-templates or frontend equivalent
   - Test navigation flow from marketing to template selection

6. **Testing** (All)
   - Write tests for template selection component
   - Write tests for template API endpoints
   - Write tests for template context persistence
   - E2E test: landing → template selection → plan wizard
