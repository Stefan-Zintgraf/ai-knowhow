*******************************
File access over EtherCAT (FoE)
*******************************

The File access over EtherCAT (FoE) mailbox command specifies a standard way to download a firmware or any other files from a client to a server or to upload a firmware or any other files from a server to a client.

Reference:

- ETG.1000.5, ETG.1000.6 and ETG.5003.2 

Specification
*************

FoE file download
=================

**Regular download**

.. uml::

        skinparam monochrome true
        skinparam SequenceMessageAlign direction
        hide footbox

        Master -> Slave: WRQ (file name)
        Master <- Slave: ACK (packet no 0)
        Master -> Slave: WRQ (packet no 1, full mailbox)
        Master <- Slave: ACK (packet no 1)
        Master -> Slave: WRQ (packet no 2, full mailbox)
        Master <- Slave: ACK (packet no 2)
        Master -> Slave: WRQ (packet no 3, less data or zero data)
        Master <- Slave: ACK (packet no 3)


**Segmented download**

In case of segmented download the EC-Master raises emNotify - EC_NOTIFY_MBOXRCV in `EC-Master Class B <https://developer.acontis.com/ec-master#manuals>`__ documentation to request more data from the application after each ACK from the slave.
The notification handler may not block the EC-Master, e.g. due to reading from or writing to the file system, therefore applications typically do not handle EC_NOTIFY_MBOXRCV within the JobTask context.
The segments are transferred using the slave's mailbox, so the maximum size of a segment is known from the configuration. The segment's size can be calculated as follows:


segment size = mailbox size - 12 (protocol overhead)


.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxOutSize` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxOutSize2` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxInSize` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxInSize2` (:cpp:func:`emGetCfgSlaveInfo`)

**Download with busy**

.. uml::

        skinparam monochrome true
        skinparam SequenceMessageAlign direction
        hide footbox

        Master -> Slave: WRQ (file name)
        Master <- Slave: ACK (packet no 0)
        Master -> Slave: DATA (packet no 1, full mailbox)
        Master <- Slave: ACK (packet no 1)
        Master -> Slave: DATA (packet no 2, less data or zero data)
        Master <- Slave: BUSY (X of N done)
        Master -> Slave: DATA (packet no 2, less data or zero data)
        Master <- Slave: ACK (packet no 2)

**Download with error**

.. uml::

        skinparam monochrome true
        skinparam SequenceMessageAlign direction
        hide footbox

        Master -> Slave: WRQ (with file name)
        Master <- Slave: ERR (error code and optional error text)

FoE file upload
===============

The names of availables files and their size are slave specific and cannot be retrieved using FoE. It is possible to upload the complete file in segments without the need to know the file size.

The segments are transferred using the slave's mailbox, so the maximum size of a segment is known from the configuration.

**Regular upload**

.. uml::

        skinparam monochrome true
        skinparam SequenceMessageAlign direction
        hide footbox

        Master -> Slave: RRQ (file name)
        Master <- Slave: DATA (packet no 1, full mailbox)
        Master -> Slave: ACK (packet no 1)
        Master <- Slave: DATA (packet no 2, full mailbox)
        Master -> Slave: ACK (packet no 2)
        Master <- Slave: DATA (packet no 3, less data or zero data)
        Master -> Slave: ACK (packet no 3)

Boot State
==========

For the download of firmware the BOOT state in the EtherCAT state machine is defined. In bootstrap mode only FoE Download is possible. A special Mailbox size can be supported by the slave for the Boot state (ETG.2000). This is part of the Init-Commands in the network configuration.

.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxOutSize2` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxInSize2` (:cpp:func:`emGetCfgSlaveInfo`)


emFoeFileDownload
*****************

.. doxygenfunction:: ecatFoeFileDownload
    :outline:

.. doxygenfunction:: emFoeFileDownload

.. seealso:: :cpp:func:`emGetSlaveId`

The following example demonstrates how to do a firmware update using FoE (ETG.5003.2).

.. dropdown:: **emFoeFileDownload() Example**

    This example code shows how to download a file from a buffer at the master to a slave, e.g. in order to update the firmware.

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_foe.h
        :language: cpp
        :start-after: DocumentationSnippetsFoeDownloadExample
        :end-before: DocumentationSnippetsFoeDownloadExample


emFoeFileUpload
***************

.. doxygenfunction:: ecatFoeFileUpload
    :outline:

.. doxygenfunction:: emFoeFileUpload

.. seealso:: :cpp:func:`emGetSlaveId`

emFoeDownloadReq
****************

.. doxygenfunction:: ecatFoeDownloadReq
    :outline:

.. doxygenfunction:: emFoeDownloadReq

.. seealso:: :cpp:func:`emGetSlaveId`

emFoeSegmentedDownloadReq
*************************

.. doxygenfunction:: ecatFoeSegmentedDownloadReq
    :outline:

.. doxygenfunction:: emFoeSegmentedDownloadReq

.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxOutSize` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxOutSize2` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:func:`emGetSlaveId`

emFoeUploadReq
**************

.. doxygenfunction:: ecatFoeUploadReq
    :outline:

.. doxygenfunction:: emFoeUploadReq

.. seealso:: :cpp:func:`emGetSlaveId`

emFoeSegmentedUploadReq
***********************

.. doxygenfunction:: ecatFoeSegmentedUploadReq
    :outline:

.. doxygenfunction:: emFoeSegmentedUploadReq

.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::dwMbxInSize` (:cpp:func:`emGetCfgSlaveInfo`)
    - :cpp:func:`emGetSlaveId`

The following example demonstrates how to upload a file in segments:

.. dropdown:: **emFoeSegmentedUploadReq() Example**

    The following code demonstrates how to receive FoE from the slave with address MY_FOE_SLAVE_ADDRESS and store it in a file.
    The data uploaded from MY_FOE_TRANSFER_SLAVE_FILENAME of the slave is stored in a file with filename MY_FOE_TRANSFER_LOCAL_FILENAME in this example.

    The example code can be placed after the corresponding :cpp:func:`emSetMasterState`-call in EcDemoApp.cpp:

    .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_foe.h
        :language: cpp
        :start-after: DocumentationSnippetsFoeSegmentedUploadReqExample
        :end-before: DocumentationSnippetsFoeSegmentedUploadReqExample

emConvertEcErrorToFoeError
**************************

.. doxygenfunction:: ecatConvertEcErrorToFoeError
    :outline:

.. doxygenfunction:: emConvertEcErrorToFoeError

emNotify - EC_NOTIFY_FOE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a FoE mailbox write command was not set to the expected value of 1.
Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of the union element WkcErrDesc.

.. cpp:alias:: EC_T_WKCERR_DESC
        :maxdepth: 0


emNotify - EC_NOTIFY_FOE_MBSLAVE_ERROR
**************************************

This error will be indicated in case a FoE mailbox slave send an error message.
Detailed error information is stored in structure :cpp:struct:`EC_T_MBOX_FOE_ABORT_DESC` of the union element FoeErrorDesc.

.. doxygenstruct:: EC_T_MBOX_FOE_ABORT_DESC
        :members:

Extending EC_T_MBX_DATA
***********************

FoE transfer data, e.g. progress information in notification.

.. doxygenstruct:: EC_T_MBX_DATA_FOE
        :members:
