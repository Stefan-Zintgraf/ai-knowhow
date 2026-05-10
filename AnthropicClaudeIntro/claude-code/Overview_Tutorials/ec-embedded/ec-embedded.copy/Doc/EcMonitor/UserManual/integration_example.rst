*******************
Example application
*******************

The example application will handle the following tasks:

- EC-Monitor initialization
- Process Data acquisition with EC-DAQ
- Periodic Job Task in polling or interrupt mode
- Thread with periodic tasks and application thread already implemented
- Record and replay wireshark traces
- Logging. The output messages of the demo application will be printed on the console as well as in some files.
- "Out of the box" solution for different operating systems: Windows, Linux ...   

File reference
**************

The EcMonitorDemo application consists of the following files:

.. figure:: ../Media/EcMonitorDemoFileOverview.png
    :align:     center
    :alt:   

+-----------------------+-------------------------------------------------------+
| EcDemoMain.cpp        | Entry point for the different operating               |
|                       | systems                                               |
+-----------------------+-------------------------------------------------------+
| EcDemoPlatform.h      | Operating system specific settings (task              |
|                       | priorities, timer settings)                           |
+-----------------------+-------------------------------------------------------+
| EcDemoApp.cpp         | Initialize, start and terminate EC-Monitor            |
+-----------------------+-------------------------------------------------------+
| EcDemoApp.h           | Application specific settings for EcDemoApp           |
+-----------------------+-------------------------------------------------------+
| EcDemoParms.cpp       | Parsing of command line parameters                    |
+-----------------------+-------------------------------------------------------+
| EcDemoParms.h         | Basic configuration parameters                        |
+-----------------------+-------------------------------------------------------+
| EcSelectLinkLayer.cpp | Common Functions which abstract the command           |
|                       | line parsing into Real-time Ethernet Driver parameter |
+-----------------------+-------------------------------------------------------+
| EcNotification.cpp    | Slave monitoring and error detection                  |
|                       | (function :cpp:func:`ecatNotify` )                    |
+-----------------------+-------------------------------------------------------+
| EcSlaveInfo.cpp       | Slave information services                            |
+-----------------------+-------------------------------------------------------+
| EcLogging.cpp         | Message logging functions                             |
+-----------------------+-------------------------------------------------------+
| EcTimer.cpp           | Start and monitor timeouts                            |
+-----------------------+-------------------------------------------------------+


|Product| life cycle
********************

Basically the operation of the |Product| is wrapped between the functions

- :cpp:func:`emonInitMonitor`
- :cpp:func:`emonConfigureNetwork`

and

- :cpp:func:`emonDeinitMonitor`


The |Product| is made ready for operation and started with the first two functions mentioned. During this preparation, a thread is set up and started that handles all the cyclic tasks of the |Product|.
The last function stops the |Product| and clears the memory.

An overview of the complete life cycle as a sequence diagram:

.. uml::

    skinparam monochrome true
    skinparam SequenceMessageAlign direction
    hide footbox

    participant EcDemoMain
    participant EcDemoApp
    participant EcEmbedded as "EC-Monitor"
    participant JobTask as "EcMonitorJobTask"
    participant EcTimingTask

    activate EcDemoMain
    EcDemoMain->EcDemoMain : PrepareCommandLine()
    EcDemoMain->EcDemoMain : SetAppParmsFromCommandLine()
    EcDemoMain->EcDemoMain : InitLogging()
    EcDemoMain->EcTimingTask : CreateTimingTask(pvJobTaskEvent)
    activate EcTimingTask
    EcDemoMain->EcDemoApp : EcDemoApp()

    activate EcDemoApp
    EcDemoApp->EcDemoApp : InitNotificationHandler()
    EcDemoApp->EcEmbedded : emonInitMonitor()
    activate EcEmbedded
    EcDemoApp<--EcEmbedded
    EcDemoApp->EcEmbedded : emonConfigureNetwork()
    EcDemoApp<--EcEmbedded

    EcDemoApp->JobTask : CreateJobTask()
    activate JobTask

    par
        loop
            EcTimingTask->EcTimingTask : sleep()
            EcTimingTask->JobTask : OsSetEvent(pvJobTaskEvent)
            activate JobTask
        end
    else
        JobTask->EcEmbedded : emonExecJob(ProcessAllRxFrames)
        JobTask<--EcEmbedded
        JobTask->JobTask : myAppWorkPd()
        JobTask->EcEmbedded : emonExecJob(MonitorTimer)
        JobTask<--EcEmbedded
        deactivate JobTask
    else
        EcDemoApp->EcEmbedded : emonRasSrvStart()
        EcDemoApp<--EcEmbedded
        EcDemoApp->EcEmbedded : emonRegisterClient()
        EcDemoApp<--EcEmbedded
        EcDemoApp->EcDemoApp : idle()
        EcDemoApp->JobTask : shutdownJobTask()
        deactivate JobTask
    end

    EcDemoApp->EcEmbedded : emonUnregisterClient()
    EcDemoApp<--EcEmbedded
    EcDemoApp->EcEmbedded : emonRasSrvStop()
    EcDemoApp<--EcEmbedded
    EcDemoApp->EcEmbedded : emonDeinitMonitor()
    EcDemoApp<--EcEmbedded
    deactivate EcEmbedded

    EcDemoMain<--EcDemoApp
    deactivate EcDemoApp
    EcDemoMain->EcTimingTask : shutdownTimingTask()
    deactivate EcTimingTask
    EcDemoMain->EcDemoMain : DeinitLogging()

A more detailed description of the functions:

EcDemoMain()
    A wrapper to start the demo from the respective operating system.
    In addition to initializing the operating system, parsing command line parameters and initializing logging it also starts the timing task.

EcDemoApp()
    Demo application. The function takes care of starting and stopping the |Product| and all related tasks. In between, the function runs idle, while all relevant work is done by the EcMonitorJobTask().

EcMonitorJobTask()
    Thread that does the necessary periodic work. Very important here is myAppWorkPd() between :cpp:enumerator:`eUsrJob_ProcessAllRxFrames` and :cpp:enumerator:`eUsrJob_MonitorTimer`.
    Application-specific access to the process data image can be made here, which is synchronous with the bus cycle.

EcTimingTask()
    Timing Thread. This thread sets the timing event that triggers the EcMonitorJobTask for the next cycle.

:cpp:func:`emonInitMonitor`
    Prepare the |Product| for operation and set operational parameters, e.g. used Real-time Ethernet Driver, buffer sizes, maximum number of slaves, ... .

:cpp:func:`emonConfigureNetwork`
    Loads the configuration from the ENI (XML file).

:cpp:func:`emonRegisterClient`
    Register the application as a client at the |Product| to receive event notifications.

:cpp:func:`emonDeinitMonitor`
    Clean up.