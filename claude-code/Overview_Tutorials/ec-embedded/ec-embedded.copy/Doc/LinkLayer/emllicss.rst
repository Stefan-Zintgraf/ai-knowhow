The parameters to the Real-time Ethernet Driver ICSS are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineICSS` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_ICSS
    :members: 
    
.. doxygenenum:: EC_T_LINK_ICSS_BOARD

TTS Feature
***********

Real-time Ethernet Driver PRU ICSS can optionally use Time-Triggered Send feature https://www.ti.com/lit/pdf/tidubz1 

To test it, you need to build a demo application with INCLUDE_TTS macro. Additionally, you need to set bTts flag and configure other tts parameters in :cpp:struct:`EC_T_LINK_PARMS_ICSS` structure. Please note, we have already TTS Demo applications for some of the operating systems (for ex. Linux and TI RTOS). 

dwTtsSendTimeUsec time is determined experimentally. It depends to how long your own real project prepares cyclic and acyclic frames to be sent in the current cycle.

Main purpose of the TTS feature is to reduce jitter to 40 ns (nanoseconds). To measure jitter accurately you need to have special software and hardware. For example:

- Old version of Wire Shark, ex. 1.8.4
- Dissect plugin for Wire Shark (this plugin is available only for this version of WireShark) 
- ET2000 device to insert accurate timestamps with nanoseconds resolution.

Details can be found here:
https://infosys.beckhoff.com/index.php?content=../content/1031/et2000/1309654283.html&id= 

TI AM335x ICEV2
***************
After the two 100 MBit ports have been deactivated, there are no longer any Ethernet ports that can be used for TCP/IP. The board cannot work in mixed mode, i.e. there is no CPSW+ICSS support. It is also necessary to configure the board to start in ICSS rather than CPSW mode. Set both jumpers on the board to ICSS mode.

.. seealso:: http://processors.wiki.ti.com/index.php/AM335x_Industrial_Communication_Engine_EVM_Rev2_1_HW_User_Guide 

TI AM57xx IDK
*************
After the four 100 MBit ports of the ICSS have been deactivated, the other two 1 GBit ports (CPSW) remain active and can be used for other purposes (e.g. TCP / IP).

AM5728 IDK and AM5718 IDK boards and Technical Limitations 
**********************************************************

The main difference between these two boards is number of available ICSS ports. AM5728 IDK supports only two 100 Mbit ports: port 3 and 4. It is a technical limitation of this board. On AM5718 IDK all four 100 Mbit ports are available for EtherCAT purposes.

.. note:: Real-time Ethernet Driver PRUICSS can use maximum 2 ports together (in redundancy mode) and these two ports should correspond to the same PRUSS. I.e. Port 3 and 4 OR Port 1 and 2, but not Port 1 and 4, Port 1 and 3 and etc. This technical limitation exists, because PRU firmware for PRU0 and PRU1 uses the same memory areas of OCMC Memory. In future, this limitation can be removed.
