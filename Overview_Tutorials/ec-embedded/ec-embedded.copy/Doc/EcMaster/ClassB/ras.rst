***************************************
RAS-Server for EC-Lyser and EC-Engineer
***************************************

Integration Requirements
************************

To use the diagnosis tool EC-Lyser with a customer application, some modifications have to be done during integration of the EC-Master. The task is to integrate and start the Remote API Server system within the custom application, which provides a socket based uplink, which later on is connected by the 
EC-Lyser.

.. figure:: ../Media/RAS.png
    :align:     center
    :alt:

.. uml::

    skinparam monochrome true
    skinparam SequenceMessageAlign direction

    node "EC-Lyser" {
        [RAS-Client]
    }
    node "EC-Master application" {
        [RAS-Server]
        [EC-Master core]
    }

    [RAS-Client] - [RAS-Server]
    [RAS-Server] - [EC-Master core]

An example on how to integrate the Remote API Server within the application is given with the example application EcMasterDemo, which in case is pre-configured to listen for EC-Lyser on TCP Port 6000 when command line parameter :option:`EcMasterDemo -sp` is given.

To clarify the steps, which are needed within a custom application, a developer may use the following pseudo-code segment as a point of start. The Remote API Server library :file:`EcMasterRasServer.lib` (or respectively :file:`EcMasterRasServer.a`) must be linked.


Application programming interface, reference
********************************************

emRasSrvStart
=============

.. doxygenfunction:: emRasSrvStart

.. doxygenstruct:: ECMASTERRAS_T_SRVPARMS
    :members:

.. doxygenunion:: EC_T_IPADDR

.. doxygenstruct:: EC_T_INNER_IPADDR 
    :members:

emRasSrvStop
============

.. doxygenfunction:: emRasSrvStop

emRasNotify - xxx
=================

Callback function called by Remote API Server in case of state changes or error situations.

.. cpp:alias:: EC_PF_NOTIFY


emRasNotify - ECMASTERRAS_NOTIFY_CONNECTION
===========================================

Notification about a change in the Remote API's state.

.. emRasNotify:: ECMASTERRAS_T_CONNOTIFYDESC
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_CONNOTIFYDESC
    :dwInBufSize: Size of the input buffer in bytes
    
.. doxygenstruct:: ECMASTERRAS_T_CONNOTIFYDESC
    :members:

emRasNotify - ECMASTERRAS_NOTIFY_REGISTER
=========================================

Notification about a connected application registered a client to the master stack.

.. emRasNotify:: ECMASTERRAS_NOTIFY_REGISTER
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_REGNOTIFYDESC
    :dwInBufSize: Size of the input buffer in bytes
    
.. doxygenstruct:: ECMASTERRAS_T_REGNOTIFYDESC
    :members:

emRasNotify - ECMASTERRAS_NOTIFY_UNREGISTER
===========================================

Notification about a connected application un-registered a client from the master stack.

.. emRasNotify:: ECMASTERRAS_NOTIFY_UNREGISTER
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_REGNOTIFYDESC
    :dwInBufSize: Size of the input buffer in bytes
    
.. seealso:: :cpp:struct:`ECMASTERRAS_T_REGNOTIFYDESC`

emRasNotify - ECMASTERRAS_NOTIFY_MARSHALERROR
=============================================

Notification about an error during marshalling in Remote API Server connection layer.

.. emRasNotify:: ECMASTERRAS_NOTIFY_MARSHALERRORDESC
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_MARSHALERRORDESC
    :dwInBufSize: Size of the input buffer in bytes
    
.. doxygenstruct:: ECMASTERRAS_T_MARSHALERRORDESC
    :members:
    
    
emRasNotify - ECMASTERRAS_NOTIFY_ACKERROR
=========================================

Notification about an error during creation of ack / nack packet.

.. emRasNotify:: ECMASTERRAS_NOTIFY_ACKERROR
    :pbyInBuf: Pointer to EC_T_DWORD containing error code
    :dwInBufSize: Size of the input buffer in bytes

emRasNotify - ECMASTERRAS_NOTIFY_NONOTIFYMEMORY
===============================================

Notification given, when no empty buffers for notifications are available in pre-allocated notification store. This points to a configuration error. 

.. emRasNotify:: ECMASTERRAS_NOTIFY_NONOTIFYMEMORY
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance
    :dwInBufSize: Size of the input buffer in bytes

emRasNotify - ECMASTERRAS_NOTIFY_STDNOTIFYMEMORYSMALL
=====================================================

Notification given, when buffersize for standard notifications available in pre-allocated notification store are too small to carry a specific notification. This points to a configuration error. 

.. emRasNotify:: ECMASTERRAS_NOTIFY_STDNOTIFYMEMORYSMALL
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance
    :dwInBufSize: Size of the input buffer in bytes

emRasNotify - ECMASTERRAS_NOTIFY_MBXNOTIFYMEMORYSMALL
=====================================================

Notification given, when buffersize for Mailbox notifications available in pre-allocated notification store are too small to carry a specific notification. This points to a configuration error. 
This is a serious error. If this error is given, Mailbox Transfer objects may have been become out of sync and therefore no more valid usable. Mailbox notifications should be dimensioned correctly see :cpp:func:`emRasSrvStart`

.. emRasNotify:: ECMASTERRAS_NOTIFY_MBXNOTIFYMEMORYSMALL
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance
    :dwInBufSize: Size of the input buffer in bytes

