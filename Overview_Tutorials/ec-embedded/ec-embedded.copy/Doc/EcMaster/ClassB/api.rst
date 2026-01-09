********************************
Generic API return status values
********************************

Most of the functions and also some notifications will return an error status value to indicate whether a function was successfully executed or not. Some of the return status values have a generic meaning unspecific to the called API function.

:c:macro:`EC_E_NOERROR`
    The function was successfully executed

:c:macro:`EC_E_NOTSUPPORTED`
    Unsupported feature or functionality

:c:macro:`EC_E_BUSY`
    The master currently is busy and the function has to be re-tried at a later time

:c:macro:`EC_E_NOMEMORY`
    Not enough memory or frame buffer resources available

:c:macro:`EC_E_INVALIDPARM`
    Invalid or inconsistent parameters

:c:macro:`EC_E_TIMEOUT`
    Timeout error

:c:macro:`EC_E_SLAVE_ERROR`
    A slave error was detected

    .. seealso::
        - :ref:`api:emNotify - EC_NOTIFY_STATUS_SLAVE_ERROR`
        - :ref:`api:emNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO`

:c:macro:`EC_E_INVALID_SLAVE_STATE`
   The slave is not in the requested state to execute the operation (e.g. when initiating a mailbox transfer, the slave must be at least in PREOP state)

:c:macro:`EC_E_SLAVE_NOT_ADDRESSABLE`
   The slave does not respond to its station address (e.g. when requesting its AL_STATUS value). The slave may be removed from the bus or powered-off.

:c:macro:`EC_E_LINK_DISCONNECTED`
   Link cable not connected.

:c:macro:`EC_E_MASTERCORE_INACCESSIBLE`
   Master core inaccessible. This result code usually means a remotely connected server / EtherCAT Master does not respond anymore.


The :c:macro:`EC_E_BUSY` return status value indicates that a previously requested operation is still in progress. For example if the master is requested to enter the OPERATIONAL state the next request from the API will return this status value unless the OPERATIONAL state is entered.

*****************************
Multiple EtherCAT Bus Support
*****************************

Licensing
*********

Multiple EtherCAT Bus support is included within the Class B and Class A master stack. For each bus a separate runtime license is required. A single runtime allows the usage of the multi instance functions only with an instance identifier of 0.

Overview
********

The acontis EtherCAT master allows controlling more than one EtherCAT bus within one application process. For this use case the master core is instantiated several times by using the multi instance API functions inside the application.
Each API function is available as a single instance version (prefix ecat, e.g. :cpp:func:`ecatInitMaster`) and a multi instance version (prefix em, e.g. :cpp:func:`emInitMaster`).
The first parameter of all multi instance functions :cpp:func:`emXxx` is the instance identifier.
The single instance functions :cpp:func:`ecatXxx` will use the first master core instance with the identifier 0.
The maximum number of supported instances is 12 (MAX_NUMOF_MASTER_INSTANCES).

.. figure:: ../Media/API.png
    :align:     center
    :alt:

Example application
*******************

The application EcMasterDemoMulti demonstrates a client application which handles two master instances with the following configuration (el9800.xml):

- Master instance 0: One Beckhoff EtherCAT Evaluation Board EL9800
- Master instance 1: One Beckhoff EtherCAT Evaluation Board EL9800

Parameters for this application:

.. prompt:: bash

    -ndis 192.168.1.32 1 -f el9800.xml @ -ndis 192.168.2.32 1 -f el9800.xml

*****************
General functions
*****************

emInitMaster
************

.. doxygenfunction:: ecatInitMaster
    :outline:

.. doxygenfunction:: emInitMaster

.. doxygenstruct:: EC_T_INIT_MASTER_PARMS
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

Log messages are passed from the EC-Master to the callback given at :cpp:member:`EC_T_LOG_PARMS::pfLogMsg`. EcLogging.cpp demonstrates how messages can be handled by the application.
For performance reasons the EC-Master automatically filters log messages according to :cpp:member:`EC_T_LOG_PARMS::dwLogLevel`. E.g. messages of severity :c:macro:`EC_LOG_LEVEL_WARNING` are not passed to the application if :cpp:member:`EC_T_LOG_PARMS::dwLogLevel` is set to :c:macro:`EC_LOG_LEVEL_ERROR`.

The application can provide customized log message handlers of type :cpp:type:`EC_PF_LOGMSGHK` if the default handler in EcLogging.cpp does not fulfill the application's needs. Note: The callback is typically called from the Job Task's context and should return as fast as possible.

.. doxygenstruct:: EC_T_PERF_MEAS_INTERNAL_PARMS
    :members:

.. doxygenstruct:: EC_T_PERF_MEAS_COUNTER_PARMS
    :members:

.. doxygentypedef:: EC_PF_PERF_MEAS_GETCOUNTERTICKS

.. doxygenstruct:: EC_T_PERF_MEAS_HISTOGRAM_PARMS
    :members:

emDeinitMaster
**************

.. doxygenfunction:: ecatDeinitMaster
    :outline:

.. doxygenfunction:: emDeinitMaster

emGetMasterParms
****************

.. doxygenfunction:: ecatGetMasterParms
    :outline:

.. doxygenfunction:: emGetMasterParms

.. dropdown:: **emGetMasterParms() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterParmsExample
        :end-before: DocumentationSnippetsGetMasterParmsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emInitMaster`

emSetMasterParms
****************

.. doxygenfunction:: ecatSetMasterParms
    :outline:

.. doxygenfunction:: emSetMasterParms

.. dropdown:: **emSetMasterParms() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetMasterParmsExample
        :end-before: DocumentationSnippetsSetMasterParmsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emInitMaster`

emScanBus
*********

.. doxygenfunction:: ecatScanBus
    :outline:

.. doxygenfunction:: emScanBus

.. dropdown:: **emScanBus() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsScanBusExample
        :end-before: DocumentationSnippetsScanBusExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :ref:`api_busscan:EtherCAT Bus Scan`

emRescueScan
************

.. doxygenfunction:: ecatRescueScan
    :outline:

.. doxygenfunction:: emRescueScan

.. dropdown:: **emRescueScan() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsRescueScanExample
        :end-before: DocumentationSnippetsRescueScanExample
        :language: cpp
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emSetSlavePortState`
    - :ref:`api_busscan:emNotify - EC_NOTIFY_FRAMELOSS_AFTER_SLAVE`

emConfigureNetwork
******************

.. doxygenfunction:: ecatConfigureNetwork
    :outline:

.. doxygenfunction:: emConfigureNetwork

.. doxygenenum:: EC_T_CNF_TYPE

Depending on this enum pbyCnfData is interpreted differently. This function may not be called from within the JobTask's context.

.. doxygenstruct:: EC_T_CNF_FILEBYAPP_DESC
    :members:
  
.. doxygentypedef:: EC_PF_CNF_OPEN
    :no-link:

.. doxygentypedef:: EC_PF_CNF_CLOSE
    :no-link:

.. doxygentypedef:: EC_PF_CNF_READ
    :no-link:

.. doxygentypedef:: EC_PF_CNF_ERROR
    :no-link:

.. doxygentypedef:: EC_PF_CNF_EOF
    :no-link:

.. dropdown:: **emConfigureNetwork() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsConfigureNetworkExample
        :end-before: DocumentationSnippetsConfigureNetworkExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emConfigGet
***********

.. doxygenfunction:: ecatConfigGet
    :outline:

.. doxygenfunction:: emConfigGet

.. dropdown:: **emConfigGet() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsConfigGetExample
        :end-before: DocumentationSnippetsConfigGetExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emConfigureNetwork`

emConfigExtend
**************

.. warning:: Before using this function, please check if the following patents has to be taken into consideration for your application and use case:
  **JP5212509:ADDRESS SETTING METHOD IN NETWORK SYSTEM**

.. doxygenfunction:: ecatConfigExtend
    :outline:

.. doxygenfunction:: emConfigExtend

.. dropdown:: **emConfigExtend() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsConfigExtendExample
        :end-before: DocumentationSnippetsConfigExtendExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emRegisterClient
****************

.. doxygenfunction:: ecatRegisterClient
    :outline:

.. doxygenfunction:: emRegisterClient

.. doxygentypedef:: EC_PF_NOTIFY
    :no-link:

.. doxygenstruct:: EC_T_REGISTERRESULTS
    :members:

.. dropdown:: **emRegisterClient() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsRegisterClientExample
        :end-before: DocumentationSnippetsRegisterClientExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emUnregisterClient
******************

.. doxygenfunction:: ecatUnregisterClient
    :outline:

.. doxygenfunction:: emUnregisterClient

emGetSrcMacAddress
******************

.. doxygenfunction:: ecatGetSrcMacAddress
    :outline:

.. doxygenfunction:: emGetSrcMacAddress

.. seealso:: :cpp:member:`EC_T_INIT_MASTER_PARMS::pLinkParms`

.. dropdown:: **emGetSrcMacAddress() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSrcMacAdressExample
        :end-before: DocumentationSnippetsGetSrcMacAdressExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emSetMasterState
****************

.. doxygenfunction:: ecatSetMasterState
    :outline:

.. doxygenfunction:: emSetMasterState

.. doxygenenum:: EC_T_STATE

.. dropdown:: **emSetMasterState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetMasterStateExample
        :end-before: DocumentationSnippetsSetMasterStateExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE`

emSetMasterStateReq
*******************

.. doxygenfunction:: ecatSetMasterStateReq
    :outline:

.. doxygenfunction:: emSetMasterStateReq

.. dropdown:: **emSetMasterStateReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetMasterStateReqExample
        :end-before: DocumentationSnippetsSetMasterStateReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE`

.. seealso:: :cpp:func:`emSetMasterState`

emGetMasterState
****************

.. doxygenfunction:: ecatGetMasterState
    :outline:

.. doxygenfunction:: emGetMasterState

.. dropdown:: **emGetMasterState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterStateExample
        :end-before: DocumentationSnippetsGetMasterStateExample
        :language: cpp
        :dedent: 4
        :lines: 2-

emGetMasterStateEx
******************

.. doxygenfunction:: ecatGetMasterStateEx
    :outline:

.. doxygenfunction:: emGetMasterStateEx

.. dropdown:: **emGetMasterStateEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterStateExExample
        :end-before: DocumentationSnippetsGetMasterStateExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emStart
*******

.. doxygenfunction:: ecatStart
    :outline:

.. doxygenfunction:: emStart

.. dropdown:: **emStart() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsStartExample
        :end-before: DocumentationSnippetsStartExample
        :language: cpp
        :dedent: 4
        :lines: 2-

emStop
******

.. doxygenfunction:: ecatStop
    :outline:

.. doxygenfunction:: emStop

.. dropdown:: **emStop() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsStopExample
        :end-before: DocumentationSnippetsStopExample
        :language: cpp
        :dedent: 4
        :lines: 2-

emExecJob
*********

.. doxygenfunction:: ecatExecJob
    :outline:

.. doxygenfunction:: emExecJob

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

#. :cpp:enumerator:`eUsrJob_SendAllCycFrames`
    Send all cyclic frames. New values will be written to the EtherCAT slave's outputs and new input values will be received. If the Real-time Ethernet Driver operates in interrupt mode, the process data input values will be updated immediately after receiving the frames. If the Real-time Ethernet Driver operates in polling mode, the next call to :cpp:func:`emExecJob` with the :cpp:enumerator:`eUsrJob_ProcessAllRxFrames` job will check for received frames and update the process data input values.

    .. code-block:: cpp

        pUserJobParms->dwNumFramesSent

    Indicates number of frames send within this call. Not used if pUserJobParms set to :c:macro:`EC_NULL`.

    Return: EC_E_NOERROR if successful, error code in case of failures.

    In case not all previously initiated cyclic frames are processed when calling this function an error notification will be generated ( :ref:`api:emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR`).

#. :cpp:enumerator:`eUsrJob_SendAcycFrames`
    Acyclic EtherCAT datagrams stored in the acyclic frame buffer FIFO will be sent when executing this call.

    .. code-block:: cpp

        pUserJobParms->dwNumFramesSent

    Indicates number of frames send within this call. Not used if pUserJobParms set to :c:macro:`EC_NULL`.

    Return: EC_E_NOERROR if successful, error code in case of failures.

#. :cpp:enumerator:`eUsrJob_MasterTimer`
    To trigger the master and slave state machines as well as the mailbox handling this call has to be executed cyclically. The master cycle time is determined by the period between calling :cpp:func:`emExecJob` ( :cpp:enumerator:`eUsrJob_MasterTimer`). The state-machines are handling the EtherCAT state change transfers.

    Return: EC_E_NOERROR if successful, error code in case of failures.

#. :cpp:enumerator:`eUsrJob_SendCycFramesByTaskId`
    Send cyclic frames related to a specific task id. If more than one cyclic entries are configured this user job can be used to send the appropriate cyclic frames. All frames stored in cyclic entries with the given task id will be sent.

    .. seealso:: :ref:`software-integration:Multiple cyclic entries configuration`

    .. code-block:: cpp

        pUserJobParms->SendCycFramesByTaskId.dwTaskId

    Task id.

    Return: EC_E_NOERROR if successful, error code in case of failures. If not all previously initiated cyclic frames for the same task are already processed when calling this function an error will be generated ( :ref:`api:emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR`).

#. :cpp:enumerator:`eUsrJob_ProcessRxFramesByTaskId`
    :cpp:enumerator:`eUsrJob_ProcessAcycRxFrames`

    .. seealso:: Feature-Pack Split Frame Processing

#. :cpp:enumerator:`eUsrJob_SwitchEoeFrames`
    This job must be called if :ref:`api:emIoControl - EC_IOCTL_SET_EOE_DEFFERED_SWITCHING_ENABLED` has been called before. It can be called in parallel to Send / Process jobs in a lower prioritized task

    .. code-block:: cpp

        pUserJobParms->SwitchEoeFrames.dwMaxPortsToProcess

    Indicates number of ports to be processed within this call. If zero, all ports will be processed.

    .. code-block:: cpp

        pUserJobParms->SwitchEoeFrames.dwNumFramesProcessed

    Returns number of frames processed within this call.

    Return: EC_E_NOERROR if successful

#. :cpp:enumerator:`eUsrJob_StartTask`
    Inform EC-Master that the current task is started. Specify pUserJobParms.StartTask.dwTaskId or pass pUserJobParms set to EC_NULL for task ID 0.
    
#. :cpp:enumerator:`eUsrJob_StopTask`
    Inform EC-Master that the current task is stopped. Specify pUserJobParms.StopTask.dwTaskId or pass pUserJobParms set to EC_NULL for task ID 0.
    
.. dropdown:: **emExecJob() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsExecJobExample
        :end-before: DocumentationSnippetsExecJobExample
        :language: cpp
        :dedent: 4
        :lines: 1-
    
emGetVersion
************

.. doxygenfunction:: ecatGetVersion
    :outline:

.. doxygenfunction:: emGetVersion

**EC Version Type**

.. datatemplate:xml:: EC_VERSION_TYPES
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. dropdown:: **emGetVersion() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetVersionExample
        :end-before: DocumentationSnippetsGetVersionExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emSetLicenseKey
***************

.. doxygenfunction:: ecatSetLicenseKey
    :outline:

.. doxygenfunction:: emSetLicenseKey

.. dropdown:: **emSetLicenseKey() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: IGNORE_TEST(DocumentationSnippets, emSetLicenseKey)
        :end-before: IGNORE_TEST(DocumentationSnippets, emSetLicenseKey)
        :language: cpp
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emInitMaster`
    - :cpp:func:`emConfigureNetwork`

emSetOemKey
***********

.. doxygenfunction:: ecatSetOemKey
    :outline:

.. doxygenfunction:: emSetOemKey

.. dropdown:: **emSetOemKey() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :language: cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, emSetOemKey)
        :end-before: IGNORE_TEST(DocumentationSnippets, emSetOemKey)
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emInitMaster`
    - :cpp:func:`emConfigureNetwork`

emIoControl
***********

.. doxygenfunction:: ecatIoControl
    :outline:

.. doxygenfunction:: emIoControl

.. doxygenstruct:: EC_T_IOCTLPARMS
    :members:

emIoControl - EC_IOCTL_GET_PDMEMORYSIZE
***************************************

Queries the master for the necessary size the process data image has got. This information may be used to provide process data image storage from outside the master core. This IOCTL is to be called after :cpp:func:`emConfigureNetwork` and before :cpp:func:`emStart`.

.. emIoControl:: EC_IOCTL_GET_PDMEMORYSIZE
    :pbyOutBuf: Pointer to memory where the memory size information will be stored (type: EC_T_MEMREQ_DESC).
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_MEMREQ_DESC
    :members:

emIoControl - EC_IOCTL_REGISTER_PDMEMORYPROVIDER
************************************************

This function call registers an external memory provider to the EtherCAT master, this memory will be used to store process data. If no memory provider is registered the master will internally allocate the necessary amount of memory.
The function :ref:`api:emIoControl - EC_IOCTL_GET_PDMEMORYSIZE` should be executed to determine the amount of memory the master needs to store process data values.
The external memory provider may additionally supply some hooks to give the master a possibility to synchronize memory access with the application.
The memory provider has to be registered after calling :cpp:func:`emConfigureNetwork` but prior to registering any client. Every client that registers with the master ( :cpp:func:`emRegisterClient` ) will get back the memory pointers to PDOut/PDIn data registered within this call.

.. emIoControl:: EC_IOCTL_REGISTER_PDMEMORYPROVIDER
    :pbyInBuf: Memory provider (EC_T_MEMPROV_DESC)
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_MEMPROV_DESC
    :members:

.. doxygentypedef:: EC_T_PFMEMREQ

.. doxygentypedef:: EC_T_PFMEMREL

.. seealso::
    - :ref:`api:emIoControl - EC_IOCTL_GET_PDMEMORYSIZE`
    - :cpp:func:`emConfigureNetwork`
    - :cpp:func:`emRegisterClient`
    - Feature Pack "Master Redundancy"

emIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB
**********************************************

This function call registers an callback function which is called after the cyclic frame is received. Typically this is used when the Real-time Ethernet Driver operates interrupt mode to get an event when the new input data (cyclic frame) is available.
The callback function has to be registered after calling :cpp:func:`emInitMaster` before starting the job task.

.. emIoControl:: EC_IOCTL_REGISTER_CYCFRAME_RX_CB
    :pbyInBuf: Cyclic frame received callback descriptor (EC_T_CYCFRAME_RX_CBDESC)
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_CYCFRAME_RX_CBDESC
    :members:

.. doxygentypedef:: EC_PF_CYCFRAME_RECV

emIoControl - EC_IOCTL_ISLINK_CONNECTED
***************************************

Determine whether link between the EtherCAT master and the first slave is connected.

.. emIoControl:: EC_IOCTL_ISLINK_CONNECTED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE link is connected, if EC_FALSE it is not.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

With Redundancy support enabled, :c:macro:`EC_FALSE` is only set if main and redundancy link are down.

emIoControl - EC_IOCTL_GET_LINKLAYER_MODE
*****************************************

This call allows the application to determine whether the Real-time Ethernet Driver is currently running in polling or in interrupt mode.

.. emIoControl:: EC_IOCTL_GET_LINKLAYER_MODE
    :pbyOutBuf: Pointer to struct EC_T_LINKLAYER_MODE_DESC
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_LINKLAYER_MODE_DESC
    :members:

emIoControl - EC_IOCTL_GET_CYCLIC_CONFIG_INFO
*********************************************

Determine cyclic configuration details from ENI configuration file. It can be called only after calling ecatConfigureNetwork() or emConfigureNetwork()

.. emIoControl:: EC_IOCTL_GET_CYCLIC_CONFIG_INFO
    :pbyInBuf: Pointer to dwCycEntryIndex: cyclic entry index for which to get information
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to EC_T_CYC_CONFIG_DESC data type
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_CYC_CONFIG_DESC
    :members:

emIoControl - EC_IOCTL_IS_SLAVETOSLAVE_COMM_CONFIGURED
******************************************************

Determine if any slave to slave communication is configured.

.. emIoControl:: EC_IOCTL_IS_SLAVETOSLAVE_COMM_CONFIGURED
    :pbyOutBuf: Pointer to EC_T_DWORD. If value is EC_TRUE slave to slave communication is configured, if EC_FALSE it is not.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

emIoControl - EC_LINKIOCTL...
*****************************

The generic control interface provides access to the main network adapter when adding :c:macro:`EC_IOCTL_LINKLAYER_MAIN` to the :c:macro:`EC_LINKIOCTL` parameter at dwCode.

.. code-block:: cpp

    EC_T_DWORD dwCode = (EC_IOCTL_LINKLAYER_MAIN | EC_LINKIOCTL_GET_ETHERNET_ADDRESS);

emIoControl - EC_LINKIOCTL_GET_ETHERNET_ADDRESS
***********************************************

Provides MAC addresses of main or red line.

.. emIoControl:: EC_LINKIOCTL_GET_ETHERNET_ADDRESS
    :pbyOutBuf: Pointer to MAC address buffer (6 bytes).
    :dwOutBufSize: Size of the output buffer in bytes (at least 6).
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

emIoControl - EC_LINKIOCTL_GET_SPEED
************************************

.. emIoControl:: EC_LINKIOCTL_GET_SPEED
    :pbyOutBuf: Pointer to EC_T_DWORD. Set by Real-time Ethernet Driver to 10/100/1000.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

emIoControl - EC_LINKIOCTL_GET_PCI_INFO
***************************************

Get current network adapter's PCI information

.. emIoControl:: EC_LINKIOCTL_GET_PCI_INFO
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

emIoControl - EC_IOCTL_SET_CYCFRAME_LAYOUT
******************************************

Set the cyclic frames layout.

.. emIoControl:: EC_IOCTL_SET_CYCFRAME_LAYOUT
    :pbyInBuf: Pointer to a EC_T_CYCFRAME_LAYOUT value containing the cyclic frame layout.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenenum:: EC_T_CYCFRAME_LAYOUT

emIoControl - EC_IOCTL_SET_MASTER_DEFAULT_TIMEOUTS
**************************************************

Set master default timeouts.

.. emIoControl:: EC_IOCTL_SET_MASTER_DEFAULT_TIMEOUTS
    :pbyInBuf: Pointer to EC_T_MASTERDEFAULTTIMEOUTS_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_MASTERDEFAULTTIMEOUTS_DESC
    :members:

Setting a value of this descriptor to zero resets the default timeout value to the initial value.

.. seealso:: - :cpp:func:`emSetMasterState`

emIoControl - EC_IOCTL_SET_COPYINFO_IN_SENDCYCFRAMES
****************************************************

Set copy info processed in either SendCycFrames or in ProcessAllRxFrames.

.. emIoControl:: EC_IOCTL_SET_COPYINFO_IN_SENDCYCFRAMES
    :pbyInBuf: Pointer to EC_T_BOOL. EC_TRUE: SendCycFrames, EC_FALSE: ProcessAllRxFrames
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Default: Set by ProcessAllRxFrames.

emIoControl - EC_IOCTL_SET_BUS_CYCLE_TIME
*****************************************

Set bus cycle time in usec master parameter without calling :cpp:func:`emInitMaster` again.

.. emIoControl:: EC_IOCTL_SET_BUS_CYCLE_TIME
    :pbyInBuf: Pointer to value of EC_T_DWORD. Value may not be 0!
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Implicitly recalculates Order Timeout and :cpp:member:`EC_T_INIT_MASTER_PARMS::dwEcatCmdTimeout`.

emIoControl - EC_IOCTL_ADDITIONAL_VARIABLES_FOR_SPECIFIC_DATA_TYPES
*******************************************************************

Enable or disable additional variables for specific data types. Default: Enabled.

.. emIoControl:: EC_IOCTL_ADDITIONAL_VARIABLES_FOR_SPECIFIC_DATA_TYPES
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: enable, EC_FALSE: disable.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Additional variables are added to the process image for the following data types:

- FSOE_4096
- FSOE_4098
- FSOE_4099
- FB Info 1
- FB Info 3

emIoControl - EC_IOCTL_SLV_ALIAS_ENABLE
***************************************

Enables slave alias addressing for all slaves.

.. emIoControl:: EC_IOCTL_SLV_ALIAS_ENABLE

.. important:: All slaves need to have the correct alias address set! If in doubt, don't use this IOCTL.

emIoControl - EC_IOCTL_SET_IGNORE_INPUTS_ON_WKC_ERROR
*****************************************************

Ignore inputs on WKC error

.. emIoControl:: EC_IOCTL_SET_IGNORE_INPUTS_ON_WKC_ERROR
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Ignore inputs on WKC error.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will ignore inputs data of cyclic commands on WKC error.
By default input data are updated if WKC is non zero. If WKC is not matching the expected value a notification :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR
***************************************************

Set inputs to zero on WKC error

.. emIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on WKC error.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on WKC error.
By default input data are updated if WKC is non zero. If WKC is not matching the expected value a notification :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO
**************************************************

Set inputs to zero on WKC is zero

.. emIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on WKC is zero.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on WKC is zero.
By default input data are ignored on WKC is zero and remain unchanged. If WKC is not matching the expected value a notification :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_FRAME_LOSS
****************************************************

Set inputs to zero on frame loss

.. emIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_FRAME_LOSS
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on frame loss.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on frame loss.
By default input data are ignored on frame loss and remain unchanged.

emIoControl - EC_IOCTL_SET_GENENI_ASSIGN_EEPROM_BACK_TO_EM
**********************************************************

Enable or disable creation of "assign EEPROM back to EM" InitCmd if ENI generated based on bus-scan result.

.. emIoControl:: EC_IOCTL_SET_GENENI_ASSIGN_EEPROM_BACK_TO_EM
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: generate InitCmd.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

The ENI's "assign EEPROM back to EM" InitCmd depends on the attribute "AssignToPdi" of the EEPROM tag in the slave's description within the ESI file. Because this attribute is not reflected in the SII in the slave's EEPROM, the Master cannot know its value and inserts for legacy reasons the InitCmd if not disabled using this IOCTL.

emIoControl - EC_IOCTL_SET_EOE_DEFFERED_SWITCHING_ENABLED
*********************************************************

Enable or disable deferred EoE switching

.. emIoControl:: EC_IOCTL_SET_EOE_DEFFERED_SWITCHING_ENABLED
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Deferred EoE switching enabled.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Enabling deffered EoE switching reduces the CPU load of JOB_ProcessAllRxFrames in case of EoE communication. :cpp:enumerator:`eUsrJob_SwitchEoeFrames` has to be called explicitely to switch the received EoE frames between the EoE slaves and EoE end point(s).

emIoControl - EC_IOCTL_SET_MAILBOX_POLLING_CYCLES
*************************************************

This call changes the mailbox polling cycles.

.. emIoControl:: EC_IOCTL_SET_MAILBOX_POLLING_CYCLES
    :pbyInBuf: Pointer to struct EC_T_SET_MAILBOX_POLLING_CYCLES_DESC
    :dwInBufSize: Size of the input buffer in bytes. E.g. sizeof(EC_T_SET_MAILBOX_POLLING_CYCLES_DESC)

.. doxygenstruct:: EC_T_SET_MAILBOX_POLLING_CYCLES_DESC
    :members:

emIoControl - EC_IOCTL_SET_MASTER_MAX_STATE
*******************************************

This call sets maximal master state. :cpp:func:`emSetMasterState` returns with  :c:macro:`EC_E_INVALIDSTATE` if the requested master state exceeds the maximal master state.

.. emIoControl:: EC_IOCTL_SET_MASTER_MAX_STATE
    :pbyInBuf: Pointer to value of EC_T_STATE
    :dwInBufSize: Size of the input buffer in bytes. E.g. sizeof(EC_T_STATE)

.. seealso::
    .. cpp:alias:: EC_T_STATE


emIoControl - EC_IOCTL_ACTIVATE_VOE_RECV_FIFO
*********************************************

This call activates the VoE receive FIFO and sets its size.

.. emIoControl:: EC_IOCTL_ACTIVATE_VOE_RECV_FIFO
    :pbyInBuf: Pointer to value of EC_T_WORD, size of the FIFO, use 0 to set it to the original size.
    :dwInBufSize: Size of the input buffer in bytes. E.g. sizeof(EC_T_WORD)


emIoControl - EC_IOCTL_SET_GEN_ENI_PARM
***************************************

This call changes the behavior when the configuration of the EtherCAT network is generated
according to a bus scan result of :cpp:func:`emConfigureNetwork` with the parameter
:cpp:enumerator:`EC_T_CNF_TYPE::eCnfType_GenPreopENI` or  :cpp:enumerator:`EC_T_CNF_TYPE::eCnfType_GenOpENI`.
In that case, default settings are taken to set e.g. the name of the EtherCAT slave device. The next table gives
an overview about the possible parameters to be changed.

+---------------------------------+---------------------------------------------------------------------------+
| Identifier                      | Description                                                               |
+=================================+===========================================================================+
| EC_GEN_ENI_PARM_ID_SLAVE_PREFIX | Prefix the name of the EtherCAT slave device and also the names of its    |
|                                 | variables with the given value. By default the prefix is 'Slave'.         |
+---------------------------------+---------------------------------------------------------------------------+

.. emIoControl:: EC_IOCTL_SET_GEN_ENI_PARM
    :pbyInBuf: Pointer to struct EC_T_SET_GEN_ENI_PARM
    :dwInBufSize: Size of the input buffer in bytes. E.g. sizeof(EC_T_SET_GEN_ENI_PARM)

.. doxygenstruct:: EC_T_SET_GEN_ENI_PARM
    :members:

.. doxygenunion:: EC_T_GEN_ENI_PARM
    :outline:

emIoControl - EC_IOCTL_REALLOC_MBX_QUEUE
****************************************

This call realloc the number of queues of the different mailbox protocols. 

.. emIoControl:: EC_IOCTL_REALLOC_MBX_QUEUE
    :pbyInBuf: Pointer to struct EC_T_REALLOC_MBX_QUEUE_DESC
    :dwInBufSize: Size of the input buffer in bytes. E.g. sizeof(EC_T_REALLOC_MBX_QUEUE_DESC)

.. doxygenstruct:: EC_T_REALLOC_MBX_QUEUE_DESC
    :members:

*******************
Process Data Access
*******************

emGetProcessData
****************

.. doxygenfunction:: ecatGetProcessData
    :outline:

.. doxygenfunction:: emGetProcessData

.. dropdown:: **emGetProcessData() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetProcessDataExample
        :end-before: DocumentationSnippetsGetProcessDataExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetProcessDataBits
********************

.. doxygenfunction:: ecatGetProcessDataBits
    :outline:

.. doxygenfunction:: emGetProcessDataBits

.. seealso:: :cpp:func:`emGetProcessData`

.. dropdown:: **emGetProcessDataBits() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetProcessDataBitsExample
        :end-before: DocumentationSnippetsGetProcessDataBitsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emSetProcessData
****************

.. doxygenfunction:: ecatSetProcessData
    :outline:

.. doxygenfunction:: emSetProcessData

.. dropdown:: **emSetProcessData() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetProcessDataExample
        :end-before: DocumentationSnippetsSetProcessDataExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emSetProcessDataBits
********************

.. doxygenfunction:: ecatSetProcessDataBits
    :outline:

.. doxygenfunction:: emSetProcessDataBits

.. seealso:: :cpp:func:`emSetProcessData`

.. dropdown:: **emSetProcessDataBits() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetProcessDataBitsExample
        :end-before: DocumentationSnippetsSetProcessDataBitsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emForceProcessDataBits
**********************

.. doxygenfunction:: ecatForceProcessDataBits
    :outline:

.. doxygenfunction:: emForceProcessDataBits

.. dropdown:: **emForceProcessDataBits() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsForceProcessDataBitsExample
        :end-before: DocumentationSnippetsForceProcessDataBitsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emSetProcessData`
    - :cpp:func:`emReleaseProcessDataBits`
    - :cpp:func:`emReleaseAllProcessDataBits`

emReleaseProcessDataBits
************************

.. doxygenfunction:: ecatReleaseProcessDataBits
    :outline:

.. doxygenfunction:: emReleaseProcessDataBits

.. dropdown:: **emReleaseProcessDataBits() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReleaseProcessDataBitsExample
        :end-before: DocumentationSnippetsReleaseProcessDataBitsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emSetProcessData`
    - :cpp:func:`emForceProcessDataBits`

emReleaseAllProcessDataBits
***************************

.. doxygenfunction:: ecatReleaseAllProcessDataBits
    :outline:

.. doxygenfunction:: emReleaseAllProcessDataBits

.. dropdown:: **emReleaseAllProcessDataBits() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReleaseAllProcessDataBitsExample
        :end-before: DocumentationSnippetsReleaseAllProcessDataBitsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emSetProcessData`
    - :cpp:func:`emForceProcessDataBits`

emGetProcessImageInputPtr
*************************

.. doxygenfunction:: ecatGetProcessImageInputPtr
    :outline:

.. doxygenfunction:: emGetProcessImageInputPtr

.. dropdown:: **emGetProcessImageInputPtr() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetProcessImageInputPtrExample 
        :end-before: DocumentationSnippetsGetProcessImageInputPtrExample
        :language: cpp
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emConfigureNetwork`
    - :ref:`api:emIoControl - EC_IOCTL_GET_PDMEMORYSIZE`
    - :ref:`api:emIoControl - EC_IOCTL_REGISTER_PDMEMORYPROVIDER`
    - :cpp:func:`emExecJob` ( :c:enum:`eUsrJob_ProcessAllRxFrames`) in case of Polling Mode


emGetProcessImageOutputPtr
**************************

.. doxygenfunction:: ecatGetProcessImageOutputPtr
    :outline:

.. doxygenfunction:: emGetProcessImageOutputPtr

.. dropdown:: **emGetProcessImageOutputPtr() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetProcessImageOutputPtrExample 
        :end-before: DocumentationSnippetsGetProcessImageOutputPtrExample
        :language: cpp
        :dedent: 4
        :lines: 2-

.. seealso::
    - :cpp:func:`emConfigureNetwork`
    - :ref:`api:emIoControl - EC_IOCTL_GET_PDMEMORYSIZE`
    - :ref:`api:emIoControl - EC_IOCTL_REGISTER_PDMEMORYPROVIDER`
    - :cpp:func:`emExecJob` ( :c:enum:`eUsrJob_SendAllCycFrames`)


emGetDiagnosisImagePtr
**********************

.. doxygenfunction:: ecatGetDiagnosisImagePtr
    :outline:

.. doxygenfunction:: emGetDiagnosisImagePtr

.. dropdown:: **emGetDiagnosisImagePtr() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetDiagnosisImagePtrExample
        :end-before: DocumentationSnippetsGetDiagnosisImagePtrExample
        :language: cpp
        :dedent: 4
        :lines: 2-

emGetDiagnosisImageSize
***********************

.. doxygenfunction:: ecatGetDiagnosisImageSize
    :outline:

.. doxygenfunction:: emGetDiagnosisImageSize

emGetSlaveInpVarInfoNumOf
*************************

.. doxygenfunction:: ecatGetSlaveInpVarInfoNumOf
    :outline:

.. doxygenfunction:: emGetSlaveInpVarInfoNumOf

.. seealso::
    - :cpp:func:`emGetSlaveInpVarInfo`
    - :cpp:func:`emGetSlaveInpVarInfoEx`
    
.. dropdown:: **emGetSlaveInpVarInfoNumOf() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveInpVarInfoNumOfExample
        :end-before: DocumentationSnippetsGetSlaveInpVarInfoNumOfExample
        :language: cpp
        :dedent: 4
        :lines: 1-
    

emGetSlaveInpVarInfo
********************

.. doxygenfunction:: ecatGetSlaveInpVarInfo
    :outline:

.. doxygenfunction:: emGetSlaveInpVarInfo

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO
    :members:
    
.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN

.. dropdown:: **emGetSlaveInpVarInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveInpVarInfoExample
        :end-before: DocumentationSnippetsGetSlaveInpVarInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetSlaveInpVarInfoEx
**********************

.. doxygenfunction:: ecatGetSlaveInpVarInfoEx
    :outline:

.. doxygenfunction:: emGetSlaveInpVarInfoEx

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO_EX
    :members:

.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN_EX

.. dropdown:: **emGetSlaveInpVarInfoEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveInpVarInfoExExample
        :end-before: DocumentationSnippetsGetSlaveInpVarInfoExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetSlaveOutpVarInfoNumOf
**************************

.. doxygenfunction:: ecatGetSlaveOutpVarInfoNumOf
    :outline:

.. doxygenfunction:: emGetSlaveOutpVarInfoNumOf
    
.. dropdown:: **emGetSlaveOutpVarInfoNumOf() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveOutpVarInfoNumOfExample 
        :end-before: DocumentationSnippetsGetSlaveOutpVarInfoNumOfExample
        :language: cpp
        :dedent: 4
        :lines: 1-
    
.. seealso::
    - :cpp:func:`emGetSlaveOutpVarInfo`
    - :cpp:func:`emGetSlaveOutpVarInfoEx`
    

emGetSlaveOutpVarInfo
*********************

.. doxygenfunction:: ecatGetSlaveOutpVarInfo
    :outline:

.. doxygenfunction:: emGetSlaveOutpVarInfo

.. dropdown:: **emGetSlaveOutpVarInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveOutpVarInfoExample 
        :end-before: DocumentationSnippetsGetSlaveOutpVarInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`


emGetSlaveOutpVarInfoEx
***********************

.. doxygenfunction:: ecatGetSlaveOutpVarInfoEx
    :outline:

.. doxygenfunction:: emGetSlaveOutpVarInfoEx

.. dropdown:: **emGetSlaveOutpVarInfoEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveOutpVarInfoExExample 
        :end-before: DocumentationSnippetsGetSlaveOutpVarInfoExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`


emGetSlaveInpVarByObjectEx
**************************

.. doxygenfunction:: ecatGetSlaveInpVarByObjectEx
    :outline:

.. doxygenfunction:: emGetSlaveInpVarByObjectEx

.. dropdown:: **emGetSlaveInpVarByObjectEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveInpVarByObjectExExample 
        :end-before: DocumentationSnippetsGetSlaveInpVarByObjectExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emGetSlaveOutpVarByObjectEx
***************************

.. doxygenfunction:: ecatGetSlaveOutpVarByObjectEx
    :outline:

.. doxygenfunction:: emGetSlaveOutpVarByObjectEx

.. dropdown:: **emGetSlaveOutpVarByObjectEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveOutpVarByObjectExExample
        :end-before: DocumentationSnippetsGetSlaveOutpVarByObjectExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emFindInpVarByName
******************

.. doxygenfunction:: ecatFindInpVarByName
    :outline:

.. doxygenfunction:: emFindInpVarByName

.. dropdown:: **emFindInpVarByName() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsFindInpVarByNameExample
        :end-before: DocumentationSnippetsFindInpVarByNameExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

emFindInpVarByNameEx
********************

.. doxygenfunction:: ecatFindInpVarByNameEx
    :outline:

.. doxygenfunction:: emFindInpVarByNameEx


.. dropdown:: **emFindInpVarByNameEx() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsFindInpVarByNameExExample
        :end-before: DocumentationSnippetsFindInpVarByNameExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emFindOutpVarByName
*******************

.. doxygenfunction:: ecatFindOutpVarByName
    :outline:

.. doxygenfunction:: emFindOutpVarByName

.. dropdown:: **emFindOutpVarByName() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsFindOutpVarByNameExample
        :end-before: DocumentationSnippetsFindOutpVarByNameExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

emFindOutpVarByNameEx
*********************

.. doxygenfunction:: ecatFindOutpVarByNameEx
    :outline:

.. doxygenfunction:: emFindOutpVarByNameEx

.. dropdown:: **emFindOutpVarByName() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsFindOutpVarByNameExExample
        :end-before: DocumentationSnippetsFindOutpVarByNameExExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emTraceDataConfig
*****************

.. doxygenfunction:: ecatTraceDataConfig
    :outline:

.. doxygenfunction:: emTraceDataConfig

emTraceDataGetInfo
******************

.. doxygenfunction:: ecatTraceDataGetInfo
    :outline:

.. doxygenfunction:: emTraceDataGetInfo

.. doxygenstruct:: EC_T_TRACE_DATA_INFO
    :members:
    
.. dropdown:: **emTraceDataGetInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsTraceDataConfigExample
        :end-before: DocumentationSnippetsTraceDataConfigExample
        :language: cpp
        :dedent: 4
        :lines: 1-

EC_GET_FRM_WORD
***************

.. doxygendefine:: EC_GET_FRM_WORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_WORD wResult = 0;

    wResult = EC_GET_FRM_WORD(byFrame);
    /* wResult is 0xF401 on little endian systems */

    wResult = EC_GET_FRM_WORD(byFrame + 5);
    /* wResult is 0x6000 on little endian systems */

    wResult = EC_GET_FRM_WORD(byFrame + 2);
    /* wResult is 0x85DD on little endian systems */

EC_GET_FRM_DWORD
****************

.. doxygendefine:: EC_GET_FRM_DWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_DWORD dwResult = 0;

    dwResult = EC_GET_FRM_DWORD(byFrame);
    /* dwResult is 0x85DDF401 on little endian systems */

    dwResult = EC_GET_FRM_DWORD(byFrame + 5);
    /* dwResult is 0x00C16000 on little endian systems */

    dwResult = EC_GET_FRM_DWORD(byFrame + 2);
    /* dwResult is 0x000385DD on little endian systems */

EC_GET_FRM_QWORD
****************

.. doxygendefine:: EC_GET_FRM_QWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_UINT64 ui64Result = 0;

    ui64Result = EC_GET_FRM_QWORD(byFrame + 1);
    /* wResult is 0x00C160000385DDF4 on little endian systems */

EC_SET_FRM_WORD
***************

.. doxygendefine:: EC_SET_FRM_WORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];

    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);

    EC_SET_FRM_WORD(byFrame + 1, 0x1234);
    /* byFrame = FF 34 12 FF FF FF ... */

EC_SET_FRM_DWORD
****************

.. doxygendefine:: EC_SET_FRM_DWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];

    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);

    EC_SET_FRM_DWORD(byFrame + 1, 0x12345678);
    /* byFrame = FF 78 56 34 12 FF ... */

EC_SET_FRM_QWORD
****************

.. doxygendefine:: EC_SET_FRM_QWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];

    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);

    EC_SET_FRM_QWORD(byFrame + 1, 0xFEDCBA9876543210);
    /* byFrame = FF 10 32 54 76 98 BA DC FE FF FF ... */

EC_COPYBITS
***********

.. doxygendefine:: EC_COPYBITS

.. seealso::
    - :c:macro:`EC_SETBITS`
    - :c:macro:`EC_GETBITS`

.. figure:: ../Media/EC_COPYBITS.png
    :alt:

.. code-block:: cpp

    EC_T_BYTE pbySrc[] = {0xF4, 0xED, 0x69, 0xA5};
    EC_T_BYTE pbyDst[] = {0x00, 0x00, 0x00, 0x00};
    EC_COPYBITS(pbyDst, 3, pbySrc, 6, 22);

    /* pbyDst now contains 0xB8 0x3D 0xAD 0x00 */

EC_COMPAREBITS
**************

.. doxygendefine:: EC_COMPAREBITS

.. seealso::
    - :c:macro:`EC_COPYBITS`

.. code-block:: cpp

    EC_T_BYTE pbyBuf1[] = {0xB8, 0x3D, 0xAD, 0x00};
    EC_T_BYTE pbyBuf2[] = {0xF4, 0xED, 0x69, 0xA5};
    assert(0 == EC_COMPAREBITS(pbyBuf1, 3, pbyBuf2, 6, 22));

EC_GETBITS
**********

.. doxygendefine:: EC_GETBITS

.. seealso::
    - :c:macro:`EC_GET_FRM_WORD`
    - :c:macro:`EC_GET_FRM_DWORD`
    - :c:macro:`EC_GET_FRM_QWORD`

EC_SETBITS
**********

.. doxygendefine:: EC_SETBITS

.. seealso::
    - :c:macro:`EC_SET_FRM_WORD`
    - :c:macro:`EC_SET_FRM_DWORD`
    - :c:macro:`EC_SET_FRM_QWORD`

EC_COPYBIT
**********

.. doxygendefine:: EC_COPYBIT

EC_TESTBIT
**********

.. doxygendefine:: EC_TESTBIT

EC_SETBIT
*********

.. doxygendefine:: EC_SETBIT

EC_CLRBIT
*********

.. doxygendefine:: EC_CLRBIT


******************************
Generic notification interface
******************************

One of the parameters the client has to set when registering with the EtherCAT master is a generic notification callback function ( :cpp:func:`emNotify`). The master calls this function every time a event (for example an error event) occurs about which the client has to be informed.

Within this callback function the client must not call any active EtherCAT functions which finally would lead to send EtherCAT commands (e.g. initiation of mailbox transfers, starting/stopping the master, sending raw commands). In such cases the behavior is undefined.

This callback function is usually called in the context of the EtherCAT master timer thread or the EtherCAT Real-time Ethernet Driver receiver thread. It may also be called within the context of a user thread (when calling an EtherCAT master function). To avoid dead-lock situations the notification callback handler may not use mutex semaphores.

As the whole EtherCAT operation is blocked while calling this function the error handling must not use much CPU time or even call operating system functions that may block. Usually the error handling will be done in a separate application thread.

Notification callback: emNotify
*******************************

When a client registers with the EtherCAT master the client has to determine a generic notification callback function. The master calls this function every time an event (for example an error event or operational state change event) occurs about which the client has to be informed. Within this callback function the client must not call any active EtherCAT functions which finally would lead to send EtherCAT commands (e.g. initiation of mailbox transfers, starting/stopping the master, sending raw commands). In such cases the behavior is undefined. Only EtherCAT functions which are explicitly marked to be callable within :cpp:func:`emNotify` may be called.

A further important rule exists due to the fact that this callback function is usually called in the context of the EtherCAT master timer thread. As the whole EtherCAT operation is blocked while calling this function the notification handler must not use much CPU time or even call operating system functions that may block. Time consuming operations should be executed in separate application threads.

.. cpp:alias:: EC_PF_NOTIFY

.. doxygenstruct:: EC_T_NOTIFYPARMS
    :members:

emNotify - EC_NOTIFY_STATECHANGED
*********************************

Notification about a change in the master's operational state. This notification is enabled by default.

.. emNotify:: EC_NOTIFY_STATECHANGED
    :pbyInBuf: Pointer to data of type EC_T_STATECHANGE which contains the old and the new master operational state.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_STATECHANGE
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emNotify - EC_NOTIFY_XXXX
*************************

Notification about an error.

.. emNotify:: EC_NOTIFY_XXXX
    :pbyInBuf: Pointer to data of type EC_T_ERROR_NOTIFICATION_DESC.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. seealso:: :ref:`api:Diagnosis, error detection, error notifications`

Feature Pack Master Redundancy Notifcations
*******************************************

.. seealso:: Feature Pack "Master Redundancy"

emNotifyApp
***********

By calling this function the generic notification callback function setup by :cpp:func:`emRegisterClient` is called for all clients including RAS.

.. doxygenfunction:: ecatNotifyApp
    :outline:

.. doxygenfunction:: emNotifyApp

The maximum value for dwCode is defined by :c:macro:`EC_NOTIFY_APP_MAX_CODE`

emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED
***********************************************

The following notifications can be enabled or disabled.

- :ref:`api:emNotify - EC_NOTIFY_SLAVE_STATECHANGED` (default Off)
- :ref:`api:emNotify - EC_NOTIFY_SLAVES_STATECHANGED` (default Off)
- :ref:`api:emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE` (default On)
- :ref:`api:emNotify - EC_NOTIFY_SLAVES_UNEXPECTED_STATE` (default Off)
- :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE` (default On)
- :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVES_PRESENCE` (default Off)
- :ref:`api:emNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO` (default On)
- :ref:`api:emNotify - EC_NOTIFY_SLAVES_ERROR_STATUS` (default Off)
- :ref:`api:emNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL` (default On)
- :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR`  (default On)
- :ref:`api_busscan:emNotify - EC_NOTIFY_SB_MISMATCH` (default On)
- :ref:`api_busscan:emNotify - EC_NOTIFY_SB_STATUS`  (default On)
- :ref:`api:emNotify - EC_NOTIFY_STATUS_SLAVE_ERROR` (default On)
- :ref:`api:emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR` (default On)
- :ref:`api_busscan:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` (default On)
- :ref:`api:emNotify - EC_NOTIFY_STATECHANGED` (default On)
- :ref:`mbx_coe:emNotify - EC_NOTIFY_COE_INIT_CMD` (default Off)
- :c:macro:`EC_NOTIFY_JUNCTION_RED_CHANGE` (default Off)
- :ref:`api:emNotify - EC_NOTIFY_ALL_DEVICES_OPERATIONAL` (default Off)
- :c:macro:`EC_NOTIFY_DC_STATUS` (default On)
- :c:macro:`EC_NOTIFY_DC_SLV_SYNC` (default On)
- :c:macro:`EC_NOTIFY_DCM_SYNC` (default On)
- :ref:`api:emNotify - EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR` (default On)
- :c:macro:`EC_NOTIFY_REFCLOCK_PRESENCE` (default Off)
- :c:macro:`EC_NOTIFY_DCX_SYNC` (default On)
- :c:macro:`EC_NOTIFY_HC_DETECTADDGROUPS` (default On)
- :ref:`api_busscan:emNotify - EC_NOTIFY_FRAMELOSS_AFTER_SLAVE` (default On)
- :ref:`api:emNotify - EC_NOTIFY_ETH_LINK_NOT_CONNECTED` (default On)
- :ref:`api:emNotify - EC_NOTIFY_S2SMBX_ERROR` (default On)
- :ref:`api:emNotify - EC_NOTIFY_SLAVE_INITCMD_WKC_ERROR` (default On)
- :ref:`api:emNotify - EC_NOTIFY_BAD_CONNECTION` (default On)

.. emIoControl:: EC_IOCTL_SET_NOTIFICATION_ENABLED
    :pbyInBuf: pointer to EC_T_SET_NOTIFICATION_ENABLED_PARMS.
    :dwInBufSize: size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SET_NOTIFICATION_ENABLED_PARMS
    :members:

Notifications are given to clients if enabled for dwClientId = 0  AND corresponding dwClientId.

emIoControl - EC_IOCTL_GET_NOTIFICATION_ENABLED
***********************************************

The enabled state of notifications can be retrieved using :ref:`api:emIoControl - EC_IOCTL_GET_NOTIFICATION_ENABLED`.

.. emIoControl:: EC_IOCTL_GET_NOTIFICATION_ENABLED
    :pbyInBuf: pointer to EC_T_GET_NOTIFICATION_ENABLED_PARMS.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to EC_T_BOOL to carry out current enable set.
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_GET_NOTIFICATION_ENABLED_PARMS
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED`

**********************************
Slave control and status functions
**********************************

emGetNumConfiguredSlaves
************************

.. doxygenfunction:: ecatGetNumConfiguredSlaves
    :outline:

.. doxygenfunction:: emGetNumConfiguredSlaves

.. dropdown:: **emGetNumConfiguredSlaves() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetNumConfiguredSlavesExample
        :end-before: DocumentationSnippetsGetNumConfiguredSlavesExample
        :language: cpp
        :dedent: 4
        :lines: 2-


emGetNumConnectedSlaves
***********************

.. doxygenfunction:: ecatGetNumConnectedSlaves
    :outline:

.. doxygenfunction:: emGetNumConnectedSlaves

.. dropdown:: **emGetNumConnectedSlaves() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetNumConnectedSlavesExample 
        :end-before: DocumentationSnippetsGetNumConnectedSlavesExample 
        :language: cpp
        :dedent: 4
        :lines: 2-

emGetSlaveId
************

.. doxygenfunction:: ecatGetSlaveId
    :outline:

.. doxygenfunction:: emGetSlaveId

.. dropdown:: **emGetSlaveId() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveIdExample
        :end-before: DocumentationSnippetsGetSlaveIdExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetSlaveIdAtPosition
**********************

.. doxygenfunction:: ecatGetSlaveIdAtPosition
    :outline:

.. doxygenfunction:: emGetSlaveIdAtPosition

.. dropdown:: **emGetSlaveIdAtPosition() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveIdAtPositionExample
        :end-before: DocumentationSnippetsGetSlaveIdAtPositionExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emSetSlaveState
***************

.. doxygenfunction:: ecatSetSlaveState
    :outline:

.. doxygenfunction:: emSetSlaveState

.. datatemplate:xml:: DEVICE_STATES
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. dropdown:: **emSetSlaveState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlaveStateExample
        :end-before: DocumentationSnippetsSetSlaveStateExample
        :language: cpp
        :dedent: 4
        :lines: 1-
.. seealso:: :cpp:func:`emGetSlaveId`

emSetSlaveStateReq
******************

.. doxygenfunction:: ecatSetSlaveStateReq
    :outline:

.. doxygenfunction:: emSetSlaveStateReq

.. dropdown:: **emSetSlaveStateReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlaveStateReqExample
        :end-before: DocumentationSnippetsSetSlaveStateReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emSetSlaveState`

.. seealso:: :cpp:func:`emGetSlaveId`

emGetSlaveState
***************

.. doxygenfunction:: ecatGetSlaveState
    :outline:

.. doxygenfunction:: emGetSlaveState

.. dropdown:: **emGetSlaveState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveStateExample
        :end-before: DocumentationSnippetsGetSlaveStateExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emGetSlaveId`
    - :cpp:func:`emSetSlaveState`

emIsSlavePresent
****************

This function may be called from within the JobTask. Since Slave Id is a parameter, valid response only can be retrieved after calling :cpp:func:`emConfigureNetwork`.

.. doxygenfunction:: ecatIsSlavePresent
    :outline:

.. doxygenfunction:: emIsSlavePresent

.. dropdown:: **emIsSlavePresent() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsIsSlavePresentExample
        :end-before: DocumentationSnippetsIsSlavePresentExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emGetSlaveProp
**************

.. doxygenfunction:: ecatGetSlaveProp
    :outline:

.. doxygenfunction:: emGetSlaveProp

.. dropdown:: **emGetSlaveProp() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlavePropExample
        :end-before: DocumentationSnippetsGetSlavePropExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emSlaveSerializeMbxTfers
************************

.. doxygenfunction:: ecatSlaveSerializeMbxTfers
    :outline:

.. doxygenfunction:: emSlaveSerializeMbxTfers

.. dropdown:: **emSlaveSerializeMbxTfers() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSlaveSerializeMbxTfersExample
        :end-before: DocumentationSnippetsSlaveSerializeMbxTfersExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emSlaveParallelMbxTfers
***********************

.. doxygenfunction:: ecatSlaveParallelMbxTfers
    :outline:

.. doxygenfunction:: emSlaveParallelMbxTfers

.. dropdown:: **emSlaveParallelMbxTfers() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSlaveParallelMbxTfersExample
        :end-before: DocumentationSnippetsSlaveParallelMbxTfersExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emIoControl - EC_IOCTL_SET_MBX_RETRYACCESS_PERIOD
*************************************************

Sets the mailbox retry access period in milliseconds for a specific slave. If a slave rejects a mailbox access because of a busy state, the master restarts mailbox access after that period of time.

.. emIoControl:: EC_IOCTL_SET_MBX_RETRYACCESS_PERIOD
    :pbyInBuf: Pointer to a size 6 byte array. The first 4 bytes must contain the slave id (EC_T_DWORD), the last 2 bytes the new retry access period in milliseconds(EC_T_WORD).
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

By default, the retry access period is set to 25 milliseconds.

emNotify - EC_NOTIFY_SLAVE_STATECHANGED
***************************************

This notification is given, when a slave changed its EtherCAT state. This notification is disabled by default.

.. emNotify:: EC_NOTIFY_SLAVE_STATECHANGED
    :pbyInBuf: Pointer to EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVE_STATECHANGED_NTFY_DESC
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the activation

emNotify - EC_NOTIFY_SLAVES_STATECHANGED
****************************************

Collects :ref:`api:emNotify - EC_NOTIFY_SLAVE_STATECHANGED`

This notification is disabled by default.

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the activation

.. emNotify:: EC_NOTIFY_SLAVES_STATECHANGED
    :pbyInBuf: Pointer to EC_T_SLAVES_STATECHANGED_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVES_STATECHANGED_NTFY_DESC_ENTRY
    :members:

emWriteSlaveRegister
********************

.. doxygenfunction:: ecatWriteSlaveRegister
    :outline:

.. doxygenfunction:: emWriteSlaveRegister

.. dropdown:: **emWriteSlaveRegister() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsWriteSlaveRegisterExample
        :end-before: DocumentationSnippetsWriteSlaveRegisterExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emWriteSlaveRegisterReq
***********************

.. doxygenfunction:: ecatWriteSlaveRegisterReq
    :outline:

.. doxygenfunction:: emWriteSlaveRegisterReq

.. dropdown:: **emWriteSlaveRegisterReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsWriteSlaveRegisterReqExample
        :end-before: DocumentationSnippetsWriteSlaveRegisterReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_SLAVE_REGISTER_TRANSFER`

emReadSlaveRegister
*******************

.. doxygenfunction:: ecatReadSlaveRegister
    :outline:

.. doxygenfunction:: emReadSlaveRegister

.. dropdown:: **emReadSlaveRegister() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveRegisterExample
        :end-before: DocumentationSnippetsReadSlaveRegisterExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emReadSlaveRegisterReq
**********************

.. doxygenfunction:: ecatReadSlaveRegisterReq
    :outline:

.. doxygenfunction:: emReadSlaveRegisterReq

.. dropdown:: **emReadSlaveRegisterReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveRegisterReqExample
        :end-before: DocumentationSnippetsReadSlaveRegisterReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_SLAVE_REGISTER_TRANSFER`

emNotify - EC_NOTIFY_SLAVE_REGISTER_TRANSFER
********************************************

This notification is given, when a slave register transfer is completed.

.. emNotify:: EC_NOTIFY_SLAVE_REGISTER_TRANSFER
    :pbyInBuf: Pointer to EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
    :members:

emReadSlaveEEPRom
*****************

.. doxygenfunction:: ecatReadSlaveEEPRom
    :outline:

.. doxygenfunction:: emReadSlaveEEPRom

.. dropdown:: **emReadSlaveEEPRom() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveEEPRomExample
        :end-before: DocumentationSnippetsReadSlaveEEPRomExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emReadSlaveEEPRomReq
********************

.. doxygenfunction:: ecatReadSlaveEEPRomReq
    :outline:

.. doxygenfunction:: emReadSlaveEEPRomReq

.. dropdown:: **emReadSlaveEEPRomReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveEEPRomReqExample
        :end-before: DocumentationSnippetsReadSlaveEEPRomReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_EEPROM_OPERATION`

emWriteSlaveEEPRom
******************

.. doxygenfunction:: ecatWriteSlaveEEPRom
    :outline:

.. doxygenfunction:: emWriteSlaveEEPRom

.. dropdown:: **emWriteSlaveEEPRom() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsWriteSlaveEEPRomExample 
        :end-before: DocumentationSnippetsWriteSlaveEEPRomExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emResetSlaveController`

emWriteSlaveEEPRomReq
*********************

.. doxygenfunction:: ecatWriteSlaveEEPRomReq
    :outline:

.. doxygenfunction:: emWriteSlaveEEPRomReq

.. dropdown:: **emWriteSlaveEEPRomReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsWriteSlaveEEPRomReqExample
        :end-before: DocumentationSnippetsWriteSlaveEEPRomReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emResetSlaveController`
    - :ref:`api:emNotify - EC_NOTIFY_EEPROM_OPERATION`

emAssignSlaveEEPRom
*******************

.. doxygenfunction:: ecatAssignSlaveEEPRom
    :outline:

.. doxygenfunction:: emAssignSlaveEEPRom

.. dropdown:: **emAssignSlaveEEPRom() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsAssignSlaveEEPRomExample
        :end-before: DocumentationSnippetsAssignSlaveEEPRomExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emAssignSlaveEEPRomReq
**********************

.. doxygenfunction:: ecatAssignSlaveEEPRomReq
    :outline:

.. doxygenfunction:: emAssignSlaveEEPRomReq

.. dropdown:: **emAssignSlaveEEPRomReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsAssignSlaveEEPRomReqExample
        :end-before: DocumentationSnippetsAssignSlaveEEPRomReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_EEPROM_OPERATION`

emActiveSlaveEEPRom
*******************

.. doxygenfunction:: ecatActiveSlaveEEPRom
    :outline:

.. doxygenfunction:: emActiveSlaveEEPRom

.. dropdown:: **emActiveSlaveEEPRom() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsActivateSlaveEEPRomExample 
        :end-before: DocumentationSnippetsActivateSlaveEEPRomExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emActiveSlaveEEPRomReq
**********************

.. doxygenfunction:: ecatActiveSlaveEEPRomReq
    :outline:

.. doxygenfunction:: emActiveSlaveEEPRomReq

.. dropdown:: **emActiveSlaveEEPRomReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsActivateSlaveEEPRomReqExample
        :end-before: DocumentationSnippetsActivateSlaveEEPRomReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_EEPROM_OPERATION`

emReloadSlaveEEPRom
*******************

.. doxygenfunction:: ecatReloadSlaveEEPRom
    :outline:

.. doxygenfunction:: emReloadSlaveEEPRom

.. dropdown:: **emReloadSlaveEEPRom() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReloadSlaveEEPRomExample
        :end-before: DocumentationSnippetsReloadSlaveEEPRomExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emResetSlaveController`

emReloadSlaveEEPRomReq
**********************

.. doxygenfunction:: ecatReloadSlaveEEPRomReq
    :outline:

.. doxygenfunction:: emReloadSlaveEEPRomReq

.. dropdown:: **emReloadSlaveEEPRomReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReloadSlaveEEPRomReqExample
        :end-before: DocumentationSnippetsReloadSlaveEEPRomReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :ref:`api:emNotify - EC_NOTIFY_EEPROM_OPERATION`
    - :cpp:func:`emResetSlaveController`

emNotify - EC_NOTIFY_EEPROM_OPERATION
*************************************

This notification is given, when a slave EEPROM operation is completed.

.. emNotify:: EC_NOTIFY_EEPROM_OPERATION
    :pbyInBuf: Pointer to EC_T_EEPROM_OPERATION_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_EEPROM_OPERATION_NTFY_DESC
    :members:

.. doxygenenum:: EC_T_EEPROM_OPERATION_TYPE

emResetSlaveController
**********************

.. doxygenfunction:: ecatResetSlaveController
    :outline:

.. doxygenfunction:: emResetSlaveController

.. dropdown:: **emResetSlaveController() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsResetSlaveControllerExample
        :end-before: DocumentationSnippetsResetSlaveControllerExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emIoControl - EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE
*********************************************************

Specifies if all the slaves must reach the requested master state.

.. emIoControl:: EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE all slaves must reach the master requested state, if set to EC_FALSE the master can reach the requested state even if some slaves are missing or cannot reach the requested state.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Missing mandatory slaves will be signalized by :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE`. Slaves who cannot reach the requested master state will be signalized by :ref:`api:emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE`. :ref:`api:emNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL` will not be generated anymore if this IOCTL is called with :c:macro:`EC_FALSE`, :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` will be still generated.

emGetCfgSlaveInfo
*****************

.. doxygenfunction:: ecatGetCfgSlaveInfo
    :outline:

.. doxygenfunction:: emGetCfgSlaveInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_INFO
    :members:

**Supported mailbox protocols flags**

.. datatemplate:xml:: EC_MBX_PROTOCOLS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. dropdown:: **emGetCfgSlaveInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetCfgSlaveInfoExample
        :end-before: DocumentationSnippetsGetCfgSlaveInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetCfgSlaveEoeInfo
********************

.. doxygenfunction:: ecatGetCfgSlaveEoeInfo
    :outline:

.. doxygenfunction:: emGetCfgSlaveEoeInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_EOE_INFO
    :members:

.. dropdown:: **emGetCfgSlaveEoeInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetCfgSlaveEoeInfoExample
        :end-before: DocumentationSnippetsGetCfgSlaveEoeInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetCfgSlaveSmInfo
********************

.. doxygenfunction:: ecatGetCfgSlaveSmInfo
    :outline:

.. doxygenfunction:: emGetCfgSlaveSmInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_ENTRY
    :members:

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_INFO
    :members:

.. dropdown:: **emGetCfgSlaveSmInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetCfgSlaveSmInfoExample
        :end-before: DocumentationSnippetsGetCfgSlaveSmInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetBusSlaveInfo
*****************

.. doxygenfunction:: ecatGetBusSlaveInfo
    :outline:

.. doxygenfunction:: emGetBusSlaveInfo

.. doxygenstruct:: EC_T_BUS_SLAVE_INFO
    :members:

**Port Slave ID's**

.. datatemplate:xml:: EC_SLAVE_IDS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

**EC_LINECROSSED_ flags**

.. datatemplate:xml:: EC_LINECROSSED_FLAGS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. dropdown:: **emGetBusSlaveInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetBusSlaveInfoExample
        :end-before: DocumentationSnippetsGetBusSlaveInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emReadSlaveIdentification
*************************

.. doxygenfunction:: ecatReadSlaveIdentification
    :outline:

.. doxygenfunction:: emReadSlaveIdentification

.. dropdown:: **emReadSlaveIdentification() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveIdentificationExample
        :end-before: DocumentationSnippetsReadSlaveIdentificationExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emReadSlaveIdentificationReq
****************************

.. doxygenfunction:: ecatReadSlaveIdentificationReq
    :outline:

.. doxygenfunction:: emReadSlaveIdentificationReq

.. dropdown:: **emReadSlaveIdentificationReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsReadSlaveIdentificationReqExample
        :end-before: DocumentationSnippetsReadSlaveIdentificationReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_SLAVE_IDENTIFICATION`


emNotify - EC_NOTIFY_SLAVE_IDENTIFICATION
*****************************************

This notification is given, when the read slave identification request is completed.

.. emNotify:: EC_NOTIFY_SLAVE_IDENTIFICATION
    :pbyInBuf: Pointer to EC_T_SLAVE_IDENTIFICATION_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_SLAVE_IDENTIFICATION_NTFY_DESC
    :members:

emIoControl - EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
***********************************************************

Specifies if slave errors must be automatically acknowledged

.. emIoControl:: EC_IOCTL_SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE slave errors must be automatically acknowledged, if set to EC_FALSE the application must acknowledge slave errors explicitly
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

The pending slave error will be acknowledged during the next :cpp:func:`emSetSlaveState` call.

emIoControl - EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED
*********************************************************

Specifies if the cyclic commands expected WKC must be automatically adjusted according the state and the presence of the slaves.

.. emIoControl:: EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED
    :pbyInBuf: Pointer to EC_T_BOOL variable. If set to EC_TRUE cyclic commands expected WKC must be automatically adjusted, if set to EC_FALSE the cyclic commands expected WKC stay unchanged
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

If TRUE, the notification :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is only generated if a slave doesn't increment the WKC although it should. :c:macro:`AUTO_ADJUST_CYCCMD_WKC` is disabled by default.

.. seealso::
    - :ref:`software-integration:Cyclic cmd WKC validation`
    - :ref:`software-integration:Working Counter (WKC) State in Diagnosis Image`

emSetSlaveDisabled
******************

Before using this function, please check if the following patents has to be taken into consideration for your application and use case:

- JP2014146077: CONTROL DEVICE AND OPERATION METHOD FOR CONTROL DEVICE
- JP2014146070: CONTROL DEVICE, CONTROL METHOD, AND PROGRAM
- JP2014120884: INFORMATION PROCESSING APPARATUS, INFORMATION ROCESSING PROGRAM, AND INFORMATION PROCESSING METHOD

.. doxygenfunction:: ecatSetSlaveDisabled
    :outline:

.. doxygenfunction:: emSetSlaveDisabled

.. dropdown:: **emSetSlaveDisabled() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlaveDisabledExample
        :end-before: DocumentationSnippetsSetSlaveDisabledExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emIoControl - EC_IOCTL_SET_SLAVE_MAX_STATE
*********************************************************

Specifies maximum state for specific slave.

.. emIoControl:: EC_IOCTL_SET_SLAVE_MAX_STATE
    :pbyInBuf: Pointer to EC_T_SLAVE_MAX_STATE_DESC. Specifies maximum state for the specific slave.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emSetSlaveDisconnected
**********************

Before using this function, please check if the following patents has to be taken into consideration for your application and use case:

- JP2014146077: CONTROL DEVICE AND OPERATION METHOD FOR CONTROL DEVICE
- JP2014146070: CONTROL DEVICE, CONTROL METHOD, AND PROGRAM
- JP2014120884: INFORMATION PROCESSING APPARATUS, INFORMATION ROCESSING PROGRAM, AND INFORMATION PROCESSING METHOD

.. doxygenfunction:: ecatSetSlaveDisconnected
    :outline:

.. doxygenfunction:: emSetSlaveDisconnected

.. dropdown:: **emSetSlaveDisconnected() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlaveDisconnectedExample
        :end-before: DocumentationSnippetsSetSlaveDisconnectedExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emSetSlavesDisconnected
***********************

Before using this function, please check if the following patents has to be taken into consideration for your application and use case:

- JP2014146077: CONTROL DEVICE AND OPERATION METHOD FOR CONTROL DEVICE
- JP2014146070: CONTROL DEVICE, CONTROL METHOD, AND PROGRAM
- JP2014120884: INFORMATION PROCESSING APPARATUS, INFORMATION ROCESSING PROGRAM, AND INFORMATION PROCESSING METHOD

.. doxygenfunction:: ecatSetSlavesDisconnected
    :outline:

.. doxygenfunction:: emSetSlavesDisconnected

.. dropdown:: **emSetSlavesDisconnected() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlavesDisconnectedExample
        :end-before: DocumentationSnippetsSetSlavesDisconnectedExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emSetSlaveDisconnected`

emGetSlavePortState
*******************

.. doxygenfunction:: ecatGetSlavePortState
    :outline:

.. doxygenfunction:: emGetSlavePortState

.. dropdown:: **emGetSlavePortState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlavePortStateExample
        :end-before: DocumentationSnippetsGetSlavePortStateExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emSetSlavePortState
*******************

.. doxygenfunction:: ecatSetSlavePortState
    :outline:

.. doxygenfunction:: emSetSlavePortState

.. dropdown:: **emSetSlavePortState() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlavePortStateExample
        :end-before: DocumentationSnippetsSetSlavePortStateExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :cpp:func:`emRescueScan`
    - :cpp:func:`emGetSlaveId`

emSetSlavePortStateReq
**********************

.. doxygenfunction:: ecatSetSlavePortStateReq
    :outline:

.. doxygenfunction:: emSetSlavePortStateReq

.. dropdown:: **emSetSlavePortStateReq() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSetSlavePortStateReqExample
        :end-before: DocumentationSnippetsSetSlavePortStateReqExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :ref:`api:emNotify - EC_NOTIFY_PORT_OPERATION`
    - :cpp:func:`emRescueScan`
    - :cpp:func:`emGetSlaveId`

emNotify - EC_NOTIFY_PORT_OPERATION
***********************************

This notification is given, when the port operation request is completed.

.. emNotify:: EC_NOTIFY_PORT_OPERATION
    :pbyInBuf: Pointer to EC_T_PORT_OPERATION_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_PORT_OPERATION_NTFY_DESC
    :members:

.. seealso:: :cpp:func:`emGetSlavePortState`

emIoControl - EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT
************************************************

Force state change to INIT for all new slaves in network after detection.

.. emIoControl:: EC_IOCTL_SET_NEW_BUSSLAVES_TO_INIT
    :pbyInBuf: Pointer to EC_T_BOOL. EC_TRUE: Force state change, EC_FALSE: No state change.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes

Default: No state change after detection

***********************************************
Diagnosis, error detection, error notifications
***********************************************

In case of errors on the bus or in one or multiple slaves the EtherCAT master stack will notify the application about such an event. The master automatically detects unexpected slaves states by evaluating the AL Status event interrupt. If the interrupt is set, the master reads the state of each slave and compares it to the expected (required) state. In case of a state mismatch the master generates the notification :ref:`api:emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE`. The application will then have to enter an error handling procedure.

The error notifications can be separated into two classes:

#. Slave unrelated errors
#. Slave related errors

A slave related error notification will also contain the information about which slave has generated an error. If for example a slave could not be set into the requested state the application will get the :ref:`api:emNotify - EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR` error notification including slave related information. A slave unrelated error does not contain this information even if one specific slave caused the error. For example if one or multiple slaves are powered off the working counter of the cyclic commands would be wrong. In that case the :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` error notification will be generated.

**Example Error Scenario**

Slave is powered off or disconnected while bus is operational

If the master is operational it cyclically sends EtherCAT commands to read and write the slave's process data. It expects the working counter to be incremented to the appropriate value. If one slave is powered off the master will generate the :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` to indicate such an event. Also the master detects a DL status event and performs a bus scan as reaction on this. For the not reachable slaves (powered off or disconnected) the master generates the notification :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE`.

A possible error recovery scenario would be to stay operational and in parallel wait until the slave is powered on again. The next step would be to determine the slave's state and set it operational again:

Master calls :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR`
    - Application gets informed
    - WKC State in Diagnosis Image changes

    .. seealso:: :ref:`software-integration:Working Counter (WKC) State in Diagnosis Image`

**Use cases**

#. Slave is disconnected or powered off:
    - Master detects a DL status event interrupt an performs a bus scan.
    - Master calls :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE`
    - Application gets informed and could set the whole master into a lower state, e.g. :cpp:enumerator:`eEcatState_INIT`

#. Slave state is not OPERATIONAL anymore
    - Master calls :ref:`api:emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE`
    - Application gets informed and could either set the whole master into lower state (e.g. :cpp:enumerator:`eEcatState_PREOP`), or calls :cpp:func:`emSetSlaveState` to repair the failed slave.

#. Slave is re-connected or powered on:
    - Master detects a DL status event interrupt an performs a bus scan.
    - Master calls :ref:`api_busscan:emNotify - EC_NOTIFY_SLAVE_PRESENCE`.
    - Application could wait until all slaves are re-connected by calling the functions :cpp:func:`emGetNumConnectedSlaves` and :cpp:func:`emGetNumConfiguredSlaves`.
    - After all slaves are re-connected the application could either set the whole master to :cpp:enumerator:`eEcatState_INIT` and afterwards to `:cpp:enumerator:`eEcatState_OP`, or the application uses :cpp:func:`emSetSlaveState` to repair only the failed slaves.

emSetLogParms
*************

.. doxygenfunction:: ecatSetLogParms
    :outline:

.. doxygenfunction:: emSetLogParms


emEthDbgMsg
***********

.. doxygenfunction:: ecatEthDbgMsg
    :outline:

.. doxygenfunction:: emEthDbgMsg

.. dropdown:: **emEthDbgMsg() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsEthDbgMsgExample
        :end-before: DocumentationSnippetsEthDbgMsgExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emIoControl - EC_IOCTL_GET_SLVSTATISTICS
****************************************

Get Slave's statistics counter. Counters are collected on a regularly base (default: off) and show errors on Real-time Ethernet Driver.

.. emIoControl:: EC_IOCTL_GET_SLVSTATISTICS
    :pbyInBuf: Pointer to a EC_T_DWORD type variable containing the slave id.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to struct EC_T_SLVSTATISTICS_DESC
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_SLVSTATISTICS_DESC
    :members:

.. seealso::
    - :ref:`api:emIoControl - EC_IOCTL_SET_SLVSTAT_PERIOD`
    - :ref:`api:emIoControl - EC_IOCTL_CLR_SLVSTATISTICS`

emGetSlaveStatistics
********************

.. doxygenfunction:: ecatGetSlaveStatistics
    :outline:

.. doxygenfunction:: emGetSlaveStatistics

.. dropdown:: **emGetSlaveStatistics() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetSlaveStatisticsExample
        :end-before: DocumentationSnippetsGetSlaveStatisticsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso::
    - :ref:`api:emIoControl - EC_IOCTL_GET_SLVSTATISTICS`
    - :cpp:func:`emGetSlaveId`

emIoControl - EC_IOCTL_CLR_SLVSTATISTICS
****************************************

Clear all error registers in all slaves

.. emIoControl:: EC_IOCTL_CLR_SLVSTATISTICS

emClearSlaveStatistics
**********************

.. doxygenfunction:: ecatClearSlaveStatistics
    :outline:

.. doxygenfunction:: emClearSlaveStatistics

.. dropdown:: **emClearSlaveStatistics() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsClearSlaveStatisticsExample
        :end-before: DocumentationSnippetsClearSlaveStatisticsExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetSlaveId`

emIoControl - EC_IOCTL_GET_SLVSTAT_PERIOD
*****************************************

Get Slave Statistics collection period. Period of 0: automatic slave statistics collection disabled.

.. emIoControl:: EC_IOCTL_GET_SLVSTAT_PERIOD
    :pbyOutBuf: Pointer to a EC_T_DWORD type variable containing the slave statistics collection period [ms] to get.
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

emIoControl - EC_IOCTL_SET_SLVSTAT_PERIOD
*****************************************

Update Slave Statistics collection period. It implicitly forces an immediate collection of slave statistics if performed successfully.

A Period of 0 disables automatic slave statistics collection, otherwise it set the time between the read sequences.

.. emIoControl:: EC_IOCTL_SET_SLVSTAT_PERIOD
    :pbyInBuf: pointer to a EC_T_DWORD type variable containing the slave statistics collection period [ms] to set.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emIoControl - EC_IOCTL_FORCE_SLVSTAT_COLLECTION
***********************************************

Sends datagrams to collect slave statistics counters.

.. emIoControl:: EC_IOCTL_FORCE_SLVSTAT_COLLECTION

emIoControl - EC_IOCTL_CLEAR_MASTER_INFO_COUNTERS
*************************************************

Reset Master Info Counters according to given bit masks

.. emIoControl:: EC_IOCTL_CLEAR_MASTER_INFO_COUNTERS
    :pbyInBuf: Pointer to value of EC_T_CLEAR_MASTER_INFO_COUNTERS_PARMS.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

.. doxygenstruct:: EC_T_CLEAR_MASTER_INFO_COUNTERS_PARMS
    :members:

.. code-block:: cpp

    qwMailboxStatisticsClearCounters = 0x0000000100; //Clear CoE Total Read Transfer Count.

emIoControl - EC_IOCTL_SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK
***********************************************************

Sets a bit mask to enable or disable the generation of specific error notifications of frame response errors. The application then can decide to suppress those error messages. By default all errors, expect :c:macro:`EC_FRAME_RESPONSE_ERROR_NOTIFY_MASK_NON_ECAT_FRAME` are enabled (the notification mask is set to :c:macro:`EC_FRAME_RESPONSE_ERROR_NOTIFY_MASK_DEFAULT`).

.. emIoControl:: EC_IOCTL_SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK
    :pbyInBuf: pointer to a EC_T_DWORD type value containing the new error mask.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

The following frame response error notification mask values exist:

.. datatemplate:xml:: EC_FRAME_RESPONSE_ERROR_NOTIFY_MASKS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. seealso:: :ref:`api:emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR`

emIoControl - EC_IOCTL_SET_FRAME_LOSS_SIMULATION
************************************************

This IO Control enables the application to simulate the loss of sent and/or received EtherCAT frames for testing purposes.
Three modes of operation are possible: Random, periodic or random periodic frame loss simulation.

- Random frame loss simulation: For each frame the dwFrameLossLikelihoodPpm parameter determines whether the frame will be discarded.
- Periodic frame loss simulation: After dwFixedLossNumLostFrames discarded frames, dwFixedLossNumGoodFrames frames will be processed.
- Random periodic frame loss simulation: The dwFrameLossLikelihoodPpm parameter determines whether a periodic frame loss sequence is triggered.

.. important:: Do not activate this on shipped releases. Frameloss has significant influence on performance and reliablility of the application!

.. emIoControl:: EC_IOCTL_SET_FRAME_LOSS_SIMULATION
    :pbyInBuf: Array of four EC_T_DWORDs (arrDword)
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

The parameters configurable are :

- arrDword [0] -> dwNumGoodFramesAfterStart
    Number of good frames before frame loss simulation starts
- arrDword [1] -> dwFrameLossLikelihoodPpm
    Random loss simulation: frame loss likelihood (ppm)
- arrDword [2] -> dwFixedLossNumGoodFrames
    Fixed loss simulation: number of good frames before frame loss
- arrDword [3] -> dwFixedLossNumLostFrames
    Fixed loss simulation: number of lost frames after processing the good ones

emIoControl - EC_IOCTL_SET_RXFRAME_LOSS_SIMULATION
**************************************************

Same as :ref:`api:emIoControl - EC_IOCTL_SET_FRAME_LOSS_SIMULATION` but only enables receive direction frame losses.

.. emIoControl:: EC_IOCTL_SET_RXFRAME_LOSS_SIMULATION

emIoControl - EC_IOCTL_SET_TXFRAME_LOSS_SIMULATION
**************************************************

Same as :ref:`api:emIoControl - EC_IOCTL_SET_FRAME_LOSS_SIMULATION` but only enables transmit direction frame losses.

.. emIoControl:: EC_IOCTL_SET_TXFRAME_LOSS_SIMULATION

Error notifications - general information
*****************************************

For each error an error ID (error code) will be defined. This error ID will be used as the notification code when :cpp:func:`emNotify` is called. In addition to this notification code the second parameter given to :cpp:func:`emNotify` contains a pointer to an error notification descriptor of type :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. This error notification descriptor contains detailed information about the error.

.. doxygenstruct:: EC_T_ERROR_NOTIFICATION_DESC
    :members:

If the pointer to this descriptor exists (is not set to :cpp:struct:`EC_NULL`) the detailed error information (e.g. information about the slave) is stored in the appropriate structure of a union. These error information structures are described in the following sections.

The EtherCAT master will call :cpp:func:`emNotify` every time an error is detected. In some cases this will lead to calling this function in every EtherCAT cycle (e.g. if there is no physical connection to the slaves). Using the control interface :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` it is possible to determine which errors shall be signalled and which not.

emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR
*************************************

To update the process data some EtherCAT commands will be sent cyclically by the master. These commands will address one or multiple slaves. These EtherCAT commands contain a working counter which has to be incremented by each slave that is addressed. The working counter will be checked after the EtherCAT command is received by the master.
If the expected working counter will not match to the working counter of the received command the error :ref:`api:emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` will be indicated. The working counter value expected by the master is determined by the EtherCAT configuration (XML) file for each cyclic EtherCAT command (section Config/Cyclic/Frame/Cmd/Cnt).
Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

This notification is enabled by default.

.. doxygenstruct:: EC_T_WKCERR_DESC
    :members:

.. doxygenstruct:: EC_T_SLAVE_PROP
    :members:

.. seealso::
    - :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation.
    - :ref:`software-integration:Cyclic cmd WKC validation`
    - :ref:`software-integration:Working Counter (WKC) State in Diagnosis Image`
    - :ref:`api:emIoControl - EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED`

emNotify - EC_NOTIFY_MASTER_INITCMD_WKC_ERROR
*********************************************

This error will be indicated in case of a working counter mismatch when sending master init commands. The working counter value expected by the master is determined by the EtherCAT configuration (XML) file for each master init command (section Config/Master/InitCmds/InitCmd/Cnt). In case there is no "Cnt" entry in the XML file for this init command there will be no working counter verification. The working counter has to be incremented by all slaves which have to process this init command.

Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

emNotify - EC_NOTIFY_SLAVE_INITCMD_WKC_ERROR
********************************************

This error will be indicated in case of a working counter mismatch when sending slave init commands. The working counter value expected by the master is determined by the EtherCAT configuration (XML) file for each slave init command (section Config/Slave/InitCmds/InitCmd/Cnt). In case there is no "Cnt" entry in the XML file for this init command there will be no working counter verification.

Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. The structure member SlaveProp contains information about the corresponding slave device.

emNotify - EC_NOTIFY_FOE_MBSLAVE_ERROR
**************************************

This error will be indicated in case a slave notifies an error over FoE.

emNotify - EC_NOTIFY_EOE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a EoE mailbox write command was not set to the expected value of 1.

Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. The structure member SlaveProp contains information about the corresponding slave device.

emNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a CoE mailbox write command was not set to the expected value of 1.

Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. The structure member SlaveProp contains information about the corresponding slave device.

emNotify - EC_NOTIFY_FOE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a FoE mailbox write command was not set to the expected value of 1.

emNotify - EC_NOTIFY_VOE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a VoE mailbox write command was not set to the expected value of 1.

Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. The structure member SlaveProp contains information about the corresponding slave device.

emNotify - EC_NOTIFY_S2SMBX_ERROR
*********************************

This error will be indicated in case a Slave-To-Slave mailbox transfer fails.

.. seealso:: :c:macro:`EC_E_S2SMBX_NOT_CONFIGURED`

emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR
*****************************************

This error will be indicated if the actually received Ethernet frame does not match to the frame expected or if a expected frame was not received.

This notification is enabled by default.

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation.

Missing response (timeout, :cpp:enumerator:`eRspErr_NO_RESPONSE`/ :cpp:enumerator:`eRspErr_FRAME_RETRY`) acyclic frames:
Acyclic Ethernet frames are internally queued by the master and sent to the slaves at a later time (usually after sending cyclic frames).
The master will monitor the time between queueing such a frame and receiving the result. If a maximum time is exceeded then this error will be indicated. This maximum time will be determined by the parameter dwEcatCmdTimeout when the master is initialized

.. seealso:: :cpp:func:`emInitMaster`

The master will retry sending the frame if the master configuration parameter dwEcatCmdMaxRetries is set to a value greater than 1. In case of a retry the :cpp:enumerator:`eRspErr_FRAME_RETRY` error is signalled, if the number of retries has elapsed the :cpp:enumerator:`eRspErr_NO_RESPONSE` error is signalled.

Possible reasons:

#. the frame was not received at all (due to bus problems)
    In this case the achErrorInfo member of the error notification descriptor will contain the string "L".

#. the frame was sent too late by the master due to a improper configuration.
    In this case the achErrorInfo member of the error notification descriptor will contain the string "T".

    To avoid this error the configuration may be changed as follows:

    -> higher value for master configuration parameter dwMaxAcycCmdsPerCycle
    -> shorter master timer cycle, i.e. shorter period between two calls to

    .. code-block:: cpp

        emExecJob(eUsrJob_MasterTimer)

    -> higher timeout value (master configuration parameter dwEcatCmdTimeout)

If the frame was sent too late by the master (due to improper configuration values) it will also be received too late and the master then signals an :cpp:enumerator:`eRspErr_WRONG_IDX` or :cpp:enumerator:`eRspErr_UNEXPECTED` error (as the master then doesn't expect to receive this frame).

Missing response (timeout, :cpp:enumerator:`eRspErr_NO_RESPONSE`) cyclic frames:

A response to all cyclic frames must occur until the next cycle starts. If the first cyclic frame is sent the master checks whether all cyclic frames of the last cycle were received. If there is one frame missing this error is indicated.

Possible reasons:

#. the frame was not received (due to bus problems)

#. too many or too long acyclic frames are sent in between sending cyclic frames by the master due to a improper configuration, to avoid these error notifications the configuration may be changed as follows:
    - lower value for master configuration parameter dwMaxAcycCmdsPerCycle
    - higher cyclic timer period, i.e. less calls to :cpp:func:`emExecJob` ( :cpp:enumerator:`eUsrJob_SendAllCycFrames`)

#. non-deterministic sending of acyclic frames.
    Sending acyclic frames by calling :cpp:func:`emExecJob` ( :cpp:enumerator:`eUsrJob_SendAcycFrames`) have to be properly scheduled with sending cyclic frames by calling :cpp:func:`emExecJob` ( :cpp:enumerator:`eUsrJob_SendAllCycFrames`).

Using the control interface :ref:`api:emIoControl - EC_IOCTL_SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK` it is possible to determine which response errors shall be signalled and which not.

Detailed error information is stored in structure :cpp:struct:`EC_T_FRAME_RSPERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_FRAME_RSPERR_DESC
    :members:

.. doxygenenum:: EC_T_FRAME_RSPERR_TYPE

emNotify - EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR
*************************************************

This error code will be indicated if a slave does not respond appropriately while sending slave init commands. The slave init commands are defined in the EtherCAT configuration (XML) file (Config/Slave/InitCmds/InitCmd). A timeout value for these commands may also be defined in the configuration file (Config/Slave/InitCmds/InitCmd/Timeout). If there is no timeout value defined here the frame response is expected within one single cycle.

This notification is enabled by default.

Detailed error information is stored in structure :cpp:struct:`EC_T_INITCMD_ERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_INITCMD_ERR_DESC
    :members:

.. doxygenenum:: EC_T_INITCMD_ERR_TYPE

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emNotify - EC_NOTIFY_MBSLAVE_INITCMD_TIMEOUT
********************************************

This error is identical to error code :ref:`api:emNotify - EC_NOTIFY_SLAVE_INITCMD_RESPONSE_ERROR` but it will be indicated in case of timeouts when processing mailbox init commands.

The timeout value used for CoE mailbox slaves is defined in the EtherCAT configuration (XML) file (Config/Slave/Mailbox/CoE/InitCmds/InitCmd/Timeout). In case this value is set to 0 a fixed timeout value of 500 msec will be used by the EtherCAT master. The timeout value used for EoE mailbox slaves will be set fixed to a value of 5000 msec.

emNotify - EC_NOTIFY_MASTER_INITCMD_RESPONSE_ERROR
**************************************************

This error code will be indicated if a missing or wrong command response was detected while sending master init commands. The master init commands are defined in the EtherCAT configuration (XML) file (Config/Master/InitCmds/InitCmd). A timeout value for these commands may also be defined in the configuration file (Config/Master/InitCmds/InitCmd/Timeout). If there is no timeout value defined here the frame response is expected within one single cycle.

Detailed error information is stored in structure :cpp:struct:`EC_T_INITCMD_ERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

emNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL
************************************************

When processing cyclic frames the EtherCAT master checks whether all slaves are still in OPERATIONAL state. If at least one slave device is not OPERATIONAL this error will be indicated.

emNotify - EC_NOTIFY_ALL_DEVICES_OPERATIONAL
********************************************

When processing cyclic frames the EtherCAT master checks whether all slaves are still in OPERATIONAL state. This will be notified after :ref:`api:emNotify - EC_NOTIFY_NOT_ALL_DEVICES_OPERATIONAL` and all the slaves are back in OPERATIONAL state.

emNotify - EC_NOTIFY_STATUS_SLAVE_ERROR
***************************************

When processing cyclic frames the EtherCAT master checks if at least one slave has the ERROR bit in the AL-STATUS register set. In that case this error will be indicated. The master will then automatically determine detailed error information of the slave(s) indicating an error and acknowledge the error status. The application will get a :ref:`api:emNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO` notification for each such slave. Usually those slaves will enter safe-operational state in this case. It is the application's response how to further handle such error cases.

This notification is enabled by default.

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO
********************************************

Every time the master detects a slave error, the Error bit on the specific slave is cleared and this error code will be signalled to the application. Detailed error information is stored in structure :cpp:struct:`EC_T_SLAVE_ERROR_INFO_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. This notification is enabled by default.

.. doxygenstruct:: EC_T_SLAVE_ERROR_INFO_DESC
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emNotify - EC_NOTIFY_SLAVES_ERROR_STATUS
****************************************

This notification collects notifications of type :ref:`api:emNotify - EC_NOTIFY_SLAVE_ERROR_STATUS_INFO`.
Notification is given on either collection full or master state changed whatever comes first.

This notification is disabled by default.

.. doxygenstruct:: EC_T_SLAVES_ERROR_DESC
    :members:

.. doxygenstruct:: EC_T_SLAVES_ERROR_DESC_ENTRY
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the activation

emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE
*******************************************

This error is signalized every time a slave changes into an unexpected state. Detailed error information is stored in structure :cpp:struct:`EC_T_SLAVE_UNEXPECTED_STATE_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`. This notification is enabled by default.

.. doxygenstruct:: EC_T_SLAVE_UNEXPECTED_STATE_DESC
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emNotify - EC_NOTIFY_SLAVES_UNEXPECTED_STATE
********************************************

This notification collects notifications of type :ref:`api:emNotify - EC_NOTIFY_SLAVE_UNEXPECTED_STATE`. Notification is given on either collection full or master state changed whatever comes first. This notification is disabled by default.

.. doxygenstruct:: EC_T_SLAVES_UNEXPECTED_STATE_DESC
    :members:

.. doxygenstruct:: EC_T_SLAVES_UNEXPECTED_STATE_DESC_ENTRY
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the activation

emNotify - EC_NOTIFY_ETH_LINK_NOT_CONNECTED
*******************************************

This notification will be indicated if the Ethernet link is disconnected. This error is never indicated if the Real-time Ethernet Driver does not support detection of a missing link cable.

In case of permanent frame loss no slaves can be found although the slaves are connected. This does not affect link connection detection therefore this notification will be not indicated on permanent frame loss.

emNotify - EC_NOTIFY_ETH_LINK_CONNECTED
***************************************

This notification will be indicated if the Ethernet link is reconnected after a disconnect. This notification is never indicated if the Real-time Ethernet Driver does not support detection of a missing link cable.

emNotify - EC_NOTIFY_CLIENTREGISTRATION_DROPPED
***********************************************

This notification will be indicated if the client registration was dropped because :cpp:func:`emConfigureNetwork` was called by another thread. The notification has the following parameter:

.. code-block:: cpp

    EC_T_DWORD dwDeinitForConfiguration; /* 0 = terminating Master, 1 = restarting Master */

emNotify - EC_NOTIFY_EEPROM_CHECKSUM_ERROR
******************************************

This error is signalized every time a EEPROM checksum error is detected.

Detailed error information is stored in structure :cpp:struct:`EC_T_EEPROM_CHECKSUM_ERROR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_EEPROM_CHECKSUM_ERROR_DESC
    :members:

emNotify - EC_NOTIFY_MBXRCV_INVALID_DATA
****************************************

This error is signalized when invalid mailbox data have been received from slave. Detailed error information is stored in structure :cpp:struct:`EC_T_MBXRCV_INVALID_DATA_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_MBXRCV_INVALID_DATA_DESC
    :members:

emNotify - EC_NOTIFY_PDIWATCHDOG
********************************

This error is signalized every time a PDI watchdog error is detected. Detailed error information is stored in structure :cpp:struct:`EC_T_PDIWATCHDOG_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_PDIWATCHDOG_DESC
    :members:

ecatGetText
***********

.. doxygenfunction:: ecatGetText

emLogFrameEnable
****************

.. doxygenfunction:: ecatLogFrameEnable
    :outline:

.. doxygenfunction:: emLogFrameEnable

.. doxygentypedef:: EC_T_PFLOGFRAME_CB

.. datatemplate:xml:: EC_LOG_FRAME_FLAGS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. code-block:: cpp

    /********************************************************************************/
    /** \brief  Handler to log frames.
    *
    *   CAUTION: Called by cyclic task!!! Do not consume to much CPU time!!!
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

emLogFrameDisable
*****************

.. doxygenfunction:: ecatLogFrameDisable
    :outline:

.. doxygenfunction:: emLogFrameDisable

emGetMasterInfo
***************

.. doxygenfunction:: ecatGetMasterInfo
    :outline:

.. doxygenfunction:: emGetMasterInfo

.. doxygenstruct:: EC_T_MASTER_INFO
    :members:

.. doxygenstruct:: EC_T_BUS_DIAGNOSIS_INFO
    :members:

.. doxygenstruct:: EC_T_MAILBOX_STATISTICS
    :members:

.. doxygenstruct:: EC_T_STATISTIC_TRANSFER_DUPLEX
    :members:

.. doxygenstruct:: EC_T_STATISTIC_TRANSFER
    :members:

.. doxygenstruct:: EC_T_STATISTIC
    :members:

.. dropdown:: **emGetMasterInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterInfoExample
        :end-before: DocumentationSnippetsGetMasterInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetMemoryUsage
****************

.. doxygenfunction:: ecatGetMemoryUsage
    :outline:

.. doxygenfunction:: emGetMemoryUsage

.. dropdown:: **emGetMemoryUsage() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMemoryUsageExample
        :end-before: DocumentationSnippetsGetMemoryUsageExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emGetMasterDump
***************

.. doxygenfunction:: ecatGetMasterDump
    :outline:

.. doxygenfunction:: emGetMasterDump

.. dropdown:: **emGetMasterDump() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterDumpExample
        :end-before: DocumentationSnippetsGetMasterDumpExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emGetMasterSyncUnitInfoNumOf
****************************

.. doxygenfunction:: ecatGetMasterSyncUnitInfoNumOf
    :outline:

.. doxygenfunction:: emGetMasterSyncUnitInfoNumOf

.. dropdown:: **emGetMasterSyncUnitInfoNumOf() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterSyncUnitInfoNumOfExample
        :end-before: DocumentationSnippetsGetMasterSyncUnitInfoNumOfExample
        :language: cpp
        :dedent: 4
        :lines: 1-


emGetMasterSyncUnitInfo
***********************

.. doxygenfunction:: ecatGetMasterSyncUnitInfo
    :outline:

.. doxygenfunction:: emGetMasterSyncUnitInfo

:c:macro:`MSU_ID_ALL_INFO_ENTRIES` retrieves the information from all master sync units at once. The application must ensure that pMsuInfo is capable for all entries.

.. doxygenstruct:: EC_T_MSU_INFO
    :members:

.. dropdown:: **emGetMasterSyncUnitInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsGetMasterSyncUnitInfoExample
        :end-before: DocumentationSnippetsGetMasterSyncUnitInfoExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emGetMasterSyncUnitInfoNumOf`

emBadConnectionsDetect
**********************

.. doxygenfunction:: ecatBadConnectionsDetect
    :outline:

.. doxygenfunction:: emBadConnectionsDetect

.. dropdown:: **emBadConnectionsDetect() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsBadConnectionsDetectExample
        :end-before: DocumentationSnippetsBadConnectionsDetectExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emBadConnectionsReset`

emBadConnectionsReset
*********************

.. doxygenfunction:: ecatBadConnectionsReset
    :outline:

.. doxygenfunction:: emBadConnectionsReset

.. dropdown:: **emBadConnectionsReset() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsBadConnectionsResetExample
        :end-before: DocumentationSnippetsBadConnectionsResetExample
        :language: cpp
        :dedent: 4
        :lines: 1-

emNotify - EC_NOTIFY_BAD_CONNECTION
***********************************

This error is signalized every time a bad connection is detected within the call of :cpp:func:`emBadConnectionsDetect`. It contains the exact location of the bad connection between two slaves. This notification is enabled by default.

.. doxygenstruct:: EC_T_BAD_CONNECTION_NTFY_DESC
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED` for how to control the deactivation

emSelfTestScan
**************

.. doxygenfunction:: ecatSelfTestScan
    :outline:

.. doxygenfunction:: emSelfTestScan

.. doxygenstruct:: EC_T_SELFTESTSCAN_PARMS
    :members:

.. dropdown:: **emSelfTestScan() Example**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\api.h
        :start-after: DocumentationSnippetsSelfTestScanExample
        :end-before: DocumentationSnippetsSelfTestScanExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emBadConnectionsDetect`
