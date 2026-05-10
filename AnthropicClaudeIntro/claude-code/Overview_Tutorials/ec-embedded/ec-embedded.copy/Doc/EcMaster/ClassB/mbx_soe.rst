************************************************************
Servo Drive Profil according to IEC61491 over EtherCAT (SoE)
************************************************************

The SoE Service Channel (SSC) is equivalent to the IEC61491 Service Channel used for non-cyclic data exchange. The SSC uses the EtherCAT mailbox mechanism. It allows accessing IDNs and their elements.

For extended informations about SoE see the IEC IEC61800-7-300 document 22G185eFDIS.

Following services are available:

- Write IDN:
    With :cpp:func:`emSoeWrite` the data and elements of an IDN which are writeable can be written.
- Read IDN:
    With :cpp:func:`emSoeRead` the data and elements of an IDN can be read.
- Procedure command Execution:
    With :cpp:func:`emSoeWrite` also procedure commands can be started. Procedure commands are special IDNs, which invokes fixed functional processes. When proceeding is finished, a notification will be received. To abort a running command execution :cpp:func:`emSoeAbortProcCmd` has to be called.
- Notification:
    In case of an notification all registered clients will get this notification. A notification will be received when proceeding of a command has finished. To register a client :cpp:func:`emRegisterClient` must be called.
- Emergency:
    The main purpose of this service is to provide additional information about the slave for debugging and maintenance. In case of an emergency, all registered clients will get notified. To register a client :cpp:func:`emRegisterClient` must be called.

Abbreviations:

- IDN:
    identification number: Designation of operating data under which a data block is preserved with its attribute, name, unit, minimum and maximum input values, and the data.
- SoE:
    IEC 61491 Servo drive profile over EtherCAT (SoE)
- SSC:
    SoE Service Channel (non-cyclic data exchange)

SoE ElementFlags
****************

With the ElementFlags each element of an IDN can be addressed. The ElementFlags indicating which elements of an IDN are read or written. The ElementFlags indicating which data will be transmitted in the SoE data buffer.

.. datatemplate:xml:: SOE_BM_ELEMENTFLAGS
    :source: ../_build/doxygen/xml/combined.xml
    :template: doxygroups.jinja

SoE IDN coding
**************

The parameter addressing area consist of 4096 different standard IDNs, each with 8 parameter sets and 4096 manufacturer specific IDNs, each with 8 parameter sets.

.. figure:: ../Media/soe.png
    :align:     center
    :alt:

The Control unit cycle time (TNcyc) which is an standard IDN S-0-0001 equates to wIDN = 0x1
The first manufacturer specific IDN P-0-0001 equates to wIDN = 0x8001

emSoeWrite
**********

.. doxygenfunction:: ecatSoeWrite
    :outline:

.. doxygenfunction:: emSoeWrite

.. seealso:: :cpp:func:`emGetSlaveId`

emSoeWriteReq
*************

Requests an SoE SSC Write and returns immediately.

.. doxygenfunction:: ecatSoeWriteReq
    :outline:

.. doxygenfunction:: emSoeWriteReq

.. seealso::
    - :cpp:func:`emSoeWrite`
    - :cpp:func:`emGetSlaveId`

emSoeRead
*********

.. doxygenfunction:: ecatSoeRead
    :outline:

.. doxygenfunction:: emSoeRead

.. seealso:: :cpp:func:`emGetSlaveId`

emSoeReadReq
************

.. doxygenfunction:: ecatSoeReadReq
    :outline:

.. doxygenfunction:: emSoeReadReq

.. seealso::
    - :cpp:func:`emSoeRead`
    - :cpp:func:`emGetSlaveId`

emSoeAbortProcCmd
*****************

.. doxygenfunction:: ecatSoeAbortProcCmd
    :outline:

.. doxygenfunction:: emSoeAbortProcCmd

.. seealso:: :cpp:func:`emGetSlaveId`

emConvertEcErrorToSoeError
**************************

.. doxygenfunction:: ecatConvertEcErrorToSoeError
    :outline:

.. doxygenfunction:: emConvertEcErrorToSoeError


emNotify - EC_NOTIFY_SOE_MBXSND_WKC_ERROR
*****************************************

This error will be indicated in case the working counter of a SoE mailbox write command was not set to the expected value of 1.
Detailed error information is stored in structure :cpp:struct:`EC_T_WKCERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.

emNotify - EC_NOTIFY_SOE_WRITE_ERROR
************************************

This error will be indicated in case SoE mailbox write command responded with an error.
Detailed error information is stored in structure :cpp:struct:`EC_T_INITCMD_ERR_DESC` of :cpp:struct:`EC_T_ERROR_NOTIFICATION_DESC`.



