# Dawa Dost (دوا دوست) PowerShell Runner
Set-Location -Path $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Green
Write-Host "    Launching Dawa Dost (دوا دوست) Web Server" -ForegroundColor Cyan
Write-Host "    Opening at http://localhost:8080" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Green

$pythonExe = "python"
if (Test-Path "C:\msys64\ucrt64\bin\python.exe") {
    $pythonExe = "C:\msys64\ucrt64\bin\python.exe"
}

# Automatically open default browser
Start-Process "http://localhost:8080"

& $pythonExe "$PSScriptRoot\backend\server.py"
