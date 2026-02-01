***************************
Install |Product| |Edition|
***************************

The |Product| SDK including its examples is contained in the installation package named e.g. 
:file:`EC-Simulator-`\ |FileEdition|\ :file:`-V3.2.1.01-Windows-x86_64Bit-Eval.zip`\ .

The procedure is generally the same for all operating systems supported by the |Product|\ . 

.. only:: EcSimulatorSiL

    Because the SDK is an AddOn to the EC-Master, first the EC-Master SDK must be installed.

    The installation of EC-Master for Windows contains the installer :file:`setup.exe` guiding through the installation process. For non-Windows operating systems, the files of the EC-Master SDK to be extracted are directly contained within the installation package.

    After installing EC-Master, the |Product| |Edition| SDK AddOn must be extracted within the EC-Master SDK installation folder.

    It is recommended to copy the files to a folder where the user has write access after installation. 

.. only:: EcSimulatorHiL

    The installation of |Product| for Windows contains the installer :file:`setup.exe` guiding through the installation process.

    For non-Windows operating systems, the files of the SDK to be extracted are directly contained within the installation package.

    It is recommended to copy the files to a folder where the user has write access. 

.. only:: EcSimulatorHiL

    Prepare the EtherCAT\ |R| Simulator Device
    ******************************************


    When running, the |Product| |Edition| listens on a specific network adapter for EtherCAT® frames sent by the Master, 
    simulates the network and sends them back to the Master:

    .. image:: ../Media/qsprepare1.png
       :scale: 75
       :align: center

    **The Ethernet network adapter must be dedicated to be used by** |Product| |Edition| **and may not be mixed with other devices, i.e. LAN infrastructure!**

    It is recommended to add an Intel Gigabit PCIe NIC used for |Product| to the EtherCAT\ |R| Simulator Device for this purpose.

.. only:: EcSimulatorSiL

    Prepare the EtherCAT\ |R| Simulator Device for licensed usage
    *************************************************************

    .. image:: ../Media/qssilprepare1.png
       :scale: 75
       :align: center

    **The Ethernet network adapter must be dedicated to be used by **\ |Product| |Edition|\ **'s license check and may not be mixed with other devices, i.e. LAN infrastructure!**

    The license key **must match the network adapter** given as parameter for license purposes!


Prepare the Operating System (Windows)
**************************************

.. only:: EcSimulatorHiL

    The command "ipconfig" shows the IP settings of the installed network adapters, including the IP address of the dedicated Ethernet 
    network adapter for |Product| |Edition| e.g., "192.168.99.1".

.. only:: EcSimulatorSiL

   The command "ipconfig" shows the IP settings of the installed network adapters, including the MAC address according to the license key and the IP address of the dedicated Ethernet network adapter 
   for |Product| |Edition| e.g., "192.168.99.1".


Prepare the Operating System (Linux)
************************************

.. only:: EcSimulatorHiL

   |Product| |Edition| supports different Ethernet adapter types.
   
.. only:: EcSimulatorSiL
  
   |Product| |Edition|\ 's license check supports different Ethernet adapter types.
   

It is recommended to use an Intel Pro/1000 handled by the acontis emllIntelGbe driver. 
Other network adapter types are supported too and described in the |Product| |Edition| User Manual.

1. The acontis atemsys Linux Kernel driver must be downloaded and applied to the Linux system: See https://github.com/acontis/atemsys\ .

2. The commands "lshw -short -c network" and "lspci | grep Ethernet" show the hardware information of the installed network adapters, 
   including the PCI bus address of the dedicated Ethernet network adapter for |Product| |Edition|, e.g. "01:00.0" (bus 01, device 00, function 0 as needed below):
   
   .. prompt:: bash
   
       sudo bash
       lshw -short -c network

       H/W path        Device      Class          Description
       ======================================================
       /0/100/1/0      enp1s0f0    network        I350 Gigabit Network Connection
       /0/100/19       lan         network        Ethernet Connection I217-LM
       
       lspci | grep Ethernet
       00:19.0 Ethernet controller: Intel Corporation Ethernet Connection I217-LM
       01:00.0 Ethernet controller: I350 Gigabit Network Connection

   The PCI bus address is used to specify the network adapter adapter used by EcSimulator\ |Edition|\ Demo and is formatted as 0x01bbddff:
   
   * *bb* Bus Number
   * *dd* Device Number
   * *ff* Function Number

3. The dedicated network adapter to be used must be unbound from the Linux Kernel and atemsys loaded:

     root@myLinuxTarget:~# echo "0000:01:00.0" > /sys/bus/pci/drivers/igb/unbind

     root@myLinuxTarget:~# modprobe atemsys

   Unbinding the network adapter instance from the Linux Kernel and loading the atemsys Kernel driver is non-persistent and **must be redone after reboot.**



   










