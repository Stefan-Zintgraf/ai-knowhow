..
    ****************
    IntervalZero RTX
    ****************

.. only:: EcMaster

    |Product| is available for the RTX versions listed below:

    .. list-table::
        :header-rows: 1
        
        * - RTX version
          - EC-Master version
        * - RTX 2012
          - V2.9.x.x
        * - RTX 2016
          - V2.9.x.x  
        * - RTX64 2014
          - V2.9.x.x
        * - RTX64 3.x
          - V3.1.x.x
        * - RTX64 4.x
          - V3.1.x.x

.. only:: EcSimulator

    |Product| HiL is available for RTX64 3.x and RTX64 4.x .

.. only:: not EcSimulatorSiL

    Unbind Ethernet Driver instance
    *******************************
    
    To use Real-time Ethernet Driver under RTX, the network adapter should be assigned to RTX as described in the RTX user manual.
    The NIC driver should not use the network adapter for TCP/IP and therefore the network adapter may not be configured in RtxTcpIp.ini.

    Setting up and running |EcDemo|
    *******************************
    
    The file |EcDemo|.rtss has to be executed. The full path to the ENI file has to be given as a command line parameter as well as the appropriate Real-time Ethernet Driver.
    
    .. prompt:: text >
        :substitutions:
    
        RTSSrun |EcDemo|.rtss -i8255x 1 1 -f C:/eni.xml
    
    .. seealso:: :ref:`running-ecdemo`

OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for RTX.

Extra include paths
    .. code-block::
        
        <InstallPath>\SDK\INC\RTX
        <InstallPath>\Examples\Common\RTX

Extra source paths
    .. code-block::
    
        <InstallPath>\Examples\Common\RTX
        <InstallPath>\Sources\OsLayer\RTX

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>\SDK\LIB\RTX64 (RTX64 4.x)
        <InstallPath>\SDK\LIB\RTX64_30 (RTX64 3.x)