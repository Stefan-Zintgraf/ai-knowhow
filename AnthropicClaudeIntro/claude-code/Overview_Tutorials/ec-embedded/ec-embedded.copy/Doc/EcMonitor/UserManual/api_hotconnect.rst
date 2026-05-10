***********
Hot Connect
***********

emonHCGetNumGroupMembers
************************

.. doxygenfunction:: emonHCGetNumGroupMembers

emonHCGetSlaveIdsOfGroup
************************

.. doxygenfunction:: emonHCGetSlaveIdsOfGroup

emonNotify - EC_NOTIFY_HC_DETECTADDGROUPS
*****************************************

This notification is raised when HotConnect group detection is finished, after slave addition.

.. emonNotify:: EC_NOTIFY_HC_DETECTADDGROUPS
    :pbyInBuf: pointer to notification descriptor EC_T_HC_DETECTALLGROUP_NTFY_DESC 
    :dwInBufSize: sizeof(EC_T_HC_DETECTALLGROUP_NTFY_DESC)
    
.. doxygenstruct:: EC_T_HC_DETECTALLGROUP_NTFY_DESC
    :members:
    
emonNotify - EC_NOTIFY_HC_PROBEALLGROUPS
****************************************

This notification is raised when HotConnect Group Detection is finished, after Slave Disappearance.

.. emonNotify:: EC_NOTIFY_HC_PROBEALLGROUPS
    :pbyInBuf: pointer to notification descriptor EC_T_HC_DETECTALLGROUP_NTFY_DESC 
    :dwInBufSize: sizeof(EC_T_HC_DETECTALLGROUP_NTFY_DESC)
    
.. cpp:alias:: EC_T_HC_DETECTALLGROUP_NTFY_DESC
    :maxdepth: 0

emonNotify - EC_NOTIFY_HC_TOPOCHGDONE
*************************************

This notification is raised when HotConnect has completely processed a topology change.

.. emonNotify:: EC_NOTIFY_HC_TOPOCHGDONE
    :pbyInBuf: Pointer to EC_T_DWORD (EC_E_NOERROR on success, Error code otherwise)
    :dwInBufSize: sizeof(EC_T_DWORD)
    
The notification is raised when the slaves reached the current bus state.