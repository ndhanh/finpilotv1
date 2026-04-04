# Phase 4 Implementation Review & Refactoring Summary

**Review Date**: April 4, 2026  
**Status**: ✅ **REVIEWED & FIXED** - Home Purchase Wizard Flow Validated

---

## Issues Found & Fixed

### Issue 1: Incorrect Navigation Route in TemplateSelectionPage ❌ → ✅

**Problem**:

- TemplateSelectionPage was navigating to `/plan/${templateId}/income` (e.g., `/plan/home_purchase/income`)
- This route structure doesn't exist in the wizard
- The route guard at `/plan` was being bypassed entirely

**Root Cause**:

- Original implementation assumed a nested route structure like `/plan/{template}/{step}`
- Actual wizard uses flat routes: `/plan/goal`, `/plan/timeline`, `/plan/amount`, etc.
- Template `wizard_steps` array contains step names ("goal", "amount", etc.), not full route paths

**Solution Implemented**:

```typescript
// BEFORE (WRONG)
router.push(`/plan/${templateId}/income`);

// AFTER (CORRECT)
router.push(`/plan?template=${templateId}`);
```

**Why This Works**:

1. Navigates to `/plan` with template query parameter
2. Route guard at `/plan/page.tsx` receives the URL param
3. Route guard extracts template ID from URL
4. Validates template via `getTemplate(templateId)`
5. Calls `setSelectedTemplate(template)` to store in context
6. Gets template start route via `getTemplateStartRoute()` → `/plan/goal`
7. Redirects to `/plan/goal` (the actual first wizard step)

---

## Verified Implementation Flow

### Complete User Journey (Home Purchase)

```
1. Landing Page (marketing)
   └─ Click CTA button

2. Route: /plan-templates
   └─ TemplateSelectionPage renders

3. User clicks "Bắt đầu" (home_purchase template)
   ├─ handleTemplateSelect(id)
   ├─ setSelectedTemplate(template) ← context state
   ├─ router.push(`/plan?template=home_purchase`)

4. Route: /plan?template=home_purchase
   └─ /plan/page.tsx (route guard) useEffect
      ├─ Detects ?template=home_purchase URL param
      ├─ template undefined in context (first visit)
      ├─ getTemplate('home_purchase') → template object
      ├─ setSelectedTemplate(template)
      ├─ getTemplateStartRoute('home_purchase') → '/plan/goal'
      ├─ router.push('/plan/goal')

5. Route: /plan/goal
   └─ GoalPage wizard step renders
      └─ Form submission continues through wizard steps
         /plan/timeline → /plan/amount → ... → /dashboard

6. Dashboard Results
   └─ ProjectionDashboardView
      └─ Shows template badge: 🏠 Kế hoạch mua nhà
```

### Route Guard Logic (Handles All Cases)

```typescript
// Case 1: URL has template param, context is empty
if (templateIdFromUrl && !selectedTemplate) {
  const template = getTemplate(templateIdFromUrl);
  if (template) {
    setSelectedTemplate(template);
    router.push(getTemplateStartRoute(templateIdFromUrl)); // /plan/goal
  } else {
    router.push("/plan-templates"); // invalid template
  }
}

// Case 2: Context has template (returning user)
if (selectedTemplate) {
  router.push(getTemplateStartRoute(selectedTemplate.id)); // /plan/goal
}

// Case 3: No template anywhere (direct /plan access)
router.push("/plan-templates");
```

---

## Files Reviewed & Status

### ✅ Correctly Implemented

1. **TemplateSelectionPage.tsx** - FIXED
   - Now navigates to `/plan?template=${templateId}` ✓
   - Calls `setSelectedTemplate()` before navigation ✓
   - Handler properly stores template in context ✓

2. **frontend/src/app/plan/page.tsx** - CORRECT
   - Route guard logic handles all three cases ✓
   - Dependencies array includes all required values ✓
   - Respects URL params and context state ✓

3. **lib/templates.ts** - CORRECT
   - `getTemplateStartRoute()` returns `/plan/goal` for home_purchase ✓
   - `TEMPLATE_ROUTES` mapping is accurate ✓
   - All helper functions properly defined ✓

4. **PlanContext.tsx** - CORRECT
   - Exposes `setSelectedTemplate` action ✓
   - Type definitions include template field ✓
   - Integration with usePlan hook is correct ✓

5. **Dashboard Components** - CORRECT
   - `DashboardProjection` passes template to view ✓
   - `ProjectionDashboardView` displays template badge ✓
   - Template info properly integrated in results ✓

6. **E2E Tests** - CORRECT
   - Test expectations properly updated ✓
   - Tests expect `/plan/goal`, not nested routes ✓
   - All test flows align with correct implementation ✓

7. **Marketing Navigation** - CORRECT
   - Landing page CTA points to `/plan-templates` ✓
   - `app-url.ts` returns `/plan-templates` ✓

---

## Key Design Decisions Validated

### 1. URL Parameter Approach ✓

- **Chosen**: Pass template via URL query parameter to route guard
- **Why**:
  - Immediate availability (doesn't depend on React state sync)
  - Supports deep linking: `/plan?template=home_purchase`
  - Route guard can validate before setting context
  - Graceful fallback for invalid templates

### 2. Route Guard Pattern ✓

- **Chosen**: Use `/plan/page.tsx` as centralized route guard
- **Why**:
  - All plan routes funnel through /plan first
  - Single source of truth for template selection validation
  - Prevents direct access to wizard without template
  - Handles both new and returning users

### 3. Flat Route Structure ✓

- **Chosen**: Keep wizard as flat routes (`/plan/goal`, `/plan/timeline`, etc.)
- **Why**:
  - Simpler URL patterns
  - Template info in context doesn't need to be in URL path
  - Easier navigation between steps
  - Matches existing architecture

---

## Testing Validation

### E2E Tests Passing ✓

```
✓ should navigate from landing page to template selection
✓ should display available and coming soon templates
✓ should select template and navigate to wizard
✓ should prevent direct navigation to /plan without template
✓ should show back button on template selection page
✓ should maintain template selection through wizard steps
✓ should accept template from URL parameter
✓ should redirect invalid template in URL parameter
✓ should show template info on dashboard results
```

### Context Tests Passing ✓

```
✓ should initialize with empty template
✓ should set selected template
✓ should set template ID when template is selected
✓ should clear template when cleared
✓ should persist plan data while template selected
✓ should maintain template through multiple updates
✓ Error handling when used outside provider
```

---

## Summary

### ✅ Issues Resolved

1. **Fixed navigation route** - Now uses URL parameter approach
2. **Validated route guard logic** - Handles all user flow scenarios
3. **Confirmed context integration** - Template properly persisted through wizard
4. **Updated test expectations** - Tests expect correct `/plan/goal` route

### ✅ Verified Flows

1. **New User**: `/plan-templates` → select template → `/plan?template=...` → `/plan/goal`
2. **Direct Link**: `/plan?template=home_purchase` → `/plan/goal`
3. **Invalid Template**: `/plan?template=invalid` → `/plan-templates`
4. **Direct /plan**: `/plan` → `/plan-templates`
5. **Returning User**: Template in context → `/plan/goal`

### ✅ Code Quality

- All files follow TypeScript patterns
- Proper error handling and validation
- Consistent with existing codebase style
- Comprehensive test coverage

**Status**: Phase 4 implementation is correct and ready for production testing.
