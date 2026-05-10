.. _install:

*****************
Install |Product|
*****************

The |Product| SDK including its examples is contained in the installation package named e.g. :file:`EC-Monitor-V3.2.2.05-Windows-x86_64Bit-Eval.zip`\ . The procedure is generally the same for all operating systems supported by the |Product|\ .

Prepare the Operating System (Windows)
**************************************

The installation of |Product| for Windows contains the installer :file:`setup.msi` guiding through the installation process. The acontis ECAT Protocol Driver is needed to use the Ethernet Driver NDIS. It can be installed from

- :file:`<InstallPath>\\Bin\\Windows\\x64\\EcatNdisSetup-x86_64Bit.msi`
- :file:`<InstallPath>\\Bin\\Windows\\x86\\EcatNdisSetup-x86_32Bit.msi`

The command "ipconfig" shows the IP settings of the installed network adapters, including the IP address of the dedicated Ethernet network adapter for |Product| e.g., "192.168.99.1".

Prepare the Operating System (Linux)
************************************

For non-Windows operating systems, the files of the SDK to be extracted are directly contained within the installation package. It is recommended to copy the files to a folder where the user has write access.

|Product| supports different Ethernet adapter types.

It is recommended to use an Intel Pro/1000 handled by the acontis emllIntelGbe driver. 
Other network adapter types are supported too and described in the |Product| User Manual.

1. The acontis atemsys Linux Kernel driver must be downloaded and applied to the Linux system: See https://github.com/acontis/atemsys\ .

2. The commands "lshw -short -c network" and "lspci | grep Ethernet" show the hardware information of the installed network adapters, 
   including the PCI bus address of the dedicated Ethernet network adapter for |Product|, e.g. "01:00.0" (bus 01, device 00, function 0 as needed below):
   
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

   The PCI bus address is used to specify the network adapter adapter used by |Product| Demo and is formatted as 0x01bbddff:
   
   * *bb* Bus Number
   * *dd* Device Number
   * *ff* Function Number

3. The dedicated network adapter to be used must be unbound from the Linux Kernel and atemsys loaded:

   .. prompt:: bash

     echo "0000:01:00.0" > /sys/bus/pci/drivers/igb/unbind 
     modprobe atemsys

Unbinding the network adapter instance from the Linux Kernel and loading the atemsys Kernel driver is non-persistent and **must be redone after reboot.**