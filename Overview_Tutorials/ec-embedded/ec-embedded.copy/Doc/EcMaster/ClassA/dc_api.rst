******************
Programmer's Guide
******************
 
emDcConfigure
*************
.. doxygenfunction:: ecatDcConfigure
    :outline:

.. doxygenfunction:: emDcConfigure

.. doxygenstruct:: EC_T_DC_CONFIGURE
    :members:
    
.. seealso:: Chapter "Drift Compensation" of the ETG Document "ESC Datasheet Section 1 - Technology"

emDcIsEnabled
*************

.. doxygenfunction:: ecatDcIsEnabled
    :outline:

.. doxygenfunction:: emDcIsEnabled

emGetBusTime
************

.. doxygenfunction:: ecatGetBusTime
    :outline:

.. doxygenfunction:: emGetBusTime
 
emDcContDelayCompEnable
***********************

.. doxygenfunction:: ecatDcContDelayCompEnable
    :outline:

.. doxygenfunction:: emDcContDelayCompEnable
 
emDcContDelayCompDisable
************************

.. doxygenfunction:: ecatDcContDelayCompDisable
    :outline:

.. doxygenfunction:: emDcContDelayCompDisable

emIoControl - EC_IOCTL_DC_SLV_SYNC_STATUS_GET
*********************************************

Get the last generated :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC` notification.

.. emIoControl:: EC_IOCTL_DC_SLV_SYNC_STATUS_GET
    :pbyOutBuf: Pointer to EC_T_DC_SYNC_NTFY_DESC data type
    :dwOutBufSize: Size of the output buffer in bytes
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer pbyOutBuf

.. seealso:: :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC` describes :cpp:struct:`EC_T_DC_SYNC_NTFY_DESC`
 
emIoControl - EC_IOCTL_DC_SETSYNCSTARTOFFSET
***************************************************

Set the safety offset applied to the "set DC start time" InitCmd during the PS transition.

.. emIoControl:: EC_IOCTL_DC_SETSYNCSTARTOFFSET
    :pbyInBuf: Pointer to EC_T_DC_STARTCYCSAFETY_DESC data type
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_DC_STARTCYCSAFETY_DESC
    :members:

Default: 50000000ns

emIoControl - EC_IOCTL_DC_FIRST_DC_SLV_AS_REF_CLOCK
***************************************************

Enable or disable the usage of the first DC slave on bus overriding the configured reference clock.

.. emIoControl:: EC_IOCTL_DC_FIRST_DC_SLV_AS_REF_CLOCK
    :pbyInBuf: pointer to EC_T_BOOL. EC_FALSE: disable, EC_TRUE: enable.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emFindInpVarByName - "Inputs.BusTime"
*************************************

The DC system time (written to ESC register 0x0910) is part of the process data with name "Inputs.BusTime".

.. doxygenfunction:: ecatFindInpVarByName
    :outline:

.. doxygenfunction:: emFindInpVarByName
    :no-link:
    :outline:

.. seealso:: :cpp:func:`emFindInpVarByName` in the `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__  documentation

emIoControl - EC_IOCTL_DC_ENABLE_ALL_DC_SLV
*******************************************

Enable or disable the usage of DC at all supporting slaves on bus overriding the configured settings.
Perhaps :ref:`dc_api:emIoControl - EC_IOCTL_DC_FIRST_DC_SLV_AS_REF_CLOCK` is necessary to set the reference clock at an allowed position.

.. emIoControl:: EC_IOCTL_DC_ENABLE_ALL_DC_SLV
    :pbyInBuf: pointer to EC_T_BOOL. EC_FALSE: disable, EC_TRUE: enable.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emNotify - EC_NOTIFY_REFCLOCK_PRESENCE
**************************************

Distributed clocks reference clock presence notification. It will be received before :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC` as soon as reference clock was found on bus or removed from bus.

This notification is disabled by default.

.. emNotify:: EC_NOTIFY_REFCLOCK_PRESENCE
    :pbyInBuf: pointer to notification descriptor EC_T_REFCLOCK_PRESENCE_NTFY_DESC
    :dwInBufSize: sizeof(EC_T_REFCLOCK_PRESENCE_NTFY_DESC)

.. doxygenstruct:: EC_T_REFCLOCK_PRESENCE_NTFY_DESC
    :members:

.. seealso:: emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED in the `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__ documentation for how to control the activation

emNotify - EC_NOTIFY_DC_STATUS
******************************

Distributed clocks status notification. It will be received after :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC` as soon as DC is initialized or topology change was done. After topology was changed it may be received without :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC` if slaves did not get out of sync.

If EC_E_NOERROR is returned and window monitoring is enabled, all slaves are in SYNC

.. emNotify:: EC_NOTIFY_DC_STATUS
    :pbyInBuf: Pointer to EC_T_DWORD (EC_E_NOERROR on success, Error code otherwise)
    :dwInBufSize: sizeof(EC_T_DWORD)

.. seealso:: emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED in the `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__ documentation for how to control the deactivation
 
emNotify - EC_NOTIFY_DC_SLV_SYNC
********************************

DC slave synchronization notification. Every time the slaves are coming in sync or getting out of sync the clients will be notified here.
The notification is raised in any case if any DC slaves are configured. Slaves can only be out of sync if :ref:`dc_technical:Sync Window Monitoring` is enabled otherwise they are considered in sync.

This notification is enabled by default. 

.. emNotify:: EC_NOTIFY_DC_SLV_SYNC
    :pbyInBuf: pointer to notification descriptor EC_T_DC_SYNC_NTFY_DESC
    :dwInBufSize: sizeof(EC_T_DC_SYNC_NTFY_DESC)
   
.. doxygenstruct:: EC_T_DC_SYNC_NTFY_DESC
    :members:

.. seealso:: 
    - :cpp:func:`emDcConfigure`
    - emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED in the `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__ documentation for how to control the deactivation
