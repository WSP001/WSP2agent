# 🎯 WSP2AGENT — All Essential Commands
# Quick reference for all user-friendly automation commands

Write-Host ""
Write-Host "🎯 WSP2AGENT — ESSENTIAL COMMANDS CHEATSHEET" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

$commands = @(
    @{
        Category = "🚀 QUICK START"
        Items = @(
            @{Name="Launch Mission Control UI"; Cmd=".\scripts\launch_mission_control.ps1"},
            @{Name="Run Full Automation Test"; Cmd=".\scripts\run_full_automation.ps1"},
            @{Name="Test Top-3 Workflow"; Cmd=".\scripts\test_top3_workflow.ps1"}
        )
    },
    @{
        Category = "🔍 PIPELINE OPERATIONS"
        Items = @(
            @{Name="Full Pipeline (Dry-Run)"; Cmd="python run_pipeline.py --dry-run"},
            @{Name="Pipeline with Custom Profile"; Cmd="python run_pipeline.py --dry-run --profile config/curation_profile_winter_haven.json"},
            @{Name="Pipeline with Custom Queries"; Cmd="python run_pipeline.py --dry-run --queries config/search_queries_winter_haven.json"},
            @{Name="View Search Results"; Cmd="Get-Content data\search_results.json | ConvertFrom-Json | Select-Object -First 5"}
        )
    },
    @{
        Category = "📊 DATA REVIEW"
        Items = @(
            @{Name="View Top-10 CSV"; Cmd="Get-Content data\top10_landlords.csv | Select-Object -First 11"},
            @{Name="View Top-3 Drafts JSON"; Cmd="Get-Content data\top3_emails_export.json | ConvertFrom-Json | ConvertTo-Json -Depth 10"},
            @{Name="View Ready-to-Send Emails"; Cmd="Get-Content data\FINAL_TOP3_READY_TO_SEND.md"},
            @{Name="Count Approved Rows"; Cmd="(Import-Csv data\top10_landlords.csv | Where-Object {`$_.approved -eq 'True'}).Count"}
        )
    },
    @{
        Category = "✅ APPROVAL OPERATIONS"
        Items = @(
            @{Name="Auto-Approve Top 3"; Cmd="python -c `"import pandas as pd; df=pd.read_csv('data/top10_landlords.csv'); df.loc[0:2,'approved']=True; df.to_csv('data/top10_landlords.csv',index=False); print('✅ Top 3 approved')`""},
            @{Name="Clear All Approvals"; Cmd="python -c `"import pandas as pd; df=pd.read_csv('data/top10_landlords.csv'); df['approved']=False; df.to_csv('data/top10_landlords.csv',index=False); print('✅ Cleared')`""},
            @{Name="Show Approved Contacts"; Cmd="Import-Csv data\top10_landlords.csv | Where-Object {`$_.approved -eq 'True'} | Select-Object organization,emails"}
        )
    },
    @{
        Category = "📦 PACKAGE & SEND"
        Items = @(
            @{Name="Build Packages (Approved Only)"; Cmd="python -c `"from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv',pdf_dir='out',only_approved=True)`""},
            @{Name="Dry-Run Send"; Cmd="python -c `"import modules.worker as w; w.poll_and_send(dry_run=True)`""},
            @{Name="Live Send (⚠️ REAL EMAILS)"; Cmd="python -c `"import modules.worker as w; w.poll_and_send(dry_run=False)`""},
            @{Name="Count Outbox Packages"; Cmd="(Get-ChildItem data\sandbox\outbox -Filter *.json).Count"}
        )
    },
    @{
        Category = "🔐 OAUTH & GMAIL"
        Items = @(
            @{Name="Setup Gmail OAuth"; Cmd="python -c `"import modules.gmailer as g; g.gmail_auth()`""},
            @{Name="Check OAuth Token"; Cmd="Test-Path token.json"},
            @{Name="Fetch Gmail Replies"; Cmd="python -c `"import modules.replier as r; r.fetch_replies(query=None,out_csv='data/responses.csv')`""},
            @{Name="View Responses CSV"; Cmd="Import-Csv data\responses.csv | Format-Table"}
        )
    },
    @{
        Category = "🧹 CLEANUP & MAINTENANCE"
        Items = @(
            @{Name="Clear Sandbox"; Cmd="Remove-Item data\sandbox\outbox\*,data\sandbox\sent\*,data\sandbox\failed\* -Force -ErrorAction SilentlyContinue"},
            @{Name="Clear Search Results"; Cmd="Remove-Item data\search_results.json -Force -ErrorAction SilentlyContinue"},
            @{Name="Reset Top-10"; Cmd="Remove-Item data\top10_landlords.csv -Force -ErrorAction SilentlyContinue"},
            @{Name="Full Reset (⚠️)"; Cmd="Remove-Item data\*.csv,data\*.json -Force -ErrorAction SilentlyContinue"}
        )
    },
    @{
        Category = "📈 STATUS & MONITORING"
        Items = @(
            @{Name="Show File Sizes"; Cmd="Get-ChildItem data\*.csv,data\*.json | Select-Object Name,Length,LastWriteTime"},
            @{Name="Count Sandbox Files"; Cmd="@{Outbox=(Get-ChildItem data\sandbox\outbox).Count; Sent=(Get-ChildItem data\sandbox\sent).Count; Failed=(Get-ChildItem data\sandbox\failed).Count}"},
            @{Name="View Recent Activity"; Cmd="Get-ChildItem data\sandbox\sent -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name,LastWriteTime"},
            @{Name="Check Python Env"; Cmd="python --version; pip list | Select-String 'streamlit|pandas|serpapi'"}
        )
    }
)

foreach ($category in $commands) {
    Write-Host ""
    Write-Host $category.Category -ForegroundColor Yellow
    Write-Host ("-" * 70) -ForegroundColor DarkGray
    
    foreach ($item in $category.Items) {
        Write-Host "  • " -NoNewline -ForegroundColor Green
        Write-Host "$($item.Name)" -ForegroundColor White
        Write-Host "    " -NoNewline
        Write-Host $item.Cmd -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "=" * 70
Write-Host "💡 TIP: Copy any command above and paste in PowerShell" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host ""

Write-Host "📋 INTERACTIVE MENU:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose a command category to run:" -ForegroundColor White
Write-Host "  1) Quick Start (Launch UI)" -ForegroundColor White
Write-Host "  2) Pipeline Operations" -ForegroundColor White
Write-Host "  3) Data Review" -ForegroundColor White
Write-Host "  4) Approval Operations" -ForegroundColor White
Write-Host "  5) Package & Send" -ForegroundColor White
Write-Host "  6) OAuth & Gmail" -ForegroundColor White
Write-Host "  7) Cleanup & Maintenance" -ForegroundColor White
Write-Host "  8) Status & Monitoring" -ForegroundColor White
Write-Host "  9) Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-9)"

switch ($choice) {
    "1" { 
        Write-Host ""; Write-Host "🚀 Launching Mission Control..." -ForegroundColor Cyan
        .\scripts\launch_mission_control.ps1 
    }
    "2" {
        Write-Host ""; Write-Host "🔍 Running full pipeline..." -ForegroundColor Cyan
        python run_pipeline.py --dry-run
    }
    "3" {
        Write-Host ""; Write-Host "📊 Top-10 Curated Contacts:" -ForegroundColor Cyan
        Get-Content data\top10_landlords.csv | Select-Object -First 11
    }
    "4" {
        Write-Host ""; Write-Host "✅ Auto-approving Top 3..." -ForegroundColor Cyan
        python -c "import pandas as pd; df=pd.read_csv('data/top10_landlords.csv'); df.loc[0:2,'approved']=True; df.to_csv('data/top10_landlords.csv',index=False); print('✅ Top 3 approved')"
    }
    "5" {
        Write-Host ""; Write-Host "📦 Building packages..." -ForegroundColor Cyan
        python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv',pdf_dir='out',only_approved=True)"
    }
    "6" {
        Write-Host ""; Write-Host "🔐 Setting up OAuth..." -ForegroundColor Cyan
        python -c "import modules.gmailer as g; g.gmail_auth()"
    }
    "7" {
        Write-Host ""; Write-Host "🧹 Clearing sandbox..." -ForegroundColor Cyan
        Remove-Item data\sandbox\outbox\*,data\sandbox\sent\*,data\sandbox\failed\* -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Sandbox cleared!" -ForegroundColor Green
    }
    "8" {
        Write-Host ""; Write-Host "📈 System Status:" -ForegroundColor Cyan
        Get-ChildItem data\*.csv,data\*.json | Select-Object Name,Length,LastWriteTime | Format-Table
    }
    "9" {
        Write-Host ""; Write-Host "👋 Goodbye!" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host ""; Write-Host "❌ Invalid choice" -ForegroundColor Red
    }
}
