******************************
Generic notification interface
******************************

One of the parameters the client has to set when registering with the |Product| is a generic notification callback function ( :cpp:func:`emonNotify`). This function is called every time an event occurs about which the client needs to be informed.

Within this callback function the client must not call any active EtherCAT® functions which finally would lead to send EtherCAT® commands (e.g. initiation of mailbox transfers, starting/stopping the master, sending raw commands). In such cases the behavior is undefined. Only EtherCAT® functions which are explicitly marked to be callable within :cpp:func:`emonNotify` may be called.

This callback function is usually called in the context of the |Product| timer thread or the EtherCAT® Real-time Ethernet Driver receiver thread. To avoid dead-lock situations the notification callback handler may not use mutex semaphores. 

As the whole EtherCAT® operation is blocked while calling this function the error handling must not use much CPU time or even call operating system functions that may block. Usually the error handling will be done in a separate application thread.

Notification callback
*********************

.. cpp:alias:: EC_PF_NOTIFY

.. doxygenstruct:: EC_T_NOTIFYPARMS
    :members:

emonNotifyApp
*************

By calling this function the generic notification callback function setup by :cpp:func:`emonRegisterClient` is called.

.. doxygenfunction:: emonNotifyApp

The maximum value for dwCode is defined by :c:macro:`EC_NOTIFY_APP_MAX_CODE`

Enable/Disable notifications
****************************

All notifications can be enabled or disabled. By default, all notifications are enabled except for:

.. doxygenpage:: EC_NOTIFY_DISABLED_BY_DEFAULT
    :content-only:

emonIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED
=================================================

Set notification enabled state. With :cpp:member:`EC_T_SET_NOTIFICATION_ENABLED_PARMS::dwCode` set to :c:macro:`EC_ALL_NOTIFICATIONS`, all notifications can be changed at once. 
:cpp:member:`EC_T_SET_NOTIFICATION_ENABLED_PARMS::dwEnabled` set to :c:macro:`EC_NOTIFICATION_DEFAULT`, resets to default.

.. emonIoControl:: EC_IOCTL_SET_NOTIFICATION_ENABLED
    :pbyInBuf: Pointer to EC_T_SET_NOTIFICATION_ENABLED_PARMS.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SET_NOTIFICATION_ENABLED_PARMS
    :members:

.. datatemplate:xml:: EC_SET_NOTIFICATION_ENABLED
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

emonIoControl - EC_IOCTL_GET_NOTIFICATION_ENABLED
=================================================

Get notification enabled state.

.. emonIoControl:: EC_IOCTL_GET_NOTIFICATION_ENABLED
    :pbyInBuf: Pointer to EC_T_GET_NOTIFICATION_ENABLED_PARMS.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to EC_T_BOOL to carry out current enable set. 
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes. 
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer. 

.. doxygenstruct:: EC_T_GET_NOTIFICATION_ENABLED_PARMS
    :members:

Status notifications
********************
..
    .. doxygenstruct:: EC_T_NOTIFICATION_DESC
        :members:

emonNotify - EC_NOTIFY_STATECHANGED
===================================

Notification about a change in the master's operational state.

.. emonNotify:: EC_NOTIFY_STATECHANGED
    :pbyInBuf: Pointer to data of type EC_T_STATECHANGE which contains the old and the new master operational state.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_STATECHANGE
    :members:

emonNotify - EC_NOTIFY_SB_STATUS
================================

Scan bus status notification.

.. emonNotify:: EC_NOTIFY_SB_STATUS
    :pbyInBuf: Pointer to EC_T_SB_STATUS_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_SB_STATUS_NTFY_DESC
    :members:

emonNotify - EC_NOTIFY_SB_MISMATCH
==================================

This notification is triggered when the bus scan detects a discrepancy between connected slaves and configuration due to unexpected slaves or missing mandatory slaves.
In case of permanent frame loss no slaves can be found although the slaves are connected.

.. emonNotify:: EC_NOTIFY_SB_MISMATCH
    :pbyInBuf: Pointer to EC_T_SB_MISMATCH_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SB_MISMATCH_DESC
    :members:

emonNotify - EC_NOTIFY_HC_TOPOCHGDONE
=====================================

This notification is triggered when topology change has completely processed.

.. emonNotify:: EC_NOTIFY_HC_TOPOCHGDONE
    :pbyInBuf: Pointer to EC_T_DWORD (EC_E_NOERROR on success, Error code otherwise) 
    :dwInBufSize: sizeof(EC_T_DWORD). 

emonNotify - EC_NOTIFY_SLAVE_PRESENCE
=====================================

This notification is given, if slave appears or disappears from the network.

.. emonNotify:: EC_NOTIFY_SLAVE_PRESENCE
    :pbyInBuf: Pointer to EC_T_SLAVE_PRESENCE_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
Disconnecting the slave from the network, powering it off or a bad connection can produce this notification.

.. doxygenstruct:: EC_T_SLAVE_PRESENCE_NTFY_DESC
    :members:

emonNotify - EC_NOTIFY_SLAVE_STATECHANGED
=========================================

This notification is triggered when a slave has changed its EtherCAT® state. This notification is disabled by default.

.. emonNotify:: EC_NOTIFY_SLAVE_STATECHANGED
    :pbyInBuf: Pointer to EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :members:

.. seealso:: :ref:`notification:emonIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` to enable notification.

emonNotify - EC_NOTIFY_SLAVE_REGISTER_TRANSFER
==============================================

This notification is triggered when a slave register transfer is completed. 

To avoid excessive triggering of the notification, registers that are read by the EtherCAT® master at regular intervals are not notified. These are the following registers:

.. doxygenpage:: FILTER_NotifySlaveRegisterTransfer
    :content-only:

This notification is disabled by default.

.. emonNotify:: EC_NOTIFY_SLAVE_REGISTER_TRANSFER
    :pbyInBuf: Pointer to EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
    :members:

.. seealso:: :ref:`notification:emonIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` to enable notification.

Error notifications
*******************

For each error an error ID (error code) will be defined. This error ID will be used as the notification code when :cpp:func:`emonNotify` is called. In addition to this notification code the second parameter given to :cpp:func:`emonNotify` contains a pointer to an error notification descriptor of type :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. This error notification descriptor contains detailed information about the error.

.. doxygenstruct:: EC_T_ERROR_NOTIFICATION_DESC
    :members:

If the pointer to this descriptor exists the detailed error information (e.g. information about the slave) is stored in the appropriate structure of a union. These error information structures are described in the following sections.

..
    The |Product| will call :cpp:func:`emonNotify` every time an error is detected. In some cases this will lead to calling this function in every EtherCAT® cycle (e.g. if there is no physical connection to the slaves). Using the control interface :ref:`api:emonIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` it is possible to determine which errors shall be signaled and which not.

emonNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL
==================================================

When processing cyclic frames the EtherCAT® master checks whether all slaves are still in OPERATIONAL state. If at least one slave device is not OPERATIONAL this error will be indicated.

emonNotify - EC_NOTIFY_ALL_DEVICES_OPERATIONAL
==============================================

When processing cyclic frames the EtherCAT® master checks whether all slaves are still in OPERATIONAL state. This will be notified after :ref:`notification:emonNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL` and all the slaves are back in OPERATIONAL state.

emonNotify - EC_NOTIFY_CLIENTREGISTRATION_DROPPED
=================================================

This notification will be indicated if the client registration was dropped because :cpp:func:`emonConfigureNetwork` was called by another thread.

.. code-block:: cpp
    
    EC_T_DWORD dwDeinitForConfiguration; /* 0 = terminating Master, 1 = restarting Master */

emonNotify - EC_NOTIFY_CYCCMD_WKC_ERROR
=======================================

To update the process data some EtherCAT® commands will be sent cyclically by the external master. These commands will address one or multiple slaves. These EtherCAT® commands contain a working counter which has to be incremented by each slave that is addressed. The working counter will be checked after the EtherCAT® command is received by the monitor.
If the expected working counter will not match to the working counter of the received command the error `EC_NOTIFY_CYCCMD_WKC_ERROR` will be indicated. The working counter value expected by the monitor is determined by the EtherCAT® configuration (XML) file for each cyclic EtherCAT® command (section Config/Cyclic/Frame/Cmd/Cnt).
Detailed error information are stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_WKCERR_DESC
    :members:

.. cpp:alias:: EC_T_SLAVE_PROP
    :maxdepth: 2

..
    .. seealso::
        - :ref:`software-integration:Cyclic cmd WKC validation`
        - :ref:`software-integration:Working Counter (WKC) State in Diagnosis Image`

emonNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR
===========================================

This notification will be indicated if the actually received Ethernet frame does not match to the frame expected or if a expected frame was not received.

.. doxygenstruct:: EC_T_FRAME_RSPERR_DESC
    :members:

.. doxygenenum:: EC_T_FRAME_RSPERR_TYPE

emonNotify - EC_NOTIFY_STATUS_SLAVE_ERROR
=========================================

When processing cyclic frames, the |Product| checks whether the ERROR bit in the AL-STATUS register is set for at least one slave. In this case, this notification is triggered.
If the EtherCAT® master determines the error information of the slave(s) signal an error, another notification :ref:`notification:emonNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO` with more precise error information is triggered.

emonNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO
==============================================

This notification will be indicated if the EtherCAT® master reads the AL-STATUS and AL-STATUS-CODE registers and the slave signals an error in them. Detailed error information is stored in structure :cpp:struct:`EC_T_SLAVE_ERROR_INFO_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_SLAVE_ERROR_INFO_DESC
    :members:

emonNotify - EC_NOTIFY_PDIWATCHDOG
==================================

This notification will be indicated every time a PDI watchdog error is detected. Detailed error information is stored in structure :cpp:struct:`EC_T_PDIWATCHDOG_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_PDIWATCHDOG_DESC
    :members:

emonNotify - EC_NOTIFY_COMMUNICATION_TIMEOUT
============================================

This notification will be indicated if the |Product| does not detect any EtherCAT® communication on the Ethernet tap for a parameterizable timeout.
The descriptor of the notification contains information on which port of the Ethernet tap the timeout occurred.

.. doxygenstruct:: EC_T_COMMUNICATION_TIMEOUT_NTFY_DESC
    :members:

.. seealso:: :cpp:member:`EC_T_MONITOR_INIT_PARMS::dwCommunicationTimeoutMsec`

emonNotify - EC_NOTIFY_TAP_LINK_STATUS
======================================

This notification will be indicated if the link status between |Product| and Ethernet TAP device has changed.

.. doxygenstruct:: EC_T_TAP_LINK_STATUS_NTFY_DESC 
    :members:

