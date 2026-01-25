---
name: agile-board
description: "Board-specific implementation for creating and managing issues. Use when: creating issues on ZenHub/Jira/Linear, moving issues between pipelines, adding to sprints, setting board-specific fields. For story templates and estimation, use project-management skill. On first use in a project, run setup if .claude/agile-board-config.json is missing."
model: haiku
---

# Agile Board Integration

Board-specific implementation for Jira, ZenHub, Linear, and other project management platforms.

## Overview

**This skill provides the "WHERE"**: Board-specific MCP tools, APIs, and configuration for creating and managing issues on project management boards.

**For the "WHAT" and "HOW"**: Use `project-management` skill for story templates, estimation, and sprint workflows.

**Key capabilities**:
- Create and update issues on ZenHub/Jira/Linear boards
- Set story points/estimates in board-specific fields
- Link issues to parent epics
- Move issues between pipelines/columns
- Manage sprints and board configuration

## Critical Rules

### 1. Issue Creation Best Practices
- ✅ **Use native issues when possible**
  - ZenHub: Always use GitHub issues (NOT ZenHub-native)
  - Jira: Use Jira issues
  - Linear: Use Linear issues
- ✅ **Story points in dedicated field** - Use board's estimate API, NOT title/description
- ❌ **NEVER put story points in title** - Use `setIssueEstimate` API instead

### 2. Acceptance Criteria Format
- ✅ **ALWAYS use checkbox format** for trackability
```markdown
## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours
- [ ] Error messages display for invalid credentials
```
- ❌ **NEVER use non-checkbox format**

### 3. Australian English
- ✅ **All issue titles, descriptions, comments** use Australian English spelling
- ✅ normalise, organisation, authorisation, colour, behaviour
- ❌ NOT: normalize, organization, authorization, color, behavior

### 4. Labels and Links
- ✅ **Add labels during creation** (most boards don't allow updates after)
- ✅ **Link to parent epic at creation** (easier than linking later)
- ❌ **NEVER skip epic linking** for stories (breaks hierarchy tracking)

### 5. First-Time Setup Required
- ✅ **CRITICAL**: Check if `.claude/agile-board-config.json` exists before using this skill
- ✅ **Run setup script** if config missing: `python3 ~/.claude/skills/agile-board/scripts/setup.py`
- ❌ **NEVER proceed** without valid board configuration

## First Time Setup (Per Project)

**CRITICAL**: Before using this skill, check if `.claude/agile-board-config.json` exists in the current project.

### Improved Automated Setup Flow

The setup script provides an intelligent, automated experience that minimizes manual input.

**Interactive mode** (recommended):
```bash
python3 ~/.claude/skills/agile-board/scripts/setup.py
```

**What you provide**:
1. Board type (ZenHub/Jira/Linear)
2. API token (e.g., from app.zenhub.com → Settings → API Tokens)
3. Select workspace from list (auto-fetched)
4. Select default pipeline from list (auto-fetched)
5. Default labels (optional)

**What it auto-fetches** (ZenHub):
- ✅ GitHub repository ID (via `gh` CLI)
- ✅ Your ZenHub workspaces (via GraphQL API)
- ✅ Workspace pipelines (via GraphQL API)
- ✅ Organization ID (via GraphQL API)

**What it configures**:
1. `.claude/agile-board-config.json` - Project-local board settings
2. `~/.claude.json` - MCP server configuration for this project
3. `~/.claude/settings.json` - Permission wildcards to auto-approve MCP calls
4. `.gitignore` - Excludes config file from version control

**Config location**: Project-local, NOT in the skill directory
- ✅ `/home/user/project-a/.claude/agile-board-config.json`
- ❌ `~/.claude/skills/agile-board/config.json`

**Non-interactive mode** (for automation):
```bash
python3 ~/.claude/skills/agile-board/scripts/setup.py \
  --board-type zenhub \
  --api-token zh_xxx \
  --workspace-id "Z2lkOi8..." \
  --repository-id "R_kgDO..." \
  --organization-id "Z2lkOi8..." \
  --default-pipeline-id "Z2lkOi8..." \
  --default-pipeline-name "Product Backlog" \
  --default-labels "backend,python" \
  --force
```

### Automated Setup via Skill

**If config is missing**, Claude Code automatically handles setup with GUI prompts:

**Flow**:
1. **Ask user for board type** (ZenHub/Jira/Linear) via `AskUserQuestion`
2. **Ask for API token** via conversation
3. **Auto-fetch GitHub repo ID** via `gh` CLI
4. **Fetch workspaces** via ZenHub GraphQL API
5. **Show workspace selection** via `AskUserQuestion` GUI
6. **Fetch pipelines** for selected workspace via GraphQL API
7. **Show pipeline selection** via `AskUserQuestion` GUI
8. **Ask for default labels** via conversation (optional)
9. **Run setup script** non-interactively with all values as CLI arguments

**Example**:
```bash
python3 ~/.claude/skills/agile-board/scripts/setup.py \
  --board-type zenhub \
  --api-token "zh_xxx" \
  --repository-id "R_kgDORAKQMg" \
  --workspace-id "Z2lkOi8vcmFwdG9yL1dvcmtzcGFjZS82OTQ4YzNiYWYzNWNjNDAwMjFkYjI2Zjc" \
  --organization-id "Z2lkOi8vcmFwdG9yL09yZ2FuaXphdGlvbi8xMjM0NTY" \
  --default-pipeline-id "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjUwMzk" \
  --default-pipeline-name "Product Backlog" \
  --default-labels "backend,python" \
  --force
```

**Benefits**:
- ✅ GUI workspace/pipeline selection (not terminal text input)
- ✅ Script runs non-interactively (no prompts, only writes files)
- ✅ All values validated before running script
- ✅ Clear error messages if API calls fail

## Quick Start

After setup, you can:
- Create issues/tickets
- Set story points/estimates
- Link issues to parent epics
- Move issues between pipelines/columns
- Add labels and assignees
- Manage sprints

## Model Selection

**Recommended model**: Haiku (fast and cost-effective)

**Why Haiku is appropriate**:
- **MCP tool operations** - Straightforward API calls with defined parameters
- **Simple CRUD operations** - Creating, reading, updating tickets
- **Pipeline transitions** - Moving tickets between states
- **No complex reasoning required** - All operations follow clear patterns
- **High frequency operations** - Cost savings with faster model

**Operations this skill handles**:
- `moveIssueToPipeline` - Simple state transition
- `createIssue` - Template-based creation
- `setIssueEstimate` - Setting numeric value
- `assignIssues` - Adding assignees
- All board-specific MCP tool calls

## Board Types

This skill supports multiple board types through board-specific reference documentation:

- **ZenHub**: See `references/zenhub.md` for MCP tool usage
- **Jira**: See `references/jira.md` for REST API patterns
- **Linear**: See `references/linear.md` for GraphQL queries

The setup script configures which board type to use via the project's config file.

## Common Operations

### Creating an Issue

**Pre-creation** (use `project-management` skill):
1. Draft story using story templates
2. Write acceptance criteria
3. Estimate using T-shirt sizing

**Board creation** (use this skill):
1. Create issue on board (via MCP or API)
2. Set issue type
3. Set estimate in dedicated field
4. Link to parent epic
5. Add labels (cannot change later!)
6. Move to pipeline

**Board-specific details**: See your board's reference file in `references/`

### Issue Hierarchy

```
Epic (Level 3)
  └── Story/Feature (Level 4)
      └── Sub-task (Level 5)
```

Link stories to parent epic for tracking.

### Board-Specific Rules

Different boards have different limitations:

**ZenHub**:
- ✅ Use GitHub issues (NOT ZenHub-native)
- ✅ Set story points via `setIssueEstimate` API
- ❌ Cannot update labels after creation

**Jira** (planned):
- Story points in custom field
- Can update labels after creation

**Linear** (planned):
- Estimates in points or time
- Can update labels after creation

## Story Content & Sprint Workflows

For story structure, templates, sprint planning, and velocity tracking:
- **See `project-management` skill** for detailed guidance

**Board-specific implementation**:
- Use board's API/MCP tools to create issues with story content
- Move issues between pipelines/sprints using board-specific tools
- See `references/` for board-specific sprint operations (e.g., ZenHub GraphQL for adding issues to sprints)

## Configuration

The project's `.claude/agile-board-config.json` contains:

```json
{
  "board_type": "zenhub",
  "workspace_id": "...",
  "repository_id": "...",
  "organization_id": "...",
  "default_labels": ["backend", "python"],
  "default_pipeline_id": "...",
  "default_pipeline_name": "Product Backlog"
}
```

**Switching boards**: Delete `.claude/agile-board-config.json` and re-run setup script.

**Multi-project usage**: Each project has its own config, so you can use ZenHub in one project and Jira in another.

## Troubleshooting

### Issue: "config file not found"

**Solution**: Run setup script in the project directory:
```bash
cd /path/to/your/project
python ~/.claude/skills/agile-board/scripts/setup.py
```

### Issue: "Cannot update labels"

**Cause**: Most board APIs don't support updating labels after creation

**Solution**: Add labels during initial issue creation

### Issue: "Parent epic not found"

**Cause**: Epic ID is incorrect or epic doesn't exist

**Solution**:
1. List available epics
2. Verify epic ID format matches your board type
3. Ensure epic exists before linking

### Issue: "Story points not showing"

**Cause**: Estimate set in wrong field (e.g., description instead of dedicated field)

**Solution**: Use your board's specific estimate API call (see `references/`)

### Issue: "Wrong board config loaded"

**Cause**: Working in different project than expected

**Solution**: Check current directory - config is loaded from current project's `.claude/` directory

## Related Skills

- **project-management** - Story templates, estimation guide, sprint workflows
- **developer-analysis** - Pre-implementation analysis, POC scripts, design proposals
- **git-workflow** - Branch naming, commit conventions, PR creation

## References

### Workflow Documentation
- `references/ticket-workflow.md` - **Ticket update workflow** throughout development lifecycle (commit, PR creation, PR review)

### Board-Specific Implementation
- `references/zenhub.md` - ZenHub MCP tools, field mappings, pipeline IDs
- `references/jira.md` - Jira REST API patterns, custom fields
- `references/linear.md` - Linear GraphQL queries, status IDs

Choose your board type during setup, and the skill will reference the appropriate documentation.
