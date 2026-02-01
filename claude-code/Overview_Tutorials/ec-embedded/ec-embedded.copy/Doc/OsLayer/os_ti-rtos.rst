..
    *******
    TI-RTOS
    *******

Setting up and running EcMasterDemo
***********************************

Prerequisites, basic settings: 
==============================

TI SDK RTOS v4.02 for AM335x/AM437x/AM57x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure your Code Composer Studio uses correct versions of SYS/BIOS, XDCtools and  PDK.
For TI SDK 4.02 corresponding versions are:

- XDCtools: 3.50.3_33_core
- PDK 1.0.9
- SYS/BIOS 6.52.0.12

Ensure environment variable PDK_INSTALL_PATH is pointing to the installed root directory of SDK.
Eg: For AM572x demo project, PDK_INSTALL_PATH=C:/ti/pdk_am57xx_1_0_9/packages

TI SDK RTOS for AM654x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At lease Version 9 of the Code Composer Studio is needed and together with the TI Processor SDK-rtos for am65xxevm Version 07.01.00.14 this lead to the packages:

- XDCtools: 3.61.3_29_core
- PDK 7.1.0.55
- SYS/BIOS 6.83.0.18

Ensure environment variable PDK_INSTALL_PATH is pointing to the installed root directory of SDK.
For AM654x demo project, PDK_INSTALL_PATH=C:/ti/pdk_am65xx_07_01_00_55/packages


How to create the demo applications
===================================

#. Create ENI file for EtherCAT configuration.
    xxd.exe is capable of converting ENI files to a C file as array, e.g. "xxd.exe -i eni.xml ENI.c". Replace MasterENI.c file with the generated one
#. On TI RTOS the EcMasterDemo can run with either an Real-time Ethernet Driver CPSW or ICSS.
    Eg: AM572x with Real-time Ethernet Driver ICSS
    
    Workspace/TI-RTOS_AM57x in Code Composer Studio and import all projects from this directory:
    
    - EcMaster
    - emllICSS
    - EcMasterDemoICSS or 
    - EcMasterDemoDcICSS

    Hardcoded parameters for the demo can be changed using DEMO_PARAMETERS definition. 
    
How to run the EC-Master demo applications
==========================================

-	The compiled .out application files of the demo can be uploaded to the device via JTAG debugger from Code Composer Studio Debugger.
-	The SD Card bootable demo binary is generated as an APP file from post build script calling pdkAppImageCreate.bat from the PSDK package.

How to run the EC-Master motion demo application
================================================

#. Create an appropriate ENI file as en EcMasterDemo with the xxd.exe tool
    The DC configuration has to be done appropriately, please see the EtherCAT general documentation and EC-Master manuals for details
#. Create an appropriate motion demo configuration file and copy it into the config directory of the project
    See example in Examples/EcMasterDemoMotion/Config/DemoConfig.xml
    See additional info in: Examples/EcMasterDemoMotion/readme.txt 
#. Convert DemoConfig.xml to C file DemoConfig.c  as array.  
#. Build the Project and download it to target Processor.
#. The demo logging is done over UART.

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

OS Compiler settings
********************

Besides the general settings from :ref:`gettingstarted:Compiling the EcMasterDemo` the following settings are necessary to build the example application for TI-RTOS.

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/TI-RTOS
        <InstallPath>/Examples/Common/TI-RTOS

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/TI-RTOS
        <InstallPath>/Sources/OsLayer/TI-RTOS

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>/SDK/LIB/TI-RTOS