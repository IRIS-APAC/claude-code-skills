# Branch Naming Conventions

## GitFlow Branch Types

This project follows **GitFlow** branching model with strict naming conventions.

```
main (production)
  └── develop (integration)
       ├── feature/epic-X-story-Y.Z-description
       ├── bugfix/description
       └── hotfix/description (from main)
```

## Branch Naming Patterns

| Branch Type | Pattern | Example | Target | Purpose |
|-------------|---------|---------|--------|---------|
| **Feature** | `feature/epic-X-story-Y.Z-description` | `feature/epic-1-story-1.3-hybrid-search` | develop | New functionality from requirements |
| **Bugfix** | `bugfix/description` | `bugfix/fix-embedding-timeout` | develop | Bug fixes for develop/feature branches |
| **Hotfix** | `hotfix/description` | `hotfix/critical-auth-bypass` | main | Urgent production fixes (from main) |
| **Release** | `release/vX.Y.Z` | `release/v1.0.0` | main | Release preparation |

## Feature Branch Naming

**Format**: `feature/epic-X-story-Y.Z-description`

**Examples**:
- `feature/epic-1-story-1.1-opensearch-setup`
- `feature/epic-1-story-1.3-hybrid-search`
- `feature/epic-2-story-2.1-funnelback-connector`
- `feature/epic-4-story-4.8-caption-generation`

**Rules**:
- Must include epic and story numbers if from requirements
- Description uses kebab-case (hyphens)
- Keep description concise but clear (3-5 words)
- Use Australian English spelling

**Creating**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-1-story-1.3-hybrid-search
```

## Bugfix Branch Naming

**Format**: `bugfix/description`

**Examples**:
- `bugfix/fix-auth-token-validation`
- `bugfix/fix-embedding-timeout`
- `bugfix/correct-filter-normalisation`

**Rules**:
- Start with `fix-` for clarity
- Description uses kebab-case
- Targets develop branch (NOT main)
- For production bugs, use hotfix instead

**Creating**:
```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-auth-token-validation
```

## Hotfix Branch Naming

**Format**: `hotfix/description`

**Examples**:
- `hotfix/critical-auth-bypass`
- `hotfix/opensearch-connection-leak`

**Rules**:
- ONLY for urgent production fixes
- Branches from main
- Merges to main AND develop
- Requires immediate attention

**Creating**:
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-auth-bypass
```

**After merging to main**:
```bash
# Also merge to develop
git checkout develop
git merge main
git push origin develop
```

## Release Branch Naming

**Format**: `release/vX.Y.Z`

**Examples**:
- `release/v1.0.0`
- `release/v1.1.0`
- `release/v2.0.0-beta.1`

**Rules**:
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Created from develop
- Merges to main (with tag) AND develop
- Only bug fixes allowed (no new features)

**Creating**:
```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Bump version, update changelog
# Only bug fixes allowed now

# Merge to main
git checkout main
git merge release/v1.0.0 --no-ff
git tag -a v1.0.0 -m "Release v1.0.0: Phase 2a MVP"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge release/v1.0.0
git push origin develop
```

## Branch Lifecycle

### 1. Create from develop
```bash
git checkout develop
git pull origin develop
git checkout -b feature/epic-1-story-1.3-hybrid-search
```

### 2. Work and commit
```bash
# Make changes
git add src/file.py
git commit -m "feat(retrieval): implement hybrid search"
```

### 3. Push to remote
```bash
git push -u origin feature/epic-1-story-1.3-hybrid-search
```

### 4. Create PR targeting develop
```bash
gh pr create --base develop --title "[Epic 1 / Story 1.3] Implement hybrid search"
```

### 5. After merge, delete branch
```bash
gh pr merge 42 --merge --delete-branch
```

## Common Mistakes

### ❌ Wrong: Starting from main
```bash
git checkout main  # Wrong!
git checkout -b feature/my-feature
```

### ✅ Correct: Starting from develop
```bash
git checkout develop  # Correct
git pull origin develop
git checkout -b feature/epic-1-story-1.3-hybrid-search
```

### ❌ Wrong: PR targeting main
```bash
gh pr create --base main  # Wrong for features!
```

### ✅ Correct: PR targeting develop
```bash
gh pr create --base develop  # Correct for features
```

### ❌ Wrong: American English in branch names
```bash
git checkout -b feature/epic-1-story-1.3-normalize-filters  # Wrong!
```

### ✅ Correct: Australian English
```bash
git checkout -b feature/epic-1-story-1.3-normalise-filters  # Correct
```

## Long-Lived Branches

Only two long-lived branches exist:

- **main** - Production code, tagged releases
- **develop** - Integration branch, latest development

All other branches are **short-lived** and deleted after merge.

## Branch Protection Rules

**main**:
- ✅ Requires PR
- ✅ Requires approvals
- ❌ No direct pushes
- ❌ No force pushes
- ✅ Status checks must pass

**develop**:
- ✅ Requires PR
- ✅ Requires approvals
- ❌ No direct pushes
- ✅ Status checks must pass

## Naming Conventions Summary

**DO**:
- ✅ Use epic/story numbers for features
- ✅ Use kebab-case for descriptions
- ✅ Use Australian English spelling
- ✅ Keep names concise (3-5 words)
- ✅ Verify target branch before PR

**DON'T**:
- ❌ Branch from main (unless hotfix)
- ❌ Create long-lived feature branches
- ❌ Use underscores or camelCase
- ❌ Use American English spelling
- ❌ Include redundant words ("feature-" in feature branches)
