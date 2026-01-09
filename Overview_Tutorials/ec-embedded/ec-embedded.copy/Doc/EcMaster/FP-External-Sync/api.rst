********************************************
Application programming interface, reference
********************************************

emDcmConfigure
**************

.. doxygenfunction:: ecatDcmConfigure
    :outline:

.. doxygenfunction:: emDcmConfigure

.. doxygenstruct:: EC_T_DCM_CONFIG
    :members:

.. doxygenstruct:: EC_T_DCM_CONFIG_DCX
    :members:

emDcxGetStatus
**************

.. doxygenfunction:: ecatDcxGetStatus
    :outline:

.. doxygenfunction:: emDcxGetStatus

Notifications
*************

At startup the EC-Master raises the notifications :c:macro:`EC_NOTIFY_DC_SLV_SYNC`, :c:macro:`EC_NOTIFY_DC_STATUS` and :c:macro:`EC_NOTIFY_DCM_SYNC`, :c:macro:`EC_NOTIFY_DCX_SYNC` at master state transition from INIT to PREOP. 

The order is typically as follows (:c:macro:`EC_NOTIFY_DCM_SYNC`, :c:macro:`EC_NOTIFY_DCX_SYNC` may be before or after reaching PREOP):

INIT
    :c:macro:`EC_NOTIFY_STATECHANGED`

    […]

    :c:macro:`EC_NOTIFY_DC_SLV_SYNC`

    […]

    :c:macro:`EC_NOTIFY_DC_STATUS`
    
    […]

    [ :c:macro:`EC_NOTIFY_DCM_SYNC` ]
    
    [ :c:macro:`EC_NOTIFY_DCX_SYNC` ]

PREOP
    :c:macro:`EC_NOTIFY_STATECHANGED`
    
    […]
    
    [ :c:macro:`EC_NOTIFY_DCM_SYNC` ]
    
    [ :c:macro:`EC_NOTIFY_DCX_SYNC` ]

SAFEOP
    :c:macro:`EC_NOTIFY_STATECHANGED`

OP
    :c:macro:`EC_NOTIFY_STATECHANGED`


emNotify – EC_NOTIFY_DCX_SYNC
=============================

.. emNotify:: EC_NOTIFY_DCX_SYNC
    :pbyInBuf: Pointer to notification descriptor EC_T_DCX_SYNC_NTFY_DESC
    :dwInBufSize: sizeof(EC_T_DCX_SYNC_NTFY_DESC). 

.. doxygenstruct:: EC_T_DCX_SYNC_NTFY_DESC
    :members:
