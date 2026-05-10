*********
Diagnosis
*********

emonGetDiagnosisImagePtr
************************

.. doxygenfunction:: emonGetDiagnosisImagePtr

.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::wWkcStateDiagOffsIn`
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::wWkcStateDiagOffsOut`

emonGetDiagnosisImageSize
*************************

.. doxygenfunction:: emonGetDiagnosisImageSize

.. seealso::
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::wWkcStateDiagOffsIn`
    - :cpp:member:`EC_T_CFG_SLAVE_INFO::wWkcStateDiagOffsOut`

emonGetMasterSyncUnitInfoNumOf
******************************

.. doxygenfunction:: emonGetMasterSyncUnitInfoNumOf

emonGetMasterSyncUnitInfo
*************************

.. doxygenfunction:: emonGetMasterSyncUnitInfo

:c:macro:`MSU_ID_ALL_INFO_ENTRIES` retrieves the information from all master sync units at once. The application must ensure that pMsuInfo is capable for all entries.

.. doxygenstruct:: EC_T_MSU_INFO
    :members:

.. seealso:: :cpp:func:`emonGetMasterSyncUnitInfoNumOf`

emonGetSlaveStatistics
**********************

.. doxygenfunction:: emonGetSlaveStatistics

.. seealso::
    - :ref:`api_diag:emonIoControl - EC_IOCTL_GET_SLVSTATISTICS`
    - :cpp:func:`emonGetSlaveId`

emonIoControl - EC_IOCTL_GET_SLVSTATISTICS
******************************************

Get Slave's statistics counter. Counters are collected on a regularly base (default: off) and show errors on Real-time Ethernet Drivers.

.. emonIoControl:: EC_IOCTL_GET_SLVSTATISTICS
    :pbyInBuf: Pointer to a EC_T_DWORD type variable containing the slave id.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.
    :pbyOutBuf: Pointer to struct EC_T_SLVSTATISTICS_DESC
    :dwOutBufSize: Size of the output buffer provided at pbyOutBuf in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. doxygenstruct:: EC_T_SLVSTATISTICS_DESC
    :members:

emonClearSlaveStatistics
************************

.. doxygenfunction:: emonClearSlaveStatistics

.. note:: Only the buffered error register values are deleted. The actual counters on the slaves remain unchanged.

.. seealso:: :cpp:func:`emonGetSlaveId`

emonIoControl - EC_IOCTL_CLR_SLVSTATISTICS
******************************************

Clear all buffered error registers for all slaves. The actual counters on the slaves remain unchanged.

.. emonIoControl:: EC_IOCTL_CLR_SLVSTATISTICS

emonIoControl - EC_IOCTL_SB_STATUS_GET
**************************************

This call will get the status of the last bus scan.

.. emonIoControl:: EC_IOCTL_SB_STATUS_GET
    :pbyOutBuf: Pointer to EC_T_SB_STATUS_NTFY_DESC.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.

.. seealso:: :ref:`notification:emonNotify - EC_NOTIFY_SB_STATUS`
