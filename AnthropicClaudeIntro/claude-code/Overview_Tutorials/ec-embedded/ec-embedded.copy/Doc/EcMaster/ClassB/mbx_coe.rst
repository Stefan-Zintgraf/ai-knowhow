********************************************
CAN application protocol over EtherCAT (CoE)
********************************************

emCoeSdoDownload
****************

.. doxygenfunction:: ecatCoeSdoDownload
    :outline:

.. doxygenfunction:: emCoeSdoDownload

.. dropdown:: **emCoeSdoDownload Example** 

    The following code demonstrates how to download a CoE object to a slave using the API :cpp:func:`emCoeSdoDownload`.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeSdoDownloadExample
        :end-before: DocumentationSnippetsCoeSdoDownloadExample

.. seealso:: :cpp:func:`emGetSlaveId`

emCoeSdoDownloadReq
*******************

.. doxygenfunction:: ecatCoeSdoDownloadReq
    :outline:

.. doxygenfunction:: emCoeSdoDownloadReq

.. dropdown:: **emCoeSdoDownloadReq Example**

    The following code demonstrates how to download a CoE object to a slave using the non-blocking API :cpp:func:`emCoeSdoDownloadReq`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeSdoDownloadReqExample
        :end-before: DocumentationSnippetsCoeSdoDownloadReqExample

.. seealso::
    - :ref:`mbx_coe:emNotify - eMbxTferType_COE_SDO_DOWNLOAD`
    - :cpp:func:`emMbxTferCreate`
    - :cpp:func:`emGetSlaveId`

emNotify - eMbxTferType_COE_SDO_DOWNLOAD
****************************************

SDO download transfer completion.

.. emNotify:: eMbxTferType_COE_SDO_DOWNLOAD
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The request parameters stored in element :cpp:member:`EC_T_MBX_DATA::CoE` of type :cpp:struct:`EC_T_MBX_DATA_COE` are part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_MBX_DATA_COE
    :members:

emCoeSdoUpload
**************

.. doxygenfunction:: ecatCoeSdoUpload
    :outline:

.. doxygenfunction:: emCoeSdoUpload

.. dropdown:: **emCoeSdoUpload Example**

    The following code demonstrates how to upload a CoE object from a slave using the API :cpp:func:`emCoeSdoUpload`.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeSdoUploadExample
        :end-before: DocumentationSnippetsCoeSdoUploadExample

.. seealso:: :cpp:func:`emGetSlaveId`

emCoeSdoUploadReq
*****************

.. doxygenfunction:: ecatCoeSdoUploadReq
    :outline:

.. doxygenfunction:: emCoeSdoUploadReq

.. dropdown:: **emCoeSdoUploadReq Example**

    The following code demonstrates how to upload a CoE object from a slave using the non-blocking API :cpp:func:`emCoeSdoUploadReq`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeSdoUploadReqExample
        :end-before: DocumentationSnippetsCoeSdoUploadReqExample
        
.. seealso::
    - :ref:`mbx_coe:emNotify - eMbxTferType_COE_SDO_UPLOAD`
    - :cpp:func:`emMbxTferCreate`
    - :cpp:func:`emGetSlaveId`

emNotify - eMbxTferType_COE_SDO_UPLOAD
**************************************

SDO upload transfer completion.

.. emNotify:: eMbxTferType_COE_SDO_UPLOAD
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

The corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The request parameters stored in element :cpp:member:`EC_T_MBX_DATA::CoE` of type :cpp:struct:`EC_T_MBX_DATA_COE` are part of :cpp:member:`EC_T_MBXTFER::MbxData`.
The SDO data stored in :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` may have to be buffered by the client.
Access to the memory area referenced by :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` outside of the notification caller context is illegal and the results are undefined.

emCoeGetODListReq
*****************

.. doxygenfunction:: ecatCoeGetODListReq
    :outline:

.. doxygenfunction:: emCoeGetODListReq

.. doxygenenum:: EC_T_COE_ODLIST_TYPE

.. dropdown:: **emCoeGetODListReq Example**

    The following code demonstrates how to get the list of objects that are available in a slave using the non-blocking API :cpp:func:`emCoeGetODListReq`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeGetODListReqExample
        :end-before: DocumentationSnippetsCoeGetODListReqExample
        
.. seealso::
    - :ref:`mbx_coe:emNotify - eMbxTferType_COE_GETODLIST`
    - :cpp:func:`emMbxTferCreate`
    - :cpp:func:`emGetSlaveId`
    - See :cpp:func:`CoeReadObjectDictionary` in EcSdoServices.cpp as an example for :cpp:func:`emCoeGetODListReq` .

emNotify - eMbxTferType_COE_GETODLIST
*************************************

Object dictionary list upload transfer completion.

.. emNotify:: eMbxTferType_COE_GETODLIST
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

The corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The object list stored in element :cpp:member:`EC_T_MBX_DATA::CoE_ODList` of type :cpp:struct:`EC_T_COE_ODLIST` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_ODLIST
    :members:

emCoeGetObjectDescReq
*********************

.. doxygenfunction:: ecatCoeGetObjectDescReq
    :outline:

.. doxygenfunction:: emCoeGetObjectDescReq

.. dropdown:: **emCoeGetObjectDescReq Example**

    The following code demonstrates how to determine the description of a specific object using the non-blocking API :cpp:func:`emCoeGetObjectDescReq`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeGetObjectDescReqExample
        :end-before: DocumentationSnippetsCoeGetObjectDescReqExample

.. seealso::
    - :ref:`mbx_coe:emNotify - eMbxTferType_COE_GETOBDESC`
    - :cpp:func:`emMbxTferCreate`
    - :cpp:func:`emGetSlaveId`
    - See :cpp:func:`CoeReadObjectDictionary` in EcSdoServices.cpp as an example for :cpp:func:`emCoeGetObjectDescReq` .

emNotify - eMbxTferType_COE_GETOBDESC
*************************************

Completion of a SDO information service transfer to get a object description.

.. emNotify:: eMbxTferType_COE_GETOBDESC
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

The corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The object description stored in element :cpp:member:`EC_T_MBX_DATA::CoE_ObDesc` of type :cpp:struct:`EC_T_COE_OBDESC` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_OBDESC
    :members:

.. seealso:: A more detailed description of the values for data type, object code etc. can be found in the EtherCAT specification ETG.1000, section 5.

emCoeGetEntryDescReq
********************

.. doxygenfunction:: ecatCoeGetEntryDescReq
    :outline:

.. doxygenfunction:: emCoeGetEntryDescReq

.. dropdown:: **emCoeGetEntryDescReq Example**

    The following code demonstrates how to get the description of a specific object entry using the non-blocking API :cpp:func:`emCoeGetEntryDescReq`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeGetEntryDescReqExample
        :end-before: DocumentationSnippetsCoeGetEntryDescReqExample

**Value info flags**

.. datatemplate:xml:: EC_COE_ENTRY_VALUEINFO
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. seealso::
    - :ref:`mbx_coe:emNotify - eMbxTferType_COE_GETENTRYDESC`
    - :cpp:func:`emMbxTferCreate`
    - :cpp:func:`emGetSlaveId`
    - See :cpp:func:`CoeReadObjectDictionary` in EcSdoServices.cpp as an example for :cpp:func:`emCoeGetEntryDescReq` .

emNotify - eMbxTferType_COE_GETENTRYDESC
****************************************

Completion of a SDO information service transfer to get a object entry description.

.. emNotify:: eMbxTferType_COE_GETENTRYDESC
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

The corresponding transfer ID can be found in :cpp:member:`EC_T_MBXTFER::dwTferId`. The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The object entry description stored in element :cpp:member:`EC_T_MBX_DATA::CoE_EntryDesc` of type :cpp:struct:`EC_T_COE_ENTRYDESC` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_ENTRYDESC
    :members:

**Object access flags**

.. datatemplate:xml:: EC_COE_ENTRY_OBJACCESS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. seealso::
    - An example for the evaluation of :cpp:member:`EC_T_COE_ENTRYDESC::pbyData` comes with EcMasterDemo.
    - A more detailed description of the values can be found in the EtherCAT specification ETG.1000, section 5 and 6.

emCoeProfileGetChannelInfo
**************************

.. doxygenfunction:: ecatCoeProfileGetChannelInfo
    :outline:

.. doxygenfunction:: emCoeProfileGetChannelInfo

.. doxygenstruct:: EC_T_PROFILE_CHANNEL_INFO
    :members:

.. dropdown:: **emCoeProfileGetChannelInfo Example**

    The following code demonstrates how to return information about a configured CoE profile channel from the ENI file using the non-blocking API :cpp:func:`emCoeProfileGetChannelInfo`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeProfileGetChannelInfoExample
        :end-before: DocumentationSnippetsCoeProfileGetChannelInfoExample


emNotify - EC_NOTIFY_COE_INIT_CMD
*********************************

Indicates a COE mailbox transfer completion during slave state transition. This notification is disabled by default.

.. emNotify:: EC_NOTIFY_COE_INIT_CMD
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object provided at pbyInBuf in bytes.

The :cpp:member:`EC_T_MBX_DATA::CoE_InitCmd` element of type :cpp:struct:`EC_T_MBX_DATA_COE_INITCMD` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_MBX_DATA_COE_INITCMD
    :members:

.. seealso:: :ref:`api:emIoControl - EC_IOCTL_SET_NOTIFICATION_ENABLED`

CoE Emergency (emNotify - eMbxTferType_COE_EMERGENCY)
*****************************************************

Indication of a CoE emergency request. A :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` is given with :cpp:member:`EC_T_MBXTFER::eMbxTferType` = :cpp:enumerator:`EC_T_MBXTFER_TYPE::eMbxTferType_COE_EMERGENCY`.

.. emNotify:: eMbxTferType_COE_EMERGENCY
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

In case of an emergency notification all registered clients will get this notification.
The corresponding mailbox transfer object will be created inside the EtherCAT master. The content in :cpp:member:`EC_T_MBXTFER::dwTferId` is undefined as it is not needed by the client and the master.
The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The emergency data stored in element :cpp:member:`EC_T_MBX_DATA::CoE_Emergency` of type :cpp:struct:`EC_T_COE_EMERGENCY` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_EMERGENCY
    :members:

.. dropdown:: **CoE Emergency Example**

    .. literalinclude:: ..\..\..\Doc\EcSimulator\Snippets\api_error_simulation_functions.h
        :language: cpp
        :start-after: DocumentationSnippetsCoeEmergencyExample 
        :end-before: DocumentationSnippetsCoeEmergencyExample

.. seealso:: A more detailed description of the values can be found in the EtherCAT specification ETG.1000, section 5.

CoE Abort (emNotify - EC_NOTIFY_MBSLAVE_COE_SDO_ABORT)
******************************************************

The application can abort asynchronous CoE Uploads and Downloads.
The slave may abort CoE Uploads and Downloads which is indicated at the return code of :cpp:func:`emCoeSdoUpload`, ... .
This notification is given if an SDO transfer aborts while sending init commands.

.. emNotify:: EC_NOTIFY_MBSLAVE_COE_SDO_ABORT
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

Detailed error information is stored in structure :cpp:struct:`EC_T_MBOX_SDO_ABORT_DESC` of the union element SdoAbortDesc.

.. doxygenstruct:: EC_T_MBOX_SDO_ABORT_DESC
    :members:

.. seealso:: :cpp:func:`emMbxTferAbort`

emConvertEcErrorToCoeError
**************************

.. doxygenfunction:: ecatConvertEcErrorToCoeError
    :outline:

.. doxygenfunction:: emConvertEcErrorToCoeError

.. dropdown:: **emConvertEcErrorToCoeError Example**

    The following code demonstrates how to convert master error code to CoE error code using the non-blocking API :cpp:func:`emConvertEcErrorToCoeError`.

    In this example the mailbox transfer object state is polled. :ref:`mbx_tfer:emNotify - EC_NOTIFY_MBOXRCV` can be used as alternative to polling.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_coe.h
        :language: cpp
        :start-after: DocumentationSnippetsConvertEcErrorToCoeErrorExample
        :end-before: DocumentationSnippetsConvertEcErrorToCoeErrorExample