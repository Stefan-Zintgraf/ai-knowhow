******************************************************
Software Integration - Server site (Remote API Server)
******************************************************

The Remote API Server is included to the master stack using application by following steps:

#. Link the Remote Server API Lib to the Project
#. Make the Remote API Server DLL available to the Runtime environment of your application.
#. Include the necessary curve up and shutdown calls to your master application
#. Compile
#. Run

Pseudo Example
**************

A master application which includes remote API hosting needs to call following steps:

.. code-block::

    #include "EcRasServer.h"
    .
    .
    emRasSrvStart(…);	/* initialize Remote API Server Module, which starts the connection
    * acceptor implicitly*/
    .
    .
    /* EC-Master API remote access provided */
    .
    .
    emRasSrvStop(…);	/* de-initialize Remote API Server Module, closes all connections */

For closer details find a Remote API Server example project <AtemDemoServer> with your installed Examples.

Remote API Server integration example (RTOS32 and RTOS32Win)
************************************************************

This section shall help you to integrate the Remote API Server into your RTOS32 and RTOS32Win application. We demonstrate step by step the integration using the example of the <AtemDemo> project. It will be assumed that EC-Master for On Time RTOS32 is installed and you can execute the demo application on you target system. The following steps are necessary to integrate the Remote API Server.

#. Open your <AtemDemo> project and add the files :file:`NetRTOS32Init.cpp` and :file:`NetRTOS32Init.h` to your project. These files are located in: :file:`(%Programfiles%)\\EC-Master-RTOS-32\\SDK\\INC\\RTOS-32`
#. Add the following libraries into you project settings: EcMasterRasServer.lib; rtip.lib. For RTOS32Win please add also netvmf.lib to use the RTOS32Win shared memory network interface for IP communication.
#. Uncomment the define #define ECMASTERRAS_SERVER in ATEMDemo.h 
#. Adjust the added NetRTOS32Init.h 

- For RTOS32 please adjust TargetIP, NetMask, DefaultGateway and DNSServer. Furthermore set the DEVICE_ID to one of the supported network adapters.
- For RTOS32Win you can use the VMF-network interface. In this case netvmf.lib should be added to your project and the #define DEVICE_ID should be set to RTVMF_DEVICE.
- Compile and run the demo

Additional API description
**************************

Following calls are necessary to initialize, de-initialize and observe the Remote API Server functionality.

emRasSrvGetVersion
==================

.. doxygenfunction:: emRasSrvGetVersion

emRasSrvStart
=============

.. doxygenfunction:: emRasSrvStart

.. doxygenstruct:: ECMASTERRAS_T_SRVPARMS
    :members:
    
emRasSrvStop
============

.. doxygenfunction:: emRasSrvStop

emrasNotify - xxx
=================

.. doxygenstruct:: EC_T_NOTIFYPARMS
    :members:
    
emrasNotify - ECMASTERRAS_NOTIFY_CONNECTION
===========================================

Notification about a change in the Remote API’s state.

.. emrasNotify:: ECMASTERRAS_NOTIFY_CONNECTION
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_CONNOTIFYDESC.
    :dwInBufSize: sizeof(ECMASTERRAS_T_CONNOTIFYDESC)

Data structure containing the new Remote API state and the cause of state change.

.. doxygenstruct:: ECMASTERRAS_T_CONNOTIFYDESC
    :members:
    
emrasNotify - ECMASTERRAS_NOTIFY_REGISTER
=========================================

Notification about a connected application registered a client to the master stack.

.. emrasNotify:: ECMASTERRAS_NOTIFY_REGISTER
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_REGNOTIFYDESC.
    :dwInBufSize: sizeof(ECMASTERRAS_T_REGNOTIFYDESC)

.. doxygenstruct:: ECMASTERRAS_T_REGNOTIFYDESC
    :members:
    
emrasNotify - ECMASTERRAS_NOTIFY_UNREGISTER
===========================================

Notification about a connected application un-registered a client from the master stack.

.. emrasNotify:: ECMASTERRAS_NOTIFY_UNREGISTER
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_REGNOTIFYDESC.
    :dwInBufSize: sizeof(ECMASTERRAS_T_REGNOTIFYDESC)

.. cpp:alias:: ECMASTERRAS_T_REGNOTIFYDESC
    
emrasNotify - ECMASTERRAS_NOTIFY_MARSHALERROR
=============================================

Notification about an error during marshaling in Remote API Server connection layer.

.. emrasNotify:: ECMASTERRAS_NOTIFY_MARSHALERROR
    :pbyInBuf: Pointer to data of type ECMASTERRAS_T_MARSHALERRORDESC.
    :dwInBufSize: sizeof(ECMASTERRAS_T_MARSHALERRORDESC)
    
.. doxygenstruct:: ECMASTERRAS_T_MARSHALERRORDESC
    :members:
    
emrasNotify - ECMASTERRAS_NOTIFY_ACKERROR
=========================================

Notification about an error during creation of ACK / NACK packet.

.. emrasNotify:: ECMASTERRAS_NOTIFY_ACKERROR
    :pbyInBuf: Pointer to EC_T_DWORD containing error code.
    :dwInBufSize: sizeof(EC_T_DWORD)
    
emrasNotify - ECMASTERRAS_NOTIFY_NONOTIFYMEMORY
===============================================

Notification raised, when no empty buffers for notifications are available in pre-allocated notification store. This points to a configuration error. 

.. emrasNotify:: ECMASTERRAS_NOTIFY_NONOTIFYMEMORY
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance.
    :dwInBufSize: sizeof(EC_T_DWORD)
    
emrasNotify - ECMASTERRAS_NOTIFY_STDNOTIFYMEMORYSMALL
=====================================================

Notification raised, when buffer size for standard notifications available in pre-allocated notification store are too small to carry a specific notification. This points to a configuration error. 

.. emrasNotify:: ECMASTERRAS_NOTIFY_STDNOTIFYMEMORYSMALL
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance.
    :dwInBufSize: sizeof(EC_T_DWORD)
    
emrasNotify - ECMASTERRAS_NOTIFY_MBXNOTIFYMEMORYSMALL
=====================================================

Notification raised, when buffer size for Mailbox notifications available in pre-allocated notification store are too small to carry a specific notification. This points to a configuration error. 

.. emrasNotify:: ECMASTERRAS_NOTIFY_MBXNOTIFYMEMORYSMALL
    :pbyInBuf: Pointer to EC_T_DWORD containing unique identification cookie of connection instance.
    :dwInBufSize: sizeof(EC_T_DWORD)
    
This is a serious error. If this error is raised, Mailbox Transfer objects may have been become out of sync and therefore no more valid usable. Mailbox notifications should be dimensioned correctly see :cpp:func:`emRasSrvStart`.

Access control
**************

The access control is used in order to restrict RAS client in calling API functions. The RAS server set actual access level according to application logic. The API calls with required access level lower than actual RAS server access level are blocked for execution; the RAS client will be notified about it. There are following access levels (in order of access rights lowering):

- “Full access”, all API functions may be executed by client. This is the default level after initialization of access control or if the RAS server did not initialize the access control subsystem as well.
- “Read/write access”, lower assess level as “full access”. Recommended for modifying API calls.
- “Read only access”, lower access level as “read/write access”, all modifying API calls are blocked.
- “Block all”, all API calls are forbidden for execution.

In order to configure the access control subsystem :cpp:func:`emRasSrvConfigAccessLevel` is used, to active/deactivate the access control call :cpp:func:`emRasSrvSetAccessControl`, to alter the access level required for each API call separately :cpp:func:`emRasSrvModifyCallAccessLevel` is used.

If the required access level of the current API call is lower than actual RAS access level an error code :cpp:struct:`EMRAS_E_ACCESSLESS` will be returned.

Configuration
=============

Default: 
    It is possible to omit the configuration data (using `EC_NULL`) in order to apply the default configuration.

Opt-in:
    The application can define for each API the lowest value of the global access level that includes the given API. All non-configured APIs are excluded below global access level “Full access”.

Opt-out:
    The application can define for each API to be completely excluded, even at global access level “Full access”.

Mixing modes: 
    “Opt-Out” (access level “Excluded”) and “Opt-in” (non-configured APIs) can be combined. “Opt-Out” is checked before “Opt-in”.

Because the first matching configuration data entry specifies the access
level of the corresponding API, there might be irrelevant configuration
data entries that the RAS server does not detect. This is by intention
as it enables the application to e.g. include
`RASSPOCCFGINITDEFAULT` at the end of the configuration in order
to minimally modify the default configuration. Entries that are more
concrete must be given before less concrete entries, see
PARAMETER_IGNORE below.

“Opt-Out” can be combined with `RASSPOCCFGINITDEFAULT` in order to
support global access levels below “Full access” in conjunction with
completely blocking discreet APIs.


emRasSrvConfigAccessLevel
=========================

.. doxygenfunction:: emRasSrvConfigAccessLevel

The access control subsystem will be initialized by calling this function. The access control configuration is defined in an array with each entry of type :cpp:struct:`ECMASTERRAS_T_SPOCCFG`. The parameter dwLen specifies the overall length of configuration data pointed by pbyData. In order to use default configuration the parameter pbyData has to be set to EC_NULL, in this case the parameter dwLen will be ignored. 

The access control subsystem creates its own copy of the input configuration structure, so the pbyData can be destroyed after this call. After initialization this configuration can be altered with :cpp:func:`emRasSrvCallAccessLevel`. After initialization the access control is active and control level is “full access”, to change use :cpp:func:`emRasSrvSetAccessControl` and :cpp:func:`emRasSrvSetAccessLevel` respectively.

.. doxygenstruct:: ECMASTERRAS_T_SPOCCFG
    :members:
    
.. doxygenenum:: ECMASTERRAS_T_ORDINAL

emRasSrvSetAccessControl
========================

.. doxygenfunction:: emRasSrvSetAccessControl

emRasSrvSetAccessLevel
======================

.. doxygenfunction:: emRasSrvSetAccessLevel

emRasSrvGetAccessLevel
======================

.. doxygenfunction:: emRasSrvGetAccessLevel

emRasSrvSetCallAccessLevel
==========================

.. doxygenfunction:: emRasSrvSetCallAccessLevel
