************
Introduction
************

The EC-EoE Gateway is a helper application to enable virtual networking
with EoE devices.

The *Network Driver for EoE Endpoint* is the interface to a virtual
network (TAP) adapter installed at the operating system and is part of
the EC-EoE Gateway. The RAS connection is a TCP/IP connection between
the EC-EoE Gateway and the Master. The Master must open the *RAS Server*
TCP port in order that the EC-EoE Gateway can connect using its *RAS
Client*.

A Third-Party Tool can use TCP/IP to communicate with slave.

.. figure:: ../Media/eoe-gateway-intro.png
    :alt:

*************
Prerequisites
*************

EC-Master installation
**********************

The IPv4 address and TCP port and the instance ID (default: 0) of the
EC-Master is needed for configuration.

The EC-Master application must open the *RAS Server* TCP port (default:
6000, API `emRasSrvStart(),` `-sp`).

Firewalls must be configured accordingly to allow the TCP connection.

Information about IPv4 networks, EoE IP addresses (ENI)
*******************************************************

The IPv4 addresses of the EoE devices are manually assigned in the
EtherCAT network configuration using EC-Engineer or another EtherCAT
configuration tool and are finally part of the ENI file loaded at
EC-Master.

The EoE devices and the TAP adapter must be **in the same IPv4 subnet**
and it must be **independent of the other network addresses** used on
the EC-EoE-Gateway system.

The IP addresses of the slave must be in the same subnet as of the
EC-EoE-Gateway (TAP adapter).

The ENI file itself is not needed at the EC-EoE-Gateway with RAS.
