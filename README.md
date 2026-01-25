# Claude Code Skills

Reusable Claude Code skills for agile project management and development workflows.

## Available Skills

- **git-workflow** - GitFlow branching strategy and commit conventions
- **agile-board** - Board-specific implementation (ZenHub/Jira/Linear)
- **project-management** - Story templates, estimation, sprint planning, epic planning
- **developer-analysis** - Engineering analysis before implementation
- **testing** - Testing strategy, coverage analysis, and quality assurance

## Installation

### 1. Clone this repository

Clone this repository to wherever you keep your projects:

```bash
git clone <your-repo-url>
cd claude-code-skills
```

### 2. Run the install script

The install script creates symlinks from `~/.claude/skills/` to the skill directories in this repository.

**Linux/Mac:**
```bash
./install-skills.sh
```

**Windows (PowerShell):**
```powershell
.\install-skills.ps1
```

Note: On Windows, you may need to run PowerShell as Administrator for symlink creation.

### 3. Update skills

To get the latest skill updates:

```bash
cd /path/to/claude-code-skills
git pull
```

The symlinks ensure Claude Code immediately uses the updated skills.

## What Gets Installed

The install script:
1. Creates `~/.claude/skills/` directory if it doesn't exist
2. Symlinks each skill directory into `~/.claude/skills/`
3. Makes skills available globally for all your projects
4. Each skill is then automatically loaded by Claude when relevant

## Per-Project Setup

### Agile Board Configuration

After installing skills, configure the agile board for each project:

```bash
cd /path/to/your/project
python /path/to/claude-code-skills/agile-board/scripts/setup.py
```

This creates a project-local `.claude/agile-board-config.json` with your board settings.

## Skills Overview

### git-workflow

GitFlow branching model with commit conventions and automated quality checks.

**Automatically triggers when:** Creating branches, writing commits, creating PRs, setting up linting/pre-commit hooks, questions about code quality automation

**Key features:**
- Branch naming: `feature/epic-X-story-Y.Z-description`
- Commit format: `type(scope): description`
- PR templates and review checklist
- **One-command linting setup** - Automated script detects languages and configures pre-commit hooks
- Pre-commit hooks for automated formatting and linting
- Multi-layer quality checks (IDE → Pre-commit → CI)
- Language-specific configs (Python, TypeScript, C#, Flutter, Terraform)

### agile-board

Board-specific implementation for creating and managing issues.

**Automatically triggers when:** Creating issues, managing sprints, updating ticket status

**Supported boards:**
- ZenHub (with MCP integration)
- Jira (REST API)
- Linear (GraphQL)

**Requires setup:** Run `setup.py` once per project to configure board type and credentials.

### project-management

Board-agnostic agile workflows.

**Automatically triggers when:** Writing user stories, creating acceptance criteria, estimating story points, planning sprints or epics

**Key features:**
- Story templates (feature, bug, technical)
- T-shirt sizing (XS=1, S=3, M=5, L=8, XL=13)
- Acceptance criteria best practices
- Sprint workflows (planning, retrospectives, velocity tracking)
- Epic planning and story dependencies
- Release planning across multiple epics

### developer-analysis

Engineering analysis before implementation.

**Automatically triggers when:** Starting work on a story, analyzing requirements, creating POC scripts for integrations, proposing technical design, reconciling with existing architecture

**Key features:**
- Requirements analysis and ambiguity identification
- POC script creation for third-party integrations
- Technical design proposals for user approval
- Architecture reconciliation
- Proactive use before implementation to reduce rework

### testing

Testing strategy, coverage analysis, and quality assurance.

**Automatically triggers when:** Planning test strategy, analyzing coverage, reviewing test quality in PRs, creating mocks for integrations, defining testing standards

**Key features:**
- Test strategy planning for stories
- Coverage analysis and reporting
- PR review test verification
- Integration mocking patterns
- Testing standards definition
- Referenced by developer-analysis and git-workflow skills

## How Skills Work Together

**Example:** "Create a story for implementing dark mode"

Claude automatically:
1. Loads `project-management` skill → Story structure, acceptance criteria, estimate
2. Loads `agile-board` skill → Board-specific creation (checks your config)
3. Uses board's MCP tools or API to create the issue
4. Applies proper formatting, estimates, and links to epics

## What's Version Controlled

✅ **Committed:**
- SKILL.md files
- Reference documentation
- Setup scripts
- Install scripts
- Example configurations

❌ **Not committed (.gitignore):**
- `config.json` files (contain workspace IDs, API tokens)
- Credentials or secrets

## Architecture

### Separation of Concerns

- **project-management** = "WHAT" and "HOW"
  - What to put in stories
  - How to structure acceptance criteria
  - How to estimate and plan

- **agile-board** = "WHERE"
  - Where to create issues (which board/platform)
  - Board-specific MCP tools and APIs

- **git-workflow** = "WHEN" and "WHY"
  - When to create branches
  - Why we use GitFlow
  - Commit and PR conventions
  - Code quality automation

- **developer-analysis** = "BEFORE"
  - Before implementation analysis
  - Requirements clarification
  - Technical design approval
  - POC validation

- **testing** = "QUALITY"
  - Test strategy and planning
  - Coverage analysis
  - Quality verification
  - Mock creation patterns

### Progressive Disclosure

Each skill uses Claude's progressive disclosure pattern:
- Core workflows in `SKILL.md`
- Detailed guides in `references/`
- Only loads what's needed when needed

## Design Documentation

See [SKILLS_ANALYSIS.md](SKILLS_ANALYSIS.md) for:
- Detailed analysis of what should/shouldn't be a skill
- Skills vs markdown documentation trade-offs
- Migration checklist and implementation notes
- Design principles and best practices

## Contributing

To add or update skills:

1. Make changes to skills in your local clone
2. Test changes locally (symlinked skills in `~/.claude/skills/` update immediately)
3. Commit and push changes
4. Team members run `git pull` in their clone to get updates

## Using with Multiple Skill Repositories

Since this installer uses symlinks, you can install skills from multiple repositories:

```bash
# Install these skills
cd ~/projects/claude-code-skills
./install-skills.sh

# Install other skills from a different repo
cd ~/projects/other-skills
./install-skills.sh
```

All skills coexist in `~/.claude/skills/` and are available to Claude Code.
