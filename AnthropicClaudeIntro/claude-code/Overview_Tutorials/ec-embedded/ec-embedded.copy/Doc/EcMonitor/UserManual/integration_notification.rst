******************
Event notification
******************

The |Product| provides event notification for a great number of events. These events are for example:

- Bus state change
- Link state change
- Working counter errors
- ...

Any thread can register for these events to be notified. This is achieved by calling the API function 

.. cpp:alias:: emonRegisterClient

An example implementation for processing notifications is contained in the class ``CEmNotification`` of the EcMonitorDemo example, see :file:`Examples/Common/EcNotification.cpp`.. It implements the full framework to catch and process the |Product| notifications. 
The class is instantiated once and registered at the |Product| with the call :cpp:func:`emonRegisterClient`. It contains the method :cpp:func:`ecatNotify` as major entry point (or callback function) for every event notification.

There are two different ways events can be handled. The method of handling an event is primarily determined by the time required to handle the event and the processing context in which the event is to be handled.

Direct event notification handling
**********************************

Minor events that take a very short time to process can be handled directly in the context in which they are recognized. A possible example of such an event is the detection of a false working counter (WKC). 

.. uml::

    skinparam monochrome true
    skinparam SequenceMessageAlign direction
    hide footbox

    participant JobTask as "EcMonitorJobTask"
    participant EcEmbedded as "EC-Monitor"
    participant EcNotification

    activate JobTask
    JobTask->EcEmbedded : emonExecJob(ProcessAllRxFrames)

    activate EcEmbedded
    EcEmbedded->EcEmbedded : Receive Frames
    EcEmbedded->EcEmbedded : Process Frames
    EcEmbedded->EcEmbedded : Detect Errors
    activate EcEmbedded
    EcEmbedded->EcNotification : invoke NotifyCallback()

    activate EcNotification
    EcNotification->EcNotification : ecatNotify()
    EcNotification->: Error Log Message
    return

    deactivate EcEmbedded
    return

    JobTask->JobTask : myAppWorkPd()

The event handling is reduced to simply issuing a log message, which is not time critical. The event is handled directly within the context of the :cpp:func:`emonExecJob` function.

Postponed notification handling
*******************************

Events that require more time-consuming processing cannot be handled directly in the context in which they are detected. The handling or processing of the event must be postponed. This is accomplished through a queue, which is also readily implemented using the ``CEmNotification`` class.

.. uml::

    skinparam monochrome true
    skinparam SequenceMessageAlign direction
    skinparam SequenceBoxBorderColor transparent
    hide footbox

    participant EcDemoApp
    participant JobTask as "EcMonitorJobTask"
    participant EcEmbedded as "EC-Monitor"
    box
        participant EcNotification
        database Notifications
    end box

    activate EcDemoApp
    activate JobTask
    JobTask->EcEmbedded : emonExecJob(ProcessAllRxFrames)

    activate EcEmbedded
    EcEmbedded->EcEmbedded : Receive Frames
    EcEmbedded->EcEmbedded : Process Frames
    EcEmbedded->EcEmbedded : Detect Errors
    activate EcEmbedded
    EcEmbedded->EcNotification : invoke NotifyCallback()

    activate EcNotification
    EcNotification->EcNotification : ecatNotify()
    activate EcNotification
    EcNotification->Notifications : EnqueueJob()
    deactivate EcNotification
    return

    deactivate EcEmbedded
    return
    deactivate JobTask
    ...
    EcDemoApp->EcNotification : ProcessNotificationJobs()
    activate EcNotification
    EcNotification->Notifications : DequeueJob()
    EcNotification<--Notifications
    activate EcNotification
    EcNotification->EcNotification : Process()
    deactivate EcNotification
    return

By calling periodically ``CEmNotification::ProcessNotificationJobs()``, the application checks and handles all queued notifications.

.. important::
    The call of ``CEmNotification::ProcessNotificationJobs()`` shall NOT be executed in the context of :cpp:func:`EcMonitorJobTask`. As the CPU time consumption may be high, this would have a high impact to the real-time behavior of the cyclic operation.