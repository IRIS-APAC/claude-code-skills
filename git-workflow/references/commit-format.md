# Commit Message Format

This project follows **Conventional Commits** with **Australian English** spelling.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Types

Maps to semantic versioning:

| Type | SemVer | Purpose | Example |
|------|--------|---------|---------|
| `feat` | MINOR | New feature | `feat(auth): implement JWT validation` |
| `fix` | PATCH | Bug fix | `fix(retrieval): correct filter normalisation` |
| `docs` | - | Documentation changes | `docs(api): update search endpoint examples` |
| `style` | - | Code formatting (no logic change) | `style(retrieval): fix indentation` |
| `refactor` | - | Code restructure (no behaviour change) | `refactor(pipeline): extract parser base class` |
| `perf` | - | Performance improvement | `perf(opensearch): add query result caching` |
| `test` | - | Adding/updating tests | `test(auth): add JWT validation tests` |
| `chore` | - | Build process, dependencies, tooling | `chore(deps): upgrade opensearch-py to 2.4.0` |

## Scopes

Match module structure or story-based identifiers:

**Module-based**:
- `api`, `auth`, `retrieval`, `embeddings`, `opensearch`, `content_store`, `pipeline`, `orchestration`, `observability`

**Story-based**:
- `story-1.3`, `epic-2`, `story-4.8`

**Examples**:
- `feat(auth): implement JWT validation`
- `fix(story-1.3): correct hybrid search score normalisation`
- `chore(epic-4): update dependencies for caption generation`

## Description

- Use imperative mood ("add" not "added" or "adds")
- Start with lowercase
- No period at the end
- Keep to 50 characters or less
- **MUST use Australian English spelling**

**Good**:
- ✅ `feat(auth): implement JWT validation with Entra OIDC`
- ✅ `fix(retrieval): correct filter normalisation for OpenSearch`
- ✅ `docs(pipeline): clarify metadata extraction workflow`

**Bad**:
- ❌ `feat(auth): Implemented JWT validation` (past tense)
- ❌ `fix(retrieval): Correct filter normalization` (American spelling)
- ❌ `docs: Updated the pipeline documentation.` (period at end)

## Body

Optional but **highly recommended** for non-trivial changes. Use for:
- **Context paragraph**: Explain WHY the change was needed (not what - git diff shows what)
- **Changes section**: Detailed bullet list of modifications
- **Impact section**: What the change achieves or fixes
- **Verified section**: Test results proving the change works

**Structure** (see Example 1 for real commit):
```
<type>(<scope>): <description>

Context paragraph explaining why this change was needed.

Changes:
- Detailed bullet list
- Of all modifications
- Organized logically

Impact:
- What this achieves
- What problems it fixes

Verified:
- Test results
- Proof it works
```

**Rules**:
- Wrap at 72 characters
- Separate from description with blank line
- Use bullet points for multiple items
- **MUST use Australian English spelling**

## Footer

Optional. Use for:
- Linking to issues/stories: `Implements Story 1.3`, `Fixes #42`, `Relates to Story 4.8`
- Breaking changes: `BREAKING CHANGE: ...`
- **NEVER include AI attribution** (`Co-Authored-By: Claude`)

## Complete Examples

### Example 1: Real commit from project (7343c67)

```
fix(tests): update S3 bucket names to match source-specific architecture

Updated integration test fixtures and documentation to use the correct
source-specific S3 bucket naming convention introduced in commit 54ff0ef.

Changes:
- Updated setup_s3_buckets() fixture in tests/conftest.py to check for:
  - content-store-funnelback-local
  - content-store-sharepoint-local
  - knowledge-search-local (unchanged)
- Updated .env.example with correct bucket naming and documentation
- Updated README.md with source-specific bucket example
- Updated docker-compose.local.yml SharePoint worker to use correct bucket
- Updated LOCAL_DEVELOPMENT.md with source-specific bucket examples

Impact:
- Fixes 36 skipped integration tests that were failing due to missing
  old bucket name (knowledge-content)
- Tests now correctly validate against buckets created by setup-local.sh

Verified:
- All incremental indexing tests now pass (12 tests)
- All Funnelback pipeline lock tests now pass (10 tests)
- All Funnelback stale cleanup tests now pass (8 tests)
- SharePoint pipeline lock tests now pass (10 of 11 tests)
```

**Why this is excellent**:
- ✅ Clear type and scope
- ✅ Context paragraph explaining WHY the change was needed
- ✅ "Changes:" section with detailed bullets
- ✅ "Impact:" section explaining what the fix achieves
- ✅ "Verified:" section with test results proving it works
- ✅ References related commit (54ff0ef)

### Example 2: Bug fix

```
fix(retrieval): correct filter normalisation for OpenSearch

- Use common post_filter when available
- Fall back to duplicated filters for older versions

Fixes #42
```

**Why good**:
- ✅ Type: fix (PATCH)
- ✅ Australian English ("normalisation")
- ✅ Explains the solution
- ✅ Links to issue

### Example 3: Documentation

```
docs(pipeline): clarify metadata extraction workflow in integration guide
```

**Why good**:
- ✅ Short and clear
- ✅ No body needed (simple change)
- ✅ Scope matches file location

### Example 4: Refactoring

```
refactor(pipeline): extract common parser base class

Move shared parsing logic from HTMLParser and PDFParser to new
ParserBase abstract class. No functional changes to parsing behaviour.

Relates to Story 4.2
```

**Why good**:
- ✅ Type: refactor (no behaviour change)
- ✅ Explains why (code organisation)
- ✅ Australian English ("behaviour")
- ✅ Links to story

### Example 5: Multi-story commit

```
feat(story-4.8): implement AI caption generation with Bedrock

- Add BedrockClient wrapper with rate limiting
- Implement caption prompt engineering
- Extract key points and keywords from document content
- Add caching to avoid duplicate API calls

Uses AWS Bedrock Claude Sonnet 4.5 with AU inference profile.
Rate limited to 20 requests/minute to stay within quotas.

Implements Story 4.8
```

**Why good**:
- ✅ Story-based scope
- ✅ Detailed bullet points
- ✅ Context in body (rate limiting)
- ✅ Australian English throughout

## Using HEREDOC for Multi-line Messages

For commits with body text, use HEREDOC to ensure proper formatting:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): implement JWT validation with Entra OIDC

- Add JWKS key caching with 1-hour TTL
- Validate required claims (iss, aud, exp, nbf)
- Extract user identity and authorisation context

Implements Story 1.4a
EOF
)"
```

**Why HEREDOC**:
- ✅ Preserves formatting
- ✅ Easier to edit multi-line text
- ✅ No escaping issues with quotes

## Common Mistakes

### ❌ Wrong: American English
```
feat(auth): implement JWT validation with Entra OIDC

- Add JWKS key caching with 1-hour TTL
- Extract user identity and authorization context  # Wrong!

Implements Story 1.4a
```

### ✅ Correct: Australian English
```
feat(auth): implement JWT validation with Entra OIDC

- Add JWKS key caching with 1-hour TTL
- Extract user identity and authorisation context  # Correct!

Implements Story 1.4a
```

### ❌ Wrong: AI Attribution
```
feat(retrieval): implement hybrid search

- Add OpenSearch hybrid query builder
- Implement RRF score normalisation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>  # NEVER DO THIS!
```

### ✅ Correct: Human Attribution Only
```
feat(retrieval): implement hybrid search

- Add OpenSearch hybrid query builder
- Implement RRF score normalisation

Implements Story 1.3
```

### ❌ Wrong: Past Tense
```
feat(auth): implemented JWT validation  # Wrong!
```

### ✅ Correct: Imperative Mood
```
feat(auth): implement JWT validation  # Correct!
```

### ❌ Wrong: Vague Description
```
fix: fix bug  # What bug? Where?
```

### ✅ Correct: Specific Description
```
fix(retrieval): correct filter normalisation for OpenSearch
```

## Australian English Spelling Quick Reference

**MUST use** (Australian):
- normalise, normalised, normalisation
- organisation, organisational
- authorise, authorised, authorisation
- optimise, optimised, optimisation
- centralise, centralised
- behaviour
- colour
- honour, labour

**NEVER use** (American):
- normalize, normalized, normalization
- organization, organizational
- authorize, authorized, authorization
- optimize, optimized, optimization
- centralize, centralized
- behavior
- color
- honor, labor

## Commit Workflow with Story/Ticket Updates

**CRITICAL**: Before committing, always update the associated story/ticket:

### 0. Before Starting Work: Move Ticket to In Progress

**When you start working on a story** (during analysis phase, before any commits), move the ticket to the "In Progress" pipeline on your agile board.

**Why**: Makes work visible, prevents duplicate effort, provides accurate progress tracking.

See [agile-board/references/ticket-workflow.md](../../agile-board/references/ticket-workflow.md#before-starting-work-move-to-in-progress) for board-specific examples.

### 1. Check Acceptance Criteria

**On every commit**, review the story's acceptance criteria:
- ✅ Mark ACs as done where appropriate (use GitHub/ZenHub UI to check boxes)
- ❌ NEVER change or modify the ACs themselves
- ✅ Only mark checkboxes, don't edit text

**Example**:
```markdown
## Acceptance Criteria (BEFORE commit)
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours
- [ ] Error messages display for invalid credentials

## Acceptance Criteria (AFTER commit that implements login)
- [x] User can log in with email/password
- [ ] Session expires after 24 hours
- [ ] Error messages display for invalid credentials
```

### 2. Post Comment on Ticket

**When you have useful information to share**, add a comment to the ticket with:
- Decisions made during implementation
- Useful context for future work
- Trade-offs or limitations
- Anything the reviewer should know

**Example comment**:
```markdown
Implemented JWT validation using Entra OIDC.

Decision: Using 1-hour TTL for JWKS key caching to balance between
performance and security. Shorter TTL would cause excessive API calls
to Microsoft endpoint.

Note: Current implementation validates required claims (iss, aud, exp, nbf)
but does not validate optional claims. This can be added later if needed.
```

### 3. Review All Staged Changes

**Before writing commit message**, review all staged changes to ensure commit message covers everything:

```bash
# Check all staged files and changes
git diff --cached --stat

# Review detailed changes
git diff --cached
```

**Why this is critical**:
- Ensures commit message accurately describes ALL changes, not just recent ones
- Prevents committing unintended changes
- Helps write comprehensive commit messages
- Catches files that shouldn't be committed (secrets, temp files)

**Example**:
```bash
$ git diff --cached --stat
agile-board/references/ticket-workflow.md       | 523 +++++++++++
git-workflow/references/commit-format.md        |  75 ++
project-management/references/story-analysis.md | 574 +++++++++++
9 files changed, 1657 insertions(+)
```

From this output, you know the commit message must cover:
- Ticket workflow documentation (523 lines)
- Commit format updates (75 lines)
- Story analysis workflow (574 lines)
- All 9 files modified

### 4. Commit Message References Story

Always link commits to stories in the footer:

```
feat(auth): implement JWT validation

- Add JWKS key caching with 1-hour TTL
- Validate required claims (iss, aud, exp, nbf)
- Extract user identity and authorisation context

Implements Story 1.4a
```

**Workflow summary**:
1. ✅ Mark ACs as done on ticket (check boxes)
2. ✅ Post comment with useful decisions/context (when relevant)
3. ✅ Review all staged changes (`git diff --cached --stat`)
4. ✅ Create commit with story reference covering ALL changes
5. ❌ DON'T modify AC text

## Commit Message Template

Save this to `.gitmessage` for easy access:

```
# <type>(<scope>): <description>
#
# [optional body]
#
# [optional footer]
#
# Type: feat, fix, docs, style, refactor, perf, test, chore
# Scope: api, auth, retrieval, embeddings, pipeline, story-X.Y
#
# Rules:
# - Use Australian English (normalise, organisation, authorisation)
# - Use imperative mood ("add" not "added")
# - Limit description to 50 characters
# - Wrap body at 72 characters
# - NO AI attribution (Co-Authored-By: Claude)
# - Reference story in footer (Implements Story X.Y)
# - Mark ACs as done on ticket BEFORE committing
# - Post comment on ticket with useful decisions/context (when relevant)
# - Review ALL staged changes (git diff --cached --stat) before writing message
```

Set as default:
```bash
git config commit.template ~/.gitmessage
```

## Viewing Commit History

```bash
# Recent commits
git log --oneline -10

# Commits with full messages
git log -5

# Commits on current branch since develop
git log develop..HEAD

# Commits by author
git log --author="Your Name" --oneline

# Commits for specific file
git log --oneline -- src/file.py
```

## Amending Commits

**CRITICAL**: Only amend commits that have NOT been pushed:

```bash
# Safe: Amend last commit (not pushed yet)
git commit --amend

# Safe: Amend with new message
git commit --amend -m "new message"

# UNSAFE: Amending after push requires force push
git commit --amend
git push --force  # ❌ Dangerous! Avoid!
```

**Better approach**: Create a new commit instead:
```bash
# Fix mistake in previous commit
git add forgotten_file.py
git commit -m "fix(scope): add forgotten file to previous commit"
```

## Pre-commit Hook Failures

**CRITICAL**: When pre-commit hooks fail, create a NEW commit (don't amend):

```bash
# ❌ WRONG - Hook failed, amending would modify PREVIOUS commit
git commit --amend

# ✅ CORRECT - Fix issue and create NEW commit
black src/  # Fix the issue
git add src/
git commit -m "style: fix formatting issues from pre-commit hook"
```

**Why**: After hook failure, the commit did NOT happen — so `--amend` would modify the PREVIOUS commit, potentially destroying work.
