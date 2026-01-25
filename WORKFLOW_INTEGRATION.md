# Workflow Integration Guide

This document shows how all 5 skills work together throughout the complete development lifecycle.

## Skills Overview

| Skill | Purpose | Role in Workflow |
|-------|---------|------------------|
| **project-management** | Story creation, estimation, sprint planning | Primary - Planning phase |
| **developer-analysis** | Pre-implementation analysis, POC scripts, design proposals | Primary - Analysis phase |
| **agile-board** | Board operations (create issues, move pipelines, set fields) | Primary - Planning & Tracking |
| **git-workflow** | Commits, branches, pull requests, code review, **implementation** | Primary - Implementation, PR, Review, Merge |
| **testing** | Test strategy patterns, coverage targets, quality guidance | **Reference** - Used by developer-analysis & git-workflow |

**Key distinction**:
- **Primary skills** drive workflow phases
- **Reference skill (testing)** provides guidance used by other skills

## Complete Development Workflow

### Phase 1: Planning (project-management + agile-board)

**Objective**: Define what to build with clear acceptance criteria and estimates.

1. **Create Epic** (if needed)
   - Use: `project-management` skill for epic breakdown
   - Reference: `project-management/references/epic-planning.md`
   - Map dependencies between stories

2. **Write User Story**
   - Use: `project-management` skill for story templates
   - Reference: `project-management/references/story-templates.md`
   - Include:
     - Description (what and why)
     - Acceptance criteria (checkbox format)
     - Technical notes
     - Testing strategy outline

3. **Estimate Story**
   - Use: `project-management` skill for T-shirt sizing
   - Reference: `project-management/references/estimation-guide.md`
   - T-shirt sizes: XS=1, S=3, M=5, L=8, XL=13
   - Break down L/XL stories into smaller chunks

4. **Create Issue on Board**
   - Use: `agile-board` skill for board-specific implementation
   - Reference: Board-specific file (e.g., `agile-board/references/zenhub.md`)
   - Set: estimate, labels, epic link, pipeline

5. **Add to Sprint**
   - Use: `project-management` skill for sprint planning
   - Reference: `project-management/references/sprint-workflows.md`
   - Verify Definition of Ready
   - Check team velocity and capacity

**Outputs**:
- ✅ Story with clear ACs in sprint backlog
- ✅ Story points set on board
- ✅ Linked to parent epic
- ✅ Sprint commitment within velocity

---

### Phase 2: Analysis (developer-analysis)

**Objective**: Understand requirements, validate integrations, propose design before coding.

**Note**: This phase *references* the testing skill when planning test strategy.

1. **Read Story Thoroughly**
   - Use: `developer-analysis` skill
   - Reference: `developer-analysis/references/story-analysis.md`
   - Read: ACs, comments, technical notes, linked docs

2. **Challenge Assumptions**
   - Use: `developer-analysis` skill (Critical Rules section)
   - Question: vague requirements, missing constraints, edge cases
   - Clarify: with user via comments or questions

3. **Check Architecture Alignment**
   - Use: `developer-analysis` skill
   - Review: `/docs/architecture/`, ADRs, existing patterns
   - Identify: conflicts or needed updates

4. **Create POC Script** (if third-party integration)
   - Use: `developer-analysis` skill
   - Store in: `scripts/poc/`
   - Validate: API works, authentication succeeds, integration feasible
   - Document: findings in `scripts/poc/README.md`

5. **Plan Testing Strategy**
   - Use: `developer-analysis` skill
   - Reference: `testing/references/test-strategy.md` for patterns
   - Define in design proposal:
     - Test layers needed (unit 60%, integration 30%, E2E 10%)
     - Coverage targets (80% min, 90% target)
     - Mock strategy for external dependencies (Mockoon for APIs)
     - Key test scenarios (happy path, edge cases, errors)

6. **Propose Design**
   - Use: `developer-analysis` skill
   - Post as comment on story ticket
   - Include:
     - High-level approach
     - Key technical decisions
     - POC findings (if applicable)
     - Component breakdown
     - Configuration needed (.env, YAML)
     - Testing strategy
     - Trade-offs considered

7. **Wait for Approval**
   - User reviews design proposal
   - Clarifications or changes requested
   - Final approval to proceed

**Outputs**:
- ✅ Requirements clarified and validated
- ✅ POC script proves integration works (if applicable)
- ✅ Design approved by user
- ✅ Testing strategy documented
- ✅ Configuration plan defined

---

### Phase 3: Implementation (git-workflow + agile-board)

**Objective**: Write code, tests, and commit changes with proper workflow.

**Note**: git-workflow covers implementation INCLUDING writing tests. References testing skill for coverage targets and quality patterns.

1. **Move Story to "In Progress"**
   - Use: `agile-board` skill
   - Move issue to "In Progress" pipeline

2. **Create Feature Branch**
   - Use: `git-workflow` skill
   - Reference: `git-workflow/references/branch-naming.md`
   - Format: `feature/epic-X-story-Y.Z-description`
   - Start from: `develop` (NOT main)

3. **Write Tests First** (TDD recommended)
   - Use: `git-workflow` skill
   - Reference: `testing/references/test-strategy.md` for patterns
   - Test for each AC (unit + integration)
   - Test edge cases and error scenarios
   - Run tests: should fail initially (Red)

4. **Implement Code**
   - Use: `git-workflow` skill
   - Follow: approved design proposal (from developer-analysis)
   - Use: POC script as reference (if created)
   - Apply: modular design, dependency injection, configuration
   - Add: Australian English comments/docs

5. **Write Tests** (if not using TDD)
   - Use: `git-workflow` skill
   - Reference: `testing/references/test-strategy.md` for patterns
   - Test all ACs (unit + integration)
   - Test edge cases and errors
   - Aim for: 90%+ coverage

6. **Run Tests Locally**
   - Use: `git-workflow` skill
   - Reference: `testing/references/coverage-guide.md` for targets
   - Run: test suite with coverage
   - Verify: >80% coverage (90%+ target)
   - Verify: all tests pass
   - Capture: test output for PR

7. **Commit Changes**
   - Use: `git-workflow` skill
   - Reference: `git-workflow/references/commit-format.md`
   - Format: `type(scope): description`
   - Include: detailed explanation, "Relates to Story X.Y"
   - Stage: specific files (NOT `git add .`)

8. **Mark ACs Complete** (as implemented)
   - Use: `agile-board` skill
   - Reference: `agile-board/references/ticket-workflow.md`
   - Update: checkboxes in story description
   - Add: commit references

**Outputs**:
- ✅ Code implemented following approved design
- ✅ Tests written for all ACs (>80% coverage)
- ✅ Commits following conventional format
- ✅ ACs marked complete on story ticket
- ✅ Australian English used throughout

---

### Phase 4: Pull Request (git-workflow)

**Objective**: Create PR with comprehensive description and test results for review.

**Note**: Test results from Phase 3 are included in PR description.

1. **Push Branch**
   - Use: `git-workflow` skill
   - Command: `git push -u origin feature/...`

2. **Create Pull Request**
   - Use: `git-workflow` skill
   - Reference: `git-workflow/references/pr-template.md`
   - Target: `develop` (CRITICAL - NOT main)
   - Include:
     - Summary (1-2 sentences)
     - Story/Issue reference
     - Changes (bullet list)
     - Test results (paste output + coverage)
     - Checklist (tests pass, coverage >80%, Australian English, etc.)

3. **Verify PR Target Branch**
   - Use: `git-workflow` skill
   - Command: `gh pr view --json baseRefName`
   - Expected: `"baseRefName": "develop"`

4. **Update Story Ticket**
   - Use: `agile-board` skill
   - Reference: `agile-board/references/ticket-workflow.md`
   - Add: PR link to story comments
   - Move: to "Review" or "QA" pipeline

**Outputs**:
- ✅ PR created targeting `develop`
- ✅ PR description includes test results and coverage
- ✅ Story ticket updated with PR link
- ✅ Story moved to Review pipeline

---

### Phase 5: Code Review (git-workflow + project-management)

**Objective**: Verify code quality, test coverage, and AC completion.

**Note**: git-workflow references testing skill for coverage analysis and quality standards during review.

1. **Review Code Quality**
   - Use: `git-workflow` skill
   - Reference: `git-workflow/references/pr-review.md`
   - Check:
     - Code follows design proposal
     - Australian English used
     - Type safety/strong typing
     - Error handling
     - No hardcoded secrets
     - Modular, reusable code

2. **Verify Acceptance Criteria**
   - Use: `project-management` skill
   - Check: All ACs marked complete
   - Verify: Each AC has corresponding tests
   - Test: functionality matches ACs

3. **Review Test Quality**
   - Use: `git-workflow` skill
   - Reference: `testing/references/coverage-guide.md` for standards
   - Check:
     - Coverage ≥80% (aim for 90%+)
     - Tests verify behaviour (not implementation)
     - Edge cases and errors tested
     - Test names are descriptive
     - Tests are independent

4. **Check Security**
   - Use: `developer-analysis` skill (security checklist)
   - Verify: input validation, auth/authz, no XSS/injection
   - Check: secrets management, rate limiting

5. **Approve or Request Changes**
   - Use: `git-workflow` skill
   - Approve: `gh pr review 42 --approve -b "LGTM..."`
   - Changes: `gh pr review 42 --request-changes -b "Please..."`

**Outputs**:
- ✅ Code quality verified
- ✅ All ACs tested and working
- ✅ Coverage ≥80%
- ✅ Security concerns addressed
- ✅ PR approved or changes requested

---

### Phase 6: Merge & Deploy (git-workflow + agile-board)

**Objective**: Merge code and close story.

1. **Verify Approvals**
   - Use: `git-workflow` skill
   - Check: PR approved by required reviewers
   - Check: CI/CD tests pass

2. **Merge Pull Request**
   - Use: `git-workflow` skill
   - CRITICAL: Use merge commit (NOT squash/rebase)
   - Command: `gh pr merge 42 --merge --delete-branch`
   - Preserves: full commit history

3. **Close Story**
   - Use: `agile-board` skill
   - Move: to "Done" pipeline
   - Verify: all ACs checked
   - Add: final comment with PR link

4. **Update Epic Progress**
   - Use: `project-management` skill
   - Track: story points completed
   - Update: epic burndown

**Outputs**:
- ✅ Code merged to `develop`
- ✅ Feature branch deleted
- ✅ Story marked Done
- ✅ Epic progress updated

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: PLANNING                                           │
│ Primary Skills: project-management + agile-board            │
├─────────────────────────────────────────────────────────────┤
│ 1. Write story (ACs, estimates) → project-management       │
│ 2. Create issue on board → agile-board                     │
│ 3. Add to sprint → project-management                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: ANALYSIS                                           │
│ Primary Skill: developer-analysis                           │
│ References: testing (for test strategy patterns)            │
├─────────────────────────────────────────────────────────────┤
│ 1. Read story, challenge assumptions → developer-analysis  │
│ 2. Create POC script (if needed) → developer-analysis      │
│ 3. Plan testing strategy → developer-analysis              │
│    (references testing skill for patterns)                  │
│ 4. Propose design → developer-analysis                     │
│ 5. Get approval from user                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: IMPLEMENTATION                                     │
│ Primary Skills: git-workflow + agile-board                  │
│ References: testing (for coverage targets, quality)         │
├─────────────────────────────────────────────────────────────┤
│ 1. Move story to "In Progress" → agile-board               │
│ 2. Create feature branch → git-workflow                    │
│ 3. Write tests + code → git-workflow                       │
│    (references testing skill for patterns)                  │
│ 4. Commit changes → git-workflow                           │
│ 5. Mark ACs complete → agile-board                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: PULL REQUEST                                       │
│ Primary Skills: git-workflow + agile-board                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Push branch → git-workflow                              │
│ 2. Create PR (w/ test results) → git-workflow              │
│ 3. Update story with PR link → agile-board                 │
│ 4. Move to Review pipeline → agile-board                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: CODE REVIEW                                        │
│ Primary Skills: git-workflow + project-management           │
│ References: testing (for coverage standards)                │
├─────────────────────────────────────────────────────────────┤
│ 1. Review code quality → git-workflow                      │
│ 2. Verify ACs complete → project-management                │
│ 3. Check test coverage → git-workflow                      │
│    (references testing skill for standards)                 │
│ 4. Approve or request changes → git-workflow               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 6: MERGE & DEPLOY                                     │
│ Primary Skills: git-workflow + agile-board                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Merge PR (merge commit) → git-workflow                  │
│ 2. Close story → agile-board                               │
│ 3. Update epic progress → project-management               │
└─────────────────────────────────────────────────────────────┘
```

## Skill Interaction Examples

### Example 1: New Feature Story

**Scenario**: Add user authentication

**Phase 1 - Planning**:
```
project-management: Write story with ACs (login, logout, session mgmt)
project-management: Estimate as M (5 points)
agile-board: Create GitHub issue with estimate=5
agile-board: Link to Epic 2 (User Management)
project-management: Add to Sprint 3
```

**Phase 2 - Analysis**:
```
developer-analysis: Challenge - "What about password reset? MFA? Session timeout?"
developer-analysis: Create POC for Auth0 integration (scripts/poc/auth0_test.py)
developer-analysis: Plan strategy - unit tests for services, integration for API, E2E for flows
                    (references testing/references/test-strategy.md)
developer-analysis: Propose design - Auth0 integration, JWT tokens, Redis sessions
[User approves design]
```

**Phase 3 - Implementation**:
```
agile-board: Move issue to "In Progress"
git-workflow: Create branch feature/epic-2-story-2.1-auth
git-workflow: Write tests for auth service (test_auth_service.py)
              (references testing skill for patterns)
git-workflow: Implement auth service following POC from developer-analysis
git-workflow: Commit "feat(auth): implement user authentication with Auth0"
agile-board: Mark AC checkboxes complete
```

**Phase 4 - Pull Request**:
```
git-workflow: Push branch
git-workflow: Create PR with test results (Coverage: 92%)
agile-board: Update story with PR link
agile-board: Move to "Review" pipeline
```

**Phase 5 - Review**:
```
git-workflow: Review code quality (Australian English, type hints, error handling)
project-management: Verify all ACs tested (login, logout, session mgmt)
git-workflow: Check coverage 92% > 80% ✓ (references testing/references/coverage-guide.md)
git-workflow: Approve PR
```

**Phase 6 - Merge**:
```
git-workflow: Merge PR with merge commit
agile-board: Move to "Done"
project-management: Update Epic 2 burndown (5 points completed)
```

### Example 2: Bug Fix Story

**Scenario**: Fix search returning duplicates

**Phase 1 - Planning**:
```
project-management: Write bug story with reproduction steps
project-management: Estimate as S (3 points) - isolated fix
agile-board: Create issue, label "bug"
project-management: Add to current sprint (high priority)
```

**Phase 2 - Analysis**:
```
developer-analysis: Investigate root cause in search service
developer-analysis: Identify missing DISTINCT clause in query
developer-analysis: Plan regression test to prevent recurrence
                    (references testing/references/test-strategy.md)
developer-analysis: Propose fix - add DISTINCT + test
[User approves]
```

**Phase 3 - Implementation**:
```
git-workflow: Create branch bugfix/epic-1-story-1.5-duplicate-results
git-workflow: Write regression test (test_search_returns_unique_results)
git-workflow: Apply fix (add DISTINCT to SQL query)
git-workflow: Verify test passes
git-workflow: Commit "fix(search): prevent duplicate results in query"
agile-board: Mark AC complete ("Returns unique results")
```

**Phases 4-6**: Same as Example 1

---

## Cross-Skill Dependencies

### Primary Skills (workflow actors)

**developer-analysis** depends on:
- **project-management**: Story ACs for requirements
- **testing** (reference): Test strategy patterns and coverage targets

**git-workflow** depends on:
- **project-management**: ACs for PR verification and implementation guidance
- **developer-analysis**: Design proposal to follow during implementation
- **testing** (reference): Coverage targets, quality patterns, test organization

**agile-board** depends on:
- **project-management**: Story content, estimates, templates

**project-management** depends on:
- **developer-analysis**: Design feedback for feasibility
- **agile-board**: Board-specific fields and limitations

### Reference Skill

**testing** (reference skill):
- Does NOT actively participate in workflow
- Provides guidance referenced by developer-analysis and git-workflow
- Contains patterns, standards, and best practices

---

## Quick Reference: When to Use Which Skill

| Task | Primary Skill | References |
|------|---------------|------------|
| Create user story | project-management | - |
| Estimate complexity | project-management | - |
| Create issue on board | agile-board | project-management |
| Analyse requirements | developer-analysis | - |
| Create POC script | developer-analysis | - |
| Propose design | developer-analysis | testing (patterns) |
| Plan test strategy | developer-analysis | testing (patterns) |
| Create branch | git-workflow | - |
| Write tests | git-workflow | testing (patterns) |
| Implement code | git-workflow | developer-analysis (design) |
| Commit changes | git-workflow | - |
| Create PR | git-workflow | - |
| Review PR | git-workflow | testing (standards), project-management (ACs) |
| Check coverage | git-workflow | testing (targets) |
| Merge PR | git-workflow | - |
| Update story status | agile-board | - |

---

## Australian English Throughout

All skills enforce **Australian English spelling** as a project-wide standard:

- ✅ normalise, organisation, authorisation, behaviour, colour, analyse
- ❌ normalize, organization, authorization, behavior, color, analyze

This applies to:
- Story titles and descriptions
- Commit messages
- PR titles and descriptions
- Code comments and documentation
- Test names
- All written communication

---

## Summary

The 5 skills form a **complete development workflow**:

### Primary Skills (workflow actors)

1. **project-management** - Define what to build (Planning)
2. **developer-analysis** - Validate and design before coding (Analysis)
3. **git-workflow** - Implement (code + tests), create PRs, review, merge (Implementation & Review)
4. **agile-board** - Track progress on project boards (Planning & Tracking)

### Reference Skill (guidance)

5. **testing** - Quality and coverage standards (Referenced by developer-analysis and git-workflow)

**How they work together**:
- **Primary skills** actively drive the workflow phases
- **Reference skill (testing)** provides patterns and standards used by other skills
- Each skill has a specific role and references others throughout the lifecycle

This ensures:
- Clear requirements before implementation
- Validated integrations with POC scripts
- Approved designs before coding
- High test coverage (>80%) through git-workflow referencing testing skill
- Proper git workflow and code review
- Accurate tracking on project boards

**Key principle**:
- **Primary skills** = workflow actors (do the work)
- **Reference skill** = guidance provider (used by others)
