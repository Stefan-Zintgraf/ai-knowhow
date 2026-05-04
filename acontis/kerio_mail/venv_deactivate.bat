@echo off
REM Kerio mail tools: deactivates venv in cmd.exe if activated with venv_activate.bat
if not defined VIRTUAL_ENV (
    echo No venv active in this session ^(VIRTUAL_ENV not set^). 1>&2
    exit /b 1
)
call deactivate
