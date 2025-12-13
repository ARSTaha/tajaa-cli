#!/bin/bash
# Tajaa CLI - Quick GitHub Upload Script for Linux/Mac
# Run this after creating your repository on GitHub

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        TAJAA CLI - GitHub Upload Assistant                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found!"
    echo "Please run this script from the tajaa-cli directory."
    exit 1
fi

echo "✓ Project directory confirmed"
echo ""

# Prompt for user information
echo "══════════════════════════════════════════════════════════"
echo "STEP 1: Configure Git"
echo "══════════════════════════════════════════════════════════"
echo ""

read -p "Enter your GitHub username (default: ARSTaha): " GIT_USER
GIT_USER=${GIT_USER:-ARSTaha}

read -p "Enter your GitHub email: " GIT_EMAIL
if [ -z "$GIT_EMAIL" ]; then
    echo "❌ Email is required!"
    exit 1
fi

echo ""
echo "══════════════════════════════════════════════════════════"
echo "STEP 2: Initialize Git Repository"
echo "══════════════════════════════════════════════════════════"
echo ""

# Initialize Git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi
echo ""

# Configure Git
echo "Configuring Git user..."
git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"
echo "✓ Git configured for $GIT_USER <$GIT_EMAIL>"
echo ""

echo "══════════════════════════════════════════════════════════"
echo "STEP 3: Stage All Files"
echo "══════════════════════════════════════════════════════════"
echo ""

echo "Adding all files to Git..."
git add .
echo "✓ All files staged"
echo ""

# Show status
echo "Files to be committed:"
git status --short
echo ""

echo "══════════════════════════════════════════════════════════"
echo "STEP 4: Create Initial Commit"
echo "══════════════════════════════════════════════════════════"
echo ""

echo "Creating initial commit..."
git commit -m "Initial commit: Tajaa CLI v2.0.0 - Production-grade pentesting tool"
echo "✓ Initial commit created"
echo ""

echo "══════════════════════════════════════════════════════════"
echo "STEP 5: Set Main Branch"
echo "══════════════════════════════════════════════════════════"
echo ""

echo "Setting branch to 'main'..."
git branch -M main
echo "✓ Branch set to 'main'"
echo ""

echo "══════════════════════════════════════════════════════════"
echo "STEP 6: Add Remote Repository"
echo "══════════════════════════════════════════════════════════"
echo ""

REPO_URL="https://github.com/$GIT_USER/tajaa-cli.git"
echo "Repository URL: $REPO_URL"

# Remove existing remote if it exists
git remote remove origin 2>/dev/null

echo "Adding remote repository..."
git remote add origin "$REPO_URL"
echo "✓ Remote repository added"
echo ""

echo "══════════════════════════════════════════════════════════"
echo "STEP 7: Ready to Push!"
echo "══════════════════════════════════════════════════════════"
echo ""

echo "⚠️  IMPORTANT: Before pushing, make sure you have:"
echo "   1. Created the repository on GitHub: https://github.com/new"
echo "   2. Repository name: tajaa-cli"
echo "   3. DO NOT initialize with README, .gitignore, or license"
echo "   4. Created a Personal Access Token: https://github.com/settings/tokens"
echo ""

read -p "Have you created the repository on GitHub? (yes/no): " READY

if [ "$READY" = "yes" ] || [ "$READY" = "y" ]; then
    echo ""
    echo "Pushing to GitHub..."
    echo "You will be prompted for your credentials:"
    echo "  Username: $GIT_USER"
    echo "  Password: Use your Personal Access Token (NOT your GitHub password)"
    echo ""

    git push -u origin main

    if [ $? -eq 0 ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║              ✓ SUCCESS! Repository Uploaded!               ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""

        echo "Your repository is now live at:"
        echo "https://github.com/$GIT_USER/tajaa-cli"
        echo ""

        echo "Next steps:"
        echo "  1. Visit your repository"
        echo "  2. Add topics/tags for better discoverability"
        echo "  3. Star your own repository ⭐"
        echo "  4. Share with the community!"
        echo ""
    else
        echo ""
        echo "❌ Push failed. Please check:"
        echo "  1. Repository exists on GitHub"
        echo "  2. You're using a Personal Access Token (not password)"
        echo "  3. Token has 'repo' permissions"
        echo ""
        echo "For help, see: GITHUB_UPLOAD_GUIDE.md"
        echo ""
    fi
else
    echo ""
    echo "⚠️  Setup complete! When ready to push:"
    echo ""
    echo "1. Create repository on GitHub: https://github.com/new"
    echo "2. Run this command:"
    echo ""
    echo "   git push -u origin main"
    echo ""
fi

echo "════════════════════════════════════════════════════════════"
echo ""

