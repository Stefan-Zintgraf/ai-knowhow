The parameters to the Windows TAP Real-time Ethernet Driver are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineTap` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_TAP
    :members: 

The adapter must be manually installed as described in the OpenVPN's Windows TAP-driver manual, see https://community.openvpn.net/openvpn/wiki/GettingTapWindows .

While |Product| is connected to the adapter using emllTap, the Master can use it with e.g. emllNdis.