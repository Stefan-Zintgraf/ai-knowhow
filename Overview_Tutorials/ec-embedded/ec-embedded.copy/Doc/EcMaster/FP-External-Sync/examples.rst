********
Examples
********

Configuration
*************

The following example code demonstrates the DCX external synchronization configuration of the secondary segment. To configure the primary segment in DCM Mastershift mode, see document EC-Master ClassA.

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-External-Sync\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, ExternalSync_Config)
    :end-before: IGNORE_TEST(DocumentationSnippets, ExternalSync_Config)
    :lines: 2-

EcMasterDemoDc
**************

The external synchronization feature is also included in the demo application *EcMasterDemoDc*.

*EcMasterDemoDc* must run on the primary and secondary EtherCAT segments with different DCM configurations:

Primary
    ``–dcmmode mastershift``

Secondary
    ``-dcmmode dcx``

To start the demo the full path and file name of the configuration file has to be given as a 
command line parameter as well as the appropriate Real-time Ethernet Driver.

Example primary segment:

.. prompt:: text >

    EcMasterDemoDc –intelgbe 1 1 –f PrimaryENI.xml –dcmmode mastershift

Example secondary segment:

.. prompt:: text >
    
    EcMasterDemoDc –intelgbe 1 1 –f SecondaryENI.xml –dcmmode dcx
