*****************************
Master-Master Synchronization
*****************************

Process Data areas
******************

The INPUTs and OUTPUTs of Slaves are part of the Process Data Image. The Slaves’ Process Data size (cyclic datagrams) and content structure (variables) is defined by the ENI file. The Process Data Image can be extended with Master-To-Master Process Data by API, see MasterRedParms at :cpp:func:`emInitMaster`.

Master-To-Master Process data is asymmetrically, bi-directionally implemented as ACTIVE to INACTIVE Master Process Data and INACTIVE to ACTIVE Master Process Data.

Each Process Data area has a dedicated pointer exposed by API:

+-------------------------------------+--------------------------------------------------+
| Slave OUTPUTs                       | :cpp:func:`emGetProcessImageOutputPtr`           |
+-------------------------------------+--------------------------------------------------+
| ACTIVE to INACTIVE Master (OUTPUTs) |	:cpp:func:`emGetMasterRedProcessImageOutputPtr`  |
+-------------------------------------+--------------------------------------------------+
| Slave INPUTs                        | :cpp:func:`emGetProcessImageInputPtr`            |
+-------------------------------------+--------------------------------------------------+
| INACTIVE to ACTIVE Master (INPUTs)  | :cpp:func:`emGetMasterRedProcessImageInputPtr`   |
+-------------------------------------+--------------------------------------------------+

The memory is by default allocated by :cpp:func:`emInitMaster`, but can also be provided by the application, see structure :cpp:struct:`EC_T_MEMPROV_DESC` at :ref:`emIoControl - EC_IOCTL_REGISTER_PDMEMORYPROVIDER`.

Synchronization
===============

The Application must perform the same sequence on both masters. The Master shall perform the appropriate activities based on the INACTIVE/ACTIVE State.
The Process Data Image is cyclically updated in the following order

.. seealso:: :ref:`EcMasterDemoMasterRed`

#. ProcessAllRxFrames updates the Process Data Image with contents of the last received frames. This contains OUTPUTs to Slaves, INPUTs from Slaves, and INACTIVE to ACTIVE Master Process Data. The data was polled by SendAllCycFrames within the last cycle.
#. The ACTIVE application changes the OUTPUTs in the Process Data Image, e.g. at myAppWorkPd.
#. SendAllCycFrames at the ACTIVE Master pushes the following:

- Slave OUTPUTs from the Process Data Image of this cycle 
- ACTIVE to INACTIVE Master OUTPUTs from the Process Data Image of this cycle
- Merged Slave INPUTs from the last cycle to the INACTIVE Master SendAllCycFrames polls the INPUTs for the next cycle.

Consistency
===========

EtherCAT® ensures consistency and integrity constraints on EtherCAT® datagram level. Process data is distributed across different datagrams in different frames. The ACTIVE Master merges the received frames from MAIN and RED Real-time Ethernet Driver before further processing. The EC-Master must report Process Data communication errors to the Application using :ref:`emNotify - EC_NOTIFY_CYCCMD_WKC_ERROR`. The ACTIVE Master sends the merged Slave INPUTs to the INACTIVE Master as Shadow Process Data to ensure consistency.

Independent of Master Redundancy: Consistency and integrity constraints checks of the overall Process Data Image that is synchronized across multiple datagrams must be ensured by the Application, as the EC-Master checks on EtherCAT® datagram level.

Memory Provider
===============

The EC-Master by default allocates the Process Data Image. The EC-Master alternatively supports registering a Memory Provider so that the Application can allocate the Process Data Image. Multi-threaded Process Data access by the Application must be synchronized by the Application. This is not Master Redundancy specific and also not needed for single threaded Process Data handling in Job Task.

State Synchronization
*********************

The INACTIVE Master assumes the Master State (INIT, PREOP, SAFEOP, OP) from the Cyclic Master Red Frame in order to immediately continue sending Process Data to Slaves on Takeover. Therefor the INACTIVE Application cannot tell the INACTIVE EC-Master about the current EtherCAT® State (INIT, PREOP, SAFE-OP or OP). The ACTIVE and INACTIVE Application can get the current EtherCAT® State by calling :cpp:func:`emGetMasterState`. (REQ031, REQ032)

Topology Knowledge
******************

Slaves’ presence and Slaves’ ESM State (INIT, PREOP, SAFEOP, OP) information is stored in the Slave State Image that is automatically synchronized in CMF.
On Takeover the new ACTIVE Master immediately exchanges process data, but it needs some time to validate the Slave State Image to know which slaves are present. The System’s requirements constrain the delay until the Application must have the knowledge of Slaves’ presence after Takeover with time-out. A regular bus scan is time expensive due to e.g. EEPROM reading from the slaves. Because the Bus Slave Info cache is extensive, bus slaves are recorded explicitly and APIs like :cpp:func:`emGetBusSlaveInfo` return :cpp:struct:`EC_E_MASTER_RED_STATE_INACTIVE` until the Master has read the Slave’s EEPROM which is only possible while the Master is Bus Owner.

Shadow Process Data
*******************

The ACTIVE Master always sends Frames on both Real-time Ethernet Driver Instances to implement Cable Redundancy and merges the returning data when processing the frames. This is called Split and Merge.

The INACTIVE Master implements Store and Forward, but in case of a line break, it does not see all INPUT data from Slaves in Cyclic Slave Frames, see :ref:`Frame Processing with Line-Break`. The data from Cyclic Slave Frames seen by the INACTIVE Master is therefore in case of line-break inconsistent and incomplete. Therefore the ACTIVE Master sends the merge result as Shadow Process Data in Cyclic Master Red Frames to the INACTIVE Master on both Real-time Ethernet Driver Instances to supply consistent Process Data. The INACTIVE Master reads the Process Data INPUTs, OUTPUTs from the Shadow Process Data.

Cyclic Master Red Frames
************************

The ACTIVE Master sends the Cyclic Master Red Frames to the INACTIVE Master containing Shadow Process Data from slaves and Master-To-Master Process Data when the Application calls SendAllCycFrames. The INACTIVE Master automatically processes (parses) the frames from the ACTIVE Master and returns them. 

The Cyclic Master Red Frames are conforming to the EtherCAT® standard, but do not address any slave. Additionally they contain Master-To-Master Process Data. Because Cyclic Master Red Frames are additional frames they must be considered for bus load and CPU load. 

EtherCAT® Network Information
*****************************

Because Hot Standby must be implemented the ENIs must match each other, especially in respect of Fixed Address assignments, Topology declaration, Sync Manager Settings, FMMU settings, etc. The EtherCAT® Network Information (ENI) is not automatically synchronized between the Masters. The Application has to ensure the correct ENI is loaded.