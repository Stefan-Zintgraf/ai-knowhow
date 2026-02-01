**********************
Slave status functions
**********************

emonGetNumConfiguredSlaves
**************************

.. doxygenfunction:: emonGetNumConfiguredSlaves

emonGetNumConnectedSlaves
*************************

.. doxygenfunction:: emonGetNumConnectedSlaves

emonGetSlaveId
**************

.. doxygenfunction:: emonGetSlaveId

emonGetSlaveIdAtPosition
************************

.. doxygenfunction:: emonGetSlaveIdAtPosition

emonGetSlaveState
*****************

.. doxygenfunction:: emonGetSlaveState

.. admonition:: Limitation
    :class: admonition hint

    Since it is not possible to determine the actual requested slave state from the master, the highest slave state of all slaves is assumed to be the requested state.

.. seealso:: 
    
    - :cpp:func:`emonGetSlaveId`
    - :ref:`notification:emonNotify - EC_NOTIFY_SLAVE_STATECHANGED`

emonIsSlavePresent
******************

.. doxygenfunction:: emonIsSlavePresent

.. seealso:: 
    
    - :cpp:func:`emonGetSlaveId`
    - :ref:`notification:emonNotify - EC_NOTIFY_SLAVE_PRESENCE`

emonGetSlaveProp
****************

.. doxygenfunction:: emonGetSlaveProp

.. doxygenstruct:: EC_T_SLAVE_PROP
    :members:

.. seealso:: :cpp:func:`emonGetSlaveId`

emonGetSlaveInpVarInfoNumOf
***************************

.. doxygenfunction:: emonGetSlaveInpVarInfoNumOf

.. seealso:: 
    - :cpp:func:`emonGetSlaveInpVarInfo`
    - :cpp:func:`emonGetSlaveInpVarInfoEx`

emonGetSlaveInpVarInfo
**********************

.. doxygenfunction:: emonGetSlaveInpVarInfo

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO
    :members:
    
.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN
    
emonGetSlaveInpVarInfoEx
************************

.. doxygenfunction:: emonGetSlaveInpVarInfoEx

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO_EX
    :members:
    
.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN_EX

emonGetSlaveOutpVarInfoNumOf
****************************

.. doxygenfunction:: emonGetSlaveOutpVarInfoNumOf

.. seealso:: 
    - :cpp:func:`emonGetSlaveOutpVarInfo`
    - :cpp:func:`emonGetSlaveOutpVarInfoEx`

emonGetSlaveOutpVarInfo
***********************

.. doxygenfunction:: emonGetSlaveOutpVarInfo

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

emonGetSlaveOutpVarInfoEx
*************************

.. doxygenfunction:: emonGetSlaveOutpVarInfoEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emonGetSlaveInpVarByObjectEx
****************************

.. doxygenfunction:: emonGetSlaveInpVarByObjectEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emonGetSlaveOutpVarByObjectEx
*****************************

.. doxygenfunction:: emonGetSlaveOutpVarByObjectEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emonReadSlaveRegister
*********************

.. doxygenfunction:: emonReadSlaveRegister

emonGetCfgSlaveInfo
*******************

.. doxygenfunction:: emonGetCfgSlaveInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_INFO
    :members:

**Flags EC_MBX_PROTOCOL_**

.. datatemplate:xml:: EC_MBX_PROTOCOLS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

emonGetCfgSlaveSmInfo
*********************

.. doxygenfunction:: emonGetCfgSlaveSmInfo

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_ENTRY
    :members:

.. doxygenstruct:: EC_T_CFG_SLAVE_SM_INFO
    :members:

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, emonGetCfgSlaveSmInfo)
        :end-before: IGNORE_TEST(DocumentationSnippets, emonGetCfgSlaveSmInfo)
        :dedent: 4
        :lines: 2-

emonGetBusSlaveInfo
*******************

.. doxygenfunction:: emonGetBusSlaveInfo

.. doxygenstruct:: EC_T_BUS_SLAVE_INFO
    :members:

**Port Slave ID's**

.. datatemplate:xml:: EC_SLAVE_IDS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

**Flags EC_LINECROSSED_**

.. datatemplate:xml:: EC_LINECROSSED_FLAGS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

