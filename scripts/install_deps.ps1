# scripts/install_deps.ps1
# Usage:
#   cd "C:\Users\Roberto002\My Drive\WSP2AGENT"
#   .\scripts\install_deps.ps1

param()

Write-Host "Installing WSP2AGENT dependencies..." -ForegroundColor Cyan

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating existing virtualenv (.venv)..." -ForegroundColor Green
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtualenv not found. Creating .venv..." -ForegroundColor Yellow
    python -m venv .venv
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Upgrading pip, setuptools, wheel..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing pinned requirements..." -ForegroundColor Cyan
python -m pip install -r requirements.txt

Write-Host "`nKey packages installed:" -ForegroundColor Green
python -m pip freeze | Select-String -Pattern "serpapi|lxml|reportlab|google-api-python-client|beautifulsoup4|pandas|python-dotenv|tqdm"

Write-Host "`nDependency install complete." -ForegroundColor Cyan
