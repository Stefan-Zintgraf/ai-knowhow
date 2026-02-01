*****************
General functions
*****************

emonInitMonitor
***************

.. doxygenfunction:: emonInitMonitor

.. doxygenstruct:: EC_T_MONITOR_INIT_PARMS
    :members:

.. doxygenenum:: EC_T_ETHERNET_TAP_TYPE

.. doxygenstruct:: EC_T_OS_PARMS
    :members:

.. doxygenstruct:: EC_T_LOG_PARMS
    :members:

.. datatemplate:xml:: EC_LOG_LEVELS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. doxygentypedef:: EC_PF_LOGMSGHK

.. doxygenstruct:: EC_T_PERF_MEAS_INTERNAL_PARMS
    :members:

.. doxygenstruct:: EC_T_PERF_MEAS_COUNTER_PARMS
    :members:

.. doxygentypedef:: EC_PF_PERF_MEAS_GETCOUNTERTICKS

.. doxygenstruct:: EC_T_PERF_MEAS_HISTOGRAM_PARMS
    :members:

.. doxygenstruct:: EC_T_WORKER_THREAD_PARMS
    :members:

.. doxygenstruct:: EC_T_MBX_PARMS
    :members:

.. doxygenstruct:: EC_T_MBX_PARMS_COE
    :members:

.. doxygenstruct:: EC_T_MBX_PARMS_FOE
    :members:

emonDeinitMonitor
*****************

.. doxygenfunction:: emonDeinitMonitor

emonConfigureNetwork
********************

.. doxygenfunction:: emonConfigureNetwork

.. doxygenenum:: EC_T_CNF_TYPE

emonGetMonitorStatus
********************

.. doxygenfunction:: emonGetMonitorStatus

.. doxygenstruct:: EC_T_MONITOR_STATUS
    :members:
    
**Slave device state’s** 

.. datatemplate:xml:: DEVICE_STATES
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

emonSetLicenseKey
*****************

.. doxygenfunction:: emonSetLicenseKey

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, emonSetLicenseKey)
        :end-before: IGNORE_TEST(DocumentationSnippets, emonSetLicenseKey)
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emonInitMonitor`
    - :cpp:func:`emonConfigureNetwork`

emonRegisterClient
******************

.. doxygenfunction:: emonRegisterClient

.. doxygentypedef:: EC_PF_NOTIFY

.. doxygenstruct:: EC_T_REGISTERRESULTS
    :members:

emonUnregisterClient
********************

.. doxygenfunction:: emonUnregisterClient

emonGetSrcMacAddress
********************

.. doxygenfunction:: emonGetSrcMacAddress

.. doxygenstruct:: ETHERNET_ADDRESS
    :members:

.. seealso:: :cpp:member:`EC_T_MONITOR_INIT_PARMS::pLinkParms`

emonExecJob
***********

.. doxygenfunction:: emonExecJob

*Brief job overview:*

.. doxygenenum:: EC_T_USER_JOB
  :outline:

.. doxygenunion:: EC_T_USER_JOB_PARMS
  :outline:

*Detailed job description:*

#. :cpp:enumerator:`eUsrJob_ProcessAllRxFrames`
    When the Real-time Ethernet Driver operates in polling mode this call will process all currently received frames, when the Real-time Ethernet Driver operates in interrupt mode all received frames are processed immediately and this call just returns with nothing done.

    .. code-block:: cpp

        pUserJobParms->bAllCycFramesProcessed

    This flag is set to a value of :c:macro:`EC_TRUE` it indicates that all previously initiated cyclic frames ( :cpp:enumerator:`eUsrJob_SendAllCycFrames` ) are received and processed within this call. Not used if pUserJobParms set to :c:macro:`EC_NULL`.

    Return: EC_E_NOERROR if successful, error code in case of failures.

#. :cpp:enumerator:`eUsrJob_MonitorTimer`
    To trigger the monitor and slave state machines as well as the mailbox handling this call has to be executed cyclically. The monitor cycle time is determined by the period between calling :cpp:func:`emonExecJob` ( :cpp:enumerator:`eUsrJob_MonitorTimer`). The state-machines are handling the EtherCAT® state change transfers.

    Return: EC_E_NOERROR if successful, error code in case of failures.

emonGetMonitorParms
*******************

.. doxygenfunction:: emonGetMonitorParms

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, emonGetMonitorParms)
        :end-before: IGNORE_TEST(DocumentationSnippets, emonGetMonitorParms)
        :dedent: 4
        :lines: 2-

.. seealso:: :cpp:func:`emonInitMonitor`

emonSetMonitorParms
*******************

.. doxygenfunction:: emonSetMonitorParms

.. seealso:: :cpp:func:`emonInitMonitor`

emonGetVersion
**************

.. doxygenfunction:: emonGetVersion

emonGetText
***********

.. doxygenfunction:: emonGetText

emonGetMemoryUsage
******************

.. doxygenfunction:: emonGetMemoryUsage

emonGetMasterState
******************

.. doxygenfunction:: emonGetMasterState

.. doxygenenum:: EC_T_STATE
    :outline:

emonGetMasterStateEx
********************

.. doxygenfunction:: emonGetMasterStateEx

.. admonition:: Limitation
    :class: admonition hint

    Since it is not possible to determine the actual requested master state, the highest slave state of all slaves is assumed to be the requested master state.

emonFindInpVarByName - "Inputs.DevicesState"
********************************************

The device status of all slaves (OR-linked) is part of the process data with name "Inputs.DevicesState".

.. cpp:alias:: emonFindInpVarByName

emonFindInpVarByName - "Inputs.BusTime"
***************************************

The DC system time (written to ESC register 0x0910) is part of the process data with name "Inputs.BusTime".

.. cpp:alias:: emonFindInpVarByName

emonExportEniBuilderConfig
**************************

.. doxygenfunction:: emonExportEniBuilderConfig

.. seealso::
    :ref:`integration_genebi:Operation without ENI`

emonIoControl
*************

With ``emonIoControl`` a generic control interface exists between the application and the |Product| and its Real-time Ethernet Drivers.

.. doxygenstruct:: EC_T_IOCTLPARMS
    :members:

emonIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB
************************************************

This function call registers an callback function which is called after the cyclic frame is received. Typically this is used when the Real-time Ethernet Driver operates interrupt mode to get an event when the new input data (cyclic frame) is available.
The callback function has to be registered after calling :cpp:func:`emonInitMonitor` before starting the job task.

.. emonIoControl:: EC_IOCTL_REGISTER_CYCFRAME_RX_CB
    :pbyInBuf: Cyclic frame received callback descriptor (EC_T_CYCFRAME_RX_CBDESC)
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_CYCFRAME_RX_CBDESC
    :members:

.. doxygentypedef:: EC_PF_CYCFRAME_RECV

emonIoControl - EC_IOCTL_GET_CYCLIC_CONFIG_INFO
***********************************************

Get cyclic configuration details from ENI configuration file.

.. emonIoControl:: EC_IOCTL_GET_CYCLIC_CONFIG_INFO
    :pbyInBuf: Pointer to dwCycEntryIndex: cyclic entry index for which to get information
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to EC_T_CYC_CONFIG_DESC data type
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_CYC_CONFIG_DESC
    :members:

emonIoControl - EC_IOCTL_IS_SLAVETOSLAVE_COMM_CONFIGURED
********************************************************

Determine if any slave-to-slave communication is configured.

.. emonIoControl:: EC_IOCTL_IS_SLAVETOSLAVE_COMM_CONFIGURED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE slave-to-slave communication is configured, if EC_FALSE it is not.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.