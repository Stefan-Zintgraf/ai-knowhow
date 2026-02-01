@ECHO OFF
REM ---------------------------------------------------------------------------
REM Parameter:
REM 1. Manual selection, e.g. Master, Simulator
REM 2. Builder selection, e.g. Pdf
REM No parameter: Build all
REM ---------------------------------------------------------------------------

REM Command file for Sphinx documentation
pushd %~dp0

call ..\Common\Tools\SetEnv.bat

REM Manual selection
set INCLUDE_ECMASTER=0
set INCLUDE_ECSIMULATOR=0
REM Build step
set BUILD_CLEAN=0
set BUILD_CLEAN_ONLY=0
REM Builder
set BUILD_PDF=0
set BUILD_HTML=0
set BUILD_LIVE=0

if "%1" == "Clean" (
  set BUILD_CLEAN=1
  set BUILD_CLEAN_ONLY=1
)
if "%1" == "Master"    set INCLUDE_ECMASTER=1
if "%1" == "Simulator" set INCLUDE_ECSIMULATOR=1
if "%1" == "" (
    set BUILD_CLEAN=1
    set INCLUDE_ECMASTER=1
    set INCLUDE_ECSIMULATOR=0
)

if "%2" == "Pdf"  set BUILD_PDF=1
if "%2" == "Html" set BUILD_HTML=1
if "%2" == "Live" set BUILD_LIVE=1
if "%2" == "" (
    set BUILD_PDF=1
    set BUILD_HTML=1
)

set SOURCEDIR=%~dp0.
set BUILDDIRBASE=%~dp0_build
set CONFDIR=%~dp0Conf
set COMMONDIR=%~dp0..\Common
set COMMONTOOLSDIR=%~dp0..\Common\Tools

REM Clean up
if "1" == "%BUILD_CLEAN%" (
    if exist "%BUILDDIRBASE%" rmdir /S /Q "%BUILDDIRBASE%"
    mkdir "%BUILDDIRBASE%"
    if "1" == "%BUILD_CLEAN_ONLY%" goto :end
)

%PYTHON% -m pip freeze > %BUILDDIRBASE%\python_packages.txt 2>&1

REM Build documentation with Sphinx
if "1" == "%INCLUDE_ECMASTER%" (
    set ECWRAPPERSWIFT_ATNUMBER="AT3307"
    call :buildManualAndCopy EC-Master
)

if "1" == "%INCLUDE_ECSIMULATOR%" (
    set ECWRAPPERSWIFT_ATNUMBER="AT3509"
    call :buildManualAndCopy EC-Simulator
)

goto :end

:buildManualAndCopy
    set "PRODUCTNAME=%1"
    set "BUILDDIR=%BUILDDIRBASE%\%PRODUCTNAME%"
    mkdir %BUILDDIR%
    call :buildManual
    if "1" == "%BUILD_PDF%" copy %BUILDDIR%\latex\%PRODUCTNAME%_Swift.pdf ..\%PRODUCTNAME%_Swift.pdf
@goto :eof

:buildManual
    if "1" == "%BUILD_HTML%" (
        echo Generating %PRODUCTNAME% Swift HTML User Manual...
        %SPHINXBUILD% -M html      "%SOURCEDIR%" "%BUILDDIR%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_html_error.log" >"%BUILDDIR%\build_html.log" 2>&1
        type "%BUILDDIR%\build_html_error.log"
        echo Finished.
    )

    if "1" == "%BUILD_PDF%" (
        echo Generating %PRODUCTNAME% Swift PDF User Manual...
        %SPHINXBUILD% -M latexpdf  "%SOURCEDIR%" "%BUILDDIR%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_pdf_error.log" >"%BUILDDIR%\build_pdf.log" 2>&1
        type "%BUILDDIR%\build_pdf_error.log"
        findstr /n /c:"! LaTeX Error:" "%BUILDDIR%\build_pdf.log"
        echo Finished.
    )

    if "1" == "%BUILD_LIVE%" (
        echo Start %PRODUCTNAME% Swift doc live generation
        START /B %SPHINXAUTOBUILD% "%SOURCEDIR%" "%BUILDDIR%" -N -c "%CONFDIR%" --port=0 --open-browser
    )
@goto :eof

:end
popd

