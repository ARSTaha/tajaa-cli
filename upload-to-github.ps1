# Tajaa CLI - Quick GitHub Upload Script
# Run this in PowerShell after creating your repository on GitHub

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "        TAJAA CLI - GitHub Upload Assistant                " -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the tajaa-cli directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Project directory confirmed`n" -ForegroundColor Green

# Prompt for user information
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 1: Configure Git" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

$gitUser = Read-Host "Enter your GitHub username (default: ARSTaha)"
if ([string]::IsNullOrWhiteSpace($gitUser)) {
    $gitUser = "ARSTaha"
}

$gitEmail = Read-Host "Enter your GitHub email"
if ([string]::IsNullOrWhiteSpace($gitEmail)) {
    Write-Host "[ERROR] Email is required!" -ForegroundColor Red
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "STEP 2: Initialize Git Repository" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

# Initialize Git if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "[OK] Git repository initialized`n" -ForegroundColor Green
} else {
    Write-Host "[OK] Git repository already initialized`n" -ForegroundColor Green
}

# Configure Git
Write-Host "Configuring Git user..." -ForegroundColor Cyan
git config user.name $gitUser
git config user.email $gitEmail
Write-Host "[OK] Git configured for $gitUser ($gitEmail)`n" -ForegroundColor Green

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 3: Stage All Files" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Adding all files to Git..." -ForegroundColor Cyan
git add .
Write-Host "[OK] All files staged`n" -ForegroundColor Green

# Show status
Write-Host "Files to be committed:" -ForegroundColor Cyan
git status --short
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 4: Create Initial Commit" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Tajaa CLI v2.0.0 - Production-grade pentesting tool"
Write-Host "[OK] Initial commit created`n" -ForegroundColor Green

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 5: Set Main Branch" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Setting branch to 'main'..." -ForegroundColor Cyan
git branch -M main
Write-Host "[OK] Branch set to 'main'`n" -ForegroundColor Green

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 6: Add Remote Repository" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

$repoUrl = "https://github.com/$gitUser/tajaa-cli.git"
Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan

# Remove existing remote if it exists
git remote remove origin 2>$null

Write-Host "Adding remote repository..." -ForegroundColor Cyan
git remote add origin $repoUrl
Write-Host "[OK] Remote repository added`n" -ForegroundColor Green

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 7: Ready to Push!" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "WARNING: Before pushing, make sure you have:" -ForegroundColor Yellow
Write-Host "   1. Created the repository on GitHub: https://github.com/new" -ForegroundColor White
Write-Host "   2. Repository name: tajaa-cli" -ForegroundColor White
Write-Host "   3. DO NOT initialize with README, .gitignore, or license" -ForegroundColor White
Write-Host "   4. Created a Personal Access Token: https://github.com/settings/tokens`n" -ForegroundColor White

$ready = Read-Host "Have you created the repository on GitHub? (yes/no)"

if ($ready -eq "yes" -or $ready -eq "y") {
    Write-Host "`nPushing to GitHub..." -ForegroundColor Cyan
    Write-Host "You will be prompted for your credentials:" -ForegroundColor Yellow
    Write-Host "  Username: $gitUser" -ForegroundColor White
    Write-Host "  Password: Use your Personal Access Token (NOT your GitHub password)`n" -ForegroundColor White
    
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n============================================================" -ForegroundColor Green
        Write-Host "              SUCCESS! Repository Uploaded!               " -ForegroundColor Green
        Write-Host "============================================================`n" -ForegroundColor Green
        
        Write-Host "Your repository is now live at:" -ForegroundColor Cyan
        Write-Host "https://github.com/$gitUser/tajaa-cli`n" -ForegroundColor White
        
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Visit your repository" -ForegroundColor White
        Write-Host "  2. Add topics/tags for better discoverability" -ForegroundColor White
        Write-Host "  3. Star your own repository" -ForegroundColor White
        Write-Host "  4. Share with the community!`n" -ForegroundColor White
    } else {
        Write-Host "`n[ERROR] Push failed. Please check:" -ForegroundColor Red
        Write-Host "  1. Repository exists on GitHub" -ForegroundColor White
        Write-Host "  2. You're using a Personal Access Token (not password)" -ForegroundColor White
        Write-Host "  3. Token has 'repo' permissions" -ForegroundColor White
        Write-Host "`nFor help, see: GITHUB_UPLOAD_GUIDE.md`n" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nWARNING: Setup complete! When ready to push:" -ForegroundColor Yellow
    Write-Host "`n1. Create repository on GitHub: https://github.com/new" -ForegroundColor White
    Write-Host "2. Run this command:`n" -ForegroundColor White
    Write-Host "   git push -u origin main`n" -ForegroundColor Cyan
}

Write-Host "============================================================`n" -ForegroundColor Cyan

