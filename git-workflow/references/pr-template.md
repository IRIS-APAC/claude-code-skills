# Pull Request Template

## PR Creation Workflow

**CRITICAL**: Before creating a PR, complete these steps:

### 1. Check Acceptance Criteria Completion

Review the story/ticket's acceptance criteria:
- ✅ All ACs should be complete (checked) for the PR
- ⚠️ If ACs are intentionally incomplete, document why

**If ACs are deferred**:
1. Update the story description:
   - Change deferred AC to ~~strikethrough~~
   - Add *italic justification* on the same line
2. Create/update another ticket with the deferred work
3. Link the ticket in the justification

**Example**:
```markdown
## Acceptance Criteria
- [x] User can log in with email/password
- [x] Session expires after 24 hours
- ~~[ ] Error messages display for invalid credentials~~ *Deferred to Story 1.5 - requires UX design review*
```

### 2. Update Story Description with Implementation Details

**Append an "Implementation" section** to the story description with:
- Implementation approach and decisions
- Testing results (unit, integration, manual)
- Performance metrics (if applicable)
- Known limitations or edge cases
- Links to related PRs or documentation

**Example**:
```markdown
## Implementation

**Approach**: Implemented JWT validation using Entra OIDC with JWKS key caching.

**Key decisions**:
- Using 1-hour TTL for JWKS key caching (balances performance vs security)
- Validating required claims only (iss, aud, exp, nbf)
- Optional claims validation deferred to Story 1.5

**Testing**:
- Unit tests: 42/42 passing
- Integration tests: 12/12 passing
- Manual testing: Verified with test Entra app (client ID: xxx)

**Performance**:
- JWT validation: <5ms average
- JWKS fetch (cache miss): ~200ms
- JWKS fetch (cache hit): <1ms

**Verified**:
- [x] All acceptance criteria implemented
- [x] Tests passing with >80% coverage
- [x] Manual testing completed
- [x] Security review (no hardcoded secrets)
```

**Why append to description**:
- Reviewer sees everything in one place
- No need to scroll through comments
- Permanent record of implementation details

### 3. Verify Story Updates Complete

Before creating PR, confirm:
- ✅ All completed ACs are checked on the ticket
- ✅ Deferred ACs have strikethrough + justification + ticket for deferred work
- ✅ Implementation section added to story description
- ✅ All commits have story reference in footer

### 4. Move Ticket to Review/QA After PR Creation

**After creating the PR**, move the ticket to the "Review/QA" pipeline on your agile board:

**Why**:
- Indicates code is ready for review
- Tracks work-in-review separately from work-in-progress
- Provides visibility into the review queue

**Common pipeline names**: "Review/QA", "In Review", "Code Review", "Testing", "QA"

See [agile-board/references/ticket-workflow.md](../../agile-board/references/ticket-workflow.md#move-ticket-to-reviewqa-pipeline) for board-specific examples.

## PR Title Format

```
[Epic X / Story Y.Z] Brief description
```

**Examples**:
- `[Epic 1 / Story 1.3] Implement hybrid search service`
- `[Epic 4 / Story 4.8] Add AI caption generation`
- `[Bugfix] Fix auth token expiry handling`
- `[Hotfix] Fix critical OpenSearch connection leak`

## PR Description Template

```markdown
## Summary
Brief description of changes (1-2 sentences)

## Story/Issue
Implements Story 1.3: Hybrid Search Service
Fixes #42

## Changes
- Bullet list of key changes
- Focus on what changed, not implementation details
- Use Australian English spelling

## Test Results
All tests passing ✅

\`\`\`
<paste your test output here>
Coverage: 89% (target: >80%)
\`\`\`

## Checklist
- [ ] All tests pass with coverage report
- [ ] Australian English spelling used throughout
- [ ] Type safety/strong typing used
- [ ] Code documentation added
- [ ] Error handling follows best practices
- [ ] Linting/formatting passes
- [ ] No secrets committed
- [ ] Documentation updated (if needed)

## Screenshots/Logs
(if applicable)
```

## Test Commands by Language/Framework

Before creating a PR, run your test suite with coverage:

| Language/Framework | Test Command | Coverage |
|-------------------|--------------|----------|
| **Python** | `pytest tests/ -v` | `--cov=src --cov-report=term-missing` |
| **Node/TypeScript** | `npm test` | `-- --coverage` |
| **Jest** | `jest` | `--coverage` |
| **C# (.NET)** | `dotnet test` | `/p:CollectCoverage=true` |
| **Flutter/Dart** | `flutter test` | `--coverage` |
| **CDK** | `npm test` (TypeScript) or `pytest` (Python) | Language-specific |
| **Terraform** | `terraform validate && terraform plan` | N/A |

## Creating PR with GitHub CLI

### Basic PR Creation

```bash
# Push branch first
git push -u origin feature/epic-1-story-1.3-hybrid-search

# Create PR targeting develop
gh pr create \
  --base develop \
  --title "[Epic 1 / Story 1.3] Implement hybrid search" \
  --body "## Summary
Implement hybrid search combining BM25 keyword search with vector semantic search.

## Story/Issue
Implements Story 1.3: Hybrid Search Service

## Changes
- Add OpenSearch hybrid query builder
- Implement RRF score normalisation
- Add filter allowlist enforcement
- Configure search pipeline with score normalisation

## Testing
- [x] Unit tests pass (\`pytest tests/unit\`)
- [x] Integration tests pass (\`pytest tests/integration\`)
- [x] Manual testing with sample queries
- [x] API contract validated

## Checklist
- [x] Australian English spelling used throughout
- [x] Type hints added for new functions
- [x] Docstrings added for public APIs
- [x] Error handling follows standard patterns
- [x] No secrets committed
- [x] Documentation updated in STORY_1.3_HYBRID_SEARCH.md"
```

### PR with Template File

Save template to `.github/pull_request_template.md`:

```bash
# Create PR using template
gh pr create \
  --base develop \
  --title "[Epic 1 / Story 1.3] Implement hybrid search" \
  --body-file .github/pull_request_template.md
```

### PR with HEREDOC

```bash
gh pr create --base develop --title "[Epic 1 / Story 1.3] Implement hybrid search" --body "$(cat <<'EOF'
## Summary
Implement hybrid search combining BM25 keyword search with vector semantic search.

## Story/Issue
Implements Story 1.3: Hybrid Search Service

## Changes
- Add OpenSearch hybrid query builder
- Implement RRF score normalisation
- Add filter allowlist enforcement

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed

## Checklist
- [x] Australian English spelling used throughout
- [x] Type hints added
- [x] Docstrings added
EOF
)"
```

## Verifying Target Branch

**CRITICAL**: Always verify the PR targets `develop` (NOT `main`):

```bash
# After creating PR
gh pr view --json baseRefName

# Expected output:
# {
#   "baseRefName": "develop"
# }

# If targeting wrong branch, close and recreate
gh pr close 42
gh pr create --base develop --title "..." --body "..."
```

## PR Checklist Examples

### Feature PR Checklist

```markdown
## Checklist
- [x] Australian English spelling used throughout
- [x] Type hints added for new functions
- [x] Docstrings added for public APIs (Google-style)
- [x] Error handling follows standard patterns (no bare except)
- [x] CloudWatch EMF metrics emitted for key operations
- [x] Request ID tracking in API responses
- [x] No secrets committed (.env files gitignored)
- [x] Unit tests added with >80% coverage
- [x] Integration tests added
- [x] Documentation updated in docs/stories/
- [x] API contract matches Appendix D (if API changes)
```

### Bugfix PR Checklist

```markdown
## Checklist
- [x] Root cause identified and documented
- [x] Fix tested with reproduction steps
- [x] Regression tests added
- [x] Related code reviewed for similar issues
- [x] Australian English spelling in commit messages
- [x] No breaking changes introduced
```

### Documentation PR Checklist

```markdown
## Checklist
- [x] Australian English spelling throughout
- [x] Code examples tested
- [x] Links verified
- [x] Formatting checked (markdown lint)
- [x] Screenshots current (if applicable)
```

## Example PRs

### Example 1: Feature Implementation

**Title**: `[Epic 1 / Story 1.3] Implement hybrid search service`

**Body**:
```markdown
## Summary
Implement hybrid search combining BM25 keyword search with vector semantic search using OpenSearch.

## Story/Issue
Implements Story 1.3: Hybrid Search Service
Relates to Epic 1: Search Infrastructure

## Changes
- Add OpenSearch hybrid query builder with BM25 + kNN
- Implement RRF (Reciprocal Rank Fusion) score normalisation
- Add filter allowlist enforcement (source, collection_id, doc_type)
- Configure search pipeline with score normalisation
- Add retrieval service with query preprocessing

## Testing
- [x] Unit tests pass (`pytest tests/unit/retrieval`)
- [x] Integration tests pass (`pytest tests/integration/test_search.py`)
- [x] Manual testing with sample queries:
  - Query: "academic integrity policy" → 5 results, scores normalised
  - Query: "machine learning course" → 3 results, filters applied
- [x] API contract validated (matches Appendix D response format)

## Performance
- Average query latency: 120ms (BM25) + 80ms (vector) = 200ms total
- RRF normalisation adds <5ms overhead

## Checklist
- [x] Australian English spelling used throughout
- [x] Type hints added for all functions
- [x] Google-style docstrings for public APIs
- [x] Error handling with specific exception types
- [x] CloudWatch EMF metrics for query latency
- [x] Request ID tracking in responses
- [x] No secrets committed
- [x] Documentation updated: docs/stories/STORY_1.3_HYBRID_SEARCH.md

## Screenshots/Logs
See attached: hybrid_search_results.png
```

### Example 2: Bugfix

**Title**: `[Bugfix] Fix filter normalisation for OpenSearch`

**Body**:
```markdown
## Summary
Fix filter normalisation to use common post_filter when available, falling back to duplicated filters for older OpenSearch versions.

## Story/Issue
Fixes #42

## Root Cause
OpenSearch 2.x supports both common `post_filter` and duplicated filter modes, but older versions only support duplicated filters. The code was only using duplicated mode, causing inefficient queries.

## Changes
- Detect OpenSearch version via cluster API
- Use common post_filter for OpenSearch 2.x+
- Fall back to duplicated filters for older versions
- Add version caching to avoid repeated API calls

## Testing
- [x] Unit tests added for both filter modes
- [x] Integration tests with OpenSearch 2.11 (local)
- [x] Tested with OpenSearch 1.x (mocked)
- [x] Manual verification: queries run 15% faster with post_filter

## Checklist
- [x] Root cause documented
- [x] Regression tests added
- [x] No breaking changes
- [x] Australian English spelling
```

### Example 3: Hotfix

**Title**: `[Hotfix] Fix critical OpenSearch connection leak`

**Body**:
```markdown
## Summary
Fix critical connection leak in OpenSearch client causing production timeouts after 100 requests.

## Issue
Production monitoring showed increasing connection count, causing 503 errors after ~100 search requests. Connection pool exhausted.

## Root Cause
OpenSearch client connections not properly closed in error paths. Client instances created per request instead of reused.

## Changes
- Move OpenSearch client to singleton pattern
- Add proper connection cleanup in error handlers
- Implement connection pool monitoring

## Testing
- [x] Load test: 1000 requests, no connection leaks
- [x] Error path tested: connection still closes on exceptions
- [x] Production validation: connection count stable after deployment

## Urgency
CRITICAL - Deployed to production immediately after testing.

## Checklist
- [x] Hotfix merged to main
- [x] Hotfix merged back to develop
- [x] Production monitoring confirms fix
```

## Common PR Mistakes

### ❌ Wrong: Targeting main instead of develop
```bash
gh pr create --base main  # Wrong for features!
```

### ✅ Correct: Targeting develop
```bash
gh pr create --base develop  # Correct for features
```

### ❌ Wrong: Vague title
```bash
--title "Update code"  # What code? Why?
```

### ✅ Correct: Specific title
```bash
--title "[Epic 1 / Story 1.3] Implement hybrid search service"
```

### ❌ Wrong: American English in description
```bash
--body "Implement query normalization..."  # American spelling!
```

### ✅ Correct: Australian English
```bash
--body "Implement query normalisation..."  # Australian spelling
```

### ❌ Wrong: No testing section
```markdown
## Changes
- Added new feature

## Checklist
- [x] Done
```

### ✅ Correct: Detailed testing
```markdown
## Changes
- Added new feature

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed

## Checklist
- [x] Tests added with >80% coverage
- [x] Documentation updated
```

## Automated PR Checks

PRs must pass these automated checks:

1. **Linting**: `ruff check`, `mypy`
2. **Unit tests**: `pytest tests/unit` (>80% coverage)
3. **Integration tests**: `pytest tests/integration`
4. **Security**: `bandit`, `safety`
5. **Build**: Docker image builds successfully
6. **Spelling**: Australian English check (custom script)

If checks fail:
```bash
# Fix locally
ruff check --fix src/
mypy src/

# Commit fix
git add .
git commit -m "style: fix linting issues"
git push

# Checks automatically re-run
```

## GitHub PR Template File

Save to `.github/pull_request_template.md` for automatic PR template:

```markdown
## Summary
<!-- Brief description of changes (1-2 sentences) -->

## Story/Issue
<!-- Implements Story X.Y / Fixes #XX -->

## Changes
<!-- Bullet list of key changes -->
-

## Testing
- [ ] Unit tests pass (`pytest tests/unit`)
- [ ] Integration tests pass (`pytest tests/integration`)
- [ ] Manual testing completed
- [ ] API contract validated (if applicable)

## Checklist
- [ ] Australian English spelling used throughout
- [ ] Type hints added for new functions
- [ ] Docstrings added for public APIs
- [ ] Error handling follows standard patterns
- [ ] No secrets committed
- [ ] Documentation updated (if needed)

## Screenshots/Logs
<!-- If applicable -->
```

This template automatically appears when creating PRs via the GitHub web UI.
