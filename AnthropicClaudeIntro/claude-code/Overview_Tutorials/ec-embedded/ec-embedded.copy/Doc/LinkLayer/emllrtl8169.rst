The parameters to the Real-time Ethernet Driver Realtek RTL8169 are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineRTL8169` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_RTL8169
    :members:

RTL8169 usage under Linux
*************************

Because the Linux Kernel module de-initializes the PHY on unloading, Linux must be prevented from loading the r8169 module on startup.

Supported PCI devices
*********************
    
.. datatemplate:xml:: PCI_DEVICES_EMLLRTL8169
    :source: ../_build/doxygen/xml/combined.xml
    :template: hlist-doxygroups.jinja