# Epic Planning and Dependencies

Strategic planning for epics, releases, and cross-project coordination.

## Epic Planning Overview

**Epic planning** bridges the gap between high-level requirements and sprint-level execution.

**Time horizons**:
- **Sprint planning** - 2 weeks (tactical)
- **Epic planning** - 4-12 weeks (strategic)
- **Release planning** - 3-6 months (roadmap)

## Challenge Assumptions During Epic Planning

**CRITICAL**: Challenge assumptions throughout epic planning to avoid flawed plans.

**Why challenge at epic level**:
- Epics represent significant investment (weeks/months of work)
- Early mistakes cascade to all child stories
- Wrong epic scope wastes entire team's capacity
- Missed dependencies cause delays across multiple sprints
- Poor architecture decisions are expensive to fix later

**What to challenge in epic planning**:

**Vague epic scope**:
```
Epic: "Improve user experience"
Challenge: "Which user experience? What specific pain points? What's the success metric?
           Is this about performance, UI/UX, accessibility, or something else?
           Can we narrow this to a focused, measurable epic?"
```

**Unrealistic epic timeline**:
```
Epic: "Rebuild authentication system - 1 sprint"
Challenge: "This includes SSO, MFA, session management, password reset, and audit logging.
           Our velocity is 20 points/sprint. This epic has 45 points of stories.
           Should we plan for 2-3 sprints, or reduce scope?"
```

**Missing dependencies**:
```
Epic: "Implement new search service"
Challenge: "Does this depend on the OpenSearch infrastructure epic completing first?
           Do we need the data migration epic done before we can test this?
           Should we block this until those are complete?"
```

**Hidden complexity**:
```
Epic: "Add export functionality"
Challenge: "What formats (CSV, PDF, Excel)? How large are the exports (pagination needed)?
           Async processing for large datasets? Email notification when ready?
           This might be larger than one epic."
```

**Architecture assumptions**:
```
Epic: "Build microservices for user management"
Challenge: "Do we have the team to maintain microservices? What's the deployment complexity?
           Have we considered the distributed data problem? Would a modular monolith work?
           What's the actual scale requirement that drives this decision?"
```

**Under-estimated integration work**:
```
Epic: "Integrate with Entra ID - 2 stories"
Challenge: "Have we tested the Entra API? What about error handling, token refresh,
           group sync, permission mapping, audit logging? Should we create a POC first?
           This might be 5-6 stories, not 2."
```

**Missing non-functional requirements**:
```
Epic: "Build document processing pipeline"
Challenge: "What's the throughput requirement? Error handling for corrupt files?
           Retry logic? Monitoring and alerting? Security (virus scanning)?
           These might need additional stories."
```

**How to challenge effectively during epic planning**:
- ✅ Review similar past epics - what did we miss?
- ✅ Ask "what could go wrong?" for each story
- ✅ Challenge with historical velocity data
- ✅ Identify cross-epic dependencies early
- ✅ Suggest POC stories for uncertain integrations
- ✅ Question architecture decisions with trade-off analysis
- ✅ Validate timeline against team capacity
- ❌ Don't accept vague epic descriptions
- ❌ Don't ignore technical complexity
- ❌ Don't skip dependency analysis
- ❌ Don't plan without considering team velocity

**Epic challenge checklist**:
- [ ] Epic scope is focused and measurable
- [ ] All major dependencies identified
- [ ] Story estimates realistic based on complexity
- [ ] Timeline validated against team velocity
- [ ] Architecture decisions justified with trade-offs
- [ ] Non-functional requirements captured (performance, security, monitoring)
- [ ] Integration points validated (POC created if needed)
- [ ] Edge cases and error scenarios considered
- [ ] Cross-epic dependencies mapped
- [ ] Risk mitigation stories included

## Epic Breakdown Process

### 1. Review Epic Requirements

**Inputs**:
- Epic description and objectives
- Business requirements document
- Technical constraints
- Delivery timeline/deadline

**Questions to answer**:
- What user value does this epic deliver?
- What are the non-negotiable requirements?
- What are the nice-to-haves?
- What technical dependencies exist?
- Who are the stakeholders?

### 2. Identify Stories

**Story identification strategies**:

**User journey mapping**:
```
Epic: User Authentication System

User Journey:
1. Sign up → Story: User registration
2. Log in → Story: User login
3. Stay logged in → Story: Session management
4. Forgot password → Story: Password reset
5. Manage account → Story: Profile management
```

**Technical layering**:
```
Epic: Hybrid Search Service

Technical Layers:
1. Infrastructure → Story: OpenSearch setup
2. Data layer → Story: Index schema design
3. Service layer → Story: Search API implementation
4. Integration → Story: Query processing pipeline
```

**Feature decomposition**:
```
Epic: Document Processing Pipeline

Features:
1. PDF parsing → Story: PDF text extraction
2. OCR → Story: Scanned document OCR
3. Metadata extraction → Story: Metadata enrichment
4. Caption generation → Story: AI captions
```

### 3. Map Dependencies

Identify which stories must happen before others:

```
Story Dependencies:

Story 1.1: OpenSearch setup
  ↓
Story 1.2: Index schema (depends on 1.1)
  ↓
Story 1.3: Hybrid search (depends on 1.2)
  ↓
Story 1.4: API integration (depends on 1.3)
```

See "Story Dependencies" section below for detailed dependency management.

### 4. Estimate Stories

Use T-shirt sizing for all stories (see `estimation-guide.md`).

**Epic estimation**:
- Individual story estimates: S(3) + M(5) + M(5) + S(3) = 16 points
- Add buffer for unknowns: 16 × 1.2 = ~19 points
- Compare to team velocity (e.g., 20 points/sprint)
- Timeline: ~1 sprint + buffer = 1.5 sprints

### 5. Sequence Stories

**Sequencing strategies**:

**Critical path first**:
- Identify must-have stories for epic completion
- Schedule these first to de-risk timeline

**Vertical slicing**:
- Deliver end-to-end functionality incrementally
- Each sprint delivers working feature

**Dependency-driven**:
- Schedule stories based on dependencies
- Avoid blocking stories at sprint boundaries

### 6. Allocate to Sprints

**Example epic breakdown**:
```
Epic 1: Search Infrastructure (6 weeks, 3 sprints)

Sprint 1 (20 points):
  - Story 1.1: OpenSearch setup (M-5)
  - Story 1.2: Index schema (S-3)
  - Story 1.5: Basic auth (M-5)
  - Other work: Bug fixes (S-3)
  Buffer: 4 points

Sprint 2 (20 points):
  - Story 1.3: Hybrid search (M-5)
  - Story 1.4: Query processing (M-5)
  - Story 1.6: Error handling (S-3)
  Other work: Tech debt (S-3)
  Buffer: 4 points

Sprint 3 (20 points):
  - Story 1.7: Performance optimization (M-5)
  - Story 1.8: Monitoring (S-3)
  - Story 1.9: Documentation (S-3)
  Next epic: Story 2.1 (M-5)
  Buffer: 4 points
```

**Rules of thumb**:
- Reserve 20% capacity for buffer/unknowns
- Don't fill sprint to 100% (leaves no room for interruptions)
- Start next epic in final sprint if capacity available

### 7. Set Epic Timeline

**Timeline planning**:
```
Epic: Search Infrastructure
Start: Sprint 1 (Week 1)
End: Sprint 3 (Week 6)
Buffer: +1 sprint (Week 8) if needed

Key milestones:
- Week 2: OpenSearch operational
- Week 4: Hybrid search working (demo-able)
- Week 6: Production-ready with monitoring
```

**Use board tools** to set epic dates (see `agile-board` skill for board-specific APIs).

## Story Dependencies

### Types of Dependencies

**1. Technical dependencies**:
```
Story A: Create database schema
  ↓ (blocks)
Story B: Implement CRUD operations
```

**2. Sequential dependencies**:
```
Story A: User registration
  ↓ (enables)
Story B: User login
```

**3. Cross-epic dependencies**:
```
Epic 1, Story 1.3: Search API
  ↓ (required by)
Epic 2, Story 2.1: Frontend search UI
```

**4. Cross-project dependencies**:
```
Project A: Authentication service
  ↓ (consumed by)
Project B: Document search service
```

### Identifying Dependencies

**During epic planning**:
- Review each story's acceptance criteria
- Ask: "What must exist before this story can be implemented?"
- Document dependencies in story Technical Notes

**Example story with dependencies**:
```markdown
## Story 1.3: Implement hybrid search service

## Technical Notes
**Dependencies**:
- Story 1.1: OpenSearch collection must exist
- Story 1.2: Index schema must be deployed
- External: BGE-M3 model embeddings (from separate project)

**Blocks**:
- Story 1.4: API integration (can't integrate without search service)
- Story 2.1: Frontend search (requires working API)
```

### Tracking Dependencies

**In board tools**:
- Use dependency/blocker relationships (see `agile-board` skill)
- ZenHub: `createBlockage(blockingIssueId, blockedIssueId)`
- Jira: Link issues with "blocks" relationship
- Linear: Create blocker relationships

**Dependency matrix** (for complex epics):

| Story | Depends On | Blocks | Status |
|-------|------------|--------|--------|
| 1.1   | None       | 1.2, 1.3 | Done |
| 1.2   | 1.1        | 1.3    | In Progress |
| 1.3   | 1.1, 1.2   | 1.4, 2.1 | Blocked |
| 1.4   | 1.3        | None   | Not Started |
| 2.1   | 1.3        | None   | Not Started |

### Managing Blocked Stories

**When story is blocked**:
1. **Document blocker** in story comments
2. **Update board** - move to "Blocked" status or add blocker label
3. **Communicate** with team (daily standup)
4. **Find alternatives** - can team work on different story?
5. **Escalate** if blocker is external or prolonged

**Example**:
```markdown
## Story 1.4: API Integration (BLOCKED)

**Blocker**: Story 1.3 (Hybrid search) delayed due to OpenSearch configuration issues.

**ETA**: Unblocked by end of Sprint 2 (Friday).

**Action**: Team working on Story 1.5 (Auth) instead. Will resume 1.4 when unblocked.
```

### Dependency Best Practices

**DO**:
- ✅ Identify dependencies early (during epic planning)
- ✅ Schedule dependent stories in correct sequence
- ✅ Track cross-epic dependencies explicitly
- ✅ Communicate blockers immediately
- ✅ Have backup stories ready if primary work is blocked

**DON'T**:
- ❌ Assume dependencies will resolve themselves
- ❌ Schedule dependent stories in same sprint (leaves no buffer)
- ❌ Hide blockers from team
- ❌ Let blocked stories sit idle

## Interface Design and Mocking

### Overview

**CRITICAL**: When planning epics, consider interfaces between components to enable parallel development.

**Benefits**:
- Teams can work in isolation
- No waiting for dependencies
- Integration issues caught early
- External integrators can develop against mocks

### Interface Planning Process

#### 1. Identify Component Boundaries

**During epic planning**, identify all component interfaces:

**Example - Microservices Architecture**:
```
Epic 1: Authentication Service
  ↓ (API interface)
Epic 2: Search Service (consumes auth)
  ↓ (API interface)
Epic 3: Frontend (consumes search)
```

**Questions to ask**:
- What APIs will be exposed?
- What data will be exchanged?
- What's the contract format? (REST, GraphQL, gRPC?)
- Who are the consumers?

#### 2. Define Interface Contracts

**Create API specification BEFORE implementing**:

**OpenAPI/Swagger example**:
```yaml
openapi: 3.0.0
info:
  title: Authentication API
  version: 1.0.0
paths:
  /auth/validate:
    post:
      summary: Validate JWT token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                token:
                  type: string
              required:
                - token
      responses:
        '200':
          description: Token is valid
          content:
            application/json:
              schema:
                type: object
                properties:
                  valid:
                    type: boolean
                  user_id:
                    type: string
                  email:
                    type: string
        '401':
          description: Token is invalid
```

**GraphQL schema example**:
```graphql
type Query {
  validateToken(token: String!): ValidationResult!
}

type ValidationResult {
  valid: Boolean!
  userId: String
  email: String
  error: String
}
```

#### 3. Document Interfaces

**Create interface documentation**:

**Common locations**:
- `/docs/api/` - API specifications
- `/docs/interfaces/` - Interface contracts
- `/contracts/` - Shared contract definitions
- `README.md` in each service - Links to relevant interfaces

**Documentation should include**:
- Request/response formats
- Error handling
- Authentication requirements
- Rate limiting
- Versioning strategy
- Example requests/responses

#### 4. Create Mocks with Mockoon

**Use Mockoon as the standard approach** for creating API mocks.

**Why Mockoon**:
- Standardised across all projects
- Easy to create and maintain
- Can run locally or in CI/CD
- Supports OpenAPI import
- Realistic response simulation

**Mockoon setup**:
```bash
# Install Mockoon CLI
npm install -g @mockoon/cli

# Create mock from OpenAPI spec with auto-reload on changes
mockoon-cli start \
  --data ./docs/api/auth-service.yaml \
  --port 3001 \
  --watch
```

The `--watch` parameter monitors the mock file for changes and automatically reloads the server, enabling rapid iteration during development.

**Mockoon environment file** (`mocks/auth-service.mockoon.json`):
```json
{
  "name": "Authentication Service Mock",
  "port": 3001,
  "routes": [
    {
      "method": "post",
      "endpoint": "auth/validate",
      "responses": [
        {
          "statusCode": 200,
          "headers": [
            {"key": "Content-Type", "value": "application/json"}
          ],
          "body": "{\n  \"valid\": true,\n  \"user_id\": \"user-123\",\n  \"email\": \"test@example.com\"\n}"
        }
      ]
    }
  ]
}
```

#### 5. Create Mocks for Integrators

**CRITICAL**: If creating an API, provide mocks that integrators can use.

**Deliverables for integrators**:
1. **OpenAPI/Swagger spec** - Machine-readable API definition
2. **Mockoon environment** - Ready-to-run mock server
3. **Docker Compose** - Mock server in container
4. **Example requests** - Postman/cURL examples
5. **Integration guide** - How to use the mock

**Docker Compose for mock** (`docker-compose.mock.yml`):
```yaml
version: '3.8'
services:
  auth-mock:
    image: mockoon/cli:latest
    command: ["--data", "/data/auth-service.mockoon.json", "--port", "3001", "--watch"]
    volumes:
      - ./mocks:/data
    ports:
      - "3001:3001"
```

**Integration guide** (`docs/INTEGRATION.md`):
```markdown
# Integration Guide: Authentication Service

## Using the Mock Server

### Quick Start

1. Start the mock server:
   ```bash
   docker-compose -f docker-compose.mock.yml up -d
   ```

2. Mock server runs at: `http://localhost:3001`

3. Test with curl:
   ```bash
   curl -X POST http://localhost:3001/auth/validate \
     -H "Content-Type: application/json" \
     -d '{"token": "test-token"}'
   ```

### Mock Responses

The mock server returns realistic responses:
- Valid token → 200 with user details
- Invalid token → 401 with error
- Missing token → 400 with validation error

### Switching to Production

Change base URL from `http://localhost:3001` to `https://api.example.com` when ready.

### Support

Questions? Contact: auth-team@example.com
```

#### 6. Work in Isolation

**Teams can now develop in parallel**:

**Team A (Auth Service)**:
- Implements real auth service
- Tests against own integration tests

**Team B (Search Service)**:
- Develops search service
- Uses auth mock for development
- No dependency on Team A

**Team C (Frontend)**:
- Develops UI
- Uses search mock for development
- No dependency on Team A or B

**Integration Sprint**:
- Replace mocks with real services
- Run integration tests
- Fix any interface mismatches

### Mock Best Practices

**DO**:
- ✅ Create interface contract BEFORE implementation
- ✅ Use Mockoon for all API mocks (standardisation)
- ✅ Provide mocks to external integrators
- ✅ Keep mocks updated with interface changes
- ✅ Include realistic error responses in mocks
- ✅ Version mocks alongside API versions

**DON'T**:
- ❌ Create mocks without interface contract
- ❌ Use different mocking approaches across projects
- ❌ Let mocks drift from real implementation
- ❌ Skip error scenarios in mocks
- ❌ Forget to document how to use mocks

### Integration Testing Strategy

**Once real services are available**:

**Integration test layers**:
```
1. Unit tests → Mock all external dependencies
2. Integration tests (component) → Mock external services, use real internal components
3. Integration tests (end-to-end) → Use real services, no mocks
4. Contract tests → Verify real service matches contract used by mocks
```

**Contract testing example** (using Pact):
```python
# Test that real auth service matches contract
def test_auth_service_validates_token():
    # Real service
    response = requests.post(
        "https://api.example.com/auth/validate",
        json={"token": "test-token"}
    )

    # Should match mock contract
    assert response.status_code == 200
    assert "valid" in response.json()
    assert "user_id" in response.json()
    assert "email" in response.json()
```

### Example: Complete Interface Planning

**Scenario**: Epic 1 (Auth Service) and Epic 2 (Search Service) need to integrate

**Step 1: Identify interface**
- Search Service needs to validate user tokens
- Auth Service exposes `/auth/validate` endpoint

**Step 2: Define contract**
- Create `docs/api/auth-service.yaml` OpenAPI spec
- Define request/response formats
- Document error codes

**Step 3: Create mock**
- Create `mocks/auth-service.mockoon.json`
- Import OpenAPI spec into Mockoon
- Add realistic responses for all scenarios

**Step 4: Provide to Search team**
- Share OpenAPI spec
- Share Mockoon environment
- Share Docker Compose file
- Write integration guide

**Step 5: Parallel development**
- Auth team implements real service
- Search team develops against mock
- Teams work independently

**Step 6: Integration sprint**
- Search team switches from mock to real service
- Run integration tests
- Fix any interface mismatches
- Verify contract compliance

**Result**: Both epics delivered on time with minimal blocking

## Release Planning

### Multi-Epic Planning

**Release scope**:
```
Release 1.0 (12 weeks, 6 sprints):

Epic 1: Search Infrastructure (3 sprints) - Weeks 1-6
  - 9 stories, 45 points

Epic 2: Document Processing (2 sprints) - Weeks 5-8
  - 6 stories, 30 points
  - Starts Sprint 3 (overlaps with Epic 1)

Epic 3: User Interface (2 sprints) - Weeks 7-12
  - 8 stories, 35 points
  - Starts Sprint 4 (depends on Epic 1 completion)

Epic 4: Authentication (1.5 sprints) - Weeks 9-12
  - 5 stories, 25 points
  - Starts Sprint 5 (can run in parallel)

Total: 135 points across 6 sprints
Average: 22.5 points/sprint (within team velocity of 20-25)
```

**Timeline visualization**:
```
Sprint:  1    2    3    4    5    6
Epic 1: |====|====|====|
Epic 2:           |====|====|
Epic 3:                |====|====|====|
Epic 4:                     |====|====|
```

### Cross-Project Coordination

**When projects depend on each other**:

**Example**: Project A (Auth Service) → Project B (Search Service)

**Coordination points**:
1. **Define interface contract** - API specification that Project B needs
2. **Set milestone** - When will Project A deliver?
3. **Mock dependencies** - Project B can develop with mocked auth
4. **Integration sprint** - Dedicated sprint for integration testing
5. **Regular syncs** - Weekly cross-team standups

**Dependency tracking**:
```
Project A: Authentication Service
  Epic 1: JWT validation
    - Milestone: Sprint 2 (API contract ready)
    - Deliverable: JWT validation endpoint

Project B: Search Service
  Epic 1: Search Infrastructure
    - Story 1.5: Auth integration
    - Dependency: Project A, Epic 1, Sprint 2 milestone
    - Mitigation: Develop with mocked JWT validation
```

### Capacity Planning Across Epics

**Team capacity allocation**:
```
Sprint 3 (20 points capacity):

Epic 1 (finishing): 10 points
  - Story 1.8: Monitoring (S-3)
  - Story 1.9: Documentation (S-3)
  - Buffer: 4 points

Epic 2 (starting): 10 points
  - Story 2.1: PDF parser (M-5)
  - Story 2.2: Metadata extraction (M-5)
```

**When to start next epic**:
- ✅ Current epic has 1 sprint remaining
- ✅ Critical stories for current epic are done
- ✅ Next epic has no blockers
- ✅ Team has capacity (not overcommitted)

## Epic Metrics and Tracking

### Epic Burndown

Track remaining points over time:

```
Epic 1: Search Infrastructure (45 points total)

Sprint 1: 45 → 30 (15 points completed)
Sprint 2: 30 → 12 (18 points completed)
Sprint 3: 12 → 0  (12 points completed)

Status: On track (completed in 3 sprints as planned)
```

### Epic Velocity

**Epic velocity** = Total points completed ÷ Number of sprints

```
Epic 1: 45 points ÷ 3 sprints = 15 points/sprint (epic velocity)
Team velocity: 20 points/sprint (total capacity)
Epic capacity: 75% of team capacity
```

Use epic velocity to:
- Plan future epics of similar complexity
- Understand team's sustainable epic throughput
- Identify when epics are consuming too much capacity

### Dependency Risk Score

Track how dependent epic is:

**Low risk** (0-2 external dependencies):
- Epic can progress independently
- Timeline is predictable

**Medium risk** (3-5 external dependencies):
- Some coordination required
- Monitor dependencies weekly

**High risk** (6+ external dependencies):
- Significant coordination overhead
- Daily dependency tracking
- Consider breaking epic differently

## Example: Complete Epic Planning Session

**Epic**: Hybrid Search Service (Epic 1)

**Step 1: Requirements review**
- Objective: Enable semantic search for documents
- Deadline: End of Sprint 3 (6 weeks)
- Stakeholders: Product Owner, Research Team

**Step 2: Story identification**
```
Story 1.1: OpenSearch setup (M-5)
Story 1.2: Index schema (S-3)
Story 1.3: Hybrid search implementation (M-5)
Story 1.4: Query processing pipeline (M-5)
Story 1.5: Filter enforcement (S-3)
Story 1.6: Error handling (S-3)
Story 1.7: Performance optimization (M-5)
Story 1.8: Monitoring (S-3)
Story 1.9: Documentation (S-3)

Total: 35 points
```

**Step 3: Dependencies**
```
1.1 (OpenSearch) → 1.2 (Schema) → 1.3 (Hybrid search) → 1.4 (Pipeline)
1.5, 1.6, 1.7 depend on 1.3
1.8 can happen anytime after 1.3
```

**Step 4: Sprint allocation**
```
Sprint 1 (20 points):
  - 1.1: OpenSearch (M-5)
  - 1.2: Schema (S-3)
  - 1.5: Filters (S-3)
  - Other: Bug fixes (S-3)
  - Buffer: 6 points

Sprint 2 (20 points):
  - 1.3: Hybrid search (M-5)
  - 1.4: Pipeline (M-5)
  - 1.6: Error handling (S-3)
  - Other: Tech debt (S-3)
  - Buffer: 4 points

Sprint 3 (20 points):
  - 1.7: Performance (M-5)
  - 1.8: Monitoring (S-3)
  - 1.9: Documentation (S-3)
  - Next epic: 2.1 (M-5)
  - Buffer: 4 points
```

**Step 5: Set timeline**
- Start: Sprint 1, Week 1
- Demo: Sprint 2, Week 4 (hybrid search working)
- Complete: Sprint 3, Week 6
- Buffer: +1 sprint if needed

**Step 6: Track progress**
- Weekly epic burndown review
- Daily standup: dependency check
- Sprint review: demo incremental progress

## Tools and Templates

### Epic Planning Template

```markdown
# Epic X: [Name]

## Objective
[What user value does this deliver?]

## Timeline
- Start: Sprint X
- Target completion: Sprint Y
- Buffer: +Z sprints

## Stories

| Story | Title | Estimate | Dependencies | Sprint |
|-------|-------|----------|--------------|--------|
| X.1   | ...   | M (5)    | None         | 1      |
| X.2   | ...   | S (3)    | X.1          | 1      |
| X.3   | ...   | M (5)    | X.1, X.2     | 2      |

**Total**: [points]

## Risks
- [ ] Cross-project dependency on [Project Y]
- [ ] New technology (learning curve)
- [ ] External API stability

## Milestones
- Sprint 1: [Milestone]
- Sprint 2: [Demo-able feature]
- Sprint 3: [Production-ready]
```

### Dependency Tracking Spreadsheet

Create a spreadsheet to track cross-epic and cross-project dependencies:

| Epic | Story | Depends On | Blocks | Status | Risk |
|------|-------|------------|--------|--------|------|
| 1    | 1.3   | 1.1, 1.2   | 1.4, 2.1 | In Progress | Low |
| 2    | 2.1   | 1.3        | 2.2    | Blocked | Medium |

## Further Reading

- Scrum: Epic vs. Story vs. Task
- SAFe: Program Increment (PI) Planning
- Dependency management in distributed teams
- Critical path method (CPM) for project planning
