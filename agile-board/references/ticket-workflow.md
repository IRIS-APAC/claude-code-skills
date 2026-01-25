# Ticket Update Workflow

This document describes the workflow for updating stories/tickets throughout the development lifecycle.

## Overview

Tickets should be updated at specific points in the development process:
1. **Start work** - Move ticket to "In Progress" pipeline
2. **On commit** - Mark ACs as done (only if actually completed), post comments with decisions
3. **On PR creation** - Check AC completion, update story description, move to "Review/QA" pipeline
4. **On PR review** - Verify all ACs have implementation and tests
5. **On PR approval and merge** - Move ticket to "Done" pipeline
6. **On PR rejection** - Move ticket back to "In Progress" pipeline

## 0. Before Starting Work: Move to In Progress

**When**: When you start working on a story (during analysis phase, before any commits)

**Action**: Move the ticket to the "In Progress" pipeline (or equivalent column on your board)

**Why**:
- Makes it visible that work has started
- Prevents duplicate work by other team members
- Provides accurate sprint progress tracking

**ZenHub example** (using MCP tool):
- Use `mcp__zenhub__moveIssueToPipeline` with the issue ID and pipeline ID
- Pipeline IDs are stored in your board config (`.claude/agile-board-config.json`)

**Jira example** (using MCP tool):
- Use Atlassian Rovo MCP Server or compatible Jira MCP implementation
- Transition issue using `transitionIssue` with issue key and transition ID
- Transition IDs vary by Jira workflow configuration
- Check your board config for workflow transition mappings

**Common pipeline names**:
- "In Progress" (most common)
- "In Development"
- "Active"
- "Working"

## 1. On Commit: Mark ACs and Post Comments

### Mark Acceptance Criteria as Done

**When**: After every commit that completes work toward an AC

**How**:
1. Open the story/ticket on your board (GitHub, ZenHub, Jira, etc.)
2. Review the acceptance criteria checkboxes
3. Mark completed ACs as done (check the box)
4. **NEVER modify the AC text** - only check/uncheck boxes

**Example**:
```markdown
## Before commit
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours

## After implementing login
- [x] User can log in with email/password
- [ ] Session expires after 24 hours
```

### Post Comment with Implementation Details

**When**: When you have useful information to share (decisions, context, trade-offs)

**What to include**:
- Decisions made during implementation
- Useful context for future work
- Trade-offs or limitations
- Anything the reviewer or team should know

**Example comment**:
```markdown
Implemented JWT validation using Entra OIDC.

**Decision**: Using 1-hour TTL for JWKS key caching to balance between
performance and security. Shorter TTL would cause excessive API calls
to Microsoft endpoint (~200ms per call).

**Note**: Current implementation validates required claims (iss, aud, exp, nbf)
but does not validate optional claims. This can be added later if needed.

**Trade-off**: Caching introduces potential 1-hour delay for key rotation,
but this is acceptable given Entra's key rotation policy (monthly).
```

**Why post comments**:
- Creates a permanent record of decisions
- Helps reviewers understand the implementation
- Provides context for future developers
- Documents trade-offs and limitations

## 2. On PR Creation: Check ACs and Update Story Description

### Check Acceptance Criteria Completion

**Before creating PR**, review all ACs:

**If all ACs are complete**:
- ✅ All checkboxes should be checked
- ✅ Proceed with PR creation

**If ACs are intentionally incomplete**:
1. Update the story description (NOT a comment)
2. Change the deferred AC to ~~strikethrough~~
3. Add *italic justification* on the same line explaining why
4. Create a new ticket for the deferred work
5. Link the new ticket in the justification

**Example of deferred AC**:
```markdown
## Acceptance Criteria
- [x] User can log in with email/password
- [x] Session expires after 24 hours
- ~~[ ] Error messages display for invalid credentials~~ *Deferred to Story 1.5 - requires UX design review and accessibility audit*
- [x] Login attempts are logged for security monitoring
```

**Then create or update the deferred work story** (e.g., Story 1.5):
- Title: "Add error messages for invalid login credentials"
- Description: Include the deferred AC and context from Story 1.4
- Link to Story 1.4 in the description
- DO NOT mark the deferred story as complete

### Update Story Description with Implementation Details

**Append an "Implementation" section** to the story description (NOT a comment):

**Template**:
```markdown
## Implementation

**Approach**: [Brief description of implementation approach]

**Key decisions**:
- [Decision 1 with rationale]
- [Decision 2 with rationale]
- [Decision 3 with rationale]

**Testing**:
- Unit tests: [count/count passing]
- Integration tests: [count/count passing]
- Manual testing: [description of manual tests performed]

**Performance** (if applicable):
- [Metric 1]: [value]
- [Metric 2]: [value]

**Known limitations** (if any):
- [Limitation 1]
- [Limitation 2]

**Verified**:
- [x] All acceptance criteria implemented (or deferred with justification)
- [x] Tests passing with >80% coverage
- [x] Manual testing completed
- [x] Security review (no hardcoded secrets)
- [x] Australian English spelling throughout
```

**Example**:
```markdown
## Implementation

**Approach**: Implemented JWT validation using Entra OIDC with JWKS key caching.

**Key decisions**:
- Using 1-hour TTL for JWKS key caching (balances performance vs security)
- Validating required claims only (iss, aud, exp, nbf) - optional claims deferred to Story 1.5
- Using `pyjwt` library instead of manual JWT parsing (industry standard, well-tested)

**Testing**:
- Unit tests: 42/42 passing
- Integration tests: 12/12 passing
- Manual testing: Verified with test Entra app (client ID: abc123), tested token expiry, invalid tokens

**Performance**:
- JWT validation: <5ms average
- JWKS fetch (cache miss): ~200ms (acceptable for hourly rotation)
- JWKS fetch (cache hit): <1ms

**Known limitations**:
- Optional JWT claims are not validated (deferred to Story 1.5)
- Cache invalidation requires service restart (acceptable given 1-hour TTL)

**Verified**:
- [x] All acceptance criteria implemented (error messages deferred to Story 1.5)
- [x] Tests passing with 94% coverage
- [x] Manual testing completed with test Entra app
- [x] Security review (API key in environment variable, no secrets in logs)
- [x] Australian English spelling throughout
```

**Why append to description instead of comment**:
- Reviewer sees everything in one place
- No need to scroll through comments
- Permanent record attached to the story
- Clear separation between story definition and implementation

### Verify Before Creating PR

**Checklist**:
- ✅ All completed ACs are checked on the ticket
- ✅ Deferred ACs have ~~strikethrough~~ + *italic justification* + new ticket created
- ✅ Implementation section added to story description
- ✅ All commits have story reference in footer (e.g., "Implements Story 1.4")
- ✅ Comments posted on ticket with key decisions

### Move Ticket to Review/QA Pipeline

**After creating PR**, move the ticket to the "Review/QA" pipeline (or equivalent column):

**Why**:
- Indicates code is ready for review
- Tracks work-in-review vs work-in-progress
- Provides visibility into review queue

**ZenHub example** (using MCP tool):
- Use `mcp__zenhub__moveIssueToPipeline` with the issue ID and "Review/QA" pipeline ID
- Pipeline IDs are stored in your board config (`.claude/agile-board-config.json`)

**Jira example** (using MCP tool):
- Use Atlassian Rovo MCP Server or compatible Jira MCP implementation
- Transition issue to review status using `transitionIssue` with issue key and "In Review" transition ID
- Transition IDs vary by Jira workflow configuration
- Check your board config for workflow transition mappings

**Common pipeline names**:
- "Review/QA" (most common)
- "In Review"
- "Code Review"
- "Testing"
- "QA"

**Timing**: Move the ticket immediately after creating the PR, not before.

## 3. On PR Review: Verify ACs Have Implementation and Tests

### Reviewer Responsibilities

**CRITICAL**: Reviewers must verify acceptance criteria BEFORE reviewing code.

**AC Verification Checklist**:
- [ ] **All ACs have implementation** - Each AC has corresponding code changes
- [ ] **All ACs have tests** - Both unit and integration tests for each AC
- [ ] **Deferred ACs properly documented**:
  - ~~Strikethrough~~ format with *italic justification*
  - New ticket created for deferred work
  - New ticket is NOT completed yet
- [ ] **Implementation section exists** - Story description has complete implementation details

**Example verification**:

Story has:
```markdown
## Acceptance Criteria
- [x] User can log in with email/password
- [x] Session expires after 24 hours
- ~~[ ] Error messages display for invalid credentials~~ *Deferred to Story 1.5 - requires UX design review*
```

Reviewer checks:
1. ✅ AC 1 (Login):
   - Implementation: `auth.py:42-78`, `session.py:15-32`
   - Unit tests: `test_auth.py:15-32` (8 tests)
   - Integration tests: `test_auth_integration.py:10-45` (3 tests)
2. ✅ AC 2 (Session expiry):
   - Implementation: `session.py:23-45`, `middleware.py:67-89`
   - Unit tests: `test_session.py:8-19` (4 tests)
   - Integration tests: `test_session_integration.py:12-34` (2 tests)
3. ✅ AC 3 (Deferred):
   - Story 1.5 exists: ✅
   - Story 1.5 NOT completed: ✅
   - Story 1.5 has error messages work: ✅

### Request Changes If Issues Found

**If deferred ACs don't have a ticket**:
```bash
gh pr review 42 --request-changes -b "Deferred AC 'Error messages display for invalid credentials' needs a ticket.

Please create Story 1.5 for this work and link it in the AC justification."
```

**If ACs missing tests**:
```bash
gh pr review 42 --request-changes -b "AC 'Session expires after 24 hours' has implementation but no integration tests.

Please add integration test verifying:
- Session expires after exactly 24 hours
- User redirected to login after expiry
- Expired session cannot be reused"
```

**If Implementation section missing**:
```bash
gh pr review 42 --request-changes -b "Story description is missing Implementation section.

Please append Implementation section to story description with:
- Implementation approach and key decisions
- Testing results (unit, integration, manual)
- Performance metrics
- Known limitations"
```

**When changes are requested**, move ticket back to "In Progress" pipeline (see section 5 below).

## 4. On PR Rejection: Move Back to In Progress

**When**: PR review requests changes

**Action**: Move the ticket back to the "In Progress" pipeline

**Why**:
- Indicates work is not complete and needs more development
- Removes it from the review queue
- Accurately reflects current state

**ZenHub example** (using MCP tool):
- Use `mcp__zenhub__moveIssueToPipeline` with the issue ID and "In Progress" pipeline ID
- Pipeline IDs are stored in your board config (`.claude/agile-board-config.json`)

**Jira example** (using MCP tool):
- Use Atlassian Rovo MCP Server or compatible Jira MCP implementation
- Transition issue back to in-progress status using `transitionIssue` with issue key and "In Progress" transition ID
- Transition IDs vary by Jira workflow configuration
- Check your board config for workflow transition mappings

**Then**:
1. Address the requested changes
2. Push new commits to the PR branch
3. Post comment on PR indicating changes are ready for re-review
4. Move ticket back to "Review/QA" pipeline once ready

## 5. On PR Approval and Merge: Move to Done

**When**: PR is approved and merged

**Action**: Move the ticket to the "Done" pipeline

**Why**:
- Marks work as complete
- Tracks completed work for sprint velocity
- Provides accurate sprint burndown

**ZenHub example** (using MCP tool):
- Use `mcp__zenhub__moveIssueToPipeline` with the issue ID and "Done" pipeline ID
- Pipeline IDs are stored in your board config (`.claude/agile-board-config.json`)

**Jira example** (using MCP tool):
- Use Atlassian Rovo MCP Server or compatible Jira MCP implementation
- Transition issue to done status using `transitionIssue` with issue key and "Done" transition ID
- May also need to set resolution (e.g., "Done", "Fixed", "Completed")
- Transition IDs vary by Jira workflow configuration
- Check your board config for workflow transition mappings

**Common "Done" pipeline names**:
- "Done" (most common)
- "Closed"
- "Complete"
- "Deployed"
- "Released"

**Timing**: Move the ticket immediately after merging the PR.

**Note**: Some boards (like ZenHub) may auto-close the issue when the PR is merged. Verify the ticket is in the correct "Done" pipeline.

## Board-Specific Tools

### ZenHub

**Mark ACs as done**:
- Open issue on GitHub
- Check the checkbox in the description

**Post comment**:
```bash
gh issue comment 42 -b "Implemented JWT validation using Entra OIDC.

Decision: Using 1-hour TTL for JWKS key caching..."
```

**Update story description**:
```bash
gh issue edit 42 --body "$(cat <<'EOF'
[Original story description]

## Implementation

**Approach**: Implemented JWT validation using Entra OIDC...
EOF
)"
```

**Create deferred work ticket**:
```bash
gh issue create \
  --title "Add error messages for invalid login credentials" \
  --body "Deferred from Story 1.4.

Requires UX design review and accessibility audit before implementation.

## Acceptance Criteria
- [ ] Error messages display for invalid credentials
- [ ] Messages are accessible (ARIA labels)
- [ ] Messages follow UX style guide

Relates to Story 1.4"
```

### Jira

**Mark ACs as done**:
- Open issue in Jira web UI
- Check the checkbox in the description
- Or use Atlassian Rovo MCP Server to update issue description

**Post comment**:
- Use Atlassian Rovo MCP Server `addComment` function with issue key and comment text
- Or use Jira REST API: `POST /rest/api/3/issue/{issueIdOrKey}/comment`

**Update story description**:
- Use Atlassian Rovo MCP Server `updateIssue` function
- Append Implementation section to description field
- Or use Jira REST API: `PUT /rest/api/3/issue/{issueIdOrKey}`

**Create deferred work ticket**:
- Use Atlassian Rovo MCP Server `createIssue` function
- Specify project key, issue type, summary, description
- Link to original story using `issuelinks` field
- Or use Jira REST API: `POST /rest/api/3/issue`

**Move issue between statuses**:
- Use Atlassian Rovo MCP Server `transitionIssue` function with issue key and transition ID
- Transition IDs vary by Jira workflow (check workflow configuration)
- Common transitions: "In Progress", "In Review", "Done"

### Linear (Planned)

Similar workflow using Linear GraphQL API or `linear` CLI tool.

## Common Mistakes

### ❌ Wrong: Modifying AC Text

```markdown
## Before
- [ ] User can log in with email/password

## After (WRONG!)
- [x] User can log in with email/password via JWT
```

**Why wrong**: Changes the original requirement, makes it unclear what was originally agreed

**Correct**: Only check the box, don't modify text

### ❌ Wrong: Deferred AC Without Justification

```markdown
- ~~[ ] Error messages display for invalid credentials~~
```

**Why wrong**: No explanation of why deferred, no link to new ticket

**Correct**:
```markdown
- ~~[ ] Error messages display for invalid credentials~~ *Deferred to Story 1.5 - requires UX design review*
```

### ❌ Wrong: Implementation Details in Comment

**Why wrong**: Reviewer has to scroll through comments to find implementation details

**Correct**: Append Implementation section to story description

### ❌ Wrong: Deferred Work in Completed Ticket

**Why wrong**: Deferred work gets lost if it's in a completed ticket

**Correct**: Create new ticket for deferred work, keep it NOT completed

### ❌ Wrong: No Tests for AC

**Why wrong**: Can't verify AC is actually implemented correctly

**Correct**: Each AC must have both unit and integration tests

## Summary

**Before starting work**:
1. Move ticket to "In Progress" pipeline

**On commit**:
1. Mark ACs as done (check boxes only, don't modify text)
2. Post comment with useful decisions and context (when relevant)

**On PR creation**:
1. Check all ACs are complete (or properly deferred)
2. Defer ACs: ~~strikethrough~~ + *italic justification* + new ticket
3. Append Implementation section to story description
4. Verify all commits reference the story
5. **Move ticket to "Review/QA" pipeline**

**On PR review**:
1. Verify all ACs have implementation
2. Verify all ACs have tests (unit + integration)
3. Verify deferred ACs have new tickets (not completed)
4. Verify Implementation section exists in story description

**On PR rejection (changes requested)**:
1. **Move ticket back to "In Progress" pipeline**
2. Address requested changes
3. Push new commits
4. Move ticket back to "Review/QA" when ready for re-review

**On PR approval and merge**:
1. **Move ticket to "Done" pipeline**

**Result**: Clear audit trail of what was implemented, why decisions were made, what was deferred, and accurate board state throughout the development lifecycle.
