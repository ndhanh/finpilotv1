---
description: "Task list template for feature implementation"
---

# Tasks: FinPilot MVP Core

**Input**: Design documents from `/specs/001-mvp-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included for critical calculation logic and API contracts. E2E tests for user journeys.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Backend**: FastAPI with SQLAlchemy, pytest
- **Frontend**: Next.js 14 with TypeScript, Jest, Playwright

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Next.js 14 frontend project with TypeScript and TailwindCSS dependencies
- [x] T003 Initialize FastAPI backend project with SQLAlchemy and async support
- [x] T004 [P] Configure Docker Compose with PostgreSQL, backend, and frontend services
- [x] T005 [P] Setup ESLint and Prettier for frontend code quality
- [x] T006 [P] Setup black and isort for backend code formatting

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Setup PostgreSQL database schema with migrations (Alembic)
- [x] T008 [P] Implement JWT authentication with httpOnly cookies in backend/auth/security.py
- [x] T009 [P] Setup FastAPI routing structure and CORS middleware in backend/src/main.py
- [x] T010 Create base SQLAlchemy models (User, Plan) in backend/src/models/
- [x] T011 Configure error handling and structured logging in backend/src/utils/
- [x] T012 Implement deterministic projection calculation engine in backend/src/calculations/projection.py
- [x] T013 Implement rule-based recommendation engine in backend/src/calculations/rules.py
- [x] T014 Create Pydantic schemas for all API requests/responses in backend/src/schemas/
- [x] T015 Setup pytest fixtures for database and calculation testing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - House Purchase Planning Journey (Priority: P1) 🎯 MVP

**Goal**: Enable users to complete a full house purchase planning flow from onboarding to saved plan

**Independent Test**: User can start planning without login, answer 6 questions, see projection dashboard, and save plan

### Tests for User Story 1

- [ ] T016 [P] [US1] Unit tests for projection calculations in backend/tests/test_calculations/test_projection.py
- [ ] T017 [P] [US1] Unit tests for recommendation rules in backend/tests/test_calculations/test_rules.py
- [ ] T018 [P] [US1] API contract tests for projection endpoint in backend/tests/test_api/test_projections.py
- [ ] T019 [US1] E2E test for complete house purchase journey in frontend/**tests**/e2e/onboarding.spec.ts

### Implementation for User Story 1

- [x] T020 [P] [US1] Create Goal and GoalAssumptions models in backend/src/models/goal.py
- [x] T021 [P] [US1] Create FinancialSnapshot and ProjectionResult models in backend/src/models/
- [x] T022 [P] [US1] Create CalculationAudit model for audit trail in backend/src/models/audit.py
- [ ] T023 [US1] Implement goal service CRUD operations in backend/src/services/goal_service.py
- [ ] T024 [US1] Implement projection service with calculation orchestration in backend/src/services/projection_service.py
- [ ] T025 [US1] Implement plan service for saving/loading plans in backend/src/services/plan_service.py
- [ ] T026 [US1] Create projection API endpoint in backend/src/api/projections.py
- [ ] T027 [US1] Create goals API endpoints in backend/src/api/goals.py
- [ ] T028 [US1] Create plans API endpoints in backend/src/api/plans.py
- [ ] T029 [US1] Add VND formatting utilities in frontend/src/lib/formatting.ts
- [ ] T030 [US1] Create onboarding question components in frontend/src/components/planning/
- [ ] T031 [US1] Implement progressive data capture with localStorage in frontend/src/hooks/usePlan.ts
- [ ] T032 [US1] Create plan context for state management in frontend/src/context/PlanContext.tsx
- [x] T033 [US1] Build onboarding flow pages in frontend/src/app/plan/
- [ ] T034 [US1] Create projection chart component with Recharts in frontend/src/components/dashboard/ProjectionChart.tsx
- [ ] T035 [US1] Build results dashboard page in frontend/src/app/plan/results/page.tsx
- [ ] T036 [US1] Implement save plan prompt and signup flow in frontend/src/components/dashboard/SavePlanPrompt.tsx
- [ ] T037 [US1] Add API client wrapper for backend communication in frontend/src/lib/api.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Emergency Fund Planning Journey (Priority: P2)

**Goal**: Enable users to plan for emergency fund goals with simplified flow

**Independent Test**: User can select emergency fund goal, input basic details, see projection, and save plan

### Tests for User Story 2

- [ ] T038 [P] [US2] Unit tests for emergency fund calculations in backend/tests/test_calculations/test_emergency_fund.py
- [ ] T039 [US2] E2E test for emergency fund journey in frontend/**tests**/e2e/emergency-fund.spec.ts

### Implementation for User Story 2

- [ ] T040 [US2] Extend goal service for emergency fund logic in backend/src/services/goal_service.py
- [ ] T041 [US2] Add emergency fund calculation rules in backend/src/calculations/rules.py
- [ ] T042 [US2] Update goal API to support emergency fund type in backend/src/api/goals.py
- [ ] T043 [US2] Add emergency fund option to goal selection in frontend/src/app/plan/goal/page.tsx
- [ ] T044 [US2] Create emergency fund specific input flow in frontend/src/app/plan/emergency/
- [ ] T045 [US2] Adapt dashboard for emergency fund display in frontend/src/components/dashboard/

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Plan Management and Updates (Priority: P3)

**Goal**: Enable returning users to view, update, and manage their saved plans

**Independent Test**: Authenticated user can login, view saved plans, update plan details, and see updated projections

### Tests for User Story 3

- [ ] T046 [P] [US3] API contract tests for plan CRUD in backend/tests/test_api/test_plans.py
- [ ] T047 [US3] E2E test for plan management flow in frontend/**tests**/e2e/plan-management.spec.ts

### Implementation for User Story 3

- [ ] T048 [US3] Implement user service for profile management in backend/src/services/user_service.py
- [ ] T049 [US3] Create user API endpoints in backend/src/api/users.py
- [ ] T050 [US3] Add authentication API endpoints in backend/src/api/auth.py
- [ ] T051 [US3] Create dashboard layout for authenticated users in frontend/src/app/dashboard/layout.tsx
- [ ] T052 [US3] Build plan list page in frontend/src/app/dashboard/page.tsx
- [ ] T053 [US3] Create individual plan view page in frontend/src/app/dashboard/plan/[id]/page.tsx
- [ ] T054 [US3] Implement plan edit flow in frontend/src/app/dashboard/plan/[id]/edit/page.tsx
- [ ] T055 [US3] Add auth context and hooks in frontend/src/context/AuthContext.tsx and frontend/src/hooks/useAuth.ts
- [ ] T056 [US3] Create login/signup forms in frontend/src/components/auth/
- [ ] T057 [US3] Add protected route middleware in frontend/src/middleware.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final polish, localization, and production readiness

- [ ] T058 Add Vietnamese localization strings in frontend/src/lib/i18n/
- [ ] T059 Implement Vietnamese date formatting (DD/MM/YYYY) in frontend/src/lib/formatting.ts
- [ ] T060 Add comprehensive error boundaries in frontend/src/components/common/ErrorBoundary.tsx
- [ ] T061 Implement loading states and skeletons in frontend/src/components/common/
- [ ] T062 Add accessibility features (ARIA labels, keyboard navigation) throughout frontend
- [ ] T063 Setup production Docker configuration with nginx reverse proxy
- [ ] T064 Add health check endpoints in backend/src/api/health.py
- [ ] T065 Implement rate limiting on auth endpoints in backend/src/middleware/
- [ ] T066 Add GDPR-style data export functionality in backend/src/api/users.py
- [ ] T067 Performance optimization: Add database indexes and query optimization
- [ ] T068 Security audit: Input validation, SQL injection prevention, XSS protection
- [ ] T069 Add comprehensive logging and monitoring setup
- [ ] T070 Final E2E test suite for all user journeys

---

## Dependencies & Parallel Execution

**Critical Path** (must complete in sequence):
T001 → T002-T003 → T004 → T007 → T008-T009 → T010-T011 → T012-T013 → T014-T015

**Parallel Opportunities**:

- Frontend setup (T002, T005, T006) can run parallel to backend setup
- Model creation (T020-T022) can run parallel to service implementation
- Component development (T029-T037) can run parallel to API development
- Auth implementation (T048-T057) can run after foundation but parallel to other stories

**Milestone Checkpoints**:

- **Week 1 End**: Setup complete, foundation started
- **Week 2 End**: Foundation complete, US1 implementation started
- **Week 3 End**: US1 complete, US2 and US3 in progress
- **Week 4 End**: All stories complete, polish and testing

---

## Implementation Strategy

**MVP First**: Focus on US1 (House Purchase) as the primary MVP deliverable. US2 and US3 are enhancements.

**Incremental Delivery**: Each user story delivers independent value and can be tested/deployed separately.

**Technical Debt**: No shortcuts on security (JWT, input validation) or calculations (deterministic math).

**Testing Priority**: Calculation accuracy > API contracts > E2E flows > UI polish.

---

**Version**: 1.0 | **Total Tasks**: 70 | **Estimated Duration**: 4 weeks | **Team Size**: 2-3 developers
