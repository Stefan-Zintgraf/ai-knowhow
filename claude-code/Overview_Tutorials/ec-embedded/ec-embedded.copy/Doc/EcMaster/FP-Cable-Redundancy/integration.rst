******************
Sample integration
******************

Redundancy support in EcMasterDemo
**********************************

Since Version 2.5 redundancy support is automatically enabled in EcMasterDemo when giving two Real-time Ethernet Driver definitions at the command line. Different Real-time Ethernet Driver types are supported as well as using the same type twice.
Since V3.2.2.03 the parameter -junctionred sets the redundancy mode to automatic, otherwise it is disabled.

The following statement will set the device with IP 192.168.0.120 as primary and the device with IP 192.168.1.120 as secondary EtherCAT® interface, both using winpcap Ethernet Driver:

.. prompt:: cmd
    
    EcMasterDemo -f Network-ENI.xml -ndis 192.168.0.120 1 -ndis 192.168.1.120 1

EcMasterDemo logs the usage of both interfaces by means of the following lines:

.. code-block:: text
    
    EcLinkOpen(): Use WinPcap version 4.1.2 (packet.dll version 4.1.0.2001), based on libpcap version 1.0 branch 1_0_rel0b (20091008)
    EcLinkOpen(): Use network adapter  "Intel(R) PRO/100 M-Desktopadapter"
    EcLinkOpen(): Use WinPcap version 4.1.2 (packet.dll version 4.1.0.2001), based on libpcap version 1.0 branch 1_0_rel0b (20091008)
    EcLinkOpen(): Use network adapter  "Realtek RTL8168B/8111B PCI-E Gigabit Ethernet NIC"

The network adapter names will likely differ from the ones giving in the sample above depending on the EcMasterDemo host machine and the engaged Real-time Ethernet Driver.

Redundancy support in EC-SlaveTestApplication
*********************************************

The "Redundancy Real-time Ethernet Driver" definition in the EC-SlaveTestApplication activates redundant EtherCAT® network interfaces usage as demonstrated in the following screenshot:

.. figure:: ../Media/cable-red_EC-SlaveTestApplication.png
    :alt:
