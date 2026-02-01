****************************************
Real-time Ethernet Driver initialization
****************************************

The different Real-time Ethernet Driver modules are selected and parameterized by a Real-time Ethernet Driver specific structure. Each Real-time Ethernet Driver specific structure start with a common :cpp:struct:`EC_T_LINK_PARMS` structure, followed by some Real-time Ethernet Driver specific members. The common link parameter structure is passed to :cpp:member:`EC_T_INIT_MASTER_PARMS::pLinkParms` with the call of :cpp:func:`emInitMaster` like in the following example:

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\emll_init.h
        :start-after: IGNORE_TEST(DocumentationSnippets, Init_SockRawLinkParms)
        :end-before: IGNORE_TEST(DocumentationSnippets, Init_SockRawLinkParms)
        :language: cpp
        :dedent: 4
        :lines: 4-

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
