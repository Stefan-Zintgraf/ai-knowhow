***********
Error Codes
***********

Groups
******

+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| **No.**   | **Group**                                   | **Abbr.**             | **Description**                                                                                |
+===========+=============================================+=======================+================================================================================================+
| 1         | Application Error                           | APP                   | Error within application, running the simulator                                                |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. API function call with invalid parameters                                                 |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 2         | EtherCAT network information file problem   | ENI                   | Network configuration XML file error                                                           |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. malformed or empty EtherCAT Network configuration file                                    |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 3         | Simulator parameter configuration           | CFG                   | Simulator configuration parameters erroneous                                                   |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. mailbox command queue not large enough                                                    |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 4         | Bus/Slave Error                             | SLV                   | Slave error                                                                                    |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. Working Counter Error                                                                     |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 5         | Real-time Ethernet Driver                   | LLA                   | Real-time Ethernet Driver error (network interface driver)                                     |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. Intel Pro/1000 NIC could not be found                                                     |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 6         | Remote API                                  | RAS                   | Remote API error                                                                               |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. connection to Remote API server is not possible from client                               |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 7         | Internal software error                     | ISW                   | Simulator internal error                                                                       |
|           |                                             |                       |                                                                                                |
|           |                                             |                       | E.g. Simulator state machine in undefined state                                                |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 8         | DC Master Sync                              | DCM                   | DC slave and host time synchronization                                                         |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 9         | Pass-Through-Server                         | PTS                   | Initialization/De-Initialization errors                                                        |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+
| 10        | System Setup                                | SYS                   | Errors from Operating System or obviously due to System Setup                                  |
+-----------+---------------------------------------------+-----------------------+------------------------------------------------------------------------------------------------+

Generic Error Codes
*******************

.. datatemplate:xml:: EC_ERROR_CODES_GENERIC
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

DCM Error Codes
***************

.. datatemplate:xml:: EC_ERROR_CODES_DCM
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage

ADS over EtherCAT (AoE) Error Codes
***********************************

.. datatemplate:xml:: EC_ERROR_CODES_AOE
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage

CAN application protocol over EtherCAT (CoE) SDO Error Codes
************************************************************

.. datatemplate:xml:: EC_ERROR_CODES_COE
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage

File Transfer over EtherCAT (FoE) Error Codes
*********************************************

.. datatemplate:xml:: EC_ERROR_CODES_FOE
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage

Servo Drive Profil over EtherCAT (SoE) Error Codes
**************************************************

.. datatemplate:xml:: EC_ERROR_CODES_SOE
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage

Remote API Error Codes
**********************

.. datatemplate:xml:: EC_ERROR_CODES_RAS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. raw:: latex

    \newpage
