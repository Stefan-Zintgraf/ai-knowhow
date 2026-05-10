@echo off

rem ================================================================================================
rem Configuration
rem ================================================================================================

if "%DOXYGEN%" == "" (
	set DOXYGEN=C:\UserManual_Tools\doxygen\doxygen
)
if "%PYTHON%" == "" (
	set PYTHON=python
)
if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
	set SPHINXAUTOBUILD=sphinx-autobuild
)
if "%PLANTUML%" == "" (
	set PLANTUML=C:\UserManual_Tools\plantuml\plantuml.jar
)
if "%XALAN%" == "" (
	set XALAN=%~dp0..\..\..\Tools\Xalan
)

set Path=C:\UserManual_Tools\UniConvertor-2.0rc5\dlls;C:\UserManual_Tools\miktex\texmfs\install\miktex\bin\x64;C:\UserManual_Tools\Strawberry\perl\site\bin;C:\UserManual_Tools\Strawberry\perl\bin;%Path%;

set LATEXMKOPTS="-interaction=nonstopmode"

set PYTHONPATH=..\Common\Conf;%PYTHONPATH%
set PYTHONOPTIMIZE=TRUE
rem On Python Update, only change the path below
set PYTHON_DIR=\\at-srv-dev-2\EC\EC-Embedded\UserManual_Tools\Python3.8.12\pypy3.8-v7.3.9-win64
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set VENV_DIR=C:\UserManual_Tools\venv
set VENV_EXE=%VENV_DIR%\Scripts\python.exe
set VENV_ON=%VENV_DIR%\Scripts\activate.bat
set REQ_FILE=%~dp0..\Conf\requirements.txt
set WHEELS_DIR=%~dp0..\wheels

call :checkOrCreateVenv
call :activateVenv
call :updatePackages
goto :end


rem ================================================================================================
rem Check Python/venv and validate
rem ================================================================================================
:checkOrCreateVenv
    echo Validating Installations...
    if not exist "%PYTHON_EXE%" (
        echo [ERROR] Could not find Python-installation: %PYTHON_EXE%.
        goto :abort
    )
    setlocal enabledelayedexpansion
    for /f "tokens=2 delims= " %%a in ('call "%PYTHON_EXE%" --version ^| findstr /r "^Python"') do set PYTHON_VER=%%a
    if exist "%VENV_DIR%" (
        for /f "tokens=2 delims= " %%a in ('call "%VENV_EXE%" --version ^| findstr /r "^Python"') do set VENV_VER=%%a
        echo !VENV_VER! | findstr /c:"%PYTHON_VER%" >nul
        if errorlevel 1 (
            echo [WARNING] Venv version is not up-to-date; Rebuilding venv...
            rmdir /s /q "%VENV_DIR%" >nul
            "%PYTHON_EXE%" -m venv "%VENV_DIR%" >nul
            if exist "%VENV_DIR%" (
                for /f "tokens=2 delims= " %%a in ('call "%VENV_EXE%" --version ^| findstr /r "^Python"') do set VENV_VER=%%a
                echo !VENV_VER! | findstr /c:"%PYTHON_VER%" >nul
                if errorlevel 1 (
                    echo [ERROR] Could not rebuild venv; Still wrong version.
                    goto :abort
                )
            ) else (
                echo [ERROR] Could not rebuild venv; Creation failed.
                goto :abort
            )
        )
    ) else (
        echo [WARNING] Could not find venv; Creating a new one...
        "%PYTHON_EXE%" -m venv "%VENV_DIR%" >nul
        if not exist "%VENV_DIR%" (
            echo [ERROR] Could not create venv.
            goto :abort
        )
    )
    endlocal
goto :eof

rem ================================================================================================
rem Activate venv
rem ================================================================================================
:activateVenv
    if exist "%VENV_ON%" (
        call "%VENV_ON%"
    ) else (
        echo [ERROR] "%VENV_ON%" does not exist.
        goto :abort
    )
goto :eof

rem ================================================================================================
rem Optional: Update pip/setuptools/wheel
rem ================================================================================================
rem pip install --upgrade pip setuptools wheel

rem ================================================================================================
rem Install/Update packages from requirements.txt
rem ================================================================================================
:updatePackages
    if exist "%REQ_FILE%" (
        echo Installing/Updating packages from requirements.txt...
        pip install --upgrade --find-links="%WHEELS_DIR%" -r "%REQ_FILE%" --disable-pip-version-check >nul
    ) else (
        echo [WARNING] Could not find requirements.txt: %REQ_FILE%
        echo Continuing without Installation/Update of any packages...
    )
goto :eof

:abort
echo Aborting...
echo.
echo Press any key or close the window to exit...
pause >nul
exit /b 1

:end
echo Finished.
