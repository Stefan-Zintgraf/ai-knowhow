V3.1.4.06
*********

-  Add emStartLivePacketCapture to EcMonitorDemo
-  Add support for fragmented CoE SDO Info mailbox transfers
-  Fix read multiple \*.pcap files
-  Fix frame type (cyclic/acyclic) detection if cyclic frame contains NOP commands
-  Fix rebuild topology from bus scan failed in packet capture processing mode
-  Add emNotify - eMbxTferType_COE_GETODLIST
-  Add slave station address to EC_T_COE_ENTRYDESC, EC_T_COE_OBDESC and EC_T_COE_ODLIST
-  Add frame response error type eRspErr_CRC
-  Remove BlockNode handling from CEmNotification
-  Fix slave information prints contain "ERROR: Not found" in examples
-  Fix crash in case of invalid ENI containing a hot connect group head slave with physical address equal to zero
-  Increase log buffer in examples

**Platform**

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

-  Add histogram export to examples
-  Fix no messages in error log if NOPRINTF defined

**Platform**

-  Add emllBcmGenet for Raspberry PI 4 (BCM2711)
-  Fix reset MAC address at DW3504
-  Fix memory leak in OsCreateEvent() on Linux, Xenomai, RTEMS and SylixOs in case of semaphor initialization error

V3.1.4.04
*********

-  Add Hilscher netANALYZER Ethernet TAP support
-  Enhance Live Packet Capture
-  Add emNotify - eMbxTferType_COE_GETENTRYDESC

**Platform**

-  Add support for VxWorks70

V3.1.4.03
*********

-  Add packet capture processing command line option "-play"
-  Add "-oem" command line parameter to examples
-  Fix FoE monitoring in Bootstrap
-  Extend pcap file format support (nanosecond pcap)
-  Add FoE monitoring support
-  Add interrupt support

**Platform**

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

-  Add emGetSlaveInfo
-  Add performance measurement level to -perf command line parameter
-  Add emGetMemoryUsage over RAS
-  Fix topology after reconnect/restart/communication timeout
-  Fix EC_NOTIFY_TAP_LINK_STATUS in interrupt mode
-  Fix CoE response and abort handling
-  Fix blocking API handling over RAS

**Platform**

-  Add MAC protection to emllFslFec for i.MX8 and i.MX8m
-  Fix CPSW transmit channels to work with acontis CPSW Linux driver patch
-  Fix command line contains unexpected application name in RTOS-32 config files

V3.1.4.01
*********

-  Add notifications:

   -  EC_NOTIFY_PDIWATCHDOG
   -  EC_NOTIFY_STATUS_SLAVE_ERROR
   -  EC_NOTIFY_SLAVE_ERROR_STATUS_INFO
   -  EC_NOTIFY_SLAVE_STATECHANGED
   -  EC_NOTIFY_CYCCMD_WKC_ERROR

-  Fix bus load average 0 in case of Monitor and Master run with different cycle times
-  Fix unfilled MbxData after emCoeGetODList
-  Don't call OsMeasCalibrate() if performance measurement is disabled
-  Rename PerfMeas distances to offsets

**Platform**

-  Fix i8254x interrupt mode on ARM/AARCH64
-  Updated to ECAT NDIS Protocol Driver Setup V3.1.3.4. Hide command window during driver installation
-  Updated to atemsys V1.4.20
   
   - Fix support for CMA (Contiguous Memory Allocator) for kernel > 4.9.00

V3.1.3.03
*********

-  Add EC_T_MASTER_INFO::dwMasterStateSummary
-  EC_T_MASTER_INFO::BusDiagnosisInfo data available even if compiled with EXCLUDE_MASTER_OBD
-  Add EC_IOCTL_SET_NOTIFICATION_ENABLED and EC_IOCTL_GET_NOTIFICATION_ENABLED
-  Add MasterSyncUnit support
-  Fix interrupt mode support
-  Add EC_T_PACKETCAPTURE_PARMS::bReadMultipleFiles for emOpenPacketCapture()
-  Cycle time and JOB_Total timer missing in EcSimulator since V3.1.2.10

**Platform**

-  | Updated to atemsys V1.4.18
   | Remove obsolete ARM cycle count register(CCNT)
   | Fix PCI driver do registration for all Ethernet network adapters
   | Add modul parameter AllowedPciDevices to adjust PCI driver
-  Add CPU affinity support to Link Layers supporting interrupt mode

V3.1.3.02
*********

-  Support ENI file with CU2508 only
-  Add support for emCoeGetODList
-  Add EC_T_MONITOR_STATUS::bNextCyclicEntryReceived, rename EC_T_MONITOR_STATUS::bFramesInLinkLayerPending to bNextFramesReceived
-  Add EC_NOTIFY_SB_STATUS, EC_NOTIFY_SB_MISMATCH
-  Fix build topology immediately in packet capture processing mode
-  Add process data input mapping for Inputs.BusTime and Inputs.DevicesState

**Platform**

-  Add RTL8168H support to emllRTL8169
-  Fix DMA buffer alignment in emllRTL8169 (regression since V3.1.3.01)
-  Fix DMA allocation, requesting memory below 4GB for AARCH64/ARM64 on QNX
-  | Updated to ECAT NDIS Protocol Driver V3.1.3.2
   | Move promiscuous mode setting from NDIS Link-Layer to NDIS protocol
     driver
   | Add an entry “DontSetPromiscuousMode” in the Windows registry to
     avoid setting promiscuous mode in ECAT NDIS Protocol Driver
   | Rename Setup to "ECAT NDIS Protocol Driver"
-  Fix EcatDrvGetDrvVersion on Windows (regression since V3.1.3.01)
-  Add RTL8125 support to emllRTL8169
-  | Updated to atemsys V1.4.17.
   | Fix atemsys dma_set_mask_and_coherent() missing in kernels under
     3.12.55
-  NDIS fix start-up with link disconnected

V3.1.3.01
*********

-  Add the InitMonitor parameter dwMbxRecordBufferSize to specify a buffer size for Mailbox recordings
-  Fix crash on Xenomai when recording a Coe Object dictionary

V3.1.2.11
*********

-  Fix unset eMbxTferType in COE SDO upload notfication when using emCoeSdoUploadReq
-  Add EC_NOTIFY_COMMUNICATION_TIMEOUT and EC_NOTIFY_TAP_LINK_STATUS
-  Add EC_T_MONITOR_INIT_PARMS::bApiLockByApp
-  Add WKC State Support

V3.1.2.10
*********

-  Extend EC_T_FRAME_RSPERR_DESC with wCycFrameNum and dwTaskId
-  Fix emGetBusSlaveInfo returns EC_E_NOTFOUND if called with autoinc addressing for some hot-connect configurations

V3.1.2.09
*********

-  Fix CoE Emergency notification
-  Fix high CPU load in eUsrJob_MasterTimer
-  Fix emGetSlaveState in case of slave is not present

V3.1.2.08
*********

-  Enhance Hot-Connect support to detect groups on master start-up
-  Add EC_NOTIFY_MBOXRCV notification for emCoeSdoUploadReq
-  Add API emHCGetSlaveIdsOfGroup and emHCGetNumGroupMembers
-  Store eMbxTferType_COE_SDO_DOWNLOAD and eMbxTferType_COE_SDO_UPLOAD in object dictionary accessible through emCoeSdoUpload

V3.1.2.07
*********

-  Add EC_NOTIFY_MBOXRCV for eMbxTferType_COE_SDO_DOWNLOAD and eMbxTferType_COE_SDO_UPLOAD
-  Enable jumbo frame support for i8254x by default
-  Enhance Hot-Connect support to detect connection and disconnection of Hot-Connect groups
-  Enhance cycle/frame loss detection in states INIT, PREOP and during transitions

V3.1.2.06
*********

-  Fix cycle/frame loss detection for cyclic tasks with more than one frame
-  emGetSlaveState returns the current and requested state accordingly to AL-Control, AL-Status respectively

V3.1.2.05
*********

-  Add PCAP file format support for "Nokia tcpdump" and "Modified tcpdump"
-  Fix Object 0x2001 "Master State Summary", Bit 10: Bus Scan Match and Bit 16: Link Up
-  Add PCAPNG file format support
-  Add position independent ethernet tap support
-  Fix link status after emInitMonitor

V3.1.2.04
*********

-  Fix emGetMonitorParms

V3.1.2.03
*********

-  Add EC_IOCTL_GET_CYCLIC_CONFIG_INFO, EC_IOCTL_IS_SLAVETOSLAVE_COMM_CONFIGURED, EC_IOCTL_CLR_SLVSTATISTICS
-  Fix emGetSlaveInpVarInfoEx, emGetSlaveOutpVarInfoEx
-  Add QNX7 support
-  Add basic hot connect topologies support

V3.1.2.02
*********

-  Add emIsSlavePresent, EC_IOCTL_ISLINK_CONNECTED, EC_IOCTL_GET_LINKLAYER_MODE
-  Fix performance measurement in EcMonitorDemo
-  Fix invisible slave handling
-  Add Xenomai3 support
-  Add emGetMonitorStatus
-  Add emBacktracePacketCapture

V3.1.2.01
*********

-  Change emOpenPacketCapture parameter set
-  Add emStartLivePacketCapture, emStopLivePacketCapture
-  EcMonitorDemo exclude EcDaq dependency
-  Add Object 0x2200 "Bus Load" support
-  Fix Object 0x2002:03 "Bus Diagnosis"

V3.1.1.07
*********

-  Add Object 0x2001 "Master State Summary", Bit 8: Slaves in requested State

V3.1.1.06
*********

-  Initial release of EC-Monitor