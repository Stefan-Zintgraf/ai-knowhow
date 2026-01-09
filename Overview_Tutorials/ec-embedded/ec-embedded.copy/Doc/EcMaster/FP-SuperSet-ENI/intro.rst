************
Introduction
************

The Superset ENI functionality allows the user to adapt the configuration without generating a new ENI file. The base ENI file contains a superset of all the possible connected slaves. According to the use case the application can exclude slaves from this superset.

Optional Slaves
***************

A possible use case of Superset ENI is that a configuration contains several optional slaves that can be excluded depending on their presence.

The following figure shows a simple network configuration:
    .. figure:: ../Media/SupersetENI_OptSlaves.png
        :alt:
    
If Slave 1002 and Slave 1004 are not present, the bus mismatches:
    .. figure:: ../Media/SupersetENI_OptSlaves-Missing1002-1004.png
        :alt:
    
The following source code removes the missing Slaves from the configuration after loading the ENI file, so the resulting topology validates:

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-SuperSet-ENI\intro.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigExcludeSlave)
    :end-before: IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigExcludeSlave)
    :dedent: 4
    :lines: 2-


Resulting topology:
    .. figure:: ../Media/SupersetENI_OptSlaves-Result.png
        :alt:
    
Alternative Slaves
******************

Another use case of Superset ENI would be that a configuration contains several different alternatives for a slave at a certain position.

The following network includes one slave which may be of different types:
    .. figure:: ../Media/SupersetENI_AltSlaves.png
        :alt:
    
To realize this, an ENI containing all possible slave definitions is needed, e.g. the two Slaves 9001 and 9002:
    .. figure:: ../Media/SupersetENI_AltSlaves-9001or9002.png
        :alt:

The following source code first removes all alternatives from the configuration after loading the ENI file and then include one of the alternative slaves so that the resulting topology is valid:

.. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\FP-SuperSet-ENI\intro.h
    :language: cpp
    :start-after: IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigIncludeSlave)
    :end-before: IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigIncludeSlave)
    :dedent: 4
    :lines: 2-


Resulting topology:
    .. figure:: ../Media/SupersetENI_AltSlaves-Result.png
        :alt:
    