---
name: project-management
description: "Agile project management workflows for creating tickets, managing sprints, writing acceptance criteria, and setting estimates. Use when: (1) Writing user stories, (2) Creating acceptance criteria, (3) Estimating story points, (4) Sprint planning, (5) Epic planning, (6) Managing story dependencies, (7) Release planning. Works with any agile board (requires agile-board skill for board-specific implementation)."
model: sonnet
---
# Project Management

Board-agnostic agile project management workflows and best practices.

## Overview

This skill provides the **"what" and "how"** of agile project management:

- **What** to put in user stories
- **How** to structure acceptance criteria
- **How** to estimate complexity
- **How** to plan sprints
- **How** to plan epics and releases
- **How** to manage story dependencies

For **"where"** to create stories (ZenHub/Jira/Linear), use the `agile-board` skill.

## Critical Rules

### 1. Acceptance Criteria Format
- ✅ **ALWAYS use checkbox format** for trackability
- ✅ **Make criteria specific and testable** - Focus on "what", not "how"
- ✅ **Include edge cases** and error scenarios
- ❌ **NEVER be vague** ("works well", "is fast")
- ❌ **NEVER use non-checkbox format**

Example:
```markdown
## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours of inactivity
- [ ] Error message displays for invalid credentials
```

### 2. Story Estimation
- ✅ **Use T-shirt sizing**: XS=1, S=3, M=5, L=8, XL=13 points
- ✅ **Break down L/XL stories** into smaller M or S stories
- ✅ **Consider complexity factors**: files modified, new patterns, external dependencies, testing complexity, uncertainty
- ❌ **NEVER estimate epics** directly (points roll up from child stories)
- ❌ **NEVER commit to unrealistic velocity** (use historical average)

### 3. Challenge Assumptions
- ✅ **Question vague requirements** before creating stories
- ✅ **Identify missing acceptance criteria** early
- ✅ **Surface dependencies and blockers** during planning
- ✅ **Point out unrealistic estimates** with data
- ❌ **NEVER accept incomplete requirements** without clarification
- ❌ **NEVER ignore edge cases** in acceptance criteria

### 4. Sprint Planning
- ✅ **Use average velocity** to plan sprint capacity
- ✅ **Verify Definition of Ready** before adding stories to sprint
- ✅ **Identify dependencies** and sequence work accordingly
- ❌ **NEVER overcommit** beyond team's proven velocity
- ❌ **NEVER add unestimated stories** to active sprint

### 5. Definition of Done
Before marking story complete:
- [ ] All acceptance criteria met
- [ ] Tests written and passing (>80% coverage)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to dev/staging environment
- [ ] No known bugs or issues

## Quick Start

### Creating a User Story

1. **Use story template** (see`references/story-templates.md`)
2. **Estimate complexity** using T-shirt sizing (see`references/estimation-guide.md`)
3. **Create on board** using`agile-board` skill

### Estimating Stories

Use T-shirt sizing: **XS=1, S=3, M=5, L=8, XL=13**

See `references/estimation-guide.md` for full complexity factors and examples.

## Model Selection

**Recommended model**: Sonnet (Haiku for simple operations)

**Why Sonnet for most operations**:

- **Story creation** - Requires understanding requirements and context
- **AC writing** - Need to think about testability and completeness
- **T-shirt sizing** - Reasoning about complexity factors
- **Sprint planning** - Capacity calculations and dependency analysis
- **Template application** - Understanding which template fits the need

**When Haiku is appropriate**:

- Simple story point assignments (when size is already determined)
- Copying template content without modification
- Basic CRUD operations on stories

**When Extended Thinking may help**:

- **Epic planning with dependencies** - Complex dependency mapping across stories
- **Release planning** - Multi-epic coordination and sequencing
- **Interface design** - Architectural decisions for API contracts
- **Dependency analysis** - Understanding blocking relationships

**Operations by model**:

- ✅ Sonnet: Story creation, AC writing, estimation, sprint planning
- ✅ Haiku: Simple point assignments, template copying
- ✅ Extended thinking: Complex epic planning, release coordination

## Challenge Assumptions and Requirements

**CRITICAL**: Effective project management requires critical thinking and challenging assumptions during planning.

**Why challenge**:

- Prevents creating stories that don't solve the real problem
- Surfaces missing requirements early
- Identifies unrealistic timelines and estimates
- Ensures acceptance criteria are complete
- Reduces rework from misunderstood business needs

**What to challenge**:

**Vague story requirements**:

```
User: "Add a dashboard for users"
Challenge: "What metrics should the dashboard show? Who are the users (admin, end-user)?
           What's the refresh rate? What filters are needed? Mobile or desktop?"
```

**Missing acceptance criteria**:

```
User: "Story: Implement user authentication"
Challenge: "What about password reset flow? Session timeout? Multi-device support?
           Error messages for invalid credentials? Account lockout policy?"
```

**Unrealistic estimation**:

```
User: "This should be an XS story, right?"
Challenge: "Have we considered the testing complexity? Integration with existing auth?
           Database migrations needed? This seems more like M (5 points)."
```

**Hidden dependencies**:

```
User: "Let's schedule Story 2.3 for this sprint"
Challenge: "Story 2.3 depends on Story 2.1 which isn't complete yet.
           Should we do Story 2.2 first instead, which has no blockers?"
```

**Overly broad epics**:

```
User: "Epic: Improve system performance"
Challenge: "Can we narrow this down? Which part of the system? What's the performance target?
           Is this about latency, throughput, or resource usage? Let's break this into focused epics/stories."
```

**Incomplete sprint planning**:

```
User: "Let's commit to 30 points this sprint"
Challenge: "Our average velocity is 21 points. What makes us confident we can do 30?
           Are we accounting for holidays, meetings, support work?"
```

**Missing edge cases in ACs**:

```
User: "AC: User can upload a file"
Challenge: "What about file size limits? Allowed file types? Virus scanning?
           What happens if upload fails halfway? Network timeout handling?"
```

**How to challenge effectively**:

- ✅ Ask clarifying questions (don't assume)
- ✅ Reference historical velocity and estimates
- ✅ Point out missing acceptance criteria
- ✅ Identify dependencies and blockers early
- ✅ Suggest breaking down large stories
- ❌ Don't accept vague requirements without clarification
- ❌ Don't ignore unrealistic estimates
- ❌ Don't skip edge cases in acceptance criteria

**Example challenge workflow**:

```
1. Review story: "Add search functionality"
2. Identify gaps:
   - What are we searching? (users, products, documents?)
   - What fields are searchable?
   - Exact match or fuzzy search?
   - Pagination for results?
   - Search analytics/logging?
   - Performance requirements?
3. Challenge user with questions
4. Get clarifications
5. Update story with complete requirements and ACs
6. Re-estimate with full understanding
7. Proceed with story approval
```

## Story Structure

### Title Format

```
Story X.Y: Brief description in imperative mood
```

**Examples**:

- ✅`Story 1.3: Implement hybrid search service`
- ✅`Epic 4: AI Caption Generation`
- ❌`Story: Do the search thing` (vague, no number)

### Description Template

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

See `references/story-templates.md` for language-specific examples.

## Acceptance Criteria Best Practices

### Format

**Always use checkbox format** for trackability:

```markdown
## Acceptance Criteria
- [ ] First specific, testable criterion
- [ ] Second criterion with measurable outcome
- [ ] Third criterion addressing edge cases
```

### Writing Good Criteria

**DO**:

- ✅ Be specific and testable
- ✅ Focus on**what**, not**how**
- ✅ Include edge cases and error scenarios
- ✅ Make each criterion independently verifiable

**DON'T**:

- ❌ Be vague ("works well", "is fast")
- ❌ Describe implementation details
- ❌ Include multiple conditions in one bullet
- ❌ Use non-checkbox format

**Examples**:

✅ **Good**:

```markdown
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours of inactivity
- [ ] Error message displays for invalid credentials
- [ ] Password must be at least 8 characters
```

❌ **Bad**:

```markdown
- Login works
- Session management
- Error handling
```

## Estimation

### T-Shirt Sizing

| Size | Points | Complexity   | Time (with AI) |
| ---- | ------ | ------------ | -------------- |
| XS   | 1      | Trivial      | < 2 hours      |
| S    | 3      | Simple       | 2-6 hours      |
| M    | 5      | Moderate     | 1-2 days       |
| L    | 8      | Complex      | 2-4 days       |
| XL   | 13     | Very complex | 4-8 days       |

**Break down L/XL stories** into smaller M or S stories when possible.

See `references/estimation-guide.md` for full complexity factors and checklist.

### Complexity Factors

Consider:

- **Files modified** - How many files/modules affected?
- **New patterns** - Introducing new architectural patterns?
- **External dependencies** - Integrating with external services?
- **Testing complexity** - How many layers need testing?
- **Uncertainty** - How well-defined are requirements?

### When to Re-estimate

- Requirements change significantly
- New technical constraints discovered
- Actual complexity differs from initial estimate
- Dependencies added or removed

## Breaking Down Stories

### Prefer Vertical Slicing

Break by **end-to-end functionality**:

**Example**: "Implement hybrid search"

1. Story 1a: Basic BM25 + vector search (happy path) - M (5)
2. Story 1b: Error handling and edge cases - S (3)
3. Story 1c: Performance optimisation - S (3)
4. Story 1d: Advanced filters - M (5)

**Total**: 16 points across 4 deliverable increments

### Horizontal Slicing (Use Sparingly)

Only when vertical slicing isn't possible:

**Example**: "Set up OpenSearch"

1. Story 1a: Collection setup and access policies - M (5)
2. Story 1b: Index schema definition - S (3)
3. Story 1c: Search pipeline configuration - M (5)

## Epic Planning and Dependencies

See `references/epic-planning.md` for comprehensive guide on:

- Breaking epics into stories
- Managing story dependencies (blockers)
- Release planning across multiple epics
- Cross-project coordination
- Epic velocity and burndown tracking

**Quick overview**:

### Epic Breakdown

1. Review epic requirements and timeline
2. Identify stories using user journey mapping or technical layering
3. Map dependencies between stories
4. Estimate all stories (T-shirt sizing)
5. Sequence stories based on dependencies
6. Allocate stories to sprints
7. Set epic timeline with milestones

### Story Dependencies

- **Track blockers** - Story A blocks Story B
- **Sequence work** - Schedule dependent stories in correct order
- **Cross-epic dependencies** - Coordinate across multiple epics
- **Cross-project dependencies** - Coordinate between teams/projects

**Use board tools** to create dependency relationships (see `agile-board` skill).

## Sprint Planning

See `references/sprint-workflows.md` for detailed workflows.

### Sprint Planning Checklist

- [ ] Review sprint goal
- [ ] Ensure all stories have estimates
- [ ] Verify team capacity (use average velocity)
- [ ] Identify dependencies and blockers
- [ ] Confirm stories meet Definition of Ready

### Definition of Ready

Before adding story to sprint:

- [ ] Story has clear acceptance criteria
- [ ] Story is estimated (with story points)
- [ ] Story has no unresolved blockers
- [ ] Story is sized appropriately (ideally S or M)
- [ ] Technical approach is understood

### Definition of Done

Before marking story complete:

- [ ] All acceptance criteria met
- [ ] Tests written and passing (>80% coverage)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to dev/staging environment
- [ ] No known bugs or issues

## Velocity Tracking

Track completed story points per sprint:

**Example**:

- Sprint 1: 21 points completed
- Sprint 2: 23 points completed
- Sprint 3: 19 points completed
- **Average velocity**: 21 points/sprint

Use average velocity to plan sprint capacity.

## Story Hierarchy

```
Epic (Level 3)
  └── Story/Feature (Level 4)
      └── Sub-task (Level 5) - use sparingly
```

**Guidelines**:

- **Epics** - High-level feature areas (don't estimate epics, points roll up from children)
- **Stories** - User-facing functionality (estimate with story points)
- **Sub-tasks** - Only for breaking down complex stories (estimate individually)

## Common Patterns

### Feature Story

**Focus**: End-user functionality

```markdown
## Description
As a [user type], I want to [action] so that [benefit].

## Context
Current system doesn't support [X]. Users need this to [Y].

## Acceptance Criteria
- [ ] User can [action]
- [ ] System validates [conditions]
- [ ] Error messages display for [edge cases]

## Technical Notes
- Use [pattern/library]
- See [reference doc]
```

### Bug Fix Story

**Focus**: Fixing defects

```markdown
## Description
Fix [specific bug] that causes [symptom].

## Reproduction Steps
1. Do X
2. Observe Y
3. Expected Z, got W

## Root Cause
[Technical explanation of why bug occurs]

## Fix
[Description of solution]

## Acceptance Criteria
- [ ] Bug no longer occurs when following reproduction steps
- [ ] Regression test added to prevent recurrence
- [ ] Related edge cases tested
```

### Technical Story

**Focus**: Infrastructure or technical improvements

```markdown
## Description
[Technical change] to improve [aspect].

## Context
Current implementation has [limitation]. This change enables [capability].

## Acceptance Criteria
- [ ] [Technical metric] improved by [amount]
- [ ] Existing functionality unaffected
- [ ] Documentation updated with new approach

## Technical Notes
- Benchmark: [current vs. target]
- Approach: [technical details]
```

## Australian English

All story content uses **Australian English spelling**:

- ✅ normalise, organisation, authorisation, colour, behaviour
- ❌ normalize, organization, authorization, color, behavior

This is a **project-wide standard**, not optional.

## Related Skills

- **agile-board** - Board-specific implementation (ZenHub/Jira/Linear MCP tools)
- **developer-analysis** - Pre-implementation analysis, POC scripts, design proposals (use BEFORE implementing stories)
- **git-workflow** - Branch naming, commit conventions, PR creation

## References

Detailed guides in `references/` folder:

- `story-templates.md` - User story format and examples
- `estimation-guide.md` - T-shirt sizing, complexity factors, breakdown strategies
- `sprint-workflows.md` - Sprint planning, retrospectives, velocity tracking
- `epic-planning.md` - Epic breakdown, dependencies, interface design,**mocking with Mockoon**
