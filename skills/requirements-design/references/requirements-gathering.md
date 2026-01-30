# Requirements Gathering Guide

This guide provides a structured approach to gathering requirements through progressive questioning. Don't ask all questions at once—adapt to the conversation flow and the user's context.

---

## Phase 1: Project Context & Vision

### 1.1 Problem Understanding

**Core Questions:**
- What problem are we trying to solve?
- Who is experiencing this problem?
- How do they currently handle this problem (manual process, existing system, workaround)?
- What is the impact of not solving this problem (cost, time, frustration, missed opportunities)?

**Probing Questions:**
- Can you describe a specific example or scenario where this problem occurs?
- How frequently does this problem occur?
- Are there specific pain points that stand out?

**What to Listen For:**
- Quantifiable impact (hours wasted, cost, error rates)
- Emotional language (frustration, confusion, anxiety)
- Workarounds (signs of unmet needs)

---

### 1.2 Vision & Goals

**Core Questions:**
- What does success look like for this project?
- How will we know this project has succeeded?
- What are the key metrics or KPIs?
- What business value does this deliver?

**Probing Questions:**
- If this project is wildly successful, what changes for your organization/users?
- What capabilities will users have that they don't have today?
- Are there secondary benefits beyond the main goal?

**What to Document:**
- Success criteria (specific, measurable)
- Primary metrics (leading indicators)
- Secondary benefits

---

### 1.3 Stakeholders & Users

**Core Questions:**
- Who requested this project and why?
- Who will use this system? (list all user groups)
- Who will be impacted by this system? (even if not direct users)
- Who are the decision-makers?
- Who will maintain/operate this system?

**For Each User Group:**
- What is their role?
- What are their goals when using the system?
- What is their technical proficiency level?
- What devices/platforms do they use?
- How many users in this group? (scale)

**What to Document:**
- User personas with goals and pain points
- Stakeholder matrix (decision-makers, influencers, operators)
- Scale estimates per user group

---

### 1.4 Timeline & Constraints

**CRITICAL: Ask about constraints FIRST, before diving into requirements.**

**Core Questions:**
- What is the desired timeline?
- Is there a hard deadline? If so, why?
- Are there phases or milestones?
- What is the budget (hard cap or flexible)?
- Are there fixed constraints?

**Constraint Categories to Explore:**

**Platform & Infrastructure:**
- Must use specific cloud provider (Azure, AWS, GCP)?
- Any platform mandates or restrictions?
- Region restrictions for infrastructure?

**Compliance & Data Sovereignty:**
- What compliance standards must we meet (GDPR, HIPAA, SOC 2, ISO 27001, PCI-DSS, CPS 234)?
- Are there data sovereignty requirements (must data stay in EU/Australia/specific region)?
- Any restrictions on cross-border data transfers?
- Required security certifications?

**Development Infrastructure:**
- Which source control system (GitHub Enterprise, GitLab, Azure DevOps)?
- Which organization/repo structure?
- Where should documentation be stored (repo, Confluence, SharePoint, wiki)?
- CI/CD requirements or constraints?

**Architecture & Technology:**
- Any architecture principles (e.g., "Reuse over Buy over Build")?
- Approved/banned technologies (languages, frameworks, databases)?
- Must integrate with specific systems (SSO provider, monitoring, etc.)?
- Technology standards (specific versions, libraries)?

**Organizational:**
- Required process involvement (security review, architecture review)?
- Team size fixed or flexible?
- Hiring constraints?
- Required tooling (monitoring, logging, incident management)?

**Probing Questions:**
- What happens if we don't meet the deadline?
- Can scope be adjusted to meet timeline?
- Are there dependencies on other projects or teams?
- Which constraints are absolute vs flexible?
- Is there an exception process for any constraints?

**What to Document:**
- Timeline with phases
- Critical milestones and why they matter
- **Non-negotiable constraints** (capture in constraints document immediately)
- **Flexible preferences** (can be challenged)
- Dependencies
- Exception processes (if any)

---

## Phase 2: Functional Requirements

### 2.1 User Journeys

**Core Questions:**
- Walk me through how a user will accomplish [primary goal]
- What are the steps from start to finish?
- What decisions do they need to make along the way?
- What information do they need at each step?

**For Each Journey:**
1. Trigger: What causes the user to start this journey?
2. Steps: What actions do they take?
3. Decisions: What choices do they make?
4. Success: How does this journey end?
5. Failure: What can go wrong?

**Probing Questions:**
- Are there alternative paths for this journey?
- What happens if the user makes a mistake?
- Can they save progress and come back later?

**What to Document:**
- User journey maps (step-by-step flows)
- Decision points
- Error cases and recovery
- Data inputs and outputs at each step

---

### 2.2 Feature Requirements

**Core Questions:**
- What are the must-have features for the MVP?
- What features are important but can come later?
- What features are nice-to-have but low priority?

**For Each Feature:**
- What does this feature do?
- Who needs this feature and why?
- How will it be used (frequency, context)?
- What are the acceptance criteria (how do we know it's working)?

**Probing Questions:**
- What happens if we don't include this feature?
- Can this feature be simplified or split into smaller pieces?
- Are there examples of this feature in other systems?

**What to Document:**
- Feature list with MoSCoW prioritization (Must have, Should have, Could have, Won't have)
- Feature descriptions with user stories
- Acceptance criteria per feature
- Dependencies between features

---

### 2.3 Data Requirements

**Core Questions:**
- What data does the system need to store?
- Where does this data come from?
- Who creates/updates this data?
- How long should data be retained?
- Are there privacy or compliance requirements?

**For Each Data Entity:**
- What is it? (users, products, orders, etc.)
- What attributes does it have?
- What is the expected volume? (number of records, growth rate)
- Who can access it?
- Are there relationships to other entities?

**Probing Questions:**
- Is this data sensitive (PII, financial, health)?
- Does this data come from external sources?
- Do we need to sync this data with other systems?
- How often does this data change?

**What to Document:**
- Data entities and attributes
- Data sources (internal, external)
- Data volume and growth estimates
- Privacy/compliance requirements
- Data relationships (ERD if complex)

---

### 2.4 Integration Requirements

**Core Questions:**
- What existing systems must this integrate with?
- What data needs to flow between systems?
- Are there APIs available or do we need custom connectors?
- What is the integration pattern (real-time, batch, event-driven)?

**For Each Integration:**
- System name and purpose
- Data to send/receive
- Frequency (real-time, hourly, daily)
- Authentication method
- Error handling (what happens if integration fails)
- SLA (is there guaranteed uptime?)

**Probing Questions:**
- Who owns the external system?
- Can we get documentation and test credentials?
- Are there rate limits or quotas?
- What is the fallback if this system is unavailable?

**What to Document:**
- Integration inventory (system, purpose, pattern)
- Data mappings
- Authentication and credentials
- Error handling strategy
- SLA requirements

---

## Phase 3: Non-Functional Requirements

### 3.1 Performance

**Core Questions:**
- How fast must the system respond? (API latency, page load time)
- How many concurrent users must it support?
- What is the expected data volume?
- Are there peak usage times?

**Probing Questions:**
- What is acceptable performance? What would be unacceptable?
- How does performance impact user experience or business outcomes?
- Are there specific operations that must be fast?

**What to Document:**
- Latency targets (P50, P95, P99)
- Throughput requirements (requests/sec, transactions/hour)
- Data volume (current, 1-year, 3-year projections)
- Peak vs average load

---

### 3.2 Security

**Core Questions:**
- Who can access this system?
- How do users authenticate (SSO, username/password, MFA)?
- What permissions/roles are needed?
- Is there sensitive data to protect?
- Are there compliance requirements (GDPR, HIPAA, SOC 2)?

**Probing Questions:**
- What happens if someone unauthorized accesses data?
- Do we need audit logging (who did what when)?
- How are secrets (passwords, API keys) managed?
- Are there penetration testing requirements?

**What to Document:**
- Authentication method
- Authorization model (RBAC, ABAC)
- Data classification (public, internal, confidential)
- Compliance requirements
- Security testing requirements

---

### 3.3 Scalability

**Core Questions:**
- How many users today? In 1 year? In 3 years?
- How much data today? Expected growth?
- Are there seasonal or event-driven spikes?
- What is the maximum scale we need to support?

**Probing Questions:**
- What happens if we exceed capacity?
- Can we scale horizontally (add more servers)?
- Are there parts of the system that will be bottlenecks?

**What to Document:**
- Current scale (users, data, traffic)
- Growth projections (conservative and aggressive)
- Scaling strategy (horizontal, vertical, hybrid)
- Capacity planning approach

---

### 3.4 Availability & Reliability

**Core Questions:**
- How critical is this system? (can it go down?)
- What is the acceptable uptime? (99%, 99.9%, 99.99%?)
- What is the maximum acceptable downtime? (minutes, hours, days?)
- How much data loss is acceptable if something fails? (RPO)
- How quickly must the system recover? (RTO)

**Probing Questions:**
- What is the business impact of downtime?
- Are there maintenance windows?
- Do we need redundancy or failover?
- What are the failure scenarios to plan for?

**What to Document:**
- Uptime target (SLA)
- RTO (Recovery Time Objective)
- RPO (Recovery Point Objective)
- Failure scenarios and mitigation
- Backup and disaster recovery strategy

---

### 3.5 Operational

**Core Questions:**
- Who will operate and maintain this system?
- What operational tools are already in use (monitoring, logging, alerting)?
- Are there runbook requirements?
- What is the deployment frequency?
- Are there support requirements (24/7, business hours)?

**Probing Questions:**
- How will operators know if something is wrong?
- What common operational tasks will be needed?
- Are there cost constraints or budgets?
- How do we handle incidents?

**What to Document:**
- Operations team and responsibilities
- Monitoring and alerting requirements
- Deployment strategy (CI/CD, manual, scheduled)
- Support model and SLA
- Cost budget and tracking

---

## Phase 4: Technical Context

### 4.1 Existing Infrastructure

**Core Questions:**
- What infrastructure is already in place? (cloud provider, on-prem, hybrid)
- What technologies are standardized? (languages, frameworks, databases)
- What tooling is in use? (CI/CD, monitoring, logging)
- Are there architectural patterns or standards?

**Probing Questions:**
- Can we use existing infrastructure or do we need new?
- Are there technology constraints (must use X, cannot use Y)?
- Who manages the infrastructure?
- Are there cost considerations?

**What to Document:**
- Infrastructure inventory (cloud services, servers, databases)
- Technology stack (languages, frameworks, tools)
- Architectural standards and patterns
- Access and permissions

---

### 4.2 Technical Constraints

**Core Questions:**
- Are there technology restrictions? (approved list, banned list)
- Are there architectural constraints? (must be microservices, must be serverless)
- Are there existing systems we must reuse?
- Are there licensing or cost constraints?

**Probing Questions:**
- Why do these constraints exist?
- Are they hard constraints or preferences?
- What is the impact if we need an exception?

**What to Document:**
- Hard constraints (non-negotiable)
- Soft constraints (preferences)
- Rationale for each constraint
- Process for exceptions

---

### 4.3 Team & Skills

**Core Questions:**
- Who will build this system?
- What skills does the team have?
- Are there skill gaps to address?
- Is training needed?

**Probing Questions:**
- Is this an internal team or external partner?
- What is the team size?
- What is their experience level?
- Are there offshore/distributed team considerations?

**What to Document:**
- Team composition (roles, count)
- Skill inventory
- Skill gaps and training plan
- Working model (onshore, offshore, hybrid)

---

## Phase 5: Scope & Priorities

### 5.1 MVP Definition

**Core Questions:**
- What is the smallest version that delivers value?
- What features are absolute must-haves for launch?
- What can be deferred to later phases?
- What is explicitly out of scope?

**Probing Questions:**
- Can we launch with less and iterate?
- What would make this a "beta" vs "production" launch?
- Are there features we can simplify?

**What to Document:**
- MVP scope (in-scope features)
- Phase 2+ scope (deferred features)
- Explicitly out of scope (what we won't do)
- MVP success criteria

---

### 5.2 Phasing Strategy

**Core Questions:**
- Are there logical phases or milestones?
- What should be built first? Second?
- Are there dependencies that dictate order?
- Are there external forcing functions (deadlines, events)?

**Probing Questions:**
- Can phases be delivered independently?
- What is the value of each phase?
- Can we get user feedback between phases?

**What to Document:**
- Phase definitions with scope
- Timeline per phase
- Dependencies between phases
- Value delivered per phase

---

### 5.3 Risk Assessment

**Core Questions:**
- What are the biggest risks to this project?
- What could cause the project to fail?
- What are we most uncertain about?
- What assumptions are we making?

**For Each Risk:**
- Description
- Likelihood (high, medium, low)
- Impact (high, medium, low)
- Mitigation strategy
- Owner

**What to Document:**
- Risk register with mitigations
- Assumptions that need validation
- Unknowns that need research

---

## Tips for Effective Requirements Gathering

### 1. Progressive Questioning
- Start broad, then drill down
- Don't ask all questions in one session
- Adapt questions based on answers
- Follow interesting threads

### 2. Use Examples
- Ask for specific examples or scenarios
- Request to see existing systems or workarounds
- Use "show me" rather than "tell me"

### 3. Paraphrase and Confirm
- Restate requirements in your own words
- Confirm understanding before moving on
- Document and share notes for validation

### 4. Explore the "Why"
- Ask "why" multiple times to get to root causes
- Understand the motivation behind each requirement
- Challenge assumptions respectfully

### 5. Identify Gaps
- Look for missing user groups
- Find unmentioned failure scenarios
- Identify integration points not discussed
- Spot security or compliance oversights

### 6. Use Collaborative Tools
- AskUserQuestion tool for key decisions
- Sketching/diagramming (describe what you'd draw)
- Reviewing existing code/documentation

### 7. Prioritize Ruthlessly
- Use MoSCoW (Must, Should, Could, Won't)
- Validate priorities against goals
- Challenge "must haves" that aren't critical

### 8. Document Assumptions
- Explicitly state what you're assuming
- Get confirmation on assumptions
- Track which assumptions need validation

---

## Output Format

After gathering requirements, structure them into sections:

### 1. Executive Summary
- Problem statement
- Solution vision
- Key benefits
- Success metrics

### 2. Users & Stakeholders
- User personas
- Stakeholder map
- Scale estimates

### 3. Functional Requirements
- Feature list with priorities
- User stories and acceptance criteria
- Data requirements
- Integration requirements

### 4. Non-Functional Requirements
- Performance targets
- Security requirements
- Scalability requirements
- Availability/reliability targets
- Operational requirements

### 5. Technical Context
- Existing infrastructure
- Technology constraints
- Team and skills

### 6. Scope & Phasing
- MVP definition
- Phased delivery plan
- Out of scope

### 7. Risks & Assumptions
- Risk register
- Assumptions requiring validation
- Unknowns requiring research

---

## Transitioning to Documentation

Once requirements are gathered, use them to create:

1. **Product Overview**: Focus on the "why" and high-level "how"
   - Problem statement → Section 1-2 of product overview
   - Solution vision → Section 3-4
   - Benefits → Section 5
   - Phasing → Section 8

2. **Detailed Requirements**: All functional and non-functional requirements
   - Project context → Section 1
   - Technical architecture → Section 2
   - Functional requirements → Section 3-4
   - Non-functional requirements → Section 6
   - Technical decisions → Section 7

3. **Architecture & System Design**: Technical blueprint
   - Component design → Section 3
   - Data architecture → Section 4
   - API design → Section 5
   - Security architecture → Section 6
   - Observability → Section 8
