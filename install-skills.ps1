# Claude Code Skills Installer (Windows)

# Get the directory where this script is located (the repo root)
$REPO_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SKILLS_DIR = "$env:USERPROFILE\.claude\skills"

Write-Host "📦 Claude Code Skills Installer" -ForegroundColor Cyan
Write-Host "Installing from: $REPO_DIR" -ForegroundColor Gray
Write-Host ""

# Create skills directory if it doesn't exist
if (-Not (Test-Path $SKILLS_DIR)) {
    New-Item -ItemType Directory -Path $SKILLS_DIR | Out-Null
}

# Find all directories containing SKILL.md
$skillDirs = Get-ChildItem -Path $REPO_DIR -Directory | Where-Object {
    (Test-Path (Join-Path $_.FullName "SKILL.md")) -and ($_.Name -notmatch "^\.")
}

if ($skillDirs.Count -eq 0) {
    Write-Host "⚠️  No skills found (no directories with SKILL.md)" -ForegroundColor Yellow
    exit 1
}

$installedCount = 0

foreach ($skillDir in $skillDirs) {
    $skill = $skillDir.Name
    $sourcePath = $skillDir.FullName
    $targetPath = Join-Path $SKILLS_DIR $skill

    # Remove existing symlink if present
    if (Test-Path $targetPath) {
        $item = Get-Item $targetPath
        if ($item.LinkType -eq "SymbolicLink") {
            Remove-Item $targetPath
        } else {
            Write-Host "⚠️  Warning: $targetPath already exists and is not a symlink" -ForegroundColor Yellow
            Write-Host "   Please remove it manually if you want to replace it" -ForegroundColor Yellow
            continue
        }
    }

    # Create symlink (requires admin privileges on older Windows versions)
    try {
        New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath -ErrorAction Stop | Out-Null
        Write-Host "✅ Installed $skill" -ForegroundColor Green
        $installedCount++
    } catch {
        Write-Host "❌ Failed to install $skill : $_" -ForegroundColor Red
        Write-Host "   You may need to run PowerShell as Administrator" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📝 Installed $installedCount skill(s) to $SKILLS_DIR" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  - Skills are now available globally for all projects"
Write-Host "  - For agile-board: Run 'python $REPO_DIR\agile-board\scripts\setup.py' in your project"
Write-Host "  - To update skills: git pull in $REPO_DIR"
