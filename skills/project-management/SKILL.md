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

> **Note**: The "Time (with AI)" column above is for story complexity and estimation decisions only. For effort model billing and planning, a separate conversion table is used (XS=0.5d, S=1.0d, M=3.0d, L=6.0d, XL=12.0d). See the Story Points to Days Conversion table in the Effort Model Generation section.

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
- **Setting epic start/end dates and milestones**
- **Generating effort models with cost/fee calculations**
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

## Effort Model Generation

**CRITICAL**: Always generate an effort model after epic planning is complete.

### When to Generate

Generate effort model when:
- [ ] All stories are estimated with story points
- [ ] Sprint duration is defined
- [ ] Team composition is known
- [ ] Rate card is available
- [ ] Sprint start date is defined

### Effort Model Components

**Required columns**:
- Sprint number (sequential)
- Start Date (sprint/story start)
- End Date (sprint/story end)
- Epic (parent epic)
- Story ID — use `EXPENSE` for non-labour rows, `OVERHEAD` for overhead roles
- Story Title
- Story Points (T-shirt sizing: XS=1, S=3, M=5, L=8, XL=13) — blank for expense/overhead rows
- Effort (Days) - Converted from story points; blank for expense rows
- Velocity Adjuster (reduce days by xx%) - Optional % reduction to effort; blank for expense rows
- Final Effort (Days) - Effort reduced by Velocity Adjuster; blank for expense rows
- Skill/Role (assigned based on story content; use expense category for expense rows e.g. `Infrastructure`, `LLM Consumption`, `Hardware`)
- Cost (currency) - Labour: Daily rate × Final Effort (Days) via formula; Expense: direct entry
- Markup % - Expense rows only: markup applied to cost to derive Original Fee; blank for labour rows
- Original Fee (currency) - Labour: Client rate × Final Effort (Days); Expense: Cost × (1 + Markup %)
- % Discount - Optional per-row discount applied to Original Fee
- Final Discounted Fee (currency) - Original Fee × (1 − % Discount)
- Dependencies (story IDs this story depends on)
- Notes (context, risks, assumptions)

### Story Points to Days Conversion

Use **upper bound** conversion (conservative estimates):

| Story Points | Effort (Days) |
|--------------|---------------|
| XS (1)       | 0.5           |
| S (3)        | 1.0           |
| M (5)        | 3.0           |
| L (8)        | 6.0           |
| XL (13)      | 12.0          |

### Skill Assignment Rules

Auto-assign skills based on story content:
- **Lead Tech** - Kickoffs, planning, PM work, training, handover, DevOps (if senior)
- **Backend Dev** - APIs, pipelines, transformations, business logic, data processing
- **Frontend Dev** - UI components, client-side logic
- **Full Stack Dev** - Features spanning frontend + backend
- **DevOps** - Infrastructure, deployments, CI/CD, networking, VPN, SFTP
- **DBA** - Database schema, RBAC, performance tuning, index optimization
- **QA Engineer** - Testing, validation, test automation
- **Functional Lead** - Requirements gathering, business logic analysis, framing requirements, driving business engagement and UAT sessions
- **Engagement Lead** - Always included as a standard overhead row (1 day per week per sprint); append one row per sprint regardless of named assignee

### Rate Card Structure

Maintain rate card in `docs/Rate_table.csv`:
```csv
Role,Cost Daily Rate,Fee Daily Rate
Lead Tech,1100,2500
Backend Dev,550,1900
DevOps Engineer,550,1900
DBA,550,1900
QA Engineer,550,1900
Functional Lead,550,1900
Engagement Lead,1100,2750

```

### Effort Model Format

**Output format**: Formula-based Excel (.xlsx) with:
- **Formulas for calculations** (not hardcoded values)
- **Velocity Adjuster (reduce days by xx%) column (I)**: % input; left blank if no adjustment needed
- **Final Effort (Days) column (J)**: `=IF(I{r}="", H{r}, H{r}*(1-I{r}))`
- **Cost column (L)**: Labour rows: `=IFERROR(VLOOKUP(K{r}, RateCard, 2, FALSE) * J{r}, "Check skill")`; Expense rows: direct entry
- **Markup % column (M)**: Expense rows only — % markup on cost; blank for labour rows
- **Original Fee column (N)**: `=IF(E{r}="EXPENSE", L{r}*(1+M{r}), IFERROR(VLOOKUP(K{r}, RateCard, 3, FALSE) * J{r}, "Check skill"))`
- **% Discount column (O)**: % input; left blank if no discount applies
- **Final Discounted Fee column (P)**: `=IFERROR(N{r}*(1-O{r}), N{r})`
- **Sprint total rows**: must use SUMIF on col A (sprint number) — **never range-based SUM** — summing: Points (G), Effort Days (H), Final Effort Days (J), Cost (L), Original Fee (N), Final Discounted Fee (P)
- **Grand total**: `=SUM(col4:coln)` across all data rows for the same columns
- **Conditional formatting**: Highlight overloaded sprints (>100% capacity)

> ⚠️ **CRITICAL — always use SUMIF for sprint totals, never range-based SUM:**
> Overhead rows (e.g. PM, DevOps) are typically appended to the end of the STORIES list grouped by type, not interleaved within each sprint's block. This means a sprint's rows are **non-contiguous** in the sheet. A range-based `=SUM(G17:G27)` will miss any overhead rows for that sprint that sit outside the range, and will incorrectly include rows from other sprints if the range overlaps. `SUMIF` on column A (the sprint number column) is the correct pattern — it aggregates all rows matching the sprint number regardless of their physical position in the sheet.

### Overhead Rows

**CRITICAL**: Always append overhead rows to the effort model — one per sprint for each overhead role.

#### Engagement Lead (mandatory)
- **Always include** — do not skip even if no named person is assigned
- One row per sprint
- **Effort (Days)** = 1 day × number of weeks in the sprint (e.g. 2-week sprint = 2 days, 3-week sprint = 3 days)
- Story Points: leave blank
- Story ID: `OVERHEAD`
- Epic: `Project Management`
- Story Title: `Engagement Lead oversight - Sprint {N}`
- Skill: `Engagement Lead`
- Velocity Adjuster: leave blank
- Dependencies: leave blank

#### Functional Lead (include when requirements/UAT work is present)
- Add rows for requirements workshops, UAT planning, and business engagement sessions
- Estimate effort based on known sessions or default to 0.5 days per sprint if unspecified
- Story ID: `OVERHEAD` or linked story ID if directly tied to a story
- Skill: `Functional Lead`

> ⚠️ Overhead rows must carry a sprint number in column A so SUMIF picks them up correctly in sprint totals.

### Expense Rows

Use expense rows for non-labour costs: infrastructure, LLM consumption, hardware, devices, licences, etc.

#### Row format
- **Story ID**: `EXPENSE`
- **Story Points, Effort (Days), Velocity Adjuster, Final Effort (Days)**: leave blank
- **Skill**: expense category — `Infrastructure`, `LLM Consumption`, `Hardware`, `Licences` etc.
- **Cost**: direct entry (actual or estimated cost)
- **Markup %**: direct entry — controls the proposed client fee:
  - Standard markup: enter e.g. `25%` → Original Fee = Cost × 1.25
  - Pass-through (reimbursable): enter `0%` → Original Fee = Cost
- **Original Fee**: formula `=L{r}*(1+M{r})` — auto-calculated from Cost and Markup %
- **% Discount** and **Final Discounted Fee**: work the same as labour rows
- **Sprint**: tie to the sprint the expense is incurred in; use `0` for project-level expenses with no specific sprint

#### Reimbursement clause (≤15% of project cost)

Add a summary block below the Grand Total row:

| Label | Formula |
|-------|---------|
| Total Labour Cost | `=SUMIF(E4:En, "<>EXPENSE", L4:Ln)` |
| Total Expenses Cost | `=SUMIF(E4:En, "EXPENSE", L4:Ln)` |
| Expenses as % of Labour | `=Total Expenses Cost / Total Labour Cost` |
| Reimbursement Cap (15%) | `=Total Labour Cost * 0.15` |
| Status | `=IF(Total Expenses Cost > Cap, "⚠ EXCEEDS 15% CAP", "Within limit")` |

Apply **red conditional formatting** to the Status cell when expenses exceed the cap.

> ⚠️ The reimbursement summary uses Labour Cost (not total project cost) as the base, since expenses are excluded from labour. Adjust the cap % if the contract references total project cost instead.

### Sprint Allocation

When allocating stories to sprints:
1. **Calculate sprint capacity**: Team size × sprint days × 0.8 (buffer)
2. **Respect dependencies**: Dependent stories in later sprints
3. **Balance load**: Aim for 80% capacity per sprint (20% buffer)
4. **Sequential assignment**: Fill Sprint 1, then 2, then 3...
5. **Consider skills**: Don't overload single skill in one sprint

### Team Size Guidance

**For small teams (1-3 people)**:
- Accept that some sprints will have single skill doing multiple roles
- Flag in Notes column when person wears multiple hats
- Consider suggesting additional resources if critical path affected

**Example note**: "Lead Tech also doing DevOps work - risk if overloaded"

### Location-Based Considerations

Factor in location for:
- **Public holidays** - Adjust sprint capacity for holiday weeks
- **Currency** - Use appropriate currency for cost/fee
- **Rate variations** - Different locations have different rate cards

### Effort Model Example Structure

```
[Rate Card Tab]
Role | Cost Daily Rate | Fee Daily Rate
(Rows start at row 3 — referenced as $A$3:$C$[n] in VLOOKUP)

[Effort Model Tab]
Row 1: Title
Row 2: Note / warning
Row 3: Column headers
Row 4+: Data rows (stories + overhead rows e.g. Engagement Lead)

Columns: Sprint | Start Date | End Date | Epic | Story ID | Story Title |
         Story Points | Effort (Days) | Velocity Adjuster (reduce days by xx%) | Final Effort (Days) | Skill |
         Cost | Markup % | Original Fee | % Discount | Final Discounted Fee | Dependencies | Notes
         (A)      (B)            (C)        (D)    (E)        (F)
         (G)          (H)                       (I)                             (J)          (K)
         (L)     (M)        (N)            (O)           (P)                    (Q)            (R)

[Formula in Final Effort (Days) cell (col J, row r):    =IF(I{r}="", H{r}, H{r}*(1-I{r}))]
[Formula in Cost cell (col L, row r) — labour only:     =IFERROR(VLOOKUP(K{r},'Rate Card'!$A$3:$C$10,2,0)*J{r},"Check skill")]
[Cost cell — expense rows:                              direct entry]
[Formula in Original Fee cell (col N, row r):           =IF(E{r}="EXPENSE",L{r}*(1+M{r}),IFERROR(VLOOKUP(K{r},'Rate Card'!$A$3:$C$10,3,0)*J{r},"Check skill"))]
[Formula in Final Discounted Fee cell (col P, row r):   =IFERROR(N{r}*(1-O{r}),N{r})]

[Sprint Total rows — SUMIF on sprint number in column A]
[last_data_row = 3 + len(STORIES) + num_sprints + num_expense_rows]
Points:               =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $G$4:$G${last_data_row})
Days:                 =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $H$4:$H${last_data_row})
Final Effort (Days):  =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $J$4:$J${last_data_row})
Cost:                 =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $L$4:$L${last_data_row})
Original Fee:         =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $N$4:$N${last_data_row})
Final Discounted Fee: =SUMIF($A$4:$A${last_data_row}, {sprint_num}, $P$4:$P${last_data_row})

[Grand Total row]
Points:               =SUM(G4:G{last_data_row})
Days:                 =SUM(H4:H{last_data_row})
Final Effort (Days):  =SUM(J4:J{last_data_row})
Cost:                 =SUM(L4:L{last_data_row})
Original Fee:         =SUM(N4:N{last_data_row})
Final Discounted Fee: =SUM(P4:P{last_data_row})

[Reimbursement Summary block — rows below Grand Total]
Total Labour Cost:       =SUMIF($E$4:$E${last_data_row},"<>EXPENSE",$L$4:$L${last_data_row})
Total Expenses Cost:     =SUMIF($E$4:$E${last_data_row},"EXPENSE",$L$4:$L${last_data_row})
Expenses as % of Labour: =Total Expenses Cost / Total Labour Cost  [format as %]
Reimbursement Cap (15%): =Total Labour Cost * 0.15
Status:                  =IF(Total Expenses Cost > Reimbursement Cap, "EXCEEDS 15% CAP", "Within limit")
[Apply red fill to Status cell when condition is TRUE]
```

### Validation Checks

Before finalizing effort model:
- [ ] All stories have effort estimates
- [ ] All stories have skill assignments
- [ ] Functional Lead rows added for all requirements gathering and UAT stories
- [ ] Engagement Lead overhead row present for every sprint (1 day × sprint weeks)
- [ ] All overhead and expense rows have a sprint number in column A
- [ ] Expense rows present for all known non-labour costs (infrastructure, LLM, hardware etc.)
- [ ] All expense rows have Markup % entered (0% for pass-through, >0% for marked-up)
- [ ] Reimbursement summary block present below Grand Total
- [ ] Reimbursement Status cell shows "Within limit" (flag if red)
- [ ] Dependencies are captured
- [ ] Sprint dates are continuous (no gaps)
- [ ] Total effort matches story points conversion
- [ ] Rate card covers all assigned skills (including Functional Lead and Engagement Lead)
- [ ] Formulas calculate correctly (labour Cost/Original Fee reference Final Effort Days col J; expense Original Fee references Cost × (1 + Markup %))
- [ ] No sprint exceeds 120% capacity

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
