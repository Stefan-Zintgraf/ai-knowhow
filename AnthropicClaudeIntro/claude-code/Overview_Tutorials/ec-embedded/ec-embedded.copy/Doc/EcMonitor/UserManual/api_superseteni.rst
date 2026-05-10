*************************
Configuration adjustments
*************************

The Configuration adjustments allows to adapt the configuration without generating a new ENI file. The base ENI file contains a superset of all the possible connected slaves. Possible use cases are:

Optional Slaves
  ENI contains several optional slaves that can be excluded depending on their presence.
  
Alternative Slaves
  ENI contains several different alternatives for a slave at a certain position.

According to the use case the application can exclude slaves from this superset.

emonConfigLoad
**************

.. doxygenfunction:: emonConfigLoad

.. cpp:alias:: EC_T_CNF_TYPE
    :maxdepth: 0
    
emonConfigExcludeSlave
**********************

.. doxygenfunction:: emonConfigExcludeSlave

emonConfigIncludeSlave
**********************

.. doxygenfunction:: emonConfigIncludeSlave

emonConfigSetPreviousPort
*************************

.. doxygenfunction:: emonConfigSetPreviousPort

emonConfigApply
***************

.. doxygenfunction:: emonConfigApply