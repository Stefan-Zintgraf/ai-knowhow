The parameters to the Real-time Ethernet Driver ETSEC are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineETSEC` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_ETSEC
    :members: 

.. doxygenenum:: EC_T_ETSEC_TYPE 

ETSEC supported MAC's
*********************

- TSEC (not tested): Legacy hardware. Should be supported, because eTSEC is compatible to TSEC if the enhanced functionality is not used.
- eTSEC v1 (tested): This chip is used for QorIQ (i.e. P2020E) and PowerQUICC devices  (i.e. MPC8548). It has 4k of IO memory.
- eETSEC v2, also called vETSEC, v read as "virtualization" (tested): This chip is used for newer QorIQ devices (i.e. P1020). It has 12k of IO memory (4k MDIO, 4k Register group0, 4k Register group1)

    
Shared MII bus
**************

The driver will access the Ethernet PHY for the following reasons:

- Check for link (or timeout), if the driver instance is opened.
- Configure MAC according to the auto-negotiated PHY speed (mandatory).
- Check link (and reconfigure MAC) during cyclic run. Therefore :c:macro:`EC_LINKIOCTL_UPDATE_LINKSTATUS` should not be called explicitly in parallel!

.. note:: The external PHYs are connected physically to the MII bus of the first eTSEC (and/or eTSEC3, depending on SoC type). From SoC reference manuals:
   "14.5.3.6.6 MII Management Configuration Register (MIIMCFG)
   ... Note that MII management hardware is shared by all eTSECs. Thus, only through the MIIM registers of eTSEC1 can external PHYs be accessed and configured."

That means that the acontis TSEC / eTSEC driver will also mmap the register set of the corresponding eTSEC. The following initialization parameters are used to specify the MII settings:

#. Memory map of eTSEC which will manage the MII bus (connection of external PHY's):

.. code-block:: cpp
    
    poDrvSpecificParam->dwPhyMdioBase = dwCcsrbar + 0x24000;

#. Dummy address assigned to internal TBI PHY. Use any address (from 0 .. 31)
   which will not collide with any of the physical PHY's addresses:

.. code-block:: cpp

    poDrvSpecificParam->dwTbiPhyAddr = 16;

Locking 
*******

The optional lock is acquired each time the MDIO register (specified by poDrvSpecificParam->dwPhyMdioBase) are accessed:

.. code-block:: cpp
        
    poDrvSpecificParam->oMiiBusMtx = EC_NULL;
    
    /* implement locking by using return value of LinkOsCreateLock(eLockType_DEFAULT); */

Link check
**********

The driver's API function EcLinkGetStatus (pfEcLinkGetStatus) is called by the |Product| stack. On eTSEC the link status can't be obtained directly by reading eTSEC registers without access to the MII bus (Use mutex, poll for completion). Accessing the bus would violate timing constraints and is therefore not possible.

The following IOCTL updates the link status and accesses the PHY. The IOCTL is blocking and may therefore be not called from the JobTask's context.
I.e. use:

.. ifconfig:: 'EC-Master' in product

    .. code-block:: cpp

        dwRes = emIoControl(( EC_IOCTL_LINKLAYER | EC_LINKIOCTL_UPDATE_LINKSTATUS), EC_NULL);

.. ifconfig:: 'EC-Simulator' in product

    .. code-block:: cpp

        dwRes = esIoControl(dwSimulatorInstanceId, EC_IOCTL_LINKLAYER | EC_LINKIOCTL_UPDATE_LINKSTATUS, EC_NULL);

EcLinkGetStatus always returns the last known link status.

Fixed Link
**********

PHY access can be effectively disable at all to avoid concurrent access if link speed and mode as define to be fixed. This functionality is mainly provided for L2-Switch-IC's like Vertesse VSC7385 which haven't any PHY and are attached to the eTSEC MAC with fixed speed and mode.

The driver's open function will not wait until the link is up on |Product| start up. Auto-negotiation of following PHY's are not affected by this parameter and still active. There is no forced link and no PHY access at all.

Parameters for fixed link:

.. code-block:: cpp

    pETSECParam->dwPhyAddr 	= ETSEC_FIXED_LINK;
    pETSECParam->dwFixedLinkVal	= ETSEC_LINKFLAG_1000baseT_Full | ETSEC_LINKFLAG_LINKOK;