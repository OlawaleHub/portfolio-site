# Deploy the portfolio to GitHub, then to Vercel.
#
#   Usage:  .\deploy-to-github.ps1
#           .\deploy-to-github.ps1 -RepoName my-portfolio
#
# Safe to re-run: the first run commits and pushes, later runs push whatever
# has changed.
#
# If Windows refuses to run it ("running scripts is disabled on this system"),
# start it like this instead:
#
#   powershell -ExecutionPolicy Bypass -File .\deploy-to-github.ps1

[CmdletBinding()]
param(
    [string]$RepoName = "portfolio",
    [string]$CommitMessage = "Update portfolio site"
)

# Deliberately Continue, not Stop. Several steps below run git commands whose
# normal, expected output goes to stderr (a missing remote, an empty repo), and
# "Stop" would abort the script before it could explain what to do.
$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

function Write-Step($n, $text) {
    Write-Host ""
    Write-Host "[$n] $text" -ForegroundColor Cyan
}
function Write-Ok($text)   { Write-Host "    OK   $text" -ForegroundColor Green }
function Write-Warn($text) { Write-Host "    WARN $text" -ForegroundColor Yellow }
function Write-Bad($text)  { Write-Host "    FAIL $text" -ForegroundColor Red }

# Run git and return its combined text (empty string if it fails).
# Only safe for arguments that do not look like PowerShell parameters —
# for those, call git directly, because PowerShell would bind "-A", "-m",
# "-u" etc. as parameters of this function instead of passing them on.
function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    $output = & git @GitArgs 2>&1 | Where-Object { $_ -notmatch '^\s*$' }
    return ($output | Out-String).Trim()
}

Write-Host ""
Write-Host "Portfolio -> GitHub" -ForegroundColor White
Write-Host ("=" * 52)

# ---------------------------------------------------------------- 1. git present
Write-Step 1 "Checking git"
$gitVersion = (& git --version 2>&1 | Out-String).Trim()
if (-not $gitVersion -or $gitVersion -notmatch 'git version') {
    Write-Bad "git is not installed or not on PATH."
    Write-Host "    Install it from https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}
Write-Ok $gitVersion

# ---------------------------------------------------------------- 2. identity
Write-Step 2 "Checking your git identity"
$name       = Invoke-Git config user.name
$email      = Invoke-Git config user.email
$globalName = Invoke-Git config --global user.name

if (-not $name -or -not $email) {
    Write-Bad "Git does not know who you are yet, so it cannot create a commit."
    Write-Host ""
    Write-Host "    Run these two lines first, with your own details:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host '        git config --global user.name "Soliu Quadri"' -ForegroundColor White
    Write-Host '        git config --global user.email "quadrisoliu14@gmail.com"' -ForegroundColor White
    Write-Host ""
    Write-Host "    Then run this script again." -ForegroundColor Yellow
    exit 1
}
Write-Ok "name:  $name"
Write-Ok "email: $email"
if (-not $globalName) {
    Write-Warn "this identity is set for this repository only, not globally"
    Write-Host "         to set it everywhere as well:" -ForegroundColor Gray
    Write-Host "           git config --global user.name `"$name`"" -ForegroundColor Gray
    Write-Host "           git config --global user.email `"$email`"" -ForegroundColor Gray
}

# ---------------------------------------------------------------- 3. repo
Write-Step 3 "Preparing the local repository"
if (-not (Test-Path ".git")) {
    git init *> $null
    Write-Ok "initialised a new repository"
} else {
    Write-Ok "repository already exists"
}

# -M must be passed straight to git, so this is a direct call, not Invoke-Git.
git branch -M main *> $null
Write-Ok "branch: $(git branch --show-current)"

git add -A *> $null
$stagedFiles = @(git diff --cached --name-only)
$stagedFiles = @($stagedFiles | Where-Object { $_.Trim() })
Write-Ok "$($stagedFiles.Count) file(s) staged"

# ---------------------------------------------------------------- 4. commit
Write-Step 4 "Committing"
$hasCommits = $false
git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -eq 0) { $hasCommits = $true }

if (-not $hasCommits) {
    if ($stagedFiles.Count -eq 0) {
        Write-Bad "nothing to commit and no history yet - is this the right folder?"
        exit 1
    }
    git commit -m $CommitMessage *> $null
    Write-Ok "first commit created"
} elseif ($stagedFiles.Count -gt 0) {
    git commit -m $CommitMessage *> $null
    Write-Ok "committed $($stagedFiles.Count) change(s)"
} else {
    Write-Ok "working tree clean, nothing new to commit"
}

# ---------------------------------------------------------------- 5. remote
Write-Step 5 "Checking the GitHub remote"
git remote get-url origin *> $null
$hasRemote = ($LASTEXITCODE -eq 0)

if (-not $hasRemote) {
    Write-Warn "no 'origin' remote is set yet."
    Write-Host ""
    Write-Host "    Step 1 - create an EMPTY repository on GitHub:" -ForegroundColor Yellow
    Write-Host "      https://github.com/new" -ForegroundColor White
    Write-Host "      Name it:  $RepoName" -ForegroundColor White
    Write-Host "      Do NOT add a README, .gitignore or licence - you already have files." -ForegroundColor Gray
    Write-Host ""
    Write-Host "    Step 2 - tell this script where to push." -ForegroundColor Yellow
    Write-Host ""

    try {
        $user = Read-Host "    Your GitHub username (or press Enter to stop here)"
    } catch {
        $user = ""
    }

    if ([string]::IsNullOrWhiteSpace($user)) {
        Write-Host ""
        Write-Host "    Stopped before pushing. Your commit is safe locally." -ForegroundColor Yellow
        Write-Host "    Re-run this script once the empty GitHub repo exists." -ForegroundColor Yellow
        exit 0
    }

    $url = "https://github.com/$($user.Trim())/$RepoName.git"
    git remote add origin $url *> $null
    Write-Ok "origin -> $url"
} else {
    Write-Ok "origin -> $(Invoke-Git remote get-url origin)"
}

# ---------------------------------------------------------------- 6. push
Write-Step 6 "Pushing to GitHub"
Write-Host "    (a browser window may open to sign in; Git may ask for a token)" -ForegroundColor Gray

$pushOutput = (& git push -u origin main 2>&1 | Out-String).Trim()
Write-Host $pushOutput -ForegroundColor Gray

$pushOk = ($LASTEXITCODE -eq 0) -and ($pushOutput -notmatch 'error:|failed|rejected|denied|fatal:')

if ($pushOk) {
    Write-Ok "pushed"
} else {
    Write-Bad "push did not complete."
    Write-Host ""
    Write-Host "    If Git asked for a password: GitHub no longer accepts account" -ForegroundColor Yellow
    Write-Host "    passwords. Create a Personal Access Token instead:" -ForegroundColor Yellow
    Write-Host "      https://github.com/settings/tokens -> Generate new token (classic)" -ForegroundColor White
    Write-Host "      Tick the 'repo' scope, then paste the token as the password." -ForegroundColor Gray
    Write-Host ""
    Write-Host "    Easier alternative - install GitHub CLI, which handles login for you:" -ForegroundColor Yellow
    Write-Host "      winget install --id GitHub.cli" -ForegroundColor White
    Write-Host "      gh auth login" -ForegroundColor White
    Write-Host "    then re-run this script." -ForegroundColor Yellow
    exit 1
}

# ---------------------------------------------------------------- 7. next
Write-Host ""
Write-Host ("=" * 52)
Write-Host "Pushed successfully." -ForegroundColor Green
Write-Host ""
$remoteUrl = (Invoke-Git remote get-url origin) -replace '\.git$', ''
Write-Host "Your repository:  $remoteUrl" -ForegroundColor White
Write-Host ""
Write-Host "NOW DEPLOY IT ON VERCEL:" -ForegroundColor Cyan
Write-Host "  1. Go to https://vercel.com/new" -ForegroundColor White
Write-Host "  2. Find your repo under 'Import Git Repository' and click Import" -ForegroundColor White
Write-Host "  3. Framework Preset: Other   (leave build/output/install commands empty)" -ForegroundColor White
Write-Host "  4. Click Deploy" -ForegroundColor White
Write-Host ""
Write-Host "From then on, every 'git push' republishes the site automatically." -ForegroundColor Gray
Write-Host ""
