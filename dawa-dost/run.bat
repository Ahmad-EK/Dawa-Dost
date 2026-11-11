@echo off
TITLE Dawa Dost (دوا دوست)
echo ===================================================
echo     Launching Dawa Dost (دوا دوست) Web Server
echo ===================================================
echo.

cd /d "%~dp0"

REM Find available Python executable
SET PYTHON_CMD=
IF EXIST "C:\msys64\ucrt64\bin\python.exe" (
    SET PYTHON_CMD="C:\msys64\ucrt64\bin\python.exe"
) ELSE (
    SET PYTHON_CMD=python
)

REM Open default browser automatically after 1 second
start "" cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:8080"

REM Launch Dawa Dost server
%PYTHON_CMD% "%~dp0backend\server.py"

pause
