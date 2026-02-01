************
Introduction
************

The EoE module within the Master acts as an intermediary between the EtherCAT master stack
and the operating system's TCP/IP/ETH protocol stack.
It operates as an Ethernet switch, which connects the slaves, capable of handling the EOE protocol, with the operating system. 

* The EoE-Endpoint can be used with different operating systems.
* It works as a standard Ethernet driver / Network Interface Card (NIC) driver
* It requires minimal adaption to the operating system.

* It is simple to implement 

  * Single function to register all EoE service function hooks 
  * follows the open/read/write/close lifecycle of many other drivers
  * flexible data buffer handling
  * polling or interrupt driven operation