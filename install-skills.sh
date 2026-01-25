#!/bin/bash

# Get the directory where this script is located (the repo root)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "📦 Claude Code Skills Installer"
echo "Installing from: $REPO_DIR"
echo ""

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Find all directories containing SKILL.md
installed_count=0
for skill_path in "$REPO_DIR"/*/SKILL.md; do
    # Check if any SKILL.md files were found
    if [ ! -e "$skill_path" ]; then
        echo "⚠️  No skills found (no directories with SKILL.md)"
        exit 1
    fi

    # Get the skill directory name
    skill=$(basename "$(dirname "$skill_path")")

    # Skip hidden directories
    if [[ "$skill" == .* ]]; then
        continue
    fi

    skill_source="$REPO_DIR/$skill"
    skill_target="$SKILLS_DIR/$skill"

    # Remove existing symlink if present
    if [ -L "$skill_target" ]; then
        rm "$skill_target"
    elif [ -d "$skill_target" ]; then
        echo "⚠️  Warning: $skill_target already exists and is not a symlink"
        echo "   Please remove it manually if you want to replace it"
        continue
    fi

    # Create symlink
    ln -s "$skill_source" "$skill_target"
    echo "✅ Installed $skill"
    ((installed_count++))
done

echo ""
echo "📝 Installed $installed_count skill(s) to ~/.claude/skills/"
echo ""
echo "Next steps:"
echo "  - Skills are now available globally for all projects"
echo "  - For agile-board: Run 'python $REPO_DIR/agile-board/scripts/setup.py' in your project"
echo "  - To update skills: git pull in $REPO_DIR"
