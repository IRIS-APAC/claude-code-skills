# Linear Reference

Board-specific implementation details for Linear integration.

**Status**: ⚠️ PLACEHOLDER - Not yet implemented

**Official docs**: https://developers.linear.app/docs/graphql/working-with-the-graphql-api

---

## Why This is a Placeholder

The `agile-board` skill currently supports **ZenHub** through MCP tools. Linear integration is planned but not yet implemented.

**To use Linear today**: Use the Linear web UI or official Linear CLI tools directly.

**For reference implementation**: See [zenhub.md](zenhub.md) for the working pattern this file should follow.

## Planned Integration Approach

Linear integration will use the **Linear GraphQL API** for:

1. **Creating Issues** - `issueCreate` mutation
2. **Setting Estimates** - `estimate` field (1-10 scale or custom)
3. **Managing Cycles** - Add issues to cycles (Linear's sprint equivalent)
4. **Updating Issue Status** - Transition through workflow states
5. **Linking Issues** - Parent/child relationships via `parentId`

## Configuration Format

When implemented, values will come from `.claude/agile-board-config.json`:

```json
{
  "board_type": "linear",
  "team_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "workspace_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "api_key": "lin_api_xxxxxxxxxxxxxxxxxxxxx",
  "default_state_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "default_project_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Authentication**: Linear API key (generated from https://linear.app/settings/api)

## Example GraphQL Queries (Future Implementation)

### Create Issue with Estimate

```graphql
mutation CreateIssue {
  issueCreate(
    input: {
      teamId: "team-id-here"
      title: "Story 1.3: Implement hybrid search"
      description: "Story description with acceptance criteria"
      estimate: 5
      stateId: "state-id-for-backlog"
      projectId: "project-id-here"
      labelIds: ["label-id-1", "label-id-2"]
    }
  ) {
    success
    issue {
      id
      identifier
      title
      estimate
    }
  }
}
```

### Set Estimate (Update Existing Issue)

```graphql
mutation UpdateEstimate {
  issueUpdate(
    id: "issue-id-here"
    input: {
      estimate: 8
    }
  ) {
    success
    issue {
      id
      estimate
    }
  }
}
```

### Link Issue to Parent (Epic)

```graphql
mutation LinkToParent {
  issueUpdate(
    id: "child-issue-id"
    input: {
      parentId: "parent-issue-id"
    }
  ) {
    success
    issue {
      id
      parent {
        id
        title
      }
    }
  }
}
```

### Add Issue to Cycle (Sprint)

```graphql
mutation AddToCycle {
  issueUpdate(
    id: "issue-id-here"
    input: {
      cycleId: "cycle-id-here"
    }
  ) {
    success
    issue {
      id
      cycle {
        id
        name
      }
    }
  }
}
```

### Query Team States (Workflow States)

```graphql
query TeamStates {
  team(id: "team-id-here") {
    states {
      nodes {
        id
        name
        type
      }
    }
  }
}
```

## Key Differences from ZenHub

| Aspect | ZenHub | Linear |
|--------|--------|--------|
| **Issues** | GitHub issues | Linear issues (native) |
| **Story points** | `setIssueEstimate` API | `estimate` field (1-10 or custom) |
| **Epic linking** | `setParentForIssues` | `parentId` field |
| **Labels** | GitHub labels (immutable) | Linear labels (can update) |
| **Sprints** | ZenHub sprints | Cycles (with start/end dates) |
| **API** | GraphQL | GraphQL |
| **Authentication** | ZenHub API token | Linear API key |
| **Identifiers** | GitHub issue numbers | UUIDs and short identifiers (e.g., ENG-123) |

## Implementation Checklist

When implementing Linear support:

- [ ] Create Linear MCP server or GraphQL client
- [ ] Add Linear setup flow to `scripts/setup.py`
- [ ] Implement issue creation with estimates
- [ ] Implement estimate updates
- [ ] Implement parent/child relationships
- [ ] Add cycle (sprint) management
- [ ] Add state (status) transitions
- [ ] Test with Linear Free and Linear Pro accounts
- [ ] Document team/project/state ID discovery
- [ ] Update main [SKILL.md](../SKILL.md) with Linear examples
- [ ] Add Linear-specific error handling

## Finding IDs in Linear

Linear uses UUIDs for most entities. To find IDs:

### Via Linear GraphQL API Explorer

Visit: https://linear.app/YOUR-WORKSPACE/settings/api

**Find Team ID**:
```graphql
query {
  teams {
    nodes {
      id
      name
      key
    }
  }
}
```

**Find Project IDs**:
```graphql
query {
  projects {
    nodes {
      id
      name
      state
    }
  }
}
```

**Find State IDs** (workflow states):
```graphql
query {
  team(id: "your-team-id") {
    states {
      nodes {
        id
        name
        type
      }
    }
  }
}
```

**Find Cycle IDs** (active cycles):
```graphql
query {
  cycles(filter: { isActive: { eq: true } }) {
    nodes {
      id
      name
      number
      startsAt
      endsAt
    }
  }
}
```

## Linear Estimate Scale

Linear supports two estimate types:

1. **Default (1-10)**: 1, 2, 3, 5, 8 (Fibonacci-like)
2. **Custom**: T-shirt sizes (XS=1, S=2, M=3, L=5, XL=8)

Map T-shirt sizing to Linear estimates:

| T-shirt | Linear Estimate |
|---------|-----------------|
| XS (1)  | 1               |
| S (3)   | 3               |
| M (5)   | 5               |
| L (8)   | 8               |
| XL (13) | 10 (max)        |

## Contributing

Want to implement Linear support? Follow the pattern in [zenhub.md](zenhub.md):

1. Document GraphQL mutations and queries
2. Provide field mapping examples
3. Include error handling patterns
4. Add board-specific limitations (e.g., estimate scale)
5. Reference official Linear API docs

**Contributions welcome!** Open a PR or issue at the skill repository.
