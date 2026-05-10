Error simulation functions
**************************

esSetErrorAtSlavePort
=====================

.. doxygenfunction:: esSetErrorAtSlavePort

esSetErrorGenerationAtSlavePort
===============================

.. doxygenfunction:: esSetErrorGenerationAtSlavePort

esResetErrorGenerationAtSlavePorts
==================================

.. doxygenfunction:: esResetErrorGenerationAtSlavePorts

esSetLinkDownAtSlavePort
========================

.. doxygenfunction:: esSetLinkDownAtSlavePort

esSetLinkDownGenerationAtSlavePort
==================================

.. doxygenfunction:: esSetLinkDownGenerationAtSlavePort

esResetLinkDownGenerationAtSlavePorts
=====================================

.. doxygenfunction:: esResetLinkDownGenerationAtSlavePorts

esLogFrameEnableAtSlavePort
===========================

.. doxygenfunction:: esLogFrameEnableAtSlavePort

esLogFrameDisableAtSlavePort
============================

.. doxygenfunction:: esLogFrameDisableAtSlavePort

esSendSlaveCoeEmergency
=======================

.. doxygenfunction:: esSendSlaveCoeEmergency

.. dropdown:: **CoE Emergency Example**

    The following code demonstrates how to send a CoE Emergency from a local buffer to the Master.

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :start-after: DocumentationSnippetsCoeEmergencyExample
        :end-before: DocumentationSnippetsCoeEmergencyExample
        :language: cpp

esSetSimSlaveState
==================

.. doxygenfunction:: esSetSimSlaveState

.. dropdown:: **Simulate AL Status Error Example**

    The following code demonstrates how to simulate AL Status Errors for slaves without device emulation:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :start-after: DocumentationSnippetsSimulateSlaveErrorAlStatusCodeExample
        :end-before: DocumentationSnippetsSimulateSlaveErrorAlStatusCodeExample
        :language: cpp
        :dedent: 8

.. dropdown:: **Simulate AL Status Delay Example**

    The following code demonstrates how to simulate the EtherCAT state transition being delayed for some cycles by the slave application.

    :cpp:func:`APPL_StartMailboxHandlerCallback_DelayALStatus` starts the EtherCAT state transition delay and
    :cpp:func:`APPL_ApplicationCallback_DelayALStatus` stops the EtherCAT state transition delay:

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :start-after: DocumentationSnippetsDelaySimSlaveAlStatusCallbacks
        :end-before: DocumentationSnippetsDelaySimSlaveAlStatusCallbacks
        :language: cpp
        :dedent: 4

    S_oAlStatusDelayTimer simulates the delay until the slave application is ready.

    .. note:: If the delay is too long, the transition to PREOP will fail in EcSimulatorSilDemo due to InitCmd timeouts from the ENI file and checks within the SSC:

    The callbacks must be registered using :cpp:func:`esSetSlaveSscApplication`, e.g. in :cpp:func:`myAppPrepare` of EcSimulatorHilDemo / EcSimulatorSilDemo: 

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :start-after: DocumentationSnippetsDelaySimSlaveAlStatusMyAppPrepare
        :end-before: DocumentationSnippetsDelaySimSlaveAlStatusMyAppPrepare
        :language: cpp
        :dedent: 12

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :start-after: DocumentationSnippetsDelaySimSlaveAlStatusExample
        :end-before: DocumentationSnippetsDelaySimSlaveAlStatusExample
        :language: cpp
        :dedent: 12

.. seealso:: 
    - :cpp:func:`esSetSlaveSscApplication`: :cpp:member:`EC_T_SLAVE_SSC_APPL_DESC::pfnAckErrorInd`
