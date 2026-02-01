..
    *****************
    Microsoft Windows
    *****************

.. only:: not EcSimulatorSiL

    |EcDemo|
    ********

    #. Install |Product| 
        Run :file:`setup.exe` from |Product| package, which will guide you through the installation process.
    #. Determine the network interface
        For example the option `-ndis 192.168.1.1 1` will be using the network adapter card with the IP address 192.168.1.1.

    .. only:: EcMaster
 
      3. Connect EtherCAT modules
          Any EtherCAT module can be directly connected to the target system. EtherCAT requires a 100 Mbit/s connection. If the Ethernet adapter card does not support this speed, an Ethernet switch must be used.
  
          .. warning:: The local IT infrastructure should not be mixed with EtherCAT modules on the same Ethernet adapter. The EC-Master sends many broadcast packets!

    .. only:: EcMonitor

      3. Insert a TAP device after the Master Controller to capture the EtherCAT traffic and start the EtherCAT master

    4. Run the example application
        Execute |EcDemo|.exe from :file:`<InstallPath>/Bin/Windows/<Arch>/`. At least an Ethernet Driver option has to be given.
    
        .. prompt:: batch
            :substitutions:
    
            |EcDemo| -ndis 192.168.1.1 1 -f D:/eni.xml -sp

        .. only:: EcMaster
    
            .. figure:: ../../OsLayer/Media/EcMasterDemo_Windows.png
                :align:     center
                :alt:   

    .. seealso:: :ref:`running-ecdemo` for a detailed description of the demo application.

.. only:: EcMaster

    EcMasterDemoDotNet (.NET) - Microsoft Windows
    *********************************************

    #. Install |Product| 
        Run :file:`setup.exe` from |Product| package, which will guide you through the installation process.
    #. Determine the network interface
        For example the option --link `ndis 192.168.1.1 1` will be using the network adapter card with the IP address 192.168.1.1.
    #. Connect EtherCAT modules
        Any EtherCAT module can be directly connected to the target system. EtherCAT requires a 100 Mbit/s connection. If the Ethernet adapter card does not support this speed, an Ethernet switch must be used.
        
        .. warning:: The local IT infrastructure should not be mixed with EtherCAT modules on the same Ethernet adapter. The EC-Master sends many broadcast packets!
    #. Run the example application
        Execute :file:`<InstallPath>/Bin/Windows/<Arch>/EcMasterDemoDotNet.exe`. At least an Ethernet Driver option has to be given.
        
        .. prompt:: batch
        
          EcMasterDemoDotNet -mode 1 -file eni.xml -link "ndis 192.168.1.1 1" -sp 6000 (-help will show usage)

        .. figure:: ../Media/EcMasterDemoDotNet_Windows.png
            :align:     center
            :alt:

    EcMasterDemoGuiDotNet (.NET) - Microsoft Windows 
    ************************************************

    #. Prerequisites
        To run the :file:`EcMasterDemoGuiDotNet.exe`, the libraries :file:`EcMaster.dll`, :file:`EcMasterRasServer.dll`, :file:`EcWrapperDotNet.dll`, :file:`EcWrapper.dll` and :file:`emllNdis.dll` from :file:`Bin/Windows/x64` are needed in :file:`Bin/Windows/x64/Release`, :file:`Bin/Windows/x64/Debug`
    #. Visual Studio C#-project
        The C#-project for VS2015 or higher is located at :file:`Workspace/WindowsVS2015/EcMasterDemoGuiDotNet/EcMasterDemoGuiDotNet.csproj`
    #. If the reference EcWrapperDotNet is missing, it must be re-added from :file:`Bin/Windows/x64/EcWrapperDotNet.dll`
    #. EcMasterDemoGuiDotNet is now prepared for Run/Debug

.. only:: EcMonitor

    EcMonitorDemoGuiDotNet (.NET) - Microsoft Windows 
    *************************************************

    #. Prerequisites
        To run the :file:`EcMonitorDemoGuiDotNet.exe`, the libraries :file:`EcMonitor.dll`, :file:`EcWrapperDotNet.dll`, :file:`EcWrapper.dll` and :file:`emllNdis.dll` from :file:`Bin/Windows/x64` are needed in :file:`Bin/Windows/x64/Release`, :file:`Bin/Windows/x64/Debug`
    #. Visual Studio C#-project
        The C#-project for VS2015 or higher is located at :file:`Workspace/WindowsVS2015/EcMonitorDemoGuiDotNet/EcMonitorDemoGuiDotNet.csproj`
    #. If the reference EcWrapperDotNet is missing, it must be re-added from :file:`Bin/Windows/x64/EcWrapperDotNet.dll`
    #. EcMonitorDemoGuiDotNet is now prepared for Run/Debug

OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for Windows.

Extra include paths
    .. code-block::
        
        <InstallPath>\SDK\INC\Windows
        <InstallPath>\Examples\Common\Windows

Extra source paths
    .. code-block::
    
        <InstallPath>\Examples\Common\Windows
        <InstallPath>\Sources\OsLayer\Windows

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>\SDK\LIB\Windows


RtaccDevice for Real-time Ethernet Driver
*****************************************

As alternative to the NDIS based or Pcap based Ethernet Driver, an optional Real-time Ethernet Driver on Windows can be installed. The Real-time Ethernet Driver replaces the original Windows driver and also requires an extra license.

To use the Real-time Ethernet Driver under Windows, it is necessary to install the RtaccDevice driver included in the Real-time Ethernet Driver delivery:

#. Start the "Device Manager"
    .. figure:: ../../OsLayer/Media/ecatdrv-net-step1.png
        :align:     center
        :alt:       

#. Assign RtaccDevice to the network adapter
    .. figure:: ../../OsLayer/Media/ecatdrv-net-step2.png
        :align:     center
        :alt:
    
   .. figure:: ../../OsLayer/Media/ecatdrv-net-step3.png
        :align:     center
        :alt:
    
   .. figure:: ../../OsLayer/Media/ecatdrv-net-step4.png
        :align:     center
        :alt:

   Click on "Browse my computer for driver"

   .. figure:: ../../OsLayer/Media/ecatdrv-net-step5.png
        :align:     center
        :alt:

   Click on "Let me pick..."

   .. figure:: ../../OsLayer/Media/ecatdrv-net-step6.png
        :align:     center
        :alt:

   Click on "Have Disk..."

#. Enter the directory of RtaccDevice Driver

   The default folder if not changed is :file:`<InstallPath>\\Bin\\Windows\\x64`
   
   .. figure:: ../../OsLayer/Media/ecatdrv-net-step7.png
       :align:     center
       :alt:
   
   Enter the correct directory at the input box and press OK to proceed.

#. Choose the RtaccDevice Driver and click "Next" and confirm the installation
    .. figure:: ../../OsLayer/Media/ecatdrv-net-step8.png
        :align:     center
        :alt:       
    .. figure:: ../../OsLayer/Media/ecatdrv-net-step9.png
        :align:     center
        :alt:

Optionally modify search location Real-time Ethernet Driver

Search locations for Real-time Ethernet Driver can be adjusted using the PATH environment variable.
