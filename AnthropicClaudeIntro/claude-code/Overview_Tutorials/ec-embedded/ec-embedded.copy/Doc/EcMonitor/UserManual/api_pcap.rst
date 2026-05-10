**************
Packet Capture
**************

emonOpenPacketCapture
*********************

.. doxygenfunction:: emonOpenPacketCapture

.. doxygenstruct:: EC_T_PACKETCAPTURE_PARMS
    :members:

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMonitorSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, emonOpenPacketCapture)
        :end-before: IGNORE_TEST(DocumentationSnippets, emonOpenPacketCapture)
        :dedent: 4
        :lines: 2-

emonClosePacketCapture
**********************

.. doxygenfunction:: emonClosePacketCapture

emonGetPacketCaptureInfo
************************

.. doxygenfunction:: emonGetPacketCaptureInfo

.. doxygenstruct:: EC_T_PACKETCAPTURE_INFO
    :members:

.. doxygenenum:: EC_T_PACKETCAPTURE_STATUS

emonStartLivePacketCapture
**************************

.. doxygenfunction:: emonStartLivePacketCapture

emonStopLivePacketCapture
*************************

.. doxygenfunction:: emonStopLivePacketCapture

emonBacktracePacketCapture
**************************

.. doxygenfunction:: emonBacktracePacketCapture

.. seealso:: :cpp:func:`emonInitMonitor`