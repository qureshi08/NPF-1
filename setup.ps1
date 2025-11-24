# New Pindi Furniture - Quick Setup Script
# Run this script to set up the entire application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "New Pindi Furniture Admin Portal Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Step 2: Create Virtual Environment
Write-Host ""
Write-Host "[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate Virtual Environment
Write-Host ""
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Step 4: Install Dependencies
Write-Host ""
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Step 5: Check SQL Server
Write-Host ""
Write-Host "[5/6] Checking SQL Server..." -ForegroundColor Yellow
Write-Host "⚠ Please ensure:" -ForegroundColor Yellow
Write-Host "  - SQL Server is running" -ForegroundColor White
Write-Host "  - Database 'NewPindiFurnitureDB' exists" -ForegroundColor White
Write-Host "  - ODBC Driver 17 for SQL Server is installed" -ForegroundColor White
Write-Host ""
$continue = Read-Host "Continue with database initialization? (Y/N)"

if ($continue -eq "Y" -or $continue -eq "y") {
    # Step 6: Initialize Database
    Write-Host ""
    Write-Host "[6/6] Initializing database..." -ForegroundColor Yellow
    python init_db.py
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To start the application, run:" -ForegroundColor Cyan
    Write-Host "  python run.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Then open your browser to:" -ForegroundColor Cyan
    Write-Host "  http://localhost:5000" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Setup paused. Please configure SQL Server and run:" -ForegroundColor Yellow
    Write-Host "  python init_db.py" -ForegroundColor White
    Write-Host ""
}
