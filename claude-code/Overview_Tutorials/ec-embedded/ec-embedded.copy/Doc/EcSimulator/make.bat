@ECHO OFF
REM ---------------------------------------------------------------------------
REM Parameter:
REM 1. Manual selection, e.g. UserManual
REM 2. Builder selection, e.g. Pdf
REM No parameter: Build all
REM ---------------------------------------------------------------------------

REM Command file for Sphinx documentation
pushd %~dp0

call ..\Common\Tools\SetEnv.bat

REM Manual selection
set INCLUDE_ECSIMULATOR_USERMANUAL=0
set INCLUDE_ECSIMULATOR_RELEASE_NOTES=0
set INCLUDE_ECSIMULATOR_QUICKSTART=0
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
if "%1" == "Doxygen"      set BUILD_DOXYGEN=1
if "%1" == "UserManual"   set INCLUDE_ECSIMULATOR_USERMANUAL=1
if "%1" == "QuickStart"   set INCLUDE_ECSIMULATOR_QUICKSTART=1
if "%1" == "ReleaseNotes" set INCLUDE_ECSIMULATOR_RELEASE_NOTES=1
if "%1" == "" (
    set BUILD_CLEAN=1
    set BUILD_DOXYGEN=1
    set INCLUDE_ECSIMULATOR_USERMANUAL=1
    set INCLUDE_ECSIMULATOR_QUICKSTART=1
    set INCLUDE_ECSIMULATOR_RELEASE_NOTES=1
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
if "1" == "%INCLUDE_ECSIMULATOR_USERMANUAL%" (
    set "ECSIMULATOR_DOCTYPE=User Manual"
    
    set ECSIMULATOR_ATNUMBER="AT3502"
	call :buildManual UserManual HiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\UserManual-HiL\latex\EC-Simulator_UserManual.pdf" ..\EC-Simulator-HiL_UserManual.pdf
	
    set ECSIMULATOR_ATNUMBER="AT3503"
	call :buildManual UserManual SiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\UserManual-SiL\latex\EC-Simulator_UserManual.pdf" ..\EC-Simulator-SiL_UserManual.pdf
	
    set ECSIMULATOR_DOCTYPE=
)
if "1" == "%INCLUDE_ECSIMULATOR_QUICKSTART%" (
    set "ECSIMULATOR_DOCTYPE=Quick Start Guide"
    
    set ECSIMULATOR_ATNUMBER="AT3504"
    call :buildManual QuickStart HiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\QuickStart-HiL\latex\EC-Simulator_QuickStartGuide.pdf" ..\EC-Simulator-HiL_QuickStart_Guide.pdf

    set ECSIMULATOR_ATNUMBER="AT3505"
    call :buildManual QuickStart SiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\QuickStart-SiL\latex\EC-Simulator_QuickStartGuide.pdf" ..\EC-Simulator-SiL_QuickStart_Guide.pdf

    set ECSIMULATOR_DOCTYPE=
)
if "1" == "%INCLUDE_ECSIMULATOR_RELEASE_NOTES%" (
    set "ECSIMULATOR_DOCTYPE=Release Notes"
    
    set ECSIMULATOR_ATNUMBER="AT3500"
    call :buildManual ReleaseNotes HiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ReleaseNotes-HiL\latex\EC-Simulator_ReleaseNotes.pdf" ..\EC-Simulator-HiL_ReleaseNotes.pdf

    set ECSIMULATOR_ATNUMBER="AT3501"
    call :buildManual ReleaseNotes SiL
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ReleaseNotes-SiL\latex\EC-Simulator_ReleaseNotes.pdf" ..\EC-Simulator-SiL_ReleaseNotes.pdf

    set ECSIMULATOR_DOCTYPE=
)
goto :end

:buildManual
    set Name=%~1
    set Edition=%~2
	set "ECSIMULATOR_EDITION=%~2"
    if "1" == "%BUILD_HTML%" (
        echo Generating EC-Simulator HTML %Name% %Edition% ...
        %SPHINXBUILD% -M html      "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%-%Edition%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_%Edition%_html_error.log" >"%BUILDDIR%\build_%Name%_%Edition%_html.log" 2>&1
        type "%BUILDDIR%\build_%Name%_%Edition%_html_error.log"
        echo Finished.
    )
    if "1" == "%BUILD_PDF%" (
        echo Generating EC-Simulator PDF %Name% %Edition% ...
        %SPHINXBUILD% -M latexpdf  "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%-%Edition%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_%Edition%_pdf_error.log" >"%BUILDDIR%\build_%Name%_%Edition%_pdf.log" 2>&1
        type "%BUILDDIR%\build_%Name%_%Edition%_pdf_error.log"
        findstr /n /c:"! LaTeX Error:" "%BUILDDIR%\build_%Name%_%Edition%_pdf.log"
        echo Finished.
    )
    if "1" == "%BUILD_LIVE%" (
        echo Start EC-Simulator doc live generation
        START /B %SPHINXAUTOBUILD% "%SOURCEDIR%" "%BUILDDIR%\%Name%-%Edition%" -N -c "%CONFDIR%" --port=0 --open-browser
    )
    set ECSIMULATOR_EDITION=
@goto :eof

:end
popd

