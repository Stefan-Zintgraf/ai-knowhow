*********
Migration
*********

From V3.1
*********

- EcMaster source code requires EC_MASTER to be defined during compilation
- Remove VxWorks70SR540 
- Remove RZGNoOS 
- Remove WinIoT 
- Remove WinCE500 
- Remove StarterWare 
- Remove NIOS 
- Remove JSL-Ware 
- Remove SylixOS 
- Remove RTXC-Quadros 
- Remove emllNdisUio 
- Remove emllUdp 
- Remove obsolete .NET and Python interface classes, enums and methods  
- Remove the notion of auxclk and therefore also the demo -auxclk parameter and the OsAuxClk* functions. The demos have a best fit DC time implementation per platform now (see also EcDemoTimingTaskPlatform) 
- Remove EC_IOCTL_SET_PD_OFFSET_COMPAT_MODE 
- Rename SYSBIOS to TI-RTOS 
- Rename Stm32Eth to CmsisEth 
- Migrate Microsoft®  Windows®  Visual Studio®  (VS) project files to VS2015 (VS2005 and VS2010 are not delivered anymore) 
- Replace emllI8254x with emllIntelGbe and support of TTS for Intel®  i210 and i211 
- Rename AtEthercat.h to EcMaster.h 
- Rename AtemRasSrv to EcMasterRasServer 
- Rename AtemRasClnt to EcMasterRasClient 
- Rename emPerfMeasInternal to emPerfMeas, old deprecated API removed 
- Rename emConfigureMaster()to emConfigureNetwork() 
- Refactor EC_T_SB_MISMATCH_DESC 
- Rename emCoeGetOdList(), emCoeGetObjectDesc() and emCoeGetEntryDesc() to emCoeGetOdListReq(), emCoeGetObjectDescReq() and emCoeGetEntryDescReq() 

From V3.0
*********

-  Application should call ProcessAllRxFrames in interrupt mode on cyclic event timeout
-  Add SDK/INC/OsCommon.h
-  OsDeleteThreadHandle, OsSetThreadPriority, OsSetThreadAffinity,
   OsGetThreadAffinity have been refactored (additional parameters / return code)
-  Add cpuAffinityMask to ATEMRAS_T_SRVPARMS, ATEMRAS_T_CLNTCONDESC, ATEMRAS_T_CLNTPARMS
-  Add cpuIstCpuAffinityMask to EC_T_LINK_PARMS
-  Add EC_CPUSET_IS_ZERO
-  Add EC_LOG_LEVEL_INFO_API
-  EC_IOCTL_DC_REF_CLOCK_CONTROLLED_BY_PDI replaced by EC_IOCTL_DC_SLAVE_CONTROLLED_BY_PDI
-  Changed to .NET 4.0 Client Profile instead of .NET 2.0 for EcMasterDotNet
-  Removed obsolete parameter dwSlaveId from emTferSingleRawCmd, emQueueRawCmd, emClntQueueRawCmd
-  Removed obsolete members ATEMRAS_T_SRVPARMS::dwReConTOLimit, ATEMRAS_T_CLNTPARMS::dwKeepAliveTrigger, EC_T_MBX_DATA::dwFoETransferredBytes
-  Removed obsolete EcMasterDemo2

From V2.9
*********

-  The acyclic communication bandwidth restriction was done by the combination of dwMaxSlaveCmdPerFrame and dwMaxSentQueuedFramesPerCycle. 
   Because mailbox transfers consume more bandwidth than register transfers, dwMaxAcycBytesPerCycle has been added to EC_T_INIT_MASTER_PARMS to restrict it in a better way.
   
   The parameters related to acyclic communication have been renamed to identify them easily:
   
   - dwMaxQueuedEthFrames -> dwMaxAcycFramesQueued
   - dwMaxSentQueuedFramesPerCycle -> dwMaxAcycFramesPerCycle
   - dwMaxSlaveCmdPerFrame -> dwMaxAcycCmdsPerCycle
   - dwMaxAcycFramesPerCycle and dwMaxAcycCmdsPerCycle still exist to be able to limit the CPU load related to frame/command processing.

-  Removed obsolete parameter EC_T_INIT_MASTER_PARMS::dwEoETimeout
-  dwLogLevel and pfLogMsgCallBack have been moved into EC_T_INIT_MASTER_PARMS::LogParms. Additionally, a context has been added to the pfLogMsgCallBack function.
-  Set INCLUDE_FAST_MODE in case of Fast Mode (implicit assuming dropped)
-  Additional parameter dwTaskId to EC_PF_CYCFRAME_RECV
-  API change for emExecJob: EC_T_USER_JOB_PARMS\* pUserJobParms replaced parameter EC_T_VOID\* pvParam
-  IO control EC_IOCTL_SET_CYC_ERROR_NOTIFY_MASK replaced with EC_IOCTL_SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK. Error masks were renamed accordingly.
-  Additional parameter dwTaskId for memory provider callback functions pfPDOutReadRequest, pfPDOutReadRelease, pfPDInWriteRequest and pfPDInWriteRelease.
-  Correlation between WkcState and Pd offset changed. Logical mailbox state commands are no longer considered.
-  Value EC_LOG_LEVEL_UNDEFINED has been changed from 0 to -1 EC_LOG_LEVEL_SILENT is defined as 0.
-  eInitCmdErr_UNDEFINED is not defined and returned anymore
