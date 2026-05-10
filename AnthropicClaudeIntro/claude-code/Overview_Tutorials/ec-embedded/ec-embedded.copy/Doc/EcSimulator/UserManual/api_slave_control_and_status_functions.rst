Slave control and status functions
**********************************

esGetNumConfiguredSlaves
========================

.. doxygenfunction:: esGetNumConfiguredSlaves

esGetNumConnectedSlaves
=======================

.. doxygenfunction:: esGetNumConnectedSlaves

esGetSlaveId
============

.. doxygenfunction:: esGetSlaveId

.. dropdown:: Example

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_slave_control_and_status_functions.h
        :start-after: DocumentationSnippetsEsGetSlaveId
        :end-before: DocumentationSnippetsEsGetSlaveId
        :language: cpp

esGetSlaveIdAtPosition
======================

.. doxygenfunction:: esGetSlaveIdAtPosition

.. dropdown:: Example

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_slave_control_and_status_functions.h
        :start-after: DocumentationSnippetsEsGetSlaveIdAtPosition
        :end-before: DocumentationSnippetsEsGetSlaveIdAtPosition
        :language: cpp

esGetSlaveState
===============

.. doxygenfunction:: esGetSlaveState

esSetSlaveState
===============

.. doxygenfunction:: esSetSlaveState

esIsSlavePresent
================

.. doxygenfunction:: esIsSlavePresent

esGetSlaveProp
==============

.. doxygenfunction:: esGetSlaveProp

esGetSlavePortState
===================

.. doxygenfunction:: esGetSlavePortState

esGetSlaveInpVarInfoNumOf
=========================

.. doxygenfunction:: esGetSlaveInpVarInfoNumOf

esGetSlaveOutpVarInfoNumOf
==========================

.. doxygenfunction:: esGetSlaveOutpVarInfoNumOf

esGetSlaveInpVarInfo
====================

.. doxygenfunction:: esGetSlaveInpVarInfo

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO
    :members:
    
.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN
    
esGetSlaveInpVarInfoEx
======================

.. doxygenfunction:: esGetSlaveInpVarInfoEx

.. doxygenstruct:: EC_T_PROCESS_VAR_INFO_EX
    :members:
    
.. doxygendefine:: MAX_PROCESS_VAR_NAME_LEN_EX
    
esGetSlaveOutpVarInfo
=====================

.. doxygenfunction:: esGetSlaveOutpVarInfo

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

esGetSlaveOutpVarInfoEx
=======================

.. doxygenfunction:: esGetSlaveOutpVarInfoEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

esGetSlaveInpVarByObjectEx
==========================

.. doxygenfunction:: esGetSlaveInpVarByObjectEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

esGetSlaveOutpVarByObjectEx
===========================

.. doxygenfunction:: esGetSlaveOutpVarByObjectEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

esFindInpVarByName
==================

.. doxygenfunction:: esFindInpVarByName

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

esFindInpVarByNameEx
====================
.. doxygenfunction:: esFindInpVarByNameEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

esFindOutpVarByName
===================

.. doxygenfunction:: esFindOutpVarByName

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

esFindOutpVarByNameEx
=====================

.. doxygenfunction:: esFindOutpVarByNameEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`
    
esWriteSlaveRegister
====================

.. warning:: Changing contents of ESC registers may lead to unpredictiable behavior of the slaves and/or the master.

.. doxygenfunction:: esWriteSlaveRegister

esReadSlaveRegister
===================

.. doxygenfunction:: esReadSlaveRegister

esReadSlaveEEPRom
=================

.. doxygenfunction:: esReadSlaveEEPRom

esWriteSlaveEEPRom
==================

.. doxygenfunction:: esWriteSlaveEEPRom

.. note:: The EEPROM's CRC at word 7 is re-calculated automatically if the written data is completely within the ESC Configuration Area in the EEPROM's SII.

esGetSimSlaveInfo
=================

.. doxygenfunction:: esGetSimSlaveInfo

Content of :cpp:struct:`EC_T_SIM_SLAVE_INFO`, :cpp:struct:`EC_T_SIM_SLAVE_CFG_INFO`, :cpp:struct:`EC_T_SIM_SLAVE_STATUS_INFO` is subject to be extended.

.. doxygenstruct:: EC_T_SIM_SLAVE_INFO
    :members:

.. doxygenstruct:: EC_T_SIM_SLAVE_CFG_INFO
    :members:

.. doxygenstruct:: EC_T_SIM_SLAVE_STATUS_INFO
    :members:

esGetBusSlaveInfo
=================

.. doxygenfunction:: esGetBusSlaveInfo

Content of :cpp:struct:`EC_T_BUS_SLAVE_INFO` is subject to be extended.

.. doxygenstruct:: EC_T_BUS_SLAVE_INFO
    :members:
    
.. dropdown:: Get bus slave info with station address example

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_slave_control_and_status_functions.h
        :start-after: DocumentationSnippetsEsGetBusSlaveInfoWithStationAddress
        :end-before: DocumentationSnippetsEsGetBusSlaveInfoWithStationAddress
        :language: cpp

.. dropdown:: Get bus slave info with auto-inc address example

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_slave_control_and_status_functions.h
        :start-after: DocumentationSnippetsEsGetBusSlaveInfoWithAutoIncAddress
        :end-before: DocumentationSnippetsEsGetBusSlaveInfoWithAutoIncAddress
        :language: cpp

esReadSlaveIdentification
=========================

.. doxygenfunction:: esReadSlaveIdentification

esGetSlaveStatistics
====================

.. doxygenfunction:: esGetSlaveStatistics

esClearSlaveStatistics
======================

.. doxygenfunction:: esClearSlaveStatistics
