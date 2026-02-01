*******
Logging
*******

The |Product| offers a logging interface for a more detailed analysis of application errors, problems in the EtherCAT® network and for diagnosing internal processes.
The log messages are passed from the |Product| to the application via the callback :cpp:member:`EC_T_LOG_PARMS::pfLogMsg` given at :cpp:member:`EC_T_MONITOR_INIT_PARMS::LogParms`. 

.. cpp:alias:: EC_PF_LOGMSGHK 

The level of detail of the logging output can be set via :cpp:member:`EC_T_LOG_PARMS::dwLogLevel`. The log levels are firmly defined:

.. datatemplate:xml:: EC_LOG_LEVELS
    :source: ../_build/doxygen/xml/combined.xml
    :template: hlist-doxygroups.jinja

For performance reasons, the log messages are automatically filtered based on the log level and then passed to the callback.

**Example**

The ``EcMonitorDemo`` examples demonstrate how log messages can be processed by the application, see :file:`Examples/Common/EcLogging.cpp`.
The messages processed by ``EcLogging.cpp`` are of different types, e.g. |Product| log messages and application messages are logged to the console and/or files.
Identical messages are skipped automatically by default.

.. note:: With some operating systems, logging in files is deactivated, e.g. because a file system is not available.

The verbosity of the ``EcMonitorDemo`` is specified as a ``-v`` command line parameter. It is used to determine the log level of the application, see :file:`EcDemoMain.cpp`.
``EcLogging.cpp`` has various parameters beside the log level, like Roll Over setting, log task priority, CPU affinity, log buffer size and etc.