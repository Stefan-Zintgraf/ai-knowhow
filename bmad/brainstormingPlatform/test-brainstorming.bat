@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM Test suite for install-bmad.bat
REM Runs all test cases, logs output to test-logs\ folder.
REM Usage: test-brainstorming.bat [--cleanup]
REM   --cleanup  removes test directories created during the run
REM ============================================================

set "SCRIPT_DIR=%~dp0"
set "LOG_DIR=%SCRIPT_DIR%test-logs"
set "PASS=0"
set "FAIL=0"
set "TOTAL=0"
set "CLEANUP=0"
set "TIMESTAMP=%DATE:~-4%%DATE:~-7,2%%DATE:~-10,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

if /i "%~1"=="--cleanup" set "CLEANUP=1"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo ============================================================
echo  BMAD install-bmad.bat Test Suite
echo  %DATE% %TIME%
echo ============================================================
echo.

REM --- Test 1: Folder mode, happy path ---
set /a TOTAL+=1
set "TEST_TOPIC=test_happy_%RANDOM%"
echo [Test 1] Folder mode, happy path (topic: %TEST_TOPIC%)
call "%SCRIPT_DIR%install-bmad.bat" --mode folder %TEST_TOPIC% claude-code German English > "%LOG_DIR%\test1_folder_happy.log" 2>&1
if !errorlevel! equ 0 (
    echo   PASS: exit code 0
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 0, got !errorlevel!
    set /a FAIL+=1
)
if %CLEANUP%==1 if exist "%BRAINSTORMING_FOLDER%\%TEST_TOPIC%" rmdir /s /q "%BRAINSTORMING_FOLDER%\%TEST_TOPIC%"

REM --- Test 2: Folder mode, missing BRAINSTORMING_FOLDER ---
set /a TOTAL+=1
echo [Test 2] Folder mode, missing BRAINSTORMING_FOLDER
set "SAVED_BF=%BRAINSTORMING_FOLDER%"
set "BRAINSTORMING_FOLDER="
call "%SCRIPT_DIR%install-bmad.bat" --mode folder test_no_bf claude-code > "%LOG_DIR%\test2_folder_no_bf.log" 2>&1
if !errorlevel! equ 1 (
    echo   PASS: exit code 1 ^(expected^)
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 1, got !errorlevel!
    set /a FAIL+=1
)
set "BRAINSTORMING_FOLDER=%SAVED_BF%"

REM --- Test 3: Folder mode, topic with spaces ---
set /a TOTAL+=1
echo [Test 3] Folder mode, topic with spaces
call "%SCRIPT_DIR%install-bmad.bat" --mode folder "bad topic" claude-code > "%LOG_DIR%\test3_folder_spaces.log" 2>&1
if !errorlevel! equ 1 (
    echo   PASS: exit code 1 ^(expected^)
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 1, got !errorlevel!
    set /a FAIL+=1
)

REM --- Test 4: Folder mode, duplicate topic ---
set /a TOTAL+=1
set "TEST_TOPIC_DUP=test_dup_%RANDOM%"
echo [Test 4] Folder mode, duplicate topic (topic: %TEST_TOPIC_DUP%)
REM First run: should succeed
call "%SCRIPT_DIR%install-bmad.bat" --mode folder %TEST_TOPIC_DUP% claude-code German English > "%LOG_DIR%\test4_folder_dup_first.log" 2>&1
REM Second run: should fail
call "%SCRIPT_DIR%install-bmad.bat" --mode folder %TEST_TOPIC_DUP% claude-code German English > "%LOG_DIR%\test4_folder_dup_second.log" 2>&1
if !errorlevel! equ 1 (
    echo   PASS: exit code 1 on duplicate ^(expected^)
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 1 on duplicate, got !errorlevel!
    set /a FAIL+=1
)
if %CLEANUP%==1 if exist "%BRAINSTORMING_FOLDER%\%TEST_TOPIC_DUP%" rmdir /s /q "%BRAINSTORMING_FOLDER%\%TEST_TOPIC_DUP%"

REM --- Test 5: Current mode, happy path ---
set /a TOTAL+=1
set "TEST_CURRENT_DIR=%TEMP%\bmad_test_current_%RANDOM%"
echo [Test 5] Current mode, happy path (dir: %TEST_CURRENT_DIR%)
mkdir "%TEST_CURRENT_DIR%" 2>nul
pushd "%TEST_CURRENT_DIR%"
call "%SCRIPT_DIR%install-bmad.bat" --mode current claude-code German English > "%LOG_DIR%\test5_current_happy.log" 2>&1
if !errorlevel! equ 0 (
    echo   PASS: exit code 0
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 0, got !errorlevel!
    set /a FAIL+=1
)
popd
if %CLEANUP%==1 if exist "%TEST_CURRENT_DIR%" rmdir /s /q "%TEST_CURRENT_DIR%"

REM --- Test 6: Backward compat (no --mode flag) ---
set /a TOTAL+=1
set "TEST_TOPIC_COMPAT=test_compat_%RANDOM%"
echo [Test 6] Backward compat, no --mode flag (topic: %TEST_TOPIC_COMPAT%)
call "%SCRIPT_DIR%install-bmad.bat" %TEST_TOPIC_COMPAT% claude-code German English > "%LOG_DIR%\test6_compat.log" 2>&1
if !errorlevel! equ 0 (
    echo   PASS: exit code 0
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 0, got !errorlevel!
    set /a FAIL+=1
)
if %CLEANUP%==1 if exist "%BRAINSTORMING_FOLDER%\%TEST_TOPIC_COMPAT%" rmdir /s /q "%BRAINSTORMING_FOLDER%\%TEST_TOPIC_COMPAT%"

REM --- Test 7: Invalid platform ---
set /a TOTAL+=1
echo [Test 7] Invalid platform
call "%SCRIPT_DIR%install-bmad.bat" --mode folder test_invalid_plat notaplatform > "%LOG_DIR%\test7_invalid_platform.log" 2>&1
if !errorlevel! equ 1 (
    echo   PASS: exit code 1 ^(expected^)
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 1, got !errorlevel!
    set /a FAIL+=1
)

REM --- Test 8: Invalid language ---
set /a TOTAL+=1
echo [Test 8] Invalid language
call "%SCRIPT_DIR%install-bmad.bat" --mode folder test_invalid_lang claude-code Klingon > "%LOG_DIR%\test8_invalid_lang.log" 2>&1
if !errorlevel! equ 1 (
    echo   PASS: exit code 1 ^(expected^)
    set /a PASS+=1
) else (
    echo   FAIL: expected exit code 1, got !errorlevel!
    set /a FAIL+=1
)

REM --- Summary ---
echo.
echo ============================================================
echo  Results: %PASS%/%TOTAL% passed, %FAIL% failed
echo  Logs in: %LOG_DIR%
echo ============================================================

if %FAIL% gtr 0 exit /b 1
exit /b 0
