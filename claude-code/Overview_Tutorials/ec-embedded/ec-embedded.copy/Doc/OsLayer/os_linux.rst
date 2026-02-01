..
    *****
    Linux
    *****

OS optimizations
****************

Linux itself is not real-time capable, so it is recommended to use it with the additional `PREEMPT_RT` patch.

The power management can disrupt cyclical processing, it is advisable to disable the :ref:`os_linux:CPUIDLE sub-system` and :ref:`os_linux:CPUFREQ sub-system`.
The sub-systems can be disabled by changing the kernel command line parameters in the boot loader. On x86, x86_64 systems this is usually `GRUB`, on embedded devices with ARM, ARM64 is usually `u-boot`. It is also possible to build a custom kernel without these sub-systems.

Running a |Product| application on a dedicated CPU core that is isolated from the Linux scheduler (:ref:`os_linux:ISOLCPUS`) can provide additional stability.

CPUIDLE sub-system
==================

Check if CPUFREQ sub-system is enabled:
    .. prompt:: bash
        
        ls /sys/devices/system/cpu/
    
If ``cpuidle`` appears in the list, it is enabled.

Disable CPUIDLE via the kernel command-line in GRUB:
    .. code-block::

        linux  /boot/vmlinuz-4.19.0-16-rt-amd64 cpuidle.off=1
    

CPUFREQ sub-system
==================

Check if CPUFREQ sub-system is enabled:
    .. prompt:: bash
        
        ls /sys/devices/system/cpu/
    
If ``cpufreq`` appears in the list, it is enabled.

Disable CPUFREQ sub-system via the kernel command-line GRUB:
    .. code-block::

        linux  /boot/vmlinuz-4.19.0-16-rt-amd64 cpufreq.off=1

If CPUFREQ is not to be deactivated, the governor should be set to ``performance``. 

The currently active governor can be determined as follows:
    .. prompt:: bash

        cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

The available governors with:
    .. prompt:: bash

        cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_governors

To change governor use:
    .. prompt:: bash
        
        echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

ISOLCPUS
========

Isolate CPU core number 4 of a quad-core processor via the kernel command-line GRUB:
    .. code-block::

        linux  /boot/vmlinuz-4.19.0-16-rt-amd64 isolcpus=3
        
``isolcpus`` alone removes scheduler tasks from selected CPUs, but does not prevent timer interrupts, RCU callbacks, or device IRQs. To fully isolate a CPU for real-time workloads, ``nohz_full``, ``rcu_nocbs``, and ``irqaffinity`` should be used together to eliminate kernel noise and ensure deterministic execution.

Enhanced isolation of CPU core 4  via the kernel command-line GRUB:
    .. code-block::

        linux  /boot/vmlinuz-4.19.0-16-rt-amd64 isolcpus=3 nohz_full=3 rcu_nocbs=3 rcu_nocb_poll irqaffinity=0-2

Running |EcDemo| on the isolated CPU core by setting the CPU affinity ``-a``:
    .. prompt:: bash
        :substitutions:

        ./|EcDemo| -a 3
        

atemsys kernel module
*********************

To use Real-time Ethernet Driver under Linux, the atemsys kernel module must be compiled and loaded. atemsys grants direct access to hardware to improve the performance.

All necessary scripts, source code and a detailed description of the installation can be found on https://github.com/acontis/atemsys. A ready-to-use Yocto recipe is also available on https://github.com/acontis/meta-acontis

.. figure:: ../../OsLayer/Media/ec-masterarchlinux.png
    :align:     center
    :alt:       

atemsys as Device Tree Ethernet Driver
======================================

atemsys can also be used as a device tree driver to avoid certain conflicts between the Real-time Ethernet Driver and the Linux kernel, e.g. power management, shared MDIO bus, etc..

A detailed guide on how to customize the device tree accordingly can also be found on https://github.com/acontis/atemsys. Example device tree modifications for different Real-time Ethernet Drivers/SoC can be found in https://github.com/acontis/atemsys/wiki.

.. note:: This is the preferred solution on all embedded devices with device tree support.

atemsys and PHY OS Driver
=========================

To use the PHY OS Driver, the acontis kernel module atemsys has to be included in the kernel device tree as an official driver for the Ethernet controller and doesn't required any additional configuration at the application level. 
As a result atemsys can interact with Linux drivers.

Unbind Ethernet Driver instance
*******************************

Ethernet Driver instances used by Real-time Ethernet Drivers may not be bound by kernel drivers modules!
Unbind can be done by unloading the kernel driver module, via the unbind interface of the driver or by modifying the device tree.


Unbind from kernel driver
=========================

The following command unbinds an instance without unloading the kernel driver module:

**PCI**

.. prompt:: bash

    echo "<Instance-ID>" > /sys/bus/pci/drivers/<driver-name>/unbind

Example:

.. prompt:: bash

    echo "0000:00:19.0" > /sys/bus/pci/drivers/e1000e/unbind

This call requires the PCI bus, device, function codes (in the above example it is 0000:00:19.0).
The codes can be found using Linux commands like, for example:

.. prompt:: bash

    ls /sys/bus/pci/drivers/e1000e

**SoC**

.. prompt:: bash

    echo "<Instance-ID>" > /sys/bus/platform/drivers/<driver-name>/unbind

Example:

.. prompt:: bash

    echo "2188000.ethernet" > /sys/bus/platform/drivers/fec/unbind

Unload kernel driver
====================

Not all drivers allow unbinding of network adapters. If unbinding is not supported the corresponding Linux kernel driver must not be loaded.

The following command lists the loaded kernel modules that may conflict with Real-time Ethernet Driver:

.. prompt:: bash

    lsmod | egrep "<module-name>"

Example:

.. prompt:: bash

    lsmod | egrep "e1000|e1000e|igb"

PCI/PCIe: The command `lspci -v` shows which driver is assigned to which network card, e.g.:

.. prompt:: bash

    lspci -v

.. code-block:: console

    ...
    11:0a.0 Ethernet controller: Intel Corporation 82541PI Gigabit Ethernet Controller (rev 05)
    ...
    Kernel driver in use: e1000e


Modules can be prevented from loading with the following commands:

.. prompt:: bash

    echo blacklist <module-name> | sudo tee -a /etc/modprobe.d/blacklist.conf
    update-initramfs -k all -u
    sudo reboot

The following table shows the  Kernel modules related to the Real-time Ethernet Driver:

+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Chip                                  | Real-time Ethernet Driver   | Kernel driver(s)                  | Remarks                           |
+=======================================+=============================+===================================+===================================+
| Broadcom Genet                        | emllBcmGenet                | genet                             | Unbind not supported              |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Beckhoff CCAT                         | emllCCAT                    | ec_bhf                            |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| CPSW                                  | emllCPSW                    | ti_cpsw                           |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Generic                               | emllDpdk                    |                                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| DesignWare 3504                       | emllDW3504                  | stmmac                            |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
|                                       | emllEG20T                   |                                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Freescale TSEC/eTSEC v1/2             | emllETSEC                   | gianfar_driver                    |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Freescale FEC and ENET controller     | emllFslFec                  | fec, fec_ptp                      |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Cadence GEM/MACB                      | emllGEM                     | gem, macb                         |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Intel Pro/1000                        | emllI8254x                  | igb, e1000, e1000e                |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Intel Pro/1000                        | emllIntelGbe                | igb, e1000, e1000e                |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Intel Pro/100                         | emllI8255x                  | e100                              |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| ICSS                                  | emllICSS                    | prueth,pruss                      | Unbind not supported              |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| RDC R6040                             | emllR6040                   |                                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Realtek RTL8139                       | emllRTL8139                 | 8139too, 8139cp                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Realtek RTL8169 / RTL8111 / RTL8168   | emllRTL8169                 | r8169                             | Unbind not supported              |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| SuperH                                | emllSHEth                   | sh_eth                            | Unbind not supported              |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Generic                               | emllSockRaw                 |                                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+
| Generic                               | emllSockXdp                 |                                   |                                   |
+---------------------------------------+-----------------------------+-----------------------------------+-----------------------------------+

Docker
******

It is possible to operate |Product| within a Docker container with realtime priority. The atemsys kernel module should be installed on the host in order to operate the container with the lowest possible capabilities and privileges.

The following additional settings, permissions for ``docker run`` are required:

Add atemsys device to container
    .. code-block::
    
        --device=/dev/atemsys:/dev/atemsys
Allow max realtime priority
    .. code-block::
    
        --ulimit rtprio=99
Add capability to set priority an lock memory
    .. code-block::
    
        --cap-add=sys_nice
        --cap-add=ipc_lock
Publish RAS server port `6000`
    .. code-block::    
        
        -p 6000:6000

.. only:: not EcSimulatorSiL

    Setting up and running |EcDemo|
    *******************************

    #. Unbind Ethernet Driver instance, e.g.

       .. prompt:: bash

           echo 0000:00:19.0 > /sys/bus/pci/drivers/e1000e/unbind

    #. Load atemsys kernel module

       .. prompt:: bash

           insmod atemsys.ko

    #. Copy files from |Product| package :file:`/bin` and a :file:`eni.xml` to directory e.g. :file:`/tmp`.
    #. Adjust `LD_LIBRARY_PATH` search locations for Real-time Ethernet Driver if necessary, e.g.

       .. prompt:: bash

           export LD_LIBRARY_PATH=/tmp:$LD_LIBRARY_PATH

    #. Run |EcDemo|

       .. prompt:: bash
            :substitutions:

            cd /tmp
            ./|EcDemo| -intelgbe 1 1 -f eni.xml -perf

    .. seealso:: :ref:`running-ecdemo`

    Run in Docker container
    =======================

    #. Unbind Ethernet Driver instance and load atemsys on the host.
    #. Create a directory on the host (e.g. :file:`~/docker`) and copy files from |Product| package :file:`/bin` and :file:`exi.xml` into this directory.
    #. Start bash console in container
        .. prompt:: bash

            sudo docker run -it \
                --name atem_container \
                --device=/dev/atemsys:/dev/atemsys \
                --ulimit rtprio=99 \
                --cap-add=sys_nice --cap-add=ipc_lock \
                -v ~/docker:/home/docker \
                -p 6000:6000 \
                ubuntu bash

        **Command line arguments:**

        - ``-it`` Allocate a pseudo-TTY and run container
        - ``--name atem_container`` Container name
        - ``--device=/dev/atemsys:/dev/atemsys`` Add `atemsys` device to container
        - ``--ulimit rtprio=99`` Allow max realtime priority
        - ``--cap-add=sys_nice`` Add Linux capability to set priority
        - ``--cap-add=ipc_lock`` Add Linux capability to lock memory
        - ``-v ~/docker:/home/docker`` Mount previously create directory to container
        - ``-p 6000:6000`` Publish RAS server port `6000`
        - ``ubuntu bash`` Use Docker image ubuntu and start bash
    #. Run |EcDemo| in container

       .. prompt:: text #
            :substitutions:

            cd /home/docker
            export LD_LIBRARY_PATH=.
            ./|EcDemo| -intelgbe 2 1 -f eni.xml -perf


OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for Linux

Possible ARCHs (see ATECAT_ARCHSTR in :file:`SDK/INC/Linux/EcOsPlatform.h`):
    - aarch64 (ARM 64Bit)
    - armv4t-eabi (ARM 32Bit)
    - armv6-vfp-eabihf (ARM 32Bit)
    - armv7-vfp-eabihf (ARM 32Bit)
    - PPC (PPC 32Bit with "-te500v2")
    - riscv64 (RISC-V 64Bit)
    - x64 (x86 64Bit)
    - x86 (x86 32Bit)

    The ARM 32Bit architectures `armv4t-eabi` and `armv6-vfp-eabihf/armv7-vfp-eabihf` are incompatible with each other. An ARM VFP system returns success on 
        .. prompt:: bash
    
            readelf -A /proc/self/exe | grep Tag_ABI_VFP_args

Extra include paths
    .. code-block::
    
        <InstallPath>/Examples/Common/Linux
        <InstallPath>/SDK/INC/Linux 

Extra source paths
    .. code-block::
        
        <InstallPath>/Examples/Common/Linux
        <InstallPath>/Sources/OsLayer/Linux

Extra library paths to the main EtherCAT components
    .. code-block::
    
        <InstallPath>/SDK/LIB/Linux/<Arch>

Extra libraries (in this order)
    .. code-block::
        :substitutions:

        |EcLibraries| pthread dl rt

Build using cmake on Linux
**************************

Example usage to build Linux x64 Debug with cmake:

.. prompt:: bash

    cmake -DEC_OS=Linux -DEC_ARCH=x64
    cmake --build .

Cross-platform development under Windows
****************************************

The following steps describe how to develop 
Linux cross-platform developing on Windows for Linux , you can follow :

``-DEC_OS=Windows -DEC_ARCH=x64``

#. **Install MinGW**
    - Download the latest version of MinGW from the MinGW official website https://osdn.net/projects/mingw/ 
    - Install the mingw-get-setup.exe tool to C:\\MinGW 
    - Select the ''Basic Setup''
    - Apply changes

#. **Install a cross platform toolchain**
    - Download a cross-platform toolchain from e.g. the Linaro release storage server https://releases.linaro.org/components/toolchain/gcc-linaro/
    - Unpack it to C:\\MinGW\\opt

#. **Build using cmake on Linux**

   Example usage to build for Linux x64 Debug on Windows with cmake and ninja:
   
   .. prompt:: bash

       cmake -DEC_OS=Linux -DEC_ARCH=x64 -DCMAKE_BUILD_TYPE=Debug .
       cmake --build .


#. **Build for LxWin using cmake on Linux**

   Example usage to build EcMasterDemo for Linux x64 Debug on Windows with cmake and ninja:
   
   .. prompt:: text Workspace/LxWin/cmake/x64/Debug>
   
       cmake.exe -G Ninja ../../../../.. -DCMAKE_TOOLCHAIN_FILE=../../../../Linux/Toolchain.cmake -DEC_OS=LxWin -DEC_ARCH=x64 -DCMAKE_BUILD_TYPE=Debug
       ninja.exe EcMasterDemo

#. **Cross build using cmake for Linux on Windows**

   Example usage to build EcMasterDemo for Linux x64 Debug on Windows with cmake and ninja:
   
   .. prompt:: text Workspace/Linux/cmake/x64/Debug>
   
       cmake.exe -G Ninja ../../../../.. -DCMAKE_TOOLCHAIN_FILE=../../../Toolchain.cmake -DEC_OS=Linux -DEC_ARCH=x64 -DCMAKE_BUILD_TYPE=Debug
       ninja.exe EcMasterDemo
    
#. **Cross build using Eclipse CDT on Windows**
    - Download and install the latest version of Eclipse CDT from the Eclipse official website https://projects.eclipse.org/projects/tools.cdt
    - Create a start batch file for eclipse
    
    .. code-block:: batch

        set PATH=C:\MinGW\bin;C:\MinGW\msys\1.0\bin;%LINUX_CROSS_GCC_ARM_PATH%;%PATH%
        set LINUX_CROSS_GCC_ARM_PATH=C:\MinGW\opt\gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu\bin
        set CFLAGS=-IC:\MinGW\opt\gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu\aarch64-linux-gnu\libc\usr\include
        set CROSS_COMPILE=aarch64-linux-gnu-
        set ARCH=aarch64
        eclipse.exe
