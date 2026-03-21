<!--
Sync Impact Report:
- Version change: template → 1.0.0
- List of modified principles: None (initial creation)
- Added sections: Product Scoping and Architecture Guidelines, Development and Testing Standards
- Removed sections: None
- Templates requiring updates: None
- Follow-up TODOs: None
-->

# FinPilot Constitution

## Core Principles

### I. Goal-Based Financial Planning

All features must center around helping users achieve specific financial goals. Every recommendation, calculation, and interface element should directly contribute to goal attainment. Financial planning is most effective when purpose-driven rather than feature-driven.

### II. Explainable Modeling

All financial models and calculations must be transparent and explainable to users. Users should understand how inputs lead to outputs, with clear breakdowns of assumptions and methodologies. Trust in financial advice requires understanding, not blind acceptance.

### III. Vietnam-First User Experience

Design and content must prioritize Vietnamese users' cultural context, regulatory environment, and financial behaviors. Use Vietnamese language, local currency (VND), and relevant financial products/institutions. Localization builds trust and ensures relevance in the Vietnamese market.

### IV. Deterministic Calculation Quality

All financial calculations must be deterministic, reproducible, and mathematically sound. No random elements or approximations that could lead to inconsistent results. Financial decisions require predictable, reliable calculations.

### V. Progressive Data Capture

Collect user data incrementally as needed for goal achievement, rather than requiring comprehensive upfront input. Allow users to start with minimal information and expand as they engage. Reduces user friction and enables broader adoption.

### VI. Trust-Centered Product Behavior

Every interaction must prioritize user trust through transparency, security, and ethical behavior. Avoid aggressive sales tactics, hidden fees, or manipulative design patterns. Financial products require the highest standards of integrity.

## Product Scoping and Architecture Guidelines

**Product Scoping**: Features are scoped only if they directly advance user financial goals. New capabilities must demonstrate clear goal-alignment before inclusion. Trade-offs favor goal-achievement over feature completeness.

**Technical Architecture**: Systems must support explainable models through modular, auditable components. Vietnam-first UX requires localized data handling and cultural adaptation layers. Deterministic calculations demand immutable computation pipelines. Progressive capture necessitates flexible data schemas. Trust-centered behavior requires comprehensive audit logging and security-first design.

**Recommendation Logic**: All recommendations must be goal-based, with clear reasoning provided to users. Logic must be deterministic and explainable, avoiding black-box algorithms. Recommendations should adapt progressively as more data becomes available.

**UX Decisions**: Interfaces must be Vietnam-first, using local conventions, language, and cultural norms. Progressive data capture means optional fields and guided workflows. Trust is built through transparent information display and clear action consequences.

## Development and Testing Standards

**Testing Standards**: Deterministic calculations require comprehensive unit tests with known inputs/outputs. Explainable models need tests validating reasoning transparency. Vietnam-first UX requires localization testing. Trust-centered behavior demands security and ethics testing. Progressive capture needs workflow testing across data states.

**Implementation Trade-offs**: Prioritize goal-based simplicity over complex features. Choose explainable algorithms over opaque optimizations. Favor deterministic precision over performance shortcuts. Balance progressive capture with data completeness requirements. Always err on the side of trust-building transparency.

## Governance

Constitution supersedes all other practices. Amendments require majority stakeholder approval, documentation of rationale, and migration plan for existing features. All product decisions must verify compliance with principles. Complexity must be justified against principle alignment. Regular reviews ensure ongoing adherence.

**Version**: 1.0.0 | **Ratified**: 2026-03-21 | **Last Amended**: 2026-03-21
