# Start-KashmiriHeritage.ps1
# This script opens three separate PowerShell windows for DB, Backend, and Frontend.

$ProjectRoot = "C:\Users\SHAKIRSHABAN\Documents\kashmiri-dry-fruits"
$MySQLPath = "..\..\Downloads\mysql-8.0.45-winx64\mysql-8.0.45-winx64\bin\mysqld"

Write-Host "Starting Kashmiri Heritage Local Environment..." -ForegroundColor Cyan

# 1. Start Database
Write-Host "Starting MySQL Database..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot'; & '$MySQLPath' --console"

# 2. Start Backend
Write-Host "Starting Flask Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot'; .\backend\venv\Scripts\activate; `$env:FLASK_CONFIG='dev'; py .\backend\app.py"

# 3. Start Frontend
Write-Host "Starting Vue Frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\frontend'; npm run dev -- --port 3000"

Write-Host "All services are starting in separate windows." -ForegroundColor Green
