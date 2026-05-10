Header files
************

Function prototypes, definitions etc. of the API can be found in the header file :file:`EcSimulator.h` which is the main header file to include when using |Product|.

Generic API return status values
********************************

Most of the functions and also some notifications will return an error status value to indicate whether a function was successfully executed or not.
Some of the return status values have a generic meaning unspecific to the called API function.

- EC_E_NOERROR: The function was successfully executed.
- EC_E_NOTSUPPORTED: Unsupported feature or functionality.
- EC_E_BUSY: The stack currently is busy and the function has to be re-tried at a later time.
- EC_E_NOMEMORY: Not enough memory or frame buffer resources available.
- EC_E_INVALIDPARM: Invalid or inconsistent parameters.
- EC_E_TIMEOUT: Timeout error.
- EC_E_SLAVE_ERROR: A slave error was detected.
- EC_E_INVALID_SLAVE_STATE: The slave is not in the requested state to execute the operation (e.g. when initiating a mailbox transfer the slave must be at least in PREOP state).
- EC_E_SLAVE_NOT_ADDRESSABLE: The slave does not respond to its station address (e.g. when requesting its AL_STATUS value). The slave may be removed from the bus or powered-off.
- EC_E_LINK_DISCONNECTED: Link cable not connected.
- EC_E_MASTERCORE_INACCESSIBLE: Master core inaccessible. This result code usually means a remote connected server / EC-Simulator stack does not respond anymore

Multiple EtherCAT Network Support
*********************************

Overview
========

The acontis EC-Simulator stack supports multiple EtherCAT network instances within the same application process. 
The first parameter of all esXxx API functions is the Instance ID, starting with 0.
The maximum Instance ID of the EC-Simulator SDK is defined as MAX_NUMOF_SIMULATOR_INTERFACES - 1.
Implementing multiple EtherCAT network instances is realized by using multiple Instance IDs.

.. figure:: ../Media/overview.png
    :alt:
    
The Real-time Ethernet Driver can be of same or different type (emllPcap, emllIntelGbe, ...).

Licensing
=========

For each network identified with the unique Instance ID a separate runtime license is required.

General functions
*****************

esInitSimulator
===============

.. doxygenfunction:: esInitSimulator

.. doxygenstruct:: EC_T_SIMULATOR_INIT_PARMS
    :members:

.. doxygenstruct:: EC_T_OS_PARMS
    :members:
    
.. doxygenstruct:: EC_T_LOG_PARMS
    :members:
    
EC_LOG_LEVEL... 
The following log levels are defined:

.. datatemplate:xml:: EC_LOG_LEVELS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. doxygentypedef:: EC_PF_LOGMSGHK

Log messages are passed from the |Product| to the callback given at :cpp:member:`EC_T_LOG_PARMS::pfLogMsg`. :file:`EcLogging.cpp` demonstrates how messages can be handled by the application.
For performance reasons the |Product| automatically filters log messages according to :cpp:member:`EC_T_LOG_PARMS::dwLogLevel`. E.g. messages of severity :c:macro:`EC_LOG_LEVEL_WARNING` are not passed to the application if :cpp:member:`EC_T_LOG_PARMS::dwLogLevel` is set to :c:macro:`EC_LOG_LEVEL_ERROR`.

The application can provide customized log message handlers of type :cpp:type:`EC_PF_LOGMSGHK` if the default handler in :file:`EcLogging.cpp` does not fulfill the application's needs. Note: The callback is typically called from the Job Task's context and should return as fast as possible.

.. doxygenstruct:: EC_T_PERF_MEAS_INTERNAL_PARMS
    :members:

.. doxygenstruct:: EC_T_PERF_MEAS_COUNTER_PARMS
    :members:

.. doxygentypedef:: EC_PF_PERF_MEAS_GETCOUNTERTICKS 

.. doxygenstruct:: EC_T_PERF_MEAS_HISTOGRAM_PARMS
    :members:

esDeinitSimulator
=================

.. doxygenfunction:: esDeinitSimulator

esGetSimulatorParms
===================

.. doxygenfunction:: esGetSimulatorParms

.. seealso:: :cpp:func:`esInitSimulator`

esSetSimulatorParms
===================

.. doxygenfunction:: esSetSimulatorParms

.. seealso:: :cpp:func:`esInitSimulator`

esSetLogParms
=============

.. doxygenfunction:: esSetLogParms

.. seealso:: :cpp:func:`esInitSimulator`
.. seealso:: :cpp:func:`esSetSimulatorParms`

esGetSrcMacAddress
==================

.. doxygenfunction:: esGetSrcMacAddress

Refers to adapter from EC_T_SIMULATOR_INIT_PARMS.pLinkParms at :cpp:func:`esInitSimulator`.

esSetLicenseKey (HiL)
=====================

.. doxygenfunction:: esSetLicenseKey

Must be called after :cpp:func:`esInitSimulator` and before :cpp:func:`esConfigureNetwork`.This function may not be called if a non protected version is used.

Example:

.. code-block:: cpp

    dwRes = esSetLicenseKey(dwInstanceID, "DA1099F2-15C249E9-54327FBC");
    
esSetOemKey (HiL)
=================

.. doxygenfunction:: esSetOemKey

Must be called after :cpp:func:`esInitSimulator` and before :cpp:func:`esConfigureNetwork`.

Example:

.. code-block:: cpp

    dwRes = esSetOemKey(dwInstanceID, 0x1234567812345678);

esConfigureNetwork
==================

.. doxygenfunction:: esConfigureNetwork

.. doxygenenum:: EC_T_CNF_TYPE

esGetCfgSlaveInfo
=================

.. doxygenfunction:: esGetCfgSlaveInfo

Content of :cpp:struct:`EC_T_CFG_SLAVE_INFO` is subject to be extended.

.. doxygenstruct:: EC_T_CFG_SLAVE_INFO
    :members:

**Supported mailbox protocols flags**

.. datatemplate:xml:: EC_MBX_PROTOCOLS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. dropdown:: **esGetCfgSlaveInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_general.h
        :start-after: DocumentationSnippetsGetCfgSlaveInfoExample
        :end-before: DocumentationSnippetsGetCfgSlaveInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

esGetCfgSlaveSmInfo
===================

.. doxygenfunction:: esGetCfgSlaveSmInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_ENTRY
    :members:

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_INFO
    :members:

.. dropdown:: **esGetCfgSlaveSmInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_general.h
        :start-after: DocumentationSnippetsGetCfgSlaveSmInfoExample
        :end-before: DocumentationSnippetsGetCfgSlaveSmInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

esSetSlaveSscApplication
========================

.. doxygenfunction:: esSetSlaveSscApplication

.. doxygenstruct:: EC_T_SLAVE_SSC_APPL_DESC
    :members:

.. seealso:: 

    - :ref:`api_mailbox:ADS over EtherCAT (AoE)`
    - :ref:`api_mailbox:Ethernet over EtherCAT (EoE)`
    - :ref:`api_mailbox:File access over EtherCAT (FoE)`
    - :cpp:func:`esInitSimulator`
    - :cpp:func:`esConfigureNetwork`

esRegisterClient
================

.. doxygenfunction:: esRegisterClient

.. doxygentypedef:: EC_PF_NOTIFY
    
.. doxygenstruct:: EC_T_REGISTERRESULTS
    :members:

esUnregisterClient
==================

.. doxygenfunction:: esUnregisterClient

esExecJob
=========

.. doxygenfunction:: esExecJob

*Brief job overview:*

.. doxygenenum:: EC_T_USER_JOB
  :outline:

.. doxygenunion:: EC_T_USER_JOB_PARMS
  :outline:
    
*Detailed job description:*

#. :cpp:enumerator:`eUsrJob_ProcessAllRxFrames`
    If the Real-time Ethernet Driver operates in polling mode this call will process all currently received frames, in interrupt mode all received frames are processed immediately and this call just returns with nothing done.

    .. code-block:: cpp

        pUserJobParms->bAllCycFramesProcessed
    
    This flag is set to a value of :c:macro:`EC_TRUE` it indicates that all previously initiated cyclic frames ( :cpp:enumerator:`eUsrJob_SendAllCycFrames` ) are received and processed within this call. Not used if pUserJobParms set to :c:macro:`EC_NULL`.
    
    Return: EC_E_NOERROR if successful, error code in case of failures.
    
#. :cpp:enumerator:`eUsrJob_SimulatorTimer`
    This has to be called cyclically to trigger the slave state machines, copy process data from simulated slave firmware as well as the mailbox handling. The slave state machines handle the EtherCAT state transitions.
    
    Return: EC_E_NOERROR if successful, error code in case of failures.

esGetMasterState
================

.. doxygenfunction:: esGetMasterState

esIoControl
===========

.. doxygenfunction:: esIoControl

.. doxygenstruct:: EC_T_IOCTLPARMS
    :members:
    
esIoControl - EC_IOCTL_GET_PDMEMORYSIZE
=======================================

Queries the necessary size the process data image has got. This IOCTL is to be called after esConfigureNetwork.

.. esIoControl:: EC_IOCTL_GET_PDMEMORYSIZE
    :pbyOutBuf: Pointer to memory where the memory size information will be stored (EC_T_MEMREQ_DESC)
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.

.. doxygenstruct:: EC_T_MEMREQ_DESC
    :members:

esIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB
==============================================

This function call registers a callback function which is called after the cyclic frame is received. Typically this is used when the Real-time Ethernet Driver operates interrupt mode to get an event when the new input data (cyclic frame) is available.
The callback function has to be registered after calling :cpp:func:`esConfigureNetwork` before starting the job task.

.. esIoControl:: EC_IOCTL_REGISTER_CYCFRAME_RX_CB
    :pbyInBuf: Cyclic frame received callback descriptor (EC_T_CYCFRAME_RX_CBDESC)
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_CYCFRAME_RX_CBDESC
    :members:
    
.. doxygentypedef:: EC_PF_CYCFRAME_RECV

esIoControl - EC_IOCTL_ISLINK_CONNECTED
=======================================

Determine whether link between the EC-Simulator stack and the first slave is connected.

.. esIoControl:: EC_IOCTL_ISLINK_CONNECTED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE link is connected, if EC_FALSE it is not.
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.

.. important:: With cable redundancy support enabled, EC_FALSE is only set if all links are down.

esIoControl - EC_IOCTL_GET_CYCLIC_CONFIG_INFO
=============================================

Get cyclic configuration details from ENI configuration file.

.. esIoControl:: EC_IOCTL_GET_CYCLIC_CONFIG_INFO
    :pbyInBuf: Pointer to dwCycEntryIndex: cyclic entry index for which to get information
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to EC_T_CYC_CONFIG_DESC data type
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.
    
.. doxygenstruct:: EC_T_CYC_CONFIG_DESC
    :members:

esIoControl - EC_IOCTL_ADDITIONAL_VARIABLES_FOR_SPECIFIC_DATA_TYPES
===================================================================

Enable or disable additional variables for specific data types. Default: Enabled.

.. esIoControl:: EC_IOCTL_ADDITIONAL_VARIABLES_FOR_SPECIFIC_DATA_TYPES
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: enable, EC_FALSE: disable.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

esIoControl - EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL
====================================================

Enable or disable mailbox processing at slave. Default: Enabled.

.. esIoControl:: EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL
    :pbyInBuf: Pointer to value of :cpp:struct:`EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC`
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes

.. doxygenstruct:: EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC
    :members:

esIoControl - EC_IOCTL_SIMULATOR_GET_MBX_PROCESS_CTL
====================================================

Enable or disable mailbox processing at slave. Default: Enabled.

.. esIoControl:: EC_IOCTL_SIMULATOR_GET_MBX_PROCESS_CTL
    :pbyInBuf: Pointer to value of EC_T_WORD. Configured station address of slave
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes
    :pbyOutBuf: Pointer to value of :cpp:struct:`EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC`
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. seealso:: :ref:`api_general:esIoControl - EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL`

esIoControl - EC_IOCTL_GET_LINKLAYER_MODE
=========================================

This call allows the application to determine whether the Real-time Ethernet Driver is currently running in polling or in interrupt mode.

.. emIoControl:: EC_IOCTL_GET_LINKLAYER_MODE
    :pbyOutBuf: Pointer to struct EC_T_LINKLAYER_MODE_DESC
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_LINKLAYER_MODE_DESC
    :members:

esIoControl - EC_LINKIOCTL_XXXX
===============================

With EC_LINKIOCTL_XXXX a generic control interface exists between the application and the |Product| and its Real-time Ethernet Driver. 

The generic control interface :cpp:func:`esIoControl` provides access to the main network adapter when adding EC_IOCTL_LINKLAYER_MAIN to the EC_LINKIOCTL_XXXX parameter at dwCode. EC_IOCTL_LINKLAYER_RED specifies the redundant network adapter.

**Parameters**
pbyInBuf, dwInBufSize, pbyOutBuf, dwOutBufSize, pdwNumOutData are specific to EC_LINKIOCTL_XXXX, e.g. EC_LINKIOCTL_GET_ETHERNET_ADDRESS.

esIoControl - EC_LINKIOCTL_GET_ETHERNET_ADDRESS
===============================================

Get MAC address of network adapter

.. esIoControl:: EC_LINKIOCTL_GET_ETHERNET_ADDRESS
    :pbyOutBuf: Pointer to MAC address buffer (6 bytes)
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes
    :pdwNumOutData: Pointer to EC_T_DWORD: amount of bytes written to the output buffer

esIoControl - EC_LINKIOCTL_GET_SPEED
====================================

Get current network adapter's speed in MBits.

.. esIoControl:: EC_LINKIOCTL_GET_SPEED
    :pbyOutBuf: Pointer to EC_T_DWORD. Set by Real-time Ethernet Driver to 10/100/1000.
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes
    :pdwNumOutData: Pointer to EC_T_DWORD: amount of bytes written to the output buffer

esIoControl - EC_LINKIOCTL_GET_PCI_INFO
=======================================

Get current network adapter's PCI information

.. esIoControl:: EC_LINKIOCTL_GET_PCI_INFO
    :pbyOutBuf: Pointer to EC_T_PCI_INFO buffer
    :dwOutBufSize: Size of the output buffer in bytes. Must be at least the size of EC_T_PCI_INFO
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer

.. doxygenstruct:: EC_T_PCI_INFO
    :members:
.. doxygenstruct:: EC_T_PCI_INFO_LOCATION
    :members:
.. doxygenstruct:: EC_T_PCI_INFO_IDENIFICATION
    :members:
.. doxygenstruct:: EC_T_PCI_INFO_IOBAR
    :members:
.. doxygenstruct:: EC_T_PCI_INFO_MEMBAR
    :members:
.. doxygenstruct:: EC_T_PCI_INFO_INTERRUPT
    :members:

esIoControl - EC_LINKIOCTL_FORCE_LINK_STATUS
============================================

Forces the current network adapter's link status

.. esIoControl:: EC_LINKIOCTL_FORCE_LINK_STATUS
    :pbyInBuf: Pointer to EC_T_BYTE. See EC_LINK_FORCE_LINK_STATUS_...
    :dwInBufSize: Size of the input buffer in bytes. Must be at least the size of EC_T_BYTE
    
.. doxygendefine:: EC_LINK_FORCE_LINK_STATUS_DISCONNECTED
.. doxygendefine:: EC_LINK_FORCE_LINK_STATUS_OK
.. doxygendefine:: EC_LINK_FORCE_LINK_STATUS_AUTO

esGetVersion
============

.. doxygenfunction:: esGetVersion

esGetText
=========

.. doxygenfunction:: esGetText

esGetMemoryUsage
================

.. doxygenfunction:: esGetMemoryUsage

esLogFrameEnable
================

.. doxygenfunction:: esLogFrameEnable

.. code-block:: cpp
    
    /********************************************************************************/
    /** \brief  Handler to log frames.
    *
    *   CAUTION: Called by cyclic task! Do not consume too much CPU time!
    */
    EC_T_VOID LogFrameHandler(EC_T_VOID* pvContext, EC_T_DWORD dwLogFlags, EC_T_DWORD dwFrameSize, EC_T_BYTE* pbyFrame)
    {
        EC_T_STATE         eMasterState;
    
        /* get master state */
        eMasterState = (EC_T_STATE)(dwLogFlags & EC_LOG_FRAME_FLAG_MASTERSTATE_MASK);
    
        /* skip tx frame */
        if ((S_dwLogFrameLevel == 3) && !(dwLogFlags & EC_LOG_FRAME_FLAG_RX_FRAME))
            return;
    
        /* skip cyclic frame */
        if ((S_dwLogFrameLevel == 2) && !(dwLogFlags & EC_LOG_FRAME_FLAG_ACYC_FRAME))
            return;
    
        /* skip red frame */
        if (dwLogFlags & EC_LOG_FRAME_FLAG_RED_FRAME)
    return;
    
        /* do something with pbyFrame ... */
    }

esLogFrameDisable
=================

.. doxygenfunction:: esLogFrameDisable
