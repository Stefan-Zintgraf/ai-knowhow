V3.1.4.08
*********

**Enhancement**

-  Add slave address to status word and control word change log messages in EC-Motion
-  Add AMI8000 related information to Slave Objects (configured slaves) 0x8nnn in Master OD for TwinSAFE Loader support
-  Add support for SwapData types Swap_HB_LB, Swap_HW_LW and Swap_HB_LB_HW_LW

**Fixes**

-  Fix BusDiagnosisInfo counters at emGetMasterInfo() and Bus Diagnosis Object 0x2002 in Master OD erroneously set to 0xFFFFFFFF in case frame send failed (broken since V3.1.4.02)
-  Fix frame loss on line fixed at active master for master redundancy
-  Fix JobTask cycle time in Python examples
-  Fix Mailbox Gateway server forwarding non RAWMBX transfer to client

**Platform**

-  Fix swapped values in Identity Object 0x1018 in Master OD for PPC
-  Fix timestamp in History Object (0x10F3) for PPC
-  Add support for VxWorks MSI
-  Fix lock-up in emllProxy EcLinkClose() on Windows

V3.1.4.07
*********

**Platform**

-  Add SDK to EC-STA Eval packages
-  Fix VxWorks RTP AtemSys pipe release
-  Fix memory violation leading to undefined behavior like crash or erroneous timeout during DC related InitCmd on VxWorks70 PPC and x86 with emllSnarf, SystemTime() since VxWorks70SR660 and DMA on x86 since VxWorks70vw2203

V3.1.4.06
*********

**Enhancement**

-  Add EcMasterDemoMinimal
-  Add dwCyclicLostFrames and dwAcyclicLostFrames to EC_IOCTL_CLEAR_MASTER_INFO_COUNTERS
-  Add support for clearing multiple Bus Diagnosis Counters at once
-  Add slave station address to EC_T_COE_ENTRYDESC, EC_T_COE_OBDESC and EC_T_COE_ODLIST
-  Add EC_IOCTL_DC_SET_RED_PROPAGDELAY
-  Increase log buffer in examples
-  Remove BlockNode handling from CEmNotification

**Fixes**

-  Fix log level handling in emSelfTestScan
-  Fix unexpected error message "Re-register client failed" in EC-SlaveTestApplication on RAS server stop
-  Fix to not search for client descriptor on mailbox transfer with INVALID_CLIENT_ID
-  Fix slave information prints contain "ERROR: Not found" in examples
-  Fix crash in case of invalid ENI containing a hot connect group head slave with physical address equal to zero
-  Fix crash in case of invalid ENI with Slave/Mailbox/Recv/StatusBitAddr, but missing Master/MailboxStates/Count
-  Fix emSetMasterState() if EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE = false and permanent frame loss
-  Rename 0x2200 "Bus Load Base Object" to "Bus Load Statistics Object"
-  Fix DCM BusTime plausibilty check for BusTime > 0xF000000000000000

**Platform**

-  Add link status state machine to emllBcmGenet
-  Add support for Linux ARM 32 Bit to emllBcmGenet
-  Force disconnection using PHY loopback for emllI8254x if ResetOnDisconnect not set
-  Add support for emllTiEnetIcssg on AM64xEVM with FreeRTOS
-  Add emllDW3504 for Xenomai
-  Select 'ECAT Protocol Driver' installation on Windows by default if not currently installed
-  Fix PCI link layer support for QNX ARM 32 Bit
-  Add DCM MasterShift for QNX
-  Add support for emllGEM on Xilinx Kria KR260
-  Fix missing ATEMRAS_NOTIFY_CONNECTION EMRAS_EVT_SERVERSTOPPED on connection termination by server
-  Fix TX hang in emllI8254x for I219 after uncontrolled termination
-  Fix lock-up in EC-Wrapper RAS connection on termination by server
-  Set default stack size to 0x8000 for 64 Bit architectures

V3.1.4.05
*********

**Enhancement**

-  Add round-trip time measurement to emSelfTestScan()
-  Add histogram export to examples
-  Call EC_LINKIOCTL_ONTIMER in emExecJob(eUsrJob_MasterTimer) by default

**Fixes**

-  Fix initialization failure if EcLinkOpen returns EC_E_LINK_DISCONNECTED
-  Fix dwNumFramesSent sometimes not zero if link disconnected
-  Fix crash in emConfigureMaster(eCnfType_GenPreopENI) if more than 4 PDO mapping entries in EEPROM
-  Fix no messages in error log if NOPRINTF defined
-  Fix crash in emConfigureMaster() sometimes if multiple tasks configured
-  Add legacy application support to 0x2200 Bus Load object (broken since V3.1.4.03 by #4420)

**Platform**

-  Add Xenomai3 ARM 64Bit support to RTL8169
-  Add emllBcmGenet for Raspberry PI 4 (BCM2711)
-  Add support for Universal WIBU Code
-  Fix reset MAC address at DW3504
-  Fix memory leak in OsCreateEvent() on Linux, Xenomai, RTEMS and SylixOs in case of semaphor initialization error

V3.1.4.04
*********

**Enhancement**

-  Add EC_ALL_CLIENTS_ID support to emReleaseAllProcessDataBits()
-  Increase API poll time to bus cycle time
-  Add dwSlaveIdentification to EC_IOCTL_SET_MASTER_DEFAULT_TIMEOUTS

**Fixes**

-  Fix emSetSlaveState() returns EC_E_NOTFOUND for HC slave instead of EC_E_SLAVE_NOT_PRESENT
-  Fix emRescueScan() returning erroneous EC_E_NOERROR on timeout in some cases
-  Fix 400ns delay at last DC slave with cable redundancy

**Platform**

-  Add support for Xenomai3 ARM 64Bit
-  Add thread join in OsAuxClkDeinit() on Linux
-  Add support for SGMII based PHY to emllDW3504
-  Add support for PHY OS Driver to CPSW (ePHY_OSDRIVER)
-  Fix OsInit()/OsDeinit() called multiple times for DLL
-  Fix 1s delay in OsAuxClkInit() on Linux
-  Update atemsys V1.4.21

   - Add Device Tree Ethernet driver support for CPSW 
   - Add Device Tree Ethernet driver PHY reset 
   - Fix Device Tree Ethernet on Xenomai3 
   - Add HAVE_IRQ_TO_DESC define to handle non-mainstream API variance

V3.1.4.03
*********

**Enhancement**

-  Add 0x2200 Bus Load object reset entry
-  Add "-oem" command line parameter to examples
-  Add termination of blocking API calls without JobTask
-  Fix mismatch free() / delete / delete [] in emInitMaster() / emDeinitMaster() for protected version
-  Add EC_IOCTL_SET_BUS_DIAGNOSIS_COUNTERS_OVERFLOW_ENABLED
-  Add DCM MasterShift support to RTX
-  Add VxWorks70 RTP Support for Snarf

**Fixes**

-  Fix AoE sender port (broken since V3.1.4.01)
-  Fix occasional lock-up in emScanBus
-  Add project files for LxWin
-  Fix missing static libraries in Windows packages
-  Fix missing cyclic commands in some cases using EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED and eCycFrameLayout_DYNAMIC together
-  Fix unexpected error message on AoE init command response
-  Fix corrupted CoE channel profile info in case of multiple channels
-  Add missing project files to RTX64 source packages
-  Fix emIsTopologyKnown() returns true after slave dissapears
-  Fix memory leak in case of incomplete frame receiving (missing fragments) resulting in communication timeout in EoE (broken since V3.0.1.07)

**Platform**

-  Add DCM LinkLayerRefClock support to RTOS-32
-  Add QNX7 and QNX71 support to EC-Master DAQ
-  Increase resolution for OsSystemTimeGet() on Windows
-  Add bDisablePromiscousMode and bDisableForceBroadcast parameters to emllNdis
-  Add absolute path support alternative to OsGetLinkLayerRegFunc for VxWork70
-  Fix counter overrun in OsQueryMsecCount on VxWorks69 PENTIUM4
-  Fix RTOS-32 is not supporting cycle times below 1000us (broken since V3.1.1.06)
-  Fix occasional crash in RAS Server on EC_IOCTL_UNREGISTERCLIENT
-  Fix occasional crash on emRasClntRemoveConnection after emRasSrvStop
-  Fix Interrupt Mode support for emllProxy
-  Fix Multi Tasks Configuration doesn't work with emllNdis Linklayer
-  Fix memory leak on RAS socket disconnect while API call pending
-  Fix to block emRasClntRemoveConnection, emRasSrvStop until all worker threads terminated

V3.1.4.02
*********

**Enhancement**

-  Add setting WkcState bit in case of link disconnected
-  Add link layer parameters help to Python example application
-  Add performance measurement level to -perf command line parameter
-  Add emGetMemoryUsage over RAS
-  Add emSelfTestScan enhancements

**Fixes**

-  Fix EC_IOCTL_SET_DIAGMSG_CODE_BASE input buffer size check
-  Fix crash in ProcessCoEResponse() logging if pending CoE MbxTfer deleted
-  Fix emCoeGetODList for Master Object 0x3nnn, 0x8nnn, 0x9nnn, 0xAnnn if no slaves connected and/or configured
-  Fix blocking API handling over RAS
-  Fix bus diagnosis info counters overflow at emGetMasterInfo / Master Object 0xF120
-  Fix emCoeProfileGetChannelInfo returning non-empty display name string if not specified in ENI
-  Fix set all inputs to zero on link disconnection if EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO is enabled
-  Fix InitWrapper() for EC-Master caused invalid error message in EcWrapperPython
-  Fix command line contains unexpected application name in RTOS-32 config files
-  Fix bad WkcState delayed during set slave state transition
-  Fix missing link status refresh in SendCycFramesByTaskId

**Platform**

-  Add MAC protection to emllFslFec for i.MX8 and i.MX8m
-  Fix CPSW transmit channels to work with acontis CPSW Linux driver patch

V3.1.4.01
*********

**Enhancement**

-  Don't call OsMeasCalibrate() if performance measurement is disabled
-  Improve histogram behavior of PerfMeas for Cycle Time benchmark
-  Rename PerfMeas distances to offsets
-  Suppress some cascaded connection lock during emRasClntAddConnection and emRasClntRemoveConnection

**Fixes**

-  Fix Slave Diagnosis Data Objects: 0xA000-0xAFFF for hot connect configurations
-  Fix bad WkcState delayed during set slave state transition
-  Fix WkcState after Frame Loss for Master Redundancy
-  Fix pMbxTfer->MbxData.CoE.wStationAddress always 0 by EC_NOTIFY_MBOXRCV over RAS
-  Set default InitCmd Timeout to 1100ms to support e.g. EL9227-5500 having 1s delay (regression since V3.0.0.05)

**Platform**

-  Fix DCM MasterShift on SYSBIOS
-  Fix i8254x interrupt mode on ARM/AARCH64
-  Add support for cycle time below 1ms to EcMasterDemoRasServer for SYSBIOS on AM57xx boards
-  Fix RAS connection configuration of EcMasterDemoRasServer for SYSBIOS on AM572x boards (regression since V3.1.3.03)
-  Fix AoE support for PPC
-  Updated to ECAT NDIS Protocol Driver Setup V3.1.3.4 Hide command window during driver installation
-  Updated to atemsys V1.4.20 

   - Fix support for CMA (Contiguous Memory Allocator) for kernel >   4.9.00

V3.1.3.03
*********

**Enhancement**

-  Prevent calls to \`emIoControl - EC_IOCTL_SET_CYCFRAME_LAYOUT\` after configuring the master for eCycFrameLayout_FIXED
-  Add EC_T_MASTER_INFO::dwMasterStateSummary
-  EC_T_MASTER_INFO::BusDiagnosisInfo data available even if compiled with EXCLUDE_MASTER_OBD

**Fixes**

-  Decrement MbxCnt if MbxCmd for split access cannot be queued
-  Fix ScanBus() over RAS for eCnfType_None
-  Fix IoControl() is changing Input Buffer data in the RAS client
-  Add missing “\\n” in EcMasterDemoDc\\EcDemoApp.cpp

**Platform**

-  Add EcWinDemo to EC-WinRT-Linux and EC-WinRTOS-32
-  Add passing EC_T_OS_PARMS HwTimer functions for user MasterShift support to VxWorks
-  Fix EcMasterRas.cfg of the EcMasterDemoRasServer for Sysbios AM57x so that the demo works properly for AM571x boards
-  Add MAC protection for Stm32Eth CMSIS
-  Fix exception on reconnect in RIN32
-  Updated to atemsys V1.4.18 
   - Remove obsolete ARM cycle count register(CCNT) 
   - Fix PCI driver do registration for all Ethernet network adapters 
   - Add modul parameter AllowedPciDevices to adjust PCI driver
-  Add CPU affinity support to Link Layers supporting interrupt mode

V3.1.3.02
*********

**Enhancement**

-  Support ENI file with CU2508 only
-  Disconnection release closed port by ecatRescueScan

**Fixes**

-  Fix mailbox transfer to slaves found above PREOP at the beginning of IP transition (regression since V3.1.3.01)
-  Fix MbxCnt was not decremented if MbxCmd cannot be queued
-  Fix ecatExecJob(eUsrJob_SendAllCycFrames) returns dwNumFramesSent = 0 sometimes

**Platform**

-  Add RTL8168H support to emllRTL8169
-  Fix DMA buffer alignment in emllRTL8169 (regression since V3.1.3.01)
-  Fix DMA allocation, requesting memory below 4GB for AARCH64/ARM64 on QNX
-  | Updated to ECAT NDIS Protocol Driver V3.1.3.2 | Move promiscuous mode setting from NDIS Link-Layer to NDIS protocol   driver | Add an entry “DontSetPromiscuousMode” in the Windows registry to   avoid setting promiscuous mode in ECAT NDIS Protocol Driver | Rename Setup to "ECAT NDIS Protocol Driver"
-  Fix 32-bit rollover in OsMeasGetCounterTicks on Integrity
-  Fix EcatDrvGetDrvVersion on Windows (regression since V3.1.3.01)
-  Fix DMA memory allocation address handling if base is > 2GB leading to permanent frameloss in VxWorks-32Bit
-  Add RTL8125 support to emllRTL8169
-  Add Link Layer IST CPU affinity mask and priority for .NET and Python
-  Add CYCFRAME_RX_CB for .NET and Python
-  Fix RIN32 OsLayer, notifications will not be sent in interrupt mode
-  Updated to atemsys V1.4.17
   - Fix atemsys dma_set_mask_and_coherent() missing in kernels under   3.12.55

-  Fix EoE-Endpoint QnxTAP
-  NDIS fix start-up with link disconnected

V3.1.3.01
*********

**Enhancement**

-  Add emSelfTestScan

**Fixes**

-  Fix AoE command length calculation
-  Retry ESC reset procedure in emResetSlaveController
-  Fix slave sometimes set to unknown state 0 during identification procedure
-  Fix memory corruption in emCoeGetODList
-  Fix EoE communication reliability during transitions above PREOP
-  Fix parallel mailbox transfers for topologies with few slaves
-  Fix crash in AtemRasClnt on Windows x86_32Bit. Regression since V3.1.2.11.
-  Fix notfication error log messages for eMbxTferType_COE_SDO_UPLOAD and eMbxTferType_COE_SDO_DOWNLOAD in example EcNotification.cpp

**Platform**

-  Add interrupt mode support for emllSockRaw
-  Updated to EcatDrv V3.1.3.01 Add Print EcatDrv Version to Ecat Driver for Windows
-  Fix parse PCI bus hardware ID string on Windows

V3.1.2.11
*********

**Enhancement**

-  Extend EC_T_BUS_DIAGNOSIS_INFO with dwCyclicLostFrames and dwAcyclicLostFrames

**Fixes**

-  Fix crash in PRINT_PERF_MEAS() due to missing LogContext when the Log level is silent and the performance measurement is enabled
-  Fix DEVICE_STATUSCODE_APPLICATION_CONTROLLER_AVAILABLE info in OP
-  Fix Mbx transfer always return with EC_E_TIMEOUT after slave error in PS or SO transition (broken since V3.1.1.05) (merge V3.1.1)

**Platform**

-  Add OsHwTimerGetCurrentCount() to Sysbios, Fix Timer and OsQueryMsecCount()
-  Fix I8255x crash when instance is not found
-  Fix I8254x crash while exhausting frame burst
-  Fix WIBU check in installer
-  Add EC_LINKIOCTL_GET_LOGLEVEL and EC_LINKIOCTL_SET_LOGLEVEL to all LinkLayer
-  Add GetNdisVersion() and GetEcatNdisVersion() to NDIS Updated to EcatNdis Drv V3.1.3.1
-  Fix access violation in emConfigApply() called just after emConfigLoad() with an non existing ENI
-  Change EC_T_REAL to float, add EC_T_LREAL as double
-  Updated to atemsys V1.4.16. 
   - Fix Xenomai3 on ARM 
   - Add support for Device Tree Ethernet driver and PCI driver with Xenomai3
   - Fix PCI DMA address translation on ARM

V3.1.2.10
*********

**Enhancement**

-  Extend EC_T_FRAME_RSPERR_DESC with wCycFrameNum and dwTaskId
-  Add TaskId support to the internal benchmarks
-  Add new eUsrJob_StartTask / eUsrJob_EndTask jobs for more detailed benchmarks (adds time between TaskStart and BenchmarkStart)
-  Remove dwTaskId parameter from emPerfMeasInternal\* Api and add a separate emPerfMeasInternal*ByTaskId Api

**Fixes**

-  Fix crash in BlockNode and OpenBlockedPorts due to missing state machine order context for port operation
-  Fix access violation if cyclic frames delayed because of bad timing and multiple cyclic entries are configured (broken since V3.1.2.05)
-  Fix Hot-Connect detect group notification counter in case no mandatory slaves are configured
-  Fix access violation when ExecJob is used, while the master is deinitializing (broken since V3.1.2.03)

**Platform**

-  Fix KSZ9031 handling in PhyLib and for CPSW
-  Add RMII support to CPSW
-  Add new Pru-Icss firmware to emllICSS
-  Fix OsWaitForEvent on Xenomai. Timeout values must convert to ticks before passing to Xenomai API.
-  Update atemsys.cpp for VxWorks70 RTP to V3.1
-  Include EcatDrv.sys in Class-B delivery for Windows

V3.1.2.09
*********

**Enhancement**

-  Add EC_IOCTL_SET_DIAGMSG_CODE_BASE
-  Improve pcap recorder timestamps using OsPerfMeas

**Fixes**

-  Fix access violation in ecatResuceScan under some bus mismatch circumstances
-  Fix DC state machine canceling if continuous propagation delay measurement is enabled

**Platform**

-  Add ARM 32Bit support for Xenomai 3 Cobalt
-  Updated to atemsys V1.4.15
   - Fix API version IOCTLs
   
-  Fix missing signal handler for SIGINT, SIGTERM on QNX
-  Fix EcatDrv to support AuxClk period < 16ms
-  Add 64Bit DMA support for RTL8169
-  Updated to atemsys V1.4.14 
   - Fix for arm/aarch64 kernel >= 5.10.00 
   - Add support for 64Bit DMA Memory 
   - Add support for PCI DMA address translation

V3.1.2.08
*********

**Enhancement**

-  Add support for OEM in combination with eCnfType_ConfigData

**Fixes**

-  Fix ecatConfigureMaster returns EC_E_NOMEMORY for configurations without MasterSyncUnitInfos on TI RTOS
-  Fix occassional acyc MasterRed frame loss

V3.1.2.07
*********

**Enhancement**

-  Add PerMeas internal APIs over RAS: PerfMeasInternalReset, PerfMeasInternalGetRaw, PerfMeasInternalGetInfo, PerfMeasInternalGetNumOf
-  Add EC_T_PERF_MEAS_INFO::dwBinCountHistogram for ecatPerfMeasInternalGetInfo
-  Store 200 PCI device in the lookup table instead of only 64

**Fixes**

-  Fix first call to emExecJob after emInitMaster returns EC_E_DISCONNECTED
-  Master OK bit set if EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE = false and ENI contains zero slaves
-  Fix crash in PerMeas Histogram due to incorrect range calculation

**Platform**

-  RIN32M4: Add Interrupt Mode support
-  DW3504: Add device PCI ID 0x4B32
-  Fix PHY Lib - auto negotiation
-  Fix AllocSendFrame for emllProxy
-  Fix Interrupt Mode for GEM on AARCH64/ARM64
-  Add LAN743x support for Linux
-  Add EC_T_OS_PLATFORM_PARMS::bConfigMutex, nMutexType and nMutexProtocol for Linux

V3.1.2.06
*********

**Enhancement**

-  Add emGetMasterStateEx() API

**Fixes**

-  Fix erroneous permanent frame loss in some cable redundancy link disconnected situation

**Platform**

-  Add AtemRasServer support for TI RTOS on TI AM654x
-  Add MAC address generation based on UID for STM32MP1 (DW3504)
-  Add Interupt mode for FslFec on AARCH64/ARM64
-  Fix for Linux kernel <= 3.16.00, Add HAVE_ACCESS_OK_TYPE define to handle non-mainstream API variance. Connect to interrupt via binded device tree - platform device
-  Add support for Xilinx Ultascale ARM R5 to FreeRTOS
-  Add bFilterInput parameter to WinPcap

V3.1.2.05
*********

**Enhancement**

-  ecatAoeGetSlaveNetId returns the Net ID even if the slave is not present

**Fixes**

-  Mailbox API return EC_E_INVALID_SLAVE_STATE instead of EC_E_INVALIDSTATE if slave state is invalid
-  Fix DCM BusShift / DCX system time shift only if needed
-  Fix esForceProcessDataBits for mutliple slaves' INPUTs
-  Fix slave transition sometimes canceled if the previous transition failed
-  Fix emSetMasterState returns EC_E_CANCEL immediatly, just after an internal BusScan occured in some cases
-  Fix complete access to objects 0xAnnn

**Platform**

-  Add Interrupt mode to emllICSS on AM335x-Boards
-  Add wait that previous frames have been sent instead of return EC_FALSE if TX queue is full to emllICSS for the AM57xx-Boards in interrupt mode
-  CPSW: Add support for VLAN header encapsulation
-  Add Interrupt mode to emllICSS on AM57xx-Boards

V3.1.2.04
*********

**Fixes**

-  Fix OsMeasCalibrate called when PerfMeas is disabled
-  Disable cyclic distribution during 64Bit bus time emulation start to protect against corrupted bus time

**Platform**

-  Add R-IN32M4-CL3 support
-  Add emllICSSG for TI AM654x on TI RTOS
-  Add EC_LINKIOCTL_GET_ICSS_STASTISTICS, EC_LINKIOCTL_SET_MSECCOUNTERPTR to emllICSS

V3.1.2.03
*********

**Enhancement**

-  Add EC_T_SLVSTATISTICS::qwReadTime and EC_T_SLVSTATISTICS::qwChangeTime
-  Add emCoeProfileGetChannelInfo(), see ETG.2000 V1.0.10, table 93
-  Add emFoeDownloadReq, emFoeUpoadReq to RAS SPOC default configuration
-  Add new performance measurement API
-  Add RAS SPOC opt-out support
-  Don't stop transition on DEVICE_STATUSCODE_APPLICATION_CONTROLLER_AVAILABLE

**Fixes**

-  Fix Mbx transfer always return with EC_E_TIMEOUT after slave error in PS or SO transition (broken since V3.1.1.05)
-  Create new frame if needed in case of EC_IOCTL_ADD_BRD_SYNC_WINDOW_MONITORING
-  Fix WKC recalculation for disconnectiong slaves in SAFEOP error state
-  Fix Master Object 0x3nnn, SubIndex 24ff not updated
-  Fix erroneous WKC error notification in case of not connected HC groups and EC-Master compiled with EXCLUDE_MULTIPLE_CYC_ENTRIES
-  Fix delay after NOP to await ports opened

**Platform**

-  Fix LinkOsCacheDataSync for ARM64 on Linux
-  Add Mac address for licensing via Microchip ATSHA204A for GEM 32Bit
-  AlteraTSE, add support for start-up with link disconnected
-  Fix ICSS TTS feature (broken since V3.1.0.17)
-  Add NXP i.MX RT1064 support for FreeRTOS
-  Add NXP i.MX RT1064 support for emllFslFec

V3.1.2.01
*********

**Enhancement**

-  Unified naming of PCI device id definitions
-  Clear slave error registers in a single frame to avoid disturbance of acyclic communication in case of bad ESC (frame corruption)
-  Add EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC::wWkc
-  Add EC_IOCTL_SET_STOP_TRANSITION_ON_PDI_WATCHDOG
-  Add EC_IOCTL_GET_MASTER_MAX_STATE
-  Add emConfigGet

**Fixes**

-  Fix BusShift takes too much time to synchronized on start (broken since V2.9.2.11)
-  Remove EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR on SetMasterState time-out
-  Fix ecatGetSlaveInpVarInfoNumOf returns EC_E_NOTFOUND for not connected slaves
-  Fix ecatGetCfgSlaveEoeInfo copy full szDnsName
-  MasterRed: Fix cyclic EC_NOTIFY_SLAVE_STATECHANGED with unknown state for absent slave if notification enabled at INACTIVE Master

**Platform**

-  Updated to atemsys V1.4.12 
   - Fix for kernel >= 5.11.00 
   - Add support for 64Bit IO Memory of PCI card
   
-  NDIS: Set promiscuous mode
-  DW3504: Support Intel Atom (Elkhart Lake) adapter

V3.1.1.07
*********

**Fixes**

-  Delay initial BRD after NOP to wait ports opened
-  Fix wrong DcStartTime in some combined use of EC_T_DC_CONFIGURE::dwDcStartTimeGrid and EC_IOCTL_DC_SETSYNCSTARTOFFSET
-  Default DCM SetVal set to 20% like in EcMasterDemoDc
-  Make DCM settings persistent between ecatConfigureMaster calls

**Platform**

-  i8254x: Fix initial link status info if startup disconnected
-  i8254x: Don't auto negotiate to 1 Gbits
-  i8254x: Fix not sending frames if started disconnected

V3.1.1.06
*********

**Fixes**

-  CableRed: Enable ResetOnDisconnect automatically for I8254x
-  Fix Master Object 0xAnnn "Diagnosis Data" symmetrical to 0x8nnn
-  Fix Master Object 0x2001 "Master State Summary"
-  MasterRed: Detect line break if frames sent on different lines received on same line
-  Discard process data variables outside Process Data Image e.g. variables from "Image-Info" in TwinCAT are out of allocated "Image"
-  MasterRed: Add EC_NOTIFY_SLAVE_STATECHANGED at inactive master
-  Add optional parameter "--mac" for emllSimulator
-  Fix RAS Server default port for EcSimulatorHilDemo
-  Fix occassional frame loss for ESC type 5 (assume "Auto-Close" supported) affects e.g. Beckhoff CU1521

**Platform**

-  Windows: Call timeBeginPeriod(1) in each created thread to support W10 2004
-  VxWorks: Add instance identification by PCI location
-  I8254X: ResetOnDisconnect OptIn, Disable LPU, Wait for FW on Reconnect
-  Updated to atemsys V1.4.11 
   - Fix for kernel >= 5.5.00 with device tree
   - Fix Device Tree Ethernet driver support for DW3504 
   - Fix PCI driver: only for kernel >= 4.4.00
   
-  RTOS-32: Add missing Heap Lock in LinkOsMapMemory / LinkOsUnmapMemory
-  Fix ecatSetLicenseKey for PPC
-  Linux: Link pthread and rt libraries to libemllI8254.so to protect against mixed calls
-  Linux, QNX6, QNX7, VxWorks69: Fix symbol "not found" error in DW3504 (broken since V3.1.0.17)

V3.1.1.05
*********

**Fixes**

-  Fix unexpected EC_NOTIFY_FRAME_RESPONSE_ERROR in case of limited acyclic commands per cycle
-  Fix possible signed integer overflows reported by LLVM
-  Fix "Too many cyclic commands in frame" for valid EtherCAT cyclic frame. Increase internal constant MAX_NUM_CMD_PER_FRAME from 100 to 114

**Platform**

-  Fix Windows Dongled delivery
-  Fix systematic crash using EC-WinRTOS-32 EcMaster.dlm Protected
-  Fix Object 0x2007 "Add History Diagnosis Message Command" for PPC

V3.1.1.04
*********

**Enhancements**

-  Add Master OD Object 0x2007 "Add History Diagnosis Message Command"

**Fixes**

-  Fix MSU WKC state errors for LRW commands split across two frames
-  Fix endless loop in bus scan in case of topology change manual mode
-  Fix additional line break criteria at inactive Master
-  Fix duplicate bus scan on getting active for Master Redundancy
-  Fix unexpected EC_NOTIFY_FRAME_RESPONSE_ERROR after re-configure master
-  Fix ecatNotifyApp returns notified client count instead of error code

**Platform**

-  Fix emllI8254x TX stucking after cable reconnection if cable was disconnected for more than 10s
-  Fix emNotifyApp (AtemRasClient) for PPC
-  Add device ID 0x2600 for Killer Networking E2600 to RTL8169

V3.1.1.03
*********

**Enhancements**

-  Add additional line break criteria at inactive Master
-  Add RAS server stack size parameter
-  Add file rotation to Pcap Recorder

**Fixes**

-  Fix unexpected EC_NOTIFY_SLAVES_PRESENCE = false for all slaves in case of slaves disappear in quick succession
-  Add EC_T_MASTER_INFO::RedundancyDiagnosisInfo
-  Fix Object 0x2003 Redundancy Diagnosis Object not updated on red link disconnect

**Platform**

-  Fix PhyLib (TI DP83867) for GEM
-  Add device IDs for several I219 and I225LM to EcatDrv
-  Fix sporadic crash during cable disconnection on I219

V3.1.1.02
*********

**Enhancements**

-  Enhance slave identification in case of missing slaves at the beginning and permanent frame loss at main
-  Change memory logging message level from EC_LOG_LEVEL_VERBOSE to EC_LOG_LEVEL_VERBOSE_CYC
-  Fix emInitMaster invalid parameters logging
-  Remove warning about unknown "SdoAccess" (ignore)

**Fixes**

-  Fix MbxTferObject pointer in EC_NOTIFY_MBOXRCV
-  Fix SDO abort code command size for raw mailbox command responses
-  Remove interface locking from ecatGetSlaveState (usage in JobTask)

**Platform**

-  Fix ICSS receive hang-up on broken frames
-  Add PACKET_MMAP for ReceiveFrame in SockRaw
-  Fix emllFslFec maximum receive buffer size
-  Add timing task based on clock_nanosleep to the Linux examples
-  Add support for PHY Lib to GEM
-  Updated to atemsys V1.4.10 
   - Fix Device Tree Ethernet driver: Mdio/Phy sup-node, test 4.6.x   kernel
   - Add Device Tree Ethernet driver support for GEM 
   - Fix PCI driver: force DMA to 32 bit

-  Fix emllFslFec cache data synchronization issues under high memory usage
-  Fix LinkOsMemoryBarrier for Linux and Xenomai x86-64
-  Fix LinkOsMemoryBarrier for QNX 7.1 x86-64

V3.1.1.01
*********

**Enhancements**

-  Add OsReplaceQueryMsecCount

**Fixes**

-  Fix access violation in API called from the job task during ecatDeinitMaster
-  Fix race condition between CFrameSpy destructor and Job Task
-  Fix link stay masked by cable redundancy in disconnection/reconnection cases in interrupt mode

V3.1.0.20
*********

**Enhancements**

-  SDO Abort codes refractored and refreshed

**Fixes**

-  Don't re-trigger INACTIVE master on circulating last master red cyclic frame
-  Protect against unexpected frames during re-configure master

**Platform**

-  Add PHY Microchip KSZ9131 to PHY Lib
-  Fix emllFslFec for NXP i.MX8
-  Fix memory leak in SYSBIOS thread handling

V3.1.0.19
*********

**Enhancements**

-  Use verbosity passed via command line for the RAS Server in the EcMasterDemoRasServer example
-  Add debug message for memory allocations inside EC_TRACE_ADDMEM_LOG
-  Add Memory Footprint Measurements to RAS Server and Examples
-  Add Memory Footprint Message to Demos
-  Enhance DCX to remove constant offset between the two system times for topologies with the EL6695 as the first DC-capable slave in both networks
-  Notify EC_LINECROSSED_INVALID_PORT_CONNECTION at first slave in case of invalid connection detected (unsupported topology)
-  Add frame timestamp to pcap file reader
-  Add device info of INACTIVE Master to forwarded cyclic master red frame
-  Enhance performance impact of EC_T_INIT_MASTER_PARMS::bApiLockByApp

**Fixes**

-  Fix external memory provider requested twice without release during call to ecatGetProcessData
-  Always wait for DC InSync just after DCM InSync in PS transition
-  Fix erroneous line crossed detection for cycle time below 1ms
-  Fix cascaded spinlock usage leading to deadlock under some OS
-  Refresh device info at INACTIVE Master needed to send on one line only
-  Fix AoE command header length calculation (broken since V3.0.1.21)
-  Fix endless loop in bus scan until timeout sometimes at startup

**Platform**

-  Fix thread affinity setting for Xenomai
-  Fix AuxClkTask for Xenomai
-  Updated to atemsys V1.4.09 
   - Add atemsys as PCI Driver for Intel, Realtek and Beckhoff 
   - Add memory allocation and mapping on platform / PCI driver device
   - Fix PHY driver for FslFec 64Bit
   
-  Add 64Bit support for emllCCAT
-  RTOS-32: Bad DMA memory address handling if base is > 2GB leading to permanent frameloss
-  SHEth, support for fixed link
-  Add device IDs for I219 and I225LM
-  Update VxWorks7 from SR540 to SR620
-  Add NXP i.MX 8M support for emllFslFec
-  Fix Interrupt Mode for Xenomai3_x64Cobalt
-  Fix parallel usage of emllNDIS and Wireshark
-  Add Secure Boot support to EcatDrv for Windows

V3.1.0.18
*********

**Enhancements**

-  Add EC_T_INIT_MASTER_PARMS::bApiLockByApp parameter to increase performance by disabling API locks
-  Add EC_IOCTL_SET_MASTER_MAX_STATE
-  Remove unnecessary locks in ecatGetCfgSlaveInfo, ecatGetCfgSlaveEoeInfo to increase performance

**Fixes**

-  Stop Slave Statistics during ecatConfigureMaster()
-  Immediately process Acyclic Master Redundancy Frames sent on one line only
-  Fix occasional illegal unlock if compiled with EXCLUDE_INTERFACE_LOCK

**Platform**

-  Add license check for Snarf

V3.1.0.17
*********

**Enhancements**

-  Add EC_IOCTL_SET_IGNORE_SWAPDATA

**Fixes**

-  Drop old queued frames in case of permanent frameloss detection in case of Master Redundancy
-  Fix erroneous EC_T_CFG_SLAVE_INFO::wWkcStateDiagOffsOut returned if FMMU is spread over multiple cmds
-  Fix ecatBadConnectionsDetect for cable redundancy topologies

**Platform**

-  Add support for interrupt mode on ICSS and allow more send output per cycle by using all send queues.
-  Fix CRC error handling for FslFec
-  DW3504, new Synopsys DW IP 4.0 (STM32MP157)
-  Add instance identification by PCI location for RTX
-  Fix assert in OsQueryMsecCount for Xenomai on startup
-  atemsys V1.4.08: 
   -  Fix Xilinx Ultrascale 
   -  Fix cleanup of Device Tree Ethernet driver

V3.1.0.16
*********

**Enhancements**

-  Add emIsConfigured()
-  Add HC mode echm_manual_noreset

**Fixes**

-  Master Redundancy: Refresh link status of both potential forward devices
-  Wait for eventually started topology change delay in ecbtsms_writeportctl
-  Fix blocked mailbox transfers (VoE, AoE, SoE) in case the previous transfer was stopped unexpectedly
-  EC_STA: Add EC-Simulator OD reading support
-  Change InitCmd time out type from EC_T_WORD to EC_T_DWORD (ENI data type)
-  Fix port stay closed until EC_IOCTL_SB_ACCEPT_TOPOLOGY_CHANGE is called in topology change manual mode
-  Fix process data corruption in some cases if swapdata is used in ENI
-  Fix memory leak in FrameSendAndFree for CableRed/MasterRed configurations
-  Set nBitOffs in parenthesis in SETBIT and CLRBIT macros fixing their usage in case of complex expression

**Platform**

-  Fix memory leak for allocated tx descriptors after reset in emlli8254x
-  Add AARCH64/ARM64 support for emllFslFec (NXP i.MX8)
-  Fix link to not come up at the lowest possible speed for Intel Pro/1000 (i8254x)
-  Fix NDIS link layer verbose log message start up crash
-  Add PHY access and PHY Lib to RTL8169
-  Add NoPhyAccess Parameter to RTL8169
-  Fix atemsys COPYING file format to match MD5 checksum for Yocto Linux
-  Fix SYSBIOS Timer
-  Updated to atemsys V1.4.07, Add support for NXP imx8 (FslFec 64bit)

V3.1.0.15
*********

**Enhancements**

-  Show cyclically performance values if -perf and -v >= 2
-  Add EC_T_LINK_CONNECTED_INFO
-  Remove deprecated function LinkOsInterruptDone()

**Fixes**

-  Fix complete access for history objects (0x10F3) and notification counters (0x2004) objects
-  Repeat line crossed detection completely in case of DL status interrupt detected during the procedure (not only refresh DL status)
-  Fix race condition in mailbox command queueing/processing

**Platform**

-  Add support for CMSIS-RTOS (STM32)
-  Add LinkLayer STM32Eth (STM32)
-  Add support for RTX64 4.0
-  Add support for TI AM574x to ICSS
-  Add NoPhyReset Parameter to ICSS
-  Add support for Yaskawa/Profichip Antaios
-  Add static libs for Windows unrestricted (VS2015)
-  Linux / Xenomai: Updated to atemsys V1.4.06: -  Fix Mdio-Bus timeout for kernel >= 5.0.00 -  Add support for IOMMU/Vt-D for Linux
-  Fix AtemRasClient for PPC: EC_IOCTL_REGISTERCLIENT
-  Add static libs for Windows unrestricted (VS6)
-  Add link layer interrupt mode support for Windows

V3.1.0.14
*********

**Enhancements**

-  Add EC_T_DCM_CONFIG_DCX::dwMaxErrCompensableOnExtClockReconnect
-  Add EC_LOG_LEVEL_ANY to Logging interface
-  Avoid processing frames not matching the expected ones to protect against data corruption and access violation

**Fixes**

-  Fix EC_IOCTL_REGISTERCLIENT for mixed 32Bit / 64Bit connections in AtemRasClnt
-  Repeat receive times latching if new bus slaves recorded to detect missing receive times
-  Fix occasional frame re-processing in case of frame loss on one line only by Master Redundancy
-  Fix previously reconnected link remains masked even if other link disconnection detected
-  Fix EC_T_BUS_SLAVE_INFO:wMbxSupportedProtocols always returns 0
-  Fix skipped port receive times refresh in some case of slaves reconnection leading to erroneous topology detection
-  Don't execute hidden slave detection in case of unsupported topology
-  Don't reset automatically the port receive times at beginning of bus scan to avoid inconsistent information in case of cancel
-  Fix frame discard support for TX frame logging
-  Fix EC_T_SET_MAILBOX_POLLING_CYCLES_DESC packing
-  Fix InitCmd erroneously retried even if InitCmd timeout elapsed under some circumstance
-  Stabilize slave state machine immediately during canceling if no InitCmd pending
-  Fix missing Link up bit in object 0x2001
-  Fix ecatConfigExtend() returns EC_E_LINK_DISCONNECTED if called just after ecatInitMaster()

**Platform**

-  Fix Sybios OsMeasCalibrate()
-  Fix PHY Lib Device Tree Ethernet driver wait for PHY link
-  | Updated to atemsys V1.4.04: | Fix Device Tree Ethernet driver robustness | Add Device Tree Ethernet driver support for ICSS
-  Continue to probe all Bus/Dev/Func in RTX64 even if 0 is returned
-  Add PHY Lib support to ICSS
-  Add PhyAddress and PhyInterface Parameter to ICSS
-  Add PHY Lib support to FslFec
-  Add PHY Lib for handling known PHY's and OsDriver for all LinkLayers, starting with the current FslFec implementation

V3.1.0.13
*********

**Enhancements**

-  Add frame buffers count parameter to RTL8169 (dwRxBuffers/dwTxBuffers)
-  Linux / Xenomai: Updated to atemsys V1.4.03: -  Add log level (e.g. “insmod atemsys loglevel=6”)
-  Add EC_T_ADS_ADAPTER_START_PARMS::cpuAffinityMask
-  Add EC_T_MBX_GATEWAY_SRV_PARMS::cpuAffinityMask

**Fixes**

-  Byte wise access to EC_T_UINT64 (EC_SETQWORD / EC_GETQWORD) for ARMv6 to protect against unaligned access
-  Avoid processing frames not matching the expected ones to protect against data corruption and access violation
-  Fix access violation under some init/deinit race condition in EoELinkFreeSendFrame()
-  Fix CPU affinity for AtemRasSrv

V3.1.0.12
*********

**Enhancements**

-  Tolerate ESC without 0x410 register implemented
-  Adapt the DCX timestamp refresh method according the memory provider configuration
-  Use InitCmd timeout to ack pending slave error at the beginning of the transition (even if EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED not used)
-  Ignore PDI watchdog errors during a transition in which all InitCmds return successfully
-  Add ecatBadConnectionsDetect and ecatBadConnectionsReset
-  Add flags ECAT_LINK_FRAMEFLAG_CLOSE_JUNCTION_RED_PORT, ECAT_LINK_FRAMEFLAG_OPEN_JUNCTION_RED_PORT to EC_T_LINK_FRAMEDESC

**Fixes**

-  Don't force mailbox read in case of WKC = 0 to protect against endless situation
-  Fix unexpected automatic port opening in manual topology change mode (EC_IOCTL_SB_SET_TOPOLOGY_CHANGE_AUTO_MODE = EC_FALSE)
-  Refresh DL Status at the end of ecatConfigExtend() to process new slave connection(s) masked during ecatConfigExtend()
-  Fix endless mailbox polling during MbxInitCmd if slave has no mailbox data
-  Fix unexpected delay in ecatConfigureMaster if job task not running
-  Don't overwrite link layer log parms during ecatInitMaster()
-  Generate EC_NOTIFY_DC_SLV_SYNC OutOfSync at falling transition to INIT (broken since V3.0.0.06)
-  Fix erroneous line crossed detection during repeated junction redundancy line break in the middle
-  Fix EcMasterDemoRasClient connect to legacy servers
-  Fix MasterShiftByApp mode broken since (2.9.0.09)
-  Fix deadlock situation using linklayer in interrupt mode (function registered with EC_IOCTL_REGISTER_CYCFRAME_RX_CB called with internal lock)

**Platform**

-  Fix frame loss for several 100ms after ecatInitMaster() Intel Pro/1000 (i8254x)
-  Fix LinkOsGetPciInfo() under WinCE returns 0 memory BARs in case of 0 IO BARs are declared (broken since V3.0.0.12)
-  Add define NO_PCI_SUPPORT in LinkOSLayer.cpp for QNX to support platforms without PCI
-  Add AARCH64/ARM64 support for Intel Pro/1000 (i8254x)
-  Add to FslFec support atemsys as Device Tree Ethernet driver Allow to delegate whole PHY handling, PinMuxing and enable Clocks to Linux drivers via atemsys
-  | Updated to atemsys V1.4.02 | fix ARM/AARCH64 DMA configuration for PCIe and fix occasional   insmod Kernel Oops | register atemsys as Device Tree Ethernet driver "atemsys" and use   Linux PHY and Mdio-Bus Handling

V3.1.0.11
*********

**Enhancements**

-  Support ENI files generated with ESI using DynamicInputs / DynamicOutputs
-  Add INCLUDE_INTERFACE_LOCK
-  Fixed flash and add set license key
-  Add flag ECAT_LINK_FRAMEFLAG_ADD_INTERFRAME_GAP to EC_T_LINK_FRAMEDESC
-  Repeat frame to close/open junction red port 3 times to protect against permanent frameloss in case of frame doesn't reach both slaves successfully
-  Junction red port are closed only during port receive time latching command. Don't repeat Propagation delay measurement during DcInit and.
-  Apply EC_T_INIT_MASTER_PARMS::wMaxSlavesProcessedPerBusScanStep in DcSm and during hidden slave detection
-  Integrate EcSdoServ in EC-Simulator
-  Add INCLUDE_EXECJOB_REENTRANCY_SUPPORT

**Fixes**

-  Fix EoE-Endpoint registration downward compatibility with V3.0 in RAS client
-  Fix erroneous bus mismatch after excluding slaves from HC group
-  Fix drop old frames in queues
-  Fix occasionally circulating forwarded frames
-  Fix occasionally circulating forwarded frames by MasterRed
-  Fix hidden slave detection in junction redundancy topologies
-  Fix compile errors for various EXCLUDE\_ defines
-  Fix access violation in case of mailbox size smaller than SDO info header
-  Fix propagation delay measurement in junction redundancy topologies
-  Fix occasional duplicated send requests in AtemRasClnt
-  Fix segmented SoE transfers
-  Return EC_E_SDO_ABORTCODE_OFFSET if requested subindex greater than max sub index
-  Fix frame loss during propagation delay measurement and hidden slave detection in case of junction redundancy line break
-  Fix DCX (broken since V3.0.1.17)
-  Fix 0x2004 object definition to protect against invalid access by EC-Simulator
-  Fix occasional crash on invalid EtherCAT receiving
-  Fix occasional lock-up in JobTask in case of corrupt bus slave list
-  Fix missing EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL notification if slave disconnected and hot connect manual mode is used
-  Fix dead pointer usage in SendFrame
-  Fix potential memory leaks on reallocation
-  Fix resource leak if ecatInitMaster() fails
-  Unmask network adapter on disabling topology changed delay

**Platform**

-  Removed AuxClk support from QNX7
-  Fix CCAT for arm performance issue
-  Removed deprecated functions OsMakeThreadPeriodic(), OsSleepTillTick() and XenomaiOSWarnUponSwitch() from Xenomai OS-Layer
-  Removed OsMakeThreadPeriodic() and OsSleepTillTick() calls for Xenomai from all examples
-  Intel Pro/1000: Strip CRC
-  Fix assembly info properties for EC-STA, EC-EoEGateway, EcMasterDotNet.dll
-  Don't process RX frames with CRC error flag ETSEC
-  ICSS: MAC address reading and eval protection added
-  Add DCM MasterShift to SYSBIOS on AM3359
-  Fix PCI network adapter not found in VxWorks if adapter was behind more than 4 parent devices

V3.1.0.10
*********

**Enhancements**

-  Add EC_IOCTL_SB_SET_TOPOLOGY_CHANGED_DELAYS
-  Add wInitCmd to EC_IOCTL_SET_MASTER_DEFAULT_TIMEOUTS
-  Add max. client count to RAS Server

**Fixes**

-  Fix unmask send at reconnected device for INACTIVE Master for Master Redundancy
-  Fix apply topology changed delay at INACTIVE Master for Master Redundancy
-  Fix propagation delay calculation in case of junction redundancy line break
-  Fix endless order cancelling situation if cable reconnection occurs during first buss can triggered by first ecatSetMasterstate
-  Fix cable red bit for acyclic master red frames send on one line only for Master Redundancy
-  Fix reading slave MbxOut size from Diagnosis Interface for MbxGateway
-  Fix erroneous bus mismatch notification on startup
-  Fix ecatNotifyApp return EC_E_NOERROR on success
-  Fix crash in ESCTypeText in 64Bit
-  Fix occasional crash in AtemRasSrv during client connection due to uninitialized member variables
-  Report instead of crash in case of C++ to .NET marshalling error in EcMasterDotNet

**Platform**

-  Fix OsAuxClkDeinit
-  CPSW: EC_LINKIOCTL_UPDATE_LINKSTATUS not needed any more
-  CPSW: Fix start with link disconnected and link reconnection
-  FslFec: Add support for Toradex Colibri iMX7
-  FslFec, GEM: Add EC_LINKIOCTL_PHY_READ and EC_LINKIOCTL_PHY_WRITE
-  Linux / Xenomai: Updated to atemsys V1.3.16: -  Fix for API changes at kernel >= 4.18.00 -  Fix for ARM DMA allocation for PCIe
-  LxWin: Fix link layer integration
-  QNX: Fix IO memory mapping under 32Bit (regression since V3.1.0.07)
-  SockRaw: optionally replace Ethernet padding with NOP commands
-  VxWorks70: Use vxbDmaEndBufLib instead of legacy API
-  VxWorks70: Fix bad physical memory handling (32/64Bit)
-  Windows: AuxClk fallback to kernel timer implementation if no interrupt assigned to ECAT driver for LocalApic implementation

V3.1.0.09
*********

**Enhancements**

-  Add EC_LINKIOCTL_SET_LINKSTATUS to I8254x
-  Add segmented CoE up- and download to EcMbxGatewayClient

**Fixes**

-  Fix acyclic slave frames occasionally erroneously dropped on foreign frame receiving for Master Redundancy

**Platform**

-  Add support for AARCH64 to FreeRTOS
-  Add EC_T_OS_PLATFORM_PARMS::bUseKernelTimerForAuxClk for Windows

V3.1.0.08
*********

**Enhancements**

-  Fix parsing variables of Specific Data Types
-  Move EoEGateway config file location to executable's folder
-  Add MAC protection to CCAT

**Fixes**

-  Fix fairness in mailbox scheduling
-  Fix unexpected slave transition during startup if fullmanual mode is used
-  Fix erroneous behavior if slave disconnected during ecbtsms_chkwrttmpaddr
-  Set EoE TAP threads priority below JobTask/ReceiveThread Priority

V3.1.0.07
*********

**Fixes**

-  Fix INACTIVE to ACTIVE MasterRed INPUTs in case of line break
-  Fix ACTIVE to INACTIVE MasterRed OUTPUTs flashing in EcMasterDemoMasterRed
-  Fix missing EC_NOTIFY_SLAVE_PRESENCE if permanent frame loss during startup
-  ProcessAllRxFrames (interrupt mode): Flush frames received on only one line: Prepone processing of frames (same cycle, not at permanent frame loss handling)
-  Fix EC_T_PROCESS_VAR_INFO_EX::wWkcStateDiagOffs (ecatFindInpVarByNameEx, ecatGetSlaveInpVarByObjectEx, ecatGetSlaveInpVarInfoEx)
-  Fix EoE retry access period if bus cycle less than 1ms
-  Add support for ARM (am5728) and CPSW to SylixOs
-  Add support for Renesas RZN1D Board to DW3504 Link-Layer

**Platform**

-  Updated to atemsys V1.3.15 -  Fix crash while loading kernel module on ARM64 -  Add support for kernel >= 5.0.00…
-  Fix discard of frames with CRC errors for FslFec Link-Layer
-  Add support for Xlinix Zynq Ultrascale(ARM64) for GEM Link-Layer
-  Add support for ARM / CX9020 to CCAT Link-Layer

V3.1.0.06
*********

**Fixes**

-  Added myAppWorkpdMasterRed
-  Fix overwriting data with data from previously ACTIVE Master on take-over
-  For all examples execute myAppWorkPd() only for SafeOP and OP
-  Fix EC_IOCTL_GET_SLVSTATISTICS for PPC
-  Stop invalid mailbox InitCmds
-  Fix EC_IOCTL_DC_SLAVE_CONTROLLED_BY_PDI for PPC
-  Fix ecatSetMasterState lock-up if DC initialization canceled
-  Fix race condition during emConfigExtend accessing to BusSlave objects
-  Fix memory leak in EoE-Endpoint LinuxTAP
-  Add ecatGetCfgSlaveEoeInfo
-  Add vlan support to EcMasterDemo (EC-Master library must be compiled with VLAN_FRAME_SUPPORT)
-  Add parameter "-play" to llAccept to send frames from pcap trace to network
-  Fix compilation of llAccept
-  Fix occasional circulating bit inserted to cyclic master red frameProcess instead of drop frames with slave data on red device flush
-  Exclude MasterRed frames from slave frame loss monitoring

**Platform**

-  Fix EC-Win packaging
-  Add EC-WinLx support
-  Enable ResetOnDisconnect by default for Intel Pro/1000 Generally needed for CableRed
-  Log PCI info including device ID for Intel Pro/1000
-  Re-enable interrupt in Intel Pro/1000 for "ResetOnDisconnect"
-  Add Linux aarch64
-  PRUICSS LinkLayer add support for dcm mode LinkLayerRefClock
-  Fix time stamping on send frame for emllAlteraTSE, emllEG20T, emllEMAC, emllICSS, emllNdisUio, emllR6040, emllRIN32M3, emllRZT1, emllSnarf

V3.1.0.05
*********

**Fixes**

-  Fix endless loop in BT state machine if returning frame setting station address is corrupted
-  Fix AtemRasClient for PPC: EC_NOTIFY_RAWCMD_DONE
-  Fix McSm order logging for multi-instance
-  Fix logging ForeignCyclicMasterRed CmdFlags
-  Fix WKC of empty acyclic master red frames
-  Fix erroneous transition during slave identification if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT is used and transition to INIT takes a long time
-  Fix erroneous timeout during ecatSetMasterState() for LinkLayerRefClock and MasterRefClock modes if no DC slave is present
-  Fix erroneous timeout during DC initialization if bus cycle less than 1ms because of endless loop during receive times latching
-  Don't skip DC initialization if no configured DC slaves connected and EC_IOCLT_DC_FIRST_DC_SLV_AS_REF_CLOCK is used
-  Fix handling of EK1200 (Beckhoff CX)
-  Fix race condition between ecatSetMasterState() and topology change handling regarding DC initialization

**Platform**

-  Probe Local APIC timer usage for Windows
-  Fix FreeRTOS DMA allocation
-  GEM force LED mode to blink for activity on PHY Microchip KSZ9031RNX

V3.1.0.04
*********

**Enhancements**

-  Support parallel usage of AuxClk and optimzed linklayers for Windows
-  Add LinkOsSetThreadAffinity, LinkOsGetThreadAffinity for VxWorks

**Fixes**

-  Send acyclic master red frames on both devices and handle frame loss
-  Enhance circulating frame protection for junction redundancy
-  Use first DC slave as RefClock again if RefClock is optional
-  Fix crash during ecatConfigExtend if link disconnect
-  Avoid circulating frames when opening ports after junction red line fix
-  Fix acyclic frame processing for repeated lost frames with mailbox commands NOP
-  Check if DL status interrupt detected just after port receive times latching to protect against incoherent values generating invalid topology
-  Fix unexpected EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR with error "PDI watchdog" in continuous transitions (INIT->OP)
-  Remove automatic mailbox read after VoE write. Restart stuck mailbox read if mailbox write returns WKC = 0
-  Check if DL status interrupt detected just after port receive times latching to protect against incoherent values generating invalid topology
-  Read mailbox first before retrying MbxCmd WKC = 0 because some slaves reject MbxIn access as long as MbxOut is full
-  Prevent data corruption if error detected just after extended config has been applied during ecatConfigExtend()
-  Don't remove acyclic frame from pending queue in case of mismatching acyclic frame, but allow further processing and retrying
-  Fix invalid read access during eCnfType_GenPreopENI
-  Fix erroneous expected WKC if DL status read command corrupted during DL status irq
-  Force mbx read to read eventually next MbxOut after repeating mailbox done
-  Fix memory corruption during ecatConfigExtend if slave SII length exceeds internal buffer
-  Read mailbox first before retrying MbxInitCmd because some slaves reject MbxIn access as long as MbxOut is full
-  Prevent for repeated DC initialization during topology change handling if master is in PREOP
-  Fix distance between receive times latching and reading too short if done by acyclic command generating bad topology detection / erroneous line crossed
-  Fix erroneous slave detection in several cases of slave disabled / disconnected and mismatching slave is connection
-  Fix erroneous slave disappear in some case of slave disconnection while writing the temp fixed address
-  Fix crash in Intel Pro/1000 EcLinkSendFrame on non-allocated frame
-  Fix building OS-Layer for RTOS-32 using Borland Compiler
-  Fix RTX64 DLL exports

V3.1.0.03
*********

**Enhancements**

-  PRUICSS LinkLayer TTS parameter moved to new descriptor EC_T_LINK_TTS
-  Save error only acknowledged by ecatSetSlaveState() not ecatSetMasterState() if EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED used

**Fixes**

-  Fix CoE transfer size calculation in case of Complete Access in EC-STA
-  Fix occasional crash on retransmissions of SoE / VoE mailbox transfers
-  Fix erroneous bus mismatch returned at line break occasionally (broken since V3.0.1.47)
-  Fix mailbox management locking
-  Only stop PS and SO transitions because of PDI watchdog expired. Other transitions continue until timeout and return EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR.
-  Calling ecatSetSlaveState always generates EC_NOTIFY_SLAVE_STATECHANGED even EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR
-  Fix endless loop in some case of mis connection (broken since V3.0.1.43)
-  Fix slave state machine stuck for the extended slave (broken since V3.0.1.47)
-  Fix bad propagation delay because of timestamp overflow
-  Don't notify EC_NOTIFY_SLAVE_STATECHANGED beore InitCmds in II or PP transition
-  Use timeout of OSP_I transition for slave error acknowledgment if EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED is used
-  Fix WKC recalculation in case of SafeOpError and according 1Byte PDO setting
-  Fix erroneous system offset if DC slave connected before previous first one and eDcmMode_LinkLayerRefClock is used
-  Fix erroneous timeout elapsed during slave identification
-  Probe register 0x0210 for ESC Type 2
-  Fix CRC protected EEPROM area always at once for PowerPC
-  Fix instance identification by PCI location for QNX
-  Fix EC_NOTIFY_RAWCMD_DONE for ecatQueueQueueRawCmd via RAS
-  Fix memory leaks in ecatDeinitMaster if splitted frame processing is enabled and compiler switch EXCLUDE_MULTIPLE_CYC_ENTRIES set

**Other Changes**

-  Refactor EC_T_SLVSTATISTICS_DESC
-  Changed .NET 4.0 Client Profile instead of .NET 2.0 for Windows x86
-  Removed EcMasterDemo2
-  Removed obsolete parameter from ecatTferSingleRawCmd, ecatQueueRawCmd, ecatClntQueueRawCmd, EC_T_MBX_DATA::dwFoETransferredBytes

V3.1.0.02
*********

**Enhancements**

-  Write CRC protected EEPROM area always at once
-  Always return identification value based on Omron GX-JC06-H main device for sub device if main device provide it by rotary switch

**Fixes**

-  Fix link layer parameter handling for DW3504, ETSEC, GEM, I8254x, R6040, RTL8169, SHEth
-  Fix crash in topology resynchronization if there are more slaves on the bus than expected. Only with complier switch EXCLUDE_HOTCONNECT
-  Fix topology change delay applied on cable reconnection
-  Apply identification fallback method if configured method failed by timeout
-  Pending error acknowledgment move from API to slave state machine

V3.1.0.01
*********

**Enhancements**

-  OS-Layer / LinkOsLayer refactoringOsDeleteThreadHandle, OsSetThreadPriority, OsSetThreadAffinity, OsGetThreadAffinity
-  Add support for EC_LINKIOCTL_SET_LINKENABLED with EC_LINKENABLED_ONLY_SEND for interrupt mode
-  Enhance line cross detection inside junction redundancy line
-  Allow topology changed to cancel current topology changed handling as soon as scan bus finished
-  Reorder InitCmds for Omron slaves to protect against WKC error during raising transitions to SAFEOP
-  Separate OS-Layer / LinkOsLayer
-  Suspend read slave statistic while topology is unknown
-  If timeout elapsed during receive times latching with cyclic command in DC state machine, try with acyclic command
-  Increase default order timeout to 20s to cover DC Initialization
-  Rename EC_IOCTL_DC_REF_CLOCK_CONTROLLED_BY_PDI to EC_IOCTL_DC_SLAVE_CONTROLLED_BY_PDI
-  Don't check 0x0210 during DL status interrupt handling, but directly read 0x0110
-  Enhance detection of line crossed slave position
-  Allow EEPROM filled with zeros for GenOpENI

**Fixes**

-  Fix Object 0x2001, Bit 9 "Master in requested State"
-  Slave absent at INACTIVE Master on link disconnection
-  Fix topology change handling at INACTIVE master (regression since V3.0)
-  Send acyclic master red frames only at adapter leading to other master (Support frame dropper connected to master port) (regression since V3.0)
-  Support permanent frame loss by cable redundancy again
-  Wait for DC at start of INIT transition in slave state machine if EC_T_DC_CONFIGURE::bDcInitBeforeSlaveStateChange is used
-  Fix using uninitialized system time offset reference slave during topology change handling
-  Don't re-read identification value if ADO is matching and value non zero
-  Ignore network changes explicitly during ecatConfigExtend() and ecatRescueScan() instead of only disabling port operations
-  Recalculate WKC just after the slave presence notification. Application get information in this order: WkcState = 1, Slave Disappear, WkcState = 0
-  Fix DC system time offset calculation for LinkLayerRefClock mode
-  Fix FoE busy handling during segmented transfer (emFoeSegmentedDownloadReq)
-  Fix endless loop in BusScan if new port connection is detected but topology change delay has been started
-  Only acknowledge topology change during in HcSm if port operation are enabled. Fix ConfigExtend() mask port connection detection
-  Reset bus slave candidate in config slave in SetSlavePresence() to protect against invalid access to freed memory
-  Consider error at transition start only if using EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
-  Fix invalid access to freed memory during reset of mailbox slaves in ecatConfigExtend()
-  Fix missed cable connection if disconnection occurs immediately after
-  Fix missing DC initialization of ref clock slave selected if EC_IOCLT_DC_FIRST_DC_SLV_AS_REF_CLOCK used
-  Don't stop systematically topology change delay if topology change detected to assure the delay before opening port
-  Fix wrong system time offset calculation if eDcmMode_LinkLayerRefClock used and DC system time offset ref slave disappear
-  Continue master state transition over several states even if slave occurs during transition.(EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE = true)
-  Set \_DLSTATUS_IN_PROGRESS if topology change detected without DL status IRQ
-  DL/AL status interrupt can interrupt topology change handling as soon as topology known
-  Set \_ALSTATUS_IN_PROGRESS if slave error detected without AL status IRQ
-  Fix FoE busy handling during segmented transfer (emFoeSegmentedDownloadReq)
-  Only acknowledge error in ecatSetSlaveState() if using EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
-  Increase receive times latching with cyclic command timeout to 3x cycle in DC state machine to protect against erroneous acyclic command method
-  Fix erroneous transition if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT and EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED used and transition to INIT take a long time
-  Fix parameter check in several mailbox related APIs
-  Fix erroneous topology detection in some junction redundancy cases if several junction slaves on the network and line break
-  Fix missing master state change in some case if state change request interrupted by AL or DL status interrupt
-  Fix erroneous expected WKC in case of slave with PDI watchdog expired cannot finish transition to INIT
-  Don't refresh or notify junction redundancy and line crossed information if build topology has not be bought during the scan bus. Fix invalid flags
-  Fix erroneous slave error notification if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT used and transition to INIT take a long time
-  Fix DC ARMW burst bulk in link layer mode
-  Update MSU management at INACTIVE Master for WKC validation at takeover (Regression)
-  Fix DC start time recalculation
-  If timeout elapsed during receive times latching with cyclic command, try with acyclic command
-  Wait for TopologyChange related order before inserting a new one
-  Fix transition failure if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT used and transition to INIT take a long time (broken since 3.0.1.33)
-  Fix missing config slave synchronization in duplicate slaves synchronization
-  Fix handling of duplicate slaves if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT used
-  Fix topology detection if consecutive slaves with matching fixed address (duplicate) are connected
-  Fix redundancy line RX frame counter
-  Call ForceSyncManagersEnabled(DEVICE_STATE_UNKNOWN) on slave disconnection. Fix erroneous WkcState errors (broken since 3.0.1.28)
-  Remove WKC adjustment in case of PDI watchdog expired spontaneously to support the use case that the slave recover by itself
-  Fix cyclic frame lost counter

**Platform**

-  Add Ansys to Realtek PCI device list
-  LxWin MAC eval license unlocking
-  Add instance identification by PCI bus address to QNX 6
-  Add DCM MasterShift to Renesas NoOs
-  Add support for Toradex Colibri imx6 to FslFec
-  Removed EC-Master linking from AtemRasClnt (Windows_x64)
-  Updated to atemsys V1.3.14 Fix edge type interrupt (enabled if Kernel >= 3.4.1, because exported irq_to_desc needed) Fix Xenomai Cobalt interrupt mode
-  Removed real_malloc, real_free wrappers from Xenomai

V3.0.1.36
*********

**Core**

-  Fix transition failure if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT used and transition to INIT takes a long time (broken since 3.0.1.33)
-  Fix missing WKC adjustment in case of PDI watchdog expired spontaneously if EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called
-  Fix erroneous canceling of eMcSmOrderType_TOPOLOGY_CHANGE generating bus mismatch just after eCnfType_GenPreopENI

V3.0.1.35
*********

**Core**

-  Fix erroneous EC_NOTIFY_CYCCMD_WKC_ERROR, if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED have been called (broken since 3.0.1.33)
-  Trigger eMcSmOrderType_TOPOLOGY_CHANGE at the end of ecatConfigExtend even if no bus slave has been added to the topology

V3.0.1.34
*********

**Core**

-  Trigger eMcSmOrderType_TOPOLOGY_CHANGE at the end of ecatConfigExtend instead of eMcSmOrderType_REQ_SB, to trigger DC state machine if needed
-  Fix junction redundancy line break detection at branching slave
-  Add EC_IOCTL_SB_SET_NO_DC_SLAVES_AFTER_JUNCTION
-  Reset PDI watchdog on transition start to stop failing transition faster
-  Validate target state in ecatSetSlaveState() and in StartInitCmd() and generate at least a generic EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR
-  Fix timeout in receive times latching during bus scan
-  Fix illegal access to removed bus slave if junction red tail slave disconnected during hidden slave detection
-  Fix temporary fixed address assignment for duplicated slaves

**Platform**

-  Add EC-EngineerWeb support (shared objects) for Linux

V3.0.1.33
*********

**Core**

-  Fix ecatRescueScan() stucks sometimes if cyclic frames permanent frame
-  Fix erroneous topology detection in some junction redundancy cases if several junction slaves on the network and line break
-  Don't stop transition if slave error or PDI watchdog have been detected at transition start

V3.0.1.32
*********

**Core**

-  State change because of ecatSetSlaveDisabled() / ecatSetSlaveDisconnect() triggered in slave OnTimer and not in API call to avoid race condition
-  Enhance ecatRescueScan to support line crossed topologies
-  Fix invalid expected WKC if AL status refresh executed during slave transition and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called
-  Fix missing EC_NOTIFY_SB_DUPLICATE_HC_NODE notifications
-  Fix returned object name in ecCoeGetEntryDescReq if object data contains unit type record

V3.0.1.31
*********

**Core**

-  Acknowledge AL-Status errors for new slaves on the network if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT is enabled
-  Fix endless resynchronization in case of slave with identification located at the end of the configuration have been connected at the begin of network
-  Refactor MbxState management with LogMsg
-  Wait for McSm becomes stable at the beginning of ecatConfigExtend()
-  Re-enable port operation at the very end of ecatRescueScan() to assure the repeatability of the function behavior
-  Fix WKC recalculation according PDI watchdog state and sync manager mode
-  Protect McSm Order enqueuing against race condition
-  Monitor port receive time and consider them missing if the value didn't change
-  Fix erroneous port open in hidden slave detection after ecatRescueScan()

**Platform**

-  Add OsReplaceGetLinkLayerRegFunc
-  Remove RTAI and RCX from demo applications

V3.0.1.30
*********

**Core**

-  Fix erroneous topology detection in some junction redundancy cases if several junction slaves on the network (OC#169)
-  Fix erroneous topology detection in some junction redundancy line break cases if several junction slaves on the network (OC#167)
-  Fix race condition in mailbox command queueing/processing
-  Reduce port time limit from 200 to 170 for EL9010 detection
-  Fix SetMasterstate() returns EC_E_TIMEOUT instead of EC_E_SLAVE_ERROR if PDI watchdog expired during transition

V3.0.1.29
*********

**Core**

-  Add API emGetSlaveOutpVarByObjectEx and emGetSlaveInpVarByObjectEx
-  Fix missing topology change detection during emConfigExtend()
-  Fix PDO to SyncManager assignment for slaves with 4 SyncManagers in one direction
-  Fix RescueScan frame loss after slave detection if there are multiple branching slaves in the topology
-  Fix missing EC_NOTIFY_SLAVE_ERROR_STATUS_INFO if emSetSlaveState() has been call before
-  Fix unexpected slave absence notifications if topology change happen during DL status handling
-  Repeat DC state initialization if it has been interrupted by topology changes during transition above INIT
-  Fix systematical frame loss during reconnection at red or main port

**Platform**

-  Enhance LinkOSLayer for Windows 10 to run a 32Bit Link-Layer on a 64Bit platform

V3.0.1.28
*********

**Core**

-  Avoid unexpected DL status interrupt handling caused by PDI watchdog monitor (since V3.0.1.25)
-  Fix erroneous EC_NOTIFY_CYCCMD_WKC_ERROR if transition failed before writing AL control and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called (broken since 3.0.1.27)
-  Fix port closed by RescueScan because of frameloss detection cannot be reopened enduring by ecatSetSlavePortState()
-  Reset WkcState monitoring counters during cyclic frame adjustment to protect against permanent bad WkcState
-  Fix race condition in DL status interrupt handling if slaves reappear in quick succession
-  Fix erroneous topology detection in some junction redundancy line break cases if several junction slaves on the network
-  Fix AtemRasClient: ecatScanBus returns busmismatch, line crossed,…
-  Fix AtemRasClient for PPC: FindProcVarByName

**Platform**

-  Updated to atemsys V1.3.13 Add ARM64 support
-  Add ARM64 support for RTL8169
-  Fix crash in EcMasterDemo for Xenomai3
-  PRUICSS LinkLayer force LED mode to blink for activity

V3.0.1.27
*********

**Core**

-  Enhance ecatRescueScan for topologies with more than one non EtherCAT device in a line. Reduce amount of slave presence notifications during ecatRescueScan
-  Fix Wkc recalculation in case of failing transistion due to a PDI watchdog interrupt
-  Resync on slave with matching identification after bus mismatch detected even if end of group is not fully present
-  Fix erroneous line crossed flags and junction red line information in some line crossed case or unexpected junction redundancy with line break
-  Fix AtemRasClient for PPC: ecatGetBusSlaveInfo
-  Fix ecatSetMasterstate returns no error even if slave disappear during transition (broken since V3.0.1.26)

**Platform**

-  Add AtemRasServer support to SylixOS x86 und x64
-  Fix stack overflow with Microsoft .NET Core on Linux
-  Updated to atemsys V1.3.12 Add atemsys API version selection. Share atemsys to V2.7 ... V3.0.

V3.0.1.26
*********

**Core**

-  Reset PDI watchdog expired state only after successful transition. eInitCmdErr_PDI_WATCHDOG returned even if detected before transition
-  Fix erroneous line crossed flags in case of junction red line break at head port B
-  Enhance mailbox state change response time if slave slicing is activated
-  Interrupt SetSlaveState request if DL status interrupt detected to detect PDI watchdog expired error

V3.0.1.25
*********

**Core**

-  Support junction red topologies containing slaves without receive times at all
-  Fix erroneous bus mismatch on reconnection of extended config slaves
-  Disable hidden slave detection during RescueScan
-  Fix DC handling of junction redundancy (broken since V3.0.1.24)
-  Protect against endless DL Status interrupt handling in case of permanent PDI watchdog expired state
-  Support line crossed detection for slave without receive time at processing unit
-  Add EC_IOCTL_DC_REF_CLOCK_CONTROLLED_BY_PDI
-  Restore exactly junction red port state during hidden slave detection and DC
-  Add EC_IOCTL_DC_ENABLE_ALL_DC_SLV
-  Fix RescueScan frame loss detection if frame loss occurs within a junction redundancy line
-  Fix occasional crash for custom dwMaxAcycBytesPerCycle values

V3.0.1.24
*********

**Core**

-  Skip hidden slave detection if unexpected connection has been detected to protect for permanent frame loss
-  Add frame discard support to frame logging
-  Fix erroneous PortSlaveIds in EC_T_BUS_SLAVE_INFO if ecatGetBusSlaveInfo is called during a DL status interrupt
-  Enhance junction redundancy detection/checks for unexpected/unconfigured junction redundancy lines
-  Fix commands to close and open ports sent in a single frame during hidden slave detection and DC initialization by junction redundancy
-  Ignore topology errors during ecatConfigExtend and ecatRescueScan
-  Fix ecatConfigExtend if unexpected bus slave becomes valid during extending bus scan because of delayed identification value
-  Fix resetting of junction redundancy flags in case of a topology change
-  Fix occasional crash for custom dwMaxAcycBytesPerCycle values
-  Fix ecatConfigExtend if slave identification fails several times
-  Fix erroneous line crossed detection under Windows by some random circumstances
-  Fix BusSlave still considered as unexpected after ecatConfigExtend() has been called and some config slaves were missing
-  Fix ecatGetSlaveProp() over RAS

**Platform**

-  FslFec Fix sporadical endless loops during PHY initialization
-  FslFec Support for PHY 8081
-  Add I8254x auto negotiation timeout parameter
-  Fix 64Bit OsMeasGetCounterTicks for QNX (ARM)
-  Extend PRUICSS LinkLayer for Emerson TI AM5728 Board

V3.0.1.23
*********

**Core**

-  Fix crash in ecatConfigExtend
-  Fix strict junction redundancy check for line crossed slaves in broken junction redundancy line
-  Fix segmented SDO download start with toggle bit set to 1
-  Add handling of remaining 32Bit Os Counter Tick Measurents for Performance Measurement
-  Enhance propagation delay calculation
-  Fix emGetslaveProp always return EC_FALSE (broken since V3.0.1.22)
-  Fix invalid read in ENI parsing if data type of variable is unknown

**Platform**

-  Fix 64Bit Counter Tick measurent for VxWorks at ARM

V3.0.1.22
*********

**Core**

-  Ignore pending PDI Watchdog by new connected slaves
-  Adjust LineCrossedFlags behavior
-  Enhance mailbox polling performance for running transfers
-  Add ecatGetMasterDump API
-  Add EcMbxGatewaySrv to AtemRasSrv
-  Reorganize Notifications while errors during InitCmds
-  Fix invalid read in EC_COPYBITS_INLINE (last byte at buffer with odd length)
-  Fix detection of unconnected Port A if junction redundancy is enabled
-  Don't consider return value of last ScanBus during ecatConfigExtend to not drop extended configuration in case of missing config slaves
-  EC_IOCLT_DC_FIRST_DC_SLV_AS_REF_CLOCK sets first slave with DC support as reference clock
-  Fix DC distribution in case of line break if reference clock is on red line
-  Fix crash under Windows 10 64Bit if linklayer instance not found
-  Fix mandatory slaves considered absent on MasterRed take-over
-  Notify slave presence at INACTIVE Master
-  Fix slave InitCmd response error after slave was in INIT with error

**Platform**

-  Configurable TX/RX DMA Desc buffer count for GEM, DW3504, R6040 and SHEth
-  Setup GMIItoRGMII converter independent of PHY access for GEM
-  DW3504 Remove cable connected check in EcLinkAllocSendFrame
-  Fix memory leak in emllPcap

V3.0.1.21
*********

**Core**

-  Fix missing bus mismatch on adding incomplete hot connect group
-  Add diagnosis info reset of 0xAnnn on writing 0xF200:16 (due to ETG.1510)
-  Fix diagnosis info reset object 0xF200:16 reading (due to ETG.1510)
-  Don't reset WKC error counter (0xAnnn:14) on slave disconnection (ETG.1510)
-  Fix client notification for clients without notification callback
-  Enhance fairness in mailbox scheduling
-  Fix EC_T_BUS_SLAVE_INFO::wLineCrossedFlags always zero
-  Fix SoE on PowerPC (broken since V3.0.1.19)
-  Fix AoE InitCmds on PowerPC (broken since V3.0.1.19)

V3.0.1.20
*********

**Core**

-  Add hidden slave connection detection in junction redundancy segment
-  Update MSU management at INACTIVE Master for WKC validation at MasterRed take over
-  Fix emVoeWriteReq (broken since V3.0.1.19)
-  Detect topology correctly in case of junction redundancy line break in a segment containing a another junction slave (OC#418)
-  ecatRescueScan returns EC_E_FRAMELOSS_AFTER_SLAVE again (broken since V3.0.1.19)
-  Add legacy access support to objects 0x8nnn, 0x9nnn, 0xAnnn Enhanced due to ETG.1510 in V3.0.1.18, legacy EC-Engineer was incompatible (broken since V3.0.1.18)
-  Fix last cyclic frame flag (EC_T_CMF_CMD_FLAG_LAST_CYC_FRAME) for MasterRed
-  Fix parsing variables of Specific Data Types
-  Fix GX-JC06-H enhanced identification method in case of EC_IOCTL_SB_SET_IDENTIFICATION_FALLBACK_ENABLED

V3.0.1.19
*********

**Core**

-  Add GX-JC06-H enhanced identification method in case of EC_IOCTL_SB_SET_IDENTIFICATION_FALLBACK_ENABLED
-  Fix corrupted network information after ecatConfigExtend() failed
-  Fix enhance slave mailbox sending and processing
-  Expedited transfers according to object size in MbxGateway
-  Add EC_T_BUS_SLAVE_INFO::wLineCrossedFlags

V3.0.1.18
*********

**Core**

-  Fix activation of Sync Window Monitoring Commands
-  Fix get MAC-address in SockRaw
-  Upload request to non-existing object in Master OD aborted as SDO REQ, not SDO RES
-  Fix Hot Connect Slaves considered present on takeover
-  Support RescueScan with not configured junction redundancy connection
-  Fix timeout in emReadSlaveIdentificationReq
-  Fix defect license check
-  Fix erroneous merged BusTime if the reference clock is on the red line
-  Fix slave disappear on getting ACTIVE
-  Fix wrong notification of unexpected cyclic frame on getting ACTIVE
-  Support ENI with DC enabled but NOP cmd to 0x900 is missing
-  Fix ENI variable type parsing for STRING
-  Fix handling of delayed CoE Frames
-  Add EC_IOCTL_SB_SET_JUNCTION_REDUNDANCY_MODE
-  Fix erroneous EC_E_MAX_BUS_SLAVES_EXCEEDED in case of topology change while scan at the end of the network
-  Enhance Master Object Dictionary regarding ETG.1510

**Platform**

-  Fix LinkOsMemoryBarrier and OsMemoryBarrier for Linux, Xenomai (ARM) (Fixes building Bin/Xenomai_armv6-vfp-eabihf/libemllGem.so)
-  Add emllUdp
-  Fix unexpected master version print under VxWorks
-  Use clock_gettime in OsQueryMsecCount for QNX to support multiprocessor system

V3.0.1.17
*********

**Core**

-  Add EcMbxGatewayClnt to AtemRasClnt
-  Detect topology correctly in case of junction redundancy line break in a segment containing a another junction slave
-  Add InSyncStartDelayCycle to EC_T_DCM_CONFIG_BUSSHIFT, \_MASTERSHIFT, \_MASTERREFCLOCK, \_DCX
-  Add EC_IOCTL_SET_MAILBOX_POLLING_CYCLES to change Mailbox polling cycle
-  Reorder InitCmd for Omron slaves to protect against WKC error during falling transitions to INIT
-  Force topology change at the end of ecatRescueScan
-  Add support for disabled/disconnected slaves in junction redundancy
-  Add EC_IOCTL_SB_SET_IDENTIFICATION_FALLBACK_ENABLED
-  Reduce WKC error period during slave reconnection after it was in OP
-  Always wait for DCM InSync just before PS transition if mode is not DCX
-  Refresh branching information after disconnection at branching slave, fixing erroneous topology information leading to wrong propagation delay in case of junction redundancy line break
-  Add EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR and
-  EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO to RAS
-  Add API emGetBusTime

**Platform**

-  Add OsInit() to DllMain of AtEmRasClnt. To increase performance under Windows because of timeBegin(1)

V3.0.1.16
*********

**Core**

-  Fix wrong DC start time after ecatSetMasterstate(INIT) in case of 64Bit distribution due to Master InitCmd BWR 0x910 in IP transition
-  Add emReloadSlaveEEPRomReq
-  Fix erroneous acyclic frame timeout / retry mechanism (broken since 3.0.1.07)
-  Fix AcycCmdTimeout calculation if EC_T_INIT_MASTER_PARMS.dwEcatCmdTimeout == 0

**Platform**

-  Fix byMaxSubIndex, byObjCode for ecatCoeGetObjectDesc on PPC
-  Use CPU's unaligned access handling for WORD and DWORD (> ARMv6 only) in Linux
-  Implement Marvell 88E1510 specific LED initialization in GEM

V3.0.1.15
*********

**Core**

-  Fix erroneous bus mismatch when new bus slaves have been recorded during DL interrupt handling

V3.0.1.14
*********

**Core**

-  Add DoS protection to HandleLinkPolling
-  Fix update of PDO "Inputs.BusTime"
-  Add exclusive API lock to ecatConfigExtend()
-  Fix erroneously bus mismatch in case ecatConfigExcludeSlave() previously called

V3.0.1.13
*********

**Core**

-  Fix topology information in case of junction red line break behind another junction slave
-  Fix erroneous WkcState == 1 if Slaves of an Msu are missing and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called
-  Fix missing mismatch notification if previous port was not matching by slaves with identification
-  Add EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR
-  Fix crash in Object 0x2006 Mailbox Statistics Object on write access

**Platform**

-  Add x86 for SylixOs

V3.0.1.12
*********

**Core**

-  Filter start-up Eeprom check init-commands (Product-ID, Vendor-ID, Revision, Serialnumber). BusScan already checks Eeprom entries if necessary.

**Platform**

-  Adaption of eT-Kernel for NXP-LS1021a
-  Adaption of ETSEC for eT-Kernel for NXP-LS1021a

V3.0.1.11
*********

**Core**

-  Recalculate WKC at end of rising transitions only in case of success
-  Suppress JunctionRedChange notifications/errors during ecatRescueScan
-  Fix detection of junction redundancy connections which contain junction slaves
-  Fix detection of missing/unexpected junction redundancy connections (emConfigAddJunctionRedundancyConnection)
-  Fix propagation delay calculation in case of junction redundancy line break
-  Unexpected junction redundancy connections are marked as line crossed on the junction red tail slave. (emConfigAddJunctionRedundancyConnection)
-  Fix bus slave leak in case of hot connect group members appear in quick succession

**Platform**

-  GEM Xilinx GMIITORGMII Converter support
-  Added new Link Layer Altera/Intel Triple Speed Ethernet

V3.0.1.10
*********

**Core**

-  Fix McSm order leak in ecatSetSlaveState()
-  Fix erroneous EC_NOTIFY_CYCCMD_WKC_ERROR if Slaves of an Msu are missing and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called.
-  Fix occasional crash in case of interrupt mode due to race condition between ProcessAcycRxFrames and OnMasterTimer
-  Fix undefined behavior of ecatConfigExtend() if error occurs during bus scans
-  Fix handshake between ecatDeinitMaster / ecatConfigureMaster and IST if linklayer in interrupt mode
-  Fix crash for unsupported cascaded junction redundancy
-  Fix ecatGetNumConnectedSlaves() can return 65535 instead of 0
-  Fix parsing of port descriptor (ESC:0x0007) considering "not configured" port as configured. Erroneous line crossed notification by cable redundancy
-  Protect against negative memory usage returned by ecatGetMemoryUsage()

**Platform**

-  Call OsHwTimerGetInputFrequency() before OsHwTimerGetCurrentCount() to allow some run once initialization

V3.0.1.09
*********

**Core**

-  Fix crash during ecatConfigExtend if slaves disappear
-  Fix missing EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL notification after slaves disappear
-  Add EC-STA Eval building
-  ecatRescueScan, ecatConfigExtend without JobTask
-  Fix occasional crash in ecatConfigureMaster in Interrupt Mode (re-configure)
-  Fix occasional crash in OnMasterTimer in Interrupt Mode
-  Add missing documentation to EC-STA
-  Fix recalculation of cyclic Wkc (EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED) for rising state transitions
-  Fix missing EC_NOTIFY_SLAVES_STATECHANGED notification for reappeared slave which is set to origin state by ecatSetSlaveState
-  Set first slave with DC capabilities as bus time reference in DCM modes LinkLayerRefClock and MasterRefClock
-  Updated to atemsys V1.3.11 IO-Control to enable access to ARM cycle count register(CCNT)
-  Refactor EcEniBuilderEmbedded

**Platform**

-  INCLUDE_ASSERT_FUNC for Linux (DEBUG only)
-  Add device ID for I219
-  Fix linklayer instance selection in INTIME

V3.0.1.08
*********

**Core**

-  Fix segmented SDO upload start with toggle bit set to 1 (broken since V3.0.0.19)
-  Fix race condition between API calls and ecatDeinitMaster / ecatConfigureMaster
-  Sysbios RAS support added for ECM on AM572x
-  Fix unexpected EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL notification while waiting for ecatHCAcceptTopoChange

V3.0.1.07
*********

**Core**

-  Fix race condition between API calls and ecatDeinitMaster / ecatConfigureMaster
-  Fix erroneous WkcState == 1 if Slaves of an Msu are missing and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called
-  DCM logging prints only one line to buffer
-  Fix master InitCmd for eCnfType_GenPreopENI, eCnfType_GenOpENI
-  Fix crash in EoE Endpoint after ecatConfigureMaster
-  Return code of initiating error instead of SDO abort code E.g. segmented CoE upload with too small buffer
-  Fix FoE with RAS server V2.4.2.07
-  Fix race condition in acyclic frame handling
-  ecatSetLicenseKey() returns EC_E_LICENSE_MISSING if license is invalid
-  Fix erroneous name of object 0x2006 sub index 3, 4, 7 and 8

**Core**

-  Remove #include <windows.h> in RTOS-32 EcOsPlatform.h

V3.0.1.06
*********

**Core**

-  Fix FoE regression to legacy RAS server (introduced with V2.9.1.12)
-  Use standard DC loop control values for all Hilscher ESC again
-  Fix erroneous max acyclic frames throttling

**Platform**

-  Fix DW3504 Big frames descriptors corruption
-  Fix LinkOsLayer DMA CacheSync with wrong index

V3.0.1.05
*********

**Core**

-  Add DcStartTimeGrid support for LinkLayerRefCloc
-  Fix topology detection if first slave isn´t matching
-  Simple synchronize RescueScan to McSM
-  Enable variable display of absent slave in EC-STA
-  Add auto inc address information to slave in EC-STA
-  Fix Slave OUTPUTs listed as Master INPUTs (GenOpENI)
-  Always enable VoE support for Omron slaves during GenPreopENI
-  Refactor EoE switch to not need a pending receive and send frame pointer anymore
-  Use standard DC loop control values for all Hilscher ESC again

**Platform**

-  Updated to atemsys V1.3.10 Fix compilation on Ubuntu 18.04, Kernel 4.9.90, Xenomai 3.0.6 x64 Cobalt

V3.0.1.04
*********

**Core**

-  Fix set slaves to INIT on reconnection in HotConnect manual mode
-  Fix erroneous WkcState == 1 if Slaves of an Msu are missing and EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED has been called
-  Missing pass of LogParms in EcMotionControl
-  Explicit device ID handling waits until request cleanup done
-  Add EC_T_INIT_MASTER_PARMS::wMaxSlavesProcessedPerBusScanStep to reduce reaction time on topology change by low CPU load if stack is idle
-  Don't refresh AL status of new bus slaves but reset them directly if EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT has been set
-  Don't count slaves during bus scan explicitely if already known because of cyclic or acyclic BRD AL status
-  Always enable VoE support for Omron slaves during GenPreopENI
-  Recalculate DC start time if half of the DC start time safety time has been elapsed
-  Default DC start time safety time calculated based on cycle time
-  Always enable VoE support for Omron slaves during GenPreopENI
-  Fix crash during emConfigExtend if ENI file doesn't contain any slaves
-  Use default value if EC_T_INIT_MASTER_PARMS::dwEcatCmdMaxRetries is zero
-  Don't use lock during notifications generated within the state machines

**Platform**

-  Add new OS and LinkOsLayer, SylixOS and i8254x
-  TI AM3359 ICEv2: board can now boot from sd card using app images.
-  Fix alignment for ARM under WinCE

V3.0.1.03
*********

**Core**

-  Fix repeated EC_NOTIFY_CYCCMD_WKC_ERROR notifications if hot-connect group disappears
-  Eliminate zero bytes malloc during ecatInitMaster()
-  Fix EC_COPYBITS_INLINE with BitOffs + BitSize >= 0x10000 and BitSize > 8
-  Fix erroneous "DC start time" InitCmd during further IP transitions
-  Reduce spinlock usage during topology change
-  Fix ecatGetMasterRedProcessImageInputPtr() Regression since V3.0.0.17
-  Fix ecatResetSlaveController with default EC_T_INITMASTERPARMS (EC-STA, EcMasterTests broken)

**Platform**

-  Support optimized link layers I8254x I8255x in EC-STA
-  Fixed bug in workspaces causing non-working app for TI RTOS on AM5728
-  EC-Master license unlocking for EC-Win with VMF License Query

V3.0.1.02
*********

**Core**

-  Adjust the DCX adjustment delay according the cycle time
-  EC_NOTIFY_ALL_DEVICES_OPERATIONAL is enabled by default to match the ecatNotification.cpp expectation
-  Add support for zero-lengthed cyclic cmds in ENI
-  Fix erroneous bad MSU WkcState on slave disconnection (broken since 3.0.0.19)
-  Fix dwMaxAcycBytesPerCycle change not applied after calling emSetMasterParms
-  Fix unexpected EC_NOTIFY_CYCCMD_WKC_ERROR notification if hot-connect group disappears
-  Fix ecatReleaseAllProcessDataBits returning EC_E_ERROR on success
-  Fix missing port descriptor correction for slaves with invalid descriptors after second bus scan
-  Reduce CPU load in OnMasterTimer during slave disconnection
-  Enhance bus topology detection for hot connect slaves with invalid identification values
-  Adjust EoE retry access period dynamically to increase bandwidth usage
-  Add EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO
-  Add EC_E_SIGNATURE_MISMATCH
-  Add support for zero-lengthed cyclic cmds in ENI

**RAS**

-  Add support for ecatNotifyApp without parms
-  Fix ecatSetSlavesDisconnected
-  Fix ecatGetVersion (broken since V3.0.0.17)
-  Enable ecatAoeWriteControl, re-enable ecatTferSingleRawCmd
-  Fix protocol corruption in case of concurrent send requests at server
-  Fix occassional crash related to unregister client / MbxTfers
-  Abort pending transfer in ecatMbxTferDelete
-  Add logging

**Platform**

-  Removed dependency to VS2005 Redists from EcMasterDotNetNative.dll

V3.0.1.01
*********

**Core**

-  Fix erroneous bad WkcState if transition failed (broken since 3.0.0.17)
-  Use standard DC loop control values for old Hilscher ESC again (build < 20)
-  Fix ecatGetSlaveInpVarInfo, ecatGetSlaveOutpVarInfo ecatGetSlaveInpVarInfoEx, ecatGetSlaveOutpVarInfoEx over RAS
-  Fix CoE Emergency over RAS
-  Fix ecatCoeSdoUploadReq, ecatAoeReadReq, ecatMarshalAoeWriteReq over RAS

**Platform**

-  Allow unlimited DLL-instances per host / user with WIBU protection
-  Fix EcMasterDemoMulti for Linux
-  Set version information to DLLs for Windows
-  Fix crash in EcMasterDotNet with RAS due to uninitialized logging structure
-  atemsys for linux: added possibility to set log verbosity level dynamically when loading by insmod

V3.0.0.19
*********

**Core**

-  Fix missing data at uploads (AoE, CoE, FoE) (regression since V3.0.0.17)
-  Add bExtended to EC_T_CFG_SLAVE_INFO
-  Fix crash in emConfigExtend() in case of max bus slaves exceeded
-  Retry DC start time InitCmd if more than the half of safety time is elapsed during DC activation InitCmd
-  Set WkcState bit if hot-connect group disappears
-  Fix FoE data display (binary / ASCII) in the EC-SlaveTestApp
-  Don’t set PD Input to zero in case of HC group disconnection
-  Fix FoE cancel in case of EoE in BOOTSTRAP (only FoE allowed by ETG.1000.6) "In Bootstrap state the mailbox is active but restricted to the FoE protocol"
-  Fix segmented SDO upload start with toggle bit set to (broken since V3.0.0.17)
-  Fix race condition during notification in case of parallel calls to Job_ProcessRxFramesByTaskId / Job_ProcessAcycRxFrames
-  Protect against systematical acyc command queue overload because of dwMaxSlavesProcessedPerCycle equal to bus slaves count
-  Fix missing ScanBus on reconnection if EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE set to FALSE
-  Fix erroneous line crossed detected in case of line break

**Platform**

-  Fix EC_IOCTL_ISLINK_CONNECTED in ETSEC
-  PRUICSS Link Layer on TI RTOS has migrated to latest TI RTOS SDK 4.02
-  PRUICSS Link Layer now supports Time-Triggered Send (TTS) feature on RT Linux (for am5721/am5728/am3359)
-  PRUICSS Link Layer now supports Time-Triggered Send (TTS) Feature on AM3359 board

V3.0.0.18
*********

**Core**

-  Add ecatSlaveSerializeMbxTfers and ecatSlaveParallelMbxTfers to RAS
-  Fix crash during ecatDeinitMaster()
-  Fix ecatFoeDownloadReq (don’t upload download payload to RAS client)

V3.0.0.17
*********

**Core**

-  Fix ecatNotifyApp() over RAS always returns zero dwNumOutdata (broken since 3.0.0.5)
-  Fix unexpected EC_NOTIFY_SLAVE_UNEXPECTED_STATE notification if ScanBus during ecatSetSlaveDisabled() / ecatSetSlaveDisconnect()
-  Fix erroneous bad WkcState during transition if set state / check state are not the last InitCmds of the transition
-  Fix EC-Master stucks after emHCAcceptTopoChange() has been called
-  Fix emGetslaveProp return EC_FALSE by mismatch at the beginning for first slave
-  Fix missing SlaveId as MbxTferId in VoE notification
-  Fix crash in emRasClntRemoveConnection while transfer is pending
-  Set MSG_NOSIGNAL at socket send to prevent from unexpected SIGPIPE
-  Extrapolate propagation delay of DC slaves without coherent port receive times (e.g. ESC20)
-  Fix leak in client management if connection terminates while a notification is pending
-  Fix erroneous BI transition during AL status refreshing
-  Execute ecatSetSlaveState within McSm
-  Fix overwriting of mailbox objects in asynchronous mailbox RAS-APIs (emCoeSdoUploadReq/emCoeSdoDownloadReq)
-  Fix race condition in RAS client while accessing emMbxTferCreate and emMbxTferDelete
-  RescueScan returns EC_E_TIMEOUT if timeoput elapsed within BusScan
-  Fix GetBusSlaveBySlaveId returns a bus slave even though the slave id is invalid
-  Move slave statistics from CfgSlave to BusSlave, adjust ProcessCmdResult chain
-  Fix MaxSubIndex at object descriptions of 0x10F3, 0x2004
-  Fix mailbox read response stuck if acyclic frame queue is full

V3.0.0.16
*********

**Core**

-  Fix RAS API lock (connection lock instead of global lock)
-  Fix missing mailbox read response command if acyclic frame queue is full
-  Cancel running bus scan if emSetMasterState timeouts
-  Return correct variable type instead of DEFTYPE_NULL for ARRAY types like DEFTYPE_ARRAY_OF_BYTE
-  Always recalculate Wkc if SM/FMMU configuration changed in slave state transition

V3.0.0.15
*********

**Core**

-  Fix bus slave leak during emConfigExtend leading to erroneous EC_E_MAX_BUS_SLAVES_EXCEEDED errors in some cases
-  Fix missing EC_NOTIFY_ETH_LINK_CONNECTED notification if link was disconnected at start
-  Fix NULL pointer access in some case of repeated bus scan by bus mismatch (ResyncSlave is NULL)
-  Fix notify EC_NOTIFY_CYCCMD_WKC_ERROR immediately if cyclic command not related to hot-connect
-  Send all Init-Commands in falling transition even if the slave is not responding
-  Fix emReadSlaveIdentificationReq with EC_E_NOWAIT returns EC_E_INVALIDPARM
-  Add emFoeUploadReq/emFoeDownloadReq to RAS
-  Set LockType from SPIN to DEFAULT, removed external CmdQueue locking
-  Fix master state machine hangs waiting for DCM InSync if DCM BusTime Ref slave disappear
-  Fix erroneous HIDWORD during 64Bit bus time emulation start
-  Fix wrong amount of sent frames sometimes returned by eUsrJob_SendAcycFrames
-  Don't change DCM first (DC start time aligned) time on DcmReset
-  ecatSetMasterState returns EC_E_TIMEOUT_WAITING_FOR_DC and EC_E_TIMEOUT_WAITING_FOR_DCM
-  Set dwScanBusStatus to EC_E_BUSCONFIG_MISMATCH for all unexpected bus slaves
-  Fix erroneous mismatch on slaves reconnection if line disconnected
-  Fix line reconnection with line break in the middle (Broken since 2.9.2.03)
-  Change return type of API LinkOsCreateContext to error codes
-  Updated to atemsys V1.3.08 (Add support for Linux kernel >= 4.13.00)
-  Fix endless scan bus in ecatConfigureMaster(GenPreopENI / eCnfType_GenOpENI) if cable disconnected during the call
-  Fix race condition in ecatConfigureMaster(GenPreopENI / eCnfType_GenOpENI) if a scan bus is running
-  Fix erroneous offset between external and internal SYNC signals in case of SyncToTimerIrq or different DCM SetVal are used in DCX mode
-  Fix process variable to PDO assignment in case of several sync managers share same <Send>/<Recv> entry (Broken since 2.9.2.01)
-  Support EC_NOWAIT at ecatCoeGetODList, ecatCoeGetObjectDesc, ecatCoeGetEntryDesc
-  Flush the queue of the other line containing old frames by cable redundancy
-  Fix Re-register client in EcMasterDemoRasServer

**Platform**

-  PRUICSS Link Layer now supports Time-Triggered Send (TTS) Feature (TI RTOS, am5718/am5728)
-  Fix Renesas NoOs Timer issue

V3.0.0.14
*********

**Core**

-  Add dwTferId to ecatReadSlaveEEPRomReq, ecatWriteSlaveEEPRomReq, ecatAssignSlaveEEPRomReq, ecatActiveSlaveEEPRomReq, EC_T_EEPROM_OPERATION_NTFY_DESC and ecatSetSlavePortStateReq, EC_T_PORT_OPERATION_NTFY_DESC
-  EcWin EVAL license unlocking
-  Fix GenPreopENIWithCRC
-  Fix GetBusSlaveBySlaveId returns a bus slave even though slave id is invalid due to bus mismatch

**Platform**

-  Fix VxWorks70 "cannot map IO memory"

V3.0.0.13
*********

**Core**

-  Fix buffer overflow caused by DCM LinkLayerRefClock logging
-  Add VoE tab to EC-SlaveTestApplication
-  Add TwinSafeLoader support (OBJ8XXX, SI 2 Slave Type String)
-  Fix erroneous reset of SDO complete access bit in case segmented mailbox transfer
-  Fix HC group state change to master state if HC group member is disconnected/disabled by API
-  EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT also clears FMMU configuration
-  Fix unexpected WkcState errors in eUsrJob_ProcessRxFramesByTaskId
-  Add dwTferId to emReadSlaveRegisterReq, emWriteSlaveRegisterReq EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC, emReadSlaveIdentificationReq and EC_T_SLAVE_IDENTIFICATION_NTFY_DESC
-  Fix EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC::bRead wasn´t set after slave register read request finished
-  Fix max response length of MbxGateway server
-  Fix Master State Summary Object 0x2001, SI 13 in case of eDcmMode_Off
-  Fix DCM configuration parameter handling
-  Fix DC start time offset calculation in DCX mode
-  Fix race condition in McSM order management
-  Add EC_T_DCM_CONFIG_BUSSHIFT::bUseDcLoopCtlStdValues

**Platform**

-  Fix out data len at ecatVoeRead in DotNet
-  Fix variables access starting at offset 0x10000 in DotNet

V3.0.0.12
*********

**Core**

-  Fix inactive master doesn't forward frames to slaves in case of line break (since 3.0.0.11)
-  Remove LinkOsPlatformInit()
-  Fix missing initialization of EoE uplink ports
-  Fix unexpected MSU WkcState errors
-  Fix configuration errors for slaves with process data size > 8 kByte
-  Fix line break error in case of junction redundancy line fixed
-  Fix 32Bits internal and external counters by DCX
-  Add junction redundancy flag to EC_T_BUS_SLAVE_INFO::adwPortSlaveIds
-  Fix hot connect mode border close
-  Fix missing notifications in manual topology change mode (EC_IOCTL_SB_SET_TOPOLOGY_CHANGE_AUTO_MODE = EC_FALSE)
-  Fix erroneous line cross notification if number of maximum bus slaves exceeded Remove parameter pvDmaObject from API LinkOsAllocDmaBuffer and LinkOsFreeDmaBuffer
-  Fix time-out handling in emConfigExtend
-  Change parameter pbyPhysical/pbyPhysAddr to qwPhysAddr in APIs LinkOsMapMemory, LinkOsUnmapMemory, LinkOsAllocDmaBuffer, LinkOsFreeDmaBuffer
-  Fix EXCLUDE_LOG_MESSAGES compiler errors
-  Fix crash if identification failed during bus scan
-  Add EcFeatures.h
-  Fix core to not change given EC_T_INITMASTERPARMS
-  Fix VLAN, support Canonical Format Indicator in VLAN ID

**Platform**

-  Add protected version support to SockRaw
-  CPSW: cyclic frames should have higher prio as acyclic
-  Fix VLAN with emllPcap
-  Fix not received frames for some RTL8169 cards
-  Enable MasterRed for x86 / x64, Windows / Linux only

V3.0.0.11
*********

**Core**

-  Add dwMaxAcycBytesPerCycle and rename the acyclic commands related EC_T_INITMASTERPARMS
-  Add API emReadSlaveIdentificationReq
-  Add API emSetSlaveStateReq
-  Add API emActiveSlaveEEPRomReq, emAssignSlaveEEPRomReq, emReadSlaveEEPRomReq, emWriteSlaveEEPRomReq
-  Fix missing EC_NOTIFY_JUNCTION_RED_CHANGE in some disconnect / reconnect situations
-  Queue blocking APIs at RAS Server
-  Fix delayed and skip behavior of added CoE InitCmd
-  Fix too many WkcStateImage offsets in some cases if more than one MasterSyncUnit exists
-  Add DcStartTimeCallback to struct EC_T_DCM_CONFIG_MASTERSHIFT and EC_T_DCM_CONFIG_LINKLAYERREFCLOCK
-  Add emReadSlaveRegisterReq, emWriteSlaveRegisterReq
-  Avoid systematical frame loss on cable redundancy line fixed in some situation
-  Fix RAS Client locking (connection lock instead of global lock)
-  Force Wkc recalculation at startup in case of enabled IO-Control EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED

**
Platform**

-  Added support for new board TI AM3359-ICEV2 to ICSS Link Layer
-  Add API wWkcStateDiagOffsIn and wWkcStateDiagOffsOut to EC_T_MSU_INFO

V3.0.0.10
*********

**Core**

-  Fix erroneous frame loss information at junction redundancy ports during rescue scan
-  Fix Superset-ENI exclude individual slaves
-  Master Object Dictionary 0x2006: Remove wrong size check for subindex 0
-  Add possibility to delay added CoE InitCmd during transitions
-  Fix hot connect slave set erroneously back to INIT after reconnection of another hot connect slave if manual mode is used
-  Fix process variable to PDO assignment in case of unordered PDO entries in ENI
-  Avoid disconnection during huge transfer segmented by the operating system if EC_E_BSD_EINPROGRESS is supported
-  Fix Wkc state diagnosis signalizes error in master states INIT, PREOP and in case of frameloss
-  Fix adjust DcStartTimeOffset if bus cycle time has been changed

**Platforms**

-  EoF not reached workaround for EC-Master-RTOS-32 lib under VS2015
-  Add PRUICSS Link Layer now works under TI RTOS
-  PRUICSS Link Layer can now work in redundancy mode (master/slave PRUs)
-  PRUICSS Link Layer now works under VxWorks

V3.0.0.09
*********

**Core**

-  Add EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT
-  Add EC_IOCTL_SB_SET_ERROR_ON_LINE_BREAK
-  Generate EC_NOTIFY_SB_DUPLICATE_HC_NODE if bus mismatching due to slaves with duplicated identification values
-  Add compiler flag INCLUDE_SLAVE_IDENTIFICATION
-  LogFrameCallBack preserved at configure master
-  Protect against sending empty EoE fragments (deny empty frames) Affects EoE-Endpoints (e.g. VxWorks)
-  emMbxTferAbort() applied to all FoE transfers, not only the segmented ones
-  Fix occasional timeout in ecatRegisterClient

**Master Redundancy**

-  Protect against line crossed false positives (disabled detection)
-  ACTIVE Master needs link connected. Master state Unknown on link disconnect.
-  Don't forward AcycMasterRed frames or own frames
-  Add EC_T_CMF_CMD_TYPE_BRD_ALSTATUS

**Platforms**

-  CPSW Link Layer fix Port 2 on AM57x
-  Fix EcatDrv for Windows x64 (WdfCoInstaller01007 instead of WdfCoInstaller01009)
-  Updated to atemsys V1.3.07
-  PRU-ICSS Link Layer supports now Port 1 & Port 2 on AM571x IDK on VxWorks and Linux.

V3.0.0.08
*********

**Core**

-  Add API ecatGetMasterSyncUnitInfo / ecatGetMasterSyncUnitInfoNumOf
-  Add bDisabled, bDisconnected to EC_T_CFG_SLAVE_INFO
-  Add ecatSetSlavesDisabled / ecatSetSlavesDisconnected to RAS
-  Fix Master OD 0x2020, SI 14, Linklayer driver Ident
-  Fix correlation between WkcState and Pd offset (logical mailbox state command have been erroneously considered)
-  Deny invalid SoE parameters at ecatSoeRead, ecatSoeWrite, (add EC_E_SOE_ERRORCODE_INVL_DRIVE_NO, EC_E_SOE_ERRCODE_NO_ELEM_ADR)
-  Support startup with network on redundancy line (Master2)
-  Fix Bus Load Measurement (Master OD 0x2200:04) for multi task ENIs
-  Fix reconnecting Master
-  Fix EC_IOCTL_SET_SLVSTAT_PERIOD with dwPeriod = 0
-  Fix foreign communication filtering
-  Longer topo change delay at INACTIVE master than at ACTIVE master
-  Deny ecatBlockNode in case of Master Redundancy
-  Auto-append new line to log messages
-  Add API ecatSetSlavesDisabled / ecatSetSlavesDisconnected

V3.0.0.07
*********

**Core**

-  Fix scanbus returns EC_E_BUSCONFIG_MISMATCH if identification failed
-  Fix time-out for first frame in case of closed port
-  Fix emGetMemoryUsage
-  Fix occasional cyclic master red frame re-processing at inactive master
-  Fix occasional master red frame forwarded bit set at active master
-  Add EoE mailbox statistics, don´t count access to master object dictionary.
-  Add pending EoE transfer cancel if slave is disconnected
-  Add 32 bits support to internal and external DCX counters
-  Add mailbox transfers cancel on Master INACTIVE / Slave disappears

**Platforms**

-  Updated to atemsys V1.3.06 for Linux / Xenomai
-  Reduce amount of interrupts by using bAckErrInIrq by RTL8169
-  Fix second PCI device usage for Linux and Xenomai
-  Use correct PCI domain in atemsys for Linux and Xenomai (atemsys V1.3.05)

V3.0.0.06
*********

**Core**

-  Fix stalled connection detection in RAS Client
-  Fix lock up on RAS Client disconnect if socket was disconnected before
-  Fix unidentified slaves after bus mismatch behind a junction slave
-  Fix RED Frame ID at MasterRed Frames from MAIN device
-  Add dynamic frame support for MasterRed with Hot Connect
-  Add port information to junction redundancy change notification EC_T_JUNCTION_RED_CHANGE_DESC
-  Add emConfigAddJunctionRedundancyConnection
-  Adjust DCM nMaxValidVal if DcStartTimeGrid is set
-  Add Memory Provider with read/write, request/release for MasterRed
-  Support revision checks with operator >=
-  Don't call OsQueryMsecCount() in EcTimer::IsElapsed if timer not started to improve performance
-  Fix crash in DCM mode LinkLayerRefClock after reconnection
-  Support SyncToTimerIrq for DcmMastershift and DcmBusShift under RTOS-32
-  Avoid null pointer exception while parsing hot connect configured eni
-  Generate EC_NOTIFY_HC_DETECTADDGROUPS at start-up if hot-connect groups connected
-  Fix erroneous EC_NOTIFY_CYCCMD_WKC_ERROR notification if hot-connect group disappears
-  Fix unexpected RAS client disconnection after configuration download
-  Fix EXCLUDE_VARREAD, EXCLUDE_PORT_OPERATION, EXCLUDE_OEM compiler errors
-  Fix EXCLUDE_GEN_OP_ENI compiler errors. (INCLUDE_CONFIG_EXTEND depends on INCLUDE_GEN_OP_ENI)
-  Enhance invalid ENI detection
-  Fix Wkc recalculation only in case of hot-connect or modified configuration (ecatConfigExcludeSlave)
-  Fix external memory provider support for splitted frame processing
-  Fix invalid performance measurement time prints in the examples in case of reset
-  Add MasterSyncUnit to ecatGetCfgSlaveInfo, ecatGetSlaveInpVarInfoEx
-  Support DCM SetVal 0
-  Fix access violation due to multiple assignment of same Client ID
-  Change FoE MAX_FILE_NAME_SIZE from 32 to 64
-  Fix duplicated master-master-link frames receiving by MasterRed
-  Add NIC part of MAC address comparison on red frame merge

**Platforms**

-  Support for Yocto Linux
-  Change OsMemcpy for Xenomai/ARM (Link Layer handles unaligned memory access)
-  Fix atemsys version check (atemsys V1.3.03)
-  Fix support for Intel Pro/1000 I218LM
-  Add EC-STA packaging
-  Fix multiple connection at RAS-Server (xenomai) Thread names must be unique on Xenomai.

V3.0.0.05
*********

**Core**

-  Change default DCM InSyncLimit to 25us
-  Add OS parms size check in ecatInitMaster
-  Add EC_NOWAIT support at ecatOpenBlockedPorts
-  Generate EC_NOTIFY_SLAVE_UNEXPECTED_STATE if hot connect member reappear in unexpected state
-  Generate EC_NOTIFY_CYCCMD_WKC_ERROR if HC group member is disconnected
-  Fix erroneous SB_MISMATCH notification after junction redundancy line break
-  Add EC_IOCTL_SET_EOE_DEFFERED_SWITCHING_ENABLED
-  Fix notification EC_NOTIFY_SB_DUPLICATE_HC_NODE always disabled
-  Fix change state of new slaves from bootstrap to init to make requesting ID mechanism (AL control) possible.
-  Fix timeout handling of master and slave init commands
-  Support emAoeWriteControl over RAS
-  Add EC_IOCTL_GET_SLVSTAT_PERIOD
-  Fix NewestAckMessage reset in Object 0x10F3 History Object
-  Fix Object 0x2001 Master State Summary, Bit 9: Master in requested State
-  Deny invalid paramater BOOTSTRAP at ecatSetMasterState
-  Fix INPUTs temporary discarded on slave re-connect (AUTO_ADJUST_CYCCMD_WKC)
-  Log DCM differences greater than 10% of the cycle if verbosity level 2 in EcMasterDemoDc / EcMasterDemoMotion
-  Add junction red change notification to RAS
-  Fix junction redundancy line break detection
-  Enable DC window monitoring in case of DCM timeout elapsed during startup
-  Fix exception in DcmGetLog()
-  Fix BusShift part of DCX configuration was not applied
-  Fix crash in ecatConfigureMaster() if dcmConfigure() was called before
-  Fix sometimes bad first difference value for DCX
-  Port stay closed on reconnection if closed by API
-  Support combined use of cable and junction redundancy without enhanced line crossed detection
-  Add defined cable red frame ID to dectect frames which were only sent on one line
-  Add line cross notification to RAS
-  Allow EC_NOWAIT in emTferSingleRawCmd(). Fix emSetSlaveState returns
-  Fix client re-registration in EcMasterDemoRasServer

**Platforms**

-  Support for Yocto Linux
-  Add instance identification by PCI location for Windows
-  Increase buffer count to 64 for DW3504
-  Add uC/OS-III support for ARM
-  Add ETSEC support to QNX for ARM
-  Add atemsys version check for Xenomai3 x86Cobalt (atemsys V1.3.01)
-  Add CPSW and EMAC support to VxWorks 7
-  Fix Xenomai3 x86Cobalt Link Layer rtdm access (atemsys V1.2.16)
-  Fix EC_NOWAIT support at OsWaitForEvent on Linux

V3.0.0.04
*********

**Core**

-  Don't open the red master port automatically if topology change is in manual mode
-  Protect against NULL pointer access to pdwNumOutData during emNotifyApp()
-  Fix EoE-Endpoint (Uplink)
-  Fix EoE-Endpoint (EcMasterDemoDotNetNative)
-  Fix ecatSetMasterState returns DC error code in case of DC initialization error
-  Fix FoE mailbox statistics (PPC)
-  Support port receive time latching without enhanced line crossed detection
-  Add EC_IOCTL_SET_ADJUST_CYCFRAMES_AFTER_SLAVES_STATE_CHANGE

**Platforms**

-  Add CPSW and EMAC support for VxWorks 7

V3.0.0.03
*********

**Core**

-  Add slave to slave mailbox communication
-  Add propagation delay calculation for topologies with junction redundancy
-  Add DCM mode eDcmMode_MasterShiftByApp for better management of EC_IOCTL_DCM_REGISTER_STARTSO_CALLBACK and EC_IOCTL_DCM_REGISTER_TIMESTAMP
-  Protect for unnecessary mailbox repeating during redport handling in DC state machine
-  Fix file name length reading to not exceed given buffer for FoE up- and download
-  Add open fast hot-connect ports immediately without topology change delay
-  Fix Mailbox Statistics FoE counting direction (read/write) fixed, cumulated counting fixed
-  Fix EC_IOCTL_SET_BUS_CYCLE_TIME modifies init master parameter dwBusCycleTimeUsec
-  EC_E_NOTSUPPORTED is returned instead of EC_E_INVALIDCMD if IOCTL is not supported
-  Skip some DC related master InitCmds during state transition of single slave
-  Fix AoE Mailbox APIs return vendor specific AoE device error
-  Fix DC window sync monitoring after RefClock reconnect
-  Fix crash if DC refclock removed by ecatConfigExcludeSlave()
-  Fix External Synchronization Status PDO handling in DCM mode DCX
-  Fix SockRaw default link layer parameter to fix starting with ENI
-  Fix erroneous RAS disconnection at the end of large FoE transfer
-  Add cyclic task id to EC_LINKIOCTL_SENDCYCLICFRAMES
-  Add parameter bDcInitBeforeSlaveStateChange to struct EC_T_DC_CONFIGURE for DC initialization before slave state change to Pre-OP
-  Fix DC start time calculation in DCM mode MasterRefClock
-  Add Cyclic Master Red Frames
-  Refactor splitted frame processing to avoid race conditions in polling mode
-  Add non EtherCAT frame received notification(eRspErr_NON_ECAT_FRAME) to EC_NOTIFY_FRAME_RESPONSE_ERROR
-  IO control EC_IOCTL_SET_CYC_ERROR_NOTIFY_MASK replaced with EC_IOCTL_SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK
-  Fix WKC calculation for splitted sync units
-  Fix unexpected VoE notification to RAS clients
-  EC_E_MAX_BUS_SLAVES_EXCEEDED correctly returned instead EC_E_LINE_CROSSED if more slaves are connected than MasterInitParms.dwMaxBusSlaves
-  Fix connect to RAS Server V2.x
-  Fix DCX with external memory provider write request callback

**Platform**

-  Intel I219 support

V3.0.0.02
*********

**Core**

-  API change for ecatExecJob. Replaced parameter EC_T_VOID\* pvParam withEC_T_USER_JOB_PARMS\* pUserJobParms
-  Add dwTaskId to EC_PF_CYCFRAME_RECV
-  Add ecatClearSlaveStatistics, emGetSlaveStatistics
-  Add ecatPerfMeasSetIrqCtlEnabled
-  Fix Mailbox Statistics Object (0x2006) (SubIndex 65 size wrong, complete access size check wrong)
-  Deny instead of truncate too long FoE file name
-  Performance Measurement including minimum time
-  Add splitted frame processing
-  Always trigger DC state machine if topology change detected
-  Master Object Dict. History Object. Big Endian Support for notifications.
-  Fix access violation in SetMasterState() during ecatconfigureMaster()
-  Fix bus mismatch errors if a slave needs more than one cycle to return the idenfification value (Ado 0x134)
-  Frame leak during Configure Master
-  DC works again together with redundancy even if link layers don't support enhanced line crossed detection
-  Fix connection drop if read data from socket take more time than watchdog
-  Start DC window monitoring only after DCM/DCX is in sync
-  Add ecatConfigExtend
-  SupersetEni supports now HC group modification
-  Fix crash during remote configuration on a master running with GenPreop
-  Fix If DCX enabled, master state change from PREOP to SAFEOP only when DCM Mastershift and DCX in sync
-  Add ecatRescueScan
-  Fix multiple client registration support (EC-Engineer doesn't get all notifications)
-  Fix topology detection if slave with matching fixed adress (duplicate) is connected
-  Fix Mastershift.bCtlOff = EC_TRUE in EC_T_DCM_CONFIG_DCX disabled erroneously DCX controller too
-  Configure DC slave controller registers 0x0934 in DCM mode BusShift to minimize synchronization jitter
-  Fix CopyInfo copy 0 on WKC error
-  Add FoeDownloadReq
-  Add emSetSlaveDisabled
-  Add EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED
-  Add EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
-  Add emSetSlaveDisabled
-  Add EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED
-  Add EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
-  Add DCX time stamp difference alignment to DcStartTimeGrid to compensate DCX initial error
-  Add dwDcStartTimeGrid to struct EC_T_DC_CONFIGURE for DC start time alignment on startup
-  All APIs return EC_E_INVALIDSTATE if master instance was not initialized
-  Rename struct EC_T_DCX_CONFIG to EC_T_DCM_CONFIG_DCX
-  Add CoE Index, SubIndex info at EC_NOTIFY_MBOXRCV for CoE up-/download
-  Add EC_IOCLT_DC_FIRST_DC_SLV_AS_REF_CLOCK
-  Fix no external synchronization error handling in DCX with EL6695
-  Send master InitCmds to new slaves with FPRD instead of BRD
-  Configure all DC slave controller registers 0x0934 and 0x0930 in the same way
-  Implement emGetMemoryUsage
-  Avoid reading mailbox when slave is in INIT
-  Execute DC initialization for bridge slaves even if there is no DC configuration for them in the ENI file
-  Fix erroneous bus time calculation in 64 bit timestamp emulation
-  Update pbyElementFlags at ecatSoeWriteReq, ecatSoeReadReq
-  Fix erroneous log message unknown text ID 0x1022F
-  Reduce time to get InSync in DCM mode MasterRefClock
-  Initialize slave frame description after allocation
-  Master Object Dictionary is using ecatGetText() to create strings for notifications.
-  Fix slave error notifications during emReadSlaveIdentification (Ado 0x134)
-  Don't queue command directly in EC_IOCTL_FORCE_SLVSTAT_COLLECTION only set a request flag to fix lock issue between jobtask and API
-  No OsLock() in JobTask required anymore to queue notifications if RAS client is connected.
-  Fix propagation delay calculation in DCM modes MasterRefClock and LinkLayerRefClock
-  Add Dcx mode - External synchronization
-  Add EC_IOCTL_SET_GENENI_ASSIGN_EEPROM_BACK_TO_ECAT
-  Force process priority class to time critical only for highest priority (Fix RAS client to normal priority process class, e.g. EC-Engineer, EC-STA)
-  Add ecatNotifyApp command line switch to EcMasterDemoRasClient
-  Don't process PotentialRefClock tag as ReferenceClock tag
-  Fix long delay (20s) in SetMasterState if slaves are absent
-  Fix error parsing "read hot connect prev address" identify command (Ado 16)
-  Fix RAS client taking several minutes to detect inactive RAS server <= V2.7 on RAS logon.
-  Fix config slave still have old link to invalid bus slave during remote configuration EC-Engineer
-  Fix erroneous line crossed notification due to acyclic AL status BRD during port receive time latching.
-  Fix crash if ecatSetSlavePortState is called for absent slave Return immediately from ecatSetSlavePortState if called for absent slave
-  Reset SettleTime timer on reference clock disconnection
-  Change verbosity level for "Input Value updated" message
-  Fix error in EC_COPYBITS
-  Fix error 0x98110021 during EC-Engineer remote configuration
-  Fix missing topology change delay in some case of line fixed
-  Avoid OsMalloc in Job_MasterTimer because of ecatConfigureMaster(GenPreopEni)
-  Fix EEPROM Write: Repeat also last word in case of EEPROM was busy
-  Fix SoE Fragmented Write and Read
-  Fix compiler errors with EXCLUDE_LINE_CROSSED_DETECTION
-  Add sanity checks in EcMemPool
-  Fix emGetSlaveInpVarInfoEx() missing index and sub index

**Platform**

-  Fix erroneous filtering of own traffic in WinPcap linklayer for Windows 8 and above
-  VxWorks7: support new VxBus
-  DW3504 add PhyInterface and UseDmaBuffers parameters.
-  EcWin: Add RtosCommStart to the demo
-  Add RTLockHeap() to LinkOsMapMemory() for RTOS-32 to protect for race condition
-  ETSEC Vxworks DIAB supported
-  Master shift for RTOS32 implementation
-  EcWin: remove unused code for EXCLUDE_ECWIN_SHM
-  I8254X: Add PCI_DEVICE_I219V
-  Fslfec: Read mac from eFuse for iMX6 if exists
-  Set JobTask and Logging Task stack size to 0x8000 for RTOS-32 (Fix stack overflow in EcMasterDemoMotion)
-  JSL-Ware implementation
-  Add Npcap support for emllPcap (PCAP_OPENFLAG_NOCAPTURE_LOCAL + NDIS 6)
-  SYSBIOS use IDK 1.1.0.8
-  GEM: add license check
-  Xenomai: use rt_timer_read instead of rt_timer_tsc
-  Add instance identification by PCI location for INtime Fix wrong frame size in snarf linklayer sending corrupted frames

V3.0.0.01
*********

**Core**

-  Support Master Redundancy
-  Fix missed slave connection if connection up during bus scan
-  Fix read/write of word/dword in EcMasterDemoDotNet
-  Only enable log to link layer if bLogToLinkLayer is enabled even in level EC_LOG_LEVEL_VERBOSE
-  Add EC_IOCTL_SET_IGNORE_INPUTS_ON_WKC_ERROR
-  Improve unexpected cyclic frame detection detection in case of too short cycle
-  Remove EcLinkMode_RANDOM
-  Remove CYCFRAME_RX_CB if no cyclic frames sent.
-  Add emSetMasterRedStateReq, emGetMasterRedState, EC_T_MASTER_RED_PARMS
-  Fix access violation in case of some bus mismatch case
-  Added EC_T_OS_PARMS::pfSystemQueryMsecCount
-  Generate DC out of sync notification if DC timeout too short and go further in the master state machine
-  Detected more line crossed topologies
-  Fix very long default timeout for acyclic commands
-  Fix Slave state machine stucking in PREOP if DC unit disabled and slave is DC configured

**Platform**

-  Support 64Bit based PCI address in Linux
-  Fix support for Intel Pro/1000 I218 and add Device ID 0x15A3
-  Fix wrong frame length for I8254X to fix Store and Forward (removed CRC)
-  Renesas SuperH for ARM Linux
-  Change CPSW command line parameters
-  CPSW link layer add am437x support for Linux
-  Fix corrupted frames in ETSEC for PPC
-  Remove forwarding bit check in MAC address in Winpcap for Windows 8 or later