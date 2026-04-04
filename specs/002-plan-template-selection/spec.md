# Feature Specification: Plan Template Selection & Navigation

**Feature Branch**: `002-plan-template-selection`  
**Created**: April 4, 2026  
**Status**: Draft  
**Input**: User description: "Feature to allow users to select between different financial planning templates (home purchase, emergency fund) from landing page and navigate to respective planning wizards"

## Problem & User Insight

Vietnamese young professionals (ages 22-40) want to achieve major financial goals like buying a house, but feel overwhelmed by the complexity. Currently:

- Users don't know where to start
- No clear visualization of their financial path
- Existing financial planning tools are either too technical or too complex
- Users need simple, goal-based guidance without overwhelming choices

This feature reduces decision friction by providing a clear entry point with pre-defined planning templates for common goals.

## Target Users

**Primary**: Young professionals in Vietnam (22-40 years old)

- First-time homebuyers uncertain about affordability
- Users wanting to build emergency savings
- Individuals seeking simple, non-overwhelming planning tools

**Secondary**: Couples planning joint financial goals

## User Scenarios & Testing

### User Story 1 - User Discovers and Clicks CTA from Landing Page (Priority: P1)

A new user lands on the FinPilot landing page seeking clarity on financial planning. They see the "Bắt đầu ngay" (Start Now) call-to-action button and click it to explore planning options.

**Why this priority**: This is the critical entry point to the entire planning experience. Without this working, no users can access the template selection feature.

**Independent Test**: Can be fully tested by landing on the page, locating the CTA button, and verifying navigation to the template selection page.

**Acceptance Scenarios**:

1. **Given** user is on the FinPilot landing page, **When** user clicks the "Bắt đầu ngay" button, **Then** user is navigated to the plan template selection page
2. **Given** user is on the landing page, **When** user scrolls through sections, **Then** the CTA button remains clearly visible and clickable
3. **Given** user clicks the CTA button, **When** navigation occurs, **Then** the page loads without errors and displays available templates

---

### User Story 2 - User Views and Selects Home Purchase Plan Template (Priority: P1)

User arrives at the template selection page and sees two planning options. They understand the purpose of each template and select the home purchase planning option to begin their plan.

**Why this priority**: This is the core user flow enabling users to start the home purchase planning experience. Home purchase is the primary use case for MVP.

**Independent Test**: Can be fully tested by navigating to template selection page, viewing available templates, selecting home purchase plan, and verifying navigation to the planning wizard.

**Acceptance Scenarios**:

1. **Given** user is on the template selection page, **When** page loads, **Then** user sees exactly two plan templates: "Kế hoạch mua nhà" (Home Purchase Plan) and "Kế hoạch quỹ khẩn cấp" (Emergency Fund Plan)
2. **Given** user views the home purchase plan template card, **When** they examine it, **Then** they see a clear title, description, and call-to-action button
3. **Given** user clicks the home purchase plan card/button, **When** action is triggered, **Then** user is navigated to the home purchase planning wizard
4. **Given** user has selected home purchase plan, **When** wizard loads, **Then** the first step of the planning form is displayed without errors

---

### User Story 3 - User Views Emergency Fund Plan Template Option (Priority: P2)

User sees the emergency fund planning option on the template selection page, even if they don't select it in the MVP. This prepares the UI for future expansion while validating template selection pattern.

**Why this priority**: Provides visual consistency and demonstrates the template selection pattern. Emergency fund planning will be implemented in future iterations, but the template option should be visible and inform users of planned features.

**Independent Test**: Can be fully tested by verifying the emergency fund template card is visible, contains appropriate messaging, and displays a clear status (e.g., "Coming Soon" or disabled state).

**Acceptance Scenarios**:

1. **Given** user is on the template selection page, **When** page fully loads, **Then** emergency fund plan template card is visible alongside home purchase template
2. **Given** user views the emergency fund template card, **When** they examine it, **Then** they see it displays "Coming Soon" status or equivalent messaging
3. **Given** user attempts to interact with emergency fund template, **When** it is not available in MVP, **Then** they see appropriate messaging (tooltip or disabled state) explaining it will be available soon

---

### Edge Cases

- What happens if user is on a slow connection and page takes time to load? (Show loading state with skeleton screens)
- What happens if user clicks the CTA button multiple times rapidly? (Prevent double navigation or show loading state)
- What happens if user navigates back from the planning wizard? (Preserve page state so they return to template selection)
- What happens if JavaScript is disabled or template selection page fails to load? (Show graceful error message with retry option)
- What happens if user lands on template selection page directly via URL? (Page should load properly, treating it as valid entry point)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display a template selection page accessible from the landing page "Bắt đầu ngay" button
- **FR-002**: System MUST display exactly two plan template options: "Kế hoạch mua nhà" and "Kế hoạch quỹ khẩn cấp"
- **FR-003**: System MUST allow users to select the home purchase plan template and navigate to the home purchase planning wizard
- **FR-004**: System MUST prevent selection of emergency fund plan template in MVP (display "Coming Soon" status with clear messaging)
- **FR-005**: System MUST display template cards with clear titles, descriptions, and visual call-to-action elements
- **FR-006**: System MUST maintain responsive design across mobile, tablet, and desktop viewports
- **FR-007**: System MUST implement loading states during navigation transitions to prevent perception of slowness
- **FR-008**: System MUST preserve template selection page state when user navigates back from the planning wizard
- **FR-009**: System MUST track user's template selection (for analytics and future personalization)

### Key Entities

- **Plan Template**: A pre-configured planning structure with target goal (home purchase, emergency fund), associated questions, calculations, and output format
  - Attributes: ID, name (Vietnamese), description, goal_type, icon, status (available/coming_soon), order
  - Relationships: One template has many planning sessions

- **Planning Session**: A user's instance of starting a particular plan template
  - Attributes: ID, user_id, template_id, created_at, current_step, status (in_progress/completed/abandoned)
  - Relationships: One user has many planning sessions

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can navigate from landing page to template selection page in under 2 seconds with successful page load
- **SC-002**: 100% of template cards display correctly across mobile (375px), tablet (768px), and desktop (1920px) viewports
- **SC-003**: Users can click and select home purchase template and reach home purchase planning wizard without errors
- **SC-004**: 95% of template selection page loads complete without JavaScript errors (measured via error tracking)
- **SC-005**: Users spend average of 30-60 seconds on template selection page before selecting a template (indicates page clarity)
- **SC-006**: Zero navigation errors when transitioning from landing page → template selection → home purchase wizard
- **SC-007**: 90% of users successfully complete a template selection action (click select) on first attempt without confusion

## User Experience Details

### Page Layout & Components

**Template Selection Page Structure**:

1. **Header Section**
   - Page title: "Chọn kế hoạch của bạn" (Choose Your Plan)
   - Subtitle: Brief explanation of what comes next and reassurance about simplicity
   - Tone: Friendly, encouraging, non-judgmental

2. **Template Cards Container**
   - Grid layout (responsive: 1 column on mobile, 2 columns on desktop)
   - Two card components displayed:
     - Home Purchase Plan Card (enabled)
     - Emergency Fund Plan Card (disabled/coming soon)

3. **Template Card Components**
   - Visual icon representing the goal type
   - Title in Vietnamese
   - 1-2 sentence description explaining the purpose
   - Call-to-action button with appropriate state:
     - **Home Purchase**: "Bắt đầu kế hoạch mua nhà" (Start Home Purchase Plan)
     - **Emergency Fund**: "Sắp có" (Coming Soon) - disabled button
   - Optional: Badge or indicator showing MVP availability

4. **Navigation**
   - Back button to landing page (or browser back)
   - Progress indicator showing current step in user journey

### Information Collected at This Stage

None - this page is purely for navigation and template selection. Question collection happens in subsequent wizard steps.

### Tone & User Experience Approach

- **Friendly & Encouraging**: Reassure users that planning doesn't have to be complicated
- **Clear & Simple**: Avoid financial jargon; use simple Vietnamese language
- **Non-judgmental**: Don't make users feel bad about their financial situation
- **Visual Clarity**: Use icons and whitespace to make options stand out
- **Mobile-first**: Ensure single-column layout on phone doesn't overwhelm users

## Assumptions

1. Users have basic understanding of Vietnamese language (no translation feature in MVP)
2. Users access from modern browsers supporting ES6+ JavaScript
3. Home purchase planning wizard already exists or will be built in parallel feature (001-mvp-core)
4. Emergency fund wizard will be implemented in future iteration; MVP shows "Coming Soon" state
5. Users don't require authentication to view template selection page (accessible to anonymous visitors)
6. Page load time from landing to template selection is acceptable at <2 seconds
7. Analytics tracking infrastructure exists or will be implemented separately

## Dependencies & Future Features

- **Depends on**: Landing page implementation (feature 00-landing) must have CTA button pointing to /plan-templates route
- **Depends on**: Home purchase planning wizard implementation (feature 001-mvp-core)
- **Enables**: Emergency fund planning feature (future iteration)
- **Enables**: Plan comparison or recommendation experience (future enhancement)
