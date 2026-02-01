******************
Technical overview
******************

The ENI file contains predefined DCM configuration settings. 
For example, the EC-Master selects the DCM Mode Bus Shift or DCM Mode Master Shift based on the values specified in the ENI file. 
Therefore, the application does not need to activate DCM explicitly via API. 
However, some settings can still be modified programmatically after loading the ENI file. 
For instance, the parameter "Controller set value" sets the position of the SYNC signals at the slaves in relation to the cyclic frame:

.. figure:: ../Media/DCM_Topologie.png
    :align:     center
    :alt:   

The parameter "Controller set value" (nCtlSetVal) cannot be derived from the ENI file. It is one of the parameters that can be set using emDcmConfigure().

The actual position of the SYNC signals at the slaves, relative to the cyclic frame, typically varies from cycle to cycle due to jitter in the application's JobTask.

The example program EcMasterDemoDc demonstrates, in contrast to EcMasterDemo, how to programmatically configure DCM parameters and how the application can generate the DCM log.

The EtherCAT technology provides sufficient diagnostic capabilities through WKC monitoring to detect communication issues.
However, for in-depth analysis, more detailed information, such as the DCM log, is required.
The DCM log can be used to evaluate drift control quality and measure jitter values.
To enable this, the application's JobTask must cyclically retrieve the DCM status from the master.
This data should be written from a low-priority thread to avoid impacting real-time performance during diagnostics.

DCM Modes
*********

The following DCM Modes are available:

+-------------------+---------------------------------------------------------+
| Name              | Purpose                                                 |
+===================+=========================================================+
| BusShift          | Synchronize slaves to master timer (Default)            |
+-------------------+---------------------------------------------------------+
| MasterShift       | Synchronize master timer to slave. Feasibility          |
|                   | depending on target HW and SW.                          |
+-------------------+---------------------------------------------------------+
| LinkLayerRefClock | Bus Shift using Link Layer clock. Special HW needed.    |
+-------------------+---------------------------------------------------------+
| MasterRefClock    | Bus Shift excluding reference clock controlling.        |
|                   | Lowers CPU usages, but very high timer accuracy needed. |
+-------------------+---------------------------------------------------------+
| DCX               | Synchronization of two or more EtherCAT segments by a   |
|                   | a bridge device. Only available with Feature Pack       |
|                   | External Synchronization.                               |
+-------------------+---------------------------------------------------------+

The Distributed Clocks Master Synchronization (DCM) in Bus Shift mode adjusts the bus time register of the DC reference clock. All DC slaves converge to this time. 
This mode is useful to synchronize multiple EtherCAT networks or if it is not possible to adjust the timing of the Master.

.. seealso:: :cpp:func:`emDcmConfigure`


Sync signal activation
**********************

The sync signals are activated during transition PREOP - SAFEOP according to Init Command (Ado 0x0980, 0x0990, 0x09A0, 0x09A8).

DCM in sync
***********

DCM in sync means that the synchronization between the send time of the cyclic frames and the system time of the reference clock was successful. 
 
The master awaits that DCM is in sync in Master state transition PREOP->SAFEOP. Therefore the master state transition may timeout if DCM does not get in sync.
Due to the Master's DC implementation, DCM may get in sync in transition INIT->PREOP. 

In sync is assumed if there is no error reported from the DCM controller within the settle time or if there is no DC slave connected.

Controller adjustment
*********************

To adjust the controller parameters the diagnostic values in file dcmlog0.0.csv can be used.
The generation of logging information can be enabled setting bLogEnabled to :c:macro:`EC_TRUE` with the function :cpp:func:`emDcmConfigure`.

Controller log file description:

+---------------------------+---------------------------------------------------------------------------------------+
| Column name               | Description                                                                           |
+===========================+=======================================================================================+
| Time[ms]                  | Controller execution timestamp                                                        |
+---------------------------+---------------------------------------------------------------------------------------+
| SyncSetVal [ns]           | Controller set value (distance between frame send time and SYNC0)                     |
+---------------------------+---------------------------------------------------------------------------------------+
| BusTime [ns]              | System Time                                                                           |
+---------------------------+---------------------------------------------------------------------------------------+
| BusTimeOff                | System Time modulo Sync Cycle Time                                                    |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlAdj [ns]               | Controller adjust value                                                               |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlErr [ns]               | Controller error (EC_T_DCM_SYNC_NTFY_DESC.nCtlErrorNsecCur)                           |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlErrFilt                | Filtered controller error                                                             |
+---------------------------+---------------------------------------------------------------------------------------+
| Drift [ppm]               | Drift between local clock and DC reference clock                                      |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlErr [1/10 pmil]        | For internal use only                                                                 |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlOutSum                 | For internal use only                                                                 |
+---------------------------+---------------------------------------------------------------------------------------+
| CtlOutTot                 | For internal use only                                                                 |
+---------------------------+---------------------------------------------------------------------------------------+
| DCStartTime               | DC start time send to the slaves to activate their SYNC signals                       |
+---------------------------+---------------------------------------------------------------------------------------+
| DCMErrorCode              | Current error code of the DCM controller (same value as returned by emDcmGetStatus)   |
+---------------------------+---------------------------------------------------------------------------------------+
| DCMInSync                 | Current InSync state of the DCM controller                                            |
+---------------------------+---------------------------------------------------------------------------------------+
| DCInSync                  | Current InSync state of the DC slaves                                                 |
+---------------------------+---------------------------------------------------------------------------------------+
| SystemTimeDifference [ns] | Current system time difference of the DC slave if monitoring is enabled               |
+---------------------------+---------------------------------------------------------------------------------------+

Log file analyze:
To understand how the controller values correlates the following table can help:

+-------------------+-------------------+-------------------+-------------------+
| Controller error  |   Drift           | Reference-Clock   | Output            |
+===================+===================+===================+===================+
| Positive          |   Must decrease   | Must run faster   | Double cycle time |
+-------------------+-------------------+-------------------+-------------------+
| Negative          |   Must increase   | Must run slower   | Half cycle time   |
+-------------------+-------------------+-------------------+-------------------+

The DCM Controller reacts if the controller error is positive or negative. E.g. on a positive controller error (CtlErr ) the drift is too high and has to be decreased. Therefore the controller will speed up the reference clock.

In some case the drift is too high (EcMasterDemoDc shows error messages) and cannot be balanced by the controller. This holds if the drift is higher than about 400ppm.

Diagram 1: Bus offset in nanoseconds

.. figure:: ../Media/DCM_Diagram1.png
    :align:     center
    :alt:   

Diagram 2: Drift in ppm (part per million)

.. figure:: ../Media/DCM_Diagram2.png
    :align:     center
    :alt:   

Diagram 3: Controller error in nanoseconds

.. figure:: ../Media/DCM_Diagram3.png
    :align:     center
    :alt:   

Diagram 4: Controller error in steady state in nanoseconds

.. figure:: ../Media/DCM_Diagram4.png
    :align:     center
    :alt:   

Troubleshooting:

DCM BusShift needs a very deterministic and accurate time base.

The following statements have to be true:

- The timer input frequency must be determined with an accuracy greater than 600 ppm (333333 Hz vs 333000 Hz. E.g. at 1 ms, the cycle time must be between 999.400 µs and 1000.600 µs)
- The timer frequency must never change after the application start

On a PC platform the following settings have to be disabled in the BIOS. Be sure that these settings are really applied.

- System management interrupt
- Legacy USB support
- Intel C-STATE tech
- Intel Speedstep tech
- Spread Spectrum

DCM Master Shift mode
*********************

In this mode, the local time base will be adjusted to synchronize it with the network "bus time". The following function pointers have to be implemented to enable the adjustment:

:cpp:struct:`EC_T_OS_PARMS::pfHwTimerGetInputFrequency`

:cpp:struct:`EC_T_OS_PARMS::pfHwTimerModifyInitialCount`

The master shift must not be enabled in the ENI file because it doesn't need any cyclic command. This mode can be activate using :cpp:func:`emDcmConfigure`

DCM Master Ref Clock mode
*************************

The DCM Master Ref Clock mode is similar to the bus shift mode, without its control loop. This reduces the CPU load and makes it a good alternative for low performance CPU. Because of the missing control loop, the reaction time on disturbance is longer and the cycle must be very accurate.

This mode can be activate using :cpp:func:`emDcmConfigure`

DCM Linklayer Ref Clock mode
****************************

In this mode the Real-time Ethernet Driver should provide the time base for the cyclic frames. :c:macro:`EC_LINKIOCTL_GETTIME` will be called during the DC initialization to initialize the DC related registers of the DC slaves and during the  slave transition PREOP to SAFEOP to start the DC SYNC signals if needed.

:c:macro:`EC_LINKIOCTL_GETTIME` should return the current 64 bits value in nanosecond of a time counter running continuously.

During the call to EcLinkSendFrame, the Real-time Ethernet Driver should insert the send time of the frame following the instruction given by :cpp:struct:`EC_T_LINK_FRAMEDESC::wTimestampOffset` and :cpp:struct:`EC_T_LINK_FRAMEDESC::wTimestampSize` of the parameter pLinkFrameDesc. A value of 0 means that no time stamp should be inserted.
