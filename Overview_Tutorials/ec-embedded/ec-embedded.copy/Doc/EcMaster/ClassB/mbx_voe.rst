********************************************
Vendor specific protocol over EtherCAT (VoE)
********************************************

VoE is for vendor specific protocols. With VoE the vendor has access to a raw EtherCAT mailbox without a specific header or specific protocol mechanism.

emVoeWrite
**********

.. doxygenfunction:: ecatVoeWrite
    :outline:

.. doxygenfunction:: emVoeWrite

.. dropdown:: **emVoeWrite() Example**

 .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_voe.h
    :language: cpp
    :start-after: DocumentationSnippetsVoeWriteExample
    :end-before: DocumentationSnippetsVoeWriteExample
    :dedent: 1

.. seealso:: 
    - :cpp:func:`emGetCfgSlaveInfo`
    - :cpp:func:`emGetSlaveId`

emVoeWriteReq
*************

.. doxygenfunction:: ecatVoeWriteReq
    :outline:

.. doxygenfunction:: emVoeWriteReq

.. dropdown:: **emVoeWriteReq() Example**

 .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_voe.h
    :language: cpp
    :start-after: DocumentationSnippetsVoeWriteReqExampleApiCall
    :end-before: DocumentationSnippetsVoeWriteReqExampleApiCall
    :dedent: 1

.. seealso:: :cpp:func:`emGetSlaveId`

emVoeRead
*********

.. doxygenfunction:: ecatVoeRead
    :outline:

.. doxygenfunction:: emVoeRead

.. doxygenstruct:: ETHERCAT_MBOX_HEADER
	:members:

.. dropdown:: **emVoeRead() Example**

 .. literalinclude:: ..\..\..\Doc\EcMaster\Snippets\ClassB\mbx_voe.h
    :language: cpp
    :start-after: DocumentationSnippetsVoeReadExample
    :end-before: DocumentationSnippetsVoeReadExample
    :dedent: 1

.. seealso:: :cpp:func:`emGetSlaveId`


emNotify - eMbxTferType_VOE_READ
********************************

The corresponding Slave ID can be found in pMbxTfer->dwTferId.
The MBX data stored in pMbxTfer->pbyMbxTferData may have to be buffered by the client. After emNotify returns the pointer and thus the data is invalid. Access to the memory area pointed to by pMbxTfer-> pbyMbxTferData after returning from emNotify is illegal and the results are undefined.

.. emNotify:: eMbxTferType_VOE_READ
    :pbyInBuf: pMbxTfer - Pointer to a structure of type EC_T_MBXTFER, this structure contains the used mailbox transfer object . To retrieve this VoE mailbox data emVoeRead has to be called.
    :dwInBufSize: Size of the transfer object.
    
emNotify - eMbxTferType_VOE_WRITE
*********************************

VoE mailbox was successfully written to the VoE slave.
The corresponding transfer ID can be found in pMbxTfer->dwTferId. The transfer result is stored in pMbxTfer->dwErrorCode.

.. emNotify:: eMbxTferType_VOE_WRITE
    :pbyInBuf: pMbxTfer - Pointer to a structure of type EC_T_MBXTFER, this structure contains the corresponding mailbox transfer object.
    :dwInBufSize: Size of the transfer object.