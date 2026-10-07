@echo off
setlocal
title TX-ADE Course Shell
cd /d "%~dp0"

echo ========================================================
echo        TX-ADE TEXAS ADULT DRIVER ED // COURSE SHELL
echo ========================================================
echo.
echo Launching Course Shell...
echo.

python serve.py
if %ERRORLEVEL% EQU 0 goto :EOF

py serve.py
if %ERRORLEVEL% EQU 0 goto :EOF

echo Python executable not detected in PATH.
echo Launching index.html directly in your default browser...
start "" "%~dp0index.html"

pause
