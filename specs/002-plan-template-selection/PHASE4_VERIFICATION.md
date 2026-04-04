# Phase 4 Home Purchase Flow - Verification Complete ✅

**Review Date**: April 4, 2026  
**Status**: All systems verified and working correctly

---

## Navigation Fix Summary

### Problem Identified

TemplateSelectionPage was using incorrect route pattern:

```typescript
// ❌ BEFORE (non-existent route structure)
router.push(`/plan/${templateId}/income`); // → /plan/home_purchase/income
```

### Solution Applied

Updated to use URL parameter approach:

```typescript
// ✅ AFTER (correct route guard pattern)
router.push(`/plan?template=${templateId}`); // → /plan?template=home_purchase
```

### Why This Works

The `/plan/page.tsx` route guard:

1. Extracts `template=home_purchase` from URL params
2. Validates template exists
3. Stores in React context via `setSelectedTemplate()`
4. Redirects to template's first wizard step
5. Uses `getTemplateStartRoute('home_purchase')` → `/plan/goal`

---

## Route Structure Verified ✓

All wizard step routes exist and accessible:

```
/plan/
├── page.tsx (route guard)
├── goal/
│   └── page.tsx ← First step (home_purchase starts here)
├── amount/
│   └── page.tsx
├── assets/
│   └── page.tsx
├── debt/
│   └── page.tsx
├── savings/
│   └── page.tsx
├── timeline/
│   └── page.tsx
├── results/
│   └── page.tsx
└── review/
    └── page.tsx
```

Home purchase wizard_steps mapping:

```javascript
// lib/templates.ts
wizard_steps: ['goal', 'amount', 'assets', 'debt', 'savings', 'timeline', 'results', 'review']
              ↓
              /plan/{step}/page.tsx
```

---

## Complete Home Purchase User Flow

### Step-by-Step Navigation

```
1. User on marketing landing page
   └─ Clicks "Bắt đầu lập kế hoạch" CTA
      └─ Points to /plan-templates (via getAppPlanUrl())

2. TemplateSelectionPage (/plan-templates)
   └─ User clicks "Bắt đầu" button for home_purchase template
      └─ handleTemplateSelect('home_purchase')
         ├─ setSelectedTemplate(template) [context state]
         └─ router.push('/plan?template=home_purchase')

3. Route Guard (/plan?template=home_purchase)
   └─ /plan/page.tsx useEffect triggers
      ├─ Detects URL param: ?template=home_purchase
      ├─ selectedTemplate is undefined (first visit)
      ├─ Gets template object: getTemplate('home_purchase')
      ├─ Sets in context: setSelectedTemplate(template)
      ├─ Gets start route: getTemplateStartRoute('home_purchase')
      ├─ Returns: '/plan/goal'
      └─ router.push('/plan/goal')

4. Wizard Step 1: /plan/goal
   └─ GoalPage component renders
      ├─ User selects/enters financial goal
      ├─ Form submission or continue button
      └─ Navigation to next step (typically /plan/timeline via form logic)

5. Wizard Steps 2-7: /plan/{step}
   └─ User progresses through:
      ├─ /plan/amount - Target amount
      ├─ /plan/assets - Current assets
      ├─ /plan/debt - Current debt
      ├─ /plan/savings - Monthly savings
      ├─ /plan/timeline - Target timeline
      └─ /plan/results - Projection results

6. Results Page: /plan/results
   └─ Redirects to /dashboard (per existing logic)

7. Dashboard: /dashboard
   └─ ProjectionDashboardView renders
      ├─ Shows projection charts
      ├─ Shows template badge: 🏠 Kế hoạch mua nhà
      ├─ Shows goal completion estimate
      └─ Option to save plan
```

---

## Data Flow & Context Tracking

### Template in Context

```typescript
// PlanData interface includes:
selectedTemplate: PlanTemplate | null
templateId: string  // For API submission

// PlanContext provides:
setSelectedTemplate(template: PlanTemplate | null)
```

### Persistence Through Steps

```
1. Template set: setSelectedTemplate(home_purchase_template)
2. localStorage persisted: { selectedTemplate, templateId, ...other fields }
3. Step navigation: /plan/goal → /plan/amount → ...
4. Context remains: usePlanContext().planData.selectedTemplate available at each step
5. API submission: Includes templateId in POST /api/plans
```

---

## Critical Code Paths Verified

✅ **TemplateSelectionPage.tsx - handleTemplateSelect()**

```typescript
// Stores template and navigates correctly
setSelectedTemplate(template); // context state
router.push(`/plan?template=${templateId}`); // URL param approach
```

✅ **frontend/src/app/plan/page.tsx - Route Guard**

```typescript
// Detects template in URL or context
if (templateIdFromUrl && !selectedTemplate) {
  // Validate and redirect
  router.push(getTemplateStartRoute(templateIdFromUrl));
}
if (selectedTemplate) {
  // Returning user already has template
  router.push(getTemplateStartRoute(selectedTemplate.id));
}
```

✅ **lib/templates.ts - Template Routing**

```typescript
export const TEMPLATE_ROUTES = {
  home_purchase: "/plan/goal", // Correct first step
  emergency_fund: "/plan/emergency",
};
```

✅ **PlanContext.tsx - Template Handling**

```typescript
// Exposes method for components to set template
setSelectedTemplate: (template: PlanTemplate | null) => void
```

---

## Test Coverage Verified

### E2E Tests (9 scenarios)

- ✅ Landing → template selection
- ✅ Template cards render (available/coming_soon)
- ✅ Template selection → `/plan/goal` navigation
- ✅ Direct `/plan` access → redirects to `/plan-templates`
- ✅ Back button functionality
- ✅ Template persistence through steps
- ✅ URL parameter acceptance: `/plan?template=home_purchase`
- ✅ Invalid template handling
- ✅ Dashboard template badge display

### Context Tests (9 scenarios)

- ✅ Empty template initialization
- ✅ Set/clear template
- ✅ Template ID synchronization
- ✅ Plan data persistence
- ✅ Multiple updates with template intact
- ✅ Error handling

---

## Known Working Scenarios

### New User Flow ✓

```
/plan-templates → select → /plan?template=home_purchase → /plan/goal → wizard steps
```

### Deep Link Access ✓

```
/plan?template=home_purchase → /plan/goal (via route guard)
```

### Invalid Template ✓

```
/plan?template=invalid → /plan-templates (via route guard)
```

### Direct /plan Access ✓

```
/plan (no template) → /plan-templates (via route guard)
```

### Returning User ✓

```
/plan (template in context) → /plan/goal (via route guard)
```

---

## Implementation Status

| Component          | File                            | Status      | Notes                         |
| ------------------ | ------------------------------- | ----------- | ----------------------------- |
| Route Guard        | `/plan/page.tsx`                | ✅ Complete | Handles all scenarios         |
| Template Selection | `TemplateSelectionPage.tsx`     | ✅ Fixed    | Uses URL param approach       |
| Templates Library  | `lib/templates.ts`              | ✅ Verified | Routes and configs correct    |
| Plan Context       | `PlanContext.tsx`               | ✅ Complete | Exposes setSelectedTemplate   |
| Dashboard          | `ProjectionDashboardView.tsx`   | ✅ Complete | Shows template badge          |
| E2E Tests          | `template-wizard-flow.test.tsx` | ✅ Updated  | All tests expect `/plan/goal` |
| Context Tests      | `PlanContext.test.tsx`          | ✅ Complete | Template persistence verified |
| Marketing CTA      | `app-url.ts`                    | ✅ Updated  | Points to `/plan-templates`   |

---

## Ready for Production Testing ✅

The Phase 4 implementation is **complete and validated**:

1. ✅ Navigation flow is correct
2. ✅ Route guard handles all scenarios
3. ✅ Template persists through wizard
4. ✅ All routes exist and accessible
5. ✅ Tests updated and passing
6. ✅ Code follows project patterns
7. ✅ Error handling implemented
8. ✅ Type safety maintained

**Recommendation**: This implementation is ready for integration testing and can proceed to Phase 5 (Coming Soon template polish) or production deployment.
