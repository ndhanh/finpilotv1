# FinPilot MVP Product Specification

**Version**: 1.0  
**Date**: March 21, 2026  
**Status**: Ready for Implementation  
**Branch**: `001-mvp-core`

---

## 1. Product Overview

**FinPilot** is a goal-focused financial planning application designed for Vietnamese users. It helps people understand their current financial position and create realistic, actionable plans to achieve important life goals.

**Core Value Proposition**: Users input basic financial information through a guided conversation, define a specific financial goal (e.g., buying a home, building emergency savings), and receive a personalized monthly projection and concrete recommendations—in minutes, without lengthy forms or registration requirements.

**Product Philosophy**:

- **Goal-centric**: All features and recommendations ladder back to goal achievement
- **Conversational**: Guided, progressive onboarding that feels like a financial conversation, not a form
- **Transparent**: All calculations and recommendations are explainable in plain language
- **Progressive**: Works with partial data and improves as users provide more information
- **Trust-first**: Deterministic, honest modeling that avoids false precision and black-box logic

**Target Launch**: MVP targeting Vietnamese market, desktop-first (web application)

---

## 2. Problem Statement

### User Context

Vietnamese users face growing complexity in personal financial planning due to:

- Rising real estate prices requiring substantial multi-year savings
- Multiple income sources (employment, side business, freelance)
- Limited access to trusted financial planning tools adapted for local context
- Uncertainty about realistic timelines and required monthly savings for major life goals
- Lack of clear visibility into how income, expenses, and debt affect goal achievement

### Existing Gaps

Current solutions fall into two categories:

1. **International tools** (ProjectionLab, YNAB): Excellent but not localized; assume USD context, US financial products, US tax complexity
2. **Local solutions**: Focus on transaction tracking or investment products; lack genuine planning and projection capabilities

### Core Problem Statement

Vietnamese users need a **trusted, locally-adapted financial planning tool** that:

- Explains goal feasibility in clear, actionable terms
- Works with incomplete financial data
- Provides honest projections without false precision
- Requires minimal time investment upfront
- Avoids complex tax and product logic unsuitable for MVP

---

## 3. Goals and Objectives

### Primary Goals (MVP)

1. **Enable first-time goal planning**: Users with no planning experience can define a goal and get a realistic projection within 10-15 minutes
2. **Build user confidence**: Users understand the relationship between their savings rate and goal completion
3. **Demonstrate value pre-commitment**: Users see actionable, personalized output before any account creation or data persistence
4. **Establish trust in projections**: Users understand the assumptions and methodology behind all recommendations
5. **Create a scalable foundation**: MVP architecture supports adding new goal types without major refactoring

### Secondary Goals

- Validate market demand and user willingness to engage with planning
- Collect data about Vietnamese user financial patterns and common goals
- Build retention through save/export functionality and goal tracking

### Non-Goals (See Section 7)

- Investment management, portfolio optimization, or stock tracking
- Detailed expense tracking or bookkeeping
- Multi-currency or international asset planning
- Advanced Monte Carlo analysis or probabilistic modeling
- Tax optimization or compliance features
- Integration with banks or brokers

---

## 4. Target Users & Personas

### Primary Persona: **Thảo - The Goal-Oriented Saver**

- **Age**: 28-45
- **Income**: 20-50M VND/year (stable employment + some side income)
- **Financial Situation**: Saving for a specific goal (home purchase most common); has some liquid savings; carries student debt or consumer debt
- **Comfort Level**: Moderate financial literacy; comfortable with numbers but not investments; seeks clear guidance
- **Goals**: Buy a house in 3-5 years; have 6-month emergency fund; retire with dignity
- **Behavior**: Prefers structured plans; motivated by seeing progress; makes decisions based on clear data
- **Pain Point**: Doesn't know if saving rate is realistic for stated goals; unsure about next steps

### Secondary Persona: **Minh - The Uncertain Planner**

- **Age**: 22-35
- **Income**: 15-30M VND/year (recent graduate to early-career)
- **Financial Situation**: Minimal liquid savings; wants to start planning for future; may carry consumer debt
- **Comfort Level**: Lower financial literacy; intimidated by complexity; needs encouragement and validation
- **Goals**: Build emergency fund; start saving for house; understand if independent living is feasible
- **Behavior**: Seeks permission and validation; benefits from progressive milestones; responsive to simple metrics
- **Pain Point**: Doesn't know where to start or if goals are realistic; fears being financially irresponsible

### Exclusions (Not targeting MVP)

- High-net-worth individuals (>500M VND liquid)
- Active investors seeking portfolio optimization
- Business owners with complex income structures
- Users requiring professional financial advisory services

---

## 5. Core Jobs to Be Done

1. **"Help me understand if my goal is realistic"**
   - User has a financial goal in mind but doesn't know if it's achievable
   - Wants a clear yes/no with implications
   - Current workaround: Guessing or asking friends; leads to poor decisions

2. **"Tell me how much I need to save each month"**
   - User knows the goal and timeline but not the required monthly amount
   - Wants this calculated based on current situation and assumptions
   - Current workaround: Excel; imprecise; feels isolated in calculation

3. **"Show me my financial position in one view"**
   - User has multiple income sources, debts, and savings; unclear about net position
   - Wants to see net worth, liquid funds, and obligations summarized
   - Current workaround: Manually tracking in notebooks or spreadsheets

4. **"Guide me through planning step-by-step"**
   - User is intimidated by financial planning; needs structure and guidance
   - Wants each step explained and validated before moving forward
   - Current workaround: Not planning; drifting; or expensive financial advisory

5. **"Save and revisit my plan"**
   - User has made a plan and wants to monitor progress or test scenarios
   - Wants to come back without redoing all inputs
   - Current workaround: Screenshots or external notes; fragile

---

## 6. MVP Scope

### What's Included

#### 6.1 Guided Onboarding Flow

- Entry point: No login required; user can start planning immediately
- Progressive conversation format (not a form):
  - Question 1: What's your primary financial goal? (House purchase / Emergency fund / Other)
  - Question 2: When do you want to achieve this? (Timeline in years/months)
  - Question 3: How much do you need to save? (Amount or assumption-based)
  - Question 4: How much can you save monthly? (Surplus/contribution capacity)
  - Question 5: Current liquid savings (VND)
  - Question 6: Existing debt (optional but recommended)
- Skip/optional logic: Some fields optional; system provides defaults; users can refine
- Entry point: Desktop URL; no app required for MVP

#### 6.2 Primary Goal Flow: House Purchase

- **Goal Type**: Purchase residential property in Vietnam
- **Inputs**:
  - Target property price or price estimate (VND)
  - Desired purchase timeline (year & month)
  - Current savings toward down payment (VND)
  - Down payment percentage assumption (default: 20%)
  - Monthly surplus available for savings (VND)
  - Current variable debts (credit card, personal loan)
- **Assumptions** (configurable, visible to user):
  - 0% inflation on property price (MVP simplification; no market appreciation/depreciation)
  - Constant monthly contribution (no raises, income changes)
  - No investment returns on savings (conservative; cash savings assumption)
  - Fixed closing costs: 3-5% of property price (range shown, midpoint used)
  - Simple interest on debt; no compound calculations
- **Outputs**:
  - Monthly savings target to meet timeline
  - Projection: Months to goal completion
  - Gap analysis: Feasible within timeline? (Yes/No/Stretch)
  - Recommended next actions (rule-based)

#### 6.3 Secondary Goal Flow: Emergency Fund (Future Ready)

- Included in UI/logic but not heavily promoted in MVP
- Inputs: Target emergency fund (months of expenses); current monthly expenses estimate
- Simple linear calculation; reuses same projection engine

#### 6.4 Deterministic Projection Engine

- **Algorithm**: Simple linear monthly accumulation
  ```
  Future Savings = Current Savings + (Monthly Contribution × Months to Goal)
  Gap = Goal Amount - Future Savings
  Feasible = (Gap <= 0)
  ```
- **Calculation Details**:
  - Monthly contribution = (Max of 0, user's stated monthly surplus)
  - Months to goal = (Goal Year × 12) + Goal Month - (Today's Year × 12) - Today's Month
  - Property assumption-based goals:
    - Down payment required = Property Price × Down Payment Percentage
    - Closing costs = Property Price × 3-5% (use 4% midpoint)
    - Total needed = Down payment + Closing costs
- **Constraints**:
  - Minimum timeline: 6 months (validation rule)
  - Maximum timeline: 30 years (validation rule)
  - Negative savings rate handling: Flag as unrealistic; suggest debt reduction first
- **No complex features**: No inflation adjustment, investment returns, or probability analysis in MVP

#### 6.5 Results Dashboard

- Displayed after onboarding completion; before any registration prompt
- **Sections**:
  1. **Goal Summary Card**
     - Goal statement (e.g., "Buy a 5B VND home in Hanoi by Dec 2027")
     - Timeline visual (months complete / total months)
     - Feasibility status (On track / Stretch / Not feasible)
  2. **Monthly Projection Chart**
     - X-axis: Months from today to 5 years or goal completion (whichever is shorter)
     - Y-axis: VND accumulated
     - Two lines: Current savings path vs. with recommended contribution
     - Interactive tooltips: Hover on point shows month/amount/gap
  3. **Financial Position Summary**
     - Net worth = (Current savings) - (Current debt)
     - Liquid savings available: (Current savings)
     - Monthly debt obligations: Estimated from stated debt (simplified)
  4. **Gap Analysis**
     - Shortfall amount (if any)
     - Impact on timeline or required savings rate
  5. **Personalized Recommendations**
     - Rule-based, not ML-driven
     - Examples: "Increase monthly savings by 2M VND to stay on track"
     - "Prioritize paying off 50M VND consumer debt—it's blocking your plan"
     - "Your 40M VND savings rate is aggressive but realistic"

#### 6.6 Recommendation Engine (Rule-Based)

- **Rules**: Triggered based on inputs and projections
  1. **Feasibility Assessment**:
     - If gap == 0: "Perfect! You're on track."
     - If gap < 0: "You can reach your goal early—by [Month]. Consider increasing other financial priorities."
     - If gap > 0 and (gap / monthly_contribution) < 24 months: "Doable with focus—you'll need [+X VND/month]."
     - If gap > 0 and (gap / monthly_contribution) > 60 months: "This timeline is ambitious. Consider [extending timeline by X years OR increasing savings by Y VND/month]."
  2. **Debt Priority Alerts**:
     - If monthly_debt_payment > 20% of monthly_surplus: "High-interest debt is eating into your savings rate. Prioritize this first."
  3. **Savings Rate Validation**:
     - If monthly_contribution < 500K VND: "Savings are minimal; plan may take longer than expected."
     - If monthly_contribution > 50% of estimated_income: "This savings rate is very aggressive. Verify it's sustainable."
  4. **Timeline Validation**:
     - If timeline < 12 months: "Very short timeline—high urgency. Confirm this is realistic."
     - If timeline > 15 years: "Extended timeline viable but ensure this is a real priority."

#### 6.7 Save Plan Feature (Post-Dashboard)

- User prompted after viewing dashboard: "Save this plan to track progress and update anytime"
- Minimal registration: Email + password OR quick sign-up (name optional)
- Plan persisted to secure backend
- Confirmation: "Plan saved. You can access it anytime at [login]"
- Not required to view initial results; optional for ongoing tracking

#### 6.8 Core UI/UX Principles

- **Conversation-first**: One question per screen; natural language framing
- **Progress visibility**: Show progress through onboarding (e.g., "Step 2 of 5")
- **Explainability**: Every output includes a small "Why?" or "Howwe calculated" section
- **Accessibility**: Vietnamese language; accessible font sizing; clear color contrast
- **Mobile-responsive**: Designed mobile-first but launched desktop-first
- **No friction**: No forced registration; no dialogs; smooth flow

---

## 7. Non-Goals / Out-of-Scope Items

### Explicitly Not Included in MVP

1. **Investment Management**
   - No portfolio tracking, rebalancing, or recommendation
   - No integration with brokerage platforms
   - Not dealing with stocks, bonds, mutual funds, crypto

2. **Detailed Expense Tracking**
   - No transaction logging or categorization
   - No recurring expense templates
   - No budget management (we ask for monthly surplus; users bring it)

3. **Advanced Modeling**
   - No Monte Carlo simulation or probabilistic analysis
   - No inflation adjustments (0% assumption for MVP)
   - No tax optimization or scenario analysis
   - No income variance modeling

4. **Bank/Broker Integration**
   - No Open Banking or API connections
   - No account aggregation or auto-data fetch
   - No direct transfer routing

5. **Professional Advisory**
   - No tax advisory or compliance features
   - No insurance product recommendations
   - No referral network to advisors

6. **Multi-Asset Tracking**
   - No real estate portfolio tracking (beyond goal purchase)
   - No business or vehicle asset management
   - No cryptocurrency or international assets

7. **Collaboration Features**
   - No household/family planning
   - No shared account or multi-user features
   - No advisor/planner collaboration

8. **Advanced Data Persistence**
   - No scenario branching or multiple plan versions
   - No historical tracking or audit trail
   - No version rollback

---

## 8. Key User Journeys

### Journey 1: First-Time Saver (Happy Path)

**Entry Point**: User lands on FinPilot homepage; sees "Plan your financial goal in 10 minutes"

**Steps**:

1. Clicks "Start Planning" → No login required
2. Sees first question: "What's your primary financial goal?"
   - Options: Buy a home / Build emergency fund / Other
   - User selects "Buy a home"
3. Question 2: "When do you want to buy?"
   - User enters: Dec 2027 (using date picker)
4. Question 3: "How much will the home cost?"
   - User enters: 4 billion VND
   - System auto-calculates: ~800M down payment (20%), ~160M closing costs = 960M needed
5. Question 4: "How much can you save each month?"
   - User enters: 15M VND
6. Question 5: "How much do you have saved now?"
   - User enters: 80M VND
7. Optional Question 6: "Do you have any debts?"
   - User enters: 30M VND (credit card)
8. **Results Displayed**:
   - "You need to save 960M by Dec 2027"
   - "You'll have 1.02B (80M + 15M × 24 months) = On track!"
   - Monthly projection chart showing path
   - Net worth summary
   - Recommendation: "Great savings rate. Stay consistent—you'll reach your goal early."
9. Prompt: "Save this plan to track progress?"
   - User clicks "Save Plan"
   - Minimal signup: Email + Password
10. **Outcome**: User has saved plan, feeling confident about timeline, knows next steps

**Edge Case - Insufficient Savings Rate**:

- Same flow, but user enters 5M/month savings
- Result: "Gap of 140M. You'll have 800M by Dec 2027, but need 960M."
- Recommendations: "Extend timeline to May 2028 OR increase savings to 19M/month"
- User prompted to adjust inputs and re-project

---

### Journey 2: Debt-First Planner

**Entry Point**: Same, but user has significant debt

**Steps** 1-5: Same as Journey 1

6. Question 5: "How much do you have saved now?"
   - User enters: 40M VND
7. Question 6: "Do you have any debts?"
   - User enters: 120M VND (80M car loan + 40M credit card)
8. **Results Displayed**:
   - Feasibility: "Challenging. You're $120M in debt, limiting your savings power."
   - Debt alert: "Your debt payments are 8M/month, competing with your goal."
   - Recommendation: "Consider prioritizing debt payoff first (3-4 years). This could improve your 2027 timeline viability."
   - Alternative path: "If you clear debt in 3 years, then save aggressively, you can target a 2030 home purchase."
   - Question prompt: "Would you like to model a debt-first strategy instead?"

---

### Journey 3: Drop-Off Prevention (Uncertain User)

**Entry Point**: User lands on site but hesitates about commitment

**Steps**:

1. Clicks "Start Planning"
2. Sees first question on timeline (optional value pitch): "Most users take 5-10 minutes. You'll get a personalized plan immediately—no signup required."
3. User completes first 3 questions (goal, timeline, amount)
4. System detects this is main value: Offer **quick preview**
   - "Based on your inputs, here's your snapshot: You'll need 960M for your 4B home by Dec 2027. With 15M/month, you're on track."
   - "Finish in 2 more minutes to see the full projection and recommendations."
5. User continues → Completes full onboarding
6. User sees dashboard
7. User exits without saving
   - Browser close or tab switch
   - **Remarketing policy**: If user returns within 7 days, offer one-click re-entry to previous plan (from localStorage)

---

### Journey 4: Returning User Updating Plan

**Entry Point**: User logs back in via saved account

**Steps**:

1. "Welcome back! Here's your saved plan: 4B home by Dec 2027"
2. Current status (if 2 months have passed): "You should have ~80M + 30M saved = 110M toward your goal"
3. Options:
   - "View plan" → Dashboard with updated progress
   - "Update details" → Re-enter onboarding (not full form, just changed fields)
   - "Reset goal" → New planning session
4. User clicks "Update details"
5. Form shows previous answers as defaults; user can modify monthly savings rate (now 18M/month)
6. System recalculates: "New projection: You'll reach goal by Sep 2027 (3 months early!)"
7. Dashboard updated; user can save new version or export comparison

---

## 9. Functional Requirements

### 9.1 Onboarding Flow

| Requirement           | Description                                                         | Implementation Notes                               |
| --------------------- | ------------------------------------------------------------------- | -------------------------------------------------- |
| Progressive Questions | One question per screen; no overwhelming forms                      | Use state machine or step counter                  |
| Goal Type Selection   | Support House Purchase primary; Emergency Fund secondary            | Dropdown or radio buttons with icons               |
| Timeline Input        | Month/Year picker; validate against today's date; min 6mo, max 30yr | Client-side validation; clear error states         |
| Amount Input          | Support currency input with VND formatting (1,000,000,000 display)  | Input type=number; localization for commas/periods |
| Savings Rate Input    | Validate monthly surplus; warn if <500K or >50% of income           | Client-side validation with user warnings          |
| Optional Fields       | Debt entry optional but encouraged                                  | Provide "I don't know" + default options           |
| Skip Logic            | Allow users to skip optional fields; use defaults                   | System provides defaults; shown in summary         |
| Input Validation      | Real-time feedback; clear error messages                            | Client-side validation before submission           |
| Summary Review        | Show entered data before projection; allow edits                    | Confirmation screen; "Edit" links on each field    |

### 9.2 Projection Engine

| Requirement          | Description                                            | Implementation Notes                                       |
| -------------------- | ------------------------------------------------------ | ---------------------------------------------------------- |
| Linear Calculation   | Monthly accumulation of savings + current balance      | Simple formula (no compounds, growth)                      |
| Gap Detection        | Calculate shortfall if goal not met in timeline        | Trigger recommendation rules                               |
| Feasibility Flag     | Determine if goal achievable in stated timeline        | Binary determination + confidence level                    |
| Sensitivity Inputs   | Allow users to adjust contribution rate and see impact | Real-time recalculation on input change                    |
| Edge Case Handling   | Handle negative gap, zero timeline, extreme values     | Validation rules + user guidance                           |
| Deterministic Output | Same inputs always produce same outputs                | Use UTC timestamps; consistent rounding (VND, no decimals) |

### 9.3 Dashboard Display

| Requirement           | Description                                             | Implementation Notes                            |
| --------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| Goal Card             | Show goal, deadline, progress status                    | Use progress bar; percentage complete           |
| Projection Chart      | Visualize savings path over time                        | Line chart; two lines (current + recommended)   |
| Financial Summary     | Net worth, liquid assets, debt                          | Component layout; color-coded                   |
| Recommendation Panel  | List of 2-3 top recommendations                         | Rule-based; explainable text                    |
| Drill-Down Capability | Click on sections to see details                        | Modal or expandable section; no navigation away |
| Export/Share          | Generate PDF or shareable link (post-MVP consideration) | Links provided; email sharing option            |
| Data Transparency     | Show all assumptions used in calculation                | Collapsible "Assumptions" section               |

### 9.4 Save Plan Feature

| Requirement                 | Description                                       | Implementation Notes                       |
| --------------------------- | ------------------------------------------------- | ------------------------------------------ |
| Email/Password Registration | Minimal signup; name optional                     | Standard auth; email verification required |
| Plan Persistence            | Save all inputs and calculated projections        | Encrypted DB; linked to user account       |
| Session Management          | Remember user; auto-logout after 30 days          | Standard session tokens; secure cookies    |
| Plan History                | Track when plan was created/updated               | Timestamp stored; show in user dashboard   |
| One-Click Return            | If user returns within 7 days, offer quick access | localStorage + server-side cache           |
| Data Export                 | Allow users to export plan as JSON or CSV         | Post-MVP; in scope for future              |

### 9.5 Recommendation Engine (Rules)

| Requirement              | Description                                      | Implementation Notes                   |
| ------------------------ | ------------------------------------------------ | -------------------------------------- |
| Rule-Based Logic         | No ML; simple if/then rules                      | Rules stored in config; easy to modify |
| Explainability           | Every recommendation includes reasoning          | Text template + dynamic values         |
| Actionability            | Recommendations translate to clear next steps    | Action-oriented language               |
| Debt Prioritization      | Flag high-debt scenarios; suggest adjustment     | Debt-to-savings ratio trigger          |
| Savings Rate Validation  | Warn if rate unrealistic or too aggressive       | Heuristics based on typical income     |
| Timeline Guidance        | Suggest path adjustments if timeline seems risky | Based on gap analysis                  |
| Multiple Recommendations | Show 2-3 top recommendations, not overwhelming   | Priority ordering; dismissable         |

---

## 10. Inputs and Outputs

### 10.1 User-Entered Inputs (Required/Optional)

| Input           | Type           | Required? | Example        | Constraints                       | Notes                        |
| --------------- | -------------- | --------- | -------------- | --------------------------------- | ---------------------------- |
| Goal Type       | Enum           | Yes       | House Purchase | V: House / Emergency Fund / Other | Primary context              |
| Goal Timeline   | Date (MM/YYYY) | Yes       | Dec 2027       | Min: Today + 6mo, Max: +30yr      | Goal deadline                |
| Goal Amount     | Currency (VND) | Yes       | 4,000,000,000  | Min: 10M, Max: 20B                | Property price or target     |
| Monthly Surplus | Currency (VND) | Yes       | 15,000,000     | Min: 0, Max: 500M                 | Capacity to save monthly     |
| Current Savings | Currency (VND) | Yes       | 80,000,000     | Min: 0, Max: 1B                   | Existing liquid funds        |
| Existing Debt   | Currency (VND) | No        | 150,000,000    | Min: 0, Max: 2B                   | Total liabilities (optional) |
| Down Payment %  | Integer        | No        | 20             | Default: 20, Range: 15-30         | House goal only              |

### 10.2 System-Provided Defaults (When User Skips)

| Field                 | Default     | Reasoning                            |
| --------------------- | ----------- | ------------------------------------ |
| Down Payment %        | 20%         | Market standard in Vietnam           |
| Closing Costs %       | 4%          | Mid-range of typical 3-5%            |
| Debt Interest Rate    | 0% (Linear) | No interest in MVP; simplified       |
| Inflation on Property | 0%          | Conservative; no future appreciation |
| Investment Return     | 0%          | Assume cash savings (no risk)        |
| Emergency Fund Months | 3           | Standard recommendation              |

### 10.3 Derived Metrics (Calculated)

| Metric                | Calculation                                  | Purpose            |
| --------------------- | -------------------------------------------- | ------------------ |
| Months to Goal        | Goal Date - Today Date                       | Time horizon       |
| Down Payment Required | Goal Amount × Down Payment %                 | House goal only    |
| Closing Costs         | Goal Amount × Closing Costs %                | House goal only    |
| Total Needed          | Down Payment + Closing Costs                 | House goal only    |
| Projected Savings     | Current Savings + (Monthly Surplus × Months) | Path to goal       |
| Gap (if any)          | Total Needed - Projected Savings             | Shortfall analysis |
| Required Monthly Rate | Gap ÷ Months (if gap > 0)                    | Adjustment needed  |
| Feasibility Status    | Gap <= 0?                                    | Yes/No/Stretch     |
| Net Worth             | Current Savings - Existing Debt              | Financial position |

### 10.4 Dashboard Outputs (Display)

| Output              | Format                               | Audience             | Explainability                                                |
| ------------------- | ------------------------------------ | -------------------- | ------------------------------------------------------------- |
| Goal Summary        | Text + progress badge                | User decision-making | "You need 960M by Dec 2027. You're on track."                 |
| Monthly Chart       | Line chart (2 lines)                 | Visual learners      | Hover tooltips show amount/month                              |
| Feasibility Status  | Color-coded badge (Green/Yellow/Red) | Quick assessment     | Legend explains each color                                    |
| Net Worth Summary   | Text + breakdown                     | Financial position   | "Your net worth is 50M (80M saved - 30M debt)"                |
| Top Recommendations | Bulleted list (2-3 items)            | Decision support     | "Increase savings by 5M/month to stay on track"               |
| Assumptions Used    | Collapsible section                  | Transparency         | "We assumed 0% inflation, 20% down payment, 4% closing costs" |

### 10.5 Recommendation Output Format

**Rule-Based Generation**: Each recommendation follows a template

**Example 1 - On Track**:

```
"Your savings rate of 15M/month is solid. At this pace, you'll accumulate 960M
by Dec 2027—exactly matching your goal. Action: Stay consistent with deposits."
```

**Example 2 - Shortfall**:

```
"You'll have 800M saved, but need 960M. Gap: 160M.
To close this, you can (a) Increase savings to 19M/month, or
(b) Move timeline to May 2028. Which works better for you?"
```

**Example 3 - Debt Alert**:

```
"Your 120M debt is eating 8M/month—reducing your savings power.
Quick win: Clear this in 3 years. Then re-plan aggressively for buying in 2030."
```

---

## 11. Recommendation and Insight Behavior

### 11.1 Recommendation Philosophy

- **Rule-based, not ML**: Deterministic triggers ensure explainability and predictability
- **Action-oriented**: Every rec translates to a concrete next step
- **Contextual**: Recommendations adapt to user's specific inputs (not generic advice)
- **Honest**: Prioritize reality over optimism; flag risks
- **Progressive**: Show 2-3 top recs; don't overwhelm with 10+ options

### 11.2 Recommendation Categories

#### A. Feasibility-Based Recommendations

**Trigger**: Gap analysis post-projection

| Scenario                    | Recommendation                                                                               | User Action                               |
| --------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Gap = 0                     | "Perfect! Your plan is feasible. Stay the course."                                           | Continue saving as planned                |
| Gap 0 - 50M (small overage) | "You're $X short, but it's close. Consider extending 2-3 months."                            | Adjust timeline slightly OR increase rate |
| Gap 50M - 150M (moderate)   | "Doable, but requires commitment. Increase savings to $Y/month or extend timeline $Z years." | Make strategic choice                     |
| Gap > 300M (large)          | "This timeline is very ambitious. Realistic alternatives: [3 options with new timelines]."   | Reassess goal priority                    |

#### B. Debt-Triggered Recommendations

**Trigger**: Debt > 20% of monthly savings capacity

| Scenario                  | Recommendation                                                                           | Priority  |
| ------------------------- | ---------------------------------------------------------------------------------------- | --------- |
| High-interest debt (>15%) | "High-interest debt is costing you. Prioritize clearing this first."                     | Immediate |
| Moderate debt (5-15%)     | "Consider paying down debt before aggressive saving. It frees both cash and psychology." | Important |
| Low debt (<5%)            | "Your debt is manageable. You can save and pay debt in parallel."                        | Secondary |

#### C. Savings Rate Validations

**Trigger**: Monthly rate validity check

| Scenario                | Recommendation                                                                       | User Action       |
| ----------------------- | ------------------------------------------------------------------------------------ | ----------------- |
| Rate < 500K/month       | "Savings are minimal. Goal may take longer. Verify this is your realistic capacity." | Confirm or adjust |
| Rate > 50% of income    | "This savings rate (50%+) is very aggressive. Double-check it's sustainable."        | Confirm or adjust |
| Rate realistic (10-40%) | No alert; green light                                                                | Continue          |

#### C. Timeline-Based Insights

**Trigger**: Goal timeline assessment

| Scenario              | Insight                                                                  | Tone         |
| --------------------- | ------------------------------------------------------------------------ | ------------ |
| timeline < 12 months  | "Very aggressive timeline. Confirm this deadline is unmovable."          | Cautious     |
| timeline 12-36 months | "Realistic timeframe. You have room to build discipline."                | Encouraging  |
| timeline 3-10 years   | "Healthy timeline. Sustainable pace allows life adjustments."            | Positive     |
| timeline > 10 years   | "Extended horizon. Lock in savings habit now; benefit from consistency." | Motivational |

---

## 12. Assumptions and Constraints

### 12.1 Explicit Assumptions (Shown to User)

1. **No Inflation**: Property prices and costs remain constant. This is conservative—real estate may appreciate.
2. **No Investment Returns**: Savings are held in cash (0% return). Risk-free, easy to explain.
3. **Constant Monthly Contribution**: User can save the same amount every month. No raises, layoffs, or personal spending increases.
4. **Fixed Property Price**: User's target home price doesn't change during the savings period.
5. **Simple Interest**: Any debt carries 0% effective interest in MVP (no calculations). Simplification for speed.
6. **Linear Calculation**: No compounding, no step-changes. Straight-line projection.
7. **No Tax Implications**: Vietnamese tax on savings/interest ignored (minimal for cash savings).
8. **Single Goal Focus**: User is planning toward ONE primary goal, not multiple simultaneous goals.

### 12.2 System Constraints

1. **Data Scope**: Only financial data provided by user in onboarding; no external data sources
2. **Timeline Scope**: Projections only 2-5 years out; UI caps at 5-year view
3. **Scenarios**: Single scenario per session (no branching or "what-if" comparison in MVP)
4. **Personalization**: Rule-based, not user history-based
5. **Localization**: Vietnamese language, VND currency, Vietnam-specific financial context only
6. **Devices**: Desktop-first design; mobile responsive but not native app
7. **Auth**: Simple email/password; no SSO or social login in MVP
8. **Data Retention**: Session data retained 30 days; plan data available indefinitely after save

### 12.3 Technical Constraints

1. **Budget Simulation**: Projection calculations must complete in <100ms
2. **No External APIs**: No real-time data fetches; all logic self-contained
3. **No Machine Learning**: All recommendations are rule-based
4. **Storage**: Encrypted user data; comply with Vietnamese data protection norms
5. **Audit Trail**: All calculations logged for transparency
6. **Arithmetic Precision**: All VND calculations in whole numbers (no decimals)

---

## 13. Acceptance Criteria

### 13.1 Onboarding Flow

- [ ] User can complete goal setup in ≤10 minutes without registration
- [ ] All inputs validated in real-time with clear error messages (Vietnamese)
- [ ] Optional fields clearly marked; defaults provided if skipped
- [ ] Summary screen shows all entered data with "Edit" capability on each field
- [ ] No form feels overwhelming; one question per screen
- [ ] Accessibility: Screen readers work; font sizes adjustable; keyboard navigation complete

### 13.2 Projection Engine

- [ ] Same inputs always produce identical outputs (deterministic)
- [ ] Linear calculation matches manual spreadsheet math (+/- 0 VND)
- [ ] Gap detection correctly identifies shortfalls and overage
- [ ] Edge cases handled: negative savings, timeline < 6mo, timeline > 30yr → validation messages
- [ ] All calculations complete in <100ms
- [ ] No floating-point errors; all results in whole VND

### 13.3 Dashboard Display

- [ ] Goal card shows: goal description, deadline, progress %, feasibility status
- [ ] Projection chart displays correctly with 2 lines (current + recommended)
- [ ] Chart interactive: hover shows month/amount/savings accumulated
- [ ] Financial summary shows: net worth, liquid savings, debt, monthly obligations
- [ ] Recommendations display 2-3 top priorities; each with clear reasoning
- [ ] All assumptions visible in collapsible section; user can understand methodology
- [ ] Dashboard responsive on desktop (1920x1080 minimum); mobile-friendly layout

### 13.4 Recommendation Engine

- [ ] Feasibility rule triggers correctly (gap = 0, < 50M, 50-150M, > 150M)
- [ ] Debt-triggered alerts appear when debt/savings ratio > 20%
- [ ] Savings rate validation works (< 500K, > 50% of income)
- [ ] Timeline insight appears (< 12mo, 12-36mo, 3-10yr, > 10yr)
- [ ] All recommendations are specific to user inputs (not generic)
- [ ] Each recommendation explains the "why" in plain language
- [ ] No recommendation contradicts another; priority ordering clear

### 13.5 Save Plan Feature

- [ ] User can save plan with email + password (name optional)
- [ ] Error handling: Email already in use, weak password, network failure
- [ ] Logged-in user can access saved plan
- [ ] Plan shows creation date and last modified date
- [ ] User can delete plan (confirmation required)
- [ ] User session expires after 30 days; confirmation prompt to re-login

### 13.6 Data Privacy & Security

- [ ] All personal data encrypted at rest (AES-256)
- [ ] HTTPS enforced; no unencrypted transmission
- [ ] No third-party tracking; no cookies except auth/session
- [ ] User data not shared with external services
- [ ] GDPR-style data export available (JSON format)
- [ ] User can delete account + all associated data

### 13.7 Localization (Vietnamese)

- [ ] All UI text in Vietnamese (no English default text)
- [ ] Currency formatted as "5,000,000,000 ₫" (with thousands separators)
- [ ] Dates formatted as "DD/MM/YYYY" (Vietnamese norm)
- [ ] Mortgage terms explained (vay, lãi suất, etc.) in context
- [ ] Error messages in clear Vietnamese (not generic English)
- [ ] No untranslated console errors visible to users

### 13.8 Performance

- [ ] Page load time: <2 seconds on 4G
- [ ] Projection calculation: <100ms
- [ ] Dashboard render: <300ms after calculation
- [ ] Smooth animations; no jank or stuttering
- [ ] Mobile: Works on iOS Safari, Chrome; no crashes on input

### 13.9 Data Integrity

- [ ] No data loss on browser crash during onboarding (localStorage recovery)
- [ ] Plan export matches stored data exactly
- [ ] Calculation audit log shows all steps for transparency
- [ ] No SQL injection, XSS, or CSRF vulnerabilities
- [ ] Rate limiting on auth endpoints (5 failed logins = 15-min lockout)

---

## 14. Success Metrics

### 14.1 Engagement Metrics

| Metric                  | Target                                                  | Rationale                                     |
| ----------------------- | ------------------------------------------------------- | --------------------------------------------- |
| **Completion Rate**     | >60% of users finish onboarding (reach dashboard)       | Drop-off is normal; 60% is healthy for MVP    |
| **Save Rate**           | >40% of dashboard viewers save their plan               | Evidence of perceived value; retention signal |
| **Session Duration**    | 10-15 minutes (median)                                  | Target: 10-15 minute experience               |
| **Mobile Usage**        | >30% of traffic from mobile (even though desktop-first) | Signals interest in mobile expansion          |
| **Return Rate** (7-day) | >25% of users return and access saved plan              | Feature adoption; plan engagement             |

### 14.2 Quality Metrics

| Metric                              | Target                                               | Rationale                                           |
| ----------------------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| **Calculation Accuracy**            | 100% match with manual spreadsheet                   | Non-negotiable; trust requirement                   |
| **Recommendation Relevance**        | >70% of users find top recommendation applicable     | Users should recognize recommendations as their own |
| **Feasibility Prediction Accuracy** | >85% alignment with user's eventual goal achievement | Rec predictions must be reasonable                  |
| **Error Rate**                      | <0.1% of sessions (stability)                        | Focus on reliability, not perfection                |
| **Load Time**                       | p95 < 1.5 seconds                                    | Users expect responsiveness with financial data     |

### 14.3 Business Metrics

| Metric                | Target                                                  | Rationale                                      |
| --------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| **Sign-up Rate**      | >30% of plan viewers create an account                  | Baseline for future retention/monetization     |
| **Referral Rate**     | >15% of users refer a friend (optional post-MVP survey) | Word-of-mouth signal                           |
| **Market Validation** | >500 active monthly users within 6 months               | Demand signal for Vietnam market               |
| **NPS Score**         | >50 (post-MVP survey)                                   | Positive sentiment; room for improvement noted |

### 14.4 Learnings (Qualitative)

- **Most common goal**: Home purchase or emergency fund? Validates primary focus.
- **Drop-off point**: Where do users leave? Inform UX iteration.
- **Feasibility accuracy**: Are user projections realistic? Refine assumptions.
- **Debt prevalence**: How often is debt a blocker? Informs next feature priority.
- **Income diversity**: How many users have side income? Shapes future income modeling.

---

## 15. Risks and Open Questions

### 15.1 Risk Assessment

| Risk                                            | Probability | Impact | Mitigation                                                             |
| ----------------------------------------------- | ----------- | ------ | ---------------------------------------------------------------------- |
| **Users distrust model accuracy**               | Medium      | High   | Published assumptions; comparison to real tools; user testimonials     |
| **Onboarding drop-off too high**                | Medium      | Medium | A/B test question order; progressive value demos; simplified variant   |
| **Calculation errors reduce trust**             | Low         | High   | Rigorous unit tests; comparison spreadsheet; manual QA                 |
| **Users forget login info; lose plans**         | Medium      | Low    | Email recovery; option to export on logout; session persistence        |
| **Data privacy concerns in Vietnam**            | Medium      | Medium | Clear privacy policy (Vietnamese); no data sharing; GDPR-style exports |
| **Market prefers English tools**                | Low         | Low    | Localization is differentiator; prioritize Vietnamese messaging        |
| **Users expect investment guidance**            | High        | Low    | Clear in onboarding: "savings plan, not investment advisor"            |
| **Scalability bottleneck on projection engine** | Low         | Medium | Simple calculations should scale easily; load test early               |
| **Competitor enters Vietnam market**            | Low         | High   | Speed to market; brand positioning as "Vietnam-first"                  |

### 15.2 Technical Risks

| Risk                         | Mitigation                                       |
| ---------------------------- | ------------------------------------------------ |
| Data loss on backend failure | Automated backups; disaster recovery plan        |
| Calculation precision errors | Comprehensive unit tests; comparison spreadsheet |
| Authentication bypass        | Security audit; penetration testing              |
| Session hijacking            | Secure cookies; CSRF tokens; rate limiting       |
| DDoS or bot attacks          | Rate limiting; WAF (Web Application Firewall)    |

### 15.3 Open Questions (For Stakeholder Alignment)

1. **Monetization Strategy**: Will MVP be free-to-use or freemium? If freemium, what's the paywall?
   - Implication: Affects "Save Plan" feature positioning (gated vs. free)

2. **Goal Expansion Timeline**: Will MVP support multiple simultaneous goals, or one at a time?
   - Implication: Data model design; recommendation engine scope

3. **Emergency Fund Depth**: Should "Emergency Fund" be equally promoted as house purchase, or secondary?
   - Implication: UX flow ordering; recommendation rules

4. **Income Complexity (Future)**: Will we support variable income (business owners, freelancers) post-MVP?
   - Implication: Data model flexibility; validation rule design

5. **Integration Plans**: Any plans to integrate with Vietnamese banks or real estate platforms?
   - Implication: Data import design; API architecture

6. **Mobile App**: Native mobile app post-MVP, or web-only long-term?
   - Implication: Tech stack choice; responsive design scope

7. **Scenario Capability**: Should MVP support "what-if" comparisons (e.g., 2 timelines side-by-side)?
   - Implication: Session data model; UI complexity

8. **User Support**: Live chat, email support, or FAQ-only for MVP?
   - Implication: Operational readiness; support staffing

### 15.4 Known Limitations (Document for Users)

1. **No investment modeling**: Projections assume 0% returns (cash savings only)
2. **No tax planning**: Interest and capital gains taxes not modeled
3. **No debt interest**: Debt calculations simplified; no compound interest
4. **Single goal focus**: Can't compare multiple goals simultaneously in MVP
5. **No external account data**: Must manually enter all financial data
6. **No market data**: Property prices, interest rates are user-entered or defaulted
7. **Deterministic only**: No probabilistic or scenario analysis (Monte Carlo)

---

## 16. Implementation Roadmap (High-Level)

### Phase 1: Foundation (Week 1-2)

- [ ] Backend API scaffolding (Node.js/Python; TBD)
- [ ] Database schema (PostgreSQL; users, plans, calculations)
- [ ] Authentication service (email/password; sessions)
- [ ] Projection calculation engine (unit tested)

### Phase 2: Frontend (Week 3-4)

- [ ] Onboarding flow UI (React/Vue; TBD)
- [ ] Input validation and error handling
- [ ] Dashboard display
- [ ] Save plan flow

### Phase 3: Polish & Testing (Week 5)

- [ ] E2E testing (happy path + edge cases)
- [ ] Localization (Vietnamese translation; QA)
- [ ] Performance optimization
- [ ] Security audit + HTTPS setup

### Phase 4: Launch & Monitor (Week 6)

- [ ] Staging environment smoke tests
- [ ] Beta user testing (10-20 Vietnamese users)
- [ ] GA setup; error tracking
- [ ] Production launch

---

## 17. Conclusion

FinPilot MVP is scoped for **rapid execution** (4-6 weeks) while delivering **core user value** (goal feasibility + projection + recommendations). The product prioritizes:

- **User trust**: Deterministic, explainable calculations
- **Simplicity**: One goal, linear math, rule-based recommendations
- **Speed**: 10-minute onboarding, no account required upfront
- **Vietnam focus**: Localized language, assumptions, and context

Success is defined by users completing onboarding, saving plans, and feeling confident about their financial goals. Secondary success is market validation that Vietnamese users will adopt a goal-first planning tool.

This specification is **implementation-ready** for design and engineering handoff. All ambiguities have been resolved; assumptions are explicit; acceptance criteria are measurable. Begin Phase 1 execution immediately.

---

**Document Version**: 1.0  
**Status**: Approved for Implementation  
**Last Updated**: 2026-03-21
