************
Introduction
************

What is EtherCAT?
*****************

EtherCAT® (Ethernet for Control Automation Technology) is a high-performance Ethernet Fieldbus technology that provides a reliable, efficient, and cost-effective communication solution for a wide variety of industrial automation applications. Originally developed as an open technology by Beckhoff Automation in 2003, and subsequently turned over to an independent organization known as the EtherCAT Technology Group, EtherCAT has since become one of the most widely used industrial Ethernet protocols in the world.

.. seealso:: A comprehensive introduction to EtherCAT technology can be found at https://www.acontis.com/en/what-is-ethercat-communication-protocol.html.

The EC-Master - Features
************************

Feature ID: 	Unique identification used in ETG.1500 EtherCAT Master Classes

.. _NotMandClassA: 

\*1: According to ETG.1500 Master Classes not mandatory for Class A


.. _NotMandClassB: 

\*2: According to ETG.1500 Master Classes not mandatory for Class B


.. list-table::
    :widths: 25 42 10 10 13
    :header-rows: 1

    * - Feature name
      - Short description
      - Class A
      - Class B 
      - Feature ID
    * - **Basic Features**
      -
      -
      -
      -
    * - Service Commands
      - Support of all commands 
      - ✅
      - ✅
      - 101
    * - IRQ field in datagram 
      - Use IRQ information from Slave in datagram header
      - ✅
      - ✅
      - 102
    * - Slaves with Device Emulation 
      - Support Slaves with and without application controller 
      - ✅
      - ✅
      - 103
    * - EtherCAT State Machine 
      - Support of ESM special behavior 
      - ✅
      - ✅
      - 104
    * - Error Handling  
      - Checking of network or slave errors, e.g. Working Counter 
      - ✅
      - ✅
      - 105
    * - VLAN  
      - Support VLAN Tagging 
      - ✅
      - :ref:`-- (*2) <NotMandClassB>`
      - 106
    * - EtherCAT Frame Types 
      - Support EtherCAT Frames 
      - ✅
      - ✅
      - 107
    * - UDP Frame Types
      - Support UDP Frames 
      - :ref:`-- (*1) <NotMandClassA>`
      - :ref:`-- (*2) <NotMandClassB>`
      - 108
    * - **Process Data Exchange**
      -
      -
      -
      -
    * - Cyclic PDO 
      - Cyclic process data exchange 
      - ✅
      - ✅
      - 201
    * - Multiple Tasks 
      - Different cycle tasks Multiple update rates for PDO 
      - ✅
      - ✅
      - 202
    * - Frame repetition
      - Send cyclic frames multiple times to increase immunity 
      - :ref:`-- (*1) <NotMandClassA>`
      - :ref:`-- (*2) <NotMandClassB>`
      - 203
    * - **Network Configuration**
      -
      -
      -
      -
    * - Online scanning 
      - Network configuration functionality included in EtherCAT Master  
      - ✅
      - ✅
      - 301
    * - Reading ENI 
      - Network Configuration taken from ENI file 
      - ✅
      - ✅
      - 301
    * - Compare Network configuration 
      - Compare configured and existing network configuration during boot-up 
      - ✅
      - ✅
      - 302
    * - Explicit Device identification 
      - Identification used for Hot Connect and prevention against cable swapping 
      - ✅
      - ✅
      - 303
    * - Station Alias Addressing 
      - Support configured station alias in slave, i.e. enable 2nd Address and use it 
      - ✅
      - ✅
      - 304
    * - Access to EEPROM 
      - Support routines to access EEPROM via ESC register 
      - ✅
      - ✅
      - 305
    * - **Mailbox Support**
      -
      -
      -
      -
    * - Support Mailbox  
      - Main functionality for mailbox transfer 
      - ✅
      - ✅
      - 401
    * - Mailbox Resilient Layer 
      - Support underlying resilient layer 
      - ✅
      - ✅
      - 402
    * - Multiple Mailbox channels 
      - 
      - ✅
      - ✅
      - 403
    * - Mailbox polling 
      - Polling Mailbox state in slaves  
      - ✅
      - ✅
      - 404
    * - **CAN application layer over EtherCAT (CoE)**
      -
      -
      -
      -
    * - SDO Up/Download  
      - Normal and expedited transfer 
      - ✅
      - ✅
      - 501
    * - Segmented Transfer 
      - Segmented transfer 
      - ✅
      - ✅
      - 502
    * - Complete Access 
      - Transfer the entire object (with all subindices) at once 
      - ✅
      - ✅
      - 503
    * - SDO Info service  
      - Services to read object dictionary 
      - ✅
      - ✅
      - 504
    * - Emergency Message 
      - Receive Emergency messages 
      - ✅
      - ✅
      - 505
    * - PDO in CoE 
      - PDO services transmitted via CoE 
      - :ref:`-- (*1) <NotMandClassA>`
      - :ref:`-- (*2) <NotMandClassB>`
      - 506
    * - **EoE**
      -
      -
      -
      -
    * - EoE protocol 
      - Services for tunneling Ethernet frames. includes all specified EoE services 
      - ✅
      - ✅
      - 601
    * - Virtual Switch  
      - Virtual Switch functionality 
      - ✅
      - ✅
      - 602
    * - EoE Endpoint to Operation Systems 
      - Interface to the Operation System on top of the EoE layer 
      - FP
      - :ref:`-- (*2) <NotMandClassB>`
      - 603
    * - **FoE**
      -
      -
      -
      -
    * - FoE Protocol 
      - Support FoE Protocol 
      - ✅
      - ✅
      - 701
    * - Firmware Up-/Download 
      - Password, FileName should be given by the application 
      - ✅
      - ✅
      - 702
    * - Boot State 
      - Support Boot-State for Firmware Up/Download 
      - ✅
      - ✅
      - 703
    * - **SoE**
      -
      -
      -
      -
    * - SoE Protocol 
      - Support SoE Services 
      - ✅
      - ✅
      - 801
    * - **AoE**
      -
      -
      -
      -
    * - AoE Protocol 
      - Support AoE Protocol 
      - ✅
      - ✅
      - 901
    * - **VoE**
      -
      -
      -
      -
    * - VoE Protocol 
      - External Connectivity supported 
      - ✅
      - ✅
      - 1001
    * - **Synchronization with Distributed Clock (DC)**
      -
      -
      -
      -
    * - DC support 
      - Support of Distributed Clocks 
      - ✅
      - :ref:`-- (*2) <NotMandClassB>`
      - 1101
    * - Continuous Propagation Delay compensation 
      - Continuous Calculation of the propagation delay  
      - ✅
      - :ref:`-- (*2) <NotMandClassB>`
      - 1102
    * - Sync window monitoring 
      - Continuous monitoring of the Synchronization difference in the slaves 
      - ✅
      - :ref:`-- (*2) <NotMandClassB>`
      - 1103
    * - **Slave-to-Slave Communication**
      -
      -
      -
      -
    * - via Master 
      - Information is given in ENI file or can be part of any other network configuration. Copying of the data can be handled by master stack or master’s application 
      - ✅
      - ✅
      - 1201
    * - **Master information**
      -
      -
      -
      -
    * - Master Object Dictionary 
      - 
      - FP
      - :ref:`-- (*2) <NotMandClassB>`
      - 1301

.. raw:: latex

    \newpage

Protected version
*****************

The EC-Master software can be delivered in 3 different versions:

Protected
    Binary with MAC protection
Unrestricted
    Binary without MAC protection
Source
    Source code

The protected version will automatically stop after about 1 hour of continuous operation. In order to remove this restriction a valid runtime license key is required. The runtime license protection is based on the MAC address of the Ethernet controller used for the EtherCAT protocol. With a valid License Key the protected version of EC-Master will automatically become an unrestricted version.

Licensing procedure for Development Licenses
============================================

#. Installation of EC-Master protected version
#. Determine the MAC Address by calling :cpp:func:`emGetSrcMacAddress` or from a sticker applied on the hardware near the Ethernet controller
#. Send an Email with the subject "**Development License Key Request, Commission** *your commission number*" with the MAC address to sales@acontis.com
#. Acontis will create the license keys and return them in a License Key Text File (CSV format).

   .. code-block:: none

       Number;MAC Address;License Key
       1;00-00-5A-11-77-FE;DA1099F2-15C249E9-54327FBC
       2;64-31-50-80-20-4E;1B7C1F86-D08E40A8-4F96F2BA
       3;2C-F0-5D-03-CB-2B;10005078-DFD9A2C3-5FD4B1CD-35041597-F8094AA4-6C7CCE7E

#. Activate the License Key by calling :cpp:func:`emSetLicenseKey` with the license key that corresponds to the MAC address on the hardware and check the return code. The license key is 26 or 53 characters long.

   .. code-block:: cpp
   
       dwRes = emSetLicenseKey(0, "DA1099F2-15C249E9-54327FBC");

Licensing procedure for Runtime Licenses
========================================

#. Installation of EC-Master protected version
#. Determine the MAC Address by calling :cpp:func:`emGetSrcMacAddress` or from a sticker applied on the hardware near the Ethernet controller
#. Provide the MAC Addresses and numbers from previously ordered and unused runtime license stickers in a text file to acontis as described in the example below. Please use a separate line for each runtime license sticker number and MAC Address.

   .. code-block:: none
   
       S/N; MAC Address
       100-105-1-1/1603310001;00-00-5A-11-77-FE  
       100-105-1-1/1603310002;64-31-50-80-20-4E
       100-105-1-1/1603310003;2C-F0-5D-03-CB-2B

#. Send an Email with the subject "**Runtime License Key Request, Commission** *your commission number*" with the MAC address to sales@acontis.com
#. Acontis will create the license keys and return them in a License Key Text File.

   .. code-block:: none  
   
       Number;MAC Address;License Key
       1;00-00-5A-11-77-FE;DA1099F2-15C249E9-54327FBC    
       2;64-31-50-80-20-4E;1B7C1F86-D08E40A8-4F96F2BA
       3;2C-F0-5D-03-CB-2B;10005078-DFD9A2C3-5FD4B1CD-35041597-F8094AA4-6C7CCE7E

#. Activate the License Key by calling :cpp:func:`emSetLicenseKey` with the license key that corresponds to the MAC address on the hardware and check the return code.

   .. code-block:: cpp
   
       dwRes = emSetLicenseKey(0, "DA1099F2-15C249E9-54327FBC");

.. include:: ../../Common/license.rst