********
Examples
********

Server
******

Start the mailbox gateway server after calling :cpp:func:`emConfigureMaster()` and
stop prior to :cpp:func:`emDeinitMaster()`.

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-UDP-Mailbox-Gateway\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewaySrv)
    :end-before: IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewaySrv)
    :dedent: 4
    :lines: 2-

Client
******
.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-UDP-Mailbox-Gateway\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewayClient)
    :end-before: IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewayClient)
    :dedent: 4
    :lines: 2-