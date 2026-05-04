@echo off
REM Kerio mail tools: activates .venv for the current cmd.exe session.
REM For PowerShell, use:  . .\venv_activate.ps1
setlocal
cd /d "%~dp0"
if not exist "%~dp0.venv\Scripts\activate.bat" (
    echo Error: .venv not found. Run venv_install.bat first. 1>&2
    exit /b 1
)
call "%~dp0.venv\Scripts\activate.bat"
endlocal
