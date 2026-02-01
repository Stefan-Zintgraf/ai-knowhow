************
Code example
************

The example program EcMasterDemoDc demonstrates, in contrast to EcMasterDemo, how to programmatically configure DCM parameters and how the application can generate the DCM log.

.. dropdown:: **DCM Configuration (optional)**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassA\dcm_example.h
        :start-after: DocumentationSnippetsDcmConfigurationExample
        :end-before: DocumentationSnippetsDcmConfigurationExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emDcConfigure`
.. seealso:: :cpp:func:`emDcmConfigure`

.. dropdown:: **DCM Log (optional)**

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassA\dcm_example.h
        :start-after: DocumentationSnippetsDcmLogExample
        :end-before: DocumentationSnippetsDcmLogExample
        :language: cpp
        :dedent: 4
        :lines: 1-

.. seealso:: :cpp:func:`emDcmGetLog`
