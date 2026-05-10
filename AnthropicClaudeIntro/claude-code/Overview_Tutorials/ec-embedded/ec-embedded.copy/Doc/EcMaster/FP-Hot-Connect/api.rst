********************************************
Application programming interface, reference
********************************************

emIoControl - EC_IOCTL_HC_SETMODE
*********************************

Configures the Hot-Connect mode. Can be called at any time after :cpp:func:`emInitMaster`, usually before :cpp:func:`emConfigureNetwork`, but not necessarily. If it is not called, the Hot-Connect instance operates in automatic mode :cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_automatic`.

.. emIoControl:: EC_IOCTL_HC_SETMODE
    :pbyInBuf: Pointer to EC_T_EHOTCONNECTMODE
    :dwInBufSize: sizeof(EC_T_EHOTCONNECTMODE)

Enumeration containing Hot-Connect modes of operation. The modes can be or’ed together within the call.

.. doxygenenum:: EC_T_EHOTCONNECTMODE
    
emIoControl - EC_IOCTL_HC_GETMODE
*********************************

Get the current Hot-Connect operating mode.

.. emIoControl:: EC_IOCTL_HC_GETMODE
    :pbyOutBuf: Pointer to EC_T_EHOTCONNECTMODE
    :dwOutBufSize: sizeof(EC_T_EHOTCONNECTMODE)
    :pdwNumOutData: Pointer to DWORD value carrying sizeof(EC_T_EHOTCONNECTMODE)
    
.. seealso:: :ref:`api:emIoControl - EC_IOCTL_HC_SETMODE`

emIoControl - EC_IOCTL_HC_CONFIGURETIMEOUTS
*******************************************

Configures the Timeout values used by Hot-Connect.

.. emIoControl:: EC_IOCTL_HC_CONFIGURETIMEOUTS
    :pbyInBuf: Pointer to EC_T_HC_CONFIGURETIMEOUTS_DESC
    :dwInBufSize: sizeof(EC_T_HC_CONFIGURETIMEOUTS_DESC)

.. doxygenstruct:: EC_T_HC_CONFIGURETIMEOUTS_DESC
    :members: 

emHCGetNumGroupMembers
**********************

.. doxygenfunction:: ecatHCGetNumGroupMembers
    :outline:

.. doxygenfunction:: emHCGetNumGroupMembers

emHCGetSlaveIdsOfGroup
**********************

.. doxygenfunction:: ecatHCGetSlaveIdsOfGroup
    :outline:

.. doxygenfunction:: emHCGetSlaveIdsOfGroup

emHCAcceptTopoChange
********************

.. doxygenfunction:: ecatHCAcceptTopoChange
    :outline:

.. doxygenfunction:: emHCAcceptTopoChange

emForceTopologyChange
*********************

.. doxygenfunction:: ecatForceTopologyChange
    :outline:

.. doxygenfunction:: emForceTopologyChange

emSetSlavePortState
*******************

.. doxygenfunction:: ecatSetSlavePortState
    :outline:

.. doxygenfunction:: emSetSlavePortState

emBlockNode
***********

.. doxygenfunction:: ecatBlockNode
    :outline:

.. doxygenfunction:: emBlockNode

emOpenBlockedPorts
******************

.. doxygenfunction:: ecatOpenBlockedPorts
    :outline:

.. doxygenfunction:: emOpenBlockedPorts

emNotify - EC_NOTIFY_HC_TOPOCHGDONE
***********************************

This notification is triggered when the Hot-Connect instances have fully processed a topology change. This means more precisely when the slaves have reached the current bus state.

.. emNotify:: EC_NOTIFY_HC_TOPOCHGDONE
    :pbyInBuf: Pointer to EC_T_DWORD (EC_E_NOERROR on success, Error code otherwise)
    :dwInBufSize: sizeof(EC_T_DWORD)

emNotify - EC_NOTIFY_HC_DETECTADDGROUPS
***************************************

This notification is triggered when the Hot-Connect group detection is completed after adding the slaves of a group.

.. emNotify:: EC_NOTIFY_HC_DETECTADDGROUPS
    :pbyInBuf: pointer to notification descriptor EC_T_HC_DETECTALLGROUP_NTFY_DESC 
    :dwInBufSize: sizeof(EC_T_HC_DETECTALLGROUP_NTFY_DESC)
    
.. doxygenstruct:: EC_T_HC_DETECTALLGROUP_NTFY_DESC
    :members:
    
emNotify - EC_NOTIFY_HC_PROBEALLGROUPS
**************************************

This notification is triggered when the Hot-Connect group detection is completed after a group disappears.

.. emNotify:: EC_NOTIFY_HC_PROBEALLGROUPS
    :pbyInBuf: pointer to notification descriptor EC_T_HC_DETECTALLGROUP_NTFY_DESC 
    :dwInBufSize: sizeof(EC_T_HC_DETECTALLGROUP_NTFY_DESC)
    
.. cpp:alias:: EC_T_HC_DETECTALLGROUP_NTFY_DESC
    :maxdepth: 0

emNotify - EC_NOTIFY_SB_STATUS
******************************

Scan bus status notification.

This notification is enabled by default. 

.. emNotify:: EC_NOTIFY_SB_STATUS
    :pbyInBuf: Pointer to EC_T_SB_STATUS_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_SB_STATUS_NTFY_DESC
    :members:

emNotify - EC_NOTIFY_SB_MISMATCH
********************************

This notification will be initiated if scan bus detects mismatch of connected slaves and configuration, due to unexpected slaves or missing mandatory slaves.

.. emNotify:: EC_NOTIFY_SB_MISMATCH
    :pbyInBuf: Pointer to EC_T_SB_MISMATCH_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

This notification is enabled by default. In case of permanent frame loss no slaves can be found although the slaves are connected.

.. doxygenstruct:: EC_T_SB_MISMATCH_DESC
    :members:

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
