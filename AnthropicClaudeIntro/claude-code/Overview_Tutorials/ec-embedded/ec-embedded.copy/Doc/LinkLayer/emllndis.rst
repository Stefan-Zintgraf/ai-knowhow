As default |Product| for Windows contains emllNdis.dll to use a native Windows driver for EtherCAT®.

The acontis ECAT Protocol Driver is needed to use the Ethernet Driver NDIS and can be installed from

- :file:`Bin/Windows/x64/EcatNdisSetup-x86_64Bit.msi` or 
- :file:`Bin/Windows/x86/EcatNdisSetup-x86_32Bit.msi` 

respectively depend on the Windows Operating System Type of 64 Bit or 32 Bit.

IPv4 must be installed for the network adapter as the Ethernet Driver NDIS uses the IP address to identify the network adapter. 

The parameters to the Ethernet Driver NDIS are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineNDIS` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_NDIS
    :members:
    
In case of problems while using the Ethernet Driver, it is advised to set the windows registry entry DontSetPromiscuousMode of the ECAT NDIS Protocol driver. This option is available since V3.1.3.02 of the driver.
This can be done through the following steps:

- Install ECAT NDIS Protocol driver (V3.1.3.02 or newer version)
- Open the registry editor
- Switch to Computer\\HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Ecatndis, or just look for Ecatndis in the editor
- Create a new DWORD entry named DontSetPromiscuousMode
- Set the value of DontSetPromiscuousMode to 1
- Close the registry editor and restart your computer
