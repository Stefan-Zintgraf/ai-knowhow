*****************
EtherCAT® Masters
*****************

In principle, all EtherCAT® masters with ENI are supported. EtherCAT® masters without ENI are currently not supported.

All tested EtherCAT® masters are listed below, as well as special EC-Monitor parameters that are necessary for operation.

Acontis EC-Master
*****************

Fully supported without any special parameter settings.

Beckhoff TwinCAT®
*****************

Fully supported without any special parameter settings.

CODESYS®
********

Supported starting from version V3.5 SP17 and above, with the CODESYS EtherCAT Module requiring version 4.2.0.0 or later.
In some topologies, the actual number of cyclical commands on the bus differs from the configuration in the ENI. To fix this discrepancy, the EC-Monitor parameter :cpp:member:`EC_T_MONITOR_INIT_PARMS::bProcessRestructuredCyclicCmds` must be set to :c:macro:`EC_TRUE`.

KPA EtherCAT® Master
********************

Supported.