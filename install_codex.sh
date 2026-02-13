#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Codex Skills Installer (WSL/Linux)

Installs this repo's skills into Codex by placing them under:
  $CODEX_HOME/skills (defaults to ~/.codex/skills)

Codex requires SKILL.md YAML frontmatter to include only `name` and `description`.
This script generates a Codex-compatible SKILL.md for each installed skill.

Usage:
  ./install_codex.sh [--dest <skills_dir>] [--copy] [--dry-run]

Options:
  --dest <skills_dir>  Install into a specific skills directory.
  --copy               Copy skill directories instead of symlinking their resources.
  --dry-run            Print what would change without modifying anything.
  -h, --help           Show this help text.
EOF
}

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
DEST_SKILLS_DIR="$CODEX_HOME/skills"
METHOD="overlay"
DRY_RUN="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      DEST_SKILLS_DIR="${2:-}"
      if [[ -z "$DEST_SKILLS_DIR" ]]; then
        echo "Error: --dest requires a value" >&2
        exit 2
      fi
      shift 2
      ;;
    --copy)
      METHOD="copy"
      shift
      ;;
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

echo "Codex Skills Installer"
echo "Installing from: $REPO_DIR"
echo "Destination: $DEST_SKILLS_DIR"
echo "Method: $METHOD"
echo ""

if [[ "$DRY_RUN" == "0" ]]; then
  mkdir -p "$DEST_SKILLS_DIR"
fi

installed_skills=0

extract_frontmatter_value() {
  # Extracts a scalar value from the first YAML frontmatter block.
  # Prints the value as-is (e.g. quoted string) or empty if not found.
  local key="$1"
  local file="$2"
  awk -v "k=$key" '
    NR==1 && $0=="---" { in_fm=1; next }
    in_fm && $0=="---" { exit }
    in_fm && $0 ~ ("^" k ":[[:space:]]*") {
      sub(("^" k ":[[:space:]]*"), "", $0)
      print
      exit
    }
  ' "$file"
}

strip_frontmatter() {
  # Prints the SKILL.md body without the leading YAML frontmatter block.
  local file="$1"
  awk '
    NR==1 && $0=="---" { in_fm=1; next }
    in_fm && $0=="---" { in_fm=0; next }
    !in_fm { print }
  ' "$file"
}

write_codex_skill_md() {
  local src_skill_md="$1"
  local dest_skill_md="$2"
  local fallback_name="$3"

  local name description
  name="$(extract_frontmatter_value "name" "$src_skill_md" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' || true)"
  description="$(extract_frontmatter_value "description" "$src_skill_md" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' || true)"

  if [[ -z "$name" ]]; then
    name="$fallback_name"
  fi
  if [[ -z "$description" ]]; then
    description="\"Skill: $fallback_name\""
  fi

  {
    echo "---"
    echo "name: $name"
    echo "description: $description"
    echo "---"
    echo ""
    strip_frontmatter "$src_skill_md"
  } > "$dest_skill_md"
}

if [[ -d "$REPO_DIR/skills" ]]; then
  shopt -s nullglob
  for skill_path in "$REPO_DIR"/skills/*/SKILL.md; do
    skill="$(basename "$(dirname "$skill_path")")"

    skill_source="$REPO_DIR/skills/$skill"
    skill_target="$DEST_SKILLS_DIR/$skill"

    if [[ "$METHOD" == "copy" ]]; then
      if [[ "$DRY_RUN" == "0" ]]; then
        if [[ -e "$skill_target" ]]; then
          echo "Warning: $skill_target already exists; skipping (copy mode)"
          continue
        fi
        cp -a "$skill_source" "$skill_target"
        write_codex_skill_md "$skill_source/SKILL.md" "$skill_target/SKILL.md" "$skill"
      else
        if [[ -e "$skill_target" ]]; then
          echo "[dry-run] Would skip (already exists): $skill_target"
          continue
        fi
        echo "[dry-run] Would copy: $skill_source -> $skill_target"
        echo "[dry-run] Would generate Codex SKILL.md: $skill_target/SKILL.md"
      fi
    else
      if [[ "$DRY_RUN" == "0" ]]; then
        if [[ -L "$skill_target" ]]; then
          rm "$skill_target"
        elif [[ -e "$skill_target" && ! -d "$skill_target" ]]; then
          echo "Warning: $skill_target already exists and is not a directory; skipping"
          continue
        fi
        mkdir -p "$skill_target"

        for entry in "$skill_source"/*; do
          base="$(basename "$entry")"
          if [[ "$base" == "SKILL.md" ]]; then
            continue
          fi

          entry_target="$skill_target/$base"
          if [[ -L "$entry_target" ]]; then
            rm "$entry_target"
          elif [[ -e "$entry_target" ]]; then
            echo "Warning: $entry_target already exists and is not a symlink; leaving as-is"
            continue
          fi

          ln -s "$entry" "$entry_target"
        done

        write_codex_skill_md "$skill_source/SKILL.md" "$skill_target/SKILL.md" "$skill"
      else
        echo "[dry-run] Would create/update: $skill_target/"
        echo "[dry-run] Would symlink resources from: $skill_source/"
        echo "[dry-run] Would generate Codex SKILL.md: $skill_target/SKILL.md"
      fi
    fi

    echo "Installed skill: $skill"
    installed_skills=$((installed_skills + 1))
  done
fi

echo ""
echo "Installation complete:"
echo "  - $installed_skills skill(s) installed to $DEST_SKILLS_DIR"
echo ""
echo "Next steps:"
echo "  - Restart Codex to pick up new skills."
