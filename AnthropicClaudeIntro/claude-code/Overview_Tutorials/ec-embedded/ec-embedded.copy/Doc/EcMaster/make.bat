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
set INCLUDE_ECMASTER_CLASS_A=0
set INCLUDE_ECMASTER_CLASS_B=0
set INCLUDE_ECMASTER_FP_CABLE_REDUNDANCY=0
set INCLUDE_ECMASTER_FP_EOE_ENDPOINT=0
set INCLUDE_ECMASTER_FP_EOE_GATEWAY=0
set INCLUDE_ECMASTER_FP_HOT_CONNECT=0
set INCLUDE_ECMASTER_FP_RAS=0
set INCLUDE_ECMASTER_FP_SPLIT_FRAME_PROC=0
set INCLUDE_ECMASTER_FP_SUPERSET_ENI=0
set INCLUDE_ECMASTER_FP_UDP_MAILBOX_GATEWAY=0
set INCLUDE_ECMASTER_FP_EXTERNAL_SYNC=0
set INCLUDE_ECMASTER_FP_MQTT=0
set INCLUDE_ECMASTER_RELEASE_NOTES=0
REM Build step
set BUILD_CLEAN=0
set BUILD_CLEAN_ONLY=0
set BUILD_DOXYGEN=0
REM Builder
set BUILD_PDF=0
set BUILD_HTML=0
set BUILD_LIVE=0

set ECMASTER_FP=
set ECMASTER_CLASS=
set ECMASTER_ATNUMBER=

if "%1" == "Clean" (
  set BUILD_CLEAN=1
  set BUILD_CLEAN_ONLY=1
)
if "%1" == "Doxygen" set BUILD_DOXYGEN=1
if "%1" == "ClassA"  set INCLUDE_ECMASTER_CLASS_A=1
if "%1" == "ClassB"  set INCLUDE_ECMASTER_CLASS_B=1
if "%1" == "FP-Cable-Redundancy"        set INCLUDE_ECMASTER_FP_CABLE_REDUNDANCY=1
if "%1" == "FP-EoE-EndPoint"            set INCLUDE_ECMASTER_FP_EOE_ENDPOINT=1
if "%1" == "FP-EoE-Gateway"            	set INCLUDE_ECMASTER_FP_EOE_GATEWAY=1
if "%1" == "FP-External-Sync"           set INCLUDE_ECMASTER_FP_EXTERNAL_SYNC=1
if "%1" == "FP-Hot-Connect"             set INCLUDE_ECMASTER_FP_HOT_CONNECT=1
if "%1" == "FP-MQTT"                    set INCLUDE_ECMASTER_FP_MQTT=1
if "%1" == "FP-RAS"                     set INCLUDE_ECMASTER_FP_RAS=1
if "%1" == "FP-Split-Frame-Processing"  set INCLUDE_ECMASTER_FP_SPLIT_FRAME_PROC=1
if "%1" == "FP-Superset-ENI"            set INCLUDE_ECMASTER_FP_SUPERSET_ENI=1
if "%1" == "FP-UDP-Mailbox-Gateway"     set INCLUDE_ECMASTER_FP_UDP_MAILBOX_GATEWAY=1
if "%1" == "ReleaseNotes"               set INCLUDE_ECMASTER_RELEASE_NOTES=1
if "%1" == "" (
    set BUILD_CLEAN=1
    set BUILD_DOXYGEN=1
    set INCLUDE_ECMASTER_CLASS_A=1
    set INCLUDE_ECMASTER_CLASS_B=1
    set INCLUDE_ECMASTER_FP_CABLE_REDUNDANCY=1
    set INCLUDE_ECMASTER_FP_EOE_ENDPOINT=1
    set INCLUDE_ECMASTER_FP_EOE_GATEWAY=1
    set INCLUDE_ECMASTER_FP_EXTERNAL_SYNC=1
    set INCLUDE_ECMASTER_FP_HOT_CONNECT=1
    set INCLUDE_ECMASTER_FP_MQTT=1
    set INCLUDE_ECMASTER_FP_RAS=1
    set INCLUDE_ECMASTER_FP_SPLIT_FRAME_PROC=1
    set INCLUDE_ECMASTER_FP_SUPERSET_ENI=1
    set INCLUDE_ECMASTER_FP_UDP_MAILBOX_GATEWAY=1
    set INCLUDE_ECMASTER_RELEASE_NOTES=1
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
if "1" == "%INCLUDE_ECMASTER_CLASS_A%" (
    set ECMASTER_CLASS=A
    set ECMASTER_ATNUMBER="AT3301"
    call :buildManual ClassA
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ClassA\latex\EC-Master_ClassA.pdf" ..\EC-Master_ClassA.pdf
    set ECMASTER_CLASS=
)

if "1" == "%INCLUDE_ECMASTER_CLASS_B%" (
    set ECMASTER_CLASS=B
    set ECMASTER_ATNUMBER="AT3302"
    call :buildManual ClassB
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ClassB\latex\EC-Master_ClassB.pdf" ..\EC-Master_UserManual.pdf
    set ECMASTER_CLASS=
)
	
if "1" == "%INCLUDE_ECMASTER_FP_CABLE_REDUNDANCY%" (
    set ECMASTER_FP="Cable-Redundancy"
    set ECMASTER_ATNUMBER="AT3310"
    call :buildManual FP-Cable-Redundancy
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-Cable-Redundancy\latex\EC-Master-FP-Cable-Redundancy.pdf" ..\EC-Master-FP-Cable-Redundancy.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_EOE_ENDPOINT%" (
    set ECMASTER_FP="EoE-Endpoint"
    set ECMASTER_ATNUMBER="AT3311"
    call :buildManual FP-EoE-EndPoint
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-EoE-EndPoint\latex\EC-Master-FP-EoE-EndPoint.pdf" ..\EC-Master-FP-EoE-EndPoint.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_EOE_GATEWAY%" (
    set ECMASTER_FP="EoE-Gateway"
    set ECMASTER_ATNUMBER="AT3312"
    call :buildManual FP-EoE-Gateway
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-EoE-Gateway\latex\EC-Master-FP-EoE-Gateway.pdf" ..\EC-Master-FP-EoE-Gateway.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_HOT_CONNECT%" (
    set ECMASTER_FP="Hot-Connect"
    set ECMASTER_ATNUMBER="AT3315"
    call :buildManual FP-Hot-Connect
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-Hot-Connect\latex\EC-Master-FP-Hot-Connect.pdf" ..\EC-Master-FP-Hot-Connect.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_RAS%" (
    set ECMASTER_FP="RAS"
    set ECMASTER_ATNUMBER="AT3318"
    call :buildManual FP-RAS
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-RAS\latex\EC-Master-FP-RAS.pdf" ..\EC-Master-FP-RAS.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_SPLIT_FRAME_PROC%" (
    set ECMASTER_FP="Split-Frame-Processing"
    set ECMASTER_ATNUMBER="AT3320"
    call :buildManual FP-Split-Frame-Processing
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-Split-Frame-Processing\latex\EC-Master-FP-Split-Frame-Processing.pdf" ..\EC-Master-FP-Split-Frame-Processing.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_SUPERSET_ENI%" (
    set ECMASTER_FP="Superset-ENI"
    set ECMASTER_ATNUMBER="AT3321"
    call :buildManual FP-Superset-ENI
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-Superset-ENI\latex\EC-Master-FP-Superset-ENI.pdf" ..\EC-Master-FP-Superset-ENI.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_UDP_MAILBOX_GATEWAY%" (
    set ECMASTER_FP="UDP-Mailbox-Gateway"
    set ECMASTER_ATNUMBER="AT3322"
    call :buildManual FP-UDP-Mailbox-Gateway
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-UDP-Mailbox-Gateway\latex\EC-Master-FP-UDP-Mailbox-Gateway.pdf" ..\EC-Master-FP-UDP-Mailbox-Gateway.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_EXTERNAL_SYNC%" (
    set ECMASTER_FP="External-Synchronization"
    set ECMASTER_ATNUMBER="AT3314"
    call :buildManual FP-External-Sync
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-External-Sync\latex\EC-Master-FP-External-Synchronization.pdf" ..\EC-Master-FP-External-Sync.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_FP_MQTT%" (
    set ECMASTER_FP="MQTT"
    set ECMASTER_ATNUMBER="AT3317"
    call :buildManual FP-MQTT
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\FP-MQTT\latex\EC-Master-FP-MQTT.pdf" ..\EC-Master-FP-MQTT.pdf
    set ECMASTER_FP=
)

if "1" == "%INCLUDE_ECMASTER_RELEASE_NOTES%" (
    set ECMASTER_RELEASE_NOTES=1
    set ECMASTER_ATNUMBER="AT3300"
    call :buildManual ReleaseNotes
    if "1" == "%BUILD_PDF%" copy "%BUILDDIR%\ReleaseNotes\latex\EC-Master_ReleaseNotes.pdf" ..\EC-Master_ReleaseNotes.pdf
    set ECMASTER_RELEASE_NOTES=
)

goto :end

:buildManual
    set Name=%~1

    if "1" == "%BUILD_HTML%" (
        echo Generating EC-Master %Name% HTML User Manual...
        %SPHINXBUILD% -M html      "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_html_error.log" >"%BUILDDIR%\build_%Name%_html.log" 2>&1
        type "%BUILDDIR%\build_%Name%_html_error.log"
        echo Finished.
    )

    if "1" == "%BUILD_PDF%" (
        echo Generating EC-Master %Name% PDF User Manual...
        %SPHINXBUILD% -M latexpdf  "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -v -c "%CONFDIR%" -w "%BUILDDIR%\build_%Name%_pdf_error.log" >"%BUILDDIR%\build_%Name%_pdf.log" 2>&1
        type "%BUILDDIR%\build_%Name%_pdf_error.log"
        findstr /n /c:"! LaTeX Error:" "%BUILDDIR%\build_%Name%_pdf.log"
        echo Finished.
    )

    if "1" == "%BUILD_LIVE%" (
        echo Start EC-Master doc live generation
        START /B %SPHINXAUTOBUILD% "%SOURCEDIR%\%Name%" "%BUILDDIR%\%Name%" -N -c "%CONFDIR%" --port=0 --open-browser
    )
@goto :eof

:end
popd

