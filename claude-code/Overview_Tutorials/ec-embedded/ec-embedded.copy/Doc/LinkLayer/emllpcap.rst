An Ethernet Driver based on the WinPcap library is shipped with the |Product|. This Ethernet Driver is implemented using a network filter driver that enables the software to send and receive raw Ethernet frames. Using this Ethernet Driver any Windows standard network drivers can be used.
The Windows network adapter card has to be assigned a unique IP address (private IP address range). This IP address is used by the EtherCAT® WinPcap Ethernet Driver driver to select the appropriate adapter.

It is recommended to use a separate network adapter to connect EtherCAT® devices. If the main network adapter is used for both EtherCAT® devices and the local area network there may be a main impact on the local area network operation.
The network adapter card used by EtherCAT® has to be set to a fixed private IP address, e.g. 192.168.x.y.

The parameters to the Ethernet Driver WinPcap are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineWinPcap` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_WINPCAP
    :members:

WinPcap, Npcap support
**********************

At least WinPcap version 4.1.2 or Npcap 0.07 r17 must be used. WinPcap version 4.1.2 is the preferred library. 

The |Product| installer installs WinPcap by default.

If using Npcap 0.07 r17, the WinPcap API-compatible mode must be chosen:

.. figure:: ../../LinkLayer/Media/Npcap-Installer.png 
    :align:     center
    :alt:       