# Quick test script for Top-3 workflow
# Tests: Load drafts → Build packages → Dry-run send

Write-Host "🧪 WSP2AGENT Top-3 Workflow Test" -ForegroundColor Cyan
Write-Host "=" * 60

Set-Location "C:\Users\Roberto002\My Drive\WSP2AGENT"
& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Step 1: Verify Top-3 drafts exist..." -ForegroundColor Yellow
if (-not (Test-Path "data\top3_emails_export.json")) {
    Write-Host "❌ Top-3 export not found. Generate it first:" -ForegroundColor Red
    Write-Host "   python run_pipeline.py --dry-run" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ Top-3 drafts found" -ForegroundColor Green

Write-Host ""
Write-Host "Step 2: Mark first 3 rows as approved..." -ForegroundColor Yellow
python -c @"
import pandas as pd
df = pd.read_csv('data/top10_landlords.csv')
df.loc[0:2, 'approved'] = True
df.to_csv('data/top10_landlords.csv', index=False)
print('✅ Approved first 3 rows')
"@

Write-Host ""
Write-Host "Step 3: Build packages for approved rows..." -ForegroundColor Yellow
python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv', pdf_dir='out', only_approved=True)"

Write-Host ""
Write-Host "Step 4: Dry-run send via worker..." -ForegroundColor Yellow
python -c "import modules.worker as w; w.poll_and_send(dry_run=True)"

Write-Host ""
Write-Host "✅ Test Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Check results:" -ForegroundColor Cyan
Write-Host "   - Packages: data/sandbox/outbox/" -ForegroundColor White
Write-Host "   - Sent logs: data/sandbox/sent/" -ForegroundColor White
Write-Host ""
Write-Host "To send LIVE (after verifying above):" -ForegroundColor Yellow
Write-Host "   python -c `"import modules.worker as w; w.poll_and_send(dry_run=False)`"" -ForegroundColor Cyan
