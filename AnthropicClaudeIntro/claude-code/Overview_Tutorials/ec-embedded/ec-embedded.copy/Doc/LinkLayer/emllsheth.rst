The parameters to the Renesas Real-time Ethernet Driver SuperH are setup-specific.
The function :cpp:func:`CreateLinkParmsFromCmdLineSHEth` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance. 

.. doxygenstruct:: EC_T_LINK_PARMS_SHETH
    :members:

.. doxygenenum:: EC_T_SHETH_TYPE

SHEth link status update
************************

On some targets like `Armadillo A800 eva` the link status can't be obtained directly by reading MAC PHY status register without access to the MII bus. Accessing the bus would violate timing constraints and is therefore not possible.

The following IOCTL updates the link status and accesses the PHY. The IOCTL is blocking and may therefore be not called from the JobTask's context.

.. code-block:: cpp

   dwRes = emIoControl((EC_IOCTL_LINKLAYER | EC_LINKIOCTL_UPDATE_LINKSTATUS), EC_NULL);

:cpp:func:`ecLinkGetStatus` always retuns the last known link status.


SHEth usage under Linux
***********************

Due to lacking unbind-feature of the SuperH driver, the target's Kernel must not load the SuperH driver when starting. If the SuperH was built as a module, it can be renamed to ensure, it never gets loaded. If it was compiled into the Kernel, the Kernel needs to be recompiled without it.
