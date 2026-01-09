****************************
Master synchronization (DCM)
****************************

Applications like motion control need process update every cycle in real time and it is unacceptable to miss data of a cycle or that the slaves handle the same process data values twice within a cycle.

The Distributed Clocks Master Synchronization (DCM) provides controller mechanisms to synchronize the timing at the master to the SYNC pulses triggering the slave firmware.
With DCM, the process data update at the master and the slaves is in correlated timely behavior.

Features:

- PI drift controller
- Automatic timer adjustment error determination (I controller)

.. toctree::
    :hidden:

    dcm_technical.rst
    dcm_config.rst
    dcm_api.rst
    dcm_example.rst