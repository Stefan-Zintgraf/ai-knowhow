@echo off
setlocal enabledelayedexpansion

:: set_ollama_proxy.bat - Configure Windows portproxy for Ollama
:: Usage: set_ollama_proxy.bat -on | -off | -show
:: Run as Administrator for -on and -off

set REMOTE_IP=172.17.5.114
set REMOTE_PORT=11434
set LOCAL_PORT=12434
set RULE_NAME=Ollama Proxy %LOCAL_PORT%

if "%~1"=="" goto usage
if /i "%~1"=="-on"   goto on
if /i "%~1"=="-off"  goto off
if /i "%~1"=="-show" goto show
goto usage

:usage
echo Usage: set_ollama_proxy.bat -on ^| -off ^| -show
echo.
echo   -on    Enable proxy: forwards remote Ollama %REMOTE_IP%:%REMOTE_PORT% to local port %LOCAL_PORT%
echo   -off   Remove proxy and firewall rules
echo   -show  Show proxy and firewall status
echo.
echo Run as Administrator for -on and -off.
exit /b 1

:on
call :check_admin
if errorlevel 1 exit /b 1
echo Enabling Ollama proxy: %REMOTE_IP%:%REMOTE_PORT% -^> localhost:%LOCAL_PORT%
echo.
echo [1/4] Adding portproxy (127.0.0.1 and 0.0.0.0)...
netsh interface portproxy add v4tov4 listenport=%LOCAL_PORT% listenaddress=127.0.0.1 connectport=%REMOTE_PORT% connectaddress=%REMOTE_IP% 2>nul
netsh interface portproxy add v4tov4 listenport=%LOCAL_PORT% listenaddress=0.0.0.0 connectport=%REMOTE_PORT% connectaddress=%REMOTE_IP% 2>nul
echo [2/4] Starting IP Helper service...
sc start iphlpsvc >nul 2>&1
echo [3/4] Adding firewall rule (allow port %LOCAL_PORT%)...
netsh advfirewall firewall delete rule name="%RULE_NAME%" >nul 2>&1
netsh advfirewall firewall add rule name="%RULE_NAME%" dir=in action=allow protocol=TCP localport=%LOCAL_PORT%
echo [4/4] Done.
echo.
echo Proxy enabled. Firewall allows port %LOCAL_PORT%. Test: curl http://127.0.0.1:%LOCAL_PORT%/api/tags
goto end

:off
call :check_admin
if errorlevel 1 exit /b 1
echo Disabling Ollama proxy (port %LOCAL_PORT% -^> %REMOTE_IP%:%REMOTE_PORT%)...
echo.
netsh interface portproxy delete v4tov4 listenport=%LOCAL_PORT% listenaddress=127.0.0.1 2>nul
netsh interface portproxy delete v4tov4 listenport=%LOCAL_PORT% listenaddress=0.0.0.0 2>nul
netsh advfirewall firewall delete rule name="%RULE_NAME%" 2>nul
echo Proxy and firewall rules removed.
goto end

:show
echo Ollama Proxy Status
echo Forwards: remote %REMOTE_IP%:%REMOTE_PORT% -^> local port %LOCAL_PORT%
echo.
echo Portproxy:
netsh interface portproxy show v4tov4 2>nul | findstr /C:"%LOCAL_PORT%" >nul 2>&1
if errorlevel 1 (
    echo   [ ] Not configured
) else (
    echo   [OK] Enabled - traffic to port %LOCAL_PORT% is forwarded to %REMOTE_IP%:%REMOTE_PORT%
)
echo.
echo Firewall:
netsh advfirewall firewall show rule name="%RULE_NAME%" 2>nul | findstr /C:"%RULE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo   [ ] No rule - port %LOCAL_PORT% may be blocked
) else (
    echo   [OK] Port %LOCAL_PORT% allowed - not blocked
)
echo.
goto end

:check_admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Run as Administrator.
    exit /b 1
)
exit /b 0

:end
endlocal
