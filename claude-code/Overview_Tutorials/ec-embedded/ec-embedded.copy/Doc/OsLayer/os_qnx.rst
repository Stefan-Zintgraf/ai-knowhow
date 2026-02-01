..
    ************
    QNX Neutrino
    ************

Thread priority
***************

QNX supports a total of 256 scheduling priority levels. A non-root thread can set its priority to a level from 1 to 63 (the highest priority).

Using priorities higher than 63 is only possible if  the allowed priority range is changed for non-root processes: 

.. prompt:: bash

    procnto -P priority
    
For more information's about changing the priority range refer to the QNX documentation.

.. attention:: Don't changing the priority range leads to bad timing performance!

Unbind Ethernet Driver instance
*******************************

The network interface must be unloaded if it is used by an operating system driver. Depending on the QNX version, a corresponding command must be executed in the QNX Shell or the QNX Build Script. 

QNX >= 6.5    
    .. prompt::
    
        ifconfig en1 destroy

QNX >= 7.1
    .. prompt::
    
        umount /dev/io-sock/devs-em.so/em1

IOMMU/SMMU support
******************

For systems that have to use an IOMMU/SMMU for security reasons, it is possible to create predefined typed memory region that is used by the Real-time Ethernet Driver. The definition has to be done in the QNX BSP build file and the name must match following pattern:

**smm_** *LinkLayerName* **-** *InstanceNumber(32Bit Hex)*

Example: Real-time Ethernet Driver emllIntelGbe with instance number 1
    .. code::

        smm_emllIntelGbe-0x00000001

A separate typed memory region must be defined for each Real-time Ethernet Driver instance. The typed memory is automatically used by the Real-time Ethernet Driver if it matches the pattern, otherwise the default memory is used.

.. only:: not EcSimulatorSiL

    Setting up and running |EcDemo|
    *******************************

    #. QNX Neutrino OS configuration

       In order to get real-time priority (e.g. 250), see :ref:`os_qnx:Thread priority` and also set JOBS_PRIORITY. The applications needs root privileges to increase the priority above 63.

    #. Unbind Ethernet Driver instance, e.g.
   
       .. prompt:: bash

            ifconfig en1 destroy

    #. Copy files from |Product| package :file:`/bin` and :file:`eni.xml` to directory, e.g. :file:`/tmp`.
    #. Adjust `LD_LIBRARY_PATH` search locations for Real-time Ethernet Driver if necessary, e.g.
 
       .. prompt:: bash

            export LD_LIBRARY_PATH=/tmp:$LD_LIBRARY_PATH

    #. Run |EcDemo|
   
       .. prompt:: bash
            :substitutions:

            cd /tmp
            ./|EcDemo| -intelgbe 1 1 -f eni.xml -perf

    .. seealso:: :ref:`running-ecdemo`

OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for QNX Neutrino.

Extra include paths
    .. code-block::
    
        <InstallPath>/SDK/INC/QNX 
        <InstallPath>/Examples/Common/QNX

Extra source paths
    .. code-block::
        
        <InstallPath>/Examples/Common/QNX
        <InstallPath>/Sources/OsLayer/QNX

Extra library paths to the main EtherCAT components
    .. code-block::
    
        <InstallPath>/SDK/LIB/QNX/<Arch>

Extra libraries (in this order)
    .. code-block::
        :substitutions:
        
        |EcLibraries| socket

