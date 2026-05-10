************
Architecture
************

The EC-Monitor Software Development Kit (SDK) offers the possibility for Data Tracing / Listening / Sniffing / Logging Diagnosis and Monitoring of EtherCAT® Networks. It's suitable for new (Greenfield) and existing (Brownfield) installations. Also it's independent from EtherCAT® Master Controller Software and Hardware.

EC-Monitor is implemented in C++ and can be easily ported to any embedded OS platforms using an appropriate C++ compiler. The API interfaces are C language interfaces, thus the EC-Monitor can be used in ANSI-C as well as in C++ environments.

The EC-Monitor is divided into modules, see diagram and descriptions below:

.. figure:: ../Media/EC-Monitor_Architecture.png
    :align: center
    :alt:       

EC-Monitor Library:
    In the core module cyclic (process data update) and acyclic (mailbox) EtherCAT® commands are received and processed.
Configuration Layer:
    The EC-Monitor is configured using a XML file whose format is fixed in the EtherCAT® specification ETG.2100. EC-Monitor contains an OS independent XML parser.
OS Abstraction Layer: 
    All OS dependent system calls are encapsulated in a small OS layer. Most functions are that easy that they can be implemented using simple C macros.
Real-time Ethernet Driver Layer:
    This driver receives Ethernet frames from the TAP devices.

EtherCAT® Network Configuration (ENI)
*************************************

The EC-Monitor has to know about the EtherCAT® bus topology and the cyclic/acyclic frames which are exchanged by the third party EtherCAT® master with the slaves. This configuration is determined in a configuration file which has to be available in the EtherCAT® Network Information Format (ENI). This format is completely independent from EtherCAT® slave vendors, from EtherCAT® master vendors and from EtherCAT® configuration tools. Thus inter-operability between those vendors is guaranteed.

Operating system configuration
******************************

The main task is to setup the operating system to support the appropriate network adapter for EtherCAT® usage and for some systems real-time configuration may be needed.

The operating system-specific settings and configurations are described in :ref:`os:Platform and Operating Systems (OS)`.