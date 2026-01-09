*********************************************
CAN application protocol over EtherCAT® (CoE)
*********************************************

The |Product| can forward CoE transfers to the application in real time via the notifications :ref:`api_mbx_coe:emonNotify - eMbxTferType_COE_SDO_DOWNLOAD`, :ref:`api_mbx_coe:emonNotify - eMbxTferType_COE_SDO_UPLOAD` and :ref:`emonNotify - eMbxTferType_COE_EMERGENCY<api_mbx_coe:CoE Emergency (emonNotify - eMbxTferType_COE_EMERGENCY)>`.

There is also the option of storing the recorded data from the CoE transfers in an internal object dictionary. 
This object dictionary is structured analogously to that from the slaves and can be read out via the functions :cpp:func:`emonCoeSdoUpload` / :cpp:func:`emonCoeSdoUploadReq` and :cpp:func:`emonCoeGetODListReq`.

The notifications for CoE can be deactivated using the :cpp:member:`EC_T_MBX_PARMS_COE::bDisableNotifications` parameter if they are not required or to save computing time.
In order to reduce memory consumption, the internal memory for the CoE data can be deactivated using the :cpp:member:`EC_T_MBX_PARMS_COE::bDisableODStorage` parameter.

If both parameters :cpp:member:`EC_T_MBX_PARMS_COE::bDisableNotifications` and :cpp:member:`EC_T_MBX_PARMS_COE::bDisableODStorage` are set, the CoE monitoring is completely deactivated.

emonNotify - eMbxTferType_COE_SDO_DOWNLOAD
******************************************

SDO download transfer completion.

.. emonNotify:: eMbxTferType_COE_SDO_DOWNLOAD
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`. The request parameters stored in element :cpp:member:`EC_T_MBX_DATA::CoE` of type :cpp:struct:`EC_T_MBX_DATA_COE` are part of :cpp:member:`EC_T_MBXTFER::MbxData`.
The SDO data stored in :cpp:member:`EC_T_MBXTFER::pbyMbxTferData`.

.. doxygenstruct:: EC_T_MBX_DATA_COE
    :members:

emonNotify - eMbxTferType_COE_SDO_UPLOAD
****************************************

SDO upload transfer completion.

.. emonNotify:: eMbxTferType_COE_SDO_UPLOAD
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`. The request parameters stored in element :cpp:member:`EC_T_MBX_DATA::CoE` of type :cpp:struct:`EC_T_MBX_DATA_COE` are part of :cpp:member:`EC_T_MBXTFER::MbxData`.
The SDO data stored in :cpp:member:`EC_T_MBXTFER::pbyMbxTferData`.

CoE Emergency (emonNotify - eMbxTferType_COE_EMERGENCY)
*******************************************************

Indication of a CoE emergency request. A :ref:`api_mbx:emonNotify - EC_NOTIFY_MBOXRCV` is given with :cpp:member:`EC_T_MBXTFER::eMbxTferType` = :cpp:enumerator:`EC_T_MBXTFER_TYPE::eMbxTferType_COE_EMERGENCY`.

.. emonNotify:: eMbxTferType_COE_EMERGENCY
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER, contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object in bytes.

In case of an emergency notification all registered clients will get this notification.
The corresponding mailbox transfer object will be created. :cpp:member:`EC_T_MBXTFER::dwTferId` is undefined as it is not needed by the client.
The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The emergency data stored in element :cpp:member:`EC_T_MBX_DATA::CoE_Emergency` of type :cpp:struct:`EC_T_COE_EMERGENCY` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_EMERGENCY
    :members:

.. seealso:: A more detailed description of the values can be found in the EtherCAT® specification ETG.1000, section 5.

emonCoeSdoUpload
****************

.. doxygenfunction:: emonCoeSdoUpload

.. admonition:: Limitation
    :class: admonition hint

    - Only CoE entries which have been received by the |Product| can be retrieved.
    - CoE objects received via complete access can only be retrieved as complete access and vice versa.
    - When the access method of a received object changes, the object is erased.

.. seealso:: :cpp:func:`emonGetSlaveId`

emonCoeSdoUploadReq
*******************

.. doxygenfunction:: emonCoeSdoUploadReq

.. admonition:: Limitation
    :class: admonition hint

    - Only CoE entries which have been received by the |Product| can be retrieved.
    - CoE objects received via complete access can only be retrieved as complete access and vice versa.
    - When the access method of a received object changes, the object is erased.

.. seealso::
    - :ref:`api_mbx_coe:emonNotify - eMbxTferType_COE_SDO_UPLOAD`
    - :cpp:func:`emonGetSlaveId`

emonIoControl - EC_IOCTL_MONITOR_SET_COESDO_CLEAR_ON_READ
*********************************************************

This IO control can be used to activate a clear on read of the CoE SDO data. If clear on read is activated, the data is automatically deleted after each read of the CoE SDO index, subindex via :cpp:func:`emonCoeSdoUpload` or :cpp:func:`emonCoeSdoUploadReq`. The IO-Control must be called after :cpp:func:`emonConfigureNetwork`.

.. emonIoControl:: EC_IOCTL_MONITOR_SET_COESDO_CLEAR_ON_READ
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Enables clear on read.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

emonCoeGetODListReq
*******************

.. doxygenfunction:: emonCoeGetODListReq

.. doxygenenum:: EC_T_COE_ODLIST_TYPE

.. seealso::
    - :cpp:func:`emonMbxTferCreate`
    - :cpp:func:`emonGetSlaveId`

emonNotify - eMbxTferType_COE_GETODLIST
***************************************

Notification of a detected CoE SDO information service transfer for a object dictionary list.

.. emonNotify:: eMbxTferType_COE_GETODLIST
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER.
    :dwInBufSize: Size of the transfer object in bytes.

The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The object list stored in element :cpp:member:`EC_T_MBX_DATA::CoE_ODList` of type :cpp:struct:`EC_T_COE_ODLIST` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_ODLIST
    :members:
    
emonNotify - eMbxTferType_COE_GETENTRYDESC
******************************************

Notification of a detected CoE SDO information service transfer for a object entry description.

.. emonNotify:: eMbxTferType_COE_GETENTRYDESC
    :pbyInBuf: Pointer to a structure of type EC_T_MBXTFER.
    :dwInBufSize: Size of the transfer object in bytes.

The transfer result is stored in :cpp:member:`EC_T_MBXTFER::dwErrorCode`.

The object entry description stored in element :cpp:member:`EC_T_MBX_DATA::CoE_EntryDesc` of type :cpp:struct:`EC_T_COE_ENTRYDESC` is part of :cpp:member:`EC_T_MBXTFER::MbxData` and may have to be buffered by the client.
Access to the memory area :cpp:member:`EC_T_MBXTFER::MbxData` outside of the notification caller context is illegal and the results are undefined.

.. doxygenstruct:: EC_T_COE_ENTRYDESC
    :members:

**Value info flags**

.. datatemplate:xml:: EC_COE_ENTRY_VALUEINFO
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

**Object access flags**

.. datatemplate:xml:: EC_COE_ENTRY_OBJACCESS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

.. seealso:: A more detailed description of the values can be found in the EtherCAT® specification ETG.1000, section 5 and 6.
