*********
Diagnosis
*********

EtherCAT offers comprehensive diagnostic capabilities at both hardware and software levels. Errors that can impact a network can be classified into two main categories:

Hardware errors
	#. Interruptions in the physical medium or unexpected changes in network topology, resulting in frames not reaching all network slaves or failing to return to the master. Examples include damaged cables, loose contacts, or slave resets during operation.
	#. All slaves are reached by frames, but the correct bit sequence is corrupted. Caused by factors such as electromagnetic disturbances or faulty devices.

Software errors
	#. Incorrect or mismatched parameters sent by the master during the start-up phase, failing to meet slave expectations. This may include errors in process data size/configuration or unsupported cycle times.
	#. Previously error-free slaves detecting issues during operation, such as synchronization loss or watchdog expiration.

These errors can be diagnosed cyclically or acyclically.

Working Counter
***************

Every datagram within an EtherCAT frame ends with a 16-bit Working Counter (WKC), which increments for each slave that the datagram addresses.

.. figure:: ../Media/Diag_EcDatagramWkc.png
    :align: center
    :alt:

The Working Counter is always received by the |Product| together with the corresponding datagram, and enables therefore an immediate reaction in case of invalid or inconsistent data.
The information regarding the Working Counter is essentially digital (*WKC correct* vs. *WKC invalid*), and does not differentiate between various error causes. An invalid WKC can result from several situations:

- One or more slaves are not physically connected to the network, or they are not reached by the frames.
- One or more slaves have been reset.
- One or more slaves are not in the Operational state.

If a datagram returns to the |Product| with an unexpected WKC, the |Product| discards the input data carried by that datagram. The application will be informed by an :ref:`notification:emonNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` notification.

In addition to notification, it is also possible to evaluate the WKC states of the individual slaves and their process data sections. The following example demonstrates how to evaluate the WKC state of the slave inputs:

.. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, Diag_WkcState)
    :end-before: IGNORE_TEST(DocumentationSnippets, Diag_WkcState)
    :language: cpp
    :dedent: 4
    :lines: 2-

.. seealso:: :cpp:func:`emonGetDiagnosisImagePtr`, :cpp:func:`emonGetCfgSlaveInfo`

Master Sync Units
*****************

EtherCAT configurators can optionally group network slaves into disjoint subsets called Master Sync Units. Slaves in different Master Sync Units are served by separate datagrams and are thus independent from each other in terms of Working Counter diagnostics.

The following example demonstrates how to evaluate the WKC state of the Master Sync Unit 0:

.. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, Diag_MsuWkcState)
    :end-before: IGNORE_TEST(DocumentationSnippets, Diag_MsuWkcState)
    :language: cpp
    :dedent: 4
    :lines: 2-

.. seealso:: :cpp:func:`emonGetDiagnosisImagePtr`, :cpp:func:`emonGetMasterSyncUnitInfo`

.. 
    Hardware diagnosis
    ******************

	Software diagnosis
	******************