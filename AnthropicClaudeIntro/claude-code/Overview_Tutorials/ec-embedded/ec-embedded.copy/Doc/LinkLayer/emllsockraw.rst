emllSockRaw is part of |Product| for Linux. emllSockRaw uses the native network adapter, e.g. eth0, eth1, etc . 
The network adapter must be exclusively used for EtherCAT and cannot be used for LAN (local area network) at the same time.
Because the native Linux driver for the network adapter type is typically not fully real-time capable, it cannot be used for real time applications. If possible, an acontis Real-time Ethernet Driver, e.g. emllIntelGbe, should be used instead.
emllSockRaw does not need the atemsys driver.

.. note:: Root privileges are required. A cycle time of 4 ms or higher may be needed.
        
To run the application without root privileges, set the Linux capability 'cap_net_raw' to the application.
    .. prompt:: bash
        
        sudo setcap 'cap_net_raw+pe' ./EcMasterDemo
        
To run python scripts without root privileges, create a python environment and set the Linux capability 'cap_net_raw' to the python interpreter. 
    .. prompt:: bash
        
        cd Bin/Linux
        python3 -m venv --copies PyEnv/
        source PyEnv/bin/activate
        sudo setcap 'cap_net_raw+pe' PyEnv/bin/python3
        
The parameters to emllSockRaw are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineSockRaw` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the parameters.

.. doxygenstruct:: EC_T_LINK_PARMS_SOCKRAW
    :members:
    