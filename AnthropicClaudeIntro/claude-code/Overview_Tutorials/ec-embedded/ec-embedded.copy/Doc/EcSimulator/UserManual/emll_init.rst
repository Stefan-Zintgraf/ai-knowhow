****************************************
Real-time Ethernet Driver initialization
****************************************

The different Real-time Ethernet Driver modules are selected and parameterized by a Real-time Ethernet Driver specific structure.

The size of the Real-time Ethernet Driver parameter structure depends on the adapter type. 
All Real-time Ethernet Driver parameter structures start with :cpp:struct:`EC_T_LINK_PARMS` followed by adapter type specific parameters.
The linkParms.dwSize must be set to sizeof(EC_T_LINK_PARMS_INTELGBE) or the used structure respectively. It may not be 0.
The following example shows how to pass Real-time Ethernet Driver parameters to |EcatInitStack|:

.. only:: EcSimulatorHiL
  
    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\software-integration.h
        :start-after: DocumentationSnippetsSimulatorHilRtEthInitExample
        :end-before: DocumentationSnippetsSimulatorHilRtEthInitExample
        :language: cpp
        :dedent: 4

.. only:: EcSimulatorSiL
    
    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\software-integration.h
        :start-after: DocumentationSnippetsSimulatorSilRtEthInitExample
        :end-before: DocumentationSnippetsSimulatorSilRtEthInitExample
        :language: cpp
        :dedent: 4

.. doxygenstruct:: EC_T_LINK_PARMS
    :members:

.. doxygenenum:: EC_T_LINKMODE

.. doxygenstruct:: EC_T_LINKLAYER_TIMINGTASK
    :members:

.. doxygenenum:: EC_T_LINKLAYER_TIMING

.. doxygenenum:: EC_T_PHYINTERFACE


Real-time Ethernet Driver instance selection via PCI location
*************************************************************

For some operating systems it is possible to address the Real-time Ethernet Driver instance using its PCI address as an alternative. To do this, EC_LINKUNIT_PCILOCATION (0x01000000) and the PCI location must be set as :cpp:member:`EC_T_LINK_PARMS::dwInstance`.

On Linux the PCI address  can be shown using e.g.:

.. prompt:: bash

    lspci | grep Ethernet

.. prompt:: bash

    00:19.0 Ethernet controller: Intel Corporation Ethernet Connection I217-LM (rev 04)
    04:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection
    05:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection

The format of :cpp:member:`EC_T_LINK_PARMS::dwInstance` using PCI bus address is:

`0x01bbddff`
    - `bb` Bus Number
    - `dd` Device Number
    - `ff` Function Number

.. code-block:: cpp

    EC_T_LINK_PARMS::dwInstance = 0x01001900; //"0000:00:19.0"

On Windows the integer value displayed in properties dialog must be converted to HEX. E.g the number from the following dialog `(PCI bus 11, device 0, function 0)` corresponds to `0x010B0000` (bus `0x0B`).

.. figure:: ../Media/Intel82574L.png
    :alt: 
