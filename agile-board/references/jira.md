# Jira Reference

Board-specific implementation details for Jira integration.

**Status**: ⚠️ PLACEHOLDER - Not yet implemented

**Official docs**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

---

## Why This is a Placeholder

The `agile-board` skill currently supports **ZenHub** through MCP tools. Jira integration is planned but not yet implemented.

**To use Jira today**: Use the Jira web UI or official Jira CLI tools directly.

**For reference implementation**: See [zenhub.md](zenhub.md) for the working pattern this file should follow.

## Planned Integration Approach

Jira integration will use the **Jira REST API v3** for:

1. **Creating Issues** - `POST /rest/api/3/issue`
2. **Setting Story Points** - Update custom field (typically `customfield_10016`)
3. **Managing Sprints** - Jira Agile API endpoints
4. **Updating Issue Status** - Transition issues through workflow states
5. **Linking Issues** - Parent/child epic relationships

## Configuration Format

When implemented, values will come from `.claude/agile-board-config.json`:

```json
{
  "board_type": "jira",
  "jira_url": "https://your-company.atlassian.net",
  "project_key": "PROJ",
  "board_id": "123",
  "api_token": "from-environment-variable",
  "custom_fields": {
    "story_points": "customfield_10016",
    "epic_link": "customfield_10014"
  }
}
```

**Authentication**: Jira API tokens (generated from https://id.atlassian.com/manage-profile/security/api-tokens)

## Example API Calls (Future Implementation)

### Create Issue with Story Points

```bash
curl -X POST https://your-company.atlassian.net/rest/api/3/issue \
  -H "Authorization: Basic $(echo -n email@example.com:API_TOKEN | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Story 1.3: Implement hybrid search",
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [{"type": "text", "text": "Story description here"}]
          }
        ]
      },
      "issuetype": {"name": "Story"},
      "customfield_10016": 5
    }
  }'
```

### Set Story Points (Update Existing Issue)

```bash
curl -X PUT https://your-company.atlassian.net/rest/api/3/issue/PROJ-123 \
  -H "Authorization: Basic $(echo -n email@example.com:API_TOKEN | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "customfield_10016": 8
    }
  }'
```

### Link Issue to Epic

```bash
curl -X PUT https://your-company.atlassian.net/rest/api/3/issue/PROJ-123 \
  -H "Authorization: Basic $(echo -n email@example.com:API_TOKEN | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "customfield_10014": "PROJ-100"
    }
  }'
```

## Key Differences from ZenHub

| Aspect | ZenHub | Jira |
|--------|--------|------|
| **Issues** | GitHub issues | Jira issues (separate from GitHub) |
| **Story points** | `setIssueEstimate` API | Custom field update |
| **Epic linking** | `setParentForIssues` API | Custom field (`epic_link`) |
| **Labels** | GitHub labels (immutable after creation) | Jira labels (can update) |
| **API** | GraphQL | REST v3 |
| **Authentication** | ZenHub API token | Jira API token + base64 email |

## Implementation Checklist

When implementing Jira support:

- [ ] Create Jira MCP server (or use REST API directly)
- [ ] Add Jira setup flow to `scripts/setup.py`
- [ ] Implement issue creation with custom fields
- [ ] Implement story point setting
- [ ] Implement epic linking
- [ ] Add sprint management (Jira Agile API)
- [ ] Test with Jira Cloud and Jira Server
- [ ] Document custom field discovery (varies by Jira instance)
- [ ] Update main [SKILL.md](../SKILL.md) with Jira examples
- [ ] Add Jira-specific error handling

## Finding Custom Field IDs

Jira custom fields vary by instance. To find your story points field:

```bash
# List all fields
curl -X GET https://your-company.atlassian.net/rest/api/3/field \
  -H "Authorization: Basic $(echo -n email@example.com:API_TOKEN | base64)"

# Look for fields with name like "Story Points", "Story point estimate"
# Common IDs: customfield_10016, customfield_10021
```

## Contributing

Want to implement Jira support? Follow the pattern in [zenhub.md](zenhub.md):

1. Document MCP tools or API calls
2. Provide field mapping examples
3. Include error handling patterns
4. Add board-specific limitations
5. Reference official Jira API docs

**Contributions welcome!** Open a PR or issue at the skill repository.
