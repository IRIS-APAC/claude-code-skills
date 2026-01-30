# Project Constraints Template

# Project Constraints: [Project Name]

**Last Updated**: [Date]
**Project**: [Project Name]
**Status**: 🚧 In Progress | 📝 Draft | ✅ Complete
**Reviewed By**: [Names/Roles who approved these constraints]

---

## Purpose of This Document

This document captures the **non-negotiable constraints** and **guiding principles** for this project. These constraints define the boundaries within which design and implementation decisions must be made.

**Key Distinction**:
- ✅ **Constraints** (Non-Negotiable): Must be respected, documented here
- ℹ️ **Preferences** (Flexible): Can be challenged, documented separately

---

## Summary

**Critical Constraints**:
1. [Most important constraint, e.g., "Must use Azure"]
2. [Second most important, e.g., "Must launch by Q2 2026"]
3. [Third most important, e.g., "Budget cap: $100K"]

**Flexibility Level**: [Low | Medium | High]
- Low: Most decisions are constrained
- Medium: Some flexibility within boundaries
- High: Few hard constraints, mostly principles

---

## Non-Negotiable Constraints

### 1. Platform & Infrastructure Constraints

#### Constraint: [Platform Mandate]

**Description**: [e.g., "All services must run on Azure"]

**Type**: Platform Mandate | Technology Standard | Infrastructure Requirement

**Rationale**:
- [Why this constraint exists, e.g., "Enterprise agreement with Microsoft"]
- [Business/technical reason, e.g., "Existing infrastructure and team expertise"]
- [Who decided and when, e.g., "Enterprise Architecture decision, Jan 2025"]

**Impact on Design**:
- [How this affects architecture, e.g., "All cloud services must be Azure-native"]
- [What we can't do, e.g., "Cannot use AWS services"]
- [What we must do, e.g., "Must use Azure Container Apps for hosting"]

**Flexibility**: None | Limited | Exception Process Available
- [If flexible, explain process, e.g., "Can request exception via Architecture Review Board (6-week process, rarely approved)"]
- [If none, state clearly: "This is absolute - no exceptions"]

**Verification**:
- How to check compliance: [e.g., "All infrastructure code must use Azure Resource Manager templates"]
- Who validates: [e.g., "Cloud Engineering team reviews all deployments"]

---

#### Constraint: [Technology Standard]

**Description**: [e.g., "Only Python, TypeScript, and Java are approved languages"]

**Type**: Technology Standard | Security Policy | Compliance Requirement

**Rationale**:
- [e.g., "Team expertise - all developers proficient in these languages"]
- [e.g., "Hiring pipeline - recruiters screen for these skills"]
- [e.g., "Tooling support - CI/CD, security scanning configured for these"]

**Impact on Design**:
- [Can use: Python, TypeScript, Java]
- [Cannot use: Go, Rust, Ruby, etc.]
- [Must justify: Any new frameworks or major libraries]

**Flexibility**: Limited
- [Exception process if available]
- [Timeline for exceptions, e.g., "Architecture review: 2-3 weeks"]
- [Approval criteria, e.g., "Must show significant benefit + training plan"]

**Verification**:
- Automated checks: [e.g., "CI/CD pipeline rejects non-approved languages"]
- Code review: [e.g., "Tech leads verify during PR review"]

---

### 2. Architecture Principles

#### Principle: [e.g., "Reuse over Buy over Build"]

**Description**: Prioritize reusing existing solutions, then buying commercial services, then building custom only as last resort

**Type**: Architecture Principle | Design Philosophy | Strategic Direction

**Rationale**:
- [Reduce technical debt and maintenance burden]
- [Faster time to market]
- [Focus engineering effort on business differentiation]

**Application**:
1. **First**: Check if existing internal platforms can be extended
   - [List internal platforms, e.g., "Enterprise API Gateway, Shared Auth Service"]
   - [Who to contact, e.g., "Platform team via #platform-requests Slack"]
2. **Second**: Evaluate commercial SaaS/PaaS offerings
   - [Approval process, e.g., "Procurement review required for >$5K/year"]
   - [Evaluation criteria, e.g., "Security certification, SLA, cost"]
3. **Third**: Build custom (requires justification)
   - [What justification needed, e.g., "Cost/benefit analysis, 3-year TCO comparison"]
   - [Who approves, e.g., "Architecture Review Board"]

**Flexibility**: Moderate
- [Can build if justified with data]
- [Can buy if internal platform doesn't meet needs]
- [Must document decision rationale in ADR (Architecture Decision Record)]

**Examples**:
```
✅ Good: "Evaluated internal auth service. Doesn't support MFA. Evaluated Okta ($15K/year) vs Auth0 ($12K/year). Recommend Okta (already approved vendor)."

✅ Good: "Need message queue. Internal messaging platform supports our use case. Using that."

❌ Bad: "Building custom message queue for learning purposes."

❌ Bad: "Using Auth0 without checking if internal auth service can be extended."
```

---

### 3. Compliance & Security Requirements

#### Constraint: [e.g., "Must comply with GDPR"]

**Description**: All systems handling EU personal data must comply with GDPR

**Type**: Legal Requirement | Compliance Mandate | Regulatory Constraint

**Rationale**:
- [Operating in EU]
- [Legal penalties for non-compliance]
- [Customer trust and brand protection]

**Specific Requirements**:
- **Data Residency**: [All EU user data must be stored in EU regions]
- **Right to be Forgotten**: [Must support data deletion within 30 days]
- **Consent Management**: [Explicit opt-in required for data processing]
- **Data Portability**: [Users can export their data in standard format]
- **Breach Notification**: [72-hour notification requirement]

**Impact on Design**:
- [Must use Azure EU regions only]
- [Must implement soft-delete + permanent delete workflows]
- [Must integrate with Consent Management Platform]
- [Must design data export API]
- [Must implement breach detection and notification system]

**Flexibility**: None (legally required)

**Verification**:
- Security review: [Security team reviews all data handling]
- Legal review: [Legal team reviews terms of service and privacy policy]
- Compliance audit: [Annual third-party GDPR audit]

---

#### Constraint: [e.g., "Must use Okta for SSO"]

**Description**: All applications must authenticate users via enterprise Okta SSO

**Type**: Organizational Mandate | Security Policy

**Rationale**:
- [Centralized identity management]
- [Security policy - no application-specific passwords]
- [Compliance - SAML SSO required for SOC 2]

**Technical Requirements**:
- Protocol: [SAML 2.0 or OIDC]
- Integration: [Use Okta SDK or standard SAML library]
- MFA: [Enforced at Okta level (no need to implement in app)]

**Impact on Design**:
- [Cannot use alternative auth providers (no Auth0, Firebase Auth, etc.)]
- [Cannot implement custom password auth]
- [Must handle Okta token lifecycle]

**Flexibility**: None

**Verification**:
- [Security team must approve any authentication implementation]
- [Penetration testing validates no auth bypasses]

---

### 4. Budget & Resource Constraints

#### Constraint: [Budget Cap]

**Description**: Total project budget capped at $100,000

**Type**: Budget Constraint | Financial Limit

**Breakdown**:
- Infrastructure: [$30K/year]
- Development: [$50K (contractor costs)]
- SaaS/Licenses: [$10K/year]
- Contingency: [$10K]

**Rationale**:
- [Approved budget allocation for fiscal year]
- [ROI target: break even within 18 months]

**Impact on Design**:
- [Must optimize for cost - prefer PaaS over IaaS]
- [Must size infrastructure conservatively]
- [Must evaluate build vs buy carefully]
- [Must consider open-source alternatives]

**Flexibility**: Limited
- [Can request additional $25K with business case]
- [Requires VP approval + 4-week process]
- [Rarely approved unless critical]

**Cost Monitoring**:
- Monthly review: [Project manager tracks actual vs budget]
- Alerts: [Notify if trending >10% over budget]

---

#### Constraint: [Timeline Deadline]

**Description**: Must launch by June 30, 2026

**Type**: Fixed Deadline | Regulatory Requirement | Business Commitment

**Rationale**:
- [New data protection law takes effect July 1, 2026]
- [System must be compliant before law is active]
- [Penalties for non-compliance: fines + legal liability]

**Milestones**:
| Date | Milestone | Criticality |
|------|-----------|-------------|
| Feb 28, 2026 | Architecture approved | High |
| Apr 30, 2026 | Core features complete | High |
| May 31, 2026 | Testing & security review complete | Critical |
| Jun 15, 2026 | Deployment to production | Critical |
| Jun 30, 2026 | Launch | Absolute |

**Impact on Design**:
- [Scope must be ruthlessly prioritized]
- [MVP-first approach required]
- [May need to defer nice-to-have features to Phase 2]
- [Technical debt acceptable if contained]

**Flexibility**: None (regulatory deadline)

**Contingency**:
- [If at risk, must escalate by Apr 1, 2026]
- [Options: reduce scope, increase team, accept penalties]

---

### 5. Team & Organizational Constraints

#### Constraint: [Team Size Fixed]

**Description**: Team is 3 developers, cannot grow

**Type**: Resource Constraint | Hiring Freeze

**Current Team**:
- Backend: [1 senior developer]
- Frontend: [1 mid-level developer]
- Full-stack: [1 junior developer]

**Skills**:
- Strong: [Python, TypeScript, React, PostgreSQL]
- Moderate: [Azure, Docker, CI/CD]
- Weak: [Kubernetes, service mesh, distributed systems]

**Rationale**:
- [Budget constraints]
- [Hiring freeze across organization]

**Impact on Design**:
- [Must limit operational complexity]
- [Must use managed services heavily]
- [Must avoid technologies requiring specialized expertise]
- [Must design for team's existing skills]

**Flexibility**: Limited
- [Can engage contractors for specific short-term needs (< 3 months)]
- [Can request training budget for upskilling]
- [Cannot hire permanent headcount]

---

#### Constraint: [Required Process/Team Involvement]

**Description**: Security team must review before production deployment

**Type**: Process Requirement | Governance Policy

**Process**:
1. Submit security review request 3 weeks before planned deployment
2. Provide: threat model, data flow diagrams, auth/authz design
3. Security team reviews within 2 weeks
4. Address any findings
5. Get sign-off

**Rationale**:
- [Risk management policy]
- [Required for insurance coverage]
- [SOC 2 compliance requirement]

**Impact on Timeline**:
- [Add 3-week buffer to deployment timeline]
- [Can get preliminary feedback early (recommended)]
- [Critical/high findings may block deployment]

**Flexibility**: None (required by policy)

**Best Practice**:
- [Engage security team early for design review]
- [Schedule formal review 4-5 weeks before launch]
- [Have contingency plan for findings]

---

## Flexible Preferences (Not Constraints)

These are preferences that can be challenged with data/rationale:

### Preference: [e.g., "Would prefer microservices"]

**Type**: Architectural Preference

**Rationale**: [e.g., "Modern approach, perceived scalability benefits"]

**Flexibility**: ⭐⭐⭐ FULLY OPEN TO CHALLENGE
- [This is aspirational, not required]
- [Alternative approaches acceptable if justified]
- [Decision should be based on team size, complexity, scale]

**Challenge Welcome**: Yes - please research and recommend best approach for context

---

### Preference: [e.g., "Would like to use GraphQL"]

**Type**: Technology Preference

**Rationale**: [e.g., "Developer interest, learning opportunity"]

**Flexibility**: ⭐⭐ OPEN TO DISCUSSION
- [Not required, but team would like to try]
- [REST is acceptable alternative]
- [Recommend approach based on requirements]

**Challenge Welcome**: Yes - analyze trade-offs and recommend

---

## How to Work with These Constraints

### Respect Absolute Constraints
✅ **Do**:
- Accept platform mandates (Azure vs AWS)
- Follow architecture principles (Reuse > Buy > Build)
- Meet compliance requirements (GDPR, SOC 2)
- Work within budget caps and timelines
- Involve required teams (Security review)

❌ **Don't**:
- Suggest technologies outside approved list
- Propose solutions that violate compliance
- Ignore budget or timeline constraints
- Skip required processes or reviews

### Work Creatively Within Constraints
Examples:
- "Since Azure is required, let's use Azure Container Apps instead of Kubernetes"
- "To meet budget, let's use PaaS services instead of building infrastructure"
- "Given timeline, let's defer feature X to Phase 2 and focus on compliance"
- "Since team is small, let's use managed services to minimize operational burden"

### Challenge Gently When Appropriate
When to challenge (respectfully):
- Constraint seems to contradict other constraints
- Constraint has major cost/complexity implications
- Constraint lacks clear rationale
- Better alternative exists that meets same goals

How to challenge:
```
"I understand [constraint]. I researched [alternatives] and found [option] achieves
the same goal with [benefits]. Given [context], would you be open to [alternative]?

If not, I'll work within the constraint and optimize accordingly."
```

---

## Constraint Change Log

| Date | Constraint | Change | Reason | Approved By |
|------|-----------|--------|--------|-------------|
| 2025-01-15 | Budget | Increased from $80K to $100K | Additional features requested | VP Engineering |
| 2025-02-01 | Platform | Added exception process for AWS | Cost comparison needed | Enterprise Architecture |

---

## Open Questions & Unknowns

> **CRITICAL**: These must be resolved before finalizing constraints. Escalate if blocked.

### Constraint Clarifications

| # | Question | Status | Notes/Decision |
|---|----------|--------|----------------|
| Q1 | [Example: Is Azure mandate absolute or can we request exception?] | ⏳ PENDING | **Action**: [Who] to clarify by [when] |
| Q2 | [Example: What's the approved exception process for technology choices?] | ✅ RESOLVED | [Decision and process documented] |

### Budget & Timeline

| # | Question | Status | Notes/Decision |
|---|----------|--------|----------------|
| Q1 | [Example: Is budget cap firm or flexible with business case?] | ⏳ PENDING | **Action**: Finance to confirm |

**Document Completeness**: This document is complete when all questions are resolved or explicitly accepted as "will resolve later."

---

## Contact & Escalation

**Questions about constraints**: [Team/person who can clarify]

**Request exception**: [Process and who to contact]

**Escalation**: [Who to escalate to if constraint is blocking progress]

---

## Document Review

**Review Frequency**: [Quarterly | Per milestone]

**Next Review**: [Date]

**Owner**: [Role/person responsible for keeping this current]
