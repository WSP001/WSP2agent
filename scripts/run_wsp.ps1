param()
Clear-Host
Write-Host "=== WSP2AGENT helper ===" -ForegroundColor Cyan
Write-Host "1) Dry run pipeline"
Write-Host "2) Generate PDFs"
Write-Host "3) Broker: create packages"
Write-Host "4) Worker: dry send"
Write-Host "5) Worker: real send (CAUTION)"
Write-Host "Q) Quit"

$choice = Read-Host "Select an option"

switch ($choice.ToUpper()) {
    "1" {
        python run_pipeline.py --dry-run
    }
    "2" {
        python -c "from modules.pdfs import make_personal_pdfs; make_personal_pdfs('data/top10_landlords.csv','out')"
    }
    "3" {
        python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv', pdf_dir='out')"
    }
    "4" {
        python -c "import modules.worker as w; w.poll_and_send(dry_run=$true)"
    }
    "5" {
        $confirm = Read-Host "Type SEND to confirm real email send"
        if ($confirm -eq "SEND") {
            python -c "import modules.worker as w; w.poll_and_send(dry_run=$false)"
        } else {
            Write-Host "Canceled."
        }
    }
    default {
        Write-Host "Bye."
    }
}
