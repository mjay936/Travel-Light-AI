#!/bin/bash

echo "🤖 Auto-commit script for Travel Light project"
echo "=============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if remote origin is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Error: No remote origin set"
    echo "💡 Please set up your GitHub remote first:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/travel-light.git"
    exit 1
fi

# Get current branch
BRANCH=$(git symbolic-ref --short HEAD)
echo "📍 Current branch: $BRANCH"

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes to commit"
    exit 0
fi

# Auto-add all changes
echo "📝 Staging all changes..."
git add .

# Create commit message with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="🤖 Auto-commit: Update project files - $TIMESTAMP"

# Commit changes
echo "💾 Committing changes..."
if git commit -m "$COMMIT_MSG"; then
    echo "✅ Changes committed successfully"
else
    echo "❌ Failed to commit changes"
    exit 1
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
if git push origin $BRANCH; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 View your repository at: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1\/\2/')"
else
    echo "❌ Failed to push to GitHub"
    echo "💡 You may need to authenticate or check your permissions"
    exit 1
fi

echo "🎉 Auto-commit completed successfully!"
