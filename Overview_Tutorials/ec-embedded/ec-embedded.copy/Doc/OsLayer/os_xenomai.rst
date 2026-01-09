..
    *******
    Xenomai
    *******

The system must be setup first the same way as for |Product| for Linux, especially installation of the atemsys module and Real-time Ethernet Driver usage preparation.

.. seealso:: Chapter :ref:`os_linux:Linux`

The binaries are built using the following versions:

- armv6-vfp-eabihf:
    - Xenomai 2.6.3, tested on Linux Kernel 3.8.13-xenomai-2.6.4
  
- x64:
    - Xenomai 3.0.2, tested on Linux Kernel 3.18.20 (Cobalt) 
    - EVL r0.44 (Xenomai 4), tested on Linux Kernel 5.15.106 
  
- x86:
    - Xenomai 2.6.2.1, tested on Linux Kernel 3.5.7
    - Xenomai 3.0.2, tested on Linux Kernel 3.18.20 (Cobalt) and 3.10.32-rt31 (Mercury)

.. only:: not EcSimulatorSiL

    Setting up and running |EcDemo|
    *******************************
    
    #. Prepare system
        Prepare the system to run |EcDemo| on Linux as described in chapter :ref:`os_linux:Linux`
    
    #. Compile |EcDemo|
        As a starting point there is the Eclipse project for |EcDemo| for Xenomai located at :file:`Workspace/Xenomai/`. 
        Ensure ``OPERATING_SYSTEM``, ``ARCH``, ``CFLAGS``, ``LDFLAGS``, ``LD_LIBRARY_PATH`` are set accordingly (export ARCH=x86, ...) when compiling using Eclipse!
        For Xenomai 4 the environment variable ELV_PATH should contain path of the libevl. Also ensure the following define is present:

        .. code-block::
        
            EC_VERSION_XENOMAI=4
    #. Run using GDB
        Provide search path for Xenomai libraries and prevent GDB to stop execution on SIGXCPU:
    
        .. prompt:: bash
            :substitutions:
    
            export LD_LIBRARY_PATH=../../Bin/Xenomai/x86:/usr/xenomai/lib:. 
            gdb --args ./|EcDemo| -intelgbe 2 1 -f eni.xml -v 3
            [...]
            (gdb) handle SIGXCPU nostop noprint nopass
            (gdb) run
            
    .. seealso:: :ref:`running-ecdemo`

OS compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for Xenomai.

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/Xenomai
        <InstallPath>/Examples/Common/Xenomai

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/Xenomai
        <InstallPath>/Sources/OsLayer/Xenomai

Extra library paths to the main EtherCAT components
    - Xenomai 2 and 3:
  
    .. code-block::

        <InstallPath>/SDK/LIB/Xenomai

    - Xenomai 4:

    .. code-block::

        <InstallPath>/SDK/LIB/Xenomai4


Extra libraries (in this order)
    - Xenomai 2:
    
    .. code-block::
        :substitutions:
    
        |EcLibraries| pthread dl rt native xenomai

    - Xenomai 3:
    
    .. code-block::
        :substitutions:
    
        |EcLibraries| pthread dl rt

``xeno-config --cflags`` and ``xeno-config --ldflags`` of the Xenomai installation return the needed ``CFLAGS`` and ``LDFLAGS``. If further information is needed, please refer to http://xenomai.org/ .
    - Xenomai 4:
    
    .. code-block::
        :substitutions:
    
        |EcLibraries| pthread evl dl
