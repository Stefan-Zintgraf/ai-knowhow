***************
Getting Started
***************

EC-Master Architecture
**********************

The EC-Master EtherCAT Master Stack is implemented in C++ and can be easily ported to any embedded OS platforms using an appropriate C++ compiler. The API interfaces are C language interfaces, thus the master can be used in ANSI-C as well as in C++ environments.

The Master Stack is divided into modules, see diagram and descriptions below:

.. figure:: ../Media/EC_Master_Architecture.png
    :align:     center
    :alt:       

- EtherCAT Master Core:  In the core module cyclic (process data update) and acyclic (mailbox) EtherCAT commands are sent and received. Among others there exist some state machines to handle for example the mailbox protocols.
- Configuration Layer: The EtherCAT master is configured using a XML file whose format is fixed in the EtherCAT specification ETG.2100. EC-Master contains an OS independent XML parser.
- Real-time Ethernet Driver Layer: This layer exchanges Ethernet frames between the master and the slave devices. If hard real-time requirements exist, this layer has to be optimized for the network adapter card in use.
- OS Layer: All OS dependent system calls are encapsulated in a small OS layer. Most functions are that easy that they can be implemented using simple C macros.

EtherCAT Network Configuration (ENI)
************************************

The EtherCAT master has to know about the EtherCAT bus topology and the cyclic/acyclic frames to exchange with the slaves. 
This configuration is determined in a configuration file which has to be available in the EtherCAT Network Information Format (ENI). 
This format is completely independent from EtherCAT slave vendors, from EtherCAT master vendors and from EtherCAT configuration tools. Thus interoperability between those vendors is guaranteed.

Additionally some static configuration parameters have to be defined like the identification of the network adapter card to use, the priority of the EtherCAT master timer task etc.

Operating system configuration
******************************

The main task is to setup the operating system to support the appropriate network adapter for EtherCAT usage and for some systems real-time configuration may be needed.

The operating system-specific settings and configurations are described in :ref:`toc_os:Platform and Operating Systems (OS)`.

.. _running-ecdemo:

Running EcMasterDemo
********************

The EcMasterDemo is available "out of the box" for different operating systems. It is an EC-Master example application that handles the following tasks:

- Showing basic EtherCAT communication
- Master stack initialization into OPERATIONAL state
- Process Data operations for e.g. Beckhoff EL2004, EL1004 and EL4132
- Periodic diagnosis task 
- Periodic Job Task in polling mode 
- Logging

Start the EcMasterDemo from the command line to put the EtherCAT network into operation. At least a Real-time Ethernet Driver must be specified.

.. prompt:: text >
  
  EcMasterDemo -ndis 192.168.157.2 1 -f eni.xml -t 0 -v 3

.. seealso:: 
    - :ref:`software-integration:Example application` for detailed explanation

.. program:: EcMasterDemo
.. include:: ../../Examples/ecdemo-cmdline.rst
.. include:: ../../Examples/ecdemo-cmdline-emll.rst

.. _compile-ecdemo:

Compiling the EcMasterDemo
**************************

The following main rules can be used to generate the example applications for all operating systems.

- :file:`<OS>` is a placeholder for the operating system used.
- :file:`<ARCH>` for the architecture. If different architectures are supported.

EtherCAT Master Software Development Kit (SDK)
==============================================

The EtherCAT master development kit is needed to write applications based on the master stack. 
The master stack is shipped as a library which is linked together with the application.

The following components are supplied together with an SDK:
    .. code-block::
        
        <InstallPath>/Bin
        <InstallPath>/Doc
        <InstallPath>/SDK
        <InstallPath>/SDK/INC
        <InstallPath>/SDK/LIB
        <InstallPath>/SDK/FILES
        <InstallPath>/Sources/Common

:file:`/Bin`
    Executables containing the master stack
:file:`/Doc`
    Documentation
:file:`/Examples`
    One or more example applications using a predefined EtherCAT-configuration. It is easily adaptable to different configurations using an appropriate EtherCAT configuration XML file.
:file:`/SDK`
    EtherCAT Software Development Kit containing libraries and header files to build C/C++-applications.
:file:`/SDK/INC`:
    Header files to be included with the application
:file:`/SDK/LIB`:
    Libraries to be linked with the application
:file:`/SDK/FILES`:
    Additional files for platform integration (e.g. Windows CE registry files)
:file:`/Sources/Common`:
    Shared .cpp-files

Include search path
===================

The header files are located in the following directories:
    .. code-block::

        <InstallPath>/SDK/INC
        <InstallPath>/SDK/INC/<OS>/<ARCH>
        <InstallPath>/Sources/Common

Libraries
=========

The libraries located in the following directories:
    .. code-block::
    
        <InstallPath>/SDK/LIB/<OS>/<ARCH>