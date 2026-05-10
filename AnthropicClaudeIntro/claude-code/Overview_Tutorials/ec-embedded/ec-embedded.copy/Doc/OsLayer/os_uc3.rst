..
    ********************
    µC3 for STM32
    ********************

Setting up and running EcMasterDemo in IAR for ARM IDE
*******************************************************

#. Prerequisites
    - IAR for ARM IDE, v9.32
    - µC3/Compact
    - STM32H743 target
    - EtherCAT devices

#. Connect the STM32H743 target to the PC.
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

#. Start IAR for ARM IDE and set the EcMasterDemo_STM32H743.
#. If needed, change debug project settings.
#. Build and run EcMasterDemo.

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

OS Compiler settings
********************

Besides the general settings from :ref:`gettingstarted:Compiling the EcMasterDemo` the following settings are necessary to build the example application for µC3 (STM32).

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/uC3
        <InstallPath>/Examples/Common/uC3

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/uC3

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>/SDK/LIB/uC3/M7-EWARM

Extra libraries
    .. code-block::

        EcMaster.a
        emllCmsisEth.a


********************
µC3 for i.MX8
********************

Setting up and running EcMasterDemo on NXP 8MPLUSLPD4-EVK board
***************************************************************

#. Prerequisites
    - GCC compiler for aarch64 9.2.1
    - GNU make 4.4.1
    - µC3/Standard for Cortex-A53 MPcore i.MX8M Plus GCC
    - NXP 8MPLUSLPD4-EVK board
    - EtherCAT devices

#. Install GCC toolchain from https://developer.arm.com/downloads/-/gnu-a/9-2-2019-12
#. Install make from https://xpack-dev-tools.github.io/
#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 
        .. prompt:: batch
        
            xxd.exe -i eni.xml MasterENI.c

    Replace :file:`Workspace\\uC3_iMX8\\EcMasterDemo_8MPLUSPD4-EVK\\ENI\\MasterENI.c` file with generated one. File should be manually modified to look like:

    .. code-block:: c

        unsigned char MasterENI_xml_data[] = {
        ...
        };
        unsigned int MasterENI_xml_data_size = ???;


#. Build EcMasterDemo
    .. code-block:: batch

        cd Workspace\uC3_iMX8\EcMasterDemo\
        make

#. Build EcMasterDemo_8MPLUSPD4-EVK
    .. code-block:: batch

        cd Workspace\uC3_iMX8\EcMasterDemo_8MPLUSPD4-EVK\
        make

#. Connect the target board to the PC. The J23 'DEBUG' connector is user for serial output, connect it to PC and use your terminal software of choice in order to display EcMasterDemo output. The following connection settings will be used:
    - Baude rate:   115200
    - Data:         8 bits
    - Parity:       none
    - Stop:         1 bit
    - Flow control: none

#. Connect EtherCAT devices to the board, use "ENET1" connector.
#. Prepare an u-boot SD card and copy :file:`Workspace\\uC3_iMX8\\EcMasterDemo_8MPLUSPD4-EVK\\aarch64\\EcMasterDemo_8PLUSPD4-EVK.bin` on it.
#. Boot from SD card into u-boot, interrupt booting process if needed:
    .. prompt::

        ...
        Fastboot: Normal
        Normal Boot
        Hit any key to stop autoboot:  2
        u-boot=>

#. Load the binary to RAM:
    .. prompt::

        u-boot=>fatload mmc ${mmcdev}:1 0x95000000 EcMasterDemo_8PLUSPD4-EVK.bin

#. Start EcMasterDemo:
    .. prompt::

        u-boot=>go 0x95000000

**********************
µC3 for Renesas RZ/N2H
**********************

Setting up and running EcMasterDemo for RZ/N2H
***************************************************************

#. Prerequisites
    - Renesas e2studio 2024-10
    - RZ/N2H board
    - Segger J-Link
    - EtherCAT devices

#. Set environment variables to point to µC3 kernel and driver folders, i.e.

    .. code-block:: batch

        set UC3_KERNEL_LOC=C:\uC3_RZN2H\Kernel\Standard
        set UC3_DRIVER_LOC=C:\uC3_RZN2H\Driver\Standard

#. Install and run e2studio, please select support of RZ family as optinal feature.
#. Create a new workspace and import EcMasterDemo project from :file:`\Workspace\uC3_RZN2H_e2studio`
#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 
        .. prompt:: batch
        
            xxd.exe -i eni.xml MasterENI.c

    Replace :file:`Workspace\\uC3_RZN2H_e2studio\\EcMasterDemo_xxx\\ENI\\MasterENI.c` file with generated one.
    This file should be manually modified for EcMasterDemo_xxx_SRAM to look like:

    .. code-block:: c

        const unsigned char MasterENI_xml_data[] = {
        ...
        };
        const unsigned int MasterENI_xml_data_size = ???;


    This file should be manually modified for EcMasterDemo_xxx_DDR to look like:

    .. code-block:: c

        const unsigned char MasterENI_xml_data[] __attribute__((section(".eni_file"))) = {
        ...
        };
        const unsigned int MasterENI_xml_data_size __attribute__((section(".eni_file"))) = ???;

#. Build EcMasterDemo projects and debug it as "Renesas GDB Hardware Debugging" using "J-Link ARM" as debugging hardware and "R9A09G087M44_CA55_0" as target device.



