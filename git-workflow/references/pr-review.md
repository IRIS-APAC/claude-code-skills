# Pull Request Review Guide

## Review Process

### 1. Automated Checks (Must Pass First)

Before human review, PRs must pass:
- ✅ **Linting**: `ruff`, `mypy`
- ✅ **Unit tests**: `pytest` (>80% coverage)
- ✅ **Security scan**: `bandit`, `safety`
- ✅ **Build**: Docker image builds

**Check status**:
```bash
gh pr checks 42
```

If checks fail, reviewer should wait for fixes before reviewing.

### 2. Human Review (After Checks Pass)

Requires **1 approval** from:
- Lead engineer (for architectural decisions)
- OR peer reviewer (for code quality)

## Reviewing PRs with GitHub CLI

### View PR Details
```bash
# View PR in terminal
gh pr view 42

# View PR in browser
gh pr view 42 --web

# View specific files changed
gh pr diff 42

# View PR checks status
gh pr checks 42
```

### Check Out PR Locally
```bash
# Check out PR to test locally
gh pr checkout 42

# Run tests
pytest

# Try the feature manually
python -m uvicorn integrations.funnelback.main:app --reload

# Return to your branch
git checkout develop
```

### Leave Review

**Approve**:
```bash
gh pr review 42 --approve -b "LGTM - tests pass, code looks good"
```

**Request changes**:
```bash
gh pr review 42 --request-changes -b "Please add type hints to the new functions in search.py"
```

**Comment only**:
```bash
gh pr review 42 --comment -b "Consider extracting this into a helper function for reusability"
```

### Add Inline Comments

```bash
# View diff with line numbers
gh pr diff 42

# Comment on specific file/line (use web UI for now)
gh pr view 42 --web
# Navigate to Files Changed → Click line → Add comment
```

## Code Review Checklist

### 0. Acceptance Criteria Verification (CRITICAL - Check First)

**BEFORE reviewing code**, verify the story/ticket:

- [ ] **All ACs have implementation** - Each acceptance criterion has corresponding code changes
- [ ] **All ACs have tests** - Each AC has both unit and integration tests verifying the behaviour
- [ ] **Deferred ACs are properly documented**:
  - ~~Strikethrough~~ format with *italic justification*
  - New ticket created for deferred work
  - New ticket is NOT completed yet
- [ ] **Implementation section exists** - Story description has "Implementation" section with:
  - Implementation approach and key decisions
  - Testing results (unit, integration, manual)
  - Performance metrics (if applicable)
  - Known limitations
- [ ] **Review ticket comments** - Check for relevant implementation context, decisions, or trade-offs posted during development

**Example AC verification**:

Story has:
```markdown
## Acceptance Criteria
- [x] User can log in with email/password
- [x] Session expires after 24 hours
- ~~[ ] Error messages display for invalid credentials~~ *Deferred to Story 1.5 - requires UX design review*

## Implementation
**Approach**: Implemented JWT validation using Entra OIDC...
```

Reviewer checks:
1. ✅ AC 1: Login code exists (`auth.py:42-78`), tests pass (`test_auth.py:15-32`)
2. ✅ AC 2: Session expiry code exists (`session.py:23-45`), tests pass (`test_session.py:8-19`)
3. ✅ AC 3 deferred: Story 1.5 exists, NOT completed, has error messages work
4. ✅ Implementation section: Present with testing results and decisions

**If deferred ACs don't have a ticket**:
```bash
gh pr review 42 --request-changes -b "Deferred AC 'Error messages display for invalid credentials' needs a ticket.

Please create Story 1.5 for this work and link it in the AC justification."
```

**If ACs missing tests**:
```bash
gh pr review 42 --request-changes -b "AC 'Session expires after 24 hours' has implementation but no integration tests.

Please add integration test verifying session expiry behaviour."
```

### 1. Australian English Spelling
- [ ] **Variable names** use Australian spelling (normalise, organisation, authorisation)
- [ ] **Function names** use Australian spelling
- [ ] **Comments** use Australian spelling
- [ ] **Docstrings** use Australian spelling
- [ ] **Error messages** use Australian spelling

**Examples**:
- ✅ `def normalise_query(...)`, `class AuthorisationService`, `# Normalise user input`
- ❌ `def normalize_query(...)`, `class AuthorizationService`, `# Normalize user input`

### 2. Type Safety
- [ ] **Type annotations/strong typing** used where supported by language
- [ ] **Return types** specified
- [ ] **Nullable/optional types** explicitly declared
- [ ] **Avoid dynamic/any types** unless absolutely necessary

**Language-specific examples**:
- **Python**: Type hints with `typing` module
- **TypeScript/Node**: Interface/type definitions
- **C#**: Explicit types, nullable reference types
- **Dart/Flutter**: Strong typing with null safety
- **CDK (TypeScript/Python)**: Type-safe constructs
- **Terraform**: Variable type constraints

### 3. Error Handling
- [ ] **Specific exception types** (not bare `except:`)
- [ ] **Error messages** are clear and actionable
- [ ] **Logging** before raising exceptions
- [ ] **No swallowed exceptions** (empty except blocks)

**Examples**:
```python
# ✅ Good
try:
    result = opensearch_client.search(...)
except ConnectionError as e:
    logger.error("opensearch_connection_failed", error=str(e))
    raise HTTPException(status_code=503, detail="Search service unavailable")

# ❌ Bad - Bare except
try:
    result = opensearch_client.search(...)
except:
    pass
```

### 4. Security
- [ ] **No hardcoded secrets** (API keys, passwords, tokens)
- [ ] **No credentials in logs** or error messages
- [ ] **Input validation** for user-supplied data
- [ ] **SQL injection protection** (if using SQL)
- [ ] **No eval() or exec()** on user input

**Examples**:
```python
# ✅ Good - Use environment variables
api_key = os.getenv("API_KEY")

# ❌ Bad - Hardcoded secret
api_key = "sk-1234567890abcdef"
```

### 5. API Contract Compliance
- [ ] **Matches Standard Search API Contract** (Appendix D)
- [ ] **Error responses** follow format: `{"detail": {"error": "...", "message": "..."}}`
- [ ] **Request IDs** included in responses
- [ ] **HTTP status codes** correct (400, 401, 403, 404, 503)

**Examples**:
```python
# ✅ Good - Follows API contract
{
    "detail": {
        "error": "invalid_request",
        "message": "Missing required field: query",
        "request_id": "uuid-1234"
    }
}

# ❌ Bad - Non-standard format
{
    "error": "Bad request"
}
```

### 6. Logging and Observability
- [ ] **Structured logging** with context (request_id, kb_id, user_id)
- [ ] **Log levels** appropriate (ERROR, WARNING, INFO, DEBUG)
- [ ] **No sensitive data** in logs (passwords, tokens, PII)
- [ ] **CloudWatch EMF metrics** for key operations (if applicable)

**Examples**:
```python
# ✅ Good - Structured logging
logger.info(
    "search_request",
    request_id=request_id,
    kb_id=kb_id,
    query=query,
    top_k=top_k
)

# ❌ Bad - Unstructured logging
print(f"Search: {query}")
```

### 7. Testing (CRITICAL - Must Include Results)
- [ ] **Tests run and results posted** in PR comments
- [ ] **All tests passing** with count (e.g., "288/288 passed in 4.26s")
- [ ] **Coverage report** included:
  - **Minimum**: 80% coverage (blocking requirement)
  - **Target**: 90%+ coverage (aim for this)
- [ ] **Unit tests** added for new code
- [ ] **Integration tests** added for new code (both unit AND integration required)
- [ ] **Edge cases** tested (empty input, null values, errors)
- [ ] **Test names** descriptive (`test_search_returns_empty_when_no_results`)
- [ ] **Mocks/stubs created** for external dependencies (if creating an API or service interface):
  - Mockoon environment file exists
  - OpenAPI/GraphQL spec exists
  - Integration guide provided
  - Mock responses include error scenarios

**Example test results comment**:
```
## Test Results: 288/288 Passing ✅

Verified:
- Module A: 29 tests ✅
- Module B: 29 tests ✅
- Module C: 43 tests ✅
- Module D: 29 tests ✅

pytest tests/ -v
======================== 288 passed in 4.26s =========================
```

### When Reviewer Should Run Tests Locally

**REQUIRED (must run locally)**:
- ✅ **Last story in an epic** - Verify epic-level integration, cumulative coverage, and epic ACs
- ✅ Critical changes (security, auth, payment, data loss scenarios)
- ✅ Automated CI/CD checks failed or suspicious results
- ✅ Complex changes affecting core functionality

**Optional** (trust CI/CD and posted results):
- Regular story PRs (non-epic-closing, routine changes)

**How to run locally**:
```bash
# Check out the PR
gh pr checkout 42

# Run tests with coverage
pytest --cov=src tests/

# Check coverage report
coverage report

# View detailed HTML report
coverage html
open htmlcov/index.html
```

**For last story in epic, verify**:
- All epic stories integrate correctly
- Cumulative test coverage across epic meets 80% minimum (aim for 90%+)
- No regressions from earlier epic stories
- Epic-level acceptance criteria are met
- All deferred stories from epic have tickets

**If tests fail**, document the failure and request fixes:
```
## Test Results: 287/288 - One Fix Needed ❌

❌ Failing Test: test_parse_pdf_ocr_empty_page
Error: TypeError: Logger._log() got an unexpected keyword argument 'page_num'

Fix Required:
- Change logging.getLogger() to structlog.get_logger() in pdf_parser.py

After fix, re-run:
pytest tests/unit/test_pdf_parser.py::test_parse_pdf_ocr_empty_page -v
```

### 8. Documentation
- [ ] **Code documentation** for public functions/methods (language-appropriate style)
- [ ] **README** updated if API changes
- [ ] **Story implementation docs** updated (if applicable)
- [ ] **Comments** explain "why" not "what"

**Documentation styles by language**:
- **Python**: Docstrings (Google/NumPy style)
- **TypeScript/Node**: JSDoc comments
- **C#**: XML documentation comments
- **Dart/Flutter**: DartDoc comments
- **CDK**: Inline documentation for constructs
- **Terraform**: Module/variable descriptions

**Comment quality**:
```
# ✅ Good - Explains why
# Use RRF normalisation instead of min-max to handle score distribution
scores = rrf_normalise(bm25_scores, vector_scores)

# ❌ Bad - Explains what (obvious from code)
# Normalise scores
scores = normalise(bm25_scores, vector_scores)
```

### 9. Performance
- [ ] **No N+1 queries** (database or API calls in loops)
- [ ] **No unbounded loops** without limits
- [ ] **Caching** used where appropriate
- [ ] **Database indexes** for frequently queried fields (if applicable)

**Examples**:
```python
# ✅ Good - Single query with joins
results = db.query(...).join(...).all()

# ❌ Bad - N+1 queries
for item in items:
    detail = db.query(...).filter(id=item.id).first()  # N queries!
```

### 10. Code Quality
- [ ] **No code duplication** (DRY principle)
- [ ] **Function complexity** reasonable (<10 branches)
- [ ] **Naming** clear and descriptive
- [ ] **Magic numbers** replaced with named constants
- [ ] **No commented-out code** (remove or explain why kept)

## Review Comments Template

### Request Type Hints
```
Please add type hints to the new functions:

\`\`\`python
def search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    ...
\`\`\`
```

### Request Australian English
```
Please use Australian English spelling:

- Line 42: `normalise` (not `normalize`)
- Line 56: `authorisation` (not `authorization`)
```

### Request Error Handling
```
Please add specific exception handling here instead of bare except:

\`\`\`python
except ConnectionError as e:
    logger.error("opensearch_connection_failed", error=str(e))
    raise HTTPException(status_code=503, detail="Search service unavailable")
\`\`\`
```

### Request Tests
```
Please add unit tests for the new `hybrid_search()` function, covering:
- Happy path
- Empty results
- OpenSearch connection error
```

### Suggest Improvement
```
Consider extracting this logic into a helper function for reusability:

\`\`\`python
def build_hybrid_query(query: str, filters: Dict) -> Dict:
    # ... extracted logic ...
\`\`\`
```

### Approve with Minor Suggestions
```
LGTM! Tests pass and code looks good.

Minor suggestion: Consider adding a docstring to `normalise_filters()` explaining the filter allowlist.
```

## Merge Requirements

Before merging, verify:
- ✅ All automated checks passing
- ✅ Approved by lead engineer or peer
- ✅ No merge conflicts
- ✅ Up to date with target branch (develop)
- ✅ **Target branch is correct** (develop for features, main for releases)

**Verify target branch**:
```bash
gh pr view 42 --json baseRefName
# Expected: "baseRefName": "develop"
```

**Merge using merge commit strategy**:
```bash
gh pr merge 42 --merge --delete-branch
```

**NEVER use**:
- ❌ `--squash` (loses commit history)
- ❌ `--rebase` (rewrites history)

## Common Review Issues

### Issue: American English Spelling
**Problem**:
```python
def normalize_query(query: str) -> str:  # Wrong!
    return query.lower()
```

**Solution**:
```python
def normalise_query(query: str) -> str:  # Correct!
    return query.lower()
```

**Review comment**:
> Please use Australian English spelling: `normalise` (not `normalize`)

---

### Issue: Missing Type Hints
**Problem**:
```python
def search(query, top_k=5):
    ...
```

**Solution**:
```python
def search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    ...
```

**Review comment**:
> Please add type hints for parameters and return type.

---

### Issue: Bare Except
**Problem**:
```python
try:
    result = client.search(...)
except:
    return []
```

**Solution**:
```python
try:
    result = client.search(...)
except ConnectionError as e:
    logger.error("search_failed", error=str(e))
    raise HTTPException(status_code=503, detail="Search service unavailable")
```

**Review comment**:
> Please use specific exception types instead of bare `except:`, and log the error before raising.

---

### Issue: Hardcoded Secret
**Problem**:
```python
api_key = "sk-1234567890abcdef"
```

**Solution**:
```python
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set")
```

**Review comment**:
> ⚠️ **Security**: Please remove hardcoded API key and use environment variable instead.

---

### Issue: Missing Tests
**Problem**: PR adds new function but no tests

**Review comment**:
> Please add unit tests for `hybrid_search()` covering:
> - Happy path with valid query
> - Empty results
> - OpenSearch connection error

---

### Issue: Wrong PR Target
**Problem**: PR targets `main` instead of `develop`

**Review comment**:
> ⚠️ **This PR targets main, but features should target develop.**
>
> Please close this PR and create a new one with:
> ```bash
> gh pr create --base develop --title "..." --body "..."
> ```

## Review Response Examples

### Approving Changes
```bash
gh pr review 42 --approve -b "LGTM!

✅ Tests pass
✅ Code quality good
✅ Australian English throughout
✅ Type hints present
✅ Error handling appropriate

Ready to merge."
```

**After approval and merge**, move the ticket to "Done" pipeline on the agile board. See [agile-board/references/ticket-workflow.md](../../agile-board/references/ticket-workflow.md#on-pr-approval-and-merge-move-to-done) for details.

### Requesting Changes
```bash
gh pr review 42 --request-changes -b "Please address these issues before merging:

1. Add type hints to functions in search.py (lines 42, 56, 78)
2. Fix American English spelling:
   - Line 42: normalise (not normalize)
   - Line 56: authorisation (not authorization)
3. Add unit tests for hybrid_search() function

Thanks!"
```

**When requesting changes**, the reviewer should move the ticket back to "In Progress" pipeline on the agile board. See [agile-board/references/ticket-workflow.md](../../agile-board/references/ticket-workflow.md#on-pr-rejection-move-back-to-in-progress) for details.

### Commenting (No Approval)
```bash
gh pr review 42 --comment -b "Nice work!

A few suggestions:
- Consider extracting filter logic into separate function
- Could add a docstring explaining the RRF algorithm

Not blocking, but might be worth considering."
```

## Fast-Track Approval Criteria

PRs can be fast-tracked (single reviewer) if:
- ✅ Small change (<100 lines)
- ✅ All automated checks pass
- ✅ Documentation or test-only changes
- ✅ Urgent hotfix (with post-merge review)

PRs requiring thorough review:
- ⚠️ Large changes (>500 lines)
- ⚠️ Architectural changes
- ⚠️ Security-sensitive code
- ⚠️ Breaking changes to API contract

## Post-Merge Checklist

After merging:
- [ ] Delete feature branch (automated with `--delete-branch`)
- [ ] Verify deployment to dev environment
- [ ] Monitor for errors in logs/metrics
- [ ] Update ZenHub story status to "Done"
- [ ] Notify team in Slack (if significant change)

## Additional Resources

- API Contract: `docs/Design/system-requirements.md` (Appendix D)
- Error Handling: `docs/ERROR_HANDLING.md`
- Design Patterns: `docs/DESIGN_PATTERNS.md`
- Testing Guide: `docs/stories/TESTING_STORY_1.3.md`
