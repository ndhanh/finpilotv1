# FinPilot Landing Page — Product Specification

**Version**: 1.0  
**Date**: March 29, 2026  
**Status**: Ready for Implementation  
**Source**: [`prompts/landing.md`](../../prompts/landing.md)

---

## 1. Purpose

This document specifies the **marketing landing page** for **finpilot.vn**: a public, pre-login experience that educates Vietnamese users, creates emotional connection, visualizes a plausible financial future, and drives a single primary action—**“Bắt đầu ngay”**—without requiring authentication.

**Relationship to other specs**: The broader product behavior, planning flow, and backend are described in [`specs/001-mvp-core/spec.md`](../001-mvp-core/spec.md). This spec covers **only** the landing surface and its UI/copy; it does not redefine MVP calculation rules.

---

## 2. Repository Context

Marketing and the main product are **separate Next.js apps** (separate deploys: **finpilot.vn** vs **app.finpilot.vn**).

| Item | Location / note |
|------|------------------|
| Monorepo root | `finpilotv1/` |
| **Marketing site** (finpilot.vn) | `marketing/` — App Router under `marketing/src/app/` |
| Landing route | `marketing/src/app/page.tsx` |
| Marketing UI | `marketing/src/components/` (suggested: `landing/`) |
| App URL for CTAs | `NEXT_PUBLIC_APP_URL` → links to `${APP}/plan` (see `marketing/src/lib/app-url.ts`) |
| **Main app** (app.finpilot.vn) | `frontend/` — planning flow, dashboard, API client |
| App root `/` | `frontend/src/app/page.tsx` redirects to `/plan` (no marketing on app host) |
| Utilities & types | `marketing/src/lib/`, `frontend/src/lib/`, etc. |
| Global styles | `marketing/src/app/globals.css` |
| **Current state** | Marketing home is a minimal hero; CTAs use **“Bắt đầu ngay”** and absolute URL to the app. Full landing sections from §4 are still to be implemented here. |

**Stack (aligned with prompt and existing frontend)**:

- Next.js (App Router), TypeScript, Tailwind CSS  
- Functional React components; mobile-first responsive layout  

---

## 3. Goals and Non-Goals

### 3.1 Goals

1. **Educate** visitors on what FinPilot does (goal-based planning for Vietnamese users).  
2. **Emotional resonance** through outcome-focused messaging (e.g. financial freedom, buying a home).  
3. **Visual credibility** via a **Wow** section: savings trajectory and “with vs without planning” comparison, including a concrete example (e.g. buy a house at age 32).  
4. **Conversion**: prominent **“Bắt đầu ngay”** CTAs linking to the **main app** planning entry: absolute URL `${NEXT_PUBLIC_APP_URL}/plan` (not a path on the marketing host).  
5. **Trust**: dedicated trust content; FAQ for objections.  
6. **No login** on this page; CTAs must not imply account creation is required to start.

### 3.2 Non-Goals

- Full product onboarding or persistence (handled by the **main app** at `/plan` and related routes on app.finpilot.vn).  
- Real user data or API-backed projections on the landing page (use **mock data** only).  
- Perfect charting fidelity; prefer **simple** visualization (div-based bars/lines or a lightweight chart library).  
- Backend changes strictly for landing (not required unless linking strategy demands it).

---

## 4. Page Structure

Implement the landing as a **single scroll page** composed of the following sections **in order**:

| # | Section | Role |
|---|---------|------|
| 1 | **HeroSection** | Headline, subheadline, primary CTA, optional **mock dashboard preview** (card layout). |
| 2 | **ProblemSection** | Pain points / why planning matters. |
| 3 | **SolutionSection** | How FinPilot addresses those pains (simple, clear). |
| 4 | **WowSection** | **Critical**: savings growth over time; milestone example; **with planning vs without**; chart + timeline UI. |
| 5 | **FeatureSection** | 3–4 feature cards (see Section 5). |
| 6 | **TrustSection** | Trust signals (methodology tone, transparency, localization—exact content is implementation detail). |
| 7 | **CTASection** | Repeat benefit + **“Bắt đầu ngay”**; reinforce no login. |
| 8 | **FAQSection** | Short FAQs to reduce friction. |

**Composition**: `marketing/src/app/page.tsx` imports and stacks these section components. Each section lives in `marketing/src/components/` as a dedicated file (or folder if a section splits into smaller pieces).

---

## 5. Section Requirements

### 5.1 Hero

- **Headline**: Outcome-driven (financial freedom, buying a home, etc.—Vietnamese copy).  
- **Subheadline**: One short explanation of FinPilot.  
- **Primary CTA**: Label **“Bắt đầu ngay”**; navigates to the start of the planning journey.  
- **Mock dashboard preview**: Card-based layout suggesting the in-app experience (static mock).

### 5.2 Problem & Solution

- Clear, scannable copy; avoid long paragraphs on mobile.  
- Align messaging with MVP positioning: goal-centric, honest projections, Vietnamese context.

### 5.3 Wow (Financial Simulation)

- Show **savings growth over time** (mock series).  
- Include an **example narrative** (e.g. goal: buy house at age 32).  
- **Comparison**: two tracks—**with planning** vs **without planning** (e.g. different savings trajectories or milestone timing).  
- **Visualization**: simple chart (div-based or small library) + **timeline** UI (milestones on a horizontal or vertical timeline).  
- Data from **mock modules** (see Section 7).

### 5.4 Features (3–4 cards)

Cover these themes (titles/descriptions in Vietnamese):

1. Goal-based planning  
2. Simulation (may reference **Monte Carlo** as a *concept* for education—does not require implementing Monte Carlo on the landing page)  
3. Seasonal / contextual advice  
4. Couple planning  

### 5.5 Trust

- Reinforce transparency and suitability for Vietnamese users (no false precision).  
- Optional: logos, quotes, or principles—keep lightweight.

### 5.6 CTA (bottom)

- Restate core benefit.  
- **“Bắt đầu ngay”** again.  
- Explicit **no login required** messaging.

### 5.7 FAQ

- Short Q&A; addresses common concerns (data, how it works, who it’s for).

---

## 6. Styling and UX

- **Visual language**: Clean **fintech** aesthetic—generous spacing, readable typography, soft shadows.  
- **Interaction**: Subtle hover states on buttons and cards.  
- **Responsive**: Mobile-first; sections stack; chart/timeline usable on narrow viewports.  
- **Language**: UI strings for this page should be **Vietnamese** for the marketing layer (consistent with `lang="vi"` in `marketing` root layout); adjust `metadata` in `marketing/src/app/layout.tsx` if titles/descriptions should match the new positioning.

---

## 7. Mock Data

Centralize simple, readable mock data (e.g. `marketing/src/lib/landing-mock.ts` or `marketing/src/data/landing.ts`):

| Data | Purpose |
|------|---------|
| Savings projection series | Wow chart (with vs without planning). |
| Timeline milestones | Wow timeline (ages or dates, labels). |

Data should be **realistic but obviously illustrative** (rounded numbers, clear labels). No need to match backend formulas on the landing page. Store under `marketing/src/lib/` or `marketing/src/data/`.

---

## 8. Code Quality

- Small, reusable components; clear names (`HeroSection`, `WowSection`, etc.).  
- Avoid unnecessary abstraction; prioritize **working UI** and clarity.  
- No blocking questions during implementation—reasonable defaults per [`prompts/landing.md`](../../prompts/landing.md).

---

## 9. Acceptance Criteria

1. `npm run dev` (from repo root: `npm run dev:marketing`, or `marketing/` with port **3001**) runs without errors; landing loads at `/` on the marketing app.  
2. All **eight** sections appear on the home page in the specified order.  
3. At least two **“Bắt đầu ngay”** CTAs (hero + bottom CTA) link to the correct **app** URL (`NEXT_PUBLIC_APP_URL` + `/plan`).  
4. **WowSection** includes: growth visualization, with/without comparison, timeline, and mock-driven data.  
5. **FeatureSection** has 3–4 cards covering the listed themes.  
6. Layout is usable on mobile and desktop; no critical overflow or unreadable chart on common breakpoints.  
7. Copy and CTAs communicate **no login** to start.

---

## 10. Traceability

| Prompt section | Spec section |
|----------------|--------------|
| Project context & goals | §1, §3 |
| Setup & folders | §2 |
| Page structure | §4 |
| Hero, Wow, Features, CTA | §5.1, §5.3–§5.4, §5.6 |
| Styling & UX | §6 |
| Mock data | §7 |
| Code quality & run | §8, §9 |

---

## 11. Open Implementation Choices (Explicit Defaults)

The prompt allows assumptions. Recommended defaults:

- **Primary CTA target**: full URL to main app — `${NEXT_PUBLIC_APP_URL}/plan` (dev: `http://localhost:3000/plan`).  
- **Chart**: CSS/div bars or a minimal dependency already acceptable in the project—avoid heavy chart frameworks unless already present.  
- **Component folder**: `marketing/src/components/landing/*` (keeps product components in `frontend/` only).

These can be revised without changing the spec’s intent.
