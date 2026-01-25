# User Story Templates

Templates and examples for writing effective user stories.

## Standard Story Template

```markdown
## Description
Brief overview of the story (1-2 paragraphs).
What functionality is being added and why.

## Context
Why this story is needed, what problem it solves.
Background information for developers.

## Acceptance Criteria
- [ ] Specific testable condition
- [ ] Another testable condition
- [ ] Final condition

## Technical Notes
- Implementation hints
- References to related docs
- Dependencies or blockers
- Architectural decisions

## Testing Strategy
- Unit tests for X
- Integration tests for Y
- Manual testing for Z
```

## Story Types

### Feature Story

**Focus**: End-user functionality

**Template**:
```markdown
## Description
As a [user type], I want to [action] so that [benefit].

[Additional context about the feature and why it's needed]

## Context
Current system doesn't support [X]. Users need this to [Y].

## Acceptance Criteria
- [ ] User can [specific action]
- [ ] System validates [specific conditions]
- [ ] Error messages display for [specific edge cases]
- [ ] [Performance/security requirement if applicable]

## Technical Notes
- Use [pattern/library/approach]
- See [reference documentation]
- Depends on [other story/component]

## Testing Strategy
- Unit tests for [component]
- Integration tests for [API/service]
- Manual testing: [specific scenarios]
```

**Example** (Python backend):
```markdown
## Description
As a researcher, I want to search for documents using natural language queries so that I can find relevant information even when I don't know exact keywords.

Implement hybrid search combining BM25 keyword matching with vector semantic search using OpenSearch.

## Context
Current search only uses BM25 keyword matching. Users struggle to find documents when they use different terminology than appears in the source material. Semantic search addresses this gap.

## Acceptance Criteria
- [ ] Search API accepts natural language queries
- [ ] Results combine BM25 and vector search scores using RRF normalisation
- [ ] Filter allowlist enforced (source, collection_id, doc_type)
- [ ] API response matches Standard Search API Contract (Appendix D)
- [ ] Query latency < 500ms for 95th percentile

## Technical Notes
- Use OpenSearch hybrid query type
- Set RRF normalisation in search pipeline
- Embed queries using same model as documents (BGE-M3)
- See docs/stories/STORY_1.3_HYBRID_SEARCH.md for implementation details

## Testing Strategy
- Unit tests for query builder (pytest)
- Integration tests for search endpoint (pytest with mocked OpenSearch)
- Manual testing with sample queries from requirements doc
- Performance testing: measure p95 latency
```

### Bug Fix Story

**Focus**: Fixing defects

**Template**:
```markdown
## Description
Fix [specific bug] that causes [symptom].

## Reproduction Steps
1. Do X
2. Observe Y
3. Expected Z, got W instead

## Root Cause
[Technical explanation of why bug occurs]

## Fix
[Description of solution approach]

## Acceptance Criteria
- [ ] Bug no longer occurs when following reproduction steps
- [ ] Regression test added to prevent recurrence
- [ ] Related edge cases tested
- [ ] No new bugs introduced

## Technical Notes
- Affects [file/module]
- May require [dependency update/config change]
```

**Example** (TypeScript/Node):
```markdown
## Description
Fix authentication token expiry causing 401 errors after 1 hour despite 24-hour token lifetime.

## Reproduction Steps
1. Log in to application
2. Wait 1 hour without activity
3. Attempt any API call
4. Expected: API call succeeds (token valid for 24 hours)
5. Actual: 401 Unauthorized error

## Root Cause
JWT middleware checks token expiry using local time instead of UTC, causing mismatch with token's UTC expiry timestamp.

## Fix
Update JWT validation to use UTC timestamps consistently.

## Acceptance Criteria
- [ ] Tokens remain valid for full 24 hours in any timezone
- [ ] Regression test added with timezone edge cases
- [ ] Existing auth flow unaffected
- [ ] No tokens invalidated during deployment

## Technical Notes
- Affects src/middleware/auth.ts
- Update Date comparisons to use Date.UTC()
- Test in multiple timezones (UTC, PST, AEST)
```

### Technical Story

**Focus**: Infrastructure or technical improvements

**Template**:
```markdown
## Description
[Technical change] to improve [aspect].

## Context
Current implementation has [limitation]. This change enables [capability] and improves [metric].

## Acceptance Criteria
- [ ] [Technical metric] improved by [amount]
- [ ] Existing functionality unaffected
- [ ] Documentation updated with new approach
- [ ] Performance/security/reliability impact verified

## Technical Notes
- Benchmark: [current vs. target metrics]
- Approach: [technical implementation details]
- Migration strategy: [how to deploy without downtime]

## Testing Strategy
- Benchmark tests: [measure improvement]
- Regression tests: [verify no breakage]
```

**Example** (CDK/Infrastructure):
```markdown
## Description
Implement auto-scaling for Lambda functions based on concurrent executions to reduce cold starts during traffic spikes.

## Context
Current Lambda configuration uses fixed provisioned concurrency of 5, causing cold starts during peak usage (8am-10am). Auto-scaling will maintain performance while reducing costs during off-peak hours.

## Acceptance Criteria
- [ ] Provisioned concurrency scales from 5 (off-peak) to 20 (peak)
- [ ] Scaling triggered by concurrent executions metric
- [ ] Cold start rate < 5% during peak hours
- [ ] Cost reduced by 40% compared to fixed provisioned concurrency of 20
- [ ] CloudFormation deployment succeeds without downtime

## Technical Notes
- Use Application Auto Scaling for Lambda
- Target tracking policy: 0.7 utilisation
- Scale-out cooldown: 60s, scale-in cooldown: 300s
- Alarms for under/over-provisioning

## Testing Strategy
- Load testing: simulate peak traffic
- Monitor CloudWatch metrics for 1 week
- Verify cost savings in billing console
```

## Writing Acceptance Criteria

### Format Requirements

**Always use checkbox format**:
```markdown
## Acceptance Criteria
- [ ] First criterion
- [ ] Second criterion
```

**NOT**:
```markdown
## Acceptance Criteria
* First criterion
* Second criterion
```

### INVEST Criteria

Good acceptance criteria follow **INVEST**:

- **Independent** - Can be tested without other criteria
- **Negotiable** - Details can be refined during development
- **Valuable** - Delivers user value
- **Estimable** - Can be sized
- **Small** - Fits in a sprint
- **Testable** - Can verify if met

### Good vs. Bad Examples

✅ **Good**:
```markdown
- [ ] User can upload PDF files up to 50MB
- [ ] System extracts text from PDF with OCR for scanned documents
- [ ] Upload progress indicator displays percentage complete
- [ ] Error message displays for unsupported file types
- [ ] Uploaded files appear in document list within 5 seconds
```

❌ **Bad**:
```markdown
- Upload works
- PDFs are processed
- Good user experience
- Fast performance
```

**Why bad criteria fail**:
- Not testable ("good user experience" - how measured?)
- Not specific ("upload works" - for what file types? sizes?)
- Not measurable ("fast performance" - how fast?)

## Technical Notes Best Practices

Use Technical Notes for:
- **Implementation guidance** - Preferred libraries, patterns, approaches
- **References** - Links to related docs, ADRs, external resources
- **Dependencies** - Other stories or components that must exist first
- **Constraints** - Performance targets, security requirements, compliance needs
- **Assumptions** - What we're assuming is true or will be handled elsewhere

**Example**:
```markdown
## Technical Notes
- Use OpenSearch hybrid query type (not manual score blending)
- See ADR-003 for vector search model selection rationale
- Depends on Story 1.1 (OpenSearch setup) being complete
- Target: p95 latency < 500ms, p99 < 1000ms
- Assumption: Document embeddings already exist in index
- RBAC enforcement handled by Story 1.4 (separate concern)
```

## Testing Strategy Best Practices

Be specific about:
- **Test types** - Unit, integration, E2E, performance, security
- **Test tools** - pytest, jest, cypress, k6, etc.
- **Coverage targets** - E.g., >80% line coverage
- **Manual testing** - Specific scenarios to verify manually

**Example**:
```markdown
## Testing Strategy
- Unit tests (pytest):
  - Query builder logic (100% coverage)
  - Score normalisation algorithms
  - Filter validation
- Integration tests (pytest with mocked OpenSearch):
  - End-to-end search flow
  - Error handling for OpenSearch failures
  - API contract compliance
- Manual testing:
  - Sample queries from requirements doc (Appendix B)
  - Cross-browser compatibility (Chrome, Firefox, Safari)
  - Verify results relevance with stakeholders
- Performance testing (k6):
  - Load test: 100 concurrent users, 5min duration
  - Verify p95 latency < 500ms
```

## Language-Specific Examples

### Python Backend Story

See Feature Story example above.

### TypeScript/React Frontend Story

```markdown
## Description
As a user, I want to see search results highlighted with query terms so that I can quickly identify why a document matched my search.

## Acceptance Criteria
- [ ] Query terms highlighted in result snippets
- [ ] Highlighting works for multi-word queries
- [ ] Case-insensitive matching
- [ ] Accessible colour contrast (WCAG AA compliant)
- [ ] No layout shift when highlighting applied

## Technical Notes
- Use mark-js library for highlighting
- Highlight colour: #FFF59D (yellow, passes WCAG AA)
- Debounce highlighting for performance
- See Figma designs for visual specification

## Testing Strategy
- Unit tests (jest): highlight logic
- Integration tests (React Testing Library): component rendering
- Manual testing: verify accessibility with screen reader
- Cross-browser testing: Chrome, Firefox, Safari, Edge
```

### Terraform/Infrastructure Story

See Technical Story example above for CDK.

For Terraform:
```markdown
## Technical Notes
- Use terraform workspaces for multi-environment support
- State stored in S3 backend (s3://company-terraform-state)
- Run terraform plan in CI/CD for PR validation
- Requires AWS credentials with AdministratorAccess
```

## Australian English Spelling

All story content uses **Australian English spelling**:

✅ **Correct**:
- normalise, organisation, authorisation
- colour, behaviour, analyse
- optimise, centre, metre

❌ **Wrong**:
- normalize, organization, authorization
- color, behavior, analyze
- optimize, center, meter

This is a **project-wide standard** for all documentation, code comments, and issue content.
