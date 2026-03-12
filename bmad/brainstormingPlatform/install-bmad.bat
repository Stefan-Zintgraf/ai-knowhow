@echo off
setlocal EnableDelayedExpansion

REM Install BMAD method - brainstorming and CIS - into a topic subfolder under C:\PROJ\brainstormings
REM Usage: install-bmad.bat topic platform [lang] [outlang]
REM   topic    = subfolder name (required). BMAD is installed to %BRAINSTORMING_FOLDER%\<topic>
REM   platform = IDE/platform to configure (required). See BMAD-METHOD/tools/platform-codes.yaml for full list.
REM   lang     = communication and default document language. Default: German
REM   outlang  = document output language, overrides lang for output. Default: English

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
set "EN=English"
set "DE=German"

if "%TOPIC%"=="" goto topic_empty
goto topic_check_done
:topic_empty
echo ERROR: topic (subfolder name) is required.
echo Usage: %~nx0 topic platform [lang] [outlang]
echo   e.g. %~nx0 my_project cursor German English
exit /b 1
:topic_check_done

REM Validate topic: no blanks allowed. Replace space by nothing; if result differs, topic had a space.
if "%TOPIC%"=="%TOPIC: =%" goto topic_ok
echo ERROR: topic must not contain blanks. Use underscores, e.g. my_great_idea
exit /b 1
:topic_ok

if "%PLATFORM%"=="" goto platform_empty
goto platform_check_done
:platform_empty
echo ERROR: platform is required.
echo Usage: %~nx0 topic platform [lang] [outlang]
echo   e.g. %~nx0 my_project cursor German English
exit /b 1
:platform_check_done

REM Validate platform: all codes from BMAD-METHOD/tools/platform-codes.yaml
REM To allow "none" to skip platform config, uncomment the next line.
if /i "%PLATFORM%"=="claude-code" (set "PLATFORM=claude-code" & goto platform_ok)
if /i "%PLATFORM%"=="cursor" (set "PLATFORM=cursor" & goto platform_ok)
if /i "%PLATFORM%"=="cline" (set "PLATFORM=cline" & goto platform_ok)
if /i "%PLATFORM%"=="opencode" (set "PLATFORM=opencode" & goto platform_ok)
if /i "%PLATFORM%"=="codebuddy" (set "PLATFORM=codebuddy" & goto platform_ok)
if /i "%PLATFORM%"=="auggie" (set "PLATFORM=auggie" & goto platform_ok)
if /i "%PLATFORM%"=="roo" (set "PLATFORM=roo" & goto platform_ok)
if /i "%PLATFORM%"=="rovo-dev" (set "PLATFORM=rovo-dev" & goto platform_ok)
if /i "%PLATFORM%"=="kiro" (set "PLATFORM=kiro" & goto platform_ok)
if /i "%PLATFORM%"=="github-copilot" (set "PLATFORM=github-copilot" & goto platform_ok)
if /i "%PLATFORM%"=="codex" (set "PLATFORM=codex" & goto platform_ok)
if /i "%PLATFORM%"=="qwen" (set "PLATFORM=qwen" & goto platform_ok)
if /i "%PLATFORM%"=="gemini" (set "PLATFORM=gemini" & goto platform_ok)
if /i "%PLATFORM%"=="iflow" (set "PLATFORM=iflow" & goto platform_ok)
if /i "%PLATFORM%"=="kilo" (set "PLATFORM=kilo" & goto platform_ok)
if /i "%PLATFORM%"=="crush" (set "PLATFORM=crush" & goto platform_ok)
if /i "%PLATFORM%"=="antigravity" (set "PLATFORM=antigravity" & goto platform_ok)
if /i "%PLATFORM%"=="trae" (set "PLATFORM=trae" & goto platform_ok)
if /i "%PLATFORM%"=="windsurf" (set "PLATFORM=windsurf" & goto platform_ok)
REM if /i "%PLATFORM%"=="none" set "PLATFORM=none" & goto platform_ok
echo ERROR: invalid platform. See BMAD-METHOD/tools/platform-codes.yaml for valid codes. Got: %PLATFORM%
exit /b 1
:platform_ok

if "%LANG%"=="" set LANG=%DE%
if "%OUTLANG%"=="" set OUTLANG=%EN%

REM Validate and normalize input language: English or German only
if /i "%LANG%"=="english" goto set_lang_english
if /i "%LANG%"=="german" goto set_lang_german
echo ERROR: language must be English or German. Got: %LANG%
exit /b 1
:set_lang_english
set LANG=%EN%
goto lang_ok
:set_lang_german
set LANG=%DE%
goto lang_ok
:lang_ok

REM Validate and normalize output language: English or German only
if /i "%OUTLANG%"=="english" goto set_outlang_english
if /i "%OUTLANG%"=="german" goto set_outlang_german
echo ERROR: output language must be English or German. Got: %OUTLANG%
exit /b 1
:set_outlang_english
set OUTLANG=%EN%
goto outlang_ok
:set_outlang_german
set OUTLANG=%DE%
goto outlang_ok
:outlang_ok

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
:dir_done

echo Installing BMAD to: %PROJECT_DIR%
echo Language: %LANG% / Output: %OUTLANG% / Platform: %PLATFORM%

call npx bmad-method install ^
  --directory "%PROJECT_DIR%" ^
  --modules cis ^
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
