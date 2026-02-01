The parameters to the Real-time Ethernet Driver CCAT are setup-specific. 
The function :cpp:func:`CreateLinkParmsFromCmdLineCCAT` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.
Because the link status cannot be read quickly from a register of the adapter, it will not be automatically refreshed like by the other Real-time Ethernet Drivers.

.. doxygenstruct:: EC_T_LINK_PARMS_CCAT
    :members:

.. doxygenenum:: EC_T_CCAT_TYPE

Supported PCI devices
*********************

.. datatemplate:xml:: PCI_DEVICES_EMLLCCAT
    :source: ../_build/doxygen/xml/combined.xml
    :template: hlist-doxygroups.jinja