****************
Master Variables
****************

Master variables are a EC-Master extension that allows applications to trace data in real time on the network. To ensure real-time transmission, it is implemented as part of the cyclic process data. They are placed behind the slave output data in the output area of the process data image of the EtherCAT application. The Master variables can be configured via the ENI with the help of the EC-Engineer.

Master variables can be captured with a network monitoring tool like Wireshark.

.. figure:: ../../EcMaster/Media/TraceData_Architecture.png
    :align: center
    :alt:

To transfer the data, an additional NOP command is appended to the end of the cyclic EtherCAT frame. The NOP command has ADP 0 and ADO 0x4154. The EC-Master automatically fills the data area of the NOP command with the current master variables when sending cyclic frames. Since the master variables are transferred to the network as NOP command, they are not evaluated by any ESC. Therefore, the WKC of the master variables remains 0 and the application cannot validate the data.

The easiest and most comfortable way to create master variables is with the help of the EC-Engineer.
The necessary NOP command and the process data variables are automatically created and exported to the ENI. The process variables can be accessed as usual using the :cpp:func:`emonFindOutpVarByNameEx` function.

