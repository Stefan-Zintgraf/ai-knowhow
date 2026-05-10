Notifications
*************

Notification handler
====================

The application can register a notification handler using :cpp:func:`esRegisterClient` for notifications as described below.

A further important rule exists due to the fact that this callback function is usually called in the context of the EC-Simulator stack timer thread. As the whole EtherCAT operation is blocked while calling this function the notification handler must not use much CPU time or even call operating system functions that may block.
Time consuming operations should be executed in separate application threads.

Data structure filled with detailed information about the according notification:

.. doxygenstruct:: EC_T_NOTIFYPARMS
    :members:

EC_NOTIFY_SLAVE_PRESENCE
========================

This notification is given, if slave appears or disappears from the network.

This notification is enabled by default.

.. emNotify:: EC_NOTIFY_SLAVE_PRESENCE
    :pbyInBuf: Pointer to EC_T_SLAVE_PRESENCE_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Disconnecting the slave from the network, powering it off or a bad connection will generate this notification.

.. doxygenstruct:: EC_T_SLAVE_PRESENCE_NTFY_DESC
    :members:

EC_NOTIFY_SLAVE_STATECHANGED
============================

This notification is given, when a slave changed its EtherCAT state. This notification is disabled by default.

.. emNotify:: EC_NOTIFY_SLAVES_STATECHANGED
    :pbyInBuf: Pointer to EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :members:

EC_NOTIFY_HC_TOPOCHGDONE
========================

This notification is given by eUsrJob_SimulatorTimer when the topology changes.

.. emNotify:: EC_NOTIFY_HC_TOPOCHGDONE

.. seealso:: :cpp:func:`esPowerSlave` , :cpp:func:`esDisconnectPort` , :cpp:func:`esConnectPorts`


EC_NOTIFY_SLAVE_ERROR_STATUS_INFO
=================================

This notification is given, when the Error bit on the specific slave is set or cleared Detailed error information is stored in structure :cpp:struct:`EC_T_SLAVE_ERROR_INFO_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_SLAVE_ERROR_INFO_DESC
    :members:

..  EC_NOTIFY_STATUS_SLAVE_ERROR
..  ============================
..  EC_NOTIFY_MBOXRCV
..  =================
..
..  EC_NOTIFY_ETH_LINK_CONNECTED
..  ============================
..
..  EC_NOTIFY_ETH_LINK_NOT_CONNECTED
..  ================================


EC_NOTIFY_EEPROM_OPERATION
==========================

This notification is given, when a slave EEPROM is written by the master.

.. emNotify:: EC_NOTIFY_EEPROM_OPERATION
    :pbyInBuf: Pointer to EC_T_EEPROM_OPERATION_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_EEPROM_OPERATION_NTFY_DESC
    :members:

.. doxygenenum:: EC_T_EEPROM_OPERATION_TYPE


esNotifyApp
===========

.. doxygenfunction:: esNotifyApp
