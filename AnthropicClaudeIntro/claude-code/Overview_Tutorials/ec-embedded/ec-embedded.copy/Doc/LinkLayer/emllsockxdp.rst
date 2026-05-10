The Real-time Ethernet Driver SockXdp does not need the atemsys driver and uses already established Ethernet adapters, e.g. eth0, eth1, etc. It is strongly recommended to use a separate network adapter to connect EtherCAT devices. If the main network adapter is used for both EtherCAT devices and the local area network there may be a main impact on the local area network operation. 

.. note:: Root privileges are required.
        
The parameters to the Real-time Ethernet Driver SockXdp are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineSockXdp` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_SOCKXDP
    :members:

.. doxygenenum:: EC_T_XDP_MODE

Linux System Requirements
*************************
	
To use the XDP Real-time Ethernet Driver the following system requirements need to be met:

- Your kernel have to support XDP, check if the following entry is activated in your :file:`.config` file.
	``CONFIG_XDP_SOCKETS=y``
	
	If it is not activated you need to rebuild your kernel with ``CONFIG_XDP_SOCKETS``.

Getting started
***************

- Download libxdp Version 1.4.3 from https://github.com/xdp-project/xdp-tools and install it.
- Download libbpf Version 1.5.0 from https://github.com/libbpf/libbpf and install it.
- Update the linux drivers of the NIC that would be used
- If the NIC  supports XDP, turn off xdp generic mode: 
    .. prompt:: bash
        
        ip link set dev eth0 xdpgeneric off
- If the NIC have multiple queue support, use one queue instead of multiple queues:
    .. prompt:: bash
        
        ethtool -L eth0 combined 1
