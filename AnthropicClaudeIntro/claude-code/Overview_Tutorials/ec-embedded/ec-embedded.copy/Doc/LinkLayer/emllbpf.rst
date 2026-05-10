The Ethernet Driver BPF is always part of the EC-Master for QNX package. It uses already established Ethernet adapters, e.g. wm0, rt0, etc. It is strongly recommended to use a separate network adapter to connect EtherCAT devices. If the main network adapter is used for both EtherCAT devices and the local area network there may be a main impact on the local area network operation. 

.. note:: The BPF Ethernet Driver cannot be used for real time applications and may need cycle time of 1 ms or higher.
        
The parameters to the Ethernet Driver BPF are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineBPF` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_BPF
    :members:
    