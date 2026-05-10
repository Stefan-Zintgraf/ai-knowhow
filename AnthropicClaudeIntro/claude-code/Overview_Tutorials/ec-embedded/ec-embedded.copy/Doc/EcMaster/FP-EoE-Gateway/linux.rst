************************
EC-EoE Gateway for Linux
************************

Installation 
************

#. The EC-EoE Gateway package contains all needed files to be extracted,
   e.g. in :file:`/opt/EC-EoE-Gateway`.

#. The following steps install the linux TAP adapter on the EC-EoE
   Gateway’s Linux system:

   .. prompt:: bash
        
      apt-get install uml-utilities
      tunctl -t tap0

#. IPv4 configuration

   The TAP’s subnet must match the configured IP addresses of the EoE
   slaves and must be independent from all existing networks, e.g.
   LAN, Wifi, etc..

   Example of independent subnets for LAN and EoE:

   .. code-block::

   	LAN: 192.168.0.1, netmask 255.255.255.0 (192.168.0.x)
   	EoE: 192.168.2.1, netmask 255.255.255.0 (192.168.2.x)

   The following steps configures the interface (non-persistent!):

   .. prompt:: bash

   	ip link set tap0 up
   	ip addr add 192.168.2.1/24 dev tap0
   	ifconfig tap0 mtu 200 up

Persistent IPv4 setup depends on the various ways available on Linux
according to distribution, installed network manager, etc. and is
therefore beyond the scope of this manual. The Linux distribution’s user
manual or support can provide the needed information.

Ubuntu systemd service
**********************

The following files to integrate EC-EoE-Gateway as an Ubuntu systemd
service are contained in the package.

The following files from :file:`/opt/EC-EoE-Gateway/Files/Linux` should be
placed in :file:`/etc`:

-  :file:`/etc/systemd/system/eceoegateway.service`

-  :file:`/etc/eceoegateway.conf`

Configuration and run control
=============================

#. All configuration options are in :file:`/etc/eceoegateway.conf`:

   .. code-block::

	RAS_SERVER_IP=127.0.0.1 # RAS server IP address
	RAS_SERVER_PORT=6000 # RAS server TCP port
	TAP_NAME=tap0 # TAP adapter name
	EC_EOE_GATEWAY_INSTALL_DIR=/opt/EC-EoE-Gateway # installation directory
	EC_EOE_GATEWAY_OS=Linux
	EC_EOE_GATEWAY_ARCH=x64

#. `systemctl start eceoegateway` starts the service

#. `systemctl enable eceoegateway` enables startup on boot. This
   needs IPv4 configured persistently.

#. `service eceoegateway status` shows the status of the service

Logging
=======

Log messages from the EC-EoE-Gateway are available as follows:

-  `journalctl -f -u eceoegateway.service`

-  Log files in :file:`/var/log/eceoegateway`

Manually running EcEoeGateway application
*****************************************

Instead of running EC-EoE-Gateway as an Ubuntu systemd service, it can
also be manually sstarted as a standalone application.

The EcEoeGateway binary must be started with command line parameters,
e.g.

.. prompt:: bash

    LD_LIBRARY_PATH=. ./EcEoeGateway -eoetap tap0 -rem 127.0.0.1:6000 -t 0 -log /var/log/eceoegateway

The full command line usage is printed to the console if the
EcEoeGateway binary is started without arguments.
