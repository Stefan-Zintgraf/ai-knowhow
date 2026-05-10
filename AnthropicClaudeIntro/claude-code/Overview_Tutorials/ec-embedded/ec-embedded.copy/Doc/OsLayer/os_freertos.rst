..
    ********
    FreeRTOS
    ********

Setting up and running EcMasterDemo on Xilinx Zynq UltraScale+ (ZCU104) and Xilinx Zynq-7000 (ZC702 Evaluation Kit)
*******************************************************************************************************************

Install Xilinx SDK 2018.2
or
Install Xilinx Vitis IDE 2022.2

How to create the demo applications for Xilinx Zynq
===================================================

#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 

    .. prompt::
    
        xxd.exe -i eni.xml ENI.c

    Replace ENI.c file with generated one.
#. Create a BSP project
    Based on the delivered hardware project, replace the settings file with the one from the package:

for Xilinx SDK

    .. code-block::

        setws .
        importprojects .
        
        createbsp -name ZCU104_bsp_cortexa53 -hwproject ZCU104_hw_platform -proc psu_cortexa53_0 -arch 64 -os freertos10_xilinx
        createbsp -name ZCU104_bsp_cortexr5 -hwproject ZCU104_hw_platform -proc psu_cortexr5_0  -os freertos10_xilinx
        createbsp -name ZC702Rev_bsp -hwproject ZC702Rev_hw_platform -proc ps7_cortexa9_0  -os freertos10_xilinx
        createbsp -name ZedBoard_bsp -hwproject ZedBoard_hw_platform -proc ps7_cortexa9_0  -os freertos10_xilinx
        createbsp -name ZC701ZynqDimm_bsp -hwproject ZC701ZynqDimm_hw_platform -proc ps7_cortexa9_0  -os freertos10_xilinx

replace:
    .. code-block::

        ../<BSP name>/<core name>/libsrc/freertos10_xilinx_v1_1/src/FreeRTOSConfig.h  

for Vitis IDE

    .. code-block::

        set PATH=C:\Xilinx\Vitis\2022.2\bin;%PATH%
        set BUILD_SEVENZIP="C:\Program Files\7-Zip\7z.exe"
        
        @echo "Build with Xilinx Software Commandline Tool (XSCT)"
        
        REM Create Xilinx BSP's
        @echo "Create Xilinx BSP's"
        pushd %BUILDOUTPUT%\Workspace\FreeRTOS_Zynq_Vitis\
        call xsct.bat  ZCU104\platform.tcl
        call xsct.bat  ZCU106\platform.tcl
        call xsct.bat  Kria_KR260\platform.tcl
        call xsct.bat  zc702\platform.tcl

replace:
    .. code-block::

        ../<BSP name>/psu_cortexr5_0/FreeRtos32BitR5/bsp/psu_cortexr5_0/libsrc/freertos10_xilinx_v1_12/src/FreeRTOSConfig.h


    For the new BSP project, just use the same BSP name and core as in the package.


How to run the EC-Master demo applications on Xilinx Zynq
=========================================================

Via USB debugger
    Load the application with :menuselection:`Debug Configuration --> Xilinix C/C++ application (System Debugger)` to the chosen core.
Via SD card
    By creating a :file:`BOOT.bin` file, e.g.:
    
for Xilinx SDK
    .. prompt:: 

        bootgen -w on -image ../EcMasterDemo_ZCU104_cortexa53.bif -arch zynqmp -o BOOT.bin

Maybe adjust the boot setting switches on the board


Setting up and running EcMasterDemo on TI AM64x EVM for R5 Core
***************************************************************

Install MCU-PLUS-SDK-AM64X 08.01.00.36 and Code Composer Studio 11.1 or newer.
Or  MCU-PLUS-SDK-AM64X 11.00.00.15 and Code Composer Studio 12.8 or newer.

How to create the demo applications on TI AM64x
===============================================

#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 

    .. prompt::
    
        xxd.exe -i eni.xml ENI.c

    Replace ENI.c file with generated one.
#. rebuild BSP for the correct performance measurement
    Change: 
    ti/mcu_plus_sdk_am64x_08_01_00_36/source/kernel/freertos/config/am64x/r5f/FreeRTOSConfig.h

    .. code-block::

        #define configUSE_IDLE_HOOK (0)

    or:

    ti/mcu_plus_sdk_am64x_08_01_00_36/source/kernel/freertos/portable/TI_ARM_CLANG/ARM_CR5F/port.c

    In ``vApplicationIdleHook()`` replace ``“wfi”`` with ``“nop”``.


How to run the EC-Master demo applications on TI AM64x
======================================================

#. Run via Debugger
    Follow getting started guide to flash the UART loader into the internal memory.
    Load the application with :menuselection:`Debug Configuration --> Code ComposerStudio - Device Debugging` and the Target Configuration to the R5F_0 core.

#. Run via µSD card
    Adjust and rebuild sbl_sd boot example in the mcu_plus_sdk.
    in main.c replace 

.. code-block::

    #define BOOTLOADER_APPIMAGE_MAX_FILE_SIZE (0x60000) /* Size of section MSRAM_2 specified in linker.cmd */
    uint8_t gAppImageBuf[BOOTLOADER_APPIMAGE_MAX_FILE_SIZE] __attribute__((aligned(128), section(".bss.filebuf")));

with

.. code-block::

    #define BOOTLOADER_APPIMAGE_MAX_FILE_SIZE (0x800000) /* This has to match the size of DDR section in linker.cmd */
    uint8_t gAppImageBuf[BOOTLOADER_APPIMAGE_MAX_FILE_SIZE] __attribute__((aligned(128), section(".bss.filebuf")));


Setting up and running EcMasterDemo on TI AM243x LP and TI AM243x  EVM
**********************************************************************

Install MCU-PLUS-SDK-AM243X 08.01.00.36 and Code Composer Studio 11.2 or newer.
Or MCU-PLUS-SDK-AM243X 11.00.00.15 and Code Composer Studio 12.8 or newer.

How to create the demo applications for TI AM243x
=================================================

#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 

    .. prompt::
    
        xxd.exe -i eni.xml ENI.c

    Replace ENI.c file with generated one.
#. rebuild BSP for the correct performance measurement
    Change: 
    ti/mcu_plus_sdk_am243x_08_01_00_36/source/kernel/freertos/config/am243x/r5f/FreeRTOSConfig.h

    .. code-block::

        #define configUSE_IDLE_HOOK (0)

    or:

    ti/mcu_plus_sdk_am243x_08_01_00_36/source/kernel/freertos/portable/TI_ARM_CLANG/ARM_CR5F/port.c

    ``vApplicationIdleHook()`` replace ``“wfi”`` with ``“nop”``


How to run the EC-Master demo applications on TI AM243x
=======================================================

#. Run via Debugger
    See TI AM64x

Handling Silicon Revision 2 with MCU-PLUS-SDK-AM243X 08.01.00.36 
================================================================

#. Uart
    If UART doesn't match the Baudrate of 115200 correct the Uart0 Clock Frequency from 96000000 to 48000000.

#. SD card boot
    The silicon revision 2 has additional security features. The SD card has to be created with a later MCU-PLUS-SDK-AM243X version.
    Also the Appimage has to created with a later SDK. So install mcu_plus_sdk_am243x_09_01_00_41 and use Workspace/FreeRTOS_AM243x/EcMasterDemo_am243x-evm/appimage_09_01_00_41.bat.



Setting up and running EcMasterDemo on TI J784s4 EVM for R5 Core
****************************************************************

Support for TiEnetCpswg on J784s4 is currently limited to TI J784S4X EVM with FreeRTOS in polling mode.
It's working with ti-processor-sdk-rtos-j784s4-evm-08_06_01_03.

Install PROCESSOR-SDK-RTOS-J784S4 Version: 08.06.01.03 and Code Composer Studio 11.2 or newer

How to create the demo applications on TI J784s4
================================================

#. Create ENI file for EtherCAT configuration.
    See TI AM64x

#. Adjust FreeRTOSConfig.h
    See ``…/ti-processor-sdk-rtos-j784s4-evm-08_06_01_03/pdk_j784s4_08_06_01_03/packages/ti/kernel/freertos/config/j784s4/r5f/FreeRTOSConfig.h``

    Turn off ``configUSE_IDLE_HOOK``, else vApplicationIdleHook() is called with ``asm("WFI");`` is used. With ``WFI`` the ARM ccnt counter sleep and the performance measurement fails (``WFI`` could also be replaced by ``NOP``).

    Heap size is not set with ``configTOTAL_HEAP_SIZE`` it’s configured in the linker script ``linker_r5_freertos.lds``

How to run the EC-Master demo applications on TI J784s4
=======================================================

#. Run via Debugger
    See TI AM64x

#. Run via µSD card
    See sbl_mmcsd example