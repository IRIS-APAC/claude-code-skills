#!/usr/bin/env python3
"""
Agile Board Setup Wizard

Creates project-local configuration for agile board integration.
Updates:
1. .claude/agile-board-config.json - Project-local board settings
2. ~/.claude.json - MCP server configuration for the project
3. ~/.claude/settings.json - Permission wildcards to auto-approve MCP calls

Supports both interactive and non-interactive modes:
  Interactive: python setup.py
  Non-interactive: python setup.py --board-type zenhub --api-token zh_xxx ...
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Agile Board Setup Wizard - Configure board integration for the current project"
    )
    parser.add_argument('--board-type', choices=['zenhub', 'jira', 'linear'], help='Board type')
    parser.add_argument('--force', action='store_true', help='Overwrite existing config without prompting')

    # ZenHub-specific arguments
    parser.add_argument('--api-token', help='ZenHub API token')
    parser.add_argument('--workspace-id', help='ZenHub workspace ID')
    parser.add_argument('--repository-id', help='GitHub repository ID')
    parser.add_argument('--organization-id', help='ZenHub organization ID')
    parser.add_argument('--default-pipeline-id', help='Default pipeline ID')
    parser.add_argument('--default-pipeline-name', help='Default pipeline name')
    parser.add_argument('--default-labels', help='Comma-separated list of default labels')

    # Jira-specific arguments
    parser.add_argument('--jira-url', help='Jira URL')
    parser.add_argument('--project-key', help='Jira project key')

    # Linear-specific arguments
    parser.add_argument('--team-id', help='Linear team ID')
    parser.add_argument('--linear-workspace-id', help='Linear workspace ID')

    args = parser.parse_args()

    print("🎯 Agile Board Setup Wizard")
    print("=" * 50)
    print()

    # Detect current project directory
    project_dir = Path.cwd()
    config_dir = project_dir / ".claude"
    config_file = config_dir / "agile-board-config.json"

    print(f"📁 Current project: {project_dir}")
    print(f"📝 Config will be saved to: {config_file}")
    print()

    # Check if config already exists
    if config_file.exists():
        if args.force:
            print("⚠️  Overwriting existing config (--force)")
        else:
            print("⚠️  Config file already exists!")
            try:
                overwrite = input("Overwrite existing config? (y/N): ").strip().lower()
                if overwrite != 'y':
                    print("❌ Setup cancelled")
                    sys.exit(0)
            except EOFError:
                print("❌ Config exists and no --force flag provided")
                sys.exit(1)
        print()

    # Determine board type (from args or interactive)
    if args.board_type:
        board_type = args.board_type
        print(f"✅ Board type: {board_type.title()} (from args)")
        print()
    else:
        # Ask which board type
        print("Which agile board do you use?")
        print("  1. ZenHub")
        print("  2. Jira (planned)")
        print("  3. Linear (planned)")
        print()

        board_choice = input("Enter choice (1-3): ").strip()

        board_types = {
            "1": "zenhub",
            "2": "jira",
            "3": "linear"
        }

        if board_choice not in board_types:
            print("❌ Invalid choice")
            sys.exit(1)

        board_type = board_types[board_choice]
        print(f"✅ Selected: {board_type.title()}")
        print()

    # Collect board-specific configuration
    config = {"board_type": board_type}
    mcp_config = None

    if board_type == "zenhub":
        config_data, mcp = setup_zenhub(args)
        config.update(config_data)
        mcp_config = mcp
    elif board_type == "jira":
        config_data, mcp = setup_jira(args)
        config.update(config_data)
        mcp_config = mcp
    elif board_type == "linear":
        config_data, mcp = setup_linear(args)
        config.update(config_data)
        mcp_config = mcp

    # Step 1: Create project-local config
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Project config saved: {config_file}")

    # Step 2: Update ~/.claude.json with MCP server config
    if mcp_config:
        update_claude_json(project_dir, board_type, mcp_config)

    # Step 3: Update ~/.claude/settings.json with permissions
    if mcp_config:
        update_claude_settings(board_type)

    # Step 4: Update .gitignore
    update_gitignore(project_dir)

    print()
    print("🎉 Setup complete!")
    print()
    print("What was configured:")
    print(f"  ✅ {config_file}")
    print(f"  ✅ ~/.claude.json (MCP server for {project_dir})")
    print(f"  ✅ ~/.claude/settings.json (auto-approve {board_type} MCP calls)")
    print()
    print("Next steps:")
    print("  - Restart Claude Code if it's currently running")
    print("  - Use agile-board skill to create issues")
    print(f"  - To reconfigure: rm {config_file} && python {__file__}")


def fetch_github_repo_id():
    """Auto-detect GitHub repository ID from current project"""
    try:
        # Try gh CLI first
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", "query={repository(owner:\"$OWNER\",name:\"$REPO\"){id,nameWithOwner}}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            repo_id = data["data"]["repository"]["id"]
            repo_name = data["data"]["repository"]["nameWithOwner"]
            print(f"✅ Auto-detected repository: {repo_name} (ID: {repo_id})")
            return repo_id
    except Exception:
        pass

    return None


def fetch_zenhub_workspaces(api_token, workspace_name):
    """Fetch ZenHub workspaces by name via GraphQL API

    Args:
        api_token: ZenHub API token
        workspace_name: Workspace name to search for (required - cannot list all)
    """
    import subprocess
    # Escape double quotes in workspace name
    escaped_name = workspace_name.replace('"', '\\"')
    query = f'{{"query": "query {{ viewer {{ searchWorkspaces(query: \\"{escaped_name}\\") {{ nodes {{ id name repositoriesConnection {{ nodes {{ id name ghId }} }} }} }} }} }}"}}'

    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.zenhub.com/public/graphql",
         "-H", f"Authorization: Bearer {api_token}",
         "-H", "Content-Type: application/json",
         "-d", query],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)
        nodes = data.get("data", {}).get("viewer", {}).get("searchWorkspaces", {}).get("nodes", [])
        if not nodes and "errors" in data:
            print(f"⚠️  GraphQL error: {data['errors']}")
        return nodes
    except Exception as e:
        print(f"⚠️  Error parsing workspaces: {e}")
        return None


def fetch_workspace_pipelines(api_token, workspace_id):
    """Fetch pipelines for a specific workspace"""
    query = f'{{"query": "query {{ workspace(id: \\"{workspace_id}\\") {{ pipelinesConnection {{ nodes {{ id name }} }} zenhubOrganization {{ id }} }} }}"}}'

    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.zenhub.com/public/graphql",
         "-H", f"Authorization: Bearer {api_token}",
         "-H", "Content-Type: application/json",
         "-d", query],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None, None

    try:
        data = json.loads(result.stdout)
        workspace_data = data.get("data", {}).get("workspace", {})
        pipelines = workspace_data.get("pipelinesConnection", {}).get("nodes", [])
        org_id = workspace_data.get("zenhubOrganization", {}).get("id")
        return pipelines, org_id
    except Exception as e:
        print(f"⚠️  Error parsing pipelines: {e}")
        return None, None


def setup_zenhub(args):
    """Collect ZenHub-specific configuration"""
    print("ZenHub Configuration")
    print("-" * 50)
    print()

    # Step 1: Get API token
    if args.api_token:
        api_token = args.api_token
        print(f"✅ API Token: {api_token[:10]}... (from args)")
    else:
        print("You'll need a ZenHub API Token:")
        print("  Get it from: app.zenhub.com → Settings → API Tokens")
        print()
        api_token = input("ZenHub API Token (starts with 'zh_'): ").strip()

    print()

    # Step 2: Auto-detect GitHub repository ID
    repository_id = args.repository_id
    if not repository_id:
        repository_id = fetch_github_repo_id()

    if not repository_id:
        print("⚠️  Could not auto-detect GitHub repository ID")
        repository_id = input("GitHub Repository ID (GraphQL ID): ").strip()

    print()

    # Step 3: Fetch and select workspace (if not provided via args)
    workspace_id = args.workspace_id
    if not workspace_id:
        print("To find your workspace, I need to search by name.")
        print("You can get the workspace name from app.zenhub.com")
        print()
        workspace_name = input("Workspace name (or part of it): ").strip()

        if workspace_name:
            print(f"📡 Searching for workspaces matching '{workspace_name}'...")
            workspaces = fetch_zenhub_workspaces(api_token, workspace_name)

            if not workspaces:
                print("⚠️  No workspaces found. Please enter workspace ID manually.")
                print("You can find it at: app.zenhub.com/workspaces/{workspace-id}/...")
                workspace_id = input("Workspace ID: ").strip()
            else:
                print()
                print("Found workspaces:")
                for idx, ws in enumerate(workspaces, 1):
                    print(f"  {idx}. {ws['name']} (ID: {ws['id']})")
                    repos = ws.get('repositoriesConnection', {}).get('nodes', [])
                    if repos:
                        print(f"     Repositories: {', '.join(r['name'] for r in repos)}")
                print()

                if len(workspaces) == 1:
                    workspace_id = workspaces[0]['id']
                    print(f"✅ Selected: {workspaces[0]['name']}")
                else:
                    choice = input(f"Select workspace (1-{len(workspaces)}): ").strip()
                    try:
                        selected_ws = workspaces[int(choice) - 1]
                        workspace_id = selected_ws['id']
                        print(f"✅ Selected: {selected_ws['name']}")
                    except (ValueError, IndexError):
                        print("❌ Invalid choice")
                        sys.exit(1)
        else:
            print("⚠️  Workspace name required. Please enter workspace ID manually.")
            print("You can find it at: app.zenhub.com/workspaces/{workspace-id}/...")
            workspace_id = input("Workspace ID: ").strip()
    else:
        print(f"✅ Workspace ID: {workspace_id} (from args)")

    print()

    # Step 4: Fetch and select default pipeline (if not provided via args)
    default_pipeline_id = args.default_pipeline_id
    default_pipeline_name = args.default_pipeline_name
    organization_id = args.organization_id

    if not default_pipeline_id or not organization_id:
        print("📡 Fetching workspace pipelines and organization...")
        pipelines, org_id = fetch_workspace_pipelines(api_token, workspace_id)

        if org_id and not organization_id:
            organization_id = org_id
            print(f"✅ Organization ID: {organization_id}")

        if not pipelines and not default_pipeline_id:
            print("⚠️  Could not fetch pipelines. Please enter manually.")
            default_pipeline_id = input("Default pipeline ID: ").strip()
            default_pipeline_name = input("Default pipeline name (e.g., 'Product Backlog'): ").strip()
        elif pipelines and not default_pipeline_id:
            print()
            print("Available pipelines:")
            for idx, pipeline in enumerate(pipelines, 1):
                print(f"  {idx}. {pipeline['name']} (ID: {pipeline['id']})")
            print()

            choice = input(f"Select default pipeline (1-{len(pipelines)}): ").strip()
            try:
                selected_pipeline = pipelines[int(choice) - 1]
                default_pipeline_id = selected_pipeline['id']
                default_pipeline_name = selected_pipeline['name']
                print(f"✅ Selected: {default_pipeline_name}")
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                sys.exit(1)
    else:
        print(f"✅ Pipeline: {default_pipeline_name} (from args)")

    if not organization_id:
        if args.force and args.organization_id:
            organization_id = args.organization_id
        elif args.force:
            print("❌ Error: Organization ID is required in non-interactive mode")
            sys.exit(1)
        else:
            print("⚠️  Could not fetch organization ID")
            organization_id = input("Organization ID: ").strip()

    print()

    # Step 5: Get default labels
    if args.default_labels:
        labels_input = args.default_labels
        print(f"✅ Labels: {labels_input} (from args)")
    elif args.force:
        # Non-interactive mode: use empty labels if not provided
        labels_input = ""
        print("✅ Labels: (none)")
    else:
        labels_input = input("Default labels (comma-separated, optional): ").strip()
    default_labels = [l.strip() for l in labels_input.split(',') if l.strip()]

    # MCP server configuration
    mcp_config = {
        "command": "npx",
        "args": [
            "-y",
            "mcp-remote",
            "https://api.zenhub.com/mcp",
            "--header",
            f"Authorization:${{API_TOKEN}}",
            "--header",
            f"X-zh-workspace:{workspace_id}"
        ],
        "env": {
            "API_TOKEN": api_token
        }
    }

    return {
        "workspace_id": workspace_id,
        "repository_id": repository_id,
        "organization_id": organization_id,
        "default_pipeline_id": default_pipeline_id,
        "default_pipeline_name": default_pipeline_name,
        "default_labels": default_labels
    }, mcp_config


def setup_jira(args):
    """Collect Jira-specific configuration (placeholder)"""
    print("Jira Configuration")
    print("-" * 50)
    print()
    print("⚠️  Jira integration is planned but not yet implemented.")
    print("This will create a placeholder configuration.")
    print()

    jira_url = args.jira_url or input("Jira URL (e.g., https://your-company.atlassian.net): ").strip()
    jira_url = jira_url.rstrip('/')
    project_key = args.project_key or input("Project key (e.g., PROJ): ").strip()
    project_key = project_key.upper()

    return {
        "jira_url": jira_url,
        "project_key": project_key,
        "default_labels": []
    }, None  # No MCP config for Jira yet


def setup_linear(args):
    """Collect Linear-specific configuration (placeholder)"""
    print("Linear Configuration")
    print("-" * 50)
    print()
    print("⚠️  Linear integration is planned but not yet implemented.")
    print("This will create a placeholder configuration.")
    print()

    team_id = args.team_id or input("Team ID: ").strip()
    workspace_id = args.linear_workspace_id or input("Workspace ID: ").strip()

    return {
        "team_id": team_id,
        "workspace_id": workspace_id,
        "default_labels": []
    }, None  # No MCP config for Linear yet


def update_claude_json(project_dir: Path, board_type: str, mcp_config: dict):
    """Update ~/.claude.json with MCP server configuration"""
    claude_json = Path.home() / ".claude.json"

    if not claude_json.exists():
        print(f"⚠️  {claude_json} not found - skipping MCP server setup")
        return

    try:
        with open(claude_json, 'r') as f:
            data = json.load(f)

        # Ensure projects section exists
        if "projects" not in data:
            data["projects"] = {}

        # Convert project path to string
        project_path = str(project_dir)

        # Ensure project entry exists
        if project_path not in data["projects"]:
            data["projects"][project_path] = {
                "allowedTools": [],
                "mcpContextUris": [],
                "mcpServers": {},
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": [],
                "hasTrustDialogAccepted": True,
                "projectOnboardingSeenCount": 1
            }

        # Add or update MCP server
        if "mcpServers" not in data["projects"][project_path]:
            data["projects"][project_path]["mcpServers"] = {}

        data["projects"][project_path]["mcpServers"][board_type] = mcp_config

        # Write back
        with open(claude_json, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Updated MCP server config: {claude_json}")

    except Exception as e:
        print(f"⚠️  Error updating {claude_json}: {e}")
        print("You may need to manually add the MCP server configuration.")


def update_claude_settings(board_type: str):
    """Update ~/.claude/settings.json with permission wildcards"""
    settings_file = Path.home() / ".claude" / "settings.json"
    settings_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing settings or create new
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading {settings_file}: {e}")
            settings = {}
    else:
        settings = {}

    # Ensure permissions structure exists
    if "permissions" not in settings:
        settings["permissions"] = {}
    if "allow" not in settings["permissions"]:
        settings["permissions"]["allow"] = []

    # Add wildcard permission for board type
    wildcard = f"mcp__{board_type}__*"
    if wildcard not in settings["permissions"]["allow"]:
        settings["permissions"]["allow"].append(wildcard)
        print(f"✅ Added permission wildcard: {wildcard}")
    else:
        print(f"ℹ️  Permission wildcard already exists: {wildcard}")

    # Write back
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Updated permissions: {settings_file}")
    except Exception as e:
        print(f"⚠️  Error writing {settings_file}: {e}")


def update_gitignore(project_dir: Path):
    """Update project .gitignore to exclude config file"""
    gitignore_file = project_dir / ".gitignore"
    gitignore_entry = ".claude/agile-board-config.json"

    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            gitignore_content = f.read()

        if gitignore_entry not in gitignore_content:
            with open(gitignore_file, 'a') as f:
                f.write(f"\n# Agile board config (project-specific)\n{gitignore_entry}\n")
            print(f"✅ Added to .gitignore: {gitignore_entry}")
        else:
            print(f"ℹ️  Already in .gitignore: {gitignore_entry}")
    else:
        print(f"⚠️  No .gitignore found - add this to .gitignore: {gitignore_entry}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
