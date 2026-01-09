*********************
Operation without ENI
*********************

The |Product| can operate on a reduced feature set without an ENI file. This is particularly useful in cases where an ENI file is unavailable or inaccessible. To operate the |Product| in this mode, configure the network using the :command:`eCnfType_GenEBI` configuration type.

In this mode, the |Product| is able to observe basic information on the bus such as the network topology, slave descriptions and registers. The application can retrieve this information using :ref:`api_slave:emonGetBusSlaveInfo` and :ref:`api_slave:emonReadSlaveRegister` respectively. Because the |Product| does not store or access |ECAT| Slave Information (ESI) files, it does not have a process data image, and APIs which depend on configuration data will be limited or non-functional.

The |Product| supports exporting an ENI Builder (\*.ebi) configuration file. This file contains the observed network topology and slave descriptions and can be imported in the acontis EC-Engineer, which can export an ENI file in turn. This ENI file can then be used to operate the |Product| on its full feature set.

.. seealso::
    - :ref:`api_general:emonConfigureNetwork`
    - :ref:`api_general:emonExportEniBuilderConfig`