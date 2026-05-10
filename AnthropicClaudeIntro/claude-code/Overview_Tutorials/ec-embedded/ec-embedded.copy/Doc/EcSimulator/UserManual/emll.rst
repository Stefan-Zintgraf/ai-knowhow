*************************
Real-time Ethernet Driver
*************************

The |Product| stack currently supports a variety of different Real-time Ethernet Driver modules, each of which contained in a single library file, which is loaded by the core library dynamically. 
Which library actually is loaded, is depending on the Real-time Ethernet Driver parameters at runtime. 

Real-time means operating directly on the network device's register set instead of using the operating system's native driver.

The principle of the Real-time Ethernet Driver selection is that the Ethernet Driver name (Ethernet Driver identification) is used to determine the location and name of a registration function called by |Product| and registers function pointers that allow access to the Real-time Ethernet Driver functional entries.

The EtherCAT Real-time Ethernet Driver will be initialized using a Real-time Ethernet Driver specific configuration parameter set.
A pointer to this parameter set is part of |Product|'s initialization settings when calling the function :cpp:func:`esInitSimulator` .

|Product| supports two Real-time Ethernet Driver operating modes:
- Interrupt mode all received Ethernet frames will be processed immediately in the context of the Real-time Ethernet Driver receiver task.
- Polling mode, the application must cyclically call :cpp:func:`esExecJob` with job :cpp:enumerator:`eUsrJob_ProcessAllRxFrames` in order to trigger |Product| to call the Real-time Ethernet Driver receiver polling function and process received frames.

.. important:: In polling mode, the master cycle time must be at least two times higher than the simulator cycle time. E.g. if the simulator runs with 1 ms, the master cycle time must be at least 2 ms. If the Real-time Ethernet Driver is running in interrupt mode (non-standard), processing of received frames is done immediately after the frame is received.


.. note:: Real-time Ethernet Driver modules not listed here may be available if purchased additionally. Not all Real-time Ethernet Driver modules support interrupt mode. 

.. toctree::
    :hidden:

    emll_init.rst
    
    emllbcmgenet.rst
    emllbcmnetxtreme.rst
    emllccat.rst
    emllcpsw.rst
    emlldpdk.rst
    emlldw3504.rst
    emlletsec.rst
    emllfslfec.rst
    emllgem.rst
    emllhpe.rst
    emlli8255x.rst
    emllicss.rst
    emllintelgbe.rst
    emllndis.rst
    emllpcap.rst
    emllr6040.rst
    emllremote.rst
    emllrtl8169.rst
    emllsnarf.rst
    emllsockraw.rst
    emllsockxdp.rst
    emlltap.rst
    
