********************************************
Application programming interface, reference
********************************************

In interrupt mode, all incoming frames are buffered. If all frames of a specific cyclic task have been buffered, the application will be informed by the CYCFRAME_RX_CB mechanism 

.. seealso:: emIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB in EC-Master ClassB manual.
 
emIoControl - EC_IOCTL_SET_SPLIT_FRAME_PROCESSING_ENABLED
=========================================================

Enable or disable the split frame processing. Default: Disabled.

If split frame processing is enabled the master allocates several buffers to store cyclic and acyclic EtherCAT frames. The size of these buffers depends on the number of cyclic frames in the ENI and the parameter :cpp:member:`EC_T_INIT_MASTER_PARMS::dwMaxAcycFramesQueued` configured in :cpp:func:`emInitMaster`. 

The functionality should be enabled between :cpp:func:`emInitMaster` and the start of the job task.

.. emIoControl:: EC_IOCTL_SET_SPLIT_FRAME_PROCESSING_ENABLED
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: enable, EC_FALSE: disable.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emExecJob
=========
.. doxygenfunction:: emExecJob

    
Additionally to the standard jobs, the following eUserJob are defined for split frame processing:

.. doxygenenumvalue:: eUsrJob_ProcessRxFramesByTaskId

.. doxygenenumvalue:: eUsrJob_ProcessAcycRxFrames

.. doxygenenumvalue:: eUsrJob_SendCycFramesByTaskId

#. :cpp:enumerator:`eUsrJob_ProcessRxFramesByTaskId`
    When split frame processing is enabled, this call will process all currently received frames related to the specified task. This job can be called if the Ethernet Driver is configured in polling or in interrupt mode.

    .. doxygenstruct:: EC_T_USER_JOB_PARMS::_PROCESS_RXFRAME_BY_TASKID
        :members:

#. :cpp:enumerator:`eUsrJob_ProcessAcycRxFrames`
    When split frame processing is enabled, this call will process all currently received acyclic frames. This job can be called if the Ethernet Driver is configured in polling or in interrupt mode.

#. :cpp:enumerator:`eUsrJob_SendCycFramesByTaskId`
    Send cyclic frames related to a specific task id. If more than one cyclic entries are configured this user job can be used to send the appropriate cyclic frames. All frames stored in cyclic entries with the given task id will be sent.

    .. doxygenstruct:: EC_T_USER_JOB_PARMS::_SEND_CYCFRAME_BY_TASKID
        :members: