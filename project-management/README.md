# Project Management Skill

Board-agnostic agile project management workflows and best practices.

## Files

- **SKILL.md** - Core agile workflows (loaded when triggered)

### References (Loaded as needed)

- **references/story-templates.md** - User story format, acceptance criteria examples
- **references/estimation-guide.md** - T-shirt sizing (XS=1, S=3, M=5, L=8, XL=13), complexity factors
- **references/sprint-workflows.md** - Sprint planning, daily standup, retrospectives

## When This Skill Triggers

Claude loads this skill when you:
- Write user stories (`"create a story for..."`)
- Create acceptance criteria (`"what should the acceptance criteria be..."`)
- Estimate story points (`"how should we size this story..."`)
- Plan sprints (`"what stories should we include in the sprint..."`)
- Break down large stories (`"this story is too big, how should we break it down..."`)

## What This Skill Provides

**The "WHAT" and "HOW" of agile project management**:
- **What** to put in user stories
- **How** to structure acceptance criteria
- **How** to estimate complexity (T-shirt sizing)
- **How** to plan and run sprints

**Board-agnostic** - Works with any agile board (ZenHub, Jira, Linear, etc.)

## What This Skill Does NOT Provide

**The "WHERE" - Board-specific implementation**:
- Use the `agile-board` skill for:
  - Creating issues on specific boards
  - MCP tools and API usage
  - Board-specific field mappings
  - Pipeline/status management

## Quick Reference

### Story Structure
```markdown
## Description
[What and why]

## Context
[Background]

## Acceptance Criteria
- [ ] Testable criterion 1
- [ ] Testable criterion 2

## Technical Notes
[Implementation guidance]

## Testing Strategy
[Test types and coverage]
```

### T-Shirt Sizing

| Size | Points | Time (with AI) |
|------|--------|----------------|
| XS   | 1      | < 2 hours |
| S    | 3      | 2-6 hours |
| M    | 5      | 1-2 days |
| L    | 8      | 2-4 days |
| XL   | 13     | 4-8 days (break down!) |

### Sprint Planning

1. Review sprint goal
2. Calculate capacity (avg velocity × capacity factor)
3. Select stories (highest priority first)
4. Verify Definition of Ready
5. Confirm sprint commitment

## Related Skills

- **agile-board** - Board-specific implementation (ZenHub/Jira/Linear)
- **git-workflow** - Branch naming, commit conventions, PR creation

## Best Practices

**DO**:
- ✅ Use checkbox format for acceptance criteria (`- [ ]`)
- ✅ Estimate stories with T-shirt sizing
- ✅ Break down L/XL stories before sprint
- ✅ Use Australian English spelling
- ✅ Focus on user value in stories

**DON'T**:
- ❌ Write vague acceptance criteria
- ❌ Estimate epics (points roll up from children)
- ❌ Add stories mid-sprint without removing others
- ❌ Use story points for performance reviews
- ❌ Skip sprint retrospectives
