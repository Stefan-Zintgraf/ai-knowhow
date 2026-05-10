*************
Specification
*************

Requirements
************

The following requirements are referenced in this document:

+--------+-------------------------------------+---------------------+
| No     | Requirement                         | Response\  [3]      |
+========+=====================================+=====================+
| REQ001 | The ACTIVE Master must control the  | Master              |
|        | bus                                 |                     |
+--------+-------------------------------------+---------------------+
| REQ002 | Expose Master Redundancy State      | Master              |
+--------+-------------------------------------+---------------------+
| REQ003 | Support changing Master Redundancy  | Master              |
|        | State                               |                     |
+--------+-------------------------------------+---------------------+
| REQ004 | Choose one of the Masters as Bus    | Application         |
|        | owner (Arbitration) (see also       |                     |
|        | REQ035)                             |                     |
+--------+-------------------------------------+---------------------+
| REQ005 | If the Master system fails there    | System              |
|        | must be a backup Master that can    |                     |
|        | control the bus                     |                     |
+--------+-------------------------------------+---------------------+
| REQ006 | Layer Instance must have a unique   | System              |
|        | MAC address                         |                     |
+--------+-------------------------------------+---------------------+
| REQ007 | The Real-time Ethernet Driver       | Master              |
|        | must support Interrupt Mode.        |                     |
+--------+-------------------------------------+---------------------+
| REQ008 | Configure a Network TAP with unique | System              |
|        | MAC and IP Address assignment at    |                     |
|        | each Master                         |                     |
+--------+-------------------------------------+---------------------+
| REQ009 | Provide parameters for operation    | Application         |
+--------+-------------------------------------+---------------------+
| REQ010 | EC-Master parameters and ENI files  | Application         |
|        | must be identical                   |                     |
+--------+-------------------------------------+---------------------+
| REQ011 | Port 0 must be connected            | System              |
+--------+-------------------------------------+---------------------+
| REQ012 | Links at failing Master must go     | System              |
|        | down                                |                     |
+--------+-------------------------------------+---------------------+
| REQ013 | Slaves must be connected on same    | System              |
|        | line                                |                     |
+--------+-------------------------------------+---------------------+
| REQ014 | Become ACTIVE/INACTIVE on request   | Master              |
|        | (see also REQ015)                   |                     |
+--------+-------------------------------------+---------------------+
| REQ015 | Request ACTIVE/INACTIVE             | Application         |
+--------+-------------------------------------+---------------------+
| REQ016 | Request INACTIVE on collision       | Application         |
+--------+-------------------------------------+---------------------+
| REQ017 | Report collision                    | Master              |
+--------+-------------------------------------+---------------------+
| REQ018 | Detected communication time-out     | Application         |
+--------+-------------------------------------+---------------------+
| REQ019 | Support Interrupt mode              | Master              |
+--------+-------------------------------------+---------------------+
| REQ020 | Configure Interrupt mode (polling   | Application         |
|        | mode not supported).                |                     |
+--------+-------------------------------------+---------------------+
| REQ021 | Listen if another master sending    | Application         |
|        | frames                              |                     |
+--------+-------------------------------------+---------------------+
| REQ022 | Perform the appropriate activities  | Master              |
|        | based on the INACTIVE/ACTIVE State. |                     |
+--------+-------------------------------------+---------------------+
| REQ023 | Call OnMasterTimer exactly once per | Application         |
|        | cycle                               |                     |
+--------+-------------------------------------+---------------------+
| REQ024 | Call ecatSetMasterState at Bus      | Application         |
|        | owner                               |                     |
+--------+-------------------------------------+---------------------+
| REQ025 | Report failing Master return        | Master              |
+--------+-------------------------------------+---------------------+
| REQ026 | Handle failing Master return        | Application         |
+--------+-------------------------------------+---------------------+
| REQ027 | The Master-Master Frame must be     | Master              |
|        | used to guarantee consistency       |                     |
+--------+-------------------------------------+---------------------+
| REQ028 | Report Process Data communication   | Master              |
|        | errors                              |                     |
+--------+-------------------------------------+---------------------+
| REQ029 | Consistency and integrity           | Master              |
|        | constraints checks of datagrams     |                     |
+--------+-------------------------------------+---------------------+
| REQ030 | Consistency and integrity           | Application         |
|        | constraints checks of the overall   |                     |
|        | Process Data Image                  |                     |
+--------+-------------------------------------+---------------------+
| REQ031 | The INACTIVE EC-Master must         | Master              |
|        | synchronize the EtherCAT® State from |                    |
|        | the Cyclic Master Red Frame sent by |                     |
|        | the ACTIVE EC-Master                |                     |
+--------+-------------------------------------+---------------------+
| REQ032 | Provide current EtherCAT® State at   | Master             |
|        | ACTIVE and INACTIVE Master          |                     |
|        | (ecatGetMasterState)                |                     |
+--------+-------------------------------------+---------------------+
| REQ034 | Communication between the Masters   | Master              |
|        | must be possible at any state       |                     |
|        | without additional hardware needed  |                     |
|        | to provide a TCP/IP connection      |                     |
|        | between the ACTIVE and the INACTIVE |                     |
|        | Master                              |                     |
+--------+-------------------------------------+---------------------+
| REQ035 | ACTIVE Master (else EtherCAT® frame | System              |
|        | sending stops) (see also REQ014)    |                     |
+--------+-------------------------------------+---------------------+
| REQ036 | Register an EoE endpoint as network | Application         |
|        | adapter                             |                     |
+--------+-------------------------------------+---------------------+
| REQ037 | Start RAS Server                    | Application         |
+--------+-------------------------------------+---------------------+
| REQ038 | INACTIVE Master must be always      | System              |
|        | connected to the network            |                     |
+--------+-------------------------------------+---------------------+
| REQ039 | Reduce TAP adapter’s MTU            | System              |
+--------+-------------------------------------+---------------------+
| REQ040 | Encapsulate TAP communication       | Master              |
|        | (acyclic frames)                    |                     |
+--------+-------------------------------------+---------------------+
| REQ041 | Configure Master Redundancy         | Application         |
|        | (ecatInitMaster)                    |                     |
+--------+-------------------------------------+---------------------+
| REQ042 | Retry denied mailbox transfers      | Application         |
|        | (e.g. Switchover)                   |                     |
+--------+-------------------------------------+---------------------+
| REQ043 | Slave State Sync                    | Master              |
+--------+-------------------------------------+---------------------+
| REQ044 | Hot Connect                         | Master              |
+--------+-------------------------------------+---------------------+
| REQ045 | Diagnosis Image Sync                | Master              |
+--------+-------------------------------------+---------------------+
| REQ046 | Support Master-To-Master Process    | Master              |
|        | data hosting with Memory Provider   |                     |
+--------+-------------------------------------+---------------------+
| REQ047 | ENI without LRW                     | System              |
+--------+-------------------------------------+---------------------+
| REQ048 | Handle merging of two independent   | Application         |
|        | EtherCAT® networks                  |                     |
+--------+-------------------------------------+---------------------+

Design Features
***************

Master Redundancy needs and provides the following set of features, referenced in this document:

====== ====================================== ===========
No     Feature                                Chapter
====== ====================================== ===========
1      Master Redundancy State                3.3
2      Failover                               3.6
3      Hot Standby                            2.3.3
4      Store and Forward                      4.4, 6.1
5      Master State Synchronization           4.1
6      Slave Process Data Synchronization     4.1, 4.4
7      Acyclic Master-To-Master Communication 4.4, 5.4
8      Remote Access                          5.5
9      Cable Redundancy                       6.1.2
10     Collision Detection                    3.4
13     ACTIVE to INACTIVE Master Process Data 4.1
14     INACTIVE to ACTIVE Master Process Data 4.1
====== ====================================== ===========

Master Redundancy State: Current state and Control
**************************************************

The behavior of the EC-Master is determined by its Master Redundancy State which can be either ACTIVE or INACTIVE. Initial value is INACTIVE and can be set to ACTIVE by the Application. 

If the Master system fails there must be a backup Master that can control the bus (REQ005). The Master that must control the bus (REQ001) is called the ACTIVE Master (Bus owner) and the backup Master is called INACTIVE Master.

The EC-Master exposes its current Master Redundancy State (REQ002) and a means to change it by the API :cpp:func:`emGetMasterRedState` and :cpp:func:`emSetMasterRedStateReq` (REQ003, REQ014). Changes are signalled with notification :ref:`emNotify - EC_NOTIFY_MASTER_RED_STATECHANGED`, for e.g. diagnostic over RAS.

- Calling :cpp:func:`emSetMasterRedStateReq` with same state again and state didn't change will have no effect.
- Calling :cpp:func:`emSetMasterRedStateReq` more often than once per cycle makes no sense.
- Collisions are detected within one cycle.
- MACs are NIC dependent and therefore will not change on reboot (only if you replace the NIC).
- Foreign Frames are only forwarded if the Master is INACTIVE. So the application must set the Master INACTIVE on collision to only lose frames from one cycle and not from several cycles.
- Even in case of collission, frame is still provided to application

Exclusive bus control
*********************

It is not possible to concurrently control the bus. One Master must exclusively control the bus (REQ001, REQ015). The EC-Master detects collisions in case of concurrent bus control and sends the notification :ref:`emNotify - EC_NOTIFY_FRAME_RESPONSE_ERROR` with parameter eRspErr_FOREIGN_SRC_MAC to the Application (REQ016, REQ017). Collision Detection needs each Real-time Ethernet Driver Instance to have a unique MAC address (REQ006). 

If there are more than one Master able to control the bus, Arbitration is needed to determine which Master must Control the Bus (Bus owner) the other Master may not control the Bus and stay INACTIVE. The application must choose one of the Masters as Bus owner and set it ACTIVE and the other to INACTIVE issuing :cpp:func:`emSetMasterRedStateReq`, e.g. by waiting a random delay before Takeover, see below (REQ004).

If both masters are INACTIVE, no master-Master communication is possible.

Failure Detection
*****************

The ACTIVE Master cyclically sends frames to the INACTIVE Master. If it stops sending frames it is a symptom for system failure. The INACTIVE Master cannot know if the communication from the ACTIVE Master stops, this must be detected by the application (REQ018). See also Implementation Hints.

Startup
*******

A starting Master cannot know if it is the first one or not so the startup procedure for all Masters on the network is the same (REQ022, REQ023, REQ024, REQ027, REQ028, REQ029, REQ030). It is as follows:

- Call :cpp:func:`emInitMaster` with Real-time Ethernet Driver and Master Redundancy parameters (REQ009, REQ010). Initial state is INACTIVE with automatic Store and Forward as soon as Real-time Ethernet Drivers are opened. The Master parameters must be identical at each Master (REQ010).
- Start JobTask cyclically calling :cpp:func:`emExecJob` and enable EtherCAT® link to other EtherCAT® devices
- Call :cpp:func:`emConfigureNetwork` with ENI file
- Master Redundancy requires use of interrupt mode (REQ007, REQ019, REQ020). The Application must provide a call back function. Call :ref:`emIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB` to register the callback function to trigger on ACTIVE Master’s communication at application level of ACTIVE and INACTIVE Master.
- Call :cpp:func:`emRegisterClient` to enable collision detection (REQ016)
- The Master reports collisions to the application. The application must arbitrate (REQ004).
- The Application must, before trying to get active, listen on the bus if there is another master sending frames (REQ021). Store and Forward and Master-To-Master communication is now established. On System startup there is no ACTIVE Master.

Store and Forward and Master-To-Master communication is now established. On System startup there is no ACTIVE Master.

Expected behaviour
******************

The ACTIVE Master automatically polls the INACTIVE Master for information. The ACTIVE Master does not forward frames.

The INACTIVE Master does not send frames on its own, but forwards frames from ACTIVE Master. Master to Master communication is polled like Slave to Master communication.

Master Redundancy State change requests are applied when the Application’s JobTask calls OnMasterTimer. The Application’s JobTask must call OnMasterTimer exactly once per cycle therefore the delay of applying the Master Redundancy State change request is at worst case 1 cycle.

INACTIVE Master denies acyclic communication to slaves, because it may not control the bus.

On Takeover, Mailbox transfers may be denied by the ACTIVE Master until it knows the slave is present. The first call may be not successful, because Mailbox communication was interrupted by the Takeover at the slave. The Application can retry at a later time, at earliest at the next cycle. (REQ042)

.. important:: Don’t interrupt a slave firmware update, it may destroy the device!

Failover
********

To Takeover (becoming ACTIVE) the application must call:

- :cpp:func:`emSetMasterRedStateReq` (EC_TRUE) to become ACTIVE
- :cpp:func:`emSetMasterState`, e.g. OPERATIONAL if needed, e.g. at startup

If the ACTIVE Master fails, the RED port gets deactivated and following the EtherCAT® standard the frames from MAIN return on MAIN:

.. figure:: ../Media/master-red_failover-fpo.png
    :alt:
    
Recovery from Failover
**********************

In case the failing Master returns (REQ025, REQ026), the Application at the INACTIVE Master will notice the communication from the ACTIVE Master and the INACTIVE Application must stay INACTIVE.

.. important:: In case both Masters got separated in two independent EtherCAT® networks by a double line break as shown below, the recovery from Failover by repairing the cables, will lead to collision with two ACTIVE Masters which must (REQ048) be handled by the Application at both ACTIVE Masters:

.. figure:: ../Media/master-red_failover-dividing-slaves.png
    :alt:
    
Restrictions
************

The following known restrictions apply to Master Redundancy:

- Polling Mode is not supported, because the INACTIVE Master must forward frames in the same cycle.
- Cable Redundancy is mandatory for Master Redundancy. This implies restrictions to ENI.
- At INACTIVE Master WKC mismatches are not notified, but mismatches can be alternatives detected using the Diagnosis Image (REQ045).
- All Slaves Must Reach Master State False is only supported at start-up, but not on takeover in PREOP / SAFEOP / OP.
- Distributed Clocks needs special handling for port propagation delay measurement (currently not supported)