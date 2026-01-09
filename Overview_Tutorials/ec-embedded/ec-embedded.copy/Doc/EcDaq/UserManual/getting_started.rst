***************
Getting Started
***************

Running EcMasterDemoDaq
***********************

The EcMasterDemoDaq is available "out of the box" for different
operating systems. It is an EC-Master example application that handles
the following tasks:

- Showing basic EtherCAT communication

- Master stack initialization into OPERATIONAL state

- Process Data operations for e.g. Beckhoff EL2004, EL1004 and EL4132

- Periodic diagnosis task

- Periodic Job Task in polling mode

- Logging

- Record data

Start the EcMasterDemoDaq from the command line to put the EtherCAT
network into operation. At least a Real-time Ethernet Driver must be
specified.

.. prompt:: bash

    EcMasterDemoDaq -ndis 192.168.157.2 1 -f eni.xml -t 0 -v 3 -daqrec Recorder.xml

.. include:: ../../Examples/ecdemo-cmdline.rst
