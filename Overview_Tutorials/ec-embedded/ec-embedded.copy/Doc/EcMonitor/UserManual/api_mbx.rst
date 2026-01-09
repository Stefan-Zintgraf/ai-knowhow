**************************
EtherCAT® Mailbox Transfer
**************************

To be able to initiate a mailbox transfer the client has to create a mailbox transfer object first.
This mailbox transfer object also contains the memory where the data to be transferred is stored.
The one client that initiated the mailbox transfer will be notified about a mailbox transfer completion by the :cpp:func:`emonNotify` callback function.

To be able to identify the transfer which was completed the client has to assign a unique transfer identifier for each mailbox transfer.
The mailbox transfer object can only be used for one single mailbox transfer.
If multiple transfers shall be initiated in parallel the client has to create one transfer object for each.
The transfer object can be re-used after mailbox transfer completion.

Typical mailbox transfer sequence:

#. Record a mailbox transfer.

#. Create a transfer object (for example a SDO download transfer object).
    .. code-block:: cpp

        MbxTferDesc.dwMaxDataLen = 10

        MbxTferDesc.pbyMbxTferDescData = (EC_T_PBYTE)OsMalloc(MbxTferDesc.dwMaxDataLen)

        pMbxTfer = emonMbxTferCreate(&MbxTferDesc)
            state of the transfer object = Idle

#. Set the location to write the transferred data to, determine the transfer ID, store the client ID in the object and initiate the transfer (e.g. a SDO upload). A transfer may only be initiated if the state of the transfer object is Idle.
    .. code-block:: cpp

        pMbxTfer->dwDataLen = MbxTferDesc.dwMaxDataLen;

        pMbxTfer->pbyMbxTferData = MbxTferDesc.pbyMbxTferDescData

        pMbxTfer->dwTferId = 1;

        pMbxTfer->dwClntId = dwClntId;


        dwResult = emonCoeSdoUplodadReq(pMbxTfer, dwSlaveId, wObIndex, ...);
            state of the transfer object = Pend or TferReqError

    The state will then be set to Pend to indicate that this mailbox transfer object currently is in use and the transfer is not completed.
    If the mailbox transfer cannot be initiated the master will set the object into the state TferReqError - in such cases the client
    is responsible to set the state back into Idle.

#. If the mailbox transfer is completed the notification callback function of the corresponding client ( :cpp:func:`emonNotify`) will be called with a pointer to the mailbox transfer object. The state of the transfer object is set to TferDone prior to calling :cpp:func:`emonNotify`.
    .. code-block:: cpp

        if( dwResult != EC_E_NOERROR ) { ... }

        emonNotify( EC_NOTIFY_MBOXRCV, pParms )
            state of the transfer object = TferDone

#. In case of errors the appropriate error handling has to be executed. Application must set the transfer object state to Idle.
    .. code-block:: cpp

        if( pMbxTfer->dwErrorCode != EC_E_NOERROR ) { ... }
            In emonNotify: application may set transfer object state to Idle

#. Delete the transfer object. Alternatively this object can be used for the next transfer.
    .. code-block:: cpp

        emonMbxTferDelete(pMbxTfer);

Mailbox transfer object states
******************************

The following states exist for a mailbox transfer object:

.. doxygenenum:: EC_T_MBXTFER_STATUS

A mailbox transfer will be processed by the monitor independently from the client's timeout setting.
Some types of mailbox transfers can be cancelled by the client, e.g. if the client's timeout elapsed.

After completion of the mailbox transfer (with timeout and the client may finally set the transfer object into
the state :cpp:enumerator:`EC_T_MBXTFER_STATUS::eMbxTferStatus_Idle`.
New mailbox transfers can only be requested if the object is in the state :cpp:enumerator:`EC_T_MBXTFER_STATUS::eMbxTferStatus_Idle`.

emonMbxTferCreate
*****************

.. doxygenfunction:: emonMbxTferCreate

.. doxygenstruct:: EC_T_MBXTFER_DESC
    :members:

.. doxygenstruct:: EC_T_MBXTFER
    :members:

.. doxygenenum:: EC_T_MBXTFER_TYPE

.. doxygenunion:: EC_T_MBX_DATA

emonMbxTferAbort
****************

.. doxygenfunction:: emonMbxTferAbort

Currently only supported for FoE Transfer, CoE Download and CoE Upload.

emonMbxTferDelete
*****************

.. doxygenfunction:: emonMbxTferDelete

emonNotify - EC_NOTIFY_MBOXRCV
******************************

Indicates a mailbox transfer completion.

.. emonNotify:: EC_NOTIFY_MBOXRCV
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object provided at pbyInBuf in bytes.

The element :cpp:member:`EC_T_MBXTFER::dwClntId` contains the corresponding ID of the client that is notified, the corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

On error :cpp:member:`EC_T_MBXTFER::eTferStatus` is :cpp:enumerator:`eMbxTferStatus_TferReqError`, on success :cpp:enumerator:`eMbxTferStatus_TferDone`. In order to reuse the transfer object the application must set it back to :cpp:enumerator:`eMbxTferStatus_Idle`.

The :cpp:member:`EC_T_MBXTFER::eMbxTferType` element determines the mailbox transfer type (e.g. :cpp:enumerator:`eMbxTferType_COE_SDO_DOWNLOAD` for a completion of a CoE SDO download transfer).

emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR
*******************************************

Indicates a WKC error during a mailbox write. Detailed error information is stored in structure :cpp:class:`EC_T_WKCERR_DESC` which is part of :cpp:class:`EC_T_ERROR_NOTIFICATION_DESC`.

.. emonNotify:: EC_NOTIFY_COE_MBXSND_WKC_ERROR
    :pbyInBuf: Pointer to EC_T_ERROR_NOTIFICATION_DESC
    :dwInBufSize: Size of the error description provided at pbyInBuf in bytes

emonNotify - EC_NOTIFY_AOE_MBXSND_WKC_ERROR
*******************************************

See :ref:`api_mbx:emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR`

emonNotify - EC_NOTIFY_EOE_MBXSND_WKC_ERROR
*******************************************

See :ref:`api_mbx:emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR`

emonNotify - EC_NOTIFY_FOE_MBXSND_WKC_ERROR
*******************************************

See :ref:`api_mbx:emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR`

emonNotify - EC_NOTIFY_SOE_MBXSND_WKC_ERROR
*******************************************

See :ref:`api_mbx:emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR`

emonNotify - EC_NOTIFY_VOE_MBXSND_WKC_ERROR
*******************************************

See :ref:`api_mbx:emonNotify - EC_NOTIFY_COE_MBXSND_WKC_ERROR`