The parameters to the Real-time Ethernet Driver Intel Pro/100 are setup-specific. 
The function :cpp:func:`CreateLinkParmsFromCmdLinei8255x` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_I8255X
    :members:

.. code-block:: cpp

    #include "EcLink.h"
    EC_T_LINK_PARMS_I8255X oLinkParmsAdapter;
    
    OsMemset(&oLinkParmsAdapter, 0, sizeof(EC_T_LINK_PARMS_I8255X));
    oLinkParmsAdapter.linkParms.dwSignature   = EC_LINK_PARMS_SIGNATURE_I8255X;
    oLinkParmsAdapter.linkParms.dwSize        = sizeof(EC_T_LINK_PARMS_I8255X);
    OsStrncpy(oLinkParmsAdapter.linkParms.szDriverIdent,
            EC_LINK_PARMS_IDENT_I8255X, MAX_DRIVER_IDENT_LEN - 1);
    oLinkParmsAdapter.linkParms.dwInstance    = 1;
    oLinkParmsAdapter.linkParms.eLinkMode     = EcLinkMode_POLLING;
    oLinkParmsAdapter.linkParms.dwIstPriority = dwIstPriority;

Supported PCI devices
*********************
    
.. datatemplate:xml:: PCI_DEVICES_EMLLI8255X
    :source: ../_build/doxygen/xml/combined.xml
    :template: hlist-doxygroups.jinja