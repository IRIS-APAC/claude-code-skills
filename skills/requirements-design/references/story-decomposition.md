# Story Decomposition Guide

This guide helps break down **requirements documents into epics and user stories** during the requirements phase.

**For ongoing story management** (templates, estimation, sprint planning), use the `/project-management` skill.

---

## Purpose and Scope

**This guide covers:**
- ✅ Identifying epics from requirements documents
- ✅ Breaking requirements into initial story backlog
- ✅ Mapping requirements sections to epics/stories
- ✅ Creating epic catalog structure
- ✅ Handoff to project-management skill

**This guide does NOT cover** (use `/project-management` instead):
- ❌ Detailed story templates → See project-management skill
- ❌ Estimation (story points/T-shirt sizing) → See project-management skill
- ❌ Sprint planning → See project-management skill
- ❌ Ongoing story refinement → See project-management skill
- ❌ Creating stories on boards (ZenHub/Jira) → See agile-board skill

---

## Principles of Good Decomposition

### 1. Right-Sized Stories
- **Too Big**: Story takes more than 1 sprint → break it down
- **Too Small**: Story adds no meaningful value → combine with others
- **Just Right**: Can be completed in 1-5 days by one developer (or pair)

### 2. Vertical Slicing
- Each story should deliver end-to-end value
- Include frontend, backend, database, tests
- Avoid "horizontal" stories (just build the database layer)

### 3. Independence
- Stories should be as independent as possible
- Minimize dependencies between stories in the same sprint
- Document dependencies clearly when they exist

### 4. Testable
- Every story should have clear acceptance criteria
- Criteria should be verifiable (yes/no, pass/fail)
- Include both happy path and error cases

### 5. Valuable
- Each story should deliver something a user cares about
- Technical stories should enable user value
- Infrastructure stories should be framed in terms of enabling capabilities

---

## Step 1: Identify Epics from Requirements

Epics are large bodies of work that can be broken down into stories. They typically represent major features or capabilities.

### Mapping Requirements to Epics

**From Requirements Document** → **Epics**

| Requirements Section | Epic Category | Example |
|---------------------|---------------|---------|
| Section 3: Functional Requirements | Core Feature Epics | Epic 1: User Authentication |
| Section 3.1-3.5: Feature areas | One epic per major feature | Epic 2: Document Search |
| Section 6: Non-Functional Requirements | Technical/Infrastructure Epics | Epic 0: Development Environment |
| Section 8: Dependencies & Integrations | Integration Epics | Epic 3: SharePoint Integration |

**From Architecture Document** → **Technical Epics**

| Architecture Section | Epic Category | Example |
|---------------------|---------------|---------|
| Section 3: Internal Modules | Technical Epics | Epic 4: Core Authentication Module |
| Section 5: API Design | API/Feature Epics | Epic 5: Search API Endpoints |
| Section 8: Observability | Operational Epics | Epic 6: Monitoring & Alerting |

### Epic Naming Convention

```
[Category]: [Capability Name]

Examples:
- Infrastructure: Development Environment Setup
- Core Feature: User Authentication and Authorization
- Integration: SharePoint Data Ingestion
- Operational: Monitoring and Alerting
```

### Epic Structure (Minimal)

**Epic Name**: [Category]: [Capability Name]

**Epic Goal**: [1-2 sentences describing what business value this delivers]

**Priority**: [Must Have / Should Have / Could Have / Won't Have (this phase)]

**Stories**: [Will be broken down using `/project-management` skill]

**Dependencies**: [Other epics that must be complete first]

---

## Step 2: Break Epics into Initial Stories

**At this stage**, create a high-level story list for each epic. Detailed story templates, acceptance criteria, and estimation come later with `/project-management`.

### Story Naming Convention

```
[Epic #].[Story #]: [User-focused action]

Examples:
1.1: Create OpenSearch Serverless cluster
1.2: Implement embedding generation service
1.3: Build hybrid search query handler
```

### Minimal Story Structure (Requirements Phase)

**Story ID**: [Epic #].[Story #]

**Story Title**: [User-focused description]

**As a** [user role]
**I want to** [action]
**So that** [benefit]

**Scope** (high-level):
- What this story includes
- What it depends on

**Handoff to `/project-management`**:
- Story will be refined with detailed acceptance criteria
- Story will be estimated using T-shirt sizing (XS/S/M/L/XL)
- Story will be created on board with `/agile-board`

---

## Step 3: Create Epic Catalog

Use this structure to organize all epics and stories from requirements:

```markdown
# Epic and Story Catalog: [Project Name]

**Source**: Generated from requirements documents in `docs/Design/`

**Status**: Initial decomposition from requirements phase

**Next Steps**:
- Refine stories with `/project-management` (templates, acceptance criteria, estimation)
- Create stories on board with `/agile-board`
- Plan sprints with `/project-management`

---

## Epic 0: [Foundation/Infrastructure]

**Goal**: [What it delivers]

**Priority**: Must Have

**Requirements Source**: [Link to requirements section]

### Stories (High-Level)

#### 0.1: [Story Title]
- **Scope**: [Brief description]
- **Dependencies**: None

#### 0.2: [Story Title]
- **Scope**: [Brief description]
- **Dependencies**: 0.1

[Continue for all stories...]

---

## Epic 1: [Core Feature]

**Goal**: [What it delivers]

**Priority**: Must Have

**Requirements Source**: [Link to requirements section]

### Stories (High-Level)

[Same structure as Epic 0...]

---

## Summary

**Total Epics**: [Number]

**Total Stories** (high-level): [Number]

**Phase Breakdown**:
- Phase 1 (MVP): [X] epics, [Y] stories
- Phase 2: [X] epics, [Y] stories

**Critical Path**: Epic 0 → Epic 1 → Epic 5

**Next Steps**:
1. Use `/project-management` to refine stories with:
   - Detailed acceptance criteria
   - T-shirt sizing estimates (XS/S/M/L/XL)
   - Technical notes
   - Definition of Done
2. Use `/agile-board` to create stories on board (ZenHub/Jira/Linear)
3. Use `/project-management` for sprint planning
```

---

## Step 4: Transitioning from Requirements to Stories

### From Requirements Document

**Section 3: Functional Requirements** → **Epics**
- Each requirement area becomes an epic
- Example: "Epic 1: Core Search Infrastructure" from "Requirement 3.1: Search Capabilities"

**User Stories in Requirements** → **Stories**
- Already written as stories in requirements doc
- Copy to epic catalog with epic numbering
- Refine later with `/project-management`

**Non-Functional Requirements** → **Technical Stories**
- Performance requirements → Performance optimization stories
- Security requirements → Security implementation stories
- Operational requirements → Monitoring/observability stories

### From Architecture Document

**Section 3: Internal Modules** → **Technical Stories**
- Each module to be built becomes stories
- Example: "Implement core/auth module" → Multiple stories for different aspects

**Section 5: API Design** → **Feature Stories**
- Each endpoint becomes a story or set of stories
- Example: "POST /api/search" → Story: "Implement search API endpoint"

**Section 8: Observability** → **Operational Stories**
- Logging, metrics, tracing implementation stories
- Example: "Story: Configure CloudWatch dashboards"

---

## Dependency Tracking

### Dependency Types

**1. Hard Technical Dependency**
- Story B cannot start until Story A is complete
- Example: Can't implement search API until OpenSearch cluster exists
- Document: "Depends on Story 1.1"

**2. Epic-Level Dependency**
- Epic B requires Epic A to be complete
- Example: Integration epic requires infrastructure epic
- Document in epic catalog: "Dependencies: Epic 0 (Foundation)"

### Visualizing Dependencies

```
Epic 0: Foundation
  Story 0.1: AWS account setup
    ↓ (hard dependency)
  Story 0.2: CI/CD pipeline
    ↓ (hard dependency)
  Story 0.3: Development environment

Epic 1: Core Infrastructure
  [Depends on: Epic 0]
  Story 1.1: Create OpenSearch cluster
    ↓ (hard dependency)
  Story 1.2: Implement embedding service
    ↓ (hard dependency)
  Story 1.3: Build search query handler

Epic 2: Integrations
  [Depends on: Epic 1]
  Story 2.1: SharePoint API client
    ↓
  Story 2.2: Indexing pipeline
```

---

## Red Flags During Initial Decomposition

**🚩 Epic is too vague**
- "Implement the system" → Break down by functional areas
- **Fix**: Review requirements sections, create one epic per major capability

**🚩 Story is too high-level**
- "Build authentication" → This is an epic, not a story
- **Fix**: Break into smaller stories (login, logout, session management, password reset)

**🚩 Too many stories for one epic**
- More than 15-20 stories per epic
- **Fix**: Consider splitting epic into sub-epics or combining small stories

**🚩 Horizontal slicing**
- "Build all database schemas" → Not delivering user value
- **Fix**: Slice vertically (each story includes DB + API + UI for one feature)

**🚩 Missing infrastructure stories**
- Jumping straight to features without Epic 0 (Foundation)
- **Fix**: Add Epic 0 with environment setup, CI/CD, basic infrastructure

---

## Handoff to Project Management

**Once you've created the epic catalog**, use `/project-management` to:

### 1. Refine Each Story
- Add detailed acceptance criteria (checkbox format)
- Add technical notes and implementation approach
- Add Definition of Done checklist
- Estimate complexity using T-shirt sizing (XS/S/M/L/XL)

**Example handoff**:
```
Use /project-management to refine the stories in Epic 1:
- Stories 1.1 through 1.8 need acceptance criteria
- Estimate complexity using T-shirt sizing
- Add technical notes for implementation
```

### 2. Create Stories on Board
Use `/agile-board` to create the stories on your project board:
- ZenHub, Jira, Linear, or other board
- Set priority, assignee, sprint

### 3. Plan Sprints
Use `/project-management` to:
- Calculate team velocity
- Plan sprint capacity
- Select stories for sprint
- Sequence work based on dependencies

---

## Example: Complete Epic Decomposition

**From Requirements**: Section 3.2: "Search Capabilities" (Requirements doc)

### Epic 1: Core Search Infrastructure

**Epic Goal**: Establish foundational search capabilities using OpenSearch with hybrid search (BM25 + vector) to enable intelligent document retrieval.

**User Personas**:
- Developers (need search capability to build features)
- End Users (will benefit from accurate search results)

**Priority**: Must Have (Phase 1)

**Requirements Source**: Section 3.2 in `requirements-document-search.md`

**Dependencies**: Epic 0 (Development Environment)

**Stories** (High-Level):

#### 1.1: Create OpenSearch Serverless cluster
- **Scope**: Provision OpenSearch cluster, configure networking, set up basic access
- **Dependencies**: Story 0.3 (AWS infrastructure setup)

#### 1.2: Implement embedding generation service
- **Scope**: AWS Bedrock integration for generating document embeddings
- **Dependencies**: Story 1.1

#### 1.3: Build hybrid search query handler
- **Scope**: Combine BM25 keyword search with vector similarity search
- **Dependencies**: Story 1.2

#### 1.4: Create document indexing pipeline
- **Scope**: Pipeline to ingest documents and create search indices
- **Dependencies**: Story 1.2

#### 1.5: Implement search API endpoint
- **Scope**: REST API endpoint for search queries
- **Dependencies**: Story 1.3, Story 1.4

**Total Stories**: 5 (high-level, will be refined by `/project-management`)

**Next Steps**:
```
Use /project-management to:
1. Refine stories 1.1-1.5 with detailed acceptance criteria
2. Estimate each story using T-shirt sizing
3. Identify which stories can be done in Sprint 1

Use /agile-board to:
1. Create these stories on ZenHub board
2. Assign to team members
3. Add to appropriate sprint
```

---

## Best Practices

### 1. Start with Requirements Documents
- Epic catalog should map cleanly to requirements sections
- Every epic should trace back to a requirement
- Every story should deliver something from requirements

### 2. Keep Initial Stories High-Level
- At requirements phase, focus on WHAT stories are needed
- Let `/project-management` handle HOW (acceptance criteria, estimation)
- Avoid premature detail

### 3. Document Dependencies Clearly
- Epic-level dependencies in epic catalog
- Story-level dependencies in story descriptions
- Visualize critical path

### 4. Plan for Handoff
- Epic catalog is INPUT to `/project-management`
- Epic catalog is NOT final stories (those come from refinement)
- Think of this as the "story backlog blueprint"

### 5. Include Infrastructure
- Always start with Epic 0: Foundation/Infrastructure
- Don't skip operational stories (monitoring, logging)
- Remember non-functional requirements become stories too

---

## Integration with Other Skills

```
/requirements-design
↓ Creates epic catalog with story-decomposition.md
↓
/project-management
├─ Refines stories (acceptance criteria, estimation)
├─ Plans sprints
└─ Creates Definition of Done
↓
/agile-board
└─ Creates stories on board (ZenHub/Jira/Linear)
```

---

## Summary

**Story Decomposition (requirements phase)** is about:
1. Identifying epics from requirements/architecture documents
2. Creating high-level story list for each epic
3. Documenting dependencies and sequencing
4. Creating epic catalog structure
5. **Handing off to `/project-management`** for detailed refinement

**Remember**: This is INITIAL decomposition. Detailed story work (templates, acceptance criteria, estimation, sprint planning) happens with `/project-management` skill.
