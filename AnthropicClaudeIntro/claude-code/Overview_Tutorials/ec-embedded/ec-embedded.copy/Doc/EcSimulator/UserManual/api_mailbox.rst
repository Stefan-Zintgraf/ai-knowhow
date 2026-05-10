ADS over EtherCAT (AoE)
***********************

To handle AoE object transfers within the application, the callbacks pfnAoeRead, pfnAoeWrite and/or pfnAoeReadWrite can be registered using :cpp:func:`esSetSlaveAoeObjectTransferCallbacks` or :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo. 

See also :ref:`api_mailbox:AoE Simulator and Master Example`

esAoeGetSlaveNetId
==================

.. doxygenfunction:: esAoeGetSlaveNetId

esAoeRead
=========

.. doxygenfunction:: esAoeRead

esAoeWrite
==========

.. doxygenfunction:: esAoeWrite

esAoeReadWrite
==============

.. doxygenfunction:: esAoeReadWrite

esSetSlaveAoeObjectTransferCallbacks
====================================

.. doxygenfunction:: esSetSlaveAoeObjectTransferCallbacks

AoE Simulator and Master Example
================================

The following example demonstrates how to handle AoE object transfers within the simulator application:

.. dropdown:: **AoE Simulator and Master Example**

    The following example handlers can be registered at the EC-Simulator:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleCallbacks
        :end-before: DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleCallbacks
        :language: cpp

    The following example demonstrates objects transfers between Master and Simulator:
    
    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleTransfer
        :end-before: DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleTransfer
        :language: cpp

CAN application protocol over EtherCAT (CoE)
********************************************

To handle CoE object transfers within the application, the callbacks pfnCoeRead and/or pfnCoeWrite can be registered using :cpp:func:`esSetSlaveCoeObjectTransferCallbacks` or :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo. 

See also :ref:`api_mailbox:CoE transfer Simulator and Master Example`

esExtendSlaveCoeObjectDictionary
================================

.. doxygenfunction:: esExtendSlaveCoeObjectDictionary

esDeleteSlaveCoeObject
======================

.. doxygenfunction:: esDeleteSlaveCoeObject

esClearSlaveCoeObjectDictionary
===============================

.. doxygenfunction:: esClearSlaveCoeObjectDictionary

esResetSlaveCoeObjectDictionary
===============================

.. doxygenfunction:: esResetSlaveCoeObjectDictionary

esSetSlaveCoeObjectTransferCallbacks
====================================

.. doxygenfunction:: esSetSlaveCoeObjectTransferCallbacks

.. seealso::
    - :cpp:func:`esSetSlaveSscApplication`
    - :cpp:func:`esClearSlaveCoeObjectDictionary`

.. doxygentypedef:: EC_T_PF_COE_READ_CB

.. doxygentypedef:: EC_T_PF_COE_WRITE_CB

esCoeSdoDownload
================

.. doxygenfunction:: esCoeSdoDownload

esCoeSdoUpload
==============

.. doxygenfunction:: esCoeSdoUpload

esCoeGetODListReq
=================

.. doxygenfunction:: esCoeGetODListReq

esCoeGetObjectDescReq
=====================

.. doxygenfunction:: esCoeGetObjectDescReq

.. doxygenstruct:: EC_T_COE_OBDESC
    :members:
    
esCoeGetEntryDescReq
====================

.. doxygenfunction:: esCoeGetEntryDescReq

.. doxygenstruct:: EC_T_COE_ENTRYDESC
    :members:
    
See szUnitType, szDefaultValue, szMinValue, szMaxValue, szDescription in CoeReadObjectDictionary() in EcSdoServices.cpp as an example for evaluating EC_T_COE_ENTRYDESC.pbyData.

CoE transfer Simulator and Master Example
=========================================

The following example demonstrates how to handle CoE object transfers within the simulator application:

.. dropdown:: **CoE transfer Simulator and Master Example**

    The following example handlers can be registered at the EC-Simulator:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleCallbacks
        :end-before: DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleCallbacks
        :language: cpp

    The following example demonstrates objects transfers between Master and Simulator:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleTransfer
        :end-before: DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleTransfer
        :language: cpp

Ethernet over EtherCAT (EoE)
****************************

To handle EoE frames within the application, the callback pfnEoeReceive must be registered using :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo. 

See also :ref:`api_mailbox:EoE Ping Example`

esEoeSendFrame
==============

.. doxygenfunction:: esEoeSendFrame

esGetCfgSlaveEoeInfo
====================

.. doxygenfunction:: esGetCfgSlaveEoeInfo

.. raw:: latex

    \newpage

Content of :cpp:struct:`EC_T_CFG_SLAVE_EOE_INFO` is subject to be extended.

.. doxygenstruct:: EC_T_CFG_SLAVE_EOE_INFO
    :members:

.. raw:: latex

    \newpage

.. dropdown:: **esGetCfgSlaveEoeInfo() Example**

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorGetCfgSlaveEoeInfoExample
        :end-before: DocumentationSnippetsSimulatorGetCfgSlaveEoeInfoExample
        :language: cpp

.. raw:: latex

    \newpage

EoE Ping Example
================

The following example demonstrates how to customize EoE simulation using :cpp:func:`esSetSlaveSscApplication` and :cpp:func:`esEoeSendFrame`.

.. dropdown:: **EoE Ping Example**

    The following code demonstrates how to receive EoE frames from the Master and send answers back.

    .. literalinclude:: ..\..\..\Examples\Common\EcSimulatorMbx.h
        :start-after: EoePingExample
        :end-before: EoePingExample
        :language: cpp

    The callbacks need a context. Each slave needs its individual context. If there is only one slave to be registered, a global context can be declared and used:
    
    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsEoeExampleContext
        :end-before: DocumentationSnippetsEoeExampleContext
        :language: cpp

    The callbacks must be registered using :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo: 

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsEoeExampleRegisterCallbacks
        :end-before: DocumentationSnippetsEoeExampleRegisterCallbacks
        :language: cpp

.. raw:: latex

    \newpage

File access over EtherCAT (FoE)
*******************************

The following examples demonstrate how to customize FoE simulation using :cpp:func:`esSetSlaveSscApplication` .

.. dropdown:: **FoE Download Example**

    The following code demonstrates how to receive FoE from the Master and store it in a buffer.
    The data received in this example is stored in :cpp:member:`T_MY_CONTEXT::abyFileBuf` :

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeTransferExampleContextType
        :end-before: DocumentationSnippetsFoeTransferExampleContextType
        :language: cpp

    The callback :cpp:func:`myAppFoeWrite` handles download requests from the Master, :cpp:func:`myAppFoeWriteData` copies the FoE payload from the mailbox to :cpp:member:`T_MY_CONTEXT::abyFileBuf` :

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeDownloadExampleCallbacks
        :end-before: DocumentationSnippetsFoeDownloadExampleCallbacks
        :language: cpp

    See type :cpp:type:`EC_PF_SSC_APPL_FOE_WRITE` .

    The callbacks must be registered using :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo: 

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeDownloadExampleSimulatorMyAppPrepare
        :end-before: DocumentationSnippetsFoeDownloadExampleSimulatorMyAppPrepare
        :language: cpp
        :dedent: 4


    The following code at Master downloads the file to the slave:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeDownloadExampleMaster
        :end-before: DocumentationSnippetsFoeDownloadExampleMaster
        :language: cpp
        :dedent: 4

.. raw:: latex

    \newpage

.. dropdown:: **FoE Upload Example**

    The following code demonstrates how to serve FoE data from a local buffer to the Master.
    The data served in this example is stored in :cpp:member:`T_MY_CONTEXT::abyFileBuf` :

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeTransferExampleContextType
        :end-before: DocumentationSnippetsFoeTransferExampleContextType
        :language: cpp

    :cpp:func:`myAppFoeRead` handles upload requests from the Master, :cpp:func:`myAppFoeReadData` copies the FoE payload from :cpp:member:`T_MY_CONTEXT::abyFileBuf` to the mailbox:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeUploadExampleCallbacks
        :end-before: DocumentationSnippetsFoeUploadExampleCallbacks
        :language: cpp

    The callbacks must be registered using :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo: 

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeUploadExampleSimulatorMyAppPrepare
        :end-before: DocumentationSnippetsFoeUploadExampleSimulatorMyAppPrepare
        :language: cpp
        :dedent: 4

    The following code at Master uploads the file from the slave:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsFoeUploadExampleMaster
        :end-before: DocumentationSnippetsFoeUploadExampleMaster
        :language: cpp
        :dedent: 4
    
.. seealso::
    - :cpp:func:`esInitSimulator`
    - :cpp:func:`esConfigureNetwork`

.. raw:: latex

    \newpage

Vendor specific access over EtherCAT (VoE)
******************************************

See also :ref:`api_mailbox:VoE Receive Example`

esVoeSend
=========

.. doxygenfunction:: esVoeSend

esSetVoeReceiveCallback
=======================

.. doxygenfunction:: esSetVoeReceiveCallback

VoE Receive Example
===================

The following examples demonstrate how to register a handler for VoE writes from the Master or from other slaves.

.. dropdown:: **VoE Receive Example**

    The following code demonstrates how to send VoE from the Master to the slave and store it in a buffer at the Simulator.
    The data received in this example is stored in :cpp:member:`T_MY_CONTEXT::abyVoeBuf` :

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleContextType
        :end-before: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleContextType
        :language: cpp

    :cpp:func:`myAppVoeReceiveCallback` handles write requests from the Master and copies the received VoE payload from the mailbox to :cpp:member:`T_MY_CONTEXT::abyVoeBuf` :

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleHandler
        :end-before: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleHandler
        :language: cpp

    The following code shows how to register :cpp:func:`myAppVoeReceiveCallback` and send VoE from the Master to the simulated slave:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_mailbox.h
        :start-after: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleTransfer
        :end-before: DocumentationSnippetsSimulatorVoeReceiveCallbackExampleTransfer
        :language: cpp
