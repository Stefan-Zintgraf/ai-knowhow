******************
Programmer’s Guide
******************

Configuration
*************

To activate redundancy support, the EC-Master Stack has to be configured additionally with a second Network Interface. This is done by the parameter :cpp:member:`EC_T_INIT_MASTER_PARMS::pLinkParmsRed` while initializing the stack by aims of the command :cpp:func:`emInitMaster`.

.. doxygenfunction:: emInitMaster
  :outline:

.. doxygenstruct:: EC_T_INIT_MASTER_PARMS
    :members: pLinkParmsRed
    
emIoControl - EC_IOCTL_SB_SET_RED_ENHANCED_LINE_CROSSED_DETECTION_ENABLED
=========================================================================

Enable or disable the enhanced line crossed detection if redundancy is configured.

.. emIoControl:: EC_IOCTL_SB_SET_RED_ENHANCED_LINE_CROSSED_DETECTION_ENABLED
    :pbyInBuf:  Pointer to EC_T_BOOL. If value is EC_TRUE enhanced line crossed detection is enabled, if EC_FALSE it is not.
    :dwInBufSize: Should be set to sizeof(EC_T_BOOL).
    
The line crossed detection is restricted by using redundancy. Only the simple detection works per default. No precise line crossed location will be notified.

Enabling the enhanced line crossed detection with this IOCTL permit the EC-Master to give more precise information about detected line crossed. During bus scans triggered by topology change, the EC-Master stack will close the redundancy link. This generate a controlled line break. Under this condition the EC-Master stack is able to detect all the line crossed. To achieve this, the Real-time Ethernet Driver has to support ``EC_LINKIOCTL_SET_FORCEDISCONNECTION``. At this stage only the `emllIntelGbe` Real-time Ethernet Driver supports this IOCTL.

emIoControl - EC_IOCTL_SB_SET_JUNCTION_REDUNDANCY_MODE
======================================================

Set junction redundancy mode 

.. emIoControl:: EC_IOCTL_SB_SET_JUNCTION_REDUNDANCY_MODE
    :pbyInBuf: Pointer to value of EC_T_JUNCTION_REDUNDANCY_MODE 
    :dwInBufSize: Should be set to sizeof(EC_T_JUNCTION_REDUNDANCY_MODE)

.. doxygenenum:: EC_T_JUNCTION_REDUNDANCY_MODE
    
Enabling the junction redundancy support will generate :ref:`api:emNotify - EC_NOTIFY_JUNCTION_RED_CHANGE` in case of junction redundancy status change is detected.
In case of junction redundancy line break, the SubDevices connected at port B are connected backward. This would generate an ``EC_NOTIFY_LINE_CROSSED`` if this IOCTL is not called before.

Enabling the junction redundancy support will generate :ref:`api:emNotify - EC_NOTIFY_JUNCTION_RED_CHANGE` in case of junction redundancy line break is detected.
 
In the Disabled Mode, Line break will lead to an ``EC_NOTIFY_LINE_CROSSED`` notification, because the SubDevices connected at port B are connected backward. 
In the Automatic Mode, the junction connection are detected if present during startup. Line break can notified afterwards. 

In the Strict Mode, the junction redundancy ports have to be explicitly defined using the following sequence instead of :cpp:func:`emConfigureNetwork`:

#. :cpp:func:`emConfigLoad`
#. :cpp:func:`emConfigAddJunctionRedundancyConnection`
#. :cpp:func:`emConfigApply`

In this mode, the line break can be notified during the startup. 

emConfigLoad
============

.. doxygenfunction:: ecatConfigLoad
    :outline:

.. doxygenfunction:: emConfigLoad

.. doxygenenum:: EC_T_CNF_TYPE

emConfigAddJunctionRedundancyConnection
=======================================

.. doxygenfunction:: ecatConfigAddJunctionRedundancyConnection
  :outline:

.. doxygenfunction:: emConfigAddJunctionRedundancyConnection

.. figure:: ../Media/cable-red_red-port.png
    :alt:

emConfigApply
=============  

.. doxygenfunction:: ecatConfigApply
    :outline:

.. doxygenfunction:: emConfigApply
    
Polling status information from the EC-Master Stack
***************************************************

emGetNumConnectedSlavesMain
===========================

.. doxygenfunction:: ecatGetNumConnectedSlavesMain
    :outline:

.. doxygenfunction:: emGetNumConnectedSlavesMain

emGetNumConnectedSlavesRed
==========================

.. doxygenfunction:: ecatGetNumConnectedSlavesRed
    :outline:

.. doxygenfunction:: emGetNumConnectedSlavesRed

emIoControl - EC_IOCTL_IS_MAIN_LINK_CONNECTED
=============================================

Determine whether main link is connected.

.. emIoControl:: EC_IOCTL_IS_MAIN_LINK_CONNECTED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE link is connected, if EC_FALSE it is not.
    :dwOutBufSize: Should be set to sizeof(EC_T_DWORD)
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

emIoControl - EC_IOCTL_IS_RED_LINK_CONNECTED
============================================

Determine whether redundancy link is connected.

.. emIoControl:: EC_IOCTL_IS_RED_LINK_CONNECTED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE link is connected, if EC_FALSE it is not.
    :dwOutBufSize: Should be set to sizeof(EC_T_DWORD)
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

Receiving notifications
***********************

Following notifications are defined for redundancy support.

emNotify - EC_NOTIFY_RED_LINEBRK
================================

Every time the EC-Master detects a line break this error code will be signaled once to the application.

How many SubDevices are on the main interface and how many are on the redundancy interface is stored in structure :cpp:struct:`EC_T_RED_CHANGE_DESC` of the union element RedChangeDes:

.. doxygenstruct:: EC_T_RED_CHANGE_DESC
    :members:

emNotify - EC_NOTIFY_RED_LINEFIXED
==================================

Every time the EC-Master recovers from a line break this code will be signaled once to the application.
How many SubDevices are on the main interface and how many are on the redundancy interface is stored in structure :cpp:struct:`EC_T_RED_CHANGE_DESC` of the union element RedChangeDes:

.. cpp:alias:: EC_T_RED_CHANGE_DESC
    :maxdepth: 0

emNotify - EC_NOTIFY_JUNCTION_RED_CHANGE
========================================

If a SubDevice is detected with port 0 not connected, this error code will be signaled to the application. Either due to a cabling error or a line break in the junction redundancy.
This notification is disabled by default.

.. doxygenstruct:: EC_T_JUNCTION_RED_CHANGE_DESC 
    :members:

.. doxygenstruct:: EC_T_SLAVE_PROP 
    :members: