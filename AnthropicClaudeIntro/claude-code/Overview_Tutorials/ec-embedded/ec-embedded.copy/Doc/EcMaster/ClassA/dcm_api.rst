******************
Programmer's Guide
******************

emDcmConfigure
**************

.. doxygenfunction:: ecatDcmConfigure
    :outline:

.. doxygenfunction:: emDcmConfigure

.. doxygenstruct:: EC_T_DCM_CONFIG
    :members:

.. doxygenenum:: EC_T_DCM_MODE

.. doxygenstruct:: EC_T_DCM_CONFIG_BUSSHIFT
    :members:

.. doxygenstruct:: EC_T_DCM_CONFIG_MASTERSHIFT
    :members:

.. doxygenstruct:: EC_T_DCM_CONFIG_LINKLAYERREFCLOCK
    :members:

.. doxygenstruct:: EC_T_DCM_CONFIG_MASTERREFCLOCK
    :members:
    
.. doxygenstruct:: EC_T_DCM_CONFIG_DCX
    :outline:

Contains the configuration information for the DCX external synchronization mode. 

.. seealso:: Feature Pack "External Synchronization" for further details.

.. doxygenstruct:: EC_T_DC_STARTTIME_CB_DESC
    :members:
  
.. doxygentypedef:: EC_PF_DC_STARTTIME_CB

emDcmGetStatus
**************

.. doxygenfunction:: ecatDcmGetStatus
    :outline:

.. doxygenfunction:: emDcmGetStatus

emDcmResetStatus
****************

.. doxygenfunction:: ecatDcmResetStatus
    :outline:

.. doxygenfunction:: emDcmResetStatus

emDcmGetBusShiftConfigured
**************************

.. doxygenfunction:: ecatDcmGetBusShiftConfigured
    :outline:

.. doxygenfunction:: emDcmGetBusShiftConfigured

emDcmGetLog
***********

.. doxygenfunction:: ecatDcmGetLog
    :outline:

.. doxygenfunction:: emDcmGetLog

.. seealso:: :ref:`dcm_technical:Controller adjustment` for content description of pszLog

emIoControl - EC_IOCTL_DCM_GET_LOG
**********************************

Get logging information from the DCM controller.

.. emIoControl:: EC_IOCTL_DCM_GET_LOG
    :pbyOutBuf: Pointer to struct EC_T_DCM_LOG
    :dwOutBufSize: Size of the output buffer in bytes
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer pbyOutBuf
    
.. doxygenstruct:: EC_T_DCM_LOG
    :members:

emDcmShowStatus
***************

.. doxygenfunction:: ecatDcmShowStatus
    :outline:

.. doxygenfunction:: emDcmShowStatus

emDcmGetAdjust
**************

.. doxygenfunction:: ecatDcmGetAdjust
    :outline:

.. doxygenfunction:: emDcmGetAdjust

DCM specific error codes
************************

.. datatemplate:xml:: EC_ERROR_CODES_DCM
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

Notifications
*************

At startup the master raises the notifications :ref:`dc_api:emNotify - EC_NOTIFY_DC_SLV_SYNC`, :ref:`dc_api:emNotify - EC_NOTIFY_DC_STATUS` and :ref:`dcm_api:emNotify - EC_NOTIFY_DCM_SYNC` at master state transition from INIT to PREOP. 

The order is typically as follows ( :ref:`dcm_api:emNotify - EC_NOTIFY_DCM_SYNC` may be before or after reaching PREOP):

EC_NOTIFY_STATECHANGED(INIT)[...]

EC_NOTIFY_DC_SLV_SYNC [...]

EC_NOTIFY_DC_STATUS [...]

[EC_NOTIFY_DCM_SYNC] [...]

EC_NOTIFY_STATECHANGED(PREOP) [...]

[EC_NOTIFY_DCM_SYNC] [...]

EC_NOTIFY_STATECHANGED(SAFEOP) [...]

EC_NOTIFY_STATECHANGED(OP) [...]

emNotify - EC_NOTIFY_DCM_SYNC
*****************************

DCM InSync notification.

This notification is enabled by default. 

.. emNotify:: EC_NOTIFY_DCM_SYNC
    :pbyInBuf: pointer to notification descriptor EC_T_DCM_SYNC_NTFY_DESC
    :dwInBufSize: sizeof(EC_T_DCM_SYNC_NTFY_DESC).

.. doxygenstruct:: EC_T_DCM_SYNC_NTFY_DESC
    :members:

.. seealso:: emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED in the `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__ documentation for how controls the deactivation
