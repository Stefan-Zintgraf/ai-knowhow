*********************************
Application programming interface
*********************************

Configure Master Redundancy in emInitMaster
*******************************************

The application must fill :cpp:struct:`EC_T_MASTER_RED_PARMS` when call :cpp:func:`emInitMaster`.

.. doxygenstruct:: EC_T_MASTER_RED_PARMS
    :members:
    
.. code-block:: cpp

    {
        EC_T_INIT_MASTER_PARMS oInitParms;

        OsMemset(&oInitParms, 0, sizeof(EC_T_INIT_MASTER_PARMS));
        …
        oInitParms.MasterRedParms.bEnabled = EC_TRUE;
        oInitParms.MasterRedParms.bUpdateSlavePdIn = EC_TRUE;
        oInitParms.MasterRedParms.bUpdateSlavePdOut = EC_TRUE;
        oInitParms.MasterRedParms.wMasterPdInSize = 10;
        oInitParms.MasterRedParms.wMasterPdOutSize = 20;
        oInitParms.MasterRedParms.dwMaxAcycFramesPerCycle = 3;
        …
        dwRes = ecatInitMaster(&oInitParms);
        …
    }

emSetMasterRedStateReq
**********************

Requests Master Redundancy State ACTIVE / INACTIVE.

.. doxygenfunction:: emSetMasterRedStateReq

.. code-block:: cpp

    dwRes = ecatSetMasterRedStateReq(EC_TRUE);
    if (dwRes != EC_E_NOERROR)
    {
        …
    }

emGetMasterRedState
*******************

Gets Master Redundancy State (ACTIVE / INACTIVE).

.. doxygenfunction:: emGetMasterRedState

.. code-block:: cpp

    EC_T_BOOL bMasterActive = EC_FALSE;
    dwRes = ecatGetMasterRedState(&bMasterActive);
    if (dwRes != EC_E_NOERROR)
    {
        …
    }

emGetMasterRedProcessImageInputPtr
**********************************

Gets pointer to INACTIVE to ACTIVE Master Process Data.

.. doxygenfunction:: emGetMasterRedProcessImageInputPtr

.. code-block:: cpp

    EC_T_BYTE* pInactiveToActivePd = ecatGetMasterRedProcessImageInputPtr();
    if (EC_NULL != pInactiveToActivePd)
    {
        …
    }

EC_NOTIFY_FRAME_RESPONSE_ERROR
******************************

.. doxygenstruct:: EC_NOTIFY_FRAME_RESPONSE_ERROR
    :members:

.. seealso:: Especially parameter :c:enum:`eRspErr_FOREIGN_SRC_MAC`

EC_NOTIFY_MASTER_RED_STATECHANGED
*********************************

Notification about a change of the Master Redundancy State.

.. doxygenstruct:: EC_NOTIFY_MASTER_RED_STATECHANGED
    :members:
    
APIs at ACTIVE / INACTIVE
*************************

The behaviour of APIs may be different depending on the Master Redundancy State. Some functionality may be blocked and the API returns :cpp:struct:`EC_E_MASTER_RED_STATE_ACTIVE` or :cpp:struct:`EC_E_MASTER_RED_STATE_INACTIVE` accordingly. The lists are subject to be extended.

The following APIs are blocked if the Master is INACTIVE:

.. hlist:: 
    :columns: 4

    * :cpp:func:`emCoeSdoDownloadReq`
    * :cpp:func:`emCoeSdoUploadReq`
    * :cpp:func:`emCoeGetODListReq` 
    * :cpp:func:`emCoeGetObjectDescReq`
    * :cpp:func:`emCoeGetEntryDescReq`
    * :cpp:func:`emSetSlaveState`
    * :cpp:func:`emTferSingleRawCmd`
    * :cpp:func:`emSetMasterState`
    * :cpp:func:`emQueueRawCmd`
    * :cpp:func:`emCoeRxPdoTfer`
    * :cpp:func:`emFoeFileUpload`
    * :cpp:func:`emFoeFileDownload`
    * :cpp:func:`emFoeUploadReq`
    * :cpp:func:`emFoeDownloadReq`
    * :cpp:func:`emCoeSdoDownload`
    * :cpp:func:`emCoeSdoUpload`
    * :cpp:func:`emReadSlaveEEPRom`
    * :cpp:func:`emWriteSlaveEEPRom`
    * :cpp:func:`emAssignSlaveEEPRom`
    * :cpp:func:`emActiveSlaveEEPRom`
    * :cpp:func:`emClntQueueRawCmd`
    * :cpp:func:`emReadSlaveRegister`
    * :cpp:func:`emWriteSlaveRegister`
    * :cpp:func:`emVoeRead`
    * :cpp:func:`emVoeWrite`
    * :cpp:func:`emVoeWriteReq`
    * :cpp:func:`emEthDbgMsg`
    * :cpp:func:`emAoeRead`
    * :cpp:func:`emAoeWrite`
    * :cpp:func:`emAoeWriteControl`
    * :cpp:func:`emAoeReadReq`
    * :cpp:func:`emAoeWriteReq`
    * :cpp:func:`emSoeRead`
    * :cpp:func:`emSoeWrite`
    * :cpp:func:`emSoeAbortProcCmd`
    * :cpp:func:`emAoeReadWrite` 
    * :cpp:func:`emMbxTferAbort`
    * :cpp:func:`emSoeReadReq`
    * :cpp:func:`emSoeWriteReq`
    * :cpp:func:`emSetSlavePortState`
    * :cpp:func:`emBlockNode`
    * :cpp:func:`emOpenBlockedPorts`
    * :cpp:func:`emForceTopologyChange`
    * :cpp:func:`emReloadSlaveEEPRom`
    * :cpp:func:`emResetSlaveController`
    * :cpp:func:`emGetSlaveInfo`
    * :cpp:func:`emIsTopologyChangeDetected`
    * :cpp:func:`emScanBus`
    * :cpp:func:`emClntSendRawMbx`
    * :cpp:func:`emFoeSegmentedDownloadReq`
    * :cpp:func:`emFoeSegmentedUploadReq`
    * :cpp:func:`emReadSlaveIdentification`
    * :cpp:func:`emRescueScan`
    * :cpp:func:`emGetSlaveStatistics`
    * :cpp:func:`emClearSlaveStatistics`

The following IOCTLs are blocked if the Master is INACTIVE:

.. hlist::
    :columns: 4
    
    * :ref:`emIoControl - EC_IOCTL_GET_SLVSTATISTICS`
    * :ref:`emIoControl - EC_IOCTL_SET_SLVSTAT_PERIOD`
    * :ref:`emIoControl - EC_IOCTL_FORCE_SLVSTAT_COLLECTION`
    * :ref:`emIoControl - EC_IOCTL_SB_RESTART`

The following APIs are enabled for ACTIVE / INACTIVE, but (may) behave differently:

.. hlist::
    :columns: 3
    
    * :cpp:func:`emIoControl`
    * :cpp:func:`emExecJob`
    * :cpp:func:`emIsSlavePresent`
    * :cpp:func:`emGetSlaveState`
    * :cpp:func:`emGetMasterState`
    * :cpp:func:`emCoeSdoUpload` (at INACTIVE only Master OD is accessible)
    * :cpp:func:`emCoeSdoDownload` (at INACTIVE only Master OD is accessible)

The following APIs are independent of the Master Redundancy State:

- OS Layer APIs like OsInit, OsSleep, …
- Real-time Ethernet Driver APIs like EcLinkSendFrame, …
- Trace APIs like :cpp:func:`emSetTraceMask`, …
- Performance Measurement APIs like :cpp:func:`emPerfMeasStart`, :cpp:func:`emPerfMeasEnd`
- :cpp:func:`emGetSlaveId`
- :cpp:func:`emMbxTferCreate`, :cpp:func:`emMbxTferDelete`
- :cpp:func:`emConfigureNetwork`
- :cpp:func:`emGetSlaveId`

********************
Implementation Hints
********************

Startup API order
*****************

Configuring Master Redundancy must be done when initializing the Master, before starting the Job Task to prevent from unintentional collisions and frame loss at ACTIVE Master. (REQ041)

The client registration is needed for collision detection and therefore must take place, before starting the Job Task. 

The client registration must be done immediately after configuring the master else it will be dropped.

Master Redundancy needs an ENI file given.

The Application must provide the Job Task executing the Master APIs at ACTIVE and INACTIVE Master.

Communication needs an ACTIVE Master
************************************

In order to keep real-time constraints the INACTIVE Master does not autonomously send frames so if the application decides to set both Master INACTIVE the communication on network will stop.

Links at failing Master must go down
************************************

If a Master is not able to send or forward any frames, the links at the connected EtherCAT® devices must go down else the EtherCAT® communication is destroyed. (REQ012)
The link at the INACTIVE Master may only be established as soon as it can forward frames!

Link loss to the failing Master could be used for early Master failure detection. 

Mailbox transfers and switchover
********************************

The EC-Master cancels pending Mailbox transfers on getting INACTIVE. The Application must handle the case that a mailbox transfer is denied after a failover or switchover, e.g. retry the transfer.


