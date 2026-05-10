***********
Definitions
***********

Terms
*****

+-------------------------------------+----------------------------------+
| Absent Slave                        | Config Slave not found on        |
|                                     | Bus.                             |
+-------------------------------------+----------------------------------+
| ACTIVE                              | Key value of Master Redundancy   |
|                                     | State                            |
+-------------------------------------+----------------------------------+
| Acyclic Master Red Frames           | Frames sent by ACTIVE to         |
|                                     | INACTIVE Master for acyclic      |
|                                     | Master-to-Master communication.  |
+-------------------------------------+----------------------------------+
| Application                         | EC-Master Application            |
+-------------------------------------+----------------------------------+
| Application Layer Status            | Enumeration of INIT, BOOT,       |
|                                     | PRE-OP, SAFE-OP, OP of the       |
|                                     | ESM.                             |
+-------------------------------------+----------------------------------+
| Arbitration                         | Procedure leading to decision    |
|                                     | which Master must                |
|                                     | become/be ACTIVE.                |
+-------------------------------------+----------------------------------+
| Bus                                 | EtherCAT® Network                |
+-------------------------------------+----------------------------------+
| Bus owner                           | Master that won Arbitration,     |
|                                     | got ACTIVE and may control       |
|                                     | the bus.                         |
+-------------------------------------+----------------------------------+
| Bus scan                            | Get or update topology knowledge |
|                                     | by communication with Slaves.    |
+-------------------------------------+----------------------------------+
| Bus Slave                           | Slave that can be addressed by   |
|                                     | Cmd\ s.                          |
+-------------------------------------+----------------------------------+
| Connection to Master                | Master-Slave-Communication:      |
|                                     | Slave can (directly or           |
|                                     | indirectly) receive Frames       |
|                                     | from Master.                     |
|                                     | Appl                             |
|                                     | ication-Master-Communication:    |
|                                     | RAS connection via TCP.          |
+-------------------------------------+----------------------------------+
| Control the Bus                     | Send Cmd\ s to the Bus to        |
|                                     | directly interact with Slaves.   |
+-------------------------------------+----------------------------------+
| Config Slave                        | Slave configured in ENI          |
+-------------------------------------+----------------------------------+
| Cyclic Master Red Frames            | Frames sent cyclically by        |
|                                     | ACTIVE to INACTIVE Master        |
|                                     | containing Shadow Process Data   |
|                                     | and Master Redundancy Process    |
|                                     | Data.                            |
+-------------------------------------+----------------------------------+
| Cyclic Slave Frames                 | Frames sent by ACTIVE Master     |
|                                     | to Slaves containing Process     |
|                                     | Data. Forwarded by INACTIVE      |
|                                     | Master.                          |
+-------------------------------------+----------------------------------+
| EC-Master Application               | Program executing EC-Master API  |
|                                     | functions.                       |
+-------------------------------------+----------------------------------+
| EC-Master Instance                  | Stack Instance controlled by     |
|                                     | Application\ (s) and             |
|                                     | interfacing NIC\ (s).            |
+-------------------------------------+----------------------------------+
| EtherCAT® device                    | Slave or Master.                 |
+-------------------------------------+----------------------------------+
| EtherCAT® Network Information       | EtherCAT® XML Master             |
|                                     | Configuration                    |
+-------------------------------------+----------------------------------+
| Ethernet source address semantic    | Merge of MAC address and Master  |
|                                     | State information.               |
+-------------------------------------+----------------------------------+
| Failover                            | Switching from previously        |
|                                     | ACTIVE Master to STANDBY         |
|                                     | Master upon the failure of       |
|                                     | previously ACTIVE Master.        |
+-------------------------------------+----------------------------------+
| Frame                               | EtherCAT®/Ethernet Frame.        |
+-------------------------------------+----------------------------------+
| Frame loss                          | Frame sent by Master but not     |
|                                     | received in next cycle or lost   |
|                                     | at all.                          |
+-------------------------------------+----------------------------------+
| Job Task                            | Cyclical execution of Master     |
|                                     | API\ s (“Jobs”) to send,         |
|                                     | receive and process frames.      |
+-------------------------------------+----------------------------------+
| Hybrid Access                       | Executing Master API\ s from     |
|                                     | EC-Master Library and RAS Client |
|                                     | Library.                         |
+-------------------------------------+----------------------------------+
| INACTIVE                            | Key value of Master Redundancy   |
|                                     | State                            |
+-------------------------------------+----------------------------------+
| Isolated Slave                      | Slave without Connection to      |
|                                     | Master.                          |
+-------------------------------------+----------------------------------+
| Real-time Ethernet Driver Instance  | NIC exclusively assigned to      |
|                                     | and interfaced by a Master.      |
+-------------------------------------+----------------------------------+
| Log Message                         | Hint from Master to              |
|                                     | Application as formatted,        |
|                                     | zero-terminated char array of    |
|                                     | arbitrary length.                |
+-------------------------------------+----------------------------------+
| MAIN Frame                          | Frame sent on first Ehternet     |
|                                     | Driver Instance.                 |
+-------------------------------------+----------------------------------+
| Master API                          | Functions exported from the      |
|                                     | EC-Master Library (EcMaster.dll) |
|                                     | to control an EC-Master          |
|                                     | Instance.                        |
+-------------------------------------+----------------------------------+
| Master State                        | State of the Master\ ’s          |
|                                     | internal ESM                     |
+-------------------------------------+----------------------------------+
| Master                              | EC-Master Instance               |
+-------------------------------------+----------------------------------+
| Master Redundancy Configuration     | Set Master Redundancy            |
|                                     | Parameters to Master in order    |
|                                     | to apply Master Redundancy.      |
+-------------------------------------+----------------------------------+
| Master Redundancy Parameters        | Structured parameter set needed  |
|                                     | for Master Redundancy            |
|                                     | Configuration.                   |
+-------------------------------------+----------------------------------+
| Master Redundancy State             | Enumeration of ACTIVE,           |
|                                     | INACTIVE                         |
+-------------------------------------+----------------------------------+
| Master-To-Master Process data       | ACTIVE to INACTIVE / INACTIVE    |
|                                     | to ACTIVE Master Process Data    |
+-------------------------------------+----------------------------------+
| Message                             | Implemented as Notification or   |
|                                     | Log Message.                     |
+-------------------------------------+----------------------------------+
| Network TAP                         | Virtual network adapter to OS,   |
|                                     | freely available from OpenVPN.   |
+-------------------------------------+----------------------------------+
| Notification                        | Parametrized Message of          |
|                                     | well-defined length identified   |
|                                     | by ID. Typically, but not        |
|                                     | necessarily raised by the        |
|                                     | Master. Application\ (s) can     |
|                                     | subscribe to by registering as   |
|                                     | client.                          |
+-------------------------------------+----------------------------------+
| Master Redundancy                   | Appliance implementing e.g.      |
|                                     | Failover to increase system’s    |
|                                     | availability.                    |
+-------------------------------------+----------------------------------+
| Present Slave                       | Config Slave found on Bus.       |
+-------------------------------------+----------------------------------+
| Port                                | NIC at Master or Port A, B,      |
|                                     | C or D at ESC.                   |
+-------------------------------------+----------------------------------+
| Port Link                           | Direct connection between two    |
|                                     | Port\ s.                         |
+-------------------------------------+----------------------------------+
| Process Data Image                  | RAM allocated by each Master     |
|                                     | and cyclically synchronized with |
|                                     | Slaves and other Master.         |
|                                     | Size defined in ENI.             |
+-------------------------------------+----------------------------------+
| RED Frame                           | Frame sent on second Ethernet    |
|                                     | Driver Instance.                 |
+-------------------------------------+----------------------------------+
| Redundancy Frame ID                 | Used for Split and Merge.        |
+-------------------------------------+----------------------------------+
| Shadow Process Data                 | Slave Process Data from last     |
|                                     | cycle as result from Split and   |
|                                     | Merge.                           |
+-------------------------------------+----------------------------------+
| Slave                               | EtherCAT® slave containing an    |
|                                     | ESC connected to the Bus.        |
+-------------------------------------+----------------------------------+
| Set Master Redundancy State         | Request Master Redundancy        |
|                                     | State change, e.g. in order to   |
|                                     | become ACTIVE or INACTIVE.       |
+-------------------------------------+----------------------------------+
| Split and Merge                     | The Master uses RED Frame\ s     |
|                                     | and MAIN Frame\ s to             |
|                                     | Control the Bus.                 |
+-------------------------------------+----------------------------------+
| STANDBY Master                      | INACTIVE Master ready for        |
|                                     | Takeover.                        |
+-------------------------------------+----------------------------------+
| Store and Forward                   | Receive a complete Frame,        |
|                                     | evaluate (modify) it and forward |
|                                     | it.                              |
+-------------------------------------+----------------------------------+
| Switchover                          | Intentionally switching from     |
|                                     | previously ACTIVE Master to      |
|                                     | STANDBY Master not upon          |
|                                     | the failure of previously        |
|                                     | ACTIVE Master.                   |
+-------------------------------------+----------------------------------+
| Stop                                | Becoming INACTIVE or             |
|                                     | terminate.                       |
+-------------------------------------+----------------------------------+
| System                              | Set of Applications,             |
|                                     | Masters, Slaves interacting      |
|                                     | with each other (HW, SW)         |
+-------------------------------------+----------------------------------+
| Takeover                            | Becoming ACTIVE.                 |
+-------------------------------------+----------------------------------+
| Terminate                           | Exit Application.                |
+-------------------------------------+----------------------------------+
| Topology Knowledge                  | Information about present        |
|                                     | Slaves\ ’ presence and           |
|                                     | mismatching Slaves including     |
|                                     | Port Link\ s.                    |
+-------------------------------------+----------------------------------+
| Trace Data                          | Process Data in Cyclic Slave     |
|                                     | Frames, but not addressed to     |
|                                     | slaves.                          |
+-------------------------------------+----------------------------------+
| Visible EtherCAT® device            | EtherCAT® device connected to    |
|                                     | the Bus receiving and            |
|                                     | processing Frame\ s. In case     |
|                                     | of Frame Loss there may be       |
|                                     | Slave\ s that are not visible,   |
|                                     | but receiving and processing     |
|                                     | Frame\ s.                        |
+-------------------------------------+----------------------------------+


Abbreviations
*************

========= ===================================================
AL        Application Layer
AL Status Application Layer Status
BOOT      Bootstrap State (ESM)
Cmd       Command (EtherCAT®)
CMF       Cyclic Master Red Frames (s.a. CSF)
CSF       Cyclic Slave Frames (s.a. CMF)
EC        EtherCAT®
ECAT      EtherCAT®
ENI       EtherCAT® Network Information
ESC       EtherCAT® Slave Controller
ESM       EtherCAT® State Machine
EoE       Ethernet over EtherCAT®
FoE       File access over EtherCAT®
FPRD      Configured Address Physical Read (EtherCAT® command)
INIT      Init State (ESM, Master Redundancy State)
Msg       Message, e.g. log msg from master to application.
NIC       Network Interface Card
OP        Operational State (ESM)
OS        Operating System
PoC       Proof of Concept
PREOP     Pre-Operational State (ESM)
PD        Process Data
PD Image  Process Data Image
RAS       Remote Access Service
TAP       Network tap
SAFEOP    Safe-Operational State (ESM)
WKC       Working Counter
========= ===================================================

********
Overview
********

Master Redundancy Architecture
******************************

EtherCAT® systems provide a high level of availability even in case of device failures. A typical EtherCAT® system with cable redundancy for high availability consists of a dual-NIC Master Device and Slaves:

.. figure:: ../Media/master-red_single-master-system.png
    :alt:

Without Master Redundancy, the Master device exposes a single point of failure to the system in case of failing which affects the availability of the complete EtherCAT® system:
  
.. figure:: ../Media/master-red_master-device-failure.png
    :alt:

In order to increase the availability of the EtherCAT® system, a redundant Master capable for Failover is needed as backup. The Backup Master is INACTIVE until it needs to takeover and control the bus.
The following diagram shows two redundant Master Devices. Each Master Device has two network interface cards (NICs) for EtherCAT® communication:

.. figure:: ../Media/master-red_dual-master.png
    :alt:

If the ACTIVE Master fails, the Backup Master can takeover. Because the INACTIVE Master is connected to the network, it can control the bus in case of Failover:

.. figure:: ../Media/master-red_failover.png
    :alt:
    
Master Device Architecture
**************************

Each Master Device consists of the Master application and the EC-Master stack as shown in the following figure:
 
.. figure:: ../Media/master-red_master-device.png
    :alt:

Features
********

Master Redundancy State
=======================

A Master on the network can be ACTIVE or INACTIVE. ACTIVE means that this Master controls the bus. The Application can get or set its Master’s Redundancy State at any time using an EC-Master API.

Failover and Switchover
=======================

The transition from INACTIVE to ACTIVE is called Takeover. 
The application can initiate the Takeover by calling an EC-Master API. The EC-Master automatically changes to ACTIVE / INACTIVE upon Application’s request.

Takeover is called Failover if the previously ACTIVE Master failed and the previously INACTIVE Master got ACTIVE and no INACTIVE Master remains. 

Takeover is the key functionality of Master Redundancy. 

Failover implies the need to detect the failure which must be implemented by the Application. 

Takeover is called Switchover if there is no error at the ACTIVE Master, but the Application switches the ACTIVE Master to INACTIVE and the INACTIVE Master to ACTIVE. Switchover is needed as one way to prove that failover is possible. The Applications can do a Switchover by coordinated setting the Masters to ACTIVE and INACTIVE.

“Hot Standby”, “Warm Standby” and “Cold Standby”
================================================

“Hot Standby” means that a Switchover or Failover from STANDBY to ACTIVE is processed usually without notice to the slaves. 

“Warm Standby” means that the devices recognize the failover, typically because there are several steps, like scanning the bus, needed in order that the INACTIVE Master becomes ACTIVE. The decision between the redundancy types “Hot Standby” and “Warm Standby” is determined by the Application which is responsible to detect failure and control the reaction. Going through EtherCAT® States INIT, PREOP, SAFE-OP, OP leads to “Warm Standby”. 

“Cold Standby” means that there is an offline device, a spare part to replace the failing component changed manually. 

Store and Forward
=================

The INACTIVE Master receives and forwards frames from the ACTIVE Master.

Master State Synchronization
============================

The INACTIVE Master cyclically gets the current EtherCAT® state from the ACTIVE Master.

Process Data Synchronization
============================

The INACTIVE Master cyclically gets the Process Data from the ACTIVE Master. The ACTIVE Master can also cyclically exchange Master specific Process Data with the INACTIVE Master.

Acyclic Master-To-Master Communication
======================================

The Masters can acyclically communicate which each other.

Collision Detection
===================
The EC-Master detects if another Master sends frames to the network. This is called a collision and the EC-Master reports it to the Application
