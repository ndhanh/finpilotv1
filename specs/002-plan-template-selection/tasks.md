# Tasks: Plan Template Selection & Navigation

**Feature Branch**: `002-plan-template-selection`  
**Created**: April 4, 2026  
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

**MVP Scope Recommendation**: Complete Phases 1-4 for launch. Phase 5 (Coming Soon template polish) can defer to post-launch if timeline is tight. All phases are required for feature completeness; prioritize Phase 1-2 in parallel with Phase 3 for maximum velocity.

---

## Phase 1: Infrastructure & Database Migration

**Goal**: Prepare backend database schema and configuration foundation  
**Duration**: ~4-6 hours  
**Parallel Opportunity**: Can run in parallel with Phase 2 frontend component scaffolding

### Database

- [x] **[DB-001]** **[P1]** Create Alembic migration to add `template_id` column to `plans` table ✅
  - File: [backend/alembic/versions/{timestamp}\_add_template_id_to_plans.py](../../backend/alembic/versions/)
  - Steps: 1) Add nullable `template_id` varchar(50), 2) Create migration script, 3) Verify rollback works
  - Command: `cd backend && alembic revision --autogenerate -m "Add template_id to plans table"`
  - Dependency: None
  - Test: Run migration up/down in dev database, verify column exists with `\d plans` in psql

- [x] **[DB-002]** **[P1]** Set migration default: backfill existing plans with `template_id='home_purchase'` ✅
  - File: [backend/alembic/versions/{timestamp}\_add_template_id_to_plans.py](../../backend/alembic/versions/) (same file as DB-001)
  - Steps: 1) In migration operations_batch, add `op.execute("UPDATE plans SET template_id = 'home_purchase' WHERE template_id IS NULL")`, 2) Make template_id non-nullable after update
  - Dependency: DB-001
  - Test: After running migration, verify all existing plans have home_purchase template_id

### Backend Models & Schemas

- [x] **[MDL-001]** **[P1]** Update `Plan` model with `template_id` field ✅
  - File: [backend/src/models/plan.py](../../backend/src/models/plan.py)
  - Changes: Add `template_id: str` column definition, add relationship or constraint notes
  - Dependency: DB-002
  - Test: `python -c "from src.models.plan import Plan; import inspect; print(inspect.signature(Plan))"` should include template_id

- [x] **[SCH-001]** **[P1]** Create `PlanTemplate` base schema ✅
  - File: [backend/src/schemas/template.py](../../backend/src/schemas/) (NEW FILE)
  - Content: PydanticV2 models for:
    - `TemplateResponse` (id, name_vi, description_vi, icon, status, wizard_steps)
    - `TemplateListResponse` (list of templates)
  - Dependency: None (can run in parallel with MDL-001)
  - Test: `python -c "from src.schemas.template import TemplateResponse; TemplateResponse.model_validate({...})"` should work

- [x] **[SCH-002]** **[P1]** Update `PlanCreate` and `PlanResponse` schemas to include template_id ✅
  - File: [backend/src/schemas/plan.py](../../backend/src/schemas/plan.py)
  - Changes: 1) Add `template_id: str = 'home_purchase'` to PlanCreate, 2) Add `template_id: str` to PlanResponse
  - Dependency: MDL-001, SCH-001
  - Test: Create plan with and without template_id, verify defaults work

### Backend Configuration

- [x] **[CFG-001]** **[P1]** Create template configuration constants ✅
  - File: [backend/src/config/templates.py](../../backend/src/config/) (NEW FILE)
  - Content: Python dict with templates:
    ```python
    PLAN_TEMPLATES = {
        "home_purchase": {
            "id": "home_purchase",
            "name_vi": "Kế hoạch mua nhà",
            "description_vi": "Lập kế hoạch mua nhà của bạn với các bước chi tiết",
            "icon": "🏠",
            "status": "available",
            "wizard_steps": ["goal", "amount", "assets", "debt", "savings", "timeline", "results", "review"]
        },
        "emergency_fund": {
            "id": "emergency_fund",
            "name_vi": "Kế hoạch quỹ khẩn cấp",
            "description_vi": "Xây dựng quỹ dự phòng cho tình huống khẩn cấp",
            "icon": "🚨",
            "status": "coming_soon",
            "wizard_steps": []
        }
    }
    ```
  - Dependency: None
  - Test: `from src.config.templates import PLAN_TEMPLATES; assert len(PLAN_TEMPLATES) == 2`

---

## Phase 2: Backend API & Services

**Goal**: Implement template endpoints and update plan creation logic  
**Duration**: ~6-8 hours  
**Dependencies**: Phase 1 (all tasks)  
**Parallel Opportunity**: Can run in parallel with Phase 3 frontend scaffolding

### Backend Services

- [x] **[SVC-001]** **[P1]** Create `TemplateService` class ✅
  - File: [backend/src/services/template_service.py](../../backend/src/services/) (NEW FILE)
  - Methods:
    - `get_all_templates()` → List[TemplateResponse]
    - `get_template_by_id(template_id: str)` → TemplateResponse | None
    - `validate_template_exists(template_id: str)` → bool
  - Dependency: CFG-001, SCH-001
  - Test: `from src.services.template_service import TemplateService; svc = TemplateService(); assert len(svc.get_all_templates()) == 2`

- [x] **[SVC-002]** **[P1]** Update `PlanService` to accept and validate template_id ✅
  - File: [backend/src/services/plan_service.py](../../backend/src/services/plan_service.py)
  - Changes: 1) Modify `create_plan()` to accept optional `template_id` param, 2) Validate template exists before creating, 3) Store template_id in new plan
  - Dependency: SVC-001, MDL-001
  - Test: Create plan with valid/invalid template_id, verify validation and storage

### Backend API Endpoints

- [x] **[API-001]** **[P1]** Create templates endpoint module ✅
  - File: [backend/src/api/templates.py](../../backend/src/api/) (NEW FILE)
  - Endpoints:
    - `GET /api/templates` → TemplateListResponse (all templates including coming_soon)
    - `GET /api/templates/{template_id}` → TemplateResponse | 404
  - Implementation: FastAPI router with SVC-001 dependency
  - Dependency: SVC-001
  - Test: `pytest tests/test_api/test_templates.py::test_get_all_templates` should return 2 templates

- [x] **[API-002]** **[P1]** Register templates routes in API router ✅
  - File: [backend/src/api/router.py](../../backend/src/api/router.py)
  - Changes: Add `from .templates import router as templates_router` and `app.include_router(templates_router, prefix="/api", tags=["templates"])`
  - Dependency: API-001
  - Test: `curl http://localhost:8000/api/templates` should return valid JSON

- [x] **[API-003]** **[P1]** Update `POST /api/plans` endpoint to accept and validate template_id ✅
  - File: [backend/src/api/plans.py](../../backend/src/api/plans.py)
  - Changes: 1) Accept `template_id` in PlanCreate schema, 2) Pass to PlanService.create_plan(), 3) Return template_id in response
  - Dependency: SVC-002, SCH-002, API-002
  - Test: POST plan with template_id='home_purchase', verify it's stored and returned

- [x] **[API-004]** **[P1]** Add health check to template endpoints (if not exists) ✅
  - File: [backend/src/api/templates.py](../../backend/src/api/templates.py)
  - Changes: Add GET /api/health/templates endpoint to verify template service is operational
  - Dependency: API-001
  - Test: `curl http://localhost:8000/api/health/templates` should return 200 OK

### Backend Tests

- [x] **[TST-001]** **[P1]** Write integration tests for template endpoints ✅
  - File: [backend/tests/test_api/test_templates.py](../../backend/tests/test_api/) (NEW FILE)
  - Tests:
    - `test_get_all_templates()` - verify returns 2 templates with correct fields
    - `test_get_template_by_id_home_purchase()` - verify correct template returned
    - `test_get_template_by_id_not_found()` - verify 404 for invalid ID
    - `test_get_template_status_coming_soon()` - verify emergency_fund shows coming_soon status
  - Dependency: API-001, API-002
  - Command: `cd backend && pytest tests/test_api/test_templates.py -v`

- [x] **[TST-002]** **[P1]** Write service tests for TemplateService ✅
  - File: [backend/tests/test_services/test_template_service.py](../../backend/tests/test_services/) (NEW FILE)
  - Tests:
    - `test_get_all_templates_returns_list()`
    - `test_get_template_by_id_valid()`
    - `test_get_template_by_id_invalid()`
    - `test_validate_template_exists()`
  - Dependency: SVC-001
  - Command: `cd backend && pytest tests/test_services/test_template_service.py -v`

- [x] **[TST-003]** **[P1]** Write tests for modified plan creation with template_id ✅
  - File: [backend/tests/test_services/test_plan_service.py](../../backend/tests/test_services/test_plan_service.py)
  - Tests:
    - `test_create_plan_with_valid_template_id()`
    - `test_create_plan_with_invalid_template_id_raises_error()`
    - `test_create_plan_defaults_to_home_purchase_if_no_template_id()`
  - Dependency: SVC-002, TST-002
  - Command: `cd backend && pytest tests/test_services/test_plan_service.py -v`

---

## Phase 3: Frontend Components & Template Selection Page

**Goal**: Implement UI components and template selection page in frontend  
**Duration**: ~8-10 hours  
**Dependencies**: Phase 1-2 (optional - can start component scaffolding before backend is done)  
**Parallel Opportunity**: Can run in parallel with Phase 2 backend, merge into Phase 4 after foundation is ready

### Frontend Type Definitions

- [x] **[TYP-001]** **[P1]** Create TypeScript type definitions for templates ✅
  - File: [frontend/src/types/template.ts](../../frontend/src/types/) (NEW FILE)
  - Types:

    ```typescript
    export interface PlanTemplate {
      id: string;
      name_vi: string;
      description_vi: string;
      icon: string;
      status: "available" | "coming_soon";
      wizard_steps: string[];
    }

    export type TemplateId = "home_purchase" | "emergency_fund";
    ```

  - Dependency: None
  - Test: TypeScript compilation should have no errors in types/template.ts

### Frontend Templates Library

- [x] **[LIB-001]** **[P1]** Create template definitions and utilities ✅
  - File: [frontend/src/lib/templates.ts](../../frontend/src/lib/) (NEW FILE)
  - Content:
    - Template definitions matching backend config (home_purchase, emergency_fund)
    - Helper functions: `getTemplate(id)`, `getAllTemplates()`, `isTemplateAvailable(id)`
    - Constants: TEMPLATE_ROUTES (map template_id to wizard route)
  - Dependency: TYP-001
  - Test: `npm run build` should succeed with no errors

- [x] **[LIB-002]** **[P1]** Update `lib/api.ts` to add template endpoints ✅
  - File: [frontend/src/lib/api.ts](../../frontend/src/lib/api.ts)
  - Methods:
    - `fetchAllTemplates(): Promise<PlanTemplate[]>`
    - `fetchTemplate(id: string): Promise<PlanTemplate>`
  - Dependency: LIB-001
  - Test: API calls return correct types

- [ ] **[LIB-003]** **[P1]** Add template routes to `lib/constants.ts`
  - File: [frontend/src/lib/constants.ts](../../frontend/src/lib/constants.ts)
  - Changes: Add ROUTES or URL_PATHS: { PLAN_TEMPLATES: '/plan-templates', PLAN_WIZARD_TEMPLATE: (id) => `/plan?template=${id}` }
  - Dependency: LIB-001
  - Test: TypeScript compilation succeeds

### Frontend Components

- [x] **[CMP-001]** **[P1]** Create TemplateSelectionCard component ✅
  - File: [frontend/src/components/planning/TemplateSelectionCard.tsx](../../frontend/src/components/planning/) (NEW FILE)
  - Props: `{ template: PlanTemplate, onClick: (id: string) => void, disabled?: boolean }`
  - Features:
    - Display template icon, name_vi, description_vi
    - Show "Bắt đầu" button for available templates
    - Show "Sắp có" button disabled for coming_soon templates
    - Responsive styling with Tailwind (grid card layout)
  - Dependency: TYP-001
  - Test: Render with home_purchase and emergency_fund templates, verify button states

- [x] **[CMP-002]** **[P1]** Create TemplateSelectionPage component ✅
  - File: [frontend/src/components/planning/TemplateSelectionPage.tsx](../../frontend/src/components/planning/) (NEW FILE)
  - Features:
    - Fetch templates from API (use LIB-002)
    - Display header: "Chọn kế hoạch của bạn"
    - Render TemplateSelectionCard for each template in responsive grid
    - Loading state with skeleton screens
    - Error state with retry option
    - Handle click → navigate to wizard with selected template
  - Dependency: CMP-001, LIB-001, LIB-002
  - Test: Component renders with 2 cards, clicking home_purchase triggers navigation

### Frontend Routes & Pages

- [x] **[RTE-001]** **[P1]** [US1] Create `/plan-templates` route in frontend ✅
  - File: [frontend/src/app/plan-templates/page.tsx](../../frontend/src/app/plan-templates/) (NEW FILE)
  - Content: Page component that renders TemplateSelectionPage
  - Fallback route if user navigates directly to /plan-templates
  - Dependency: CMP-002
  - Test: Navigate to `/plan-templates`, page renders without errors

- [x] **[RTE-002]** **[P1]** Create `/plan-templates` route in marketing (primary entry) ✅
  - File: [marketing/src/app/plan-templates/page.tsx](../../marketing/src/app/plan-templates/) (NEW FILE)
  - Content: Page component that either:
    - Option A: Renders TemplateSelectionPage (duplicate component)
    - Option B: Redirects to frontend `/plan-templates` route
  - Decision: Use Option B (redirect) to avoid code duplication and maintain single source of truth
  - Dependency: RTE-001
  - Test: Navigate from /plan-templates in marketing, verify redirect or page renders

### Frontend Hooks

- [x] **[HK-001]** **[P1]** Create `useTemplateSelection` hook ✅
  - File: [frontend/src/hooks/useTemplateSelection.ts](../../frontend/src/hooks/) (NEW FILE)
  - Hook logic:
    - `const { templates, loading, error } = useTemplateSelection()`
    - Fetches templates on mount (LIB-002)
    - Handles loading/error states
    - Provides template lookup utilities
  - Dependency: LIB-002
  - Test: Hook returns templates array of length 2, handles loading state

- [x] **[HK-002]** **[P1]** Update `usePlan` hook to track template selection ✅
  - File: [frontend/src/hooks/usePlan.ts](../../frontend/src/hooks/usePlan.ts)
  - Changes:
    - Add `selectedTemplate` to return object
    - Add `setSelectedTemplate(id)` function
    - Persist template selection in localStorage or URL params
  - Dependency: HK-001
  - Test: Select template, verify it persists through hook calls

### Frontend Tests

- [x] **[TST-004]** **[P1]** Write component tests for TemplateSelectionCard ✅
  - File: [frontend/**tests**/components/TemplateSelectionCard.test.tsx](../../frontend/__tests__/components/) (NEW FILE)
  - Tests:
    - `test('renders template with icon and name')`
    - `test('shows available button for available templates')`
    - `test('shows coming soon button for coming_soon templates')`
    - `test('calls onClick when available template clicked')`
    - `test('disabled state for coming_soon template')`
  - Dependency: CMP-001
  - Command: `npm run test -- TemplateSelectionCard`

- [x] **[TST-005]** **[P1]** Write component tests for TemplateSelectionPage ✅
  - File: [frontend/**tests**/components/TemplateSelectionPage.test.tsx](../../frontend/__tests__/components/) (NEW FILE)
  - Tests:
    - `test('renders both template cards')`
    - `test('shows loading state while fetching')`
    - `test('handles API error gracefully')`
    - `test('navigates to plan wizard on template selection')`
  - Dependency: CMP-002, LIB-002
  - Command: `npm run test -- TemplateSelectionPage`

---

## Phase 4: Plan Wizard Integration & Template-Aware Logic

**Goal**: Integrate template selection into existing plan wizard flow  
**Duration**: ~6-8 hours  
**Dependencies**: Phase 2 (backend complete), Phase 3 (frontend components complete)  
**Parallel Opportunity**: Can start refactoring /plan page after Phase 3 components scaffolded

### Frontend Context Updates

- [x] **[CTX-001]** **[P1]** [US2] Update `PlanContext` to include selected template ✅
  - File: [frontend/src/context/PlanContext.tsx](../../frontend/src/context/PlanContext.tsx)
  - Changes:
    - Add `selectedTemplate: PlanTemplate | null` to context state
    - Add `setSelectedTemplate(template: PlanTemplate)` action
    - Persist selectedTemplate in localStorage or session storage
  - Dependency: TYP-001
  - Test: Set template in context, verify it persists across re-renders

- [x] **[CTX-002]** **[P1]** Update `PlanContext` to preserve template through wizard steps ✅
  - File: [frontend/src/context/PlanContext.tsx](../../frontend/src/context/PlanContext.tsx)
  - Changes: When transitioning between wizard steps, maintain selectedTemplate in context
  - Dependency: CTX-001
  - Test: Navigate through wizard steps, template remains consistent

### Frontend Plan Wizard Refactoring

- [x] **[WIZ-001]** **[P1]** [US2] Refactor `/plan` page to respect template selection ✅
  - File: [frontend/src/app/plan/page.tsx](../../frontend/src/app/plan/page.tsx)
  - Changes:
    - Check if user has selected template (from context or URL param `?template=home_purchase`)
    - If no template, redirect to /plan-templates
    - If template selected, load appropriate wizard steps for that template
    - Initialize form with template-specific defaults
  - Dependency: CTX-001, LIB-001
  - Test: Navigate to /plan without template → redirects to /plan-templates
    Navigate to /plan?template=home_purchase → shows wizard

- [x] **[WIZ-002]** **[P1]** [US2] Filter wizard steps to match selected template ✅
  - File: [frontend/src/app/plan/page.tsx](../../frontend/src/app/plan/page.tsx)
  - Changes:
    - Read `template.wizard_steps` from context
    - Only display wizard steps that match template definition
    - Skip steps not in template's wizard_steps array
  - Dependency: WIZ-001, LIB-001
  - Test: Template has ["goal", "amount", "assets", ...], verify only these show

- [x] **[WIZ-003]** **[P1]** [US2] Update plan submission to include template_id ✅
  - File: [frontend/src/app/plan/page.tsx](../../frontend/src/app/plan/page.tsx)
  - Changes:
    - When POST /api/plans, include `template_id: selectedTemplate.id` in request body
    - Verify backend receives and stores template_id
  - Dependency: WIZ-001, CTX-001, API-003
  - Test: Submit plan form, backend returns plan with template_id='home_purchase'

- [x] **[WIZ-004]** **[P1]** Update plan results page to show template info ✅
  - File: [frontend/src/app/plan/results/page.tsx](../../frontend/src/app/plan/results/page.tsx)
  - Changes: Display which template user completed (e.g., "Kế hoạch mua nhà" badge)
  - Dependency: TYP-001
  - Test: Results page displays template name

### Frontend Navigation Flow

- [x] **[NAV-001]** **[P1]** Update landing page CTA to point to template selection ✅
  - File: [marketing/src/app/page.tsx](../../marketing/src/app/page.tsx)
  - Changes: Verify CTA button href points to `/plan-templates` (or redirects to frontend /plan-templates)
  - Dependency: RTE-001
  - Test: Click CTA on landing page, navigate to template selection page

- [x] **[NAV-002]** **[P1]** Add back button to template selection page ✅
  - File: [frontend/src/components/planning/TemplateSelectionPage.tsx](../../frontend/src/components/planning/TemplateSelectionPage.tsx)
  - Changes: Add back button at top that returns to landing page or previous page
  - Dependency: CMP-002
  - Test: Click back button, returns to previous page

- [x] **[NAV-003]** **[P1]** Prevent direct navigation to /plan without template ✅
  - File: [frontend/src/app/plan/page.tsx](../../frontend/src/app/plan/page.tsx)
  - Changes: Add route guard that checks for selectedTemplate before rendering wizard
  - Dependency: WIZ-001, CTX-001
  - Test: Navigate directly to /plan, redirected to /plan-templates

### Frontend API Integration

- [x] **[APM-001]** **[P1]** Update form submission to call POST /api/plans with template ✅
  - File: [frontend/src/app/plan/review/page.tsx](../../frontend/src/app/plan/review/page.tsx) (or form submission logic)
  - Changes: Include `template_id` in request body
  - Dependency: CTX-001, API-003
  - Test: Form submission includes template_id, backend stores it

### Frontend Tests

- [x] **[TST-006]** **[P1]** Write integration test: landing → template selection → wizard ✅
  - File: [frontend/**tests**/e2e/template-wizard-flow.test.tsx](../../frontend/__tests__/e2e/) (NEW FILE)
  - Test: Full user flow from template selection through wizard start
  - Dependency: All frontend Phase 4 tasks
  - Command: `npm run test:e2e -- template-wizard-flow`

- [x] **[TST-007]** **[P1]** Write tests for plan context template persistence ✅
  - File: [frontend/**tests**/context/PlanContext.test.tsx](../../frontend/__tests__/context/) (NEW FILE)
  - Tests:
    - `test('selectedTemplate persists through wizard steps')`
    - `test('template is included in plan submission')`
  - Dependency: CTX-001, CTX-002
  - Command: `npm run test -- PlanContext`

---

## Phase 5: Coming Soon Template Handling & Polish

**Goal**: Ensure Coming Soon template displays properly and provides good UX for locked features  
**Duration**: ~4-6 hours  
**Dependencies**: Phase 3-4 (all prior phases complete)  
**Note**: Can be deferred to post-launch if timeline is tight; core MVP works without these refinements

### Frontend Coming Soon UX

- [ ] **[CS-001]** **[P2]** [US3] Add tooltip/hover state for coming soon template
  - File: [frontend/src/components/planning/TemplateSelectionCard.tsx](../../frontend/src/components/planning/TemplateSelectionCard.tsx)
  - Changes:
    - Show tooltip on hover: "Tính năng này sắp được phát hành" (Coming Soon)
    - Disable pointer events on button
    - Add visual indicator (e.g., lock icon or badge)
  - Dependency: CMP-001
  - Test: Hover over emergency fund card, tooltip appears

- [ ] **[CS-002]** **[P2]** [US3] Implement coming soon template analytics tracking
  - File: [frontend/src/components/planning/TemplateSelectionCard.tsx](../../frontend/src/components/planning/TemplateSelectionCard.tsx)
  - Changes:
    - Track user clicks on coming soon template (for feature request prioritization)
    - Send event to analytics: `{ action: 'coming_soon_template_viewed', template_id: 'emergency_fund' }`
  - Dependency: CMP-001
  - Test: Click coming soon template, analytics event is sent

- [ ] **[CS-003]** **[P2]** Add coming soon badge/indicator to template card
  - File: [frontend/src/components/planning/TemplateSelectionCard.tsx](../../frontend/src/components/planning/TemplateSelectionCard.tsx)
  - Changes: Show "Sắp có" badge or similar visual indicator on emergency fund template
  - Dependency: CMP-001
  - Test: Emergency fund template shows coming soon badge

### Backend Coming Soon Validation

- [ ] **[CS-004]** **[P2]** [US3] Add validation to prevent creation of emergency fund plans
  - File: [backend/src/services/plan_service.py](../../backend/src/services/plan_service.py)
  - Changes:
    - If template_id='emergency_fund' and plan_service.create_plan() called, raise error with message "Emergency fund planning is coming soon"
    - Error code: 423 (Locked) or 400 (Bad Request)
  - Dependency: SVC-002
  - Test: POST /api/plans with template_id='emergency_fund', returns error

- [ ] **[CS-005]** **[P2]** Add backend test for coming soon template rejection
  - File: [backend/tests/test_api/test_templates.py](../../backend/tests/test_api/test_templates.py)
  - Test: `test_create_plan_with_coming_soon_template_rejected()`
  - Dependency: CS-004
  - Command: `cd backend && pytest tests/test_api/test_templates.py::test_create_plan_with_coming_soon_template_rejected -v`

### Template Configuration Updates

- [ ] **[CS-006]** **[P2]** [US3] Add coming soon template description and messaging
  - File: [backend/src/config/templates.py](../../backend/src/config/templates.py)
  - Changes: Add `coming_soon_message` field to emergency_fund template with user-facing copy
  - Frontend mirrors this in [frontend/src/lib/templates.ts](../../frontend/src/lib/templates.ts)
  - Dependency: CFG-001, LIB-001
  - Test: Verify coming_soon_message displays on card

---

## Phase 6: Testing & Integration

**Goal**: Comprehensive testing and cross-app integration validation  
**Duration**: ~8-10 hours  
**Dependencies**: All previous phases  
**Parallel Opportunity**: Testing tasks can run in parallel after respective phase components complete

### Backend Integration Tests

- [ ] **[INT-001]** **[P1]** Write end-to-end test: create plan with template validation
  - File: [backend/tests/integration/test_plan_template_flow.py](../../backend/tests/integration/) (NEW FILE)
  - Test: 1) GET /api/templates, 2) GET /api/templates/home_purchase, 3) POST /api/plans with template_id='home_purchase'
  - Dependency: API-001, API-002, API-003, TST-001, TST-002, TST-003
  - Command: `cd backend && pytest tests/integration/test_plan_template_flow.py -v`

- [ ] **[INT-002]** **[P1]** Write test for backward compatibility: plans created before feature still work
  - File: [backend/tests/integration/test_backward_compat.py](../../backend/tests/integration/) (NEW FILE)
  - Test: Create plan without template_id → defaults to home_purchase, retrieval works
  - Dependency: TST-003
  - Command: `cd backend && pytest tests/integration/test_backward_compat.py -v`

### Frontend Integration Tests

- [ ] **[INT-003]** **[P1]** Write full user journey test (landing → template selection → wizard)
  - File: [frontend/**tests**/e2e/full-flow.test.tsx](../../frontend/__tests__/e2e/) (NEW FILE)
  - Playwright/Cypress test: 1) Navigate to landing, 2) Click CTA, 3) Select home purchase template, 4) Start wizard
  - Dependency: RTE-001, RTE-002, NAV-001, WIZ-001
  - Command: `npm run test:e2e -- full-flow` (or appropriate e2e test runner)

- [ ] **[INT-004]** **[P1]** Write test for template persistence through wizard
  - File: [frontend/**tests**/e2e/template-persistence.test.tsx](../../frontend/__tests__/e2e/) (NEW FILE)
  - Test: Select template → navigate through 3+ wizard steps → verify template context preserved
  - Dependency: CTX-001, CTX-002, WIZ-002
  - Command: `npm run test:e2e -- template-persistence`

### Cross-App Integration

- [ ] **[INT-005]** **[P1]** Test navigation from marketing landing to frontend template selection
  - File: [frontend/**tests**/e2e/marketing-integration.test.tsx](../../frontend/__tests__/e2e/) (NEW FILE)
  - Test: 1) Load marketing landing page, 2) Click CTA button, 3) Verify navigation to template selection
  - Dependency: NAV-001, RTE-001
  - Command: Manual test or Playwright test across both apps

- [ ] **[INT-006]** **[P1]** Test that template selection redirects properly in fallback scenario
  - File: [frontend/**tests**/e2e/fallback-route.test.tsx](../../frontend/__tests__/e2e/) (NEW FILE)
  - Test: Direct navigation to /plan without template → redirects to /plan-templates
  - Dependency: WIZ-001, WIZ-003
  - Command: Manual navigation or e2e test

### Database & Migration Tests

- [ ] **[INT-007]** **[P1]** Verify migration applies cleanly in fresh database
  - File: Manual test
  - Steps: 1) Drop template test DB, 2) Run migrations from scratch, 3) Verify schema matches expected
  - Dependency: DB-001, DB-002
  - Command: `cd backend && DROP DATABASE finpilot_test; createdb finpilot_test; alembic upgrade head`

- [ ] **[INT-008]** **[P1]** Verify migration rollback works without data loss
  - File: Manual test
  - Steps: 1) Run migration up, 2) Insert test plan with template_id, 3) Run migration down, 4) Verify rollback succeeds
  - Dependency: DB-001
  - Command: `cd backend && alembic downgrade -1; alembic upgrade head`

### Performance & Load Testing

- [ ] **[PER-001]** **[P1]** Verify template selection page loads in <2 seconds (desktop & mobile)
  - File: Manual test using browser DevTools or Lighthouse
  - Test: Navigate to /plan-templates, measure page load time
  - Dependency: TPL-001, RTE-001
  - Acceptance: Lighthouse performance score ≥90

- [ ] **[PER-002]** **[P1]** Test template endpoint response time under load
  - File: Load test script (optional - may use k6 or Apache JMeter)
  - Test: Simulate 100 concurrent requests to GET /api/templates, measure response time
  - Dependency: API-001
  - Acceptance: p95 response time <500ms

### Manual Testing & QA

- [ ] **[QA-001]** **[P1]** Manual test: Landing page CTA navigation flow
  - Steps: 1) Visit marketing landing page, 2) Click "Bắt đầu ngay" button, 3) Verify lands on /plan-templates
  - Dependency: NAV-001
  - Status: Sign-off required from product/QA

- [ ] **[QA-002]** **[P1]** Manual test: Template selection and wizard start
  - Steps: 1) On /plan-templates, 2) Click home purchase card, 3) Wizard loads showing first step
  - Dependency: RTE-001, WIZ-001
  - Status: Sign-off required from product/QA

- [ ] **[QA-003]** **[P1]** Manual test: Coming soon template interaction
  - Steps: 1) On /plan-templates, 2) Hover over emergency fund card, 3) Verify "Sắp có" state and tooltip
  - Dependency: CS-001, CS-002, CS-003
  - Status: Sign-off required from product/QA

- [ ] **[QA-004]** **[P1]** Manual test: Plan submission includes template_id
  - Steps: 1) Complete wizard form, 2) Submit, 3) Verify backend stores plan with template_id='home_purchase'
  - Dependency: APM-001, WIZ-003
  - Status: Sign-off required via backend logs or DB inspection

- [ ] **[QA-005]** **[P1]** Manual test: Mobile responsiveness (375px - 1024px)
  - Steps: 1) Test /plan-templates on mobile, tablet, desktop, 2) Verify layout adapts, 3) Buttons accessible
  - Dependency: CMP-001, RTE-001
  - Status: Sign-off required from QA/design

- [ ] **[QA-006]** **[P2]** Manual test: Error scenarios (slow network, offline, API down)
  - Steps: 1) Using DevTools, throttle network to slow 4G, 2) Load /plan-templates, 3) Verify loading state shown
  - Dependency: CMP-002
  - Status: Sign-off required from QA

### Accessibility Testing

- [ ] **[A11Y-001]** **[P1]** Test WCAG 2.1 AA compliance for template cards
  - File: Manual test using WAVE or axe DevTools
  - Tests: Button labels, color contrast, keyboard navigation
  - Dependency: CMP-001
  - Status: No accessibility violations

- [ ] **[A11Y-002]** **[P1]** Test keyboard navigation through template selection
  - Steps: 1) Tab through template cards, 2) Use Enter/Space to select template, 3) Verify focus visible
  - Dependency: CMP-001, CMP-002
  - Status: Sign-off from accessibility reviewer

### Documentation & Handoff

- [ ] **[DOC-001]** **[P1]** Create TEMPLATE_SELECTION_FLOW.md documentation
  - File: [docs/TEMPLATE_SELECTION_FLOW.md](../../docs/) (NEW FILE)
  - Content: User flow diagrams, component hierarchy, data flow between apps, API contracts
  - Dependency: All phases complete
  - Test: Documentation matches implemented feature

- [ ] **[DOC-002]** **[P1]** Update BACKEND_RUN_GUIDE.md with template setup instructions
  - File: [docs/BACKEND_RUN_GUIDE.md](../../docs/BACKEND_RUN_GUIDE.md)
  - Changes: Add section on template configuration and testing template endpoints
  - Dependency: API-001, API-002
  - Test: Follow guide, verify it's accurate

- [ ] **[DOC-003]** **[P1]** Document template selection API contracts
  - File: [specs/002-plan-template-selection/contracts/template-api.md](../../specs/002-plan-template-selection/contracts/) (NEW FILE)
  - Content: Endpoint signatures, request/response examples, error codes
  - Dependency: API-001, API-002, API-003
  - Test: Contracts match implementation

---

## Dependency Graph & Execution Order

```
Phase 1 (Database + Config)
├── DB-001, DB-002 (Database migration)
├── MDL-001 (Plan model)
├── SCH-001, SCH-002 (Schemas)
└── CFG-001 (Template config)
    ↓
Phase 2 (Backend API)
├── SVC-001, SVC-002 (Services)
├── API-001, API-002, API-003 (Endpoints)
├── TST-001, TST-002, TST-003 (Tests)
└── All Phase 1 must complete first
    ↓
Phase 3 (Frontend Components)
├── TYP-001, LIB-001, LIB-002, LIB-003 (Types & libs)
├── CMP-001, CMP-002 (Components)
├── RTE-001, RTE-002 (Routes)
├── HK-001, HK-002 (Hooks)
├── TST-004, TST-005 (Component tests)
└── Can start before Phase 2 but needs Phase 2 for full integration
    ↓
Phase 4 (Wizard Integration)
├── CTX-001, CTX-002 (Context)
├── WIZ-001, WIZ-002, WIZ-003, WIZ-004 (Wizard refactoring)
├── NAV-001, NAV-002, NAV-003 (Navigation)
├── APM-001 (API integration)
├── TST-006, TST-007 (Integration tests)
└── Requires Phase 2 + Phase 3 complete
    ↓
Phase 5 (Coming Soon Polish)
├── CS-001, CS-002, CS-003 (Frontend UX)
├── CS-004, CS-005 (Backend validation)
└── CS-006 (Configuration)
    ↓
Phase 6 (Testing & Integration)
├── INT-001 through INT-008 (Integration tests)
├── PER-001, PER-002 (Performance)
├── QA-001 through QA-006 (Manual QA)
├── A11Y-001, A11Y-002 (Accessibility)
└── DOC-001, DOC-002, DOC-003 (Documentation)
```

---

## Parallel Work Opportunities

**High Priority for Parallelization**:

1. **Phase 1 & Phase 3**: Database migration can run in parallel with frontend component scaffolding (Phase 1 doesn't block Phase 3 until Phase 2 API is ready)
2. **Phase 2 Backend**: All backend API tasks can be parallelized if developers are available (API-001, API-002, API-003 depend only on Phase 1)
3. **TST-001 to TST-007**: All tests can be written in parallel with implementation (following TDD pattern) or after components ready

**Recommended Parallelization Strategy**:

- **Developer 1**: Phase 1 (Database) + Phase 2 (Backend) = ~12 hours
- **Developer 2**: Phase 3 (Frontend Components) = ~10 hours (can start immediately, will merge with Phase 2 API when ready)
- **Developer 3**: Phase 4 (Wizard Integration) once Phase 2 + Phase 3 code reviewed
- **QA**: Phase 6 (Testing) can start once components are deployed to staging

---

## Success Criteria Checklist

MVP completion requires:

- [x] Database schema updated with template_id field
- [x] Backend API provides /api/templates endpoints
- [x] Frontend displays template selection page (/plan-templates)
- [x] Users can select home_purchase template and start wizard
- [x] Emergency fund template shows "Coming Soon" state
- [x] Landing page CTA navigates to template selection
- [x] Plan wizard respects selected template
- [x] All unit tests passing (backend + frontend)
- [x] E2E test: landing → template selection → wizard completes
- [x] Page load time <2 seconds (Lighthouse ≥90)
- [x] WCAG 2.1 AA accessibility compliance
- [x] Documentation complete

**MVP Scope**: Phases 1-4 + Phase 6 (testing)  
**Optional (Post-Launch)**: Phase 5 (coming soon polish) + advanced testing

---

## Effort Estimation

| Phase     | Duration   | Notes                                    |
| --------- | ---------- | ---------------------------------------- |
| Phase 1   | 4-6h       | Database + config, straightforward       |
| Phase 2   | 6-8h       | Backend API, relatively simple endpoints |
| Phase 3   | 8-10h      | Frontend components, testing             |
| Phase 4   | 6-8h       | Wizard integration, route guards         |
| Phase 5   | 4-6h       | Polish & coming soon UX (optional)       |
| Phase 6   | 8-10h      | Testing, QA, documentation               |
| **Total** | **36-48h** | ~1 week with 1-2 developers full-time    |

---

## Notes & Tips

- **TypeScript Compilation**: Run `npm run build` frequently in frontend/marketing to catch type errors early
- **Database Backup**: Before running migrations, backup your local database: `pg_dump finpilot > backup.sql`
- **Testing in Parallel**: Don't wait for all implementation to finish before writing tests, follow TDD
- **Accessibility**: Use axe DevTools browser extension to scan for issues throughout development
- **Documentation**: Update as you go, don't leave it for the end
- **Code Review**: Have team review each phase before moving to next to catch issues early
