# Git Workflow Skill

GitFlow branching strategy and commit conventions skill for Claude Code.

## Files

### Core
- **SKILL.md** - Main skill instructions (loaded when triggered)

### References (Loaded as needed)
- **references/branch-naming.md** - GitFlow branch naming conventions
- **references/commit-format.md** - Conventional Commits format with Australian English
- **references/pr-template.md** - Pull request creation templates and examples
- **references/pr-review.md** - Code review checklist and guidelines

## When This Skill Triggers

Claude loads this skill when you:
- Create branches (`"create a feature branch for..."`)
- Write commit messages (`"commit these changes..."`)
- Create pull requests (`"create a PR for..."`)
- Review PRs (`"review this pull request..."`)
- Ask about git workflows (`"what branch should I target?"`)

## Critical Rules

This skill enforces:
- ✅ Feature/bugfix branches → **develop** (NOT main)
- ✅ Merge commits only (NOT squash/rebase)
- ✅ Australian English spelling in all messages
- ✅ Test results AND coverage in PRs (>80% coverage required)
- ❌ NO AI attribution in commits
- ❌ NO destructive git commands without explicit request

## Quick Commands

### Create Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-1-story-1.3-hybrid-search
```

### Commit
```bash
git commit -m "feat(retrieval): implement hybrid search

- Add OpenSearch hybrid query builder
- Implement RRF score normalisation

Implements Story 1.3"
```

### Create PR
```bash
gh pr create --base develop --title "[Epic 1 / Story 1.3] Implement hybrid search" --body "..."
```

### Review PR
```bash
gh pr checkout 42
pytest
gh pr review 42 --approve -b "LGTM - tests pass"
```

## Testing the Skill

Verify the skill loads correctly:

1. Ask Claude: "Create a feature branch for Story 1.3"
2. Claude should load this skill and suggest proper branch naming
3. Check that Australian English is used throughout

## Updating the Skill

To update:
1. Edit files in `~/.claude/skills/git-workflow/`
2. Changes take effect immediately (no restart needed)
3. Test by asking Claude about git workflows

## Related Skills

- **agile-board** - For creating GitHub issues from stories
- **project-management** - For story structure and estimation

## Portable Installation

To use on another machine:
```bash
cp -r ~/.claude/skills/git-workflow /path/to/other/machine/.claude/skills/
```

Or add to project:
```bash
cp -r ~/.claude/skills/git-workflow /path/to/project/.claude/skills/
```
