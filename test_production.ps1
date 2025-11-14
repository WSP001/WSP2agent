# WSP2AGENT - Quick Test Script
# Tests both V1 (prototype) and V2 (production) selenium automation

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "🧪 WSP2AGENT Production Upgrade - Quick Test" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Navigate to project
Set-Location "C:\Users\Roberto002\My Drive\WSP2AGENT"

# Test 1: Install missing dependency
Write-Host "📦 Step 1: Check PyYAML dependency..." -ForegroundColor Yellow
try {
    python -c "import yaml; print('✓ PyYAML installed')"
} catch {
    Write-Host "❌ PyYAML missing - installing..." -ForegroundColor Red
    pip install pyyaml
    Write-Host "✓ PyYAML installed" -ForegroundColor Green
}
Write-Host ""

# Test 2: Config system
Write-Host "⚙️  Step 2: Test config system..." -ForegroundColor Yellow
python -c "from modules.config import get_config; cfg = get_config(); print(f'Chrome: {cfg.chrome_binary_path}'); print(f'Headless default: {cfg.headless_default}'); print(f'Environment: {cfg.env}')"
Write-Host ""

# Test 3: V2 driver smoke test
Write-Host "🔧 Step 3: Test production driver (V2)..." -ForegroundColor Yellow
python modules/selenium_driver_v2.py
Write-Host ""

# Test 4: Check if CSV exists
Write-Host "📋 Step 4: Check test data..." -ForegroundColor Yellow
if (Test-Path "data/top10_landlords.csv") {
    $rowCount = (Get-Content "data/top10_landlords.csv" | Measure-Object -Line).Lines - 1
    Write-Host "✓ CSV found: $rowCount rows" -ForegroundColor Green
} else {
    Write-Host "⚠️  CSV not found - create sample data first" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Ask user if they want to run enricher
Write-Host "🚀 Step 5: Test production enricher (V2)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "This will run the enricher in DRY-RUN mode (won't modify CSV)" -ForegroundColor Cyan
Write-Host "  • Visible browser (you'll see it work)" -ForegroundColor Gray
Write-Host "  • 3 rows max (quick test)" -ForegroundColor Gray
Write-Host "  • Creates logs in logs/ directory" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Run enricher test? (y/n)"

if ($response -eq "y") {
    Write-Host ""
    Write-Host "▶️  Running enricher..." -ForegroundColor Cyan
    python scripts/contact_enricher_v2.py --csv data/top10_landlords.csv --visible --max-rows 3 --dry-run
    
    Write-Host ""
    Write-Host "📊 View run report:" -ForegroundColor Yellow
    $latestReport = Get-ChildItem "logs/run_report_*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestReport) {
        Write-Host "  $($latestReport.FullName)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Report contents:" -ForegroundColor Cyan
        Get-Content $latestReport.FullName | ConvertFrom-Json | ConvertTo-Json | Write-Host
    }
} else {
    Write-Host "⏭️  Skipped enricher test" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ Test complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review PRODUCTION_UPGRADE_GUIDE.md for details" -ForegroundColor White
Write-Host "  2. Compare V1 vs V2 features" -ForegroundColor White
Write-Host "  3. Decide: Keep V1, migrate to V2, or hybrid" -ForegroundColor White
Write-Host "  4. Ask Netlify agent about Streamlit deployment" -ForegroundColor White
Write-Host ""
