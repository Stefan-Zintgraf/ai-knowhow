********************************************
Synchronization with Distributed Clocks (DC)
********************************************

DC clock synchronization enables all EtherCAT devices (master and slaves) to share the same EtherCAT System Time.

A "DC-slave" is defined as slave who shall be synchronized by means of distributed clocks.
During network start-up several steps have to be performed by the EC-Master to set-up a consistent time base in all DC-slaves: 

- Initial propagation delay measurement and compensation (ETG.8000)
- Offset compensation (ETG.8000)
- Set start time (ETG.8000)
- After network start-up: continuous drift compensation (ETG.8000)
- The Master must synchronize itself on the reference clock (ETG.1020) -> DCM

Reference:

- ETG.1000.3 and ETG.1000.4
- ETG.1020 -> Synchronization
- ETG.8000 -> Distributed Clocks

.. toctree::
    :hidden:
    
    dc_technical.rst
    dc_config.rst
    dc_api.rst