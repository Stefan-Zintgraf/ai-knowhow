******************************************************
Software Integration - Remote site (Remote API Client)
******************************************************

The Remote API Client is included to the master stack using application by following steps:

#. Link the Remote Client API lib to the Project
#. Make the Remote API Client DLL available to the Runtime environment of your application.
#. Include the necessary connect and disconnect calls to your client application.
#. Compile
#. Run

Example
*******

Here is an example for the Remote API Client:

.. EcMasterRasClientExample


.. dropdown:: First, a connection has to be added:

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-RAS\software-integration.h
        :start-after: DocumentationSnippetsEcMasterRasClientExampleAddConnection
        :end-before: DocumentationSnippetsEcMasterRasClientExampleAddConnection
        :language: cpp
        :dedent: 8

.. dropdown:: Then, optionally the master state can be requested:

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-RAS\software-integration.h
        :start-after: DocumentationSnippetsEcMasterRasClientExampleGetMasterStateOverRAS
        :end-before: DocumentationSnippetsEcMasterRasClientExampleGetMasterStateOverRAS
        :language: cpp
        :dedent: 8

.. dropdown:: Then, the RAS client has to be initialized:

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-RAS\software-integration.h
        :start-after: DocumentationSnippetsEcMasterRasClientExampleInitRasClient
        :end-before: DocumentationSnippetsEcMasterRasClientExampleInitRasClient
        :language: cpp
        :dedent: 8


An application which uses the remote API to access a master stack needs to call following steps:

.. code-block::

    #include "EcRasClient.h"
    .
    .
    emRasClntInit(…);	/* initialize Remote API Client Module */
    .
    .
    /* do not call emInitMaster(…) */
    .
    emRasClntAddConnection(…);	/* connect to Remote API Server */
    .
    .
    /* access EC-Master API */
    .
    .
    emRasClntRemoveConnection(…);	/* disconnect from Remote API Server */
    .
    .
    /* do not call emDeinitMaster(…) */
    .
    emRasClntClose(…);	/* de-initialize Remote API Client Module, closes all connections */

For closer details find a Remote API Client example project <AtemDemo> with your installed Examples. To get the Remote API Client example use the Buildspec <AtemRasDbg> or <AtemRasRel>.

Additional API description
**************************

Following calls are necessary to initialize, de-initialize and observe
the Remote API Client functionality.

emRasClntGetVersion
===================

.. doxygenfunction:: emRasClntGetVersion

emRasClntInit
=============

.. doxygenfunction:: emRasClntInit

.. doxygenstruct:: ECMASTERRAS_T_CLNTPARMS
  :members:

emRasClntClose
==============

.. doxygenfunction:: emRasClntClose

emRasClntAddConnection
======================

.. doxygenfunction:: emRasClntAddConnection 

.. doxygenstruct:: ECMASTERRAS_T_CLNTCONDESC
  :members:

emRasClntRemoveConnection
=========================

.. doxygenfunction:: emRasClntRemoveConnection

emRasGetConnectionInfo
======================

.. doxygenfunction:: emRasGetConnectionInfo

API calls supported
*******************

This chapter lists the API calls supported via Remote API and their
restrictions (if exist). Syntax description of each call may be found in
EC-Master Manual.

Fully supported calls
*********************

-  EC_T_DWORD **emStart**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwTimeout );

-  EC_T_DWORD **emStop**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwTimeout );

-  EC_T_DWORD **emGetSlaveId**\ ( EC_T_DWORD dwInstanceID, EC_T_WORD
   wStationAddress);

-  EC_T_DWORD **emGetSlaveIdAtPosition**\ ( EC_T_DWORD dwInstanceID,
   EC_T_WORD wAutoIncAddress);

-  EC_T_BOOL **emGetSlaveProp**\ (EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwSlaveId, EC_T_SLAVE_PROP\* pSlaveProp );

-  EC_T_DWORD **emGetSlaveState**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwSlaveId, EC_T_WORD\* pwCurrDevState, EC_T_WORD\* pwReqDevState,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emSetSlaveState**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwSlaveId, EC_T_WORD wNewReqDevState, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emTferSingleRawCmd**\ ( EC_T_DWORD dwInstanceID,
   EC_T_DWORD dwSlaveId, EC_T_BYTE byCmd, EC_T_DWORD dwMemoryAddress,
   EC_T_VOID\* pvData, EC_T_WORD wLen, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emQueueRawCmd**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwSlaveId, EC_T_WORD wInvokeId, EC_T_BYTE byCmd, EC_T_DWORD
   dwMemoryAddress, EC_T_VOID\* pvData, EC_T_WORD wLen );

-  EC_T_DWORD **emGetNumConfiguredSlaves**\ ( EC_T_DWORD dwInstanceID );

-  EC_T_MBXTFER\* **emMbxTferCreate**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER_DESC\* pMbxTferDesc );

-  EC_T_VOID **emMbxTferDelete**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer );

-  EC_T_DWORD **emCoeSdoDownloadReq**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex,
   EC_T_BYTE byObSubIndex, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emCoeSdoDownload**\ ( EC_T_DWORD dwInstanceID,
   EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex, EC_T_BYTE byObSubIndex,
   EC_T_BYTE\* pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **emCoeSdoUploadReq**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex,
   EC_T_BYTE byObSubIndex, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emCoeSdoUpload**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwSlaveId, EC_T_WORD wObIndex, EC_T_BYTE byObSubIndex, EC_T_BYTE\*
   pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD\* pdwOutDataLen, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **emCoeGetODList**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_COE_ODLIST_TYPE
   eListType, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emCoeGetObjectDesc**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emCoeGetEntryDesc**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex,
   EC_T_BYTE byObSubIndex, EC_T_BYTE byValueInfo, EC_T_DWORD dwTimeout
   );

-  EC_T_DWORD **emSetMasterState**\ ( EC_T_DWORD dwInstanceID,
   EC_T_DWORD dwTimeout, EC_T_STATE eReqState );

-  EC_T_STATE **emGetMasterState**\ ( EC_T_DWORD dwInstanceID);

-  EC_T_DWORD **emFoeFileUpload**\ (EC_T_DWORD dwInstanceID , EC_T_DWORD
   dwSlaveId, EC_T_CHAR\* szFileName, EC_T_DWORD dwFileNameLen,
   EC_T_BYTE\* pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD\*
   pdwOutDataLen, EC_T_DWORD dwPassWd, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emFoeFileDownload**\ (EC_T_DWORD dwInstanceID,
   EC_T_DWORD dwSlaveId, EC_T_CHAR\* szFileName, EC_T_DWORD
   dwFileNameLen, EC_T_BYTE\* pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD
   dwPassWd, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatStart**\ ( EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatStop**\ ( EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatGetSlaveId**\ ( EC_T_WORD wStationAddress);

-  EC_T_DWORD **ecatGetSlaveIdAtPosition**\ ( EC_T_WORD
   wAutoIncAddress);

-  EC_T_BOOL **ecatGetSlaveProp**\ ( EC_T_DWORD dwSlaveId,
   EC_T_SLAVE_PROP\* pSlaveProp );

-  EC_T_DWORD **ecatGetSlaveState**\ ( EC_T_DWORD dwSlaveId, EC_T_WORD\*
   pwCurrDevState, EC_T_WORD\* pwReqDevState, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatSetSlaveState**\ ( EC_T_DWORD dwSlaveId, EC_T_WORD
   wNewReqDevState, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatTferSingleRawCmd**\ ( EC_T_DWORD dwSlaveId,
   EC_T_BYTE byCmd, EC_T_DWORD dwMemoryAddress, EC_T_VOID\* pvData,
   EC_T_WORD wLen, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatQueueRawCmd**\ ( EC_T_DWORD dwSlaveId, EC_T_WORD
   wInvokeId, EC_T_BYTE byCmd, EC_T_DWORD dwMemoryAddress, EC_T_VOID\*
   pvData, EC_T_WORD wLen );

-  EC_T_DWORD **ecatGetNumConfiguredSlaves**\ ( );

-  EC_T_MBXTFER\* **ecatMbxTferCreate**\ ( EC_T_MBXTFER_DESC\*
   pMbxTferDesc );

-  EC_T_VOID **ecatMbxTferDelete**\ ( EC_T_MBXTFER\* pMbxTfer );

-  EC_T_DWORD **ecatCoeSdoDownloadReq**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex, EC_T_BYTE byObSubIndex,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatCoeSdoDownload**\ (EC_T_DWORD dwSlaveId, EC_T_WORD
   wObIndex, EC_T_BYTE byObSubIndex, EC_T_BYTE\* pbyData, EC_T_DWORD
   dwDataLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatCoeSdoUploadReq**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex, EC_T_BYTE byObSubIndex,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatCoeSdoUpload**\ (EC_T_DWORD dwSlaveId, EC_T_WORD
   wObIndex, EC_T_BYTE byObSubIndex, EC_T_BYTE\* pbyData, EC_T_DWORD
   dwDataLen, EC_T_DWORD\* pdwOutDataLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatCoeGetODList**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_COE_ODLIST_TYPE eListType, EC_T_DWORD
   dwTimeout );

-  EC_T_DWORD **ecatCoeGetObjectDesc**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatCoeGetEntryDesc**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_WORD wObIndex, EC_T_BYTE byObSubIndex,
   EC_T_BYTE byValueInfo, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatSetMasterState**\ ( EC_T_DWORD dwTimeout, EC_T_STATE
   eReqState );

-  EC_T_STATE **ecatGetMasterState**\ ( EC_T_VOID);

-  EC_T_DWORD **ecatFoeFileUpload**\ ( EC_T_DWORD dwSlaveId, EC_T_CHAR\*
   szFileName, EC_T_DWORD dwFileNameLen, EC_T_BYTE\* pbyData, EC_T_DWORD
   dwDataLen, EC_T_DWORD\* pdwOutDataLen, EC_T_DWORD dwPassWd,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatFoeFileDownload**\ ( EC_T_DWORD dwSlaveId,
   EC_T_CHAR\* szFileName, EC_T_DWORD dwFileNameLen, EC_T_BYTE\*
   pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD dwPassWd, EC_T_DWORD
   dwTimeout );

-  EC_T_DWORD **ecatGetSlaveInpVarInfoNumOf**\ (EC_T_BOOL bFixedAddress
   EC_T_WORD wSlaveAddress, EC_T_WORD\* pwSlaveInpVarInfoNumOf);

-  EC_T_DWORD **emGetSlaveOutpVarInfoNumOf**\ (EC_T_DWORD dwInstanceID,
   EC_T_BOOL bFixedAddress, EC_T_WORD wSlaveAddress, EC_T_WORD\*
   pwSlaveOutpVarInfoNumOf );

-  EC_T_DWORD **emGetSlaveInpVarInfo**\ (EC_T_DWORD dwInstanceID,
   EC_T_BOOL bFixedAddress, EC_T_WORD wSlaveAddress, EC_T_WORD
   wNumOfVarsToRead, EC_T_PROCESS_VAR_INFO\* pSlaveProcVarInfoEntries,
   EC_T_WORD\* pwReadEntries );

-  EC_T_DWORD **emGetSlaveOutpVarInfo**\ (EC_T_DWORD dwInstanceID,
   EC_T_BOOL bFixedAddress, EC_T_WORD wSlaveAddress, EC_T_WORD
   wNumOfVarsToRead, EC_T_PROCESS_VAR_INFO\* pSlaveProcVarInfoEntries,
   EC_T_WORD\* pwReadEntries );

-  EC_T_DWORD **emFindOutpVarByName** (EC_T_DWORD dwInstanceID,
   EC_T_CHAR\* szVariableName, EC_T_PROCESS_VAR_INFO\* pSlaveOutpVarInfo
   );

-  EC_T_DWORD **emFindInpVarByName** (EC_T_DWORD dwInstanceID,
   EC_T_CHAR\* szVariableName, EC_T_PROCESS_VAR_INFO\* pSlaveOutpVarInfo
   );

-  EC_T_DWORD **ecatIsSlavePresent**\ ( EC_T_DWORD dwSlaveId,
   EC_T_BOOL\* pbPresence);

-  EC_T_DWORD **ecatResetSlaveController**\ ( EC_T_BOOL
   bFixedAddressing, EC_T_WORD wSlaveAddress, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatGetNumConnectedSlaves**\ ( EC_T_VOID )

-  EC_T_DWORD **ecatSetProcessData**\ (EC_T_BOOL bOutputData, EC_T_DWORD
   wOffset, EC_T_BYTE\* pbyData, EC_T_DWORD dwLength, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatGetProcessData**\ (EC_T_BOOL bOutputData, EC_T_DWORD
   dwOffset, EC_T_BYTE\* pbyData, EC_T_DWORD dwLength, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatReadSlaveRegister**\ ( EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wRegisterOffset, EC_T_VOID\*
   pvData, EC_T_WORD wLen, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatWriteSlaveRegister**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wRegisterOffset, EC_T_VOID\*
   pvData, EC_T_WORD wLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatSoeWrite**\ (EC_T_DWORD dwSlaveId, EC_T_BYTE
   byDriveNo, EC_T_BYTE byElementFlags, EC_T_WORD wIDN, EC_T_BYTE\*
   pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatSoeRead**\ (EC_T_DWORD dwSlaveId, EC_T_BYTE
   byDriveNo, EC_T_BYTE byElementFlags, EC_T_WORD wIDN, EC_T_BYTE\*
   pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD\* pdwOutDataLen, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatSoeAbortProcCmd**\ (EC_T_DWORD dwSlaveId, EC_T_BYTE
   byDriveNo, EC_T_BYTE byElementFlags, EC_T_WORD wIDN, EC_T_DWORD
   dwTimeout );

-  EC_T_DWORD **ecatReadSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wEEPRomStartOffset, EC_T_WORD\*
   pwReadData, EC_T_DWORD dwReadLen, EC_T_DWORD\* pdwNumOutData,
   EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatWriteSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wEEPRomStartOffset, EC_T_WORD\*
   pwWriteData, EC_T_DWORD dwWriteLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatReloadSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatResetSlaveController(**\ EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatAssignSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_BOOL bSlavePDIAccessEnable, EC_T_BOOL
   bForceAssign, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatRegisterClient**\ (EC_PF_NOTIFY pfnNotify,
   EC_T_VOID\* pCallerData, EC_T_REGISTERRESULTS\* pRegResults);

-  EC_T_DWORD **ecatUnregisterClient**\ (EC_T_DWORD dwClntId);

Restricted supported calls
**************************

-  EC_T_DWORD **emIoControl**\ ( EC_T_DWORD dwInstanceID, EC_T_DWORD
   dwCode, EC_T_IOCTLPARMS\* pParms);

   -  Supported:

      -  EC_IOCTL_REGISTERCLIENT:

      -  EC_IOCTL_UNREGISTERCLIENT:

      -  EC_IOCTL_ISLINK_CONNECTED:

      -  EC_IOCTL_SET_CYC_ERROR_NOTIFY_MASK:

      -  EC_IOCTL_GET_PDMEMORYSIZE

      -  EC_IOCTL_SLAVE_LINKMESSAGES:

      -  EC_IOCTL_DC_SLV_SYNC_STATUS_GET:

      -  EC_IOCTL_DC_SLV_SYNC_DEVLIMIT_SET:

      -  EC_IOCTL_DC_SLV_SYNC_DEVLIMIT_GET:

      -  EC_IOCTL_SB_RESTART:

      -  EC_IOCTL_SB_STATUS_GET:

      -  EC_IOCTL_SB_SET_BUSCNF_VERIFY:

      -  EC_IOCTL_SB_SET_BUSCNF_VERIFY_PROP:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO_EEP:

      -  EC_IOCTL_SB_ENABLE:

   -  Not Supported:

      -  EC_IOCTL_RESET_SLAVE:

      -  EC_IOCTL_FORCE_BROADCAST_DESTINATION:

      -  EC_IOCTL_SET_FRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_RXFRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_TXFRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_SOFT_ASSERTIONS:

      -  EC_IOCTL_SET_HARD_ASSERTIONS:

      -  EC_IOCTL_LINKLAYER_DBG_MSG:

      -  EC_IOCTL_SET_COE_DBG_LEVEL:

      -  EC_IOCTL_GET_CYCLIC_CONFIG_INFO:

      -  EC_IOCTL_REGISTER_PDMEMORYPROVIDER:

      -  EC_IOCTL_REG_DC_SLV_SYNC_NTFY:

      -  EC_IOCTL_UNREG_DC_SLV_SYNC_NTFY:

      -  EC_IOCTL_DCM_REGISTER_TIMESTAMP:

      -  EC_IOCTL_DCM_UNREGISTER_TIMESTAMP:

      -  EC_IOCTL_RED_SET_LINK:

      -  EC_IOCTL_SLV_ALIAS_ENABLE:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO_EX:

-  EC_T_DWORD **emConfigureMaster**\ ( EC_T_DWORD dwInstanceID,
   EC_T_CNF_TYPE eCnfType, EC_T_PBYTE pbyCnfData, EC_T_DWORD
   dwCnfDataLen );

   -  Supported : eCnfType = eCnfType_Data

   -  Not supported: eCnfType = eCnfType_Filename

-  EC_T_DWORD **ecatIoControl**\ ( EC_T_DWORD dwCode, EC_T_IOCTLPARMS\*
   pParms);

   -  Supported:

      -  EC_IOCTL_GETSTATE:

      -  EC_IOCTL_REGISTERCLIENT:

      -  EC_IOCTL_UNREGISTERCLIENT:

      -  EC_IOCTL_SET_CYC_ERROR_NOTIFY_MASK:

      -  EC_IOCTL_ISLINK_CONNECTED:

      -  EC_IOCTL_SET_PHYS_MBX_POLLING_PERIOD:

      -  EC_IOCTL_SET_SLAVE_STATE_UPDATE_TIMEOUT:

      -  EC_IOCTL_RESET_SLAVE:

      -  EC_IOCTL_UPDATE_ALL_SLAVE_STATE:

      -  EC_IOCTL_GET_PDMEMORYSIZE:

      -  EC_IOCTL_FORCE_BROADCAST_DESTINATION:

      -  EC_IOCTL_SLAVE_LINKMESSAGES:

      -  EC_IOCTL_SET_FRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_RXFRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_TXFRAME_LOSS_SIMULATION:

      -  EC_IOCTL_SET_SOFT_ASSERTIONS:

      -  EC_IOCTL_SET_HARD_ASSERTIONS:

      -  EC_IOCTL_DC_ENABLE:

      -  EC_IOCTL_DC_DISABLE:

      -  EC_IOCTL_DC_SLV_SYNC_STATUS_GET:

      -  EC_IOCTL_DC_SLV_SYNC_DEVLIMIT_SET:

      -  EC_IOCTL_DC_SLV_SYNC_DEVLIMIT_GET:

      -  EC_IOCTL_DC_SLV_SYNC_RESTART:

      -  EC_IOCTL_DC_SLV_SYNC_SETTLETIME_SET:

      -  EC_IOCTL_DC_SLV_SYNC_SETTLETIME_GET:

      -  EC_IOCTL_DC_SLAVESYNCDISABLE:

      -  EC_IOCTL_SB_RESTART:

      -  EC_IOCTL_SB_STATUS_GET:

      -  EC_IOCTL_SB_SET_BUSCNF_VERIFY:

      -  EC_IOCTL_SB_SET_BUSCNF_VERIFY_PROP:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO_EEP:

      -  EC_IOCTL_SB_ENABLE:

      -  EC_IOCTL_SB_BUSCNF_GETSLAVE_INFO_EX:

      -  EC_IOCTL_SLV_ALIAS_ENABLE:

   -  Not Supported:

      -  EC_IOCTL_LINKLAYER_DBG_MSG:

      -  EC_IOCTL_SET_COE_DBG_LEVEL:

      -  EC_IOCTL_GET_CYCLIC_CONFIG_INFO:

      -  EC_IOCTL_REGISTER_PDMEMORYPROVIDER:

      -  EC_IOCTL_REG_DC_SLV_SYNC_NTFY:

      -  EC_IOCTL_UNREG_DC_SLV_SYNC_NTFY:

      -  EC_IOCTL_REG_DC_MAST_SYNC_NTFY:

      -  EC_IOCTL_UNREG_DC_MAST_SYNC_NTFY:

      -  EC_IOCTL_DC_SYSTIME_ADD_OFFSET:

      -  EC_IOCTL_DC_PDM_CYCLES_SET:

      -  EC_IOCTL_DC_PDM_CYCLES_GET:

      -  EC_IOCTL_DC_CONFIGURE_BURST:

      -  EC_IOCTL_DCM_REGISTER_TIMESTAMP:

      -  EC_IOCTL_DCM_UNREGISTER_TIMESTAMP:

      -  EC_IOCTL_RED_SET_LINK:

-  EC_T_DWORD **ecatConfigureMaster**\ ( EC_T_CNF_TYPE eCnfType,
   EC_T_PBYTE pbyCnfData, EC_T_DWORD dwCnfDataLen );

   -  Supported : eCnfType = eCnfType_Data

   -  Not supported: eCnfType = eCnfType_Filename

-  EC_T_DWORD **ecatNotify**\ ( EC_T_DWORD dwCode, EC_T_NOTIFYPARMS\*
   pParms );

   -  Supported:

      -  EC_NOTIFY_STATECHANGED:

      -  EC_NOTIFY_CYCCMD_WKC_ERROR:

      -  EC_NOTIFY_MASTER_INITCMD_WKC_ERROR:

      -  EC_NOTIFY_SLAVE_INITCMD_WKC_ERROR:

      -  EC_NOTIFY_COE_MBXRCV_WKC_ERROR:

      -  EC_NOTIFY_COE_MBXSND_WKC_ERROR:

      -  EC_NOTIFY_SLAVE_NOT_ADDRESSABLE:

      -  EC_NOTIFY_FRAME_RESPONSE_ERROR:

      -  EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR:

      -  EC_NOTIFY_MBSLAVE_INITCMD_TIMEOUT:

      -  EC_NOTIFY_MASTER_INITCMD_RESPONSE_ERROR:

      -  EC_NOTIFY_CMD_MISSING:

      -  EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL:

      -  EC_NOTIFY_STATUS_SLAVE_ERROR:

      -  EC_NOTIFY_SLAVE_ERROR_STATUS_INFO:

      -  EC_NOTIFY_ETH_LINK_NOT_CONNECTED:

      -  EC_NOTIFY_RED_LINEBRK:

      -  EC_NOTIFY_ETH_LINK_CONNECTED:

      -  EC_NOTIFY_SB_STATUS:

      -  EC_NOTIFY_RAWCMD_DONE:

      -  EC_NOTIFY_MBOXRCV:

   -  Not Supported:

      -  EC_NOTIFY_CYCCMD_TIMEOUT:

      -  EC_NOTIFY_DC_STATUS:

      -  EC_NOTIFY_DC_SLV_SYNC:

      -  EC_NOTIFY_DC_MAST_SYNC:

      -  EC_NOTIFY_DC_MAST_SYNC_CYC:

      -  EC_NOTIFY_DCL_STATUS:

      -  EC_NOTIFY_DCL_SLV_LATCH_EVT:

      -  EC_NOTIFY_DCL_SLV_TIMER_READ:

      -  EC_NOTIFY_COE_TX_PDO:

      -  EC_NOTIFY_EOE_MBXRCV_WKC_ERROR:

      -  EC_NOTIFY_FOE_MBXRCV_WKC_ERROR:

      -  EC_NOTIFY_EOE_MBXSND_WKC_ERROR:

      -  EC_NOTIFY_FOE_MBXSND_WKC_ERROR:

Not supported calls
*******************

-  EC_T_DWORD **emCoeRxPdoTfer**\ ( EC_T_DWORD dwInstanceID,
   EC_T_MBXTFER\* pMbxTfer, EC_T_DWORD dwSlaveId, EC_T_DWORD dwNumber,
   EC_T_DWORD dwTimeout );

-  EC_T_DWORD **emExecJob**\ ( EC_T_DWORD dwInstanceID, EC_T_USER_JOB
   eUserJob, EC_T_PVOID pvParam );

-  EC_T_DWORD **ecatCoeRxPdoTfer**\ ( EC_T_MBXTFER\* pMbxTfer,
   EC_T_DWORD dwSlaveId, EC_T_DWORD dwNumber, EC_T_DWORD dwTimeout );

-  EC_T_DWORD **ecatExecJob**\ ( EC_T_USER_JOB eUserJob, EC_T_PVOID
   pvParam );

-  EC_T_DWORD **ecatEthDbgMsg**\ ( EC_T_BYTE byEthTypeByte0, EC_T_BYTE
   byEthTypeByte1, EC_T_CHAR\* szMsg);

-  EC_T_DWORD **ecatDcConfigure**\ (EC_T_DC_CONFIGURE\* pDcConfigure);

-  EC_T_DWORD **ecatBlockNode**\ ( EC_T_SB_MISMATCH_DESC, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatOpenBlockedPorts**\ (EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatForceTopologyChange**\ ( EC_T_DWORD dwInstanceID);

-  EC_T_DWORD **ecatDcDisable**\ ();

-  EC_T_DWORD **ecatDcDisable**\ ();

-  EC_T_DWORD **ecatSetSlavePortState**\ ( EC_T_DWORD dwSlaveID,
   EC_T_WORD wPort, EC_T_BOOL bClose, EC_T_BOOL bForce, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatHCGetSlaveIdsOfGroup**\ (EC_T_DWORD dwGroupIndex,
   EC_T_DWORD\* adwSlaveId, EC_T_DWORD dwMaxNumSlaveIds );

-  EC_T_DWORD **ecatHCGetNumGroupMembers**\ (EC_T_DWORD dwGroupIndex );

-  EC_T_DWORD **ecatHCAcceptTopoChange**\ (EC_T_VOID);

-  EC_T_DWORD **ecatReloadSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatWriteSlaveEEPRom**\ ( EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wEEPRomStartOffset, EC_T_WORD\*
   pwWriteData, EC_T_DWORD dwWriteLen, EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatReadSlaveEEPRom**\ (EC_T_BOOL bFixedAddressing,
   EC_T_WORD wSlaveAddress, EC_T_WORD wEEPRomStartOffset,EC_T_WORD\*
   pwReadData,EC_T_DWORD dwReadLen, EC_T_DWORD\* pdwNumOutData,
   EC_T_DWORD dwTimeout);

-  EC_T_DWORD **ecatEoeRegisterEndpoint**\ ( EC_T_CHAR\* szEoEDrvIdent,
   EC_T_VOID\* pLinkDrvDesc);

-  EC_T_DWORD **ecatSoeAbortProcCmd**\ (EC_T_DWORD dwSlaveId,EC_T_BYTE
   byDriveNo, EC_T_BYTE byElementFlags, EC_T_WORD wIDN,EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatSoeRead**\ (EC_T_DWORD dwSlaveId,EC_T_BYTE
   byDriveNo,EC_T_BYTE byElementFlags,EC_T_WORD wIDN, EC_T_BYTE\*
   byData,EC_T_DWORD dwDataLen, EC_T_DWORD\* pdwOutDataLen, EC_T_DWORD
   dwTimeout);

-  EC_T_DWORD **ecatSoeWrite**\ (EC_T_DWORD dwSlaveId, EC_T_BYTE
   byDriveNo, EC_T_BYTE byElementFlags, EC_T_WORD wIDN, EC_T_BYTE\*
   pbyData, EC_T_DWORD dwDataLen, EC_T_DWORD dwTimeout);