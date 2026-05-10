The parameters to the Multiplier Real-time Ethernet Driver are setup-specific. The function "CreateLinkParmsFromCmdLineMultiplier" in EcSelectLinkLayer.cpp demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_MULTIPLIER
    :members: 
    
.. doxygenenum:: EC_T_MULTIPLIER_TYPE

Configuration with EC-Engineer
******************************

This configuration is valid for one downlink port. For each used CUxxxx multiplier downlink port, a new configuration should be arranged.

- Start EC-Engineer in Offline Configuration modus.
- Add the CU2508 Ethernet Port as your first slave.

.. figure:: ../Media/CU2508_Ethernet_Port.png
    :align:     center
    :alt:
    
- Append the slaves that you are going to connect to the port.

.. figure:: ../Media/CU2508_Configuration.png
    :align:     center
    :alt:  

