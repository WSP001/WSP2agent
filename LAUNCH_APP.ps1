# WSP2AGENT One-Click Launcher
# Double-click this file to start the Streamlit control panel

# Navigate to script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "🏠 WSP2AGENT - Starting Control Panel..." -ForegroundColor Green
Write-Host "   Location: $scriptDir" -ForegroundColor Gray
Write-Host ""

# Check if virtual environment exists
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Cyan
    & $venvPath
} else {
    Write-Host "⚠️  No virtual environment found. Creating one..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "🚀 Launching Streamlit Control Panel..." -ForegroundColor Green
Write-Host "   Opening in your browser..." -ForegroundColor Gray
Write-Host ""

# Launch Streamlit
streamlit run streamlit_app/app.py

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Error occurred. Press any key to exit..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
