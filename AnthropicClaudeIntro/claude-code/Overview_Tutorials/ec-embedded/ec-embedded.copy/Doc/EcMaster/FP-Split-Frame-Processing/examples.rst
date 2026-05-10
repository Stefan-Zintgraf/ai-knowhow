************
Example code
************

Configuration
*************

Enable split frame processing.

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-Split-Frame-Processing\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_IoControl
    :end-before: IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_IoControl
    :dedent: 4

Only in interrupt mode! Register RX callback function (see also EcMasterDemoSyncSm)

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-Split-Frame-Processing\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_Interrupt
    :end-before: IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_Interrupt
    :dedent: 4

.. raw:: latex

    \newpage

Job Task
********

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-Split-Frame-Processing\examples.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, SplitFrame_JobTask)
    :end-before: IGNORE_TEST(DocumentationSnippets, SplitFrame_JobTask)
    :dedent: 4
    :lines: 2-

.. seealso:: EcMasterDemo for polling or EcMasterDemoSyncSm for interrupt mode.