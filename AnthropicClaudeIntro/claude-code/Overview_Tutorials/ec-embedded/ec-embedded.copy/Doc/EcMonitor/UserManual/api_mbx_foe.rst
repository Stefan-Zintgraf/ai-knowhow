********************************
File access over EtherCAT® (FoE)
********************************

The |Product| can record file transfers via the FoE protocol between an EtherCAT® master and a slave. These FoE transfers can be forwarded to the application as segmented packets in real time via the notifications :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_SEG_DOWNLOAD` and :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_SEG_UPLOAD`.

In addition, the FoE transfers can be stored as a file on the file system. The files are automatically created and stored in :cpp:member:`EC_T_MONITOR_INIT_PARMS::szFileStoragePath`. The file name consists of the following:
    .. code-block::

        <TimeStamp[msec]>_Slave<StationAddress>_<FoeFileName>

For example:
    .. code-block::

        0123456789_Slave1001_firmware.bin    

The notifications for FoE can be deactivated using the :cpp:member:`EC_T_MBX_PARMS_FOE::bDisableNotifications` parameter if they are not required or to save computing time.
If no file system is available or file storage is not desired, it can be disabled using the :cpp:member:`EC_T_MBX_PARMS_FOE::bDisableFileStorage` parameter.

If both parameters :cpp:member:`EC_T_MBX_PARMS_FOE::bDisableNotifications` and :cpp:member:`EC_T_MBX_PARMS_FOE::bDisableFileStorage` are set, the FoE monitoring is completely deactivated.

Notification sequence
*********************

Once the |Product| detects an FoE transfer, the application is notified via an :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_DOWNLOAD_REQ` or :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_UPLOAD_REQ` notification. This notification contains basic information about the upcoming transfer, e.g. requested file name.

After that, each individual packet is transmitted via an :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_SEG_DOWNLOAD` or :ref:`api_mbx_foe:emonNotify - eMbxTferType_FOE_SEG_UPLOAD` notification. The end of the transfer is set via the :cpp:member:`EC_T_MBXTFER::eTferStatus` = :cpp:enumerator:`eMbxTferStatus_TferDone`.

**Download**

.. uml::

    skinparam monochrome true
    skinparam SequenceMessageAlign direction
    skinparam SequenceBoxBorderColor transparent
    skinparam ParticipantPadding 50
    hide footbox

    participant Master
    participant Monitor
    participant Slave
    participant App

    Master->Slave: WRQ(file name)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_DOWNLOAD_REQ\neMbxTferStatus_Pend
    deactivate Monitor

    Master->Slave: DATA(first packet)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_SEG_DOWNLOAD\neMbxTferStatus_Pend
    deactivate Monitor

    ...
    Master->Slave: DATA(last packet)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_SEG_DOWNLOAD\neMbxTferStatus_Done
    deactivate Monitor

**Upload**

.. uml::

    skinparam monochrome true
    skinparam SequenceBoxBorderColor transparent
    skinparam ParticipantPadding 50
    hide footbox

    participant Master
    participant Monitor
    participant Slave
    participant App

    Master->Slave: RRQ(file name)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_UPLOAD_REQ\neMbxTferStatus_Pend
    deactivate Monitor

    Slave->Master: DATA(first packet)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_SEG_UPLOAD\neMbxTferStatus_Pend
    deactivate Monitor

    ...
    Slave->Master: DATA(last packet)
    activate Monitor
    Monitor->App: eMbxTferType_FOE_SEG_UPLOAD\neMbxTferStatus_Done
    deactivate Monitor

emonNotify - eMbxTferType_FOE_DOWNLOAD_REQ
******************************************

Notifies a FoE download request from the EtherCAT® master to a slave.

.. emonNotify:: eMbxTferType_FOE_DOWNLOAD_REQ
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The parameters that the master has requested from the slave are stored in the structure :cpp:member:`EC_T_MBX_DATA::FoE_Request` which is part of :cpp:member:`EC_T_MBXTFER::MbxData`.

.. doxygenstruct:: EC_T_MBX_DATA_FOE_REQ
    :members:

emonNotify - eMbxTferType_FOE_SEG_DOWNLOAD
******************************************

Transmits a data segment of the ongoing FoE download.

.. emonNotify:: eMbxTferType_FOE_SEG_DOWNLOAD
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The FoE download data segment is stored at :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` with size :cpp:member:`EC_T_MBXTFER::dwDataLen` and may have to be buffered by the application.
Access to the memory area :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` outside of the notification caller context is illegal and the results are undefined.

Information about the current transfer are in structure :cpp:member:`EC_T_MBX_DATA::FoE` which is part of :cpp:member:`EC_T_MBXTFER::MbxData`. Among other things, it contains the slave station address :cpp:member:`EC_T_MBX_DATA_FOE::wStationAddress` and the number of bytes already transmitted :cpp:member:`EC_T_MBX_DATA_FOE::dwTransferredBytes`.

.. doxygenstruct:: EC_T_MBX_DATA_FOE
        :members:

.. note:: The elements :cpp:member:`EC_T_MBX_DATA_FOE::dwRequestedBytes` and :cpp:member:`EC_T_MBX_DATA_FOE::dwFileSize` are not used by the |Product| because they are not known at runtime.

emonNotify - eMbxTferType_FOE_UPLOAD_REQ
****************************************

Notifies a FoE upload request from the EtherCAT® master to a slave.

.. emonNotify:: eMbxTferType_FOE_DOWNLOAD_REQ
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The parameters that the master has requested from the slave are stored in the structure :cpp:member:`EC_T_MBX_DATA::FoE_Request` which is part of :cpp:member:`EC_T_MBXTFER::MbxData`.

.. cpp:alias:: EC_T_MBX_DATA_FOE_REQ
    :maxdepth: 0

emonNotify - eMbxTferType_FOE_SEG_UPLOAD
****************************************

Transmits a data segment of the ongoing FoE upload.

.. emonNotify:: eMbxTferType_FOE_SEG_UPLOAD
    :pbyInBuf:  Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object pbyInBuf in bytes.

The FoE upload data segment is stored at :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` with size :cpp:member:`EC_T_MBXTFER::dwDataLen` and may have to be buffered by the application.
Access to the memory area :cpp:member:`EC_T_MBXTFER::pbyMbxTferData` outside of the notification caller context is illegal and the results are undefined.

Information about the current transfer are in structure :cpp:member:`EC_T_MBX_DATA::FoE` which is part of :cpp:member:`EC_T_MBXTFER::MbxData`. Among other things, it contains the slave station address :cpp:member:`EC_T_MBX_DATA_FOE::wStationAddress` and the number of bytes already transmitted :cpp:member:`EC_T_MBX_DATA_FOE::dwTransferredBytes`.

.. cpp:alias:: EC_T_MBX_DATA_FOE
    :maxdepth: 0

.. note:: The elements :cpp:member:`EC_T_MBX_DATA_FOE::dwRequestedBytes` and :cpp:member:`EC_T_MBX_DATA_FOE::dwFileSize` are not used by the |Product| because they are not known at runtime.

emonNotify - EC_NOTIFY_FOE_MBSLAVE_ERROR
****************************************

This error will be indicated in case a FoE mailbox slave send an error message.
Detailed error information is stored in structure :cpp:struct:`EC_T_MBOX_FOE_ABORT_DESC` which is part of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

.. doxygenstruct:: EC_T_MBOX_FOE_ABORT_DESC
        :members:

emonConvertEcErrorToFoeError
****************************

.. doxygenfunction:: emonConvertEcErrorToFoeError
