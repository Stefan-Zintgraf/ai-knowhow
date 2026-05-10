********************
Raw command transfer
********************

emTferSingleRawCmd
******************

.. doxygenfunction:: ecatTferSingleRawCmd
    :outline:

.. doxygenfunction:: emTferSingleRawCmd

The following EtherCAT commands are supported:

- :c:enum:`eRawCmd_APRD`	Auto Increment Physical Read (avoid to use, see below)
- :c:enum:`eRawCmd_APWR`	Auto Increment Physical Write (avoid to use, see below)
- :c:enum:`eRawCmd_APRW`	Auto Increment Physical Read/Write (avoid to use, see below)
- :c:enum:`eRawCmd_FPRD`	Fixed addressed Physical Read
- :c:enum:`eRawCmd_FPWR`	Fixed addressed Physical Write
- :c:enum:`eRawCmd_FPRW`	Fixed addressed Physical Read/Write
- :c:enum:`eRawCmd_BRD`	Broadcast (wire or'ed) Read
- :c:enum:`eRawCmd_BWR`	Broadcast Write
- :c:enum:`eRawCmd_BRW`	Broadcast Read/Write
- :c:enum:`eRawCmd_LRD`	Logical Read 
- :c:enum:`eRawCmd_LWR`	Logical Write
- :c:enum:`eRawCmd_LRW`	Logical Read/Write
- :c:enum:`eRawCmd_ARMW`	Auto Increment Physical Read, multiple Write


emClntSendRawMbx
*****************

.. doxygenfunction:: ecatClntSendRawMbx
    :outline:

.. doxygenfunction:: emClntSendRawMbx

emClntQueueRawCmd
*****************

.. doxygenfunction:: ecatClntQueueRawCmd
    :outline:

.. doxygenfunction:: emClntQueueRawCmd

The following EtherCAT commands are supported:

.. doxygenenum:: EC_T_RAWCMD

emQueueRawCmd
*************

.. doxygenfunction:: ecatQueueRawCmd
    :outline:

.. doxygenfunction:: emQueueRawCmd

.. seealso:: :cpp:func:`emClntQueueRawCmd`

emNotify - EC_NOTIFY_RAWCMD_DONE
********************************

This notification is given when the response to an :cpp:func:`emTferSingleRawCmd` or :cpp:func:`emClntQueueRawCmd` is received.

.. emNotify:: EC_NOTIFY_RAWCMD_DONE
    :pbyInBuf: Pointer to EC_T_RAWCMDRESPONSE_NTFY_DESC
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    
.. doxygenstruct:: EC_T_RAWCMDRESPONSE_NTFY_DESC
    :members:
    


