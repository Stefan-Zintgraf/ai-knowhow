..
    *****************
    Windriver VxWorks
    *****************

Real-time Ethernet Driver for VxWorks are available. 
If none of the Real-time Ethernet Driver can be used, the SNARF Ethernet Driver must be selected.

The identification of the Real-time Ethernet Driver is done like this:

.. figure:: ../../OsLayer/Media/Identification_LL2.png
    :align:     center
    :alt:   

VxWorks native
**************

The BSP has to be prepared to support Real-time Ethernet Driver:

#. To use a Real-time Ethernet Driver the adapter memory has to be mapped into VxWorks memory space (VxWorks 5.x only). I.e. for the Intel Pro/100 Ethernet Driver this can be achieved by setting the INCLUDE_FEI_END macro in the BSP configuration file config.h.
#. To avoid conflicts with the VxWorks network driver which normally will be loaded when INCLUDE_FEI_END is set the file configNet.h has to be adjusted in a way that the network driver is not loaded. The network driver entry has to be removed from the endDevTbl[]:

.. code-block:: text

    END_TBL_ENTRY endDevTbl [] =
        {
        :	:	:
        :	:	:
        :	:	:
    /*
    #ifdef INCLUDE_FEI_END
        {0, FEI82557_LOAD_FUNC, FEI82557_LOAD_STRING, FEI82557_BUFF_LOAN,
        NULL, FALSE},
    #endif /* INCLUDE_FEI_END */
    */
        :	:	:
        :	:	:

.. warning:: Do not call :cpp:func:`muxDevUnload` for a device managed by a VxBus driver. VxBus drivers expect to call :cpp:func:`muxDevUnload` themselves in their {vxbDrvUnlink}( ) methods, and instability may result if :cpp:func:`muxDevUnload` is called for a VxBus network device instance by other code. 

.. seealso:: The VxWorks Device Driver Developer's Guide for more information about unloading VxBus network devices

SNARF Ethernet Driver
*********************

The SNARF Ethernet Driver is only needed if none of the Real-time Ethernet Driver can be used. The appropriate network adapter drivers have to be added to the VxWorks image.

.. only:: not EcSimulatorSiL

    Setting up and running |EcDemo|
    *******************************

    #. VxWorks OS configuration
        See sections above.
    #. Determine the network interface
        Using the command line option the network interface card and Real-time Ethernet Driver to be used in the example application can be determined. 
    #. Connection of the EtherCAT® slaves
        The slaves have to be connected with the VxWorks system using an Ethernet switch or a patch cable.
        Local IT infrastructure should not be mixed with EtherCAT® modules at the same switch as the |Product| will send many broadcast packets!
        EtherCAT® requires a 100Mbit/s connection. If the VxWorks network adapter card does not support this speed an 100Mbit/s (!) Ethernet switch has to be used.
    #. Download an Real-time Ethernet Driver module
        The Real-time Ethernet Driver library (e.g. :file:`emllIntelGbe.out`) which contains hardware support for the corresponding NIC must be downloaded.
        By default the Ethernet Driver emllSnarfGpp are contained with the binary delivery.
    #. Download the example application
        The target has to be started and a target-server connection will have to be established. After this the example application can be downloaded into the target.
    #. Set up a FTP server connection on host
        The demo application needs to load a XML file (:file:`eni.xml`) for the configuration of the |Product|. This file can be accessed using a FTP server. The screen shot below show, how to configure the FTP server.
        The directory contents can be checked via FTP using the ``ls`` command. The file :file:`eni.xml` will have to be accessed using the default directory.
    #. Check for exclusive hardware access
        Be sure that the network adapter instance dedicated to EtherCAT® is not controlled by a VxWorks driver, this can be verified using:
    
        .. prompt:: text ->
    
            muxShow
    
        If it is needed, first unload the driver using: 
        (e.g. first instance of the Intel Pro/100):
    
        .. prompt:: text ->
    
            muxDevUnload "fei", 1
    
        (e.g. second instance of the Intel Pro/1000):
    
        .. prompt:: text ->
    
            muxDevUnload "gei", 2
    
        (e.g. first instance of the Realtek 8139):
    
        .. prompt:: text ->
    
            muxDevUnload "rtl", 1
    
        (e.g. first instance of the Realtek 8169):
    
        .. prompt:: text ->
    
            muxDevUnload "rtg", 1
    
        (e.g. first instance of the FEC on Freescale iMX platform):
    
        .. prompt:: text ->
    
            muxDevUnload "motfec", 1
    
        (e.g. first instance of the ETSEC on Freescale PPC platform):
    
        .. prompt:: text ->
    
            muxDevUnload "motetsec", 1
    #. Run the example application
        The downloadable module |EcDemo_out| has to be executed. The configuration file :file:`eni.xml` will be used and thus has to be accessible in the current working directory.
        The appropriate Real-time Ethernet Driver and network adapter card have to be selected.
        If the log files shall be written the global variable ``bLogFileEnb`` has to be set to 1 prior to starting the demo.
    
        Loading and running the demo:
    
        .. prompt:: text ->
            :substitutions:
    
            ld<|EcDemo|.out
            sp EcMasterAppMain,"-intelgbe 1 1 -f eni.xml"
    
    .. only:: EcMaster

        Example: 
    
        .. figure:: ../../OsLayer/Media/EcMasterDemo_VxWorks.png
            :align:     center
            :alt:   

    .. seealso:: :ref:`running-ecdemo`

OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for VxWorks.

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/VxWorks
        <InstallPath>/Examples/Common/VxWorks

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/VxWorks
        <InstallPath>/Sources/OsLayer/VxWorks

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>/SDK/LIB/VxWorks/<ARCH>

GNU/PowerPC
    ``-mlongcall`` compiler option may be needed to avoid relocation offset errors when downloading :file:`.out` files.
