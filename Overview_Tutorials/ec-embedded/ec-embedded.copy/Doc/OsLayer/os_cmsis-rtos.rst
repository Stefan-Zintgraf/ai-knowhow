..
    ********************
    CMSIS-RTOS for STM32
    ********************

Setting up and running EcMasterDemo in Keil µVision IDE
*******************************************************

#. Prerequisites
    - Keil µVision 5 IDE
    - STM32H747I-DISCO board
    - EtherCAT devices

#. Connect the STM32H747I-DISCO development board to the PC according to user manual.
#. Connect EtherCAT devices to the board.
#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 
        .. prompt:: batch
        
            xxd.exe -i eni.xml ENI.c

    Replace ENI.c file with generated one. File should be manually modified to look like:

    .. code-block:: c

        unsigned char MasterENI_xml_data[] = {
        ...
        };
        unsigned int MasterENI_xml_data_size = ???;

#. Start Keil µVision IDE and set the EcMasterDemoApp project as active.
#. If needed, change debug project settings.
#. Build and run EcMasterDemoApp.

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

OS Compiler settings
********************

Besides the general settings from :ref:`gettingstarted:Compiling the EcMasterDemo` the following settings are necessary to build the example application for CMSIS-RTOS (STM32).

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/CMSIS-RTOS
        <InstallPath>/Examples/Common/CMSIS-RTOS_STM32

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/CMSIS-RTOS
        <InstallPath>/Sources/OsLayer/CMSIS-RTOS

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>/SDK/LIB/CMSIS-RTOS/mdk-arm

Extra libraries
    .. code-block::

        EcMaster.lib
        emllCmsisEth.lib
        EcMasterDemo.lib

Setting up and running EcMasterDemo in STM32CubeIDE for STM32H747I-DISCO
************************************************************************

#. Prerequisites
    - STM32CubeIDE V1.5.0
    - EC-Master V3.1
    - *CMSIS-RTOS* sources package. Use git https://github.com/ARM-software/CMSIS_5.git or download from https://github.com/ARM-software/CMSIS_5/archive/develop.zip.
        .. note:: Alternative *ARM CMSIS Drivers for external devices* contains *CMSIS-RTOS* sources as well.

    - *ARM CMSIS Drivers for external devices* from https://www.keil.com/dd2/pack/ (for CMSIS PHY driver sources)
    - *STMicroelectronics STM32H7 Series Device Support and Examples* from https://www.keil.com/dd2/pack/ (for CMSIS MAC driver sources)

#. Environment variables
    In order to be able to build and run demo application the following environment variables (either system or project variables) has to be defined:

    - **CMSIS_LOC**, has to be set to the CMSIS package location, i.e. :file:`C:/CMSIS_5-5.7.0`
    - **FW_LOC**, points to the firmware folder in STM32Cube repository, i.e. :file:`<PATH_TO_STM32CUBE_REPOSITORY>/STM32Cube_FW_H7_V1.8.0`
    - **PATH** variable must contain the following paths (needed for tool chain):
        .. code-block::
        
            C:/ST/STM32CubeIDE_1.5.0/STM32CubeIDE/plugins/com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.7-2018-q2-update.win32_1.5.0.202011040924/tools/bin
            C:/ST/STM32CubeIDE_1.5.0/STM32CubeIDE/plugins/com.st.stm32cube.ide.mcu.externaltools.make.win32_1.5.0.202011040924/tools/bin
        
    - **PACKS_LOC**, points to the packs location, where *ARM CMSIS Drivers for external devices* and *STMicroelectronics STM32H7 Series Device Support and Examples* were installed, i.e. :file:`C:/Users/<USER_NAME>/AppData/Local/Arm/Packs`

#. Build EcMasterDemo
    - Build the EcMasterDemo project
    - Create EtherCAT network configuration
    - Build the EcMasterDemo_STM32H747I-DISCO project for CM7 CPU
#. Run on a STM32H747I-DISCO board
    - Connect the board to PC using CN2 connector. This connection will be used for powering the board and for debugging as well.
    - Connect EtherCAT cable to the Ethernet interface on the board and the EtherCAT slave(s).
    - Power on EtherCAT slave(s).
    - Using your favorite terminal application (i.e. Teraterm) connect to the serial port of STM32H747I-DISCO. Usually it is called *STMicroelectronics STLink Virtual COM Port*. Ensure it has the following settings: ``115200,8,N,1``.
    - Create a debug or run configuration, select *STM32 Cortex-M C/C++ Application* as template. For this configuration select *SWD* in *GDB Server Command Line Options*.

    .. note:: in order to let the application run with different command line parameter please change ``szCommandLine`` declared in :file:`app_main.c`        
