*****************
EtherCAT Bus Scan
*****************

The acontis EtherCAT Master stack supports scanning the EtherCAT Bus to determine which devices are available. If a configuration was provided the connected slaves are validated against the given ENI.

.. seealso:: :cpp:func:`emScanBus`

emIoControl - EC_IOCTL_SB_ENABLE
********************************

Enables Busscan support. 

.. emIoControl:: EC_IOCTL_SB_ENABLE
    :pbyInBuf: Pointer to Timeout Parameter Value in MSec (EC_T_DWORD). Timeout Parameter is used for timeout during Bus Topology determination.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
The Scanbus support is enabled by default.

emIoControl - EC_IOCTL_SB_RESTART
*********************************

This call will restart the bus scanning cycle. On completion the Notfication :ref:`api_busscan:emNotify - EC_NOTIFY_SB_STATUS` is given.

.. emIoControl:: EC_IOCTL_SB_RESTART

The timeout value given by :ref:`api_busscan:emIoControl - EC_IOCTL_SB_ENABLE` will be used.
This function may be called prior to running :cpp:func:`emConfigureNetwork`. In such a case a first bus scan will be executed before master configuration. This feature may be used to dynamically create or adjust the XML configuration file. When issuing this IoControl, the application has to take care :cpp:func:`emExecJob` is called cyclically to trigger master state machines, timers, send acyc and receive frames accordingly.

emIoControl - EC_IOCTL_SB_STATUS_GET
************************************

This call will get the status of the last bus scan.

.. emIoControl:: EC_IOCTL_SB_STATUS_GET
    :pbyOutBuf: Pointer to EC_T_SB_STATUS_NTFY_DESC.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.
    
.. seealso:: :ref:`api_busscan:emNotify - EC_NOTIFY_SB_STATUS`

emIoControl - EC_IOCTL_SB_SET_TOPOLOGY_CHANGED_DELAY
****************************************************

This call will set the topology changed delay value. The master will wait this duration in msec to react on appearing links in topology. The default value is 1000 ms.

.. emIoControl:: EC_IOCTL_SB_SET_TOPOLOGY_CHANGED_DELAY
    :pbyInBuf: Pointer to EC_T_DWORD containing the delay information in msec
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
emIoControl - EC_IOCTL_SB_SET_TOPOLOGY_CHANGED_DELAYS
*****************************************************

This call will set the topology changed delay values individually. The master will wait individual durations in msec (0 msec: disabled) for slave ports, main link and red link to react on appearing links in topology. The default value is 1000 ms.

.. emIoControl:: EC_IOCTL_SB_SET_TOPOLOGY_CHANGED_DELAYS
    :pbyInBuf: Pointer to EC_T_TOPOLOGY_CHANGED_DELAYS containing the delay information in msec
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_TOPOLOGY_CHANGED_DELAYS
    :members:
    
emIoControl - EC_IOCTL_SB_SET_ERROR_ON_CROSSED_LINES
****************************************************

This call will enable or disable bus mismatch if IN and OUT connectors are swapped. If enabled the swapped IN and OUT connectors will lead to bus mismatch.
By default swapped IN and OUT connectors will lead to bus mismatch.

.. emIoControl:: EC_IOCTL_SB_SET_ERROR_ON_CROSSED_LINES
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE swapped IN and OUT connectors will lead to bus mismatch, if set to EC_FALSE swapped IN and OUT connectors are tolerated.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
emIoControl - EC_IOCTL_SB_SET_ERROR_ON_LINEBREAK
************************************************

This call will enable or disable bus mismatch if a line is broken in a redundant network. If enabled, line breaks in cable or junction redundant networks will lead to bus mismatch.

.. emIoControl:: EC_IOCTL_SB_SET_ERROR_ON_LINEBREAK
    :pbyInBuf: Pointer to EC_T_BOOL. EC_TRUE: Return error code, EC_FALSE: Return no error.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes. 
    
Default: No error on line break.

Error codes:

- :cpp:struct:`EC_E_REDLINEBREAK`: Line break in a cable redundant network.
- :cpp:struct:`EC_E_JUNCTION_RED_LINE_BREAK`: Line break in a junction redundant network.

emIoControl - EC_IOCTL_SB_SET_TOPOLOGY_CHANGE_AUTO_MODE
*******************************************************

.. warning:: This documentation is preliminary and is subject to change

This call will enable or disable the automatical topology change mode. By default the automatical mode is enabled.

.. emIoControl:: EC_IOCTL_SB_SET_TOPOLOGY_CHANGE_AUTO_MODE
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE the automatical mode is enabled.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
In automatical mode, new slaves will be discovered automatically. In manual mode, after new slaves have been connected, a :ref:`api_busscan:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` notification will be given without opening the ports of the slaves on bus. When the application is able to handle the new slaves, it should call :ref:`api_busscan:emIoControl - EC_IOCTL_SB_ACCEPT_TOPOLOGY_CHANGE`

emIoControl - EC_IOCTL_SB_ACCEPT_TOPOLOGY_CHANGE
************************************************

.. warning:: This documentation is preliminary and is subject to change

This call will trigger a scan bus. On completion the Notfication :ref:`api_busscan:emNotify - EC_NOTIFY_SB_STATUS` is given.

.. emIoControl:: EC_IOCTL_SB_ACCEPT_TOPOLOGY_CHANGE

This function may be called after a :ref:`api_busscan:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` notification was given if the automatical topology change mode was previously disabled using :ref:`api_busscan:emIoControl - EC_IOCTL_SB_SET_TOPOLOGY_CHANGE_AUTO_MODE`.
During this scan bus the ports of the slaves will be (re)open and new slaves can be detected.
The timeout value given by :ref:`api_busscan:emIoControl - EC_IOCTL_SB_ENABLE` will be used. When issuing this IoControl, the application has to take care :cpp:func:`emExecJob` is called cyclically to trigger master state machines, timers, send acyc and receive frames accordingly.

emNotify - EC_NOTIFY_SB_STATUS
******************************

Scan bus status notification.

This notification is enabled by default. 

.. emNotify:: EC_NOTIFY_SB_STATUS
    :pbyInBuf: Pointer to EC_T_SB_STATUS_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_SB_STATUS_NTFY_DESC
    :members:
    
.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation
    
emNotify - EC_NOTIFY_SB_MISMATCH
********************************

This notification will be initiated if scan bus detects mismatch of connected slaves and configuration, due to unexpected slaves or missing mandatory slaves.

.. emNotify:: EC_NOTIFY_SB_MISMATCH
    :pbyInBuf: Pointer to EC_T_SB_MISMATCH_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

This notification is enabled by default. In case of permanent frame loss no slaves can be found although the slaves are connected.

.. doxygenstruct:: EC_T_SB_MISMATCH_DESC
    :members:
    
.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation
    
emNotify - EC_NOTIFY_SB_DUPLICATE_HC_NODE
*****************************************

Scan bus mismatch was detected while scan because of a duplicated slave(s).
An application get this notification if the there are two slaves on the network with the same product code, vendor ID and identification value (alias address or switch id).

.. emNotify:: EC_NOTIFY_SB_DUPLICATE_HC_NODE
    :pbyInBuf: Pointer to EC_T_SB_MISMATCH_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
The members of :cpp:struct:`EC_T_SB_MISMATCH_DESC` have the following meaning:

- :cpp:member:`EC_T_SB_MISMATCH_DESC::wCfgFixedAddress` Duplicated slave (config) station Address
- :cpp:member:`EC_T_SB_MISMATCH_DESC::wCfgAIncAddress` Duplicated slave (config)  Auto-Increment Address.
- :cpp:member:`EC_T_SB_MISMATCH_DESC::dwCfgVendorId` Duplicated slave (config)  Vendor ID
- :cpp:member:`EC_T_SB_MISMATCH_DESC::dwCfgProdCode` Duplicated slave (config)  Product code
- :cpp:member:`EC_T_SB_MISMATCH_DESC::dwCfgRevisionNo` Duplicated slave (config)  Revision Number
- :cpp:member:`EC_T_SB_MISMATCH_DESC::dwCfgSerialNo` Duplicated slave (config)  Serial Number


emNotify - EC_NOTIFY_SLAVE_PRESENCE
***********************************

This notification is given, if slave appears or disappears from the network.

This notification is enabled by default. 

.. emNotify:: EC_NOTIFY_SLAVE_PRESENCE
    :pbyInBuf: Pointer to EC_T_SLAVE_PRESENCE_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
Disconnecting the slave from the network, powering it off or a bad connection can produce this notification.

.. doxygenstruct:: EC_T_SLAVE_PRESENCE_NTFY_DESC
    :members:
    
.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation    
    
emNotify - EC_NOTIFY_SLAVES_PRESENCE
************************************

This notification collects notifications of the type :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE`
Notification is given either upon completion or when master status is changed, whichever comes first.
Disconnecting slaves from the network, turning them off, or having a bad connection can lead to this notification.

This notification is disabled by default. 

.. emNotify:: EC_NOTIFY_SLAVES_PRESENCE
    :pbyInBuf: Pointer to EC_T_SLAVES_PRESENCE_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVES_PRESENCE_NTFY_DESC
    :members:
    
.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED`
    
emNotify - EC_NOTIFY_LINE_CROSSED
**********************************

Cable swapping detected. All slaves' port 0 must lead to Master.

.. emNotify:: EC_NOTIFY_LINE_CROSSED
    :pbyInBuf: Pointer to EC_T_LINE_CROSSED_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_LINE_CROSSED_DESC
    :members:
    
emNotify - EC_NOTIFY_SLAVE_NOTSUPPORTED
***************************************

Is currently generated during Bus Scan if :cpp:func:`emConfigureNetwork` (GenOp/Preop) and a wrong category type is detected in the EEPROM. This notification should only print a log message or be ignored (Master print log message itself).

.. emNotify:: EC_NOTIFY_SLAVE_NOTSUPPORTED
    :pbyInBuf: Pointer to EC_T_ERROR_NOTIFICATION_DESC containing EC_T_SLAVE_NOTSUPPORTED_DESC.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_SLAVE_NOTSUPPORTED_DESC
    :members:
    
emNotify - EC_NOTIFY_FRAMELOSS_AFTER_SLAVE
******************************************

Is currently generated and automatically handled during :cpp:func:`emRescueScan` if opening port destroys communication (frameloss). This notification should only print a log message or be ignored.

.. emNotify:: EC_NOTIFY_FRAMELOSS_AFTER_SLAVE
    :pbyInBuf: Pointer to EC_T_ERROR_NOTIFICATION_DESC containing EC_T_FRAMELOSS_AFTER_SLAVE_NTFY_DESC.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_FRAMELOSS_AFTER_SLAVE_NTFY_DESC
    :members:
    
emNotify - Bus Scan notifications for Feature Packs
***************************************************

The notifications :c:macro:`EC_NOTIFY_RED_LINEBRK`, :c:macro:`EC_NOTIFY_RED_LINEFIXED` belong to the Feature Pack Redundancy.
The notifications :c:macro:`EC_NOTIFY_HC_DETECTADDGROUPS`, :c:macro:`EC_NOTIFY_HC_PROBEALLGROUPS` belong to the Feature Pack Hot Connect.

emIoControl - EC_IOCTL_SB_NOTIFY_UNEXPECTED_BUS_SLAVES
******************************************************

Specifies if unexpected bus slaves must be notified as bus mismatch.

.. emIoControl:: EC_IOCTL_SB_NOTIFY_UNEXPECTED_BUS_SLAVES
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE unexpected bus slaves on the network will be notified by EC_NOTIFY_SB_MISMATCH.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
emIsTopologyChangeDetected
**************************

.. doxygenfunction:: ecatIsTopologyChangeDetected
    :outline:

.. doxygenfunction:: emIsTopologyChangeDetected

emNotify - EC_NOTIFY_HC_TOPOCHGDONE
***********************************

This notification is raised when topology change has completely processed.

.. emNotify:: EC_NOTIFY_HC_TOPOCHGDONE
    :pbyInBuf: Pointer to EC_T_DWORD (EC_E_NOERROR on success, Error code otherwise) 
    :dwInBufSize: sizeof(EC_T_DWORD). 
    
The notification is raised when the slaves have been detected and DC initialized.

emIoControl - EC_IOCTL_SB_SET_NO_DC_SLAVES_AFTER_JUNCTION
*********************************************************

Declares that no DC slaves are located after junction

.. emIoControl:: EC_IOCTL_SB_SET_NO_DC_SLAVES_AFTER_JUNCTION
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE the hidden slave detection and the junction redundancy specific propagation delay measurement are not executed
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL if DC slaves are located in or after a junction redundancy segment will generate an undefined behavior.
