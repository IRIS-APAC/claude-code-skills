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

#### Constraint: [Data Sovereignty]

**Description**: All data must be stored and processed within specific geographic regions

**Type**: Legal Requirement | Compliance Mandate | Regulatory Constraint

**Specific Requirements**:
- **Allowed Regions**: [e.g., "EU only", "Australia only", "US + Canada"]
- **Prohibited Regions**: [e.g., "Cannot use US data centers for EU customer data"]
- **Data Transfer**: [e.g., "Cross-border transfers require Standard Contractual Clauses (SCCs)"]
- **Backup/DR**: [e.g., "Backups must also remain in-region"]

**Rationale**:
- [GDPR Article 44-50 requirements for EU data]
- [Australian Privacy Principles (APPs) requirements]
- [Customer contractual requirements]
- [National security/government regulations]

**Impact on Design**:
- [Must use Azure Australia East/Southeast regions only]
- [Cannot use multi-region replication across borders]
- [Must design region-specific deployments]
- [Must configure CDN to respect data locality]

**Flexibility**: None (legally required)

**Verification**:
- Infrastructure audit: [All resources deployed to approved regions only]
- Data flow review: [Security team validates no cross-border data movement]
- Compliance check: [Annual audit confirms data sovereignty compliance]

---

#### Constraint: [Compliance Standards]

**Description**: System must comply with specific industry/security standards

**Type**: Certification Requirement | Regulatory Compliance | Customer Requirement

**Required Standards**:
| Standard | Scope | Deadline | Impact |
|----------|-------|----------|--------|
| ISO 27001 | Information security management | [By Q2 2026] | Security controls, risk management, documentation |
| SOC 2 Type II | Security, availability, confidentiality | [Annual recertification] | Audit trail, access controls, monitoring |
| PCI-DSS Level 1 | Payment card data handling | [If handling card data] | Encryption, network segmentation, vulnerability scanning |
| HIPAA | Healthcare data (if applicable) | [Before patient data] | PHI encryption, BAAs, audit logs |
| CPS 234 | Australian prudential standard (if applicable) | [Ongoing] | Information security capability |
| NIST 800-53 | Federal systems (if government) | [Before deployment] | Comprehensive security controls |

**Specific Requirements**:
- **Access Control**: [MFA required, role-based access, least privilege]
- **Data Encryption**: [At-rest: AES-256, In-transit: TLS 1.3+]
- **Audit Logging**: [All access/changes logged, 7-year retention]
- **Vulnerability Management**: [Monthly scanning, critical patches within 30 days]
- **Incident Response**: [Documented plan, tested annually]
- **Business Continuity**: [RTO: 4 hours, RPO: 1 hour]

**Rationale**:
- [Customer contracts require SOC 2 certification]
- [Industry regulation mandates PCI-DSS for payment processing]
- [ISO 27001 demonstrates security maturity to enterprise customers]

**Impact on Design**:
- [Must implement centralized logging to SIEM]
- [Must use HSM or key vault for encryption keys]
- [Must implement network segmentation]
- [Must design for audit trails on all sensitive operations]
- [Must integrate with enterprise security tools (vulnerability scanner, SIEM)]

**Flexibility**: None (contractual/regulatory requirement)

**Compliance Evidence**:
- Security controls documentation: [Required for auditors]
- Test results: [Penetration testing, vulnerability scans]
- Process documentation: [Incident response plan, change management]
- Audit logs: [Automated collection and retention]

**Compliance Timeline**:
| Milestone | Date | Owner |
|-----------|------|-------|
| Controls implementation | [Q1 2026] | Engineering + Security |
| Internal audit | [Q2 2026] | Internal Audit team |
| Remediation | [Q3 2026] | Engineering |
| External audit | [Q4 2026] | Third-party auditor |
| Certification | [Q4 2026] | Compliance team |

---

### 4. Existing Architecture & Technical Landscape

> **Purpose**: Document the existing systems, technologies, and architecture that constrain or inform design decisions.

#### Current Architecture

**Description**: [Overview of existing system architecture, if any]

**Type**: Greenfield | Brownfield | Hybrid | Legacy Modernization

**Existing Systems**:
| System/Service | Purpose | Technology Stack | Status | Integration Points |
|---------------|---------|------------------|--------|-------------------|
| [System name] | [What it does] | [Tech used] | [Active/Legacy/Deprecated] | [How we integrate] |
| [Example: User Service] | User management & auth | Node.js, PostgreSQL, Redis | Active | REST API, shared DB |
| [Example: Billing System] | Payment processing | Java, Oracle DB | Legacy (replacing 2027) | SOAP API (unreliable) |

**Existing Data Stores**:
- **Primary**: [e.g., "PostgreSQL 14 cluster (3 nodes, 500GB)"]
- **Cache**: [e.g., "Redis (shared with other services)"]
- **Analytics**: [e.g., "Snowflake data warehouse"]
- **Files**: [e.g., "S3 bucket (2TB of user uploads)"]

**Existing Infrastructure**:
- **Cloud**: [e.g., "AWS (99% of workloads)", "On-prem datacenter (legacy only)"]
- **Container Orchestration**: [e.g., "ECS Fargate", "Kubernetes 1.27", "None - VMs only"]
- **CI/CD**: [e.g., "GitHub Actions", "Jenkins (legacy)"]
- **Monitoring**: [e.g., "DataDog", "Prometheus + Grafana", "None yet"]

**Architecture Patterns in Use**:
- [e.g., "Monolithic Rails app (main product)"]
- [e.g., "Microservices for new features (5 services)"]
- [e.g., "Event-driven with SNS/SQS"]
- [e.g., "API Gateway → Lambda → DynamoDB"]

**Rationale for Documenting**:
- [Understand what already exists]
- [Identify integration points and dependencies]
- [Respect existing investment and knowledge]
- [Plan migration paths if needed]

**Impact on Design**:
- **Must integrate with**: [List systems that cannot be replaced]
- **Should leverage**: [Existing infrastructure/services we should use]
- **Can replace**: [Legacy systems scheduled for retirement]
- **Data migration needed**: [If moving from existing datastores]

**Technical Debt**:
- [Known issues with current architecture, e.g., "Billing SOAP API is slow and unreliable"]
- [Planned improvements, e.g., "Migrating to new billing service in Q3 2026"]
- [Workarounds needed, e.g., "Must cache billing API responses aggressively"]

**Migration Strategy** (if applicable):
- [ ] **Strangler Fig**: Gradually replace legacy system while it runs
- [ ] **Big Bang**: Full replacement in one deployment
- [ ] **API Facade**: Keep legacy, add modern interface
- [ ] **No Migration**: Build alongside existing systems

**Flexibility**: Varies by component
- [Some systems are untouchable (e.g., core billing)]
- [Some can be replaced if justified (e.g., old admin UI)]
- [Document which is which]

**Examples**:
```
✅ Good: "Current system uses PostgreSQL. New service will also use PostgreSQL for consistency and can share connection pooling infrastructure."

✅ Good: "Legacy billing API is unreliable. Will implement circuit breaker pattern and aggressive caching. Planning full replacement in Q3 2026."

❌ Bad: "Ignoring existing user service and building a new one without migration plan."

❌ Bad: "Proposed MongoDB for new feature when entire stack uses PostgreSQL (adds operational complexity)."
```

---

### 5. Development & Documentation Infrastructure

#### Constraint: [Source Control System]

**Description**: Source code repository and organization structure

**Type**: Organizational Standard | Tooling Requirement

**Specific Requirements**:
- **Platform**: [e.g., "GitHub Enterprise", "GitLab", "Bitbucket", "Azure DevOps"]
- **Organization**: [e.g., "github.com/company-name"]
- **Repository Structure**:
  - [e.g., "Monorepo: company-name/platform"]
  - [e.g., "Multi-repo: company-name/service-name"]
- **Branch Protection**: [e.g., "Main/develop branches protected, PR reviews required"]
- **Access Control**: [e.g., "SSO via Okta, team-based permissions"]

**Rationale**:
- [Enterprise GitHub license already purchased]
- [Standardized across organization for consistency]
- [Integration with CI/CD and security scanning tools]

**Impact on Design**:
- [Must use Git for version control]
- [Must follow GitFlow branching strategy]
- [Must configure branch protection rules]
- [Must integrate with approved CI/CD (GitHub Actions, Azure Pipelines)]

**Repository Setup**:
```
Organization: github.com/company-name
Repository: company-name/project-name
Branches: main (production), develop (integration), feature/* (development)
Access: Engineering team (write), Security team (read), Contractors (read on specific repos)
```

**Flexibility**: None (organizational standard)

**Verification**:
- [IT configures repository according to template]
- [Security team validates access controls]

---

#### Constraint: [Documentation Storage]

**Description**: Where project and technical documentation must be maintained

**Type**: Organizational Standard | Knowledge Management

**Specific Requirements**:
- **Design Documents**: [e.g., "Stored in docs/Design/ in repository"]
- **API Documentation**: [e.g., "OpenAPI specs in repo, published to internal developer portal"]
- **User Documentation**: [e.g., "Confluence wiki: company.atlassian.net/wiki/spaces/PROJ"]
- **Runbooks/Operations**: [e.g., "PagerDuty knowledge base"]
- **Architecture Decisions**: [e.g., "ADRs in docs/ADR/ in repository"]

**Rationale**:
- [Single source of truth for each doc type]
- [Searchability across organization]
- [Version control for technical docs]
- [Access control and permissions]

**Documentation Types**:
| Type | Location | Format | Audience |
|------|----------|--------|----------|
| Design docs | Repository: docs/Design/ | Markdown | Technical team |
| ADRs | Repository: docs/ADR/ | Markdown | Architects, engineers |
| API specs | Repository: docs/API/ + Developer portal | OpenAPI/Swagger | Developers |
| User guides | Confluence wiki | Confluence pages | End users |
| Runbooks | PagerDuty / Wiki | Markdown/Wiki | Operations team |
| Meeting notes | Confluence | Confluence pages | Stakeholders |

**Impact on Design**:
- [Must maintain design docs in repository alongside code]
- [Must generate API docs from code (OpenAPI annotations)]
- [Must keep docs up-to-date with code changes]
- [Must follow documentation templates and standards]

**Flexibility**: Low
- [Can propose alternative for specific use case with justification]
- [Requires Platform team approval]

**Documentation Standards**:
- [Use Markdown for technical docs in repository]
- [Use Confluence for stakeholder-facing content]
- [Use inline code comments for implementation details]
- [Update docs in same PR as code changes]

---

### 6. Budget & Resource Constraints

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

### 7. Team Capacity & Capability

> **Purpose**: Document who is doing the work and what constraints that creates.

#### Constraint: [Team Composition & Capacity]

**Description**: [Describe who is building this - solo developer, small team, large organization, etc.]

**Type**: Resource Constraint | Capacity Limitation | Skills Constraint

**Current Capacity**:

*Choose the scenario that applies:*

**Scenario 1: Solo Developer / Building It Yourself**
- **You**: [Your role, e.g., "Full-stack developer", "Technical founder", "Product engineer"]
- **Availability**: [e.g., "20 hours/week (nights & weekends)", "Full-time", "50% of time (other projects too)"]
- **Your Skills**:
  - Strong: [e.g., "React, Node.js, PostgreSQL, AWS basics"]
  - Learning: [e.g., "TypeScript, Docker"]
  - Weak/Avoid: [e.g., "Kubernetes, distributed systems, DevOps"]
- **Support Available**: [e.g., "Can ask CTO for architecture review", "Have DevOps consultant on retainer (5 hrs/month)", "None - solo"]

**Scenario 2: Small Team (2-5 people)**
- **Team Size**: [e.g., "3 developers"]
- **Team Composition**:
  - Backend: [e.g., "1 senior developer (you)"]
  - Frontend: [e.g., "1 mid-level developer"]
  - Full-stack: [e.g., "1 junior developer"]
- **Collective Skills**:
  - Strong: [Python, TypeScript, React, PostgreSQL]
  - Moderate: [Azure, Docker, CI/CD]
  - Weak: [Kubernetes, service mesh, distributed systems]
- **Contractors/Support**: [e.g., "Can hire contractors for < 3 months", "DevOps team provides infrastructure support"]

**Scenario 3: Established Team**
- **Team Size**: [e.g., "12 engineers across 3 squads"]
- **Specializations**: [e.g., "Backend squad (4), Frontend squad (4), Platform squad (4)"]
- **Support Functions**: [e.g., "Dedicated DevOps (2), QA (3), Security (shared)"]
- **Skills**: [Document team-wide capabilities]

**Rationale for Constraints**:
- [Budget constraints - cannot hire]
- [Timeline - working solo means slower delivery]
- [Skills gaps - team needs to learn new tech]
- [Availability - part-time work only]

**Impact on Design**:
- **Operational Complexity**: [Must limit to what team can manage, e.g., "Avoid Kubernetes if solo developer"]
- **Technology Choices**: [Must match team skills, e.g., "Stick to Python since that's what we know"]
- **Scope**: [Must be realistic about what team can build, e.g., "Cannot build complex distributed system with 1 developer"]
- **Support Model**: [e.g., "Must use managed services since no ops team", "Need excellent documentation for junior devs"]
- **Pace**: [e.g., "Solo developer → expect 6 months not 2 months", "Small team → simpler architecture"]

**Growth Options** (if applicable):
- **Can grow**: [e.g., "Budget approved to hire 2 more devs in Q3"]
- **Contractors**: [e.g., "Can engage contractors for specific needs (< 3 months)"]
- **Training**: [e.g., "Budget available for courses/certifications"]
- **Cannot grow**: [e.g., "Hiring freeze - team size is fixed"]

**Flexibility**: [None | Limited | Moderate]
- [Document what's possible vs what's not]

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
