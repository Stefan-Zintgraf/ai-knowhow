@ECHO OFF
REM ---------------------------------------------------------------------------
REM Parameter:
REM 1. Manual selection, e.g. Monitor
REM 2. Builder selection, e.g. Pdf
REM No parameter: Build all
REM ---------------------------------------------------------------------------

REM Command file for Sphinx documentation
pushd %~dp0

call ..\Common\Tools\SetEnv.bat

REM Manual selection
set INCLUDE_ECMONITOR=0
set INCLUDE_ECMONITOR_RELEASE_NOTES=0
set INCLUDE_ECMONITOR_QUICKSTART=0
REM Build step
set BUILD_CLEAN=0
set BUILD_CLEAN_ONLY=0
set BUILD_DOXYGEN=0
REM Builder
set BUILD_PDF=0
set BUILD_HTML=0
set BUILD_LIVE=0

if "%1" == "Clean" (
  set BUILD_CLEAN=1
  set BUILD_CLEAN_ONLY=1
)
if "%1" == "Doxygen"        set BUILD_DOXYGEN=1
if "%1" == "UserManual"     set INCLUDE_ECMONITOR=1
if "%1" == "QuickStart"     set INCLUDE_ECMONITOR_QUICKSTART=1
if "%1" == "ReleaseNotes"   set INCLUDE_ECMONITOR_RELEASE_NOTES=1
if "%1" == "" (
    set BUILD_CLEAN=1
    set BUILD_DOXYGEN=1
    set INCLUDE_ECMONITOR=1
    set INCLUDE_ECMONITOR_RELEASE_NOTES=1
    set INCLUDE_ECMONITOR_QUICKSTART=1
)

if "%2" == "Pdf"  set BUILD_PDF=1
if "%2" == "Html" set BUILD_HTML=1
if "%2" == "Live" set BUILD_LIVE=1
if "%2" == "" (
    set BUILD_PDF=1
    set BUILD_HTML=1
)

set SOURCEDIR=%~dp0.
set BUILDDIR=%~dp0_build
set CONFDIR=%~dp0Conf
set COMMONDIR=%~dp0..\Common
set COMMONTOOLSDIR=%~dp0..\Common\Tools

REM Clean up
if "1" == "%BUILD_CLEAN%" (
    if exist "%BUILDDIR%" rmdir /S /Q "%BUILDDIR%"
    mkdir "%BUILDDIR%"
    if "1" == "%BUILD_CLEAN_ONLY%" goto :end
)

if not exist "%BUILDDIR%"  mkdir "%BUILDDIR%"

%PYTHON% -m pip freeze > "%BUILDDIR%\python_packages.txt"

REM Generate XML for Sphinx - Breathe
if not exist "%BUILDDIR%\doxygen" (
    set BUILD_DOXYGEN=1
)
if "1" == "%BUILD_DOXYGEN%" (
    %DOXYGEN% %CONFDIR%\Doxyfile >"%BUILDDIR%\doxygen.log" 2>&1
    REM Patch doxygen's index.xml to avoid multiple matches for :doxygenfunction::
    pushd "%BUILDDIR%\doxygen\xml"
    %PYTHON% %COMMONTOOLSDIR%\PatchDoxygenXml.py
    %XALAN% -o combined.xml index.xml combine.xslt
    popd
)

REM Build documentation with Sphinx
if "1" == "%INCLUDE_ECMONITOR%" (
    set "ECMONITOR_DOCTYPE=User Manual" 
    set ECMONITOR_ATNUMBER="AT3401"
    call :buildManual UserManual
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\UserManual\latex\EC-Monitor_UserManual.pdf" ..\EC-Monitor_UserManual.pdf
    set ECMONITOR_DOCTYPE=
)
if "1" == "%INCLUDE_ECMONITOR_RELEASE_NOTES%" (
    set "ECMONITOR_DOCTYPE=Release Notes"
    set ECMONITOR_ATNUMBER="AT3400"
    call :buildManual ReleaseNotes
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ReleaseNotes\latex\EC-Monitor_ReleaseNotes.pdf" ..\EC-Monitor_ReleaseNotes.pdf
    set ECMONITOR_DOCTYPE=
)
if "1" == "%INCLUDE_ECMONITOR_QUICKSTART%" (
    set "ECMONITOR_DOCTYPE=Quick Start Guide"
    set ECMONITOR_ATNUMBER="AT3402"
    call :buildManual QuickStart
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\QuickStart\latex\EC-Monitor_QuickStartGuide.pdf" ..\EC-Monitor_QuickStart_Guide.pdf
    set ECMONITOR_DOCTYPE=
)
REM %SPHINXBUILD% -b spelling %SOURCEDIR% %BUILDDIR% -E -v -c %CONFDIR% -w %BUILDDIR%\build_pdf.log
goto :end

:buildManual
    set Name=%~1
    if "1" == "%BUILD_HTML%" (
        echo Generating EC-Monitor HTML %Name% ...
        %SPHINXBUILD% -M html      "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_html_error.log" >"%BUILDDIR%\build_%Name%_html.log" 2>&1
        type "%BUILDDIR%\build_%Name%_html_error.log"
        echo Finished.
    )

    if "1" == "%BUILD_PDF%" (
        echo Generating EC-Monitor PDF %Name% ...
        %SPHINXBUILD% -M latexpdf  "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_pdf_error.log" >"%BUILDDIR%\build_%Name%_pdf.log" 2>&1
        type "%BUILDDIR%\build_%Name%_pdf_error.log"
        findstr /n /c:"! LaTeX Error:" "%BUILDDIR%\build_%Name%_pdf.log"
        echo Finished.
    )

    if "1" == "%BUILD_LIVE%" (
        echo Start EC-Monitor doc live generation
        %SPHINXAUTOBUILD% "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -N -c "%CONFDIR%" --port=0 --open-browser
    )
@goto :eof

:end
popd

