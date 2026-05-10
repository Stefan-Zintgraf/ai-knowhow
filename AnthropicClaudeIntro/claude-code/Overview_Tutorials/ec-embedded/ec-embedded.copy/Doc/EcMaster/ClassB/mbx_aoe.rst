***************************************************
Automation Device Specification over EtherCAT (AoE)
***************************************************

The AoE protocol is used to access the Object dictionary of slave devices of underlying field-buses, e.g. for a CAN application protocol Slave connected to a EtherCAT-CANopen gateway device. It is also used in relation with the EtherCAT Automation Protocol (EAP).

Reference:

- ETG.1020 -> AoE

**Current limitations**

- Fragmented AoE access is not yet implemented

emAoeGetSlaveNetId
******************

.. doxygenfunction:: ecatAoeGetSlaveNetId
    :outline:

.. doxygenfunction:: emAoeGetSlaveNetId

.. doxygenstruct:: EC_T_AOE_NETID
   :members:

.. seealso:: :cpp:func:`emGetSlaveId`

emAoeRead
*********

.. doxygenfunction:: ecatAoeRead
    :outline:

.. doxygenfunction:: emAoeRead

.. seealso::
    - :cpp:func:`emAoeReadReq`
    - :cpp:func:`emGetSlaveId`

emAoeReadReq
************

.. doxygenfunction:: ecatAoeReadReq
    :outline:

.. doxygenfunction:: emAoeReadReq

.. doxygenstruct:: EC_T_AOE_CMD_RESPONSE
	:members:

.. seealso:: :cpp:func:`emGetSlaveId`

emNotify - eMbxTferType_AOE_READ
********************************

.. emNotify:: eMbxTferType_AOE_READ
    :pbyInBuf: pMbxTfer - Pointer to a structure of type EC_T_MBXTFER, this structure contains the used mailbox transfer object. This mailbox transfer object also contains AoE device error codes in case of an AoE access error.
    :dwInBufSize: Size of the transfer object.

.. seealso:: :cpp:func:`emAoeReadReq`

emAoeWrite
**********

.. doxygenfunction:: ecatAoeWrite
    :outline:

.. doxygenfunction:: emAoeWrite

.. seealso::
    - :cpp:func:`emAoeWriteReq`
    - :cpp:func:`emGetSlaveId`

emAoeWriteReq
*************

.. doxygenfunction:: ecatAoeWriteReq
    :outline:

.. doxygenfunction:: emAoeWriteReq

.. seealso:: :cpp:func:`emGetSlaveId`

emNotify - eMbxTferType_AOE_WRITE
*********************************

.. emNotify:: eMbxTferType_AOE_WRITE
    :pbyInBuf: pMbxTfer - Pointer to a structure of type EC_T_MBXTFER, this structure contains the used mailbox transfer object. This mailbox transfer object also contains AoE device error codes in case of an AoE access error.
    :dwInBufSize: Size of the transfer object.

.. seealso:: :cpp:func:`emAoeWriteReq`

emAoeReadWrite
**************

.. doxygenfunction:: ecatAoeReadWrite
    :outline:

.. doxygenfunction:: emAoeReadWrite

.. seealso:: :cpp:func:`emGetSlaveId`

emAoeWriteControl
*****************

.. doxygenfunction:: ecatAoeWriteControl
    :outline:

.. doxygenfunction:: emAoeWriteControl

.. seealso:: :cpp:func:`emGetSlaveId`

emConvertEcErrorToAdsError
**************************

.. doxygenfunction:: ecatConvertEcErrorToAdsError
    :outline:

.. doxygenfunction:: emConvertEcErrorToAdsError