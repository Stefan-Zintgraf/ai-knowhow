.. only:: not EcMonitor

    The emllRemote is used to tunnel EtherCAT frames within a TCP socket between EC-Master and EC-Simulator.
    
.. only:: EcMonitor

    The emllRemote is used to receive EtherCAT frames tunneled through TCP sockets. 

The parameters to the Remote Driver are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineRemote` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_REMOTE
    :members: 

While |Product| listens on the given port using emllRemote, the EC-Master can connect to it using emllRemote.

.. only:: not EcMonitor

    EcSimulatorHilDemo command line example:
        .. prompt:: bash
    
            EcSimulatorHilDemo -remote 1 0 0.0.0.0 10001 0.0.0.0 0 -f eni.xml
    
    EcMasterDemo command line example:
        .. prompt:: bash
    
            EcMasterDemo -remote 1 1 0.0.0.0 0 127.0.0.1 10001

.. only:: EcMonitor

    EcMonitorDemo command line example:
        .. prompt::
            
            EcMonitorDemo -remote 1 0 0.0.0.0 10001 0.0.0.0 0 -f eni.xml
            
    EcMasterDemo command line example:
        .. prompt:: bash
    
            EcMasterDemo -integbe 1 1 -f eni.xml -mirror -remote 1 1 0.0.0.0 0 127.0.0.1 10001