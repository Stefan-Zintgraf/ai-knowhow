V3.1.4.08
*********

-  Add EC-Simulator Linux HiL x86 32 Bit Dongled
-  Add esSendSlaveCoeEmergency()
-  Fix JobTask cycle time in Python examples
-  Fix performance measurement in EcSimulatorHilDemoPython
-  Fix assert on cyclic frame processing for slaves with sync units containing empty PDOs only
-  Fix EC_T_CFG_SLAVE_INFO::wNumProcessVarsInp, EC_T_CFG_SLAVE_INFO::wNumProcessVarsOutp from esGetCfgSlaveInfo() due to erroneously skipped entries by variables not assigned to any slave

**Platform**

-  Add support for VxWorks MSI
-  Fix lock-up in emllProxy EcLinkClose() on Windows

V3.1.4.07
*********

-  Call myAppWorkpd() after cyclic frame processing in EcSimulatorHilDemoMotion in Interrupt Mode
-  Fix performance measurement in EcSimulatorHilDemoMotion

**Platform**

-  Add EcSimulatorHilDemoMotion for INtime6, QNX7, QNX71, VxWorks70
-  Fix VxWorks RTP AtemSys pipe release
-  Fix memory violation leading to undefined behavior like crash or erroneous timeout during DC related InitCmd on VxWorks70 PPC and x86 with emllSnarf, SystemTime() since VxWorks70SR660 and DMA on x86 since VxWorks70vw2203

V3.1.4.06
*********

-  Add error simulation between real slaves
-  Add support for 12 slaves license limit
-  Fix slave information prints contain "ERROR: Not found" in examples
-  Increase log buffer in examples
-  Fix EcSimulatorHilDemoMotion parameter handling
-  Fix CoE emergency if SOE_SUPPORTED in SSC (SOE_EMERGENCY_SUPPORTED=0)
-  Remove BlockNode handling from CEmNotification
-  Fix crash in case of invalid ENI containing a hot connect group head slave with physical address equal to zero

**Platform**

-  Add link status state machine to emllBcmGenet
-  Add support for Linux ARM 32 Bit to emllBcmGenet
-  Force disconnection using PHY loopback for emllI8254x if ResetOnDisconnect not set
-  Add support for emllTiEnetIcssg on AM64xEVM with FreeRTOS
-  Add emllDW3504 for Xenomai
-  Select 'ECAT Protocol Driver' installation on Windows by default if not currently installed
-  Fix PCI link layer support for QNX ARM 32 Bit
-  Add DCM MasterShift for QNX
-  Fix missing ATEMRAS_NOTIFY_CONNECTION EMRAS_EVT_SERVERSTOPPED on connection termination by server
-  Fix TX hang in emllI8254x for I219 after uncontrolled termination
-  Fix lock-up in EC-Wrapper RAS connection on termination by server
-  Set default stack size to 0x8000 for 64 Bit architectures

V3.1.4.05
*********

-  Add frame RX time to DC simulation
-  Add EC_LINKIOCTL_GET_ONTIMER_CYCLETIME, EC_LINKIOCTL_SET_ONTIMER_CYCLETIME, EC_LINKIOCTL_ONTIMER to SiL
-  Fix compiler errors for EXCLUDE_EC_SIMULATOR_HIL, EXCLUDE_EC_SIMULATOR_SIL, EXCLUDE_INTERFACE_LOCK, EXCLUDE_MASTER_OBD and INCLUDE_PERF_MEAS
-  Set EC-Master cycle time as EC-Simulator SiL cycle time by default in emInitMaster()
-  Fix missing loop closed info in DL status for initially disconnected ports
-  Fix no messages in error log if NOPRINTF defined
-  Set cycle time parameter in EcSimulatorHilDemo

**Platform**

-  Add Xenomai3 ARM 64Bit support to RTL8169
-  Add support for Universal WIBU Code
-  Add emllBcmGenet for Raspberry PI 4 (BCM2711)
-  Fix reset MAC address at DW3504
-  Fix memory leak in OsCreateEvent() on Linux, Xenomai, RTEMS and SylixOs in case of semaphor initialization error

V3.1.4.04
*********

-  Add pOsParms to EC_T_LINK_PARMS_SIMULATOR
-  Fix EcSimulatorHilDemo startup error
-  Fix EcSimulatorSilDemo startup error

**Platform**

-  Add support for Xenomai3 ARM 64Bit
-  Add support for VxWorks70

V3.1.4.03
*********

-  Fix access to some object types by implicitly pad entries to even 16bit memory addresses (SSC OBJ_WORD_ALIGN)
-  Add "-oem" command line parameter to examples
-  Add AtesRasClient
-  Add notification logging (e.g. slave state change) to EcSimulatorHilDemo
-  Fix memory leak in SSC on AoE read and SDO info
-  Fix memory leak in esInitSimulator if called with invalid parameters
-  Fix EC_IOCTL_ISLINK_CONNECTED on start

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

-  Add performance measurement level to -perf command line parameter
-  Add emGetMemoryUsage over RAS
-  Add link layer parameters help to Python example application
-  Fix crash on simulator restart in OPERATIONAL
-  Fix crash with DS402 and EXI containing Object Dictionary
-  Fix occasional crash on concurrent call of esPowerSlave and EC-Simulator frame processing
-  Fix occasional crash in emllSimulator IST
-  Fix invalid write to second byte in buffer on esCoeSdoUpload with datalen = 1
-  Fix invalid temp data read at end of CoE object type BYTE Array [0..n]
-  Fix blocking API handling over RAS
-  Fix command line contains unexpected application name in RTOS-32 config files

**Platform**

-  Add Xenomai support
-  Add MAC protection to emllFslFec for i.MX8 and i.MX8m
-  Add "EcatDrv for Optimized Link Layers" to EC-Simulator HiL User Manual
-  Fix CPSW transmit channels to work with acontis CPSW Linux driver patch

V3.1.4.01
*********

-  Add esVoeSend, esSetVoeReceiveCallback
-  Add write support to read-only CoE objects
-  Fix access to CoE SubIndex on odd word address
-  HiL: Fix start with link disconnected and link reconnection
-  Fix mailbox queue entries memory leak (SSC related)
-  SiL: Increase IST stack size from 0x4000 to 0x8000
-  SiL: Fix occasional lock-up in IST
-  Don't call OsMeasCalibrate() if performance measurement is disabled
-  Rename PerfMeas distances to offsets
-  Fix AoE support for PPC

**Platform**

-  Fix i8254x interrupt mode on ARM/AARCH64
-  Fix AoE support for PPC
-  Updated to ECAT NDIS Protocol Driver Setup V3.1.3.4. Hide command window during driver installation
-  Updated to atemsys V1.4.20
   
   - Fix support for CMA (Contiguous Memory Allocator) for kernel > 4.9.00

V3.1.3.03
*********

-  Fix topology info if master assignes other addresses than in ENI/EXI
-  No error on ScanBus request
-  Add EC_T_MASTER_INFO::dwMasterStateSummary
-  EC_T_MASTER_INFO::BusDiagnosisInfo data available even if compiled with EXCLUDE_MASTER_OBD
-  Cycle time and JOB_Total timer missing in EcMonitor since V3.1.2.10

**Platform**

-  Updated to atemsys V1.4.18
   
   - Remove obsolete ARM cycle count register(CCNT)
   - Fix PCI driver do registration for all Ethernet network adapters
   - Add modul parameter AllowedPciDevices to adjust PCI driver

-  Add CPU affinity support to Link Layers supporting interrupt mode

V3.1.3.02
*********

-  Support ENI file with CU2508 only
-  Alias can be used for all configured address command types (FPRD, FPWR, ...)
-  Use station address as alias address in simulated default EEPROM (if EEPROM for the slave not explicitely set in EXI)
-  Return simulated frame to master before post processing

**Platform**

-  Add RTL8168H support to emllRTL8169
-  Fix DMA buffer alignment in emllRTL8169 (regression since V3.1.3.01)
-  Fix DMA allocation, requesting memory below 4GB for AARCH64/ARM64 on QNX
-  Updated to ECAT NDIS Protocol Driver V3.1.3.2

   - Move promiscuous mode setting from NDIS Link-Layer to NDIS protocol driver
   - Add an entry “DontSetPromiscuousMode” in the Windows registry to avoid setting promiscuous mode in ECAT NDIS Protocol Driver
   - Rename Setup to "ECAT NDIS Protocol Driver"
   
-  Fix EcatDrvGetDrvVersion on Windows (regression since V3.1.3.01)
-  Fix DMA memory allocation address handling if base is > 2GB leading to permanent frameloss in VxWorks-32Bit
-  Add RTL8125 support to emllRTL8169
-  Add Link Layer IST CPU affinity mask and priority for .NET and Python
-  Add CYCFRAME_RX_CB for .NET and Python
-  | Updated to atemsys V1.4.17.
   | Fix atemsys dma_set_mask_and_coherent() missing in kernels under
     3.12.55
-  NDIS fix start-up with link disconnected

V3.1.3.01
*********

-  Fix EC-Simulator HiL multi link Interrupt Mode
-  Fix line crossed in mixed mode
-  Implicitely IgnoreCoeDownloadError for EXI
-  Add interrupt mode support for emllSockRaw
-  Updated to EcatDrv V3.1.3.01 Add Print EcatDrv Version to Ecat Driver for Windows
-  Fix parse PCI bus hardware ID string on Windows

V3.1.2.11
*********

-  Fix lock-up in esConfigureNetwork in case of link disconnected and only one slave configured
-  Fix ERROR SDO: Toggle bit not alternated for ENI with segmented CoE InitCmds

V3.1.2.10
*********

-  Fix force process data (MixedMode)

V3.1.2.09
*********

-  Fix occasional lock-up in e.g. esSetSlaveSscApplication due to endless "wait until SyncManager is disabled"
-  Fix auto increment address usage in case on line break
-  Fix Bus Diagnosis Object 0x2002, SubIndex 4: Number of DC Slaves found
-  Remove absent slave's objects from 0x3nnn, 0x9nnn
-  Fix esGetBusSlaveInfo wPrevPort not set
-  Refresh OD on DL Status Change
-  Fix return code of esGetBusSlaveInfo for absent slaves
-  Fix Simulator OD on reconnect slave at other position
-  Improve pcap recorder timestamps using OsPerfMeas
-  Updated to atemsys V1.4.15
-  Fix missing signal handler for SIGINT, SIGTERM on QNX
-  Fix EcatDrv to support AuxClk period < 16ms
-  Add 64Bit DMA support for RTL8169

V3.1.2.08
*********

-  Fix default port 0 connection of slaves with wHCIdentifyAddrPrev (busmismatch)
-  Add SlaveID to BusSlaveInfo
-  Fix EK1200 support
-  Add EC_NOTIFY_HC_TOPOCHGDONE for esPowerSlave, esDisconnectPort, esConnectPorts
-  Increase MAX_MBX_WRITE_ADDRESS

V3.1.2.07
*********

-  Fix identity object (0x1018) in case of Default Object Dictionary for PPC

V3.1.2.06
*********

-  Add eCnfType_Data for SiL
-  Add FSoE
-  Add EoE supported detection support
-  Add EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL, EC_IOCTL_SIMULATOR_GET_MBX_PROCESS_CTL
-  Fix HiL with winpcap
-  Fix WKC for multi sync unit slaves on LRW
-  Fix performance measurement

V3.1.2.05
*********

-  Fix esForceProcessDataBits for mutliple slaves' INPUTs

V3.1.2.04
*********

-  Add Mixed Mode 2: Real slave between simulated slaves
-  Fix Process Data Image Sync for Process Data below Ado 0x1000
-  Fix esSetProcessDataBits for INPUTs, e.g. EcSimulatorHilDemoPython
-  Fix missing EcWrapper for HiL
-  Fix encrypted ENI/EXI accepted if OEM key missing (esSetOemKey)
-  Fix missing interrupt callback registration at link layer for HiL
-  Fix last SimSlave CoE object missing at esCoeGetODList
-  Fix occasional crash in esResetSlaveCoeObjectDictionary

V3.1.1.07
*********

-  Add Object 0x2001 "Master State Summary", Bit 8: Slaves in requested State

V3.1.1.06
*********

-  Discard process data variables not assigned to slaves e.g. variables from "Image-Info" in TwinCAT are out of allocated "Image"
-  Replace MAC address fall back AA:BB:CC:CA:FE:xx with 00:00:00:00:00:xx
-  Fix occasional crash in EXI loading

V3.1.1.05
*********

-  Fix EC-Simulator SiL Dongled delivery

V3.1.1.04
*********

-  Fix NULL pointer crash in EcSimulatorHilDemo::RasNotifyCallback
-  Add SONAME for libEcSimulator.so on Linux
-  Add interrupt mode for EC-Simulator HiL
-  Add Mixed Mode with EC-Simulator at end support (Mixed Mode 1)
-  Add /EtherCATConfig/Config/ExtendedInfo/Entry/Slaves/Slave/Simulated support
-  Fix process image sync with copy offset (TwinCAT ENI)
-  Skip "not used sync managers shall be disabled" check (non-acontis Master)
-  Fix DPRAM from process image sync (forced data)
-  Prevent lock-up in esConfigureNetwork if circulating topology provided

V3.1.1.03
*********

-  EC-Master supports EC-Simulator SiL license
-  Add slave address in CoE object transfer callbacks
-  Fix station address look-up order in esGetSlaveId

V3.1.1.02
*********

-  Add supported Mbx Protocols to esGetCfgSlaveInfo, esGetSlaveInfo
-  CiA402 axis simulation enabled only for ApplicationName "DS402" in EXI (Regression since V3.1.1.01)
-  Add "-simulator ... --connect" option for e.g. Cable Redundancy
-  esLogFrameEnableAtSlavePort, esLogFrameDisableAtSlavePort
-  Add esSetLinkDownAtSlavePort, esSetLinkDownGenerationAtSlavePort, esResetLinkDownGenerationAtSlavePorts
-  Add esSetErrorAtSlavePort, esSetErrorGenerationAtSlavePort, esResetErrorGenerationAtSlavePorts
-  Fix emInitSimulator invalid parameters logging
-  Add EXI parsing "PowerOff", "PortConnection", "IgnoreCoeDownloadError"
-  Add EC_NOTIFY_SLAVE_PRESENCE
-  Fix esIsSlavePresent

V3.1.1.01
*********

-  Fix Object dictionary reset for esSetSlaveSscApplication
-  Add pvContext to esSetSlaveCoeObjectTransferCallbacks
-  Fix FoE, SDO transfers in SSC for PPC
-  Fix esGetSlaveInpVarInfoEx, esGetSlaveOutpVarInfoEx

V3.1.0.20
*********

-  Add EL6695 support (extend slave RAM size to 0xA000)
-  Fix invalid CoE access due to mismatched TYPEDEF_ARRAY\_... bit offset
-  Fix invalid process data access in simulated slave application

V3.1.0.19
*********

-  Add RAS support to EcMasterDemoMotion with EC-Simulator SiL
-  Add EC_IOCTL_REGISTER_CYCFRAME_RX_CB
-  Simulator API calls over RAS esPowerSlave, esDisconnectSlave, esConnectSlaves
-  Fix unknown tag warnings on startup with EXI
-  Fix memory leak in Diagnosis History object of SSC
-  Check Sync Manager settings according to ENI/EXI
-  Fix INPUTs access from application
-  Fix WKC error for Slaves with zero-lengthed FMMUs / Sync Managers
-  Add Multi Sync Manager Channel support to SSC and EC-Simulator
-  Fix EC-Simulator SiL OnTimer Thread on INtime
-  Fix DS402 after esPowerSlave
-  Clear slave inputs on slave power off

V3.1.0.18
*********

-  Fix crash on esPowerSlave with object dictionary from EXI or application
-  Fix link layer based license key handling (HiL)
-  Fix Reference Clock position for auto-connect floating hot connect
-  Ignore empty RECORD / ARRAY data types
-  Ignore SoE writes exceeding object's default buffer size
-  Fix WIBU Product Code for EC-Simulator Dongled
-  Fix partialy uninitialized Object Entry Data (EXI)
-  Fix occasional crash due to 0x3002 "Outputs" SDO structur (generic OD)
-  Fix object length on SDO complete access download according to object description
-  Fix missing awaiting all APIs have finished in esDeinitSimulator
-  Fix illegal unlock in ReleaseInterface if EC-Simulator compiled with EXCLUDE_INTERFACE_LOCK
-  PDI read OUTPUT Sync Manager already in SAFEOP to prevent WKC errors (simulated slaves with Process Data in Mailbox Mode)
-  Ignore 0x1C33, SubIndex 1: Synchronisation type. Needed for simulated slaves with Process Data in Mailbox Mode.
-  Add esSetLicenseKey to EcSimulatorHilDemo
-  Extended 0x1C12 / 0x1C13 to 16 entries (PDO_ASSIGN_CNT)

V3.1.0.17
*********

-  Add INPUTs from Process Data Image for slaves without device emulation
-  Add initially connect / disconnect all hot connect groups
-  Add handler for unknown data type in Object Dictionary
-  Add esResetSlaveCoeObjectDictionary
-  Add esGetNumConnectedSlaves, esGetNumConnectedSlavesMain,
-  Add esIsSlavePresent (linked in topology and powered on)
-  Add slave information to identity object (0x1018) for default Object Dictionary
-  Fix CoE OD memory leak in esSetSlaveSscApplication
-  Fix slave SSC default application flash support
-  Fix ecatPerfMeas
-  Fix crash in esSetSlaveSscApplication for default handlers
-  Fix memory leak in Object Dictionary in case of esSetSlaveSscApplication
-  Fix memory corruption during logical command parsing
-  Change esGetSlaveIdAtPosition: Use auto increment address from ENI/EXI
-  Change licensed slave count (24 / 64 / 128 / 256)
-  Add EC-Simulator-SiL-Linux-x86_32Bit-Dongled
-  Refactor emllSimulator as wrapper for EcSimulator. SiL delivery contains EC-Simulator core library.
-  Rename esRemoveSlaveCoeObject to esDeleteSlaveCoeObject
-  Rename esAddSlaveCoeObjects to esExtendSlaveCoeObjectDictionary

V3.1.0.16
*********

-  Add esSetLicenseKey for HiL (incl. MAC based key) and SiL
-  Refactor emllSimulator as wrapper for EcSimulator (SiL)
-  SiL: bDisableProcessDataImage, bJobsExecutedByApp defaults to FALSE
-  Add EcSimulatorSilDemo
-  Apply forced INPUTs to Process Data Image
-  Add esGetSlaveIdAtPosition using auto increment address from ENI/EXI
-  Add wNumProcessVarsInp, wNumProcessVarsOutp to esGetCfgSlaveInfo
-  Add esClearSlaveCoeObjectDictionary, esRemoveSlaveCoeObject
-  Add esCoeSdoDownload, esCoeSdoUpload
-  Add esCoeGetODList, esCoeGetObjectDesc, esCoeGetEntryDesc for slaves
-  Add esSetSlaveSscApplication
-  Add esAddSlaveCoeObjects
-  Add esSetSlaveCoeObjectTransferCallbacks
-  Apply mailbox settings from ENI/EXI to EEPROM default content
-  Increased SSC mailbox limits
-  Add RAS server to emllSimulator (SiL)
-  Add DL control feature "Temporary use of settings in 0x0100:0x0103[8:15]"
-  Parse Hot Connect identification (Ado134, EEPROM, DPRAM) from ENI/EXI
-  Add object mappable as TxPDO / RxPDO parsing from EXI
-  Add object access restrictions parsing from object dictionary in EXI
-  Updates to EXI parsing for new EXI format, e.g. Slave Application
-  CiA402 axis simulation enabled only for ApplicationName "DS402" in EXI
-  Add OEM EXI support
-  Add initial memset for slave process data
-  Add EC-Simulator OD reading support to EC-SlaveTestApplication
-  Fix EC-Simulator OD reading (regression since V3.1.0.15)
-  Re-init slave on power cycle (esPowerSlave)
-  Deny BOOTSTRAP and mailbox protocols requests not enabled at ENI slave
-  Fix esSetSlaveState to higher state denied
-  Fix crash in esSetSlaveState for Device Emulation (not supported)
-  Fix occasional crash in SSC CoE read
-  Fix occasional crash in SSC Mailbox handler
-  Fix crash if DS402 activated without Target Velocity
-  Ignore complete access to simple object PDO config (legacy ESI support)
-  Return coherent port receive times even if input port is not port A, supporting junction redundancy and line crossed topologies

V3.1.0.15
*********

-  Fix cyclic mailbox state cmd for HiL
-  Fix ECAT Event Mask (0x0200) register refresh
-  Prevent endless loop in ReceiveFrame
-  Set port mode auto (revert auto-close) on slave power on
-  Fix AoE for Linux x64
-  Fix EC-Simulator HiL with SockRaw
-  Add NDIS link layer
-  Fix VendorId, ProductCode, RevisionNumber, and SerialNumber internally get from EEPROM as WORD instead of DWORD, leading to missing tabs in EC-Engineer

V3.1.0.14
*********

-  Add esSetSlaveState
-  Add esReadSlaveIdentification
-  Add esGetSlaveStatistics / esClearSlaveStatistics
-  Fix esGetBusSlaveInfo returning erroneous children slaves information
-  Add CiA402 simulation
-  Add esSetOemKey for AtesRasSrv
-  Add EC-Engineer MDP scan support using online EXI
-  Add CoE Object Dictionary from EXI
-  Extend default RxPDOs, TxPDOs 0x1600...0x1603, 0x1A00...0x1A03, SI 1...8 (writeable)
-  Ignore CoE download error in case of default Object Dictionary
-  Add INPUT setting by EC-Engineer support
-  Fix EC-Simulator device information in Object Dictionary
-  Add abyMac, dwRxBufferCnt, dwBusCycleTimeUsec, bJobsExecutedByApp, qwOemKey to EC_T_LINK_PARMS_SIMULATOR
-  Add missing SDK\\INC\\EcSimulator.h to EC-Simulator SiL
-  Fix EC-Simulator SiL Process Data Image support
-  Fix esGetNumConfiguredSlaves

V3.1.0.13
*********

-  Add esConnectPorts, esDisconnectPort, esPowerSlave to EcSimulator.def
-  Update SSC from V5.11 to V5.12
-  Add EC-Simulator-HiL-QNX6
-  Fix CPU Affinity for emllSimulator

V3.1.0.12
*********

-  Refresh AL Status and Control in object dictionary
-  Add esGetSlaveId, esGetSlaveFixedAddr, esGetSlaveProp, esGetSlaveState, esGetSlaveInfo
-  Add EC-Simulator-HiL-QNX7
-  Add frame logging
-  Add Network Operation Functions (esConnectPorts, esDisconnectPort, esPowerSlave)
-  Fix occasional crash in ProcessFrame
-  Add EEPROM write by EtherCAT support

V3.1.0.11
*********

-  Add EC_NOTIFY_SLAVE_STATECHANGED
-  Add RegisterClient / UnregisterClient
-  Add EK1200 support
-  Device Emulation for non-mailbox slaves if Extended Info not available for slave
-  Increase MAX_PD_WRITE_ADDRESS, MAX_PD_READ_ADDRESS to end of DPRAM (0x3FFF)
-  Device Emulation for non-mailbox slaves if Extended Info not available for slave
-  Support Port Receive Times
-  Add EcSimulatorHilDemo

**Platform**

-  Add Linux
-  Add Windows