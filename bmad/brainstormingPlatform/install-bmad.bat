@echo off
setlocal EnableDelayedExpansion

REM Install BMAD method into a topic subfolder or the current directory.
REM Usage:
REM   install-bmad.bat --mode folder  topic platform [lang] [outlang]
REM   install-bmad.bat --mode current platform [lang] [outlang]
REM   install-bmad.bat topic platform [lang] [outlang]   (backward compat = folder mode)
REM
REM Modes:
REM   folder  - Create a topic subfolder under BRAINSTORMING_FOLDER and install CIS module (default)
REM   current - Install CIS + BMM modules into the current working directory
REM
REM Arguments:
REM   topic    = subfolder name (required in folder mode). No spaces allowed.
REM   platform = IDE/platform to configure (required). See BMAD-METHOD/tools/platform-codes.yaml.
REM   lang     = communication language. Default: German
REM   outlang  = document output language. Default: English

REM --- Parse --mode flag ---
set "MODE=folder"
if /i "%~1"=="--mode" (
    set "MODE=%~2"
    shift
    shift
)

REM --- Validate mode ---
if /i "%MODE%"=="folder" goto mode_ok
if /i "%MODE%"=="current" goto mode_ok
echo ERROR: invalid mode. Use "folder" or "current". Got: %MODE%
exit /b 1
:mode_ok

REM --- Branch by mode ---
if /i "%MODE%"=="current" goto mode_current

REM ============================================================
REM MODE: folder — existing behavior (install CIS into topic subfolder)
REM ============================================================

if not defined BRAINSTORMING_FOLDER goto base_dir_missing
set "BASE_DIR=%BRAINSTORMING_FOLDER%"
if not "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR%\"
goto base_dir_ok
:base_dir_missing
echo ERROR: BRAINSTORMING_FOLDER environment variable is not set.
echo Set it to the base directory for brainstorming topic folders, e.g. C:\PROJ\brainstormings
exit /b 1
:base_dir_ok

set "TOPIC=%~1"
set "PLATFORM=%~2"
set "LANG=%~3"
set "OUTLANG=%~4"

if "%TOPIC%"=="" goto topic_empty
goto topic_check_done
:topic_empty
echo ERROR: topic (subfolder name) is required in folder mode.
echo Usage: %~nx0 --mode folder topic platform [lang] [outlang]
echo   e.g. %~nx0 --mode folder my_project cursor German English
exit /b 1
:topic_check_done

REM Validate topic: no blanks allowed.
if "%TOPIC%"=="%TOPIC: =%" goto topic_ok
echo ERROR: topic must not contain blanks. Use underscores, e.g. my_great_idea
exit /b 1
:topic_ok

call :validate_platform "%PLATFORM%"
if errorlevel 1 exit /b 1

call :normalize_languages "%LANG%" "%OUTLANG%"
if errorlevel 1 exit /b 1

set "PROJECT_DIR=%BASE_DIR%%TOPIC%"

if exist "%PROJECT_DIR%" goto topic_exists
goto topic_new
:topic_exists
echo ERROR: topic folder already exists: %PROJECT_DIR%
echo Choose a different topic name or remove the existing folder.
exit /b 1
:topic_new

echo Creating directory: %PROJECT_DIR%
mkdir "%PROJECT_DIR%"

set "MODULES=cis"
goto do_install

REM ============================================================
REM MODE: current — install CIS + BMM into current directory
REM ============================================================
:mode_current

set "PLATFORM=%~1"
set "LANG=%~2"
set "OUTLANG=%~3"

call :validate_platform "%PLATFORM%"
if errorlevel 1 exit /b 1

call :normalize_languages "%LANG%" "%OUTLANG%"
if errorlevel 1 exit /b 1

set "PROJECT_DIR=%CD%"
set "MODULES=cis,bmm"
goto do_install

REM ============================================================
REM Common install logic
REM ============================================================
:do_install

echo Installing BMAD to: %PROJECT_DIR%
echo Mode: %MODE% / Modules: %MODULES%
echo Language: %LANG% / Output: %OUTLANG% / Platform: %PLATFORM%

call npx bmad-method install ^
  --directory "%PROJECT_DIR%" ^
  --modules %MODULES% ^
  --tools %PLATFORM% ^
  --user-name "Stefan" ^
  --communication-language %LANG% ^
  --document-output-language %OUTLANG% ^
  --output-folder _bmad-output ^
  --yes

if errorlevel 1 goto install_failed
echo BMAD installed successfully in %PROJECT_DIR%
endlocal
exit /b 0
:install_failed
echo BMAD install failed.
exit /b 1

REM ============================================================
REM Subroutine: validate_platform
REM ============================================================
:validate_platform
set "P=%~1"
if "%P%"=="" (
    echo ERROR: platform is required.
    echo Usage: %~nx0 [--mode folder^|current] [topic] platform [lang] [outlang]
    exit /b 1
)
if /i "%P%"=="claude-code" (set "PLATFORM=claude-code" & exit /b 0)
if /i "%P%"=="cursor" (set "PLATFORM=cursor" & exit /b 0)
if /i "%P%"=="cline" (set "PLATFORM=cline" & exit /b 0)
if /i "%P%"=="opencode" (set "PLATFORM=opencode" & exit /b 0)
if /i "%P%"=="codebuddy" (set "PLATFORM=codebuddy" & exit /b 0)
if /i "%P%"=="auggie" (set "PLATFORM=auggie" & exit /b 0)
if /i "%P%"=="roo" (set "PLATFORM=roo" & exit /b 0)
if /i "%P%"=="rovo-dev" (set "PLATFORM=rovo-dev" & exit /b 0)
if /i "%P%"=="kiro" (set "PLATFORM=kiro" & exit /b 0)
if /i "%P%"=="github-copilot" (set "PLATFORM=github-copilot" & exit /b 0)
if /i "%P%"=="codex" (set "PLATFORM=codex" & exit /b 0)
if /i "%P%"=="qwen" (set "PLATFORM=qwen" & exit /b 0)
if /i "%P%"=="gemini" (set "PLATFORM=gemini" & exit /b 0)
if /i "%P%"=="iflow" (set "PLATFORM=iflow" & exit /b 0)
if /i "%P%"=="kilo" (set "PLATFORM=kilo" & exit /b 0)
if /i "%P%"=="crush" (set "PLATFORM=crush" & exit /b 0)
if /i "%P%"=="antigravity" (set "PLATFORM=antigravity" & exit /b 0)
if /i "%P%"=="trae" (set "PLATFORM=trae" & exit /b 0)
if /i "%P%"=="windsurf" (set "PLATFORM=windsurf" & exit /b 0)
echo ERROR: invalid platform. See BMAD-METHOD/tools/platform-codes.yaml for valid codes. Got: %P%
exit /b 1

REM ============================================================
REM Subroutine: normalize_languages
REM ============================================================
:normalize_languages
set "EN=English"
set "DE=German"
set "L=%~1"
set "OL=%~2"

if "%L%"=="" set "L=%DE%"
if "%OL%"=="" set "OL=%EN%"

REM Validate and normalize input language
if /i "%L%"=="english" (set "LANG=%EN%" & goto nl_lang_ok)
if /i "%L%"=="german" (set "LANG=%DE%" & goto nl_lang_ok)
echo ERROR: language must be English or German. Got: %L%
exit /b 1
:nl_lang_ok

REM Validate and normalize output language
if /i "%OL%"=="english" (set "OUTLANG=%EN%" & goto nl_outlang_ok)
if /i "%OL%"=="german" (set "OUTLANG=%DE%" & goto nl_outlang_ok)
echo ERROR: output language must be English or German. Got: %OL%
exit /b 1
:nl_outlang_ok
exit /b 0
