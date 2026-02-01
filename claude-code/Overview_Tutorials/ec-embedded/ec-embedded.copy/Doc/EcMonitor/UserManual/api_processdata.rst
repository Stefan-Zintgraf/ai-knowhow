**********************
Process Data functions
**********************

emonGetProcessData
******************

.. doxygenfunction:: emonGetProcessData

emonGetProcessDataBits
**********************

.. doxygenfunction:: emonGetProcessDataBits

.. seealso:: :cpp:func:`emonGetProcessData`

emonGetProcessImageInputPtr
***************************

.. doxygenfunction:: emonGetProcessImageInputPtr

emonGetProcessImageOutputPtr
****************************

.. doxygenfunction:: emonGetProcessImageOutputPtr

emonFindInpVarByName
********************

.. doxygenfunction:: emonFindInpVarByName

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

emonFindInpVarByNameEx
**********************

.. doxygenfunction:: emonFindInpVarByNameEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`

emonFindOutpVarByName
*********************

.. doxygenfunction:: emonFindOutpVarByName

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO`

emonFindOutpVarByNameEx
***********************

.. doxygenfunction:: emonFindOutpVarByNameEx

.. seealso:: :cpp:struct:`EC_T_PROCESS_VAR_INFO_EX`
    
emonIoControl - EC_IOCTL_GET_PDMEMORYSIZE
*****************************************

Get the process data image size. This information may be used to provide process data image storage from outside the |Product| core. 
This IOCTL is to be called after :cpp:func:`emonConfigureNetwork`.

.. emonIoControl:: EC_IOCTL_GET_PDMEMORYSIZE
    :pbyOutBuf: Pointer to memory where the memory size information will be stored (type: EC_T_MEMREQ_DESC).
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.
    
.. doxygenstruct:: EC_T_MEMREQ_DESC
    :members:

    
Process Data access functions
*****************************

EC_COPYBITS
===========

.. doxygendefine:: EC_COPYBITS
    
.. seealso:: 
    - :c:macro:`EC_SETBITS` 
    - :c:macro:`EC_GETBITS`
    
.. figure:: ../Media/EC_COPYBITS.png
    :alt: 
    
.. code-block:: cpp
    
    EC_T_BYTE pbySrc[] = {0xF4, 0xED, 0x69, 0xA5};
    EC_T_BYTE pbyDst[] = {0x00, 0x00, 0x00, 0x00};
    EC_COPYBITS(pbyDst, 3, pbySrc, 6, 22);
    
    /* pbyDst now contains 0xB8 0x3C 0xAC 0x00 */
    
EC_GET_FRM_WORD
===============

.. doxygendefine:: EC_GET_FRM_WORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_WORD wResult = 0;
    
    wResult = EC_GET_FRM_WORD(byFrame);
    /* wResult is 0xF401 on little endian systems */
    
    wResult = EC_GET_FRM_WORD(byFrame + 5);
    /* wResult is 0x6000 on little endian systems */
    
    wResult = EC_GET_FRM_WORD(byFrame + 2);
    /* wResult is 0x85DD on little endian systems */

EC_GET_FRM_DWORD
================

.. doxygendefine:: EC_GET_FRM_DWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_DWORD dwResult = 0;
    
    dwResult = EC_GET_FRM_DWORD(byFrame);
    /* dwResult is 0x85DDF401 on little endian systems */
    
    dwResult = EC_GET_FRM_DWORD(byFrame + 5);
    /* dwResult is 0x00C16000 on little endian systems */
    
    dwResult = EC_GET_FRM_DWORD(byFrame + 2);
    /* dwResult is 0x000385DD on little endian systems */
    
EC_GET_FRM_QWORD
================

.. doxygendefine:: EC_GET_FRM_QWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_UINT64 ui64Result = 0;
    
    ui64Result = EC_GET_FRM_QWORD(byFrame + 1);
    /* wResult is 0x00C160000385DDF4 on little endian systems */

EC_GETBITS
==========

.. doxygendefine:: EC_GETBITS

.. seealso:: 
    - :c:macro:`EC_GET_FRM_WORD`
    - :c:macro:`EC_GET_FRM_DWORD` 
    - :c:macro:`EC_GET_FRM_QWORD`

EC_TESTBIT
**********

.. doxygendefine:: EC_TESTBIT

emonIoControl - EC_IOCTL_SET_IGNORE_INPUTS_ON_WKC_ERROR
*******************************************************

Ignore inputs on WKC error

.. emonIoControl:: EC_IOCTL_SET_IGNORE_INPUTS_ON_WKC_ERROR
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Ignore inputs on WKC error.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will ignore inputs data of cyclic commands on WKC error.
By default input data are updated if WKC is non zero. If WKC is not matching the expected value a notification :ref:`notification:emonNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emonIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR
*****************************************************

Set inputs to zero on WKC error

.. emonIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ERROR
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on WKC error.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on WKC error.
By default input data are updated if WKC is non zero. If WKC is not matching the expected value a notification :ref:`notification:emonNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emonIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO
****************************************************

Set inputs to zero on WKC is zero

.. emonIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_WKC_ZERO
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on WKC is zero.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on WKC is zero.
By default input data are ignored on WKC is zero and remain unchanged. If WKC is not matching the expected value a notification :ref:`notification:emonNotify - EC_NOTIFY_CYCCMD_WKC_ERROR` is generated and the application must consider this status for the current cycle.

emonIoControl - EC_IOCTL_SET_ZERO_INPUTS_ON_FRAME_LOSS
******************************************************

Set inputs to zero on frame loss

.. emonIoControl:: EC_IOCTL_SET_ZERO_INPUTS_ON_FRAME_LOSS
    :pbyInBuf: Pointer to value of EC_T_BOOL. EC_TRUE: Set inputs to zero on frame loss.
    :dwInBufSize: Size of the input buffer provided at pbyInBuf in bytes.

Calling this IOCTL with :c:macro:`EC_TRUE` as parameter will set inputs to zero on frame loss.
By default input data are ignored on frame loss and remain unchanged.