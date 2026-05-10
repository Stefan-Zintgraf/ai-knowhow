The Real-time Ethernet Driver emllDpdk is based on the Data Plane Development Kit (DPDK V23.11). See https://www.dpdk.org for more information.  
It does not need the atemsys driver and uses Ethernet adapters that are bound to the DPDK interface. 

The parameters to emllDpdk are setup-specific. The function :cpp:func:`CreateLinkParmsFromCmdLineDpdk` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize emllDpdk.

.. doxygenstruct:: EC_T_LINK_PARMS_DPDK
    :members:
 
.. note:: 
    - Root privileges are required.
    - emllDpdk increases the stack size by DPDK_SEND_BURST_STACK_SIZE.

The network interface must be bound according to the interface type PCI or SOC:

DPDK for PCI device
*******************

First, the driver may need to be loaded, as it may be unloaded per default. 

.. prompt:: bash
        
    sudo modprobe uio_pci_generic
        
Next the device needs to be bound with :file:`dpdk-devbind.py`. Therefore, the PCI addresses have to be found out by calling

.. prompt:: bash
   
    ./usertools/dpdk-devbind.py --status

The output will look like this (here the addresses of the PCI ports are 02:00.0 and 02:00.1, the card is an Intel X710, to be bound to the DPDK i40e driver):

.. code-block::
     
    Other Network devices
    =====================
    0000:02:00.0 'Ethernet Controller X710 for 10GBASE-T 15ff' unused=i40e,vfio-pci
    0000:02:00.1 'Ethernet Controller X710 for 10GBASE-T 15ff' unused=i40e,vfio-pci

For each port to be bound to emllDpdk, call
   
.. prompt:: bash    
        
    ./usertools/dpdk-devbind.py --bind=uio_pci_generic <address>

Example:

.. prompt:: bash    
    
    ./usertools/dpdk-devbind.py --bind=uio_pci_generic 02:00.0
        
Check https://doc.dpdk.org/guides/linux_gsg/linux_drivers.html for more information on the drivers.
        
DPDK for DPAA
*************

Port specific numbering
-----------------------

The LS1046A Ethernet Port IDs within the Linux device tree (:file:`dts`) may be non-linear, e.g. 1, 5, 6, 10, whereas the corresponding DPDK Port IDs are linear (0, 1, 2, ...).

The following example demonstrates how the DPDK Port ID can be determined from the Ethernet Port ID within the Linux device tree:

+------+------+
| DPDK | dts  |
+------+------+
| 0    | 1    | 
+------+------+
| 1    | 5    |
+------+------+
| 2    | 6    |
+------+------+
| 3    | 10   | 
+------+------+

Reassigning Ports to DPAA and Linux in DTB/DTS
----------------------------------------------

The following changes make the LS1046A ports (i.e. ports 1, 5, 6, 10) available to the emllDpaa, the Linux boot file :file:`/boot/fsl-ls1046a-frwy-sdk.dts/dtb`.

.. note:: ethernet@0 (Port 1) is known to be not assignable to emllDpaa for FRWY-LS1046A.

The section dpaa-extended-args must be extended:

.. code-block:: dts
    :emphasize-lines: 3-

    chosen {
        stdout-path = "serial0:115200n8";
        name = "chosen";

        dpaa-extended-args {

            fman0-extd-args {
                cell-index = <0>;
                compatible = "fsl,fman-extended-args";
                dma-aid-mode = "port";

                fman0_rx0-extd-args {
                    cell-index = <0>;
                    compatible = "fsl,fman-port-1g-rx-extended-args";
                    vsp-window = <8 0>;
                };

                fman0_tx0-extd-args {
                    cell-index = <0>;
                    compatible = "fsl,fman-port-1g-tx-extended-args";
                };

                fman0_rx1-extd-args {
                    cell-index = <1>;
                    compatible = "fsl,fman-port-1g-rx-extended-args";
                    vsp-window = <8 0>;
                };

                fman0_tx1-extd-args {
                    cell-index = <1>;
                    compatible = "fsl,fman-port-1g-tx-extended-args";
                };
            };

            fman1-extd-args {
                cell-index = <1>;
                compatible = "fsl,fman-extended-args";
                dma-aid-mode = "port";
                fman1_rx0-extd-args {
                    cell-index = <0>;
                    compatible = "fsl,fman-port-1g-rx-extended-args";
                    vsp-window = <8 0>;
                };

                fman1_tx0-extd-args {
                    cell-index = <0>;
                    compatible = "fsl,fman-port-1g-tx-extended-args";
                };

                fman1_rx1-extd-args {
                    cell-index = <1>;
                    compatible = "fsl,fman-port-1g-rx-extended-args";
                    vsp-window = <8 0>;
                };

                fman1_tx1-extd-args {
                    cell-index = <1>;
                    compatible = "fsl,fman-port-1g-tx-extended-args";
                };
            };
        };
    };

Furthermore some or all ports must be assigned to DPDK instead of the native Linux driver in the section ``fsl,dpaa`` as follows:

.. code-block:: dts
    :emphasize-lines: 9, 13-15

    fsl,dpaa {
        compatible = "fsl,ls1046a\\0fsl,dpaa\\0simple-bus";
        dma-coherent;
        phandle = <0x85>;

        /* assign Port 1 (ethernet@0) to emllDpaa (all ports assigned to emllDpaa must be contiguous at the start) */
            
        ethernet@0 {
            compatible = "fsl,dpa-ethernet-init";
            fsl,fman-mac = <0x34>;
            dma-coherent;

            fsl,bman-buffer-pools = <0x35 0x36 0x37>;
            fsl,qman-frame-queues-rx = <0x50 0x01 0x51 0x01>;
            fsl,qman-frame-queues-tx = <0x70 0x01 0x71 0x01>;
        };

        /* port listed in BSP, but not implemented */
            
        ethernet@1 {
            compatible = "fsl,dpa-ethernet";
            fsl,fman-mac = <0x38>;
            dma-coherent;
            status = "disabled";
        };
            
        ...

        /* assign Port 10 (ethernet@9) to the native Linux driver */
            
        ethernet@9 {
            compatible = "fsl,dpa-ethernet";
            fsl,fman-mac = <0x3e>;
            dma-coherent;
        };
        ...
    };
    
Linux System Requirements
*************************

- Kernel configuration

In the Fedora OS and other common distributions, such as Ubuntu, or Red Hat Enterprise Linux, the vendor supplied kernel configurations can be used to run most DPDK applications.
For other kernel builds, options which should be enabled for DPDK include:

.. code-block::

      HUGETLBFS        
      PROC_PAGE_MONITOR support
      
- Required Tools, Libraries and further system requirements can be checked under https://doc.dpdk.org/guides/linux_gsg/sys_reqs.html 

Huge pages setup
****************

Create huge pages (not persistent)

.. prompt:: bash
        
    mkdir -p /dev/hugepages
    mountpoint -q /dev/hugepages || mount -t hugetlbfs nodev /dev/hugepages
    echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages

Limitations
***********

If the adapter needs to be used multiple times, for cable redundancy or calling |EcatInitStack| multiple times,
the application must set EC_T_LINK_PARMS_DPDK::bEalInitDeinitByApp = EC_TRUE 
and call rte_eal_init() and rte_eal_cleanup() itself.

To initialize DPDK following call is needed:

.. code-block::

      rte_eal_init();

To deinitialize DPDK following calls are needed:

.. code-block::

      rte_eth_dev_close(dwPortId);
      rte_eal_cleanup();

