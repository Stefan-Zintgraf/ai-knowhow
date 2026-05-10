************
Introduction
************

Achieving a maximum flexibility with Hot-Connect.

The concept of Hot-Connect first of all refers to the connecting and disconnecting of slaves in a running (hot) system.
However, this is just one of several possible scenarios.
Much more often it is required to operate the system without a perfect match between the EtherCAT bus configuration (ENI file) and the actually connected slaves or wiring.

Thus the following additional use cases can be covered, without the need to change the ENI configuration file:

- Setting up a complex control system, while parts of the system are not available, powered-off or disconnected.
- Running a system that consists of mandatory as well as optional devices, e.g. in a test & measurement environment.
- Flexibility within the wiring: slaves can be connected to different ports, e.g. analogue to CAN.

In order for Hot-Connect to be used, no special EtherCAT functionality in the slave is required; in fact, any EtherCAT slave may be a member of a Hot-Connect group (HC group).
Every HC group just has to be uniquely identifiable, most often this is implemented using DIP switches.
This unique slave address then appears either in the Station Alias Register or at some address location within the slave memory.
Both methods are supported by the EC-Master.
Furthermore, the application may program the station alias address by means of the EC-Master, e.g. for first-time system initialization.

All EtherCAT activities required to support HC are automatically handled by the EC-Master in the background. There is no need for the application to interact.
Besides, as soon as a slave is connected or disconnected, the application will be informed by a call-back function (notification).
At any time the application may determine the actually connected slave devices using the appropriate EC-Master API function.

Within the HC feature pack the functionality Border Close offers additional security against connecting of slaves to an incorrect port.
By activating that function, all EtherCAT ports are closed, except the ports which are permitted by the configuration. Therefore slaves which are connected to these ports, are simply ignored and the system continues to run perfectly undisturbed.

.. figure:: ../Media/hot-connect_intro.png
        :alt:

Functionality
*************

- EtherCAT network can transferred to an operational state if optional slaves are missing.
- Operational state remains if an optional slave fails. Fail means, that the slave is driven powerless. The port of the previous slave is driven to closed loop automatically.
- Only one EtherCAT network configuration ENI for all possible slave connection combinations.
- Open/close individual ports via the application. To disconnect slaves from the bus or to allow them to participate again.

Limitations
***********

- A slave is in an undefined state if it is electrically connected but fails in such a way that it cannot be set to the operational state. The slave must then be switched off manually.
- Mandatory HC-Groups are not allowed to be connected at optional slaves.
- A slave that is not configured in the ENI is not allowed.
- A slave with an unknown Hot-Connect ID is not allowed. If such a slave is detected, the bus can be cut off at this point by the master application.
- Synchronization with Distributed Clocks (DC):

  Connecting and disconnecting of slaves while DC is active is possible, but the SYNC signals are not absolute synchronous until the propagation delay measurement and compensation is finished. 
  
  Technical background information: 
    Each slave adds a small propagation of approximately one microsecond.  In case of adding a new slave between to DC slaves this results in a shift of the SYNC signals.
