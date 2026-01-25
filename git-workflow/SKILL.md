---
name: git-workflow
description: "GitFlow branching strategy and commit conventions. Use when: (1) Creating branches (feature/bugfix/hotfix/release), (2) Writing commit messages, (3) Creating or reviewing pull requests, (4) Merging code, (5) Questions about branch targets or git operations, (6) Setting up pre-commit hooks, linting, or code quality checks, (7) Questions about automated formatting or quality enforcement. CRITICAL: Feature/bugfix always target develop, NOT main."
model: sonnet
---

# Git Workflow

This skill enforces GitFlow branching strategy and commit conventions for professional software development.

## Critical Rules - READ FIRST

### Branch Targets
- ✅ **Feature branches** (`feature/*`) → **develop** (NOT main)
- ✅ **Bugfix branches** (`bugfix/*`) → **develop** (NOT main)
- ✅ **Hotfix branches** (`hotfix/*`) → **main** (urgent production fixes only)
- ✅ **Release branches** (`release/*`) → **main** (official releases only)
- ⚠️ **ALWAYS verify target before creating PR**: `gh pr view {PR} --json baseRefName`

### Merge Strategy
- ✅ **Always use merge commits** (NOT squash or rebase)
- ✅ Command: `gh pr merge {PR} --merge --delete-branch`
- ❌ **NEVER use**: `--squash` or `--rebase`
- **Why**: Preserves full commit history for traceability

### Commit Attribution
- ❌ **NEVER attribute commits to AI tools**
- ❌ **NO "Co-Authored-By: Claude" tags**
- ✅ All commits attributed to human developer only

### Git Safety Protocol
- ❌ **NEVER run destructive commands** without explicit user request:
  - `push --force`, `reset --hard`, `checkout .`, `restore .`, `clean -f`, `branch -D`
- ❌ **NEVER skip hooks**: No `--no-verify` or `--no-gpg-sign` unless requested
- ❌ **NEVER force push to main/master** (warn user if requested)
- ❌ **NEVER amend commits after hook failures** (create NEW commit instead)
- ✅ **Prefer specific file staging** over `git add -A` or `git add .`

### Pre-commit Hooks & Linting
- ✅ **Automate quality checks** at commit time (formatting, linting, line endings)
- ✅ **Install defaults automatically** if project lacks configuration
- ✅ **Multi-layer strategy**: IDE (real-time) → Pre-commit (commit-time) → CI (enforcement)
- ❌ **NEVER bypass hooks** without user request

## Quick Start

### Check Current Status
```bash
# What branch am I on?
git branch --show-current

# What's the status?
git status

# What commits are on this branch?
git log --oneline -5
```

### Create a New Branch
```bash
# Ensure you're on develop and up to date
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/epic-1-story-1.3-hybrid-search
```

See `references/branch-naming.md` for naming conventions.

### Commit Changes
```bash
# Stage specific files (preferred)
git add src/api/search.py tests/test_search.py

# Commit with conventional format
git commit -m "feat(retrieval): implement hybrid search with score normalisation

- Add OpenSearch hybrid query builder
- Implement RRF score normalisation
- Add filter allowlist enforcement

Relates to Story 1.3"
```

See `references/commit-format.md` for message conventions.

### Create Pull Request
```bash
# Push branch
git push -u origin feature/epic-1-story-1.3-hybrid-search

# Create PR targeting develop (CRITICAL: verify base!)
gh pr create --base develop --title "[Epic 1 / Story 1.3] Implement hybrid search" --body-file .github/pull_request_template.md

# Verify target branch
gh pr view --json baseRefName
```

See `references/pr-workflow.md` for full PR creation and review process.

## Model Selection

**Recommended model**: Haiku for git operations, Sonnet for PR reviews

**Why these models**:

**Haiku for git commands**:
- **Branch creation** - Follows naming convention template
- **Commit messages** - Template-based conventional commit format
- **Git operations** - Straightforward command execution
- **No complex reasoning** - Mechanical operations

**Sonnet for PR review**:
- **AC verification** - Requires understanding story requirements
- **Code quality assessment** - Needs reasoning about design patterns
- **Australian English checking** - Language understanding
- **Security review** - Requires threat modeling
- **Test coverage analysis** - Understanding test completeness

**Operations by model**:
- ✅ Haiku: `git checkout`, `git commit`, `git push`, `git branch`
- ✅ Haiku: Branch naming, commit message formatting
- ✅ Sonnet: PR creation with comprehensive description
- ✅ Sonnet: PR review with AC verification
- ✅ Sonnet: Code review feedback

## Branching Strategy: GitFlow vs Alternatives

This skill teaches **GitFlow** by default. GitFlow is excellent for many contexts, but alternatives may be better for your project.

### When GitFlow is the Right Choice

✅ **Use GitFlow when**:
- **Release-based software** - Desktop apps, mobile apps, versioned libraries
- **Multiple version support** - Supporting v1.x and v2.x simultaneously
- **Scheduled releases** - Monthly/quarterly release cycles
- **Multiple environments** - Distinct dev/staging/production deployments
- **Large teams** - Need structured coordination across teams
- **QA process** - Dedicated testing phase before release

**Examples**: Desktop software (v1.0, v1.1, v2.0), mobile apps (App Store releases), enterprise software with SLAs

**GitFlow structure**:
```
main (production)
  ← release/v1.2 ← develop ← feature/new-feature
                          ← bugfix/fix-issue
  ← hotfix/critical-fix
```

**Benefits**:
- Clear separation between development and production
- Supports parallel release preparation and feature development
- Explicit release branches for final testing
- Hotfix workflow for urgent production fixes

### Alternative 1: GitHub Flow (Simpler)

✅ **Use GitHub Flow when**:
- **Continuous delivery** - Deploy to production multiple times per day
- **Single production version** - No need to support multiple versions
- **Small teams** - Fast-moving, high trust
- **Web applications** - SaaS, web services with rolling deployments
- **Rapid iteration** - Feature flags for incomplete features

**Examples**: SaaS applications, internal tools, microservices, web APIs

**GitHub Flow structure**:
```
main (production, always deployable)
  ← feature/new-feature
  ← bugfix/fix-issue
```

**How it differs from GitFlow**:
- ❌ No `develop` branch - everything merges to `main`
- ❌ No `release` branches - `main` is always production-ready
- ❌ No `hotfix` branches - all fixes follow same workflow
- ✅ Simpler - only `main` + feature branches
- ✅ Deploy directly from `main` after merge

**Workflow**:
1. Branch from `main` (e.g., `feature/add-search`)
2. Develop, commit, push
3. Create PR → `main` (NOT develop)
4. Review, approve, merge
5. Deploy `main` to production immediately

### Alternative 2: Trunk-Based Development (Fastest)

✅ **Use Trunk-Based Development when**:
- **Very high deployment frequency** - Multiple deploys per hour
- **Feature flags everywhere** - Features toggled on/off in production
- **Strong CI/CD** - Comprehensive automated testing and deployment
- **Experienced team** - High discipline, small commits, continuous integration
- **Microservices** - Independent services with isolated deployments

**Examples**: Google-scale engineering, high-frequency trading platforms, cloud-native microservices

**Trunk-Based structure**:
```
main (trunk, always deployable)
  ← short-lived branch (< 1 day)
```

**How it differs**:
- ✅ All developers commit to `main` daily (or more frequently)
- ✅ Short-lived feature branches (hours, not days)
- ✅ Feature flags for incomplete features
- ✅ Very strong automated testing (>90% coverage)
- ❌ No long-lived branches at all

**Workflow**:
1. Small, incremental changes
2. Commit to `main` or very short-lived branch
3. Automated tests run on every commit
4. Deploy `main` continuously (every commit or scheduled)

### Comparison Table

| Aspect | GitFlow | GitHub Flow | Trunk-Based |
|--------|---------|-------------|-------------|
| **Complexity** | High | Medium | Low (but requires discipline) |
| **Deploy frequency** | Scheduled (weekly/monthly) | On-demand (daily) | Continuous (hourly/per commit) |
| **Branches** | 5 types (main, develop, feature, release, hotfix) | 2 types (main, feature) | 1 (main) + very short-lived branches |
| **Testing phase** | Explicit (release branch) | During PR review | Continuous (automated) |
| **Rollback strategy** | Hotfix branch | Revert PR | Feature flags or revert commit |
| **Team size** | Large teams (10+) | Small-medium teams (2-10) | Any size (requires maturity) |
| **Best for** | Release-based software | Continuous delivery web apps | High-frequency deployments |

### Why This Skill Teaches GitFlow

**GitFlow is taught because**:
1. **Structured learning** - Teaches all branching concepts (feature, release, hotfix)
2. **Industry standard** - Widely used in enterprise and open source
3. **Safe default** - Works well for most projects, especially early-stage
4. **Explicit workflow** - Clear rules reduce mistakes
5. **Transferable skills** - Understanding GitFlow makes other workflows easier to adopt

**If you need a different workflow**:
- GitHub Flow: Simply target `main` instead of `develop`, skip release/hotfix branches
- Trunk-Based: Use very short-lived branches, commit to `main` frequently

### Switching Workflows

**To switch from GitFlow to GitHub Flow**:
1. Merge `develop` into `main`
2. Delete `develop` branch
3. Update PR targets: `feature/*` → `main` (not develop)
4. Skip release branches (deploy `main` directly)

**To switch from GitFlow to Trunk-Based**:
1. Adopt feature flags for incomplete features
2. Increase automated test coverage (aim for 90%+)
3. Shorten branch lifespans (< 1 day)
4. Commit to `main` frequently (multiple times per day)
5. Set up continuous deployment pipeline

## Pre-commit Hooks & Automated Quality Checks

**CRITICAL**: Pre-commit hooks prevent bad code from entering git history by automatically formatting, linting, and validating code before every commit.

### Multi-Layer Linting Strategy

Quality checks happen at **three layers**:

1. **IDE/Editor (Real-time)** - Instant feedback while coding
   - VSCode: ESLint, Black formatter, Dart analyzer extensions
   - Catches issues immediately as you type

2. **Pre-commit Hooks (Commit-time)** ⭐ **THIS SECTION** - Automated checks before commit
   - Runs automatically on `git commit`
   - Formats code, runs linters, checks for secrets
   - **Fixes line endings automatically** (fixes the issue with developers messing up line endings)
   - Blocks commit if checks fail

3. **CI Pipeline (Enforcement)** - Final enforcement in CI/CD
   - See `references/ci-cd-workflow.md`
   - Blocks merge if checks fail
   - Redundant safety net

### Automated Installation (Recommended)

**ONE-COMMAND SETUP** - Run this in your project root:

```bash
# Navigate to the git-workflow skill directory and run the setup script
python ~/.claude/skills/git-workflow/scripts/setup-linting.py
```

**What the script does**:
1. 🔍 **Detects languages** - Python, TypeScript/JS, Flutter, C#, Terraform
2. 📦 **Installs tools** - black, ruff, mypy, eslint, prettier (as needed)
3. 🔧 **Configures PATH** - Ensures tools are accessible
4. 📝 **Generates config** - Creates `.pre-commit-config.yaml` with appropriate hooks
5. 🔗 **Installs hooks** - Runs `pre-commit install` automatically
6. 🧪 **Tests setup** - Validates hooks work on all files

**After setup**:
- Hooks run automatically on `git commit` (NO manual intervention needed)
- Bypass if needed: `git commit --no-verify`
- Review changes made by hooks: `git diff`

**If you prefer manual setup**, see the Manual Installation section below.

### Language-Specific Default Configurations

**POC Script Exclusions**: POC scripts in `scripts/poc/` are intentionally hacky (hardcoded values, no type hints, minimal error handling). These are **excluded from strict linting and type checking**, but still get formatting and safety checks.

#### Python Projects

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization (ALWAYS RUN - even on POCs)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']  # Force LF line endings
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key  # CRITICAL: Prevent committing API keys

  # Python formatting (ALWAYS RUN - keeps POCs readable)
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11
        args: ['--line-length=100']

  # Python linting (SKIP POCs - too strict for exploration code)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: ['--fix', '--exit-non-zero-on-fix']
        exclude: '^scripts/poc/'  # Exclude POC scripts

  # Type checking (SKIP POCs - no type hints required)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: ['--ignore-missing-imports', '--strict']
        exclude: '^scripts/poc/'  # Exclude POC scripts
```

**Installation**: Run `python ~/.claude/skills/git-workflow/scripts/setup-linting.py` (see Automated Installation above)

**Optional: Configure ruff in pyproject.toml** (modern format):

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

# Modern format (use [tool.ruff.lint] not [tool.ruff])
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
]
ignore = [
    "E501",  # Line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"scripts/poc/**/*.py" = ["ALL"]  # POCs can be hacky
"tests/**/*.py" = ["S101"]  # Allow assert in tests
```

**Why use pyproject.toml configuration**:
- IDE integration (VSCode, PyCharm read this file)
- Consistent configuration across pre-commit hooks, IDE, and CLI
- Modern ruff format avoids deprecation warnings

**What this fixes**:
- ✅ Line endings normalized to LF (fixes Windows/Mac line ending issues)
- ✅ Code auto-formatted with Black (production code AND POCs)
- ✅ Linting errors caught (unused imports, undefined variables) - **production code only**
- ✅ Type errors caught before commit - **production code only**
- ✅ Secrets detection (prevents committing API keys) - **all files including POCs**

**POC script handling**:
- ✅ `scripts/poc/*.py` **excluded from ruff and mypy** (can be hacky)
- ✅ Still formatted with Black (keeps code readable)
- ✅ Still checked for secrets (critical security)
- ✅ Line endings still normalized (fixes CRLF issues)

#### TypeScript/Node.js Projects

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  # TypeScript/JavaScript formatting (Prettier)
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]
        args: ['--write', '--ignore-unknown']

  # TypeScript/JavaScript linting (ESLint)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        types_or: [javascript, jsx, ts, tsx]
        args: ['--fix', '--max-warnings=0']
        additional_dependencies:
          - eslint@8.56.0
          - '@typescript-eslint/parser@6.19.0'
          - '@typescript-eslint/eslint-plugin@6.19.0'
```

**Alternative: Use Husky** (if team prefers npm-based hooks):

```bash
# Install husky and lint-staged
npm install --save-dev husky lint-staged

# Initialize husky
npx husky init

# Create pre-commit hook
cat > .husky/pre-commit <<EOF
#!/usr/bin/env sh
. "\$(dirname -- "\$0")/_/husky.sh"

npx lint-staged
EOF

chmod +x .husky/pre-commit

# Configure lint-staged in package.json
cat > package.json <<EOF
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "prettier --write",
      "eslint --fix --max-warnings=0"
    ],
    "*.{json,yaml,yml,md}": [
      "prettier --write"
    ]
  }
}
EOF
```

**What this fixes**:
- ✅ Line endings normalized to LF
- ✅ Code auto-formatted with Prettier
- ✅ ESLint errors auto-fixed where possible
- ✅ Blocks commit if linting errors remain

#### Flutter/Dart Projects

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']
      - id: check-yaml
      - id: detect-private-key

  # Dart formatting and analysis
  - repo: local
    hooks:
      - id: dart-format
        name: Dart Format
        entry: dart format
        language: system
        types: [dart]
        args: ['--set-exit-if-changed', '--line-length=100']

      - id: dart-analyze
        name: Dart Analyze
        entry: dart analyze
        language: system
        types: [dart]
        pass_filenames: false
        args: ['--fatal-infos', '--fatal-warnings']

      - id: flutter-test
        name: Flutter Test (Fast Unit Tests Only)
        entry: flutter test
        language: system
        types: [dart]
        pass_filenames: false
        args: ['--no-pub', '--coverage']
        # Only run if test/ directory exists
```

**Installation**: Run `python ~/.claude/skills/git-workflow/scripts/setup-linting.py` (see Automated Installation above)

**What this fixes**:
- ✅ Line endings normalized to LF
- ✅ Dart code auto-formatted (`dart format`)
- ✅ Analysis errors caught (`dart analyze`)
- ✅ Unit tests run before commit (optional, can be disabled if slow)

#### C# / .NET Projects

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  # C# formatting and linting
  - repo: local
    hooks:
      - id: dotnet-format
        name: dotnet format
        entry: dotnet format
        language: system
        types: [c#]
        args: ['--verify-no-changes']
        pass_filenames: false

      - id: dotnet-build
        name: dotnet build (check compilation)
        entry: dotnet build
        language: system
        types: [c#]
        args: ['--no-incremental', '/WarnAsError']
        pass_filenames: false
```

**Installation**: Run `python ~/.claude/skills/git-workflow/scripts/setup-linting.py` (see Automated Installation above)

**What this fixes**:
- ✅ Line endings normalized to LF
- ✅ C# code auto-formatted (`dotnet format`)
- ✅ Compilation errors caught before commit
- ✅ Warnings treated as errors

#### JavaScript Projects (Non-TypeScript)

**Note**: JavaScript projects use the same Prettier/ESLint setup as TypeScript, just without TypeScript-specific plugins.

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  # JavaScript formatting (Prettier)
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, json, yaml, markdown]
        args: ['--write', '--ignore-unknown']

  # JavaScript linting (ESLint)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        types_or: [javascript, jsx]
        args: ['--fix', '--max-warnings=0']
        additional_dependencies:
          - eslint@8.56.0
          - eslint-config-airbnb-base@15.0.0
          - eslint-plugin-import@2.29.0
```

**What this fixes**:
- ✅ Line endings normalized to LF
- ✅ Code auto-formatted with Prettier
- ✅ ESLint errors auto-fixed where possible
- ✅ Blocks commit if linting errors remain

#### Terraform Projects

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Line ending normalization
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  # Terraform formatting and validation
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
      - id: terraform_tflint
        args:
          - --args=--config=__GIT_WORKING_DIR__/.tflint.hcl
      - id: terraform_tfsec
        args:
          - --args=--minimum-severity=MEDIUM
```

**Installation**: Run `python ~/.claude/skills/git-workflow/scripts/setup-linting.py` (see Automated Installation above)

**What this fixes**:
- ✅ Line endings normalized to LF
- ✅ Terraform code auto-formatted (`terraform fmt`)
- ✅ Terraform configuration validated (`terraform validate`)
- ✅ Linting with tflint (best practices, deprecated syntax)
- ✅ Security scanning with tfsec (misconfigurations, vulnerabilities)
- ✅ Documentation auto-generated (`terraform-docs`)

### Manual Installation (Fallback)

If you prefer manual setup or the automated script doesn't work for your environment, follow these steps:

#### Step 1: Install pre-commit framework

```bash
pip install pre-commit
```

#### Step 2: Install language-specific tools

**Python**:
```bash
pip install black ruff mypy
```

**TypeScript/JavaScript**:
```bash
npm install --save-dev eslint prettier
```

**Other languages**: Tools are typically included with SDKs (Flutter, .NET, Terraform)

#### Step 3: Update PATH (if needed)

**Linux/Mac**:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell as Administrator)**:
```powershell
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$env:APPDATA\Python\Scripts", "User")
```

#### Step 4: Create .pre-commit-config.yaml

Copy the appropriate configuration from the language-specific sections above (Python, TypeScript, Flutter, C#, or Terraform).

#### Step 5: Install git hooks

```bash
pre-commit install
```

#### Step 6: Test setup

```bash
# Run hooks on all files to verify setup
pre-commit run --all-files
```

### Multi-Language Projects (Python + TypeScript + Flutter + C# + Terraform)

**Auto-generated `.pre-commit-config.yaml`**:

```yaml
repos:
  # Common hooks (ALL languages)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']  # CRITICAL: Fixes line ending issues
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: detect-private-key

  # Python
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        types: [python]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        types: [python]
        args: ['--fix']
        exclude: '^scripts/poc/'  # POCs can be hacky

  # TypeScript/JavaScript
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        types_or: [javascript, jsx, ts, tsx]
        args: ['--fix']

  # Dart/Flutter
  - repo: local
    hooks:
      - id: dart-format
        name: Dart Format
        entry: dart format
        language: system
        types: [dart]
        args: ['--set-exit-if-changed']
```

### How Pre-commit Hooks Work in Daily Workflow

**Normal commit workflow**:

```bash
# 1. Make changes to code
vim src/api/search.py

# 2. Stage changes
git add src/api/search.py

# 3. Attempt commit
git commit -m "feat(search): add hybrid search"

# 4. Pre-commit hooks run automatically:
# ✅ end-of-file-fixer............Passed
# ✅ trailing-whitespace...........Passed
# ✅ mixed-line-ending.............Fixed (LF line endings enforced)
# ✅ black.........................Reformatted
# ✅ ruff..........................Passed
# ✅ mypy..........................Passed

# 5. If hooks made changes (formatting, line endings):
#    Files are modified but NOT staged
#    You must re-stage and commit again:

git add src/api/search.py
git commit -m "feat(search): add hybrid search"

# 6. Commit succeeds after all checks pass
```

**When hooks fail**:

```bash
git commit -m "feat(search): add broken code"

# Pre-commit output:
# ❌ ruff..........................Failed
# - src/api/search.py:42:1: F821 Undefined name 'searc_results'

# Fix the issue
vim src/api/search.py  # Fix typo: searc_results → search_results

# Stage fix
git add src/api/search.py

# Commit again (hooks will re-run)
git commit -m "feat(search): add hybrid search"

# ✅ All checks pass → Commit created
```

### Handling Hook Failures (CRITICAL)

**❌ WRONG - Never amend after hook failure**:

```bash
git commit -m "feat: add feature"
# Hooks fail

# ❌ DON'T DO THIS - amends PREVIOUS commit!
git commit --amend

# ❌ DON'T DO THIS - bypasses hooks
git commit --no-verify
```

**✅ CORRECT - Fix issue and create NEW commit**:

```bash
git commit -m "feat: add feature"
# Hooks fail (e.g., formatting)

# Hooks may have auto-fixed files - re-stage them
git add .

# Commit again (NEW commit, not amend)
git commit -m "feat: add feature"

# OR if you need to fix manually:
# 1. Fix the issue (run formatter, fix linting error)
black src/
# 2. Stage the fix
git add src/
# 3. Create NEW commit
git commit -m "style: fix formatting from pre-commit hook"
```

### Installing Pre-commit in CI (Safety Net)

Even with pre-commit hooks, run checks in CI as a safety net (developers can bypass with `--no-verify`):

**GitHub Actions** (see `references/ci-cd-workflow.md`):

```yaml
name: Pre-commit Checks

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: pre-commit/action@v3.0.0
```

### Skipping Hooks (Only When Explicitly Requested)

**NEVER skip hooks** unless user explicitly requests it:

```bash
# Only use when user explicitly says "skip hooks" or "bypass pre-commit"
git commit --no-verify -m "feat: emergency hotfix"
```

**When to skip** (rare):
- Emergency hotfix (production down, need immediate fix)
- Hook is broken and blocking all commits
- User explicitly requests it

**When NOT to skip** (always):
- "Hooks are slow" (fix the hooks, don't skip them)
- "Formatting is annoying" (that's the point, it enforces consistency)
- "Already checked locally" (hooks ensure consistency)

### Troubleshooting Pre-commit Hooks

**Hook fails with "command not found"**:

```bash
# Python tools not installed
pip install black ruff mypy

# Node tools not installed (if using ESLint/Prettier via pre-commit)
npm install -g eslint prettier

# Dart tools not in PATH
export PATH="$PATH:$HOME/flutter/bin"
```

**Hooks are too slow**:

```bash
# Only run on changed files (default behavior)
# If running on all files, that's the issue

# Speed up by removing slow hooks (e.g., tests)
# Edit .pre-commit-config.yaml and remove test hooks

# Run specific hook manually
pre-commit run black --all-files
```

**Line endings still getting messed up**:

```bash
# Ensure mixed-line-ending hook is configured
# In .pre-commit-config.yaml:

- id: mixed-line-ending
  args: ['--fix=lf']  # Force LF, not CRLF

# Also configure git to not auto-convert line endings
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows (convert to LF on commit)
```

**Developer keeps bypassing hooks**:

```bash
# Enforce in CI pipeline (they can bypass locally but not in CI)
# See references/ci-cd-workflow.md for CI configuration

# Educational approach: Explain why hooks exist
# - Catch bugs before they reach code review
# - Prevent embarrassing "fix formatting" commits
# - Ensure consistent code style across team
```

### Australian English in Configuration

All configuration files, commit messages, and comments use **Australian English spelling**:

```yaml
# ✅ CORRECT
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        # Normalise code formatting across the team

# ❌ WRONG
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        # Normalize code formatting across the team
```

## Workflows

### 1. Starting New Work

**Check config file first** (if this is a project-specific workflow):
```bash
cat .git/config | grep -A 2 "\[remote \"origin\"\]"
```

**Start from develop**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-X-story-Y.Z-description
```

**Never start from**:
- ❌ main (unless hotfix)
- ❌ Another feature branch
- ❌ Stale local develop

### 2. Making Commits

**Before committing**, run git status to review changes:
```bash
git status
git diff  # Review unstaged changes
git diff --staged  # Review staged changes
```

**Commit workflow** (with automatic linting):
```bash
# Stage specific files
git add src/module/file.py tests/test_file.py

# Commit with conventional format (Australian English!)
git commit -m "type(scope): description

Detailed explanation if needed.

Relates to Story X.Y"

# Pre-commit hooks run automatically:
# ✅ Formatting (black/prettier/dart format)
# ✅ Linting (ruff/eslint/dart analyze)
# ✅ Line ending normalization (fixes CRLF → LF)
# ✅ Secrets detection
# ✅ Type checking (mypy for Python)

# If hooks make changes (e.g., formatting), re-stage and commit:
git add src/module/file.py tests/test_file.py
git commit -m "type(scope): description"
```

**Available types**:
- `feat`: New feature (MINOR in semver)
- `fix`: Bug fix (PATCH in semver)
- `docs`: Documentation changes
- `refactor`: Code restructure (no behaviour change)
- `test`: Adding/updating tests
- `chore`: Build process, dependencies
- `perf`: Performance improvement
- `style`: Code formatting (no logic change)

**Available scopes**: Match module structure or story-based
- `api`, `auth`, `retrieval`, `embeddings`, `pipeline`, `opensearch`
- Or: `story-1.3`, `epic-2`

### 3. Creating Pull Requests

**Use `gh` CLI** (NOT git commands for PRs):

```bash
# Step 1: Run your test suite and capture results
<run your project's test command with coverage>

# Step 2: Push branch
git push -u origin feature/epic-1-story-1.3-hybrid-search

# CI automatically runs on push:
# ✅ Pre-commit checks (formatting, linting, line endings)
# ✅ Test suite with coverage
# ✅ Build verification
# ✅ Security scanning
# View status: gh pr checks

# Step 3: Create PR with test results
gh pr create \
  --base develop \
  --title "[Epic 1 / Story 1.3] Implement hybrid search" \
  --body-file <(cat <<'EOF'
## Summary
Brief description of changes (1-2 sentences)

## Story/Issue
Implements Story 1.3: Hybrid Search Service
Fixes #42

## Changes
- Bullet list of key changes
- Focus on what changed, not implementation details

## Test Results
All 42 tests passing ✅

\`\`\`
<paste your test output here>
======================== 42 passed in 2.15s =========================

Coverage: 89% (target: >80%)
\`\`\`

## Checklist
- [x] All tests pass (42/42)
- [x] Coverage >80% (89%)
- [x] Australian English spelling used throughout
- [x] Type safety/strong typing used
- [x] Code documentation added
- [x] Error handling follows best practices
- [x] Linting/formatting passes
- [x] No secrets committed
- [x] Documentation updated (if needed)
EOF
)

# Step 4: CRITICAL - Verify target branch
gh pr view --json baseRefName
# Should show: "baseRefName": "develop"
```

**CRITICAL**: Always include test results AND coverage in the PR description or first comment.

See `references/pr-template.md` for language-specific examples.

### 4. Reviewing Pull Requests

**Use `gh` CLI for review**:

```bash
# View PR details
gh pr view 42

# Check CI status (automatic linting, tests, build)
gh pr checks 42
# Should show:
# ✅ Pre-commit checks - All hooks passed
# ✅ Test suite - 288/288 passing, 89% coverage
# ✅ Build - Success
# ✅ Security scan - No vulnerabilities

# Check out PR locally for testing
gh pr checkout 42

# Run tests locally
pytest

# Verify code quality (already checked by CI, but review manually):
# - Australian English spelling
# - Code follows design proposal
# - Type safety/strong typing
# - Error handling
# - Test quality

# Leave review
gh pr review 42 --approve -b "LGTM - all CI checks pass, tests pass, code looks good"

# Or request changes
gh pr review 42 --request-changes -b "Please add type hints to the new functions"
```

See `references/pr-review.md` for review checklist.

### 5. Merging Pull Requests

**After approval**, merge using merge commit strategy:

```bash
# CRITICAL: Verify target branch first
gh pr view 42 --json baseRefName
# Expected: "baseRefName": "develop"

# Merge with merge commit (NOT squash/rebase)
gh pr merge 42 --merge --delete-branch

# If merge conflicts, resolve locally first
gh pr checkout 42
git fetch origin develop
git merge origin/develop
# ... resolve conflicts ...
git push
```

### 6. Hotfix Workflow (main branch)

**ONLY for urgent production fixes**:

```bash
# Start from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-auth-bypass

# ... make fix, commit ...

# Create PR targeting main
gh pr create --base main --title "[Hotfix] Fix critical auth bypass" --body "..."

# After merge to main, also merge to develop
git checkout develop
git merge main
git push origin develop
```

## Git Commands Reference

### Check Status
```bash
git status                    # Working tree status
git branch --show-current     # Current branch name
git log --oneline -10         # Recent commits
git diff                      # Unstaged changes
git diff --staged             # Staged changes
git diff develop...HEAD       # Changes since branching from develop
```

### Branch Operations
```bash
git checkout develop          # Switch to develop
git pull origin develop       # Update develop
git checkout -b feature/...   # Create new branch
git branch -d feature/...     # Delete local branch (safe)
git push origin --delete feature/...  # Delete remote branch
```

### Commit Operations
```bash
git add src/file.py           # Stage specific file
git commit -m "message"       # Commit with message
git commit --amend            # Amend last commit (AVOID after push!)
git log --oneline -5          # View recent commits
```

### Remote Operations
```bash
git push -u origin feature/...  # Push and set upstream
git push                        # Push to upstream
git fetch origin                # Fetch remote changes
git pull origin develop         # Pull and merge
```

## GitHub CLI (`gh`) Commands

**Preferred over git for GitHub operations**:

### PR Operations
```bash
gh pr create --base develop --title "..." --body "..."
gh pr view 42
gh pr view 42 --json baseRefName  # Check target branch
gh pr checkout 42
gh pr review 42 --approve
gh pr review 42 --request-changes
gh pr merge 42 --merge --delete-branch
gh pr list
gh pr list --state open --author @me
```

### Issue Operations
```bash
gh issue view 42
gh issue create --title "..." --body "..."
gh issue list
gh issue comment 42 --body "..."
```

### Repository Operations
```bash
gh repo view
gh repo clone owner/repo
gh pr checks  # View CI/CD status
```

## Common Scenarios

### Scenario: Started branch from wrong base
```bash
# You're on feature/my-branch but it came from main instead of develop
git checkout develop
git pull origin develop
git checkout -b feature/my-branch-fixed
git merge feature/my-branch
# Delete old branch
git branch -D feature/my-branch
git push origin --delete feature/my-branch
```

### Scenario: Need to update branch with latest develop
```bash
git checkout develop
git pull origin develop
git checkout feature/my-branch
git merge develop  # Merge commit (preferred)
# OR: git rebase develop  # Only if not pushed yet
```

### Scenario: Pre-commit hook failed
```bash
# ❌ WRONG - Don't amend!
git commit --amend

# ✅ CORRECT - Fix issue and create NEW commit
# Fix the issue (e.g., run formatter)
black src/
git add src/
git commit -m "style: fix formatting issues from pre-commit hook"
```

### Scenario: Accidentally committed to wrong branch
```bash
# You committed to develop instead of feature branch
git log -1  # Note the commit hash
git reset HEAD~1  # Undo commit, keep changes
git checkout -b feature/epic-1-story-1.3-my-feature
git add .
git commit -m "..."  # Commit on correct branch
```

## Australian English Reminder

All commit messages, PR titles, PR descriptions, and code comments must use **Australian English spelling**:

- ✅ normalise, organisation, authorisation, optimise, colour, behaviour
- ❌ normalize, organization, authorization, optimize, color, behavior

This is a **project-wide standard**, not optional.

## Related Skills

- **developer-analysis** - Pre-implementation analysis, POC scripts, design proposals (use BEFORE starting implementation)
- **agile-board** - For creating GitHub issues from stories and **ticket update workflow** (see `agile-board/references/ticket-workflow.md`)
- **project-management** - For story/epic structure

## References

See `references/` folder for detailed guides:
- `branch-naming.md` - Branch naming conventions
- `commit-format.md` - **Commit message format, AC marking workflow**
- `pr-template.md` - **Pull request template, AC completion checking, story update workflow**
- `pr-review.md` - **PR review checklist with AC verification**
- `ci-cd-workflow.md` - **CI/CD pipeline configuration, automated testing, deployment strategies**

**Pre-commit hooks** (this file):
- See "Pre-commit Hooks & Automated Quality Checks" section above for:
  - Automated installation for Python, TypeScript, Flutter projects
  - Line ending normalization (fixes Windows/Mac issues)
  - Multi-layer linting strategy (IDE → Pre-commit → CI)
  - Language-specific configurations

**For ticket update workflow** (marking ACs, posting comments, updating story descriptions):
- See `agile-board/references/ticket-workflow.md` for complete workflow across commit → PR → review
