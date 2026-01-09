******************
Programmer's Guide
******************

emEoeRegisterEndpoint
*********************

.. doxygenfunction:: ecatEoeRegisterEndpoint
    :outline:

.. doxygenfunction:: emEoeRegisterEndpoint

.. doxygenstruct:: EC_T_LINK_DRV_DESC
    :members:
    
.. doxygenstruct:: EC_T_LOG_PARMS
    :members:
    
emEoeUnregisterEndpoint
***********************

.. doxygenfunction:: ecatEoeUnregisterEndpoint
    :outline:

.. doxygenfunction:: emEoeUnregisterEndpoint

pfEcLinkOpen
************

.. doxygentypedef:: PF_EcLinkOpen

The first input parameter :cpp:var:`pvLinkParms` is of type :cpp:struct:`EC_T_LINK_OPENPARMS_EOE`

.. doxygenstruct:: EC_T_LINK_OPENPARMS_EOE
    :members:
    
pfEcLinkClose
*************

.. doxygentypedef:: PF_EcLinkClose

pfEcLinkSendFrame
*****************

.. doxygentypedef:: PF_EcLinkSendFrame

.. doxygenstruct:: EC_T_LINK_FRAMEDESC
    :members:

pfEcLinkSendAndFreeFrame
************************

.. doxygentypedef:: PF_EcLinkSendAndFreeFrame

pfEcLinkRecvFrame
*****************

.. doxygentypedef:: PF_EcLinkRecvFrame

pfEcLinkAllocSendFrame
**********************

.. doxygentypedef:: PF_EcLinkAllocSendFrame

pfEcLinkFreeSendFrame
*********************

.. doxygentypedef:: PF_EcLinkFreeSendFrame

pfEcLinkFreeRecvFrame
*********************

.. doxygentypedef:: PF_EcLinkFreeRecvFrame

pfEcLinkGetEthernetAddress
**************************

.. doxygentypedef:: PF_EcLinkGetEthernetAddress

pfEcLinkGetStatus
*****************

.. doxygentypedef:: PF_EcLinkGetStatus

pfEcLinkGetSpeed
****************

.. doxygentypedef:: PF_EcLinkGetSpeed

pfEcLinkGetMode
***************

.. doxygentypedef:: PF_EcLinkGetMode

pfEcLinkIoctl
*************

.. doxygentypedef:: PF_EcLinkIoctl

