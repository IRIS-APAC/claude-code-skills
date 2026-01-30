# Story Decomposition Guide

This guide helps break down requirements into epics and user stories that teams can estimate and implement.

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

## Step 1: Identify Epics

Epics are large bodies of work that can be broken down into stories. They typically represent major features or capabilities.

### Epic Naming Convention
```
[Category]: [Capability Name]

Examples:
Infrastructure: Development Environment Setup
Core Feature: User Authentication and Authorization
Integration: SharePoint Data Ingestion
Operational: Monitoring and Alerting
```

### Epic Template

**Epic Name**: [Category]: [Capability Name]

**Epic Goal**: [1-2 sentences describing what business value this delivers]

**User Personas**: [Who benefits from this epic]

**Priority**: [Must Have / Should Have / Could Have / Won't Have (this phase)]

**Success Criteria**:
- [How we know this epic is complete]
- [Measurable outcomes]

**Stories**: [Number] stories (enumerated below)

**Estimated Effort**: [Sum of story points or hours]

**Dependencies**: [Other epics that must be complete first]

**Risks**: [Key risks or unknowns]

---

### Example Epic

**Epic Name**: Infrastructure: Core Search Infrastructure

**Epic Goal**: Establish the foundational search capabilities using OpenSearch Serverless with hybrid search (BM25 + vector) to enable intelligent document retrieval.

**User Personas**:
- Developers (need search capability to build features)
- End Users (will benefit from accurate search results)

**Priority**: Must Have (Phase 2a)

**Success Criteria**:
- OpenSearch Serverless cluster deployed and configured
- Hybrid search pipeline implemented (BM25 + vector)
- Can index sample documents and retrieve them via search API
- Performance meets targets (< 500ms P95 latency)

**Stories**: 8 stories

**Estimated Effort**: 21 story points

**Dependencies**:
- Epic 0: Development Environment (must be complete)

**Risks**:
- OpenSearch Serverless constraints may require architectural changes
- Embedding model performance needs validation

---

## Step 2: Decompose Epics into Stories

### Story Naming Convention
```
[Epic #].[Story #]: [User-focused action]

Examples:
1.1: Create OpenSearch Serverless cluster
1.2: Implement embedding generation service
1.3: Build hybrid search query handler
```

### Story Template

**Story ID**: [Epic #].[Story #]

**Story Title**: [User-focused description]

**As a** [user role]
**I want to** [action]
**So that** [benefit]

**Priority**: [Must / Should / Could / Won't]

**Acceptance Criteria**:
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Technical Notes**:
- [Implementation approach]
- [Key technologies or patterns]
- [Gotchas or considerations]

**Definition of Done**:
- [ ] Code complete and peer reviewed
- [ ] Unit tests written (>80% coverage for new code)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to dev/staging environment
- [ ] Acceptance criteria verified

**Estimated Effort**: [Story points or hours]

**Dependencies**: [Story IDs that must be complete first]

**Assignee**: [Name or TBD]

**Sprint**: [Sprint number or TBD]

---

### Example Story

**Story ID**: 1.2

**Story Title**: Implement embedding generation service

**As a** search developer
**I want to** generate embeddings for documents and queries
**So that** I can perform vector similarity search

**Priority**: Must Have

**Acceptance Criteria**:
- [ ] Can generate 1024-dimensional embeddings via AWS Bedrock (Titan or Cohere)
- [ ] Service supports both document embedding and query embedding modes
- [ ] Batch embedding (up to 100 docs at once) works correctly
- [ ] Retries with exponential backoff on transient failures
- [ ] Embedding model version is logged for reproducibility
- [ ] Cache embeddings for frequently queried terms (TTL: 5 minutes)
- [ ] Latency < 500ms for single embedding, < 2s for batch of 100

**Technical Notes**:
- Use AWS Bedrock with Titan Embeddings V2 model
- Implement in `core/embeddings/` module
- Batching strategy: collect documents, call Bedrock batch API, distribute results
- Cache implementation: Redis with key pattern `emb:v1:sha256(text)`
- Add CloudWatch metrics: EmbeddingLatency, EmbeddingErrors, CacheHitRate

**Definition of Done**:
- [ ] Code complete and peer reviewed
- [ ] Unit tests for embedding logic (mock Bedrock)
- [ ] Integration test with real Bedrock API (dev account)
- [ ] Module documentation with usage examples
- [ ] Deployed to dev environment
- [ ] Validated with sample documents

**Estimated Effort**: 5 story points

**Dependencies**:
- Story 0.3: AWS infrastructure setup (Bedrock access, IAM roles)

**Assignee**: TBD

**Sprint**: Sprint 2

---

## Step 3: Estimation

### Story Point Scale (Fibonacci)

**1 point**:
- Very simple, well-understood task
- Few hours of work
- No unknowns
- Example: Add a new endpoint that reads from existing database table

**2 points**:
- Simple task with minor complexity
- Half a day of work
- Well understood with few unknowns
- Example: Add validation to an existing form field

**3 points**:
- Moderate complexity
- 1 day of work
- Some unknowns but generally understood
- Example: Implement a new database table with CRUD operations

**5 points**:
- Complex task
- 2-3 days of work
- Requires investigation or learning
- Example: Integrate with a new third-party API

**8 points**:
- Very complex task
- 3-5 days of work
- Significant unknowns
- Consider breaking down if possible
- Example: Implement end-to-end authentication flow

**13 points**:
- Extremely complex or poorly understood
- > 5 days of work
- **Should be broken down into smaller stories**
- Use this temporarily if decomposition isn't clear yet

**21+ points**:
- This is an epic, not a story
- **Must be broken down**

### Estimation Considerations

**Add Complexity For**:
- New technologies or patterns
- Integration with external systems
- Unclear requirements
- Tight coupling to many other components
- Performance optimization needed
- Security or compliance requirements

**Remove Complexity For**:
- Repeated patterns (already done similar work)
- Well-documented libraries or frameworks
- Clear requirements and acceptance criteria
- Isolated changes (minimal dependencies)

### Velocity Planning

**Team Velocity**: [Total story points completed per sprint]

**Sprint Capacity**: [Team velocity × sprint duration / 2 weeks]

**Buffer**: Plan for 70-80% of capacity to account for meetings, support, unknowns

**Example**:
- Team velocity: 40 points per 2-week sprint
- Sprint capacity: 40 points
- Planned work: 30 points (75% of capacity)
- Buffer: 10 points for support, bugs, unknowns

---

## Step 4: Sequencing and Dependencies

### Dependency Types

**1. Hard Technical Dependency**
- Story B cannot start until Story A is complete
- Example: Can't implement search API until OpenSearch cluster exists
- Document explicitly: "Depends on Story 1.1"

**2. Soft Technical Dependency**
- Story B is easier if Story A is done first
- Example: Integration tests easier if unit tests exist
- Document: "Recommended after Story 1.2"

**3. Knowledge Dependency**
- Story B benefits from learnings from Story A
- Example: Second integration easier after first one
- Document: "Builds on patterns from Story 2.1"

**4. Resource Dependency**
- Stories require same person/skill
- Example: Both stories need security architect review
- Document: "Requires security review (same as Story 3.5)"

### Visualizing Dependencies

```
Epic 1: Search Infrastructure
  Story 1.1: Create OpenSearch cluster
    ↓ (hard dependency)
  Story 1.2: Implement embedding service
    ↓ (hard dependency)
  Story 1.3: Build hybrid search query
    ↓ (hard dependency)
  Story 1.4: Implement search API endpoint

Epic 2: SharePoint Integration
  Story 2.1: SharePoint API client
    ↓ (hard dependency)
  Story 2.2: HTML parser
    ↓ (soft dependency)
  Story 2.3: Caption generation
    ↓ (hard dependencies: 1.2, 2.2)
  Story 2.4: Indexing pipeline
```

---

## Step 5: Story Refinement

### Red Flags (Story Needs Refinement)

**🚩 Story is too vague**
- Acceptance criteria are not specific
- "Implement feature X" without details
- **Fix**: Add specific acceptance criteria, break down into smaller pieces

**🚩 Story has too many acceptance criteria**
- More than 7-8 criteria
- Criteria cover multiple concerns
- **Fix**: Split into multiple stories, group related criteria

**🚩 Story has unclear scope**
- "And anything else needed"
- "Complete feature X"
- **Fix**: Define exact scope, move unknowns to separate investigation story

**🚩 Story has "should" or "might"**
- "Should handle edge case Y"
- "Might need to support Z"
- **Fix**: Make requirements explicit (in scope or out of scope)

**🚩 Story is horizontal (technical layer only)**
- "Build database schema"
- "Create API endpoints (no implementation)"
- **Fix**: Combine into vertical slices that deliver value

**🚩 Story has blocking unknowns**
- "Not sure if API supports this"
- "Need to investigate approach"
- **Fix**: Create spike story to resolve unknowns first

### Story Types

**1. Feature Story**
- Delivers user-facing value
- Most common type
- Example: "Implement search with filters"

**2. Technical Story**
- Enables other features
- Infrastructure, refactoring, tech debt
- Example: "Set up CI/CD pipeline"

**3. Spike Story**
- Investigation or proof of concept
- Time-boxed (usually 1-2 days)
- Deliverable is knowledge, not code
- Example: "Investigate OpenSearch performance characteristics"

**4. Bug Fix Story**
- Fixes a defect
- Include how to reproduce
- Example: "Fix search returning stale results"

**5. Documentation Story**
- Creates or updates documentation
- Example: "Write API usage guide for search service"

---

## Epic and Story Catalog Template

Use this structure to organize all epics and stories:

```markdown
# Epic and Story Catalog

## Epic 0: [Foundation]
- **Goal**: [What it delivers]
- **Priority**: Must Have
- **Estimated Effort**: [X] points

### Stories

#### 0.1: [Story Title]
- **Estimate**: [X] points
- **Dependencies**: None
- **Summary**: [One-line description]

#### 0.2: [Story Title]
- **Estimate**: [X] points
- **Dependencies**: 0.1
- **Summary**: [One-line description]

[... continue for all stories ...]

---

## Epic 1: [Core Feature]
- **Goal**: [What it delivers]
- **Priority**: Must Have
- **Estimated Effort**: [X] points

[... continue for all epics ...]

---

## Summary

**Total Epics**: [Number]
**Total Stories**: [Number]
**Total Estimated Effort**: [Number] points

**Phase 1 (MVP)**: [X] stories, [Y] points
**Phase 2**: [X] stories, [Y] points
**Phase 3**: [X] stories, [Y] points

**Critical Path**: Epic 0 → Epic 1 → Epic 5

**Sprint Plan** (assuming [X] points per sprint):
- Sprint 1: Stories [list]
- Sprint 2: Stories [list]
- Sprint 3: Stories [list]
```

---

## Best Practices

### 1. Involve the Whole Team
- Developers estimate stories (they do the work)
- Product owner prioritizes
- Architect validates technical approach
- QA reviews acceptance criteria

### 2. Estimate Relatively
- Compare stories to each other
- "This is twice as complex as story X"
- Use reference stories (known effort)

### 3. Break Down Uncertainty
- Spike stories for unknowns
- Prototype for proof of concept
- Iterate on story definition

### 4. Keep Stories Fresh
- Refine stories 1-2 sprints ahead
- Update estimates as you learn
- Adjust scope based on velocity

### 5. Track and Learn
- Record actual effort vs estimate
- Identify patterns (what's underestimated?)
- Adjust estimation approach

---

## Transitioning from Requirements to Stories

### From Requirements Document

**Section 3: Functional Requirements** → **Epics**
- Each requirement area becomes an epic
- Example: "Epic 1: Core Search Infrastructure" from "Requirement 3.1"

**User Stories in Requirements** → **Stories**
- Already written as stories
- Add technical notes and estimate

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

**Section 8: Observability** → **Technical Stories**
- Logging, metrics, tracing implementation stories

---

## Tools and Templates

### Story Tracking

**Option 1: Markdown in Git** (lightweight)
```markdown
# Sprint 3 Stories

## In Progress
- [ ] 1.2: Implement embedding service (Alice, 3 days in)

## To Do
- [ ] 1.3: Build hybrid search query (Bob, blocked on 1.2)
- [ ] 2.1: SharePoint API client (Charlie)

## Done
- [x] 1.1: Create OpenSearch cluster (Alice, completed 2025-01-25)
```

**Option 2: Issue Tracker** (Jira, GitHub Issues, Linear)
- Use labels for epic, priority, status
- Use issue links for dependencies
- Track story points in custom fields

**Option 3: Project Board** (GitHub Projects, Trello)
- Columns: Backlog, Ready, In Progress, Review, Done
- Cards for each story
- Swimlanes for epics

### Story Template (Markdown)

```markdown
## Story [Epic].[Number]: [Title]

**As a** [role]
**I want to** [action]
**So that** [benefit]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Technical Notes
- [Approach]
- [Key considerations]

### Definition of Done
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Docs updated
- [ ] Deployed to staging

**Estimate**: [X] points
**Dependencies**: [Story IDs]
**Assignee**: [Name]
**Sprint**: [Number]
```

---

## Summary

Effective story decomposition:
1. **Starts with clear epics** that represent major capabilities
2. **Breaks epics into right-sized stories** (1-5 days each)
3. **Makes stories vertical** (end-to-end value)
4. **Defines clear acceptance criteria** (testable)
5. **Estimates relatively** using story points
6. **Documents dependencies** explicitly
7. **Refines continuously** as you learn more

The goal is to create a backlog that the team can confidently estimate, prioritize, and execute.
