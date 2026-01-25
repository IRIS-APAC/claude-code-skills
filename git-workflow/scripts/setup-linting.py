#!/usr/bin/env python3
"""
Automated linting and pre-commit hooks setup for git-workflow skill.

Detects languages in the project and installs appropriate linting tools.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set


class LintingSetup:
    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.detected_languages: Set[str] = set()
        self.tools_to_install: Dict[str, List[str]] = {}
        self.pre_commit_hooks: List[Dict] = []
        self.is_windows = platform.system() == "Windows"

    def detect_languages(self) -> None:
        """Detect which languages are used in the project."""
        print("🔍 Detecting project languages...")

        # Python
        if (self.project_root / "pyproject.toml").exists() or \
           (self.project_root / "setup.py").exists() or \
           (self.project_root / "requirements.txt").exists():
            self.detected_languages.add("python")
            print("  ✓ Python detected")

        # TypeScript/JavaScript
        if (self.project_root / "package.json").exists() or \
           (self.project_root / "tsconfig.json").exists():
            self.detected_languages.add("typescript")
            print("  ✓ TypeScript/JavaScript detected")

        # Flutter/Dart
        if (self.project_root / "pubspec.yaml").exists():
            self.detected_languages.add("flutter")
            print("  ✓ Flutter/Dart detected")

        # C#
        if list(self.project_root.glob("**/*.csproj")) or \
           list(self.project_root.glob("**/*.sln")):
            self.detected_languages.add("csharp")
            print("  ✓ C# detected")

        # Terraform
        if list(self.project_root.glob("**/*.tf")):
            self.detected_languages.add("terraform")
            print("  ✓ Terraform detected")

        if not self.detected_languages:
            print("  ⚠️  No supported languages detected")
            print("     Supported: Python, TypeScript/JS, Flutter, C#, Terraform")

    def check_tool_installed(self, command: str) -> bool:
        """Check if a command-line tool is installed and in PATH."""
        return shutil.which(command) is not None

    def install_python_tools(self) -> None:
        """Install Python linting tools."""
        tools = ["black", "ruff", "mypy"]
        missing = [tool for tool in tools if not self.check_tool_installed(tool)]

        if not missing:
            print("  ✓ All Python tools already installed")
            return

        print(f"  📦 Installing Python tools: {', '.join(missing)}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--user"] + missing,
                check=True,
                capture_output=True,
            )
            print("  ✓ Python tools installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install Python tools: {e.stderr.decode()}")
            sys.exit(1)

    def install_node_tools(self) -> None:
        """Install Node.js linting tools."""
        if not self.check_tool_installed("npm"):
            print("  ⚠️  npm not found, skipping TypeScript tool installation")
            print("     Please install Node.js: https://nodejs.org/")
            return

        tools = ["eslint", "prettier"]
        # Check if tools are in node_modules or globally available
        missing = []
        for tool in tools:
            if not self.check_tool_installed(tool) and \
               not (self.project_root / "node_modules" / ".bin" / tool).exists():
                missing.append(tool)

        if not missing:
            print("  ✓ All Node.js tools already available")
            return

        print(f"  📦 Installing Node.js tools: {', '.join(missing)}")
        try:
            subprocess.run(
                ["npm", "install", "--save-dev"] + missing,
                cwd=self.project_root,
                check=True,
                capture_output=True,
            )
            print("  ✓ Node.js tools installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install Node.js tools: {e.stderr.decode()}")

    def install_tools(self) -> None:
        """Install required linting tools based on detected languages."""
        print("\n📦 Installing linting tools...")

        if "python" in self.detected_languages:
            self.install_python_tools()

        if "typescript" in self.detected_languages:
            self.install_node_tools()

        if "flutter" in self.detected_languages:
            if self.check_tool_installed("dart"):
                print("  ✓ Dart tooling available (Flutter SDK)")
            else:
                print("  ⚠️  Dart not found, please install Flutter SDK")

        if "terraform" in self.detected_languages:
            if self.check_tool_installed("terraform"):
                print("  ✓ Terraform CLI available")
            else:
                print("  ⚠️  Terraform not found, please install from https://terraform.io/")

    def update_path(self) -> None:
        """Update PATH to include user-installed tools."""
        print("\n🔧 Checking PATH configuration...")

        if self.is_windows:
            # Windows: Check if %APPDATA%\Python\Scripts is in PATH
            scripts_dir = Path(os.environ.get("APPDATA", "")) / "Python" / "Scripts"
            if scripts_dir.exists() and str(scripts_dir) not in os.environ.get("PATH", ""):
                print(f"  ⚠️  {scripts_dir} not in PATH")
                print("     Add it via System Properties > Environment Variables")
                print(f"     Or run in PowerShell as Administrator:")
                print(f'     [Environment]::SetEnvironmentVariable("Path", "$env:Path;{scripts_dir}", "User")')
        else:
            # Linux/Mac: Check if ~/.local/bin is in PATH
            local_bin = Path.home() / ".local" / "bin"
            if local_bin.exists() and str(local_bin) not in os.environ.get("PATH", ""):
                shell_rc = Path.home() / ".bashrc"
                if Path.home() / ".zshrc" in Path.home().iterdir():
                    shell_rc = Path.home() / ".zshrc"

                print(f"  ⚠️  {local_bin} not in PATH")
                print(f"     Add this to {shell_rc}:")
                print(f'     export PATH="$HOME/.local/bin:$PATH"')
                print(f"     Then run: source {shell_rc}")
            else:
                print("  ✓ PATH configured correctly")

    def generate_python_config(self) -> None:
        """Generate Python pre-commit hooks configuration."""
        self.pre_commit_hooks.append({
            "repo": "https://github.com/psf/black",
            "rev": "24.1.1",
            "hooks": [{"id": "black", "args": ["--line-length=100"]}],
        })
        self.pre_commit_hooks.append({
            "repo": "https://github.com/astral-sh/ruff-pre-commit",
            "rev": "v0.1.14",
            "hooks": [{"id": "ruff", "args": ["--fix"]}],
        })
        self.pre_commit_hooks.append({
            "repo": "https://github.com/pre-commit/mirrors-mypy",
            "rev": "v1.8.0",
            "hooks": [{"id": "mypy", "additional_dependencies": ["types-requests"]}],
        })

        # Ensure pyproject.toml exists with ruff config
        pyproject_path = self.project_root / "pyproject.toml"
        if not pyproject_path.exists():
            print("  📝 Creating pyproject.toml with ruff configuration")
            pyproject_path.write_text("""[tool.ruff]
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

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
""")

    def generate_typescript_config(self) -> None:
        """Generate TypeScript pre-commit hooks configuration."""
        self.pre_commit_hooks.append({
            "repo": "https://github.com/pre-commit/mirrors-eslint",
            "rev": "v8.56.0",
            "hooks": [{
                "id": "eslint",
                "files": r"\.(js|jsx|ts|tsx)$",
                "args": ["--fix"],
            }],
        })
        self.pre_commit_hooks.append({
            "repo": "https://github.com/pre-commit/mirrors-prettier",
            "rev": "v3.1.0",
            "hooks": [{"id": "prettier"}],
        })

    def generate_flutter_config(self) -> None:
        """Generate Flutter pre-commit hooks configuration."""
        self.pre_commit_hooks.append({
            "repo": "local",
            "hooks": [{
                "id": "dart-format",
                "name": "dart format",
                "entry": "dart",
                "args": ["format", "--line-length=100"],
                "language": "system",
                "types": ["dart"],
            }],
        })
        self.pre_commit_hooks.append({
            "repo": "local",
            "hooks": [{
                "id": "dart-analyze",
                "name": "dart analyze",
                "entry": "dart",
                "args": ["analyze", "--fatal-infos"],
                "language": "system",
                "pass_filenames": False,
            }],
        })

    def generate_terraform_config(self) -> None:
        """Generate Terraform pre-commit hooks configuration."""
        self.pre_commit_hooks.append({
            "repo": "https://github.com/antonbabenko/pre-commit-terraform",
            "rev": "v1.86.0",
            "hooks": [
                {"id": "terraform_fmt"},
                {"id": "terraform_validate"},
            ],
        })

    def generate_pre_commit_config(self) -> None:
        """Generate .pre-commit-config.yaml based on detected languages."""
        print("\n📝 Generating .pre-commit-config.yaml...")

        # Always include basic hooks
        self.pre_commit_hooks = [{
            "repo": "https://github.com/pre-commit/pre-commit-hooks",
            "rev": "v4.5.0",
            "hooks": [
                {"id": "trailing-whitespace"},
                {"id": "end-of-file-fixer"},
                {"id": "check-yaml"},
                {"id": "check-added-large-files"},
            ],
        }]

        # Add language-specific hooks
        if "python" in self.detected_languages:
            self.generate_python_config()

        if "typescript" in self.detected_languages:
            self.generate_typescript_config()

        if "flutter" in self.detected_languages:
            self.generate_flutter_config()

        if "terraform" in self.detected_languages:
            self.generate_terraform_config()

        # Write config file
        config_path = self.project_root / ".pre-commit-config.yaml"
        config_content = f"# Generated by git-workflow skill setup script\n"
        config_content += f"# Languages detected: {', '.join(sorted(self.detected_languages))}\n\n"
        config_content += "repos:\n"

        for hook in self.pre_commit_hooks:
            config_content += f"  - repo: {hook['repo']}\n"
            config_content += f"    rev: {hook['rev']}\n"
            config_content += "    hooks:\n"
            for h in hook["hooks"]:
                config_content += f"      - id: {h['id']}\n"
                if "args" in h:
                    config_content += f"        args: {h['args']}\n"
                if "additional_dependencies" in h:
                    config_content += f"        additional_dependencies: {h['additional_dependencies']}\n"
                if "files" in h:
                    config_content += f"        files: {h['files']}\n"
                if "name" in h:
                    config_content += f"        name: {h['name']}\n"
                if "entry" in h:
                    config_content += f"        entry: {h['entry']}\n"
                if "language" in h:
                    config_content += f"        language: {h['language']}\n"
                if "types" in h:
                    config_content += f"        types: {h['types']}\n"
                if "pass_filenames" in h:
                    config_content += f"        pass_filenames: {h['pass_filenames']}\n"

        config_path.write_text(config_content)
        print(f"  ✓ Created {config_path}")

    def install_pre_commit_hooks(self) -> None:
        """Install pre-commit hooks into .git/hooks."""
        print("\n🔗 Installing pre-commit hooks...")

        if not (self.project_root / ".git").exists():
            print("  ⚠️  Not a git repository, skipping hook installation")
            print("     Run 'git init' first, then re-run this script")
            return

        try:
            subprocess.run(
                ["pre-commit", "install"],
                cwd=self.project_root,
                check=True,
                capture_output=True,
            )
            print("  ✓ Pre-commit hooks installed")
        except FileNotFoundError:
            print("  ⚠️  pre-commit not found, installing...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--user", "pre-commit"],
                check=True,
            )
            subprocess.run(
                ["pre-commit", "install"],
                cwd=self.project_root,
                check=True,
            )
            print("  ✓ Pre-commit hooks installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install hooks: {e.stderr.decode()}")

    def test_hooks(self) -> None:
        """Test pre-commit hooks on all files."""
        print("\n🧪 Testing pre-commit hooks...")

        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print("  ✓ All hooks passed")
            else:
                print("  ⚠️  Some hooks made changes or failed:")
                print(result.stdout)
                print("\n  This is normal for first run - hooks may auto-fix formatting")
                print("  Run 'git diff' to see changes, then commit them")
        except FileNotFoundError:
            print("  ⚠️  pre-commit not in PATH, skipping test")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Hook test failed: {e.stderr}")

    def run(self) -> None:
        """Run the complete setup process."""
        print("=" * 60)
        print("🚀 Git Workflow - Linting Setup")
        print("=" * 60)
        print()

        self.detect_languages()

        if not self.detected_languages:
            print("\n⚠️  No supported languages detected, exiting")
            sys.exit(1)

        self.install_tools()
        self.update_path()
        self.generate_pre_commit_config()
        self.install_pre_commit_hooks()
        self.test_hooks()

        print("\n" + "=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Review changes: git diff")
        print("  2. Commit config files: git add .pre-commit-config.yaml pyproject.toml")
        print("  3. Hooks will now run automatically on 'git commit'")
        print("  4. Bypass hooks if needed: git commit --no-verify")
        print()


if __name__ == "__main__":
    setup = LintingSetup()
    setup.run()
