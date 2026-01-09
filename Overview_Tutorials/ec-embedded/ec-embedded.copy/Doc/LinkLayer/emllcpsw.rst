The parameters to the Real-time Ethernet Driver CPSW are setup-specific. 
The function :cpp:func:`CreateLinkParmsFromCmdLineCPSW` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_CPSW
    :members:

.. doxygenenum:: EC_T_CPSW_TYPE 

CPSW usage under Linux
**********************

Due to lacking unbind-feature of the CPSW driver, the target's Kernel must not load the CPSW driver when starting. If the CPSW was built as a module, it can be renamed or removed to ensure, it never gets loaded. If it was compiled into the Kernel, the Kernel needs to be recompiled without it.

It is possible to use one CPSW port for Linux kernel (TCP/IP) and another CPSW port for |Product|. To do this, the CPSW kernel driver must be patched.

Currently following Linux versions are supported:

- linux-4.1.6 from TI Linux SDK 2.0
- linux-4.4.4-rt11 from Lenze
- linux-3.10.93-rt101 from Canon

.. note :: A patch for other Linux versions can also be created on request.
	
The patch needs:

- Linux kernel with enabled CPSW driver.
- Patch applied to Linux kernel.
- EC_ETHERNET_PORT defined according to target in cpsw.c and davinci_mdio.c files.
- Kernel must be rebuilt and installed

After that Linux will have only 1 Ethernet device, another can be used by |Product|. 

.. note:: EtherCAT ports should be used as "slave" since "master" is the Linux driver.
