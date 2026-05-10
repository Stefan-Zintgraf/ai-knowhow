The parameters to the Real-time Ethernet Driver Intel Pro/1000 are setup-specific. 
The function "CreateLinkParmsFromCmdLineIntelGbe" in EcSelectLinkLayer.cpp demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_INTELGBE
    :members:
    
.. ifconfig:: 'EC-Master' in product

    NICs equipped with 82577, 82579 or 82567 may need HardCodedPhySettings. This must be set after :cpp:func:`emInitMaster`, before using the NIC, e.g.:

    .. code-block:: cpp

        {
            EC_T_IOCTLPARMS oIoCtlParms;
            OsMemset(&oIoCtlParms, 0, sizeof(EC_T_IOCTLPARMS));
            oIoCtlParms.pbyInBuf        = (EC_T_BYTE*)EC_NULL + 0x20103;
            oIoCtlParms.dwInBufSize     = sizeof(EC_T_DWORD);
            emIoControl(dwInstanceId, EC_IOCTL_LINKLAYER_MAIN + EC_LINKIOCTL_FORCELINKMODE, &oIoCtlParms);
            OsSleep(1000);
        }

.. ifconfig:: 'EC-Simulator' in product
	
    NICs equipped with 82577, 82579 or 82567 may need HardCodedPhySettings. This must be set after :cpp:func:`esInitSimulator`, before using the NIC, e.g.:

    .. code-block:: cpp

        {
            EC_T_IOCTLPARMS oIoCtlParms;
            OsMemset(&oIoCtlParms, 0, sizeof(EC_T_IOCTLPARMS));
            oIoCtlParms.pbyInBuf        = (EC_T_BYTE*)EC_NULL + 0x20103;
            oIoCtlParms.dwInBufSize     = sizeof(EC_T_DWORD);
            esIoControl(dwSimulatorInstanceId, EC_IOCTL_LINKLAYER_MAIN | EC_LINKIOCTL_FORCELINKMODE, &oIoCtlParms);
            OsSleep(1000);
        }

TTS Feature
***********

The IntelGbe Real-time Ethernet Driver can optionally use Time-Triggered Send (TTS) feature. Ethernet/EtherCAT frames are sent and time stamped according to the NIC timer instead of the CPU timer. Which is usually more accurate.

.. seealso:: :cpp:struct:`EC_T_LINKLAYER_TIMINGTASK`, :cpp:enum:`EC_T_LINKLAYER_TIMING`

Supported PCI devices
*********************

.. datatemplate:xml:: PCI_DEVICES_EMLLINTELGBE
    :source: ../_build/doxygen/xml/combined.xml
    :template: hlist-doxygroups.jinja
