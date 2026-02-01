@ECHO OFF
REM ---------------------------------------------------------------------------
REM Parameter:
REM 1. Manual selection, e.g. ClassA
REM 2. Builder selection, e.g. Pdf
REM No parameter: Build all
REM ---------------------------------------------------------------------------

REM Command file for Sphinx documentation
pushd %~dp0

call ..\Common\Tools\SetEnv.bat

REM Manual selection
set INCLUDE_ECDAQ_USERMANUAL=0
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
if "%1" == "Doxygen" set BUILD_DOXYGEN=1
if "%1" == "UserManual"  set INCLUDE_ECDAQ=1
if "%1" == "" (
    set BUILD_CLEAN=1
    set BUILD_DOXYGEN=1
    set INCLUDE_ECDAQ=1
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
if "1" == "%INCLUDE_ECDAQ%" (
    set ECDAQ_ATNUMBER="AT3650"
    call :buildManual UserManual
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\UserManual\latex\EC-Daq_UserManual.pdf" ..\EC-Daq_UserManual.pdf
)

goto :end

:buildManual
    set Name=%~1

    if "1" == "%BUILD_HTML%" (
        echo Generating EC-Daq %Name% HTML User Manual...
        %SPHINXBUILD% -M html      "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_html_error.log" >"%BUILDDIR%\build_%Name%_html.log" 2>&1
        type "%BUILDDIR%\build_%Name%_html_error.log"
        echo Finished.
    )

    if "1" == "%BUILD_PDF%" (
        echo Generating EC-Daq %Name% PDF User Manual...
        %SPHINXBUILD% -M latexpdf  "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_pdf_error.log" >"%BUILDDIR%\build_%Name%_pdf.log" 2>&1
        type "%BUILDDIR%\build_%Name%_pdf_error.log"
        echo Finished.
    )

    if "1" == "%BUILD_LIVE%" (
        echo Start EC-Daq doc live generation
        START /B %SPHINXAUTOBUILD% "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -N -c "%CONFDIR%" --port=0 --open-browser
    )
@goto :eof

:end
popd

