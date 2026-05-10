*************************
Real-time Ethernet Driver
*************************

The EtherCAT master stack currently supports a variety of different Real-time Ethernet Driver modules, each of which contained in a single library file, which is loaded by the core library dynamically. The EtherCAT master stack shipment consist of a master core library (e.g. EcMaster.dll for Windows, libEcMaster.a for Linux) and one (or more) libraries each containing support for one specific Real-time Ethernet Driver module.
Which library actually is loaded, is depending on the Real-time Ethernet Driver parameters at runtime. 

Real-time means operating directly on the network device's register set instead of using the operating system's native driver.

The principle of the Real-time Ethernet Driver selection is that the Real-time Ethernet Driver name (Real-time Ethernet Driver identification) is used to determine the location and name of a registration function called by the EtherCAT master and registers function pointers that allow access to the Real-time Ethernet Driver functional entries.

The EtherCAT Real-time Ethernet Driver will be initialized using a Real-time Ethernet Driver specific configuration parameter set.
A pointer to this parameter set is part of the master's initialization settings when calling the function :cpp:func:`emInitMaster`

The EtherCAT master supports two Real-time Ethernet Driver operating modes. 
If the Real-time Ethernet Driver operates in interrupt mode all received Ethernet frames will be processed immediately in the context of the Real-time Ethernet Driver receiver task.
When using the polling mode the EtherCAT master will call the Real-time Ethernet Driver receiver polling function prior to processing received frames.


**Real-time Ethernet Driver and PHY OS Driver**

Some operating systems, e.g. Linux and Xenomai, provide drivers for most common Ethernet controllers and their related physical transceivers (PHY).
The manufacturer specific PHY circuits can be handled by a dedicated driver.
Using the PHY OS Driver interface it is possible to use the manufacturer's dedicated PHY driver without modification of the acontis optimized Real-time Ethernet Driver.
Depending on the hardware architecture, an additional module from acontis, e.g. atemsys for Linux, grants access to the MDIO bus to the OS drivers, or request MDIO operations from the OS drivers.

.. figure:: ../Media/emll_phy_os_driver_architecture.png
    :align:     center
    :alt:       

.. note:: Real-time Ethernet Driver modules not listed here may be available if purchased additionally. Not all Real-time Ethernet Driver modules support interrupt mode. 

.. toctree::
    :hidden:

    emll_init.rst
    
    emllbcmgenet.rst
    emllbcmnetxtreme.rst
    emllbpf.rst
    emllccat.rst
    emllcmsiseth.rst
    emllcpsw.rst
    emllcpswg.rst
    emlldpdk.rst
    emlldw3504.rst
    emlletsec.rst
    emllfslfec.rst
    emllgem.rst
    emllhpe.rst
    emlli8255x.rst
    emllicss.rst
    emllicssg.rst
    emllintelgbe.rst
    emlllan743x.rst
    emllmultiplier.rst
    emllndis.rst
    emllpcap.rst
    emllr6040.rst
    emllremote.rst
    emllrtl8169.rst
    emllrzt1.rst
    emllsheth.rst
    emllsnarf.rst
    emllsockraw.rst
    emllsockxdp.rst
    emlltemac.rst
    emlltienetcpswg.rst
    emlltieneticssg.rst
    emllvlan.rst
