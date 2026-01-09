*****************************
Process Data Access Functions
*****************************

esGetProcessImageInputPtr
*************************

.. doxygenfunction:: esGetProcessImageInputPtr

The size of the process data image input area is returned by :ref:`api_general:esIoControl - EC_IOCTL_GET_PDMEMORYSIZE` and :cpp:func:`esRegisterClient` at :cpp:member:`EC_T_REGISTERRESULTS::dwPDInSize`. 

.. seealso::
    - :cpp:func:`esConfigureNetwork`
    - :ref:`api_general:esIoControl - EC_IOCTL_GET_PDMEMORYSIZE`
    - :ref:`api_general:esIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB`
    - :cpp:func:`esExecJob` ( :c:enum:`eUsrJob_ProcessAllRxFrames`) in case of polling mode

esGetProcessImageOutputPtr
**************************

.. doxygenfunction:: esGetProcessImageOutputPtr

The size of the process data image output area is returned by :ref:`api_general:esIoControl - EC_IOCTL_GET_PDMEMORYSIZE` and :cpp:func:`esRegisterClient` at :cpp:member:`EC_T_REGISTERRESULTS::dwPDOutSize`. 

.. seealso::
    - :cpp:func:`esConfigureNetwork`
    - :ref:`api_general:esIoControl - EC_IOCTL_GET_PDMEMORYSIZE`
    - :ref:`api_general:esIoControl - EC_IOCTL_REGISTER_CYCFRAME_RX_CB`
    - :cpp:func:`esExecJob` ( :c:enum:`eUsrJob_ProcessAllRxFrames`) in case of polling mode

.. raw:: latex

    \newpage

EC_COPYBITS
***********

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
***************

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
****************

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
****************

.. doxygendefine:: EC_GET_FRM_QWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[] = {0x01, 0xF4, 0xDD, 0x85, 0x03, 0x00, 0x60, 0xC1, 0x00};
    EC_T_UINT64 ui64Result = 0;
    
    ui64Result = EC_GET_FRM_QWORD(byFrame + 1);
    /* wResult is 0x00C160000385DDF4 on little endian systems */

EC_SET_FRM_WORD
***************

.. doxygendefine:: EC_SET_FRM_WORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];
    
    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);
    
    EC_SET_FRM_WORD(byFrame + 1, 0x1234);
    /* byFrame = FF 34 12 FF FF FF ... */

EC_SET_FRM_DWORD
****************

.. doxygendefine:: EC_SET_FRM_DWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];
    
    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);
    
    EC_SET_FRM_DWORD(byFrame + 1, 0x12345678);
    /* byFrame = FF 78 56 34 12 FF ... */

EC_SET_FRM_QWORD
****************

.. doxygendefine:: EC_SET_FRM_QWORD

.. code-block:: cpp

    EC_T_BYTE byFrame[32];
    
    /* Initialize the frame buffer */
    OsMemset(byFrame, 0xFF, 32);
    
    EC_SET_FRM_QWORD(byFrame + 1, 0xFEDCBA9876543210);
    /* byFrame = FF 10 32 54 76 98 BA DC FE FF FF ... */

EC_GETBITS
**********

.. doxygendefine:: EC_GETBITS

.. seealso:: 
    - :c:macro:`EC_GET_FRM_WORD`
    - :c:macro:`EC_GET_FRM_DWORD` 
    - :c:macro:`EC_GET_FRM_QWORD`

EC_SETBITS
**********

.. doxygendefine:: EC_SETBITS

.. seealso:: 
    - :c:macro:`EC_SET_FRM_WORD`
    - :c:macro:`EC_SET_FRM_DWORD`
    - :c:macro:`EC_SET_FRM_QWORD`

EC_COPYBIT
**********

.. doxygendefine:: EC_COPYBIT

EC_TESTBIT
**********

.. doxygendefine:: EC_TESTBIT

EC_SETBIT
*********

.. doxygendefine:: EC_SETBIT

EC_CLRBIT
*********

.. doxygendefine:: EC_CLRBIT

esGetProcessData
****************

.. doxygenfunction:: esGetProcessData

esSetProcessData
****************

.. doxygenfunction:: esSetProcessData

esSetProcessDataBits
********************

.. doxygenfunction:: esSetProcessDataBits

esGetProcessDataBits
********************

.. doxygenfunction:: esGetProcessDataBits
