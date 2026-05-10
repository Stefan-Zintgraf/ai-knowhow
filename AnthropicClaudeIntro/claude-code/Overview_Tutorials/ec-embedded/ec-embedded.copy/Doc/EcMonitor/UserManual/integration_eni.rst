***********************************
EtherCAT® Network Configuration ENI
***********************************

The EtherCAT® configuration file ENI contains one or more `Cyclic` entries for reading new input data values and output data values (process data update).
These entries contain one or more frames, so-called cyclic frames, which are to be sent cyclically by the EtherCAT® master.
Within the cyclic frames are one or more EtherCAT® datagrams that contain logical read/write commands for accessing the process data values.

Single cyclic entry configuration
*********************************

In the simplest case, there is only a single cyclic entry with one or more cyclic frames.

.. figure:: ../Media/Eni_SingleCycEntry.png
    :align:     center
    :alt:

Multiple cyclic entries configuration
*************************************

For more complex scenarios it is possible to configure the system using multiple cyclic entries with one or more cyclic frames for each cyclic entry.

.. figure:: ../Media/ENI_MultipleCycEntry.png
    :align:     center
    :alt:

.. 
    Copy Information for Slave-to-Slave communication
    =================================================

    It is possible to configure the system to copy input variables to output variables within EC-Master.
    The copy info declarations of the corresponding received cyclic frame are processed in :cpp:expr:`emonExecJob(eUsrJob_ProcessAllRxFrames)`.

    The exchange of process data takes two communication cycles. The duration is necessary if cable redundancy is used or if the WKC of INPUT needs to be checked before changing OUTPUT.

    The copy info declarations are located at ``/EtherCATConfig/Config/Cyclic/Frame/Cmd/CopyInfos`` in the ENI file.

    .. seealso::
        - :ref:`software-integration:Cyclic cmd WKC validation`
        - CopyInfosType in ETG.2100

    **Configuration with EC-Engineer**

    #. In the "Slave to Slave" tab of the Master select Input and Output Variable and connect them:
        .. figure:: ../Media/configengineer.png
            :align:     center
            :alt:

    **Configuration with ET9000**

    #. Select "Linked to..." from the Output Variable:
        .. figure:: ../Media/configet9000.png
            :align:     center
            :alt:

    #. Select Input Variable to be attached to the Output Variable:
        .. figure:: ../Media/outputvariable.png
            :align:     center
            :alt:

    .. hint:: Copy info declaration processing is independent of WKC values, but updating the INPUT source depends on successful Cyclic cmd WKC validation.

    Swap variables' bytes according to ENI
    ======================================

    The following screenshot (ET9000) shows how to configure variables to be swapped by the EC-Master:

    .. figure:: ../Media/swapENI.png
        :align:     center
        :alt:

    .. hint:: The EC-Master does not distinguish between WORD or BYTE swapping. Setting any PDO swap flag instructs the EC-Master to swap the PDO variable.

    The swap declarations are located at DataType's attribute SwapData of RxPdo or TxPdo, e.g. ``/EtherCATConfig/Config/Slave/ProcessData/RxPdo/Entry/DataType`` in the ENI file.