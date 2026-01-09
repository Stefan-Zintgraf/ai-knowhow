The parameters to the VLAN Real-time Ethernet Driver are setup-specific. The function "CreateLinkParmsFromCmdLineVlan" in EcSelectLinkLayer.cpp demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_VLAN
    :members: 

Switch Configuration
********************
Ensure that the Spanning Tree Protocol (STP) is disabled on the ports used for EtherCAT, because it can lead to permanent frame loss.
