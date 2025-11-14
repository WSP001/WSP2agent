# scripts/run_wsp_full.ps1
# Usage:
#   cd "C:\Users\Roberto002\My Drive\WSP2AGENT"
#   .\scripts\run_wsp_full.ps1
#   (add -SkipInstall if dependencies already installed)

param(
    [switch]$SkipInstall
)

Write-Host "=== WSP2AGENT: full safe dry-run ===" -ForegroundColor Cyan

if (-not $SkipInstall) {
    Write-Host "Running dependency installer..." -ForegroundColor Yellow
    & .\scripts\install_deps.ps1
}

if (Test-Path ".env") {
    Write-Host ".env detected. Ensure SERPAPI_KEY etc. are set inside." -ForegroundColor Green
} else {
    Write-Host "No .env found. Make sure SERPAPI_KEY is set in this session." -ForegroundColor Yellow
}

if (-not $env:SERPAPI_KEY -or $env:SERPAPI_KEY.Trim().Length -lt 10) {
    Write-Host "ERROR: SERPAPI_KEY missing for this session." -ForegroundColor Red
    Write-Host 'Set it with:  $env:SERPAPI_KEY = "cd1a94cb395604352a7893a238f7c932acfece6739909e99efeae21b69eac434"' -ForegroundColor Cyan
    exit 1
}

Write-Host "SERPAPI_KEY detected. Starting pipeline..." -ForegroundColor Green

Write-Host "`n1) python run_pipeline.py --dry-run" -ForegroundColor Cyan
python run_pipeline.py --dry-run
if ($LASTEXITCODE -ne 0) {
    Write-Host "run_pipeline.py failed. Fix errors above and rerun." -ForegroundColor Red
    exit 2
}

Write-Host "`n2) Generate PDFs" -ForegroundColor Cyan
python -c 'from modules.pdfs import make_personal_pdfs; make_personal_pdfs("data/top10_landlords.csv", out_dir="out")'

Write-Host "`n3) Compose emails" -ForegroundColor Cyan
python -c 'from modules.composer import compose_emails; compose_emails("data/top10_landlords.csv","data/top10_outreach_emails.json")'

Write-Host "`n4) Broker packages" -ForegroundColor Cyan
python -c 'from modules.broker import create_packages_from_csv; create_packages_from_csv("data/top10_landlords.csv", pdf_dir="out", only_approved=True)'

Write-Host "`n5) Worker dry-run" -ForegroundColor Cyan
python -c 'import modules.worker as w; w.poll_and_send(dry_run=True)'

Write-Host "`nDry-run workflow finished. Review data/top10_landlords.csv, out/, and data/sandbox/ for artifacts." -ForegroundColor Green
