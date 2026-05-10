***
FAQ
***

Can the library be used without EC-Master?
    Yes, in that case the all callbacks must be implemented without using EC-Master.

Will the file be closed after calling :cpp:func:`ecDaqRecStop`?
    No, the file will be closed after deleting the recorder instance by calling :cpp:func:`ecDaqRecDelete`.

What does happen if internal buffer is too small?
    The library will report an error with the logger and the message will be deleted.

    The buffer can be increased by changing :cpp:member:`EC_T_DAQ_REC_PARMS::dwThreadMaxPendingDataSets` (default: 1000).

    If this doesn’t help, maybe the recorder threads needs to run on higher priority :cpp:member:`EC_T_DAQ_REC_PARMS::dwThreadPrio`.