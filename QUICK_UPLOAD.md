# ⚡ QUICK START - Upload to GitHub in 3 Steps

## 🎯 Your Repository
https://github.com/ARSTaha/tajaa-cli

---

## Step 1: Create Repository on GitHub (2 minutes)

1. Go to: https://github.com/new
2. Settings:
   - Repository name: **tajaa-cli**
   - Description: **Professional Penetration Testing Command Manager - A production-grade OOP CLI tool for ethical hacking**
   - Public ✅
   - **DO NOT** check: README, .gitignore, or license ❌
3. Click "Create repository"

---

## Step 2: Get Your Personal Access Token (2 minutes)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: **Tajaa CLI Upload**
4. Select: ✅ repo (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

---

## Step 3: Run Upload Script (1 minute)

### Windows (PowerShell):
```powershell
cd C:\Users\muham\PycharmProjects\tajaa-cli
.\upload-to-github.ps1
```

### Linux/Mac:
```bash
cd /path/to/tajaa-cli
chmod +x upload-to-github.sh
./upload-to-github.sh
```

When prompted:
- **Username:** ARSTaha
- **Email:** your-email@example.com
- **Password:** [Your Personal Access Token]

---

## ✅ Done!

Your repository will be live at:
https://github.com/ARSTaha/tajaa-cli

---

## Alternative: Manual Commands (If Script Fails)

```powershell
cd C:\Users\muham\PycharmProjects\tajaa-cli

# If .git folder exists, remove remote (if any)
git remote remove origin 2>$null

# Configure Git
git config user.name "ARSTaha"
git config user.email "your-email@example.com"

# Add files and commit
git add .
git commit -m "Initial commit: Tajaa CLI v2.0.0"

# Set branch and add remote
git branch -M main
git remote add origin https://github.com/ARSTaha/tajaa-cli.git

# Push to GitHub
git push -u origin main
```

---

## 🆘 Troubleshooting

**Error: "Authentication failed"**
→ Make sure you're using your Personal Access Token, not your password

**Error: "Repository not found"**
→ Make sure you created the repository on GitHub first

**Error: "Updates were rejected"**
→ Run: `git pull origin main --rebase` then `git push`

---

**Need more help?** See: `GITHUB_UPLOAD_GUIDE.md`

