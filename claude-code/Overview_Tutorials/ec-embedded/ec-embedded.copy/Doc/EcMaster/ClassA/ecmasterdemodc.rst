**********************
Running EcMasterDemoDc
**********************

The EcMasterDemoDc is available "out of the box" for different operating systems. It is an EC-Master example application that handles the following tasks:

- Showing basic EtherCAT communication
- Master stack initialization into OPERATIONAL state
- DC and DCM configuration
- Process Data operations for e.g. Beckhoff EL2004, EL1004 and EL4132
- Periodic diagnosis task 
- Periodic Job Task in polling mode 
- Logging

Start the EcMasterDemoDc from the command line to put the EtherCAT network into operation. At least an Real-time Ethernet Driver must be specified.

.. prompt:: text >
  
  EcMasterDemoDc -ndis 192.168.157.2 1 -f eni.xml -t 0 -v 3 -dcmmode busshift

.. program:: EcMasterDemoDc
.. include:: ../../Examples/ecdemo-cmdline.rst