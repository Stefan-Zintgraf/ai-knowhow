************
Introduction
************

What is EtherCAT®?
******************

EtherCAT® (Ethernet for Control Automation Technology) is a high-performance Ethernet Fieldbus technology that provides a reliable, efficient, and cost-effective communication solution for a wide variety of industrial automation applications. Originally developed as an open technology by Beckhoff Automation in 2003, and subsequently turned over to an independent organization known as the EtherCAT® Technology Group, EtherCAT® has since become one of the most widely used industrial Ethernet protocols in the world.

.. seealso:: A comprehensive introduction to EtherCAT® technology can be found at https://www.acontis.com/en/what-is-EtherCAT-communication-protocol.html.

The EC-Monitor - Features
*************************


Protected version
*****************

The |Product| software is available in different protected versions:

Protected
    Binary with MAC protection
Unrestricted
    Binary without MAC protection
Source
    Source code

The protected version will automatically stop after about 30 minutes of continuous operation. In order to remove this restriction a valid runtime license key is required. The runtime license protection is based on the MAC address of the Ethernet controller used for the EtherCAT® protocol. With a valid License Key the protected version will automatically become an unrestricted version.

Licensing procedure for Development Licenses
============================================

#. Installation of EC-Monitor protected version
#. Determine the MAC Address by calling :cpp:func:`emonGetSrcMacAddress` or from a sticker applied on the hardware near the Ethernet controller
#. Send an Email with the subject "**Development License Key Request, Commission** *your commission number*" with the MAC address to sales@acontis.com
#. Acontis will create the license keys and return them in a **License Key Text File (CSV format)**.

   .. code-block:: none

       Number;MAC Address;License Key
       1;00-00-5A-11-77-FE;DA1099F2-15C249E9-54327FBC
       2;64-31-50-80-20-4E;1B7C1F86-D08E40A8-4F96F2BA

#. Activate the License Key by calling :cpp:func:`emonSetLicenseKey` with the license key that corresponds to the MAC address on the hardware and check the return code. The license key is 26 characters long.

   .. code-block:: cpp
   
       dwRes = emonSetLicenseKey(0, "DA1099F2-15C249E9-54327FBC");

Licensing procedure for Runtime Licenses
========================================

#. Installation of EC-Monitor protected version
#. Determine the MAC Address by calling :cpp:func:`emonGetSrcMacAddress` or from a sticker applied on the hardware near the Ethernet controller
#. Provide the MAC Addresses and numbers from **previously ordered and unused runtime license stickers** in a text file to acontis as described in the example below. Please use a separate line for each runtime license sticker number and MAC Address.

   .. code-block:: none
   
       S/N; MAC Address
       100-105-1-1/1603310001;00-00-5A-11-77-FE  
       100-105-1-1/1603310002;64-31-50-80-20-4E

#. Send an Email with the subject "**Runtime License Key Request, Commission** *your commission number*" with the MAC address to sales@acontis.com
#. Acontis will create the license keys and return them in a **License Key Text File (CSV format)**.

   .. code-block:: none  
   
       Number;MAC Address;License Key
       1;00-00-5A-11-77-FE;DA1099F2-15C249E9-54327FBC    
       2;64-31-50-80-20-4E;1B7C1F86-D08E40A8-4F96F2BA

#. Activate the License Key by calling :cpp:func:`emonSetLicenseKey` with the license key that corresponds to the MAC address on the hardware and check the return code.

   .. code-block:: cpp
   
       dwRes = emonSetLicenseKey(0, "DA1099F2-15C249E9-54327FBC");

.. include:: ../../Common/license.rst