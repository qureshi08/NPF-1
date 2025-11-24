# Quick Deploy Script
# Run this to prepare your app for deployment

Write-Host "🚀 Preparing New Pindi Furniture for Deployment..." -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "📝 Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host ""
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m "Ready for deployment - New Pindi Furniture ERP"

Write-Host ""
Write-Host "✅ Your app is ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create a GitHub repository at: https://github.com/new" -ForegroundColor White
Write-Host "2. Run these commands (replace YOUR_USERNAME):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/new-pindi-furniture.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Then deploy on Render:" -ForegroundColor White
Write-Host "   - Go to https://render.com" -ForegroundColor Gray
Write-Host "   - Sign up (free)" -ForegroundColor Gray
Write-Host "   - Click 'New +' → 'Web Service'" -ForegroundColor Gray
Write-Host "   - Connect your GitHub repo" -ForegroundColor Gray
Write-Host "   - Click 'Create Web Service'" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Full instructions in DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""
