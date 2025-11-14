# WSP2AGENT — One-Click Test & Deploy Script
# Run this after patch is applied

Write-Host "🚀 WSP2AGENT Mission Control — Production Deployment" -ForegroundColor Cyan
Write-Host "=" * 60

# Check current directory
$expectedPath = "C:\Users\Roberto002\My Drive\WSP2AGENT"
if ((Get-Location).Path -ne $expectedPath) {
    Write-Host "⚠️  Changing to WSP2AGENT directory..." -ForegroundColor Yellow
    Set-Location $expectedPath
}

Write-Host ""
Write-Host "📋 Pre-Flight Checks..." -ForegroundColor Yellow

# Check venv
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating..." -ForegroundColor Red
    python -m venv .venv
}

# Activate venv
Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host "✅ Upgrading SerpApi client..." -ForegroundColor Green
python -m pip install --upgrade google-search-results -q

Write-Host "✅ Installing other dependencies..." -ForegroundColor Green
python -m pip install -r requirements.txt -q

# Check OAuth token
Write-Host ""
Write-Host "🔐 OAuth Token Check..." -ForegroundColor Yellow
if (-not (Test-Path "token.json")) {
    Write-Host "⚠️  No token.json found. You'll need to run OAuth before LIVE sends:" -ForegroundColor Yellow
    Write-Host "   python -c `"import modules.gmailer as g; g.gmail_auth()`"" -ForegroundColor Cyan
    Write-Host ""
    $runOAuth = Read-Host "Run OAuth setup now? (y/N)"
    if ($runOAuth -eq 'y') {
        python -c "import modules.gmailer as g; g.gmail_auth()"
    }
} else {
    Write-Host "✅ OAuth token found (token.json exists)" -ForegroundColor Green
}

# Check Top-3 export
Write-Host ""
Write-Host "📧 Top-3 Drafts Check..." -ForegroundColor Yellow
if (-not (Test-Path "data\top3_emails_export.json")) {
    Write-Host "⚠️  No top3_emails_export.json found" -ForegroundColor Yellow
    Write-Host "   The file was created earlier. If missing, regenerate via:" -ForegroundColor Cyan
    Write-Host "   python run_pipeline.py --dry-run" -ForegroundColor Cyan
} else {
    $draftCount = (Get-Content "data\top3_emails_export.json" | ConvertFrom-Json).Count
    Write-Host "✅ Top-3 drafts found ($draftCount emails ready)" -ForegroundColor Green
}

# Check curated CSV
Write-Host ""
Write-Host "📊 Curated Contacts Check..." -ForegroundColor Yellow
if (-not (Test-Path "data\top10_landlords.csv")) {
    Write-Host "⚠️  No top10_landlords.csv found. Run pipeline first:" -ForegroundColor Yellow
    Write-Host "   python run_pipeline.py --dry-run" -ForegroundColor Cyan
} else {
    $csvLines = (Get-Content "data\top10_landlords.csv" | Measure-Object -Line).Lines
    Write-Host "✅ Curated CSV found ($csvLines rows including header)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60
Write-Host "🎯 Ready to Launch!" -ForegroundColor Green
Write-Host ""
Write-Host "Choose an option:" -ForegroundColor Cyan
Write-Host "  1) Launch Mission Control UI (Streamlit)" -ForegroundColor White
Write-Host "  2) Run Full Pipeline (Dry-Run)" -ForegroundColor White
Write-Host "  3) View Top-10 CSV" -ForegroundColor White
Write-Host "  4) View Top-3 Drafts JSON" -ForegroundColor White
Write-Host "  5) Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Launching Mission Control UI..." -ForegroundColor Cyan
        Write-Host "   Navigate to: http://localhost:8501" -ForegroundColor Yellow
        Write-Host "   Press Ctrl+C to stop server" -ForegroundColor Yellow
        Write-Host ""
        python -m streamlit run streamlit_app/app_mission_control.py
    }
    "2" {
        Write-Host ""
        Write-Host "🔄 Running full pipeline (dry-run)..." -ForegroundColor Cyan
        python run_pipeline.py --dry-run `
            --profile config/curation_profile_winter_haven.json `
            --queries config/search_queries_winter_haven.json
        Write-Host ""
        Write-Host "✅ Pipeline complete! Check data/top10_landlords.csv" -ForegroundColor Green
    }
    "3" {
        Write-Host ""
        Write-Host "📊 Top-10 Curated Contacts:" -ForegroundColor Cyan
        Write-Host "-" * 60
        Get-Content "data\top10_landlords.csv" | Select-Object -First 11
        Write-Host "-" * 60
    }
    "4" {
        Write-Host ""
        Write-Host "📧 Top-3 Ready-to-Send Drafts:" -ForegroundColor Cyan
        Write-Host "-" * 60
        Get-Content "data\top3_emails_export.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
        Write-Host "-" * 60
    }
    "5" {
        Write-Host ""
        Write-Host "👋 Goodbye! WSP2AGENT ready when you are." -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice. Run script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Done!" -ForegroundColor Green
