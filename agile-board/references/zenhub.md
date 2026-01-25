# ZenHub Reference

Board-specific implementation details for ZenHub integration.

**Official docs**: https://developers.zenhub.com/

## Configuration

Values come from `.claude/agile-board-config.json` in your project directory.

**Required fields**:
- `workspace_id` - From ZenHub workspace URL or MCP
- `repository_id` - GraphQL ID of GitHub repository
- `organization_id` - From MCP: `getWorkspacePipelinesAndRepositories`
- `default_pipeline_id` - Pipeline to use for new issues
- `default_labels` - Labels to add to new issues

## MCP Tools

The ZenHub MCP server provides these tools via `mcp__zenhub__*`:

### Workspace & Metadata
- `getWorkspacePipelinesAndRepositories()` - Get workspace structure, pipeline IDs, repo IDs
- `getTeamMembers()` - Get ZenHub user IDs and GitHub usernames
- `getIssueTypes(repositoryId)` - Get all issue type IDs

### Search & Retrieval
- `searchLatestIssues(query)` - Search for issues by text
- `getIssuesInPipeline(pipelineId, repositoryIds)` - List issues in specific pipeline
- `getActiveSprint()` - Get current sprint with issues and metadata
- `getUpcomingSprint()` - Get next sprint with issues and metadata

### Issue Creation
- `createGitHubIssue(repositoryId, title, body, labels, assignees)` - **PREFERRED** - Create GitHub issue
- `createZenhubIssue(repositoryId, title, body, labels)` - Create ZenHub-native issue (use sparingly)

### Issue Configuration
- `setIssueType(issueIds, issueTypeId)` - Set Epic/Feature/Bug/Task type
- `setIssueEstimate(issueId, estimate)` - **CRITICAL** - Set story points in dedicated field
- `assignIssues(issueIds, assigneeIds)` - Assign to team members (use GitHub user IDs)

### Issue Relationships
- `setParentForIssues(parentIssueId, childIssueIds)` - Link stories to epics
- `createBlockage(blockingIssueId, blockedIssueId)` - Create dependency
- `setDatesForIssue(issueId, startDate, endDate, zenhubOrganizationId)` - Set epic/project dates

### Pipeline Management
- `moveIssueToPipeline(issueId, pipelineId)` - Move issue to different column

### Updates
- `updateIssue(issueId, title, body, state)` - Update existing issue

## Common Issue Type IDs

Get all types with `getIssueTypes()`. Common IDs:

| Type | ID | Level | Usage |
|------|-----|-------|-------|
| Epic | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0NjU` | 3 | High-level feature areas |
| Feature | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0Njg` | 4 | **User stories** (most common) |
| Bug | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0NjY` | 4 | Bug fixes |
| Task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0Njc` | 4 | Generic tasks |
| Sub-task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0Njk` | 5 | Feature breakdown |

## Critical Rules

### 1. Always Use GitHub Issues (NOT ZenHub-native)

✅ **Correct**:
```python
mcp__zenhub__createGitHubIssue(...)
```

❌ **Avoid**:
```python
mcp__zenhub__createZenhubIssue(...)  # Only for non-code work items
```

**Why GitHub issues**:
- Enables `gh` CLI automation
- Programmatic label management
- Better GitHub integration (PRs, code references)
- Syncs to ZenHub automatically

### 2. Set Story Points in Dedicated Field (NEVER in description)

✅ **Correct**:
```python
mcp__zenhub__setIssueEstimate(issueId=issue["id"], estimate=5)
```

❌ **Wrong**:
```python
# Don't put story points in title or body
title="Story 1.3: Implement hybrid search (5 points)"  # Wrong!
body="## Estimate\n5 story points"  # Wrong!
```

**For T-shirt sizing guide**, see `project-management` skill.

### 3. Labels Cannot Be Updated After Creation

✅ **Correct**:
```python
# Add all labels at creation
mcp__zenhub__createGitHubIssue(..., labels=["epic-1", "story", "backend", "python"])
```

❌ **Won't work**:
```python
# Can't update labels via ZenHub API
mcp__zenhub__updateIssue(..., labels=[...])  # Not supported
```

**Workaround**: Use ZenHub web UI to modify labels after creation.

### 4. Use Checkbox Format for Acceptance Criteria

✅ **Correct**:
```markdown
## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Session expires after 24 hours
```

❌ **Avoid**:
```markdown
## Acceptance Criteria
* User can log in
* Session expires
```

## Example: Complete Story Creation

```python
# Step 1: Create GitHub issue
story = mcp__zenhub__createGitHubIssue(
    repositoryId="Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzMyMzU0",
    title="Story 1.3: Implement hybrid search service",
    body="""## Description
Implement hybrid search combining BM25 keyword search with vector semantic search.

## Context
Current search only uses BM25. Need vector search for semantic queries.

## Acceptance Criteria
- [ ] Configure OpenSearch hybrid query with BM25 + kNN
- [ ] Implement RRF score normalisation
- [ ] Add filter allowlist enforcement

## Technical Notes
- Use OpenSearch hybrid query type
- Set RRF normalisation in search pipeline
""",
    labels=["epic-1", "phase-2a", "story", "backend", "python"]
)

# Step 2: Set issue type to Feature
mcp__zenhub__setIssueType(
    issueIds=[story["id"]],
    issueTypeId="Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zNjY0Njg"
)

# Step 3: Set story points
mcp__zenhub__setIssueEstimate(
    issueId=story["id"],
    estimate=5  # See project-management skill for sizing
)

# Step 4: Link to parent epic
mcp__zenhub__setParentForIssues(
    parentIssueId="Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NDg4Nzc2NA",
    childIssueIds=[story["id"]]
)

# Step 5: Move to Product Backlog (if needed)
mcp__zenhub__moveIssueToPipeline(
    issueId=story["id"],
    pipelineId="Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjUwMzk"
)
```

## Advanced: Direct GraphQL API Usage

For operations not available in MCP, use the ZenHub GraphQL API directly.

**API endpoint**: `https://api.zenhub.com/public/graphql`

**Authentication**: Bearer token in `Authorization` header

### Setup: Fetching Workspaces and Pipelines

**During initial setup**, the MCP server isn't configured yet (it requires workspace ID). Use GraphQL API:

#### Step 1: Get ZenHub API Token

Get token from app.zenhub.com → Settings → API Tokens (starts with `zh_`)

#### Step 2: Get GitHub Repository ID

Auto-detect using `gh` CLI:
```bash
gh api graphql -f 'query={repository(owner:"$OWNER",name:"$REPO"){id,nameWithOwner}}'
```

Returns: `R_kgDOxxxxxx` (GraphQL ID)

#### Step 3: Search Workspaces by Name

**CRITICAL**: ZenHub requires a search query - you cannot list all workspaces. Ask user for workspace name, then search:

```bash
curl -s -X POST https://api.zenhub.com/public/graphql \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { viewer { searchWorkspaces(query: \"My Workspace\") { nodes { id name repositoriesConnection { nodes { id name ghId } } } } } }"}' \
  | python3 -m json.tool
```

**Response** (note: `id` is **numeric format**, not GraphQL format):
```json
{
  "data": {
    "viewer": {
      "searchWorkspaces": {
        "nodes": [
          {
            "id": "6948c3baf35cc40021db26f7",
            "name": "My Workspace",
            "repositoriesConnection": {
              "nodes": [
                {
                  "id": "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzMyMzU0",
                  "name": "my-repo",
                  "ghId": 1120767896
                }
              ]
            }
          }
        ]
      }
    }
  }
}
```

#### Step 4: Get Pipelines and Organization ID

**Use the numeric workspace ID** from Step 3 directly (no conversion needed):

```bash
curl -s -X POST https://api.zenhub.com/public/graphql \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { workspace(id: \"6948c3baf35cc40021db26f7\") { pipelinesConnection { nodes { id name } } zenhubOrganization { id } } }"}' \
  | python3 -m json.tool
```

**Response** (pipelines are GraphQL format, org ID is GraphQL format):
```json
{
  "data": {
    "workspace": {
      "pipelinesConnection": {
        "nodes": [
          {
            "id": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjU0NTc",
            "name": "Product Backlog"
          },
          {
            "id": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjU0NTg",
            "name": "Sprint Backlog"
          },
          {
            "id": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjU0NTk",
            "name": "In Progress"
          }
        ]
      },
      "zenhubOrganization": {
        "id": "Z2lkOi8vcmFwdG9yL1plbmh1Yk9yZ2FuaXphdGlvbi8xNjMyMjY"
      }
    }
  }
}
```

#### Complete Automated Setup Flow

**End-to-end process**:

1. **Get ZenHub API token** - From user or args
2. **Get GitHub repo ID** - Auto-detect via `gh` CLI
3. **Ask for workspace name** - Via conversation (cannot list all workspaces)
4. **Search workspaces** - Via `viewer.searchWorkspaces(query: "name")`
   - Returns: Numeric workspace IDs
5. **Show workspace selection** - Via `AskUserQuestion` GUI (let user select from search results)
6. **Fetch pipelines + org ID** - Via `workspace(id: "numeric-id")`
   - Returns: Pipeline IDs (GraphQL) + Organization ID (GraphQL)
7. **Show pipeline selection** - Via `AskUserQuestion` GUI (let user select default pipeline)
8. **Get default labels** - Via conversation (optional user input)
9. **Run setup script** - Non-interactively with all collected values as CLI arguments

### Adding Issues to Sprint

MCP provides `getActiveSprint()` and `getUpcomingSprint()` but NOT adding issues to sprints. Use GraphQL API:

```bash
curl -s -X POST https://api.zenhub.com/public/graphql \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation {
      addIssuesToSprints(input: {
        sprintIds: [\"Z2lkOi8vcmFwdG9yL1NwcmludC80NDQxMzY2\"],
        issueIds: [
          \"Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NDg5MjE5Mg\",
          \"Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NDg5MjE5NA\",
          \"Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NDg5MjE5OA\"
        ]
      }) {
        __typename
      }
    }"
  }'
```

### Removing Issues from Sprint

```bash
curl -s -X POST https://api.zenhub.com/public/graphql \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation {
      removeIssuesFromSprints(input: {
        sprintIds: [\"Z2lkOi8vcmFwdG9yL1NwcmludC80NDQxMzY2\"],
        issueIds: [\"Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NDg5MjE5Mg\"]
      }) {
        __typename
      }
    }"
  }'
```

### Get Sprint Issues with Estimates

```bash
curl -s -X POST https://api.zenhub.com/public/graphql \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query {
      sprintByInfo(workspaceId: \"6948c3baf35cc40021db26f7\", sprintNumber: 1) {
        id
        name
        state
        issues {
          nodes {
            id
            title
            estimate {
              value
            }
            state
          }
        }
      }
    }"
  }'
```

### Bulk Operations

For bulk operations (e.g., creating multiple stories from requirements), use GraphQL mutations in a loop or batched request.

**See ZenHub API docs** for full GraphQL schema: https://developers.zenhub.com/graphql-api-docs/

## Sprint Planning Workflow

**Using MCP + GraphQL API**:

1. **Get current sprint**:
   ```python
   sprint = mcp__zenhub__getActiveSprint()
   sprint_id = sprint["id"]
   ```

2. **Get backlog issues**:
   ```python
   backlog_issues = mcp__zenhub__getIssuesInPipeline(
       pipelineId="Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM1MjUwMzk",
       repositoryIds=["Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzMyMzU0"]
   )
   ```

3. **Select issues** (based on estimates and velocity)

4. **Add to sprint** (via GraphQL API):
   ```bash
   curl -X POST https://api.zenhub.com/public/graphql \
     -H "Authorization: Bearer $API_TOKEN" \
     -d '{"query":"mutation{addIssuesToSprints(input:{sprintIds:[\"$SPRINT_ID\"],issueIds:$ISSUE_IDS}){__typename}}"}'
   ```

5. **Move to Sprint Backlog pipeline**:
   ```python
   for issue in selected_issues:
       mcp__zenhub__moveIssueToPipeline(
           issueId=issue["id"],
           pipelineId=sprint_backlog_pipeline_id
       )
   ```

## Troubleshooting

### Issue: "Cannot find workspace"

**Solution**: Check `workspace_id` in `.claude/agile-board-config.json` matches MCP config in `~/.claude.json`

### Issue: "Insufficient permissions"

**Solution**: Verify API token in `~/.claude.json` is valid and has workspace access

### Issue: "Labels not updating"

**Cause**: ZenHub API doesn't support updating labels after creation

**Solution**: Use ZenHub web UI or GitHub API to modify labels

### Issue: "Story points not showing"

**Cause**: Estimate not set in dedicated field

**Solution**: Use `setIssueEstimate()`, not description

## Related Skills & Docs

- **project-management skill** - T-shirt sizing, sprint workflows, story templates
- **ZenHub API docs** - https://developers.zenhub.com/
- **ZenHub GraphQL explorer** - https://api.zenhub.com/public/graphql (interactive)
