# Agile Board Skill

Generic agile board integration for Jira, ZenHub, Linear, and other project management platforms.

## Files

- **SKILL.md** - Main skill instructions (loaded when triggered)
- **config.json.example** - Example configuration (copy to project's `.claude/` directory)
- **scripts/setup.py** - Interactive setup wizard

### References (Loaded as needed)

- **references/zenhub.md** - ZenHub MCP tools, field mappings, workflows
- **references/jira.md** - Jira REST API patterns (placeholder for future)
- **references/linear.md** - Linear GraphQL queries (placeholder for future)

## When This Skill Triggers

Claude loads this skill when you:
- Create issues/tickets (`"create a story for..."`)
- Manage sprints (`"add this to the current sprint..."`)
- Update ticket status (`"move this issue to in progress..."`)
- Estimate stories (`"set story points for..."`)
- Link issues to epics (`"link this story to epic 4..."`)

## First Time Setup

**IMPORTANT**: On first use in a new project, run the setup wizard:

```bash
python ~/.claude/skills/agile-board/scripts/setup.py
```

This creates `.claude/agile-board-config.json` in your project directory with:
- Board type (ZenHub/Jira/Linear)
- Workspace/repository IDs
- Default labels and pipelines

The config is project-specific and should be gitignored.

## Configuration Location

Configs live in **project directories**, not in the skill directory:

```
~/.claude/skills/agile-board/          # Global skill (shared)
/project-a/.claude/agile-board-config.json   # Project A uses ZenHub
/project-b/.claude/agile-board-config.json   # Project B uses Jira
```

Add to each project's `.gitignore`:
```
.claude/agile-board-config.json
```

## Switching Projects

The skill automatically detects which project you're in and uses that project's config.

## Reconfiguring

To change board settings for a project:
```bash
rm .claude/agile-board-config.json
python ~/.claude/skills/agile-board/scripts/setup.py
```

## Board Types Supported

- **ZenHub** - Full support via MCP server
- **Jira** - Planned (reference file placeholder)
- **Linear** - Planned (reference file placeholder)
