Link Layer
----------

Using one of the following demo application Link Layer options, the |Product| will dynamically load the network driver for the specified network adapter card and use the appropriate network driver to access the Ethernet adapter for EtherCAT©.
:cpp:func:`ShowSyntaxLinkLayer` in :file:`Common/EcSelectLinkLayer.cpp` is called automatically if the Demo application is started without parameters and lists the possibilities.

.. note:: Not all link layers are available on all operating systems or architectures. A detailed view in the form of a matrix can be found in the `developer center <https://developer.acontis.com/>`_.

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLALTERATSE' in ecdemo_cmdline) and not 'EXCLUDE_EMLLALTERATSE' in ecdemo_cmdline

    .. option:: -alteratse <instance> <mode>

        :<instance>:    Device instance 1 = first, 2 = second, ...
        :<mode>:    0 = Interrupt mode | 1= Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLANTAIOS' in ecdemo_cmdline) and not 'EXCLUDE_EMLLANTAIOS' in ecdemo_cmdline

    .. option:: -antaios

        Device instance fixed to 2

        Mode fixed to 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLBCMGENET' in ecdemo_cmdline) and not 'EXCLUDE_EMLLBCMGENET' in ecdemo_cmdline

    .. option:: -bcmgenet <instance> <mode>

        Hardware:   Broadcom BcmGenet
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            
.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLBCMNETXTREME' in ecdemo_cmdline) and not 'EXCLUDE_EMLLBCMNETXTREME' in ecdemo_cmdline

    .. option:: -bcmnetxtreme <instance> <mode>

        Hardware:   Broadcom NetXtreme
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            
.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLBPF' in ecdemo_cmdline) and not 'EXCLUDE_EMLLBPF' in ecdemo_cmdline

    .. option:: -bpf <instance> <mode> <interface> [<prefix>]

        Hardware:   Berkeley Packet Filter, Hardware independent
            :<instance>:    BPF instance (0=first), results to e.g. /dev/bpf0
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<interface>: Name of Ethernet Interface, e.g. wm0
        
        Optional:
            :<prefix>: Prefix of the BPF instance path, e.g. /alt

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLCCAT' in ecdemo_cmdline) and not 'EXCLUDE_EMLLCCAT' in ecdemo_cmdline

    .. option:: -ccat <instance> <mode>

        Hardware:   Beckhoff CCAT
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1= Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLCPSW' in ecdemo_cmdline) and not 'EXCLUDE_EMLLCPSW' in ecdemo_cmdline

    .. option:: -cpsw <instance> <mode> <portpriority> <masterflag> <refboard>

        Hardware:   TI CPSW
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode, 1 = Polling mode
            :<portpriority>:    Low priority (0) or high priority (1)
            :<masterflag>:  (m) Master (Initialize Switch), (s) Slave
            :<RefBoard>:    bone | am3359-icev2 | am437x-idk | am572x-idk | 387X_evm | custom | osdriver

        If custom:
            :<CpswType>:    am33XX | am437X | am57X | am387X
            :<PhyAddress>:  0 ... 31
            :<PhyInterface>:    rmii | gmii | rgmii | osdriver
            :<NotUseDmaBuffers>:    0 = FALSE | 1 = TRUE

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLDPDK' in ecdemo_cmdline) and not 'EXCLUDE_EMLLDPDK' in ecdemo_cmdline

    .. option:: -dpdk <instance> <mode> <port>

        Hardware:   Hardware independent, only available for Linux (including the NXP DPAA).
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:  0 = Interrupt mode (not implemented), 1 = Polling mode
            :<port>:  DPDK port ID, e.g. 0
            
        This option supports a large variety of NICs. Whether a NIC is supported depends on its network driver. For a list of supported network drivers see https://www.dpdk.org.

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLDW3504' in ecdemo_cmdline) and not 'EXCLUDE_EMLLDW3504' in ecdemo_cmdline

    .. option:: -dw3504 <instance> <mode> <RefBoard>

        Hardware:   Synopsys DesignWare 3504-0 Universal 10/100/1000 Ethernet MAC (DW3504)
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<RefBoard>:    Reference Board: intel_atom | lces1 | rd55up06 | r12ccpu | rzn1 | socrates | stm32mp157a-dk1 | custom

        If custom:
            :<DW3504Type>:  intel_atom | cycloneV | lces1 | stm32mp157a-dk1
            :<PhyInterface>:    fixed | mii | rmii | gmii | sgmii | rgmii | osdriver
            :<PhyAddress>:  0 ... 31 (don't use if osdriver)

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLEG20T' in ecdemo_cmdline) and not 'EXCLUDE_EMLLEG20T' in ecdemo_cmdline

    .. option:: -eg20t <instance> <mode>

        Hardware:   Intel EG20T Gigabit Ethernet Controller
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLEMAC' in ecdemo_cmdline) and not 'EXCLUDE_EMLLEMAC' in ecdemo_cmdline

    .. option:: -emac <instance> <mode> <refboard>

        Hardware:   Xilinx LogiCORE IP XPS EMAC
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<RefBoard>:    MC2002E | custom

        If custom:
            :<RegisterBase>:    Register base address as hex value
            :<RegisterLength>:  Register length as hex value
            :<NotUseDmaBuffers>:    0 = FALSE | 1 = TRUE

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLETSEC' in ecdemo_cmdline) and not 'EXCLUDE_EMLLETSEC' in ecdemo_cmdline

    .. option:: -fsletsec <instance> <mode> <refboard>

        Hardware:   Freescale TSEC / eTSEC V1 / eTSEC V2 (VeTSEC)
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<RefBoard>:    p2020rdb | twrp1025 | istmpc8548 | xj_epu20c | twrls1021a | tqmls_ls102xa | custom

        If custom:
            :<PhyAddress>:  0 ... 31
            :<RxIrq>:   Default depending on ETSEC type
            :<NotUseDmaBuffers>:    0 = FALSE | 1 = TRUE

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLFSLFEC' in ecdemo_cmdline) and not 'EXCLUDE_EMLLFSLFEC' in ecdemo_cmdline

    .. option:: -fslfec <instance> <mode> <refboard> [nopinmuxing] [nomacaddr]

        Hardware:   Freescale FEC/ENET
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<RefBoard>:    mars | sabrelite | sabresd | imx28evk | topaz | imxceetul2 | mimxrt1064-evk | imx93evk | custom

        If custom:
            :<FecType>:     imx25 | imx28 | imx53 | imx6 | vf6 | imx7 | imx8 | imx8m | imxrt1064 | imx9
            :<PhyInterface>:    fixed | mii | rmii | rmii50Mhz | gmii | sgmii | rgmii | osdriver
            :<PhyAddress>:  0 ... 31, default 0 (don't use if osdriver)

        Optional:
            :nopinmuxing: no pin muxing

        Optional:
            :nomacaddr: don't read MAC address

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLGEM' in ecdemo_cmdline) and not 'EXCLUDE_EMLLGEM' in ecdemo_cmdline

    .. option:: -gem <instance> <mode> <refboard> [osdriver] [clkdivtype_k26] [nopinmuxing]

        Hardware:   Cadence GEM/MACB
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<RefBoard>:    zc702 | zedboard | microzed | zcu102 | zcu104 | KR260 | rpi5 | polarfire | custom

        If custom:
            :<PhyAddress>:  0 ... 31
            :<PhyConnectionMode>:   MIO (0) or EMIO (1)
            :<UseGmiiToRgmii>:  Use Xilinx GmiiToRgmii converter TRUE (1) or FALSE (0)
            :<GmiiToRgmiiPort>: GmiiToRgmii converter PHY address 0 ... 31
            :<GemType>: zynq7000 | ultrascale | bcm2712 | polarfire 

        Optional:
            :osdriver: PhyInterface osdriver

        Optional:
            :clkdivtype_k26: Clock divisor

        Optional:
            :nopinmuxing: Don't use pin muxing

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLINTELGBE' in ecdemo_cmdline) and not 'EXCLUDE_EMLLI8254X' in ecdemo_cmdline

    .. option:: -intelgbe <instance> <mode> [tts <SendOffset>|tmr] [--nophyctrlonconnect]

        Hardware:   Intel Pro/1000 network adapter card
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
        
        Optional:
            :tts: Enables Real-time Ethernet Driver Time Triggered Send (TTS)
            :<SendOffset>: TTS cyclic frame send offset from cycle start (usec)

        Optional:
            :tmr: Enables Real-time Ethernet Driver Timer

        Optional:
            :\-\-nophyctrlonconnect: Disable PHY control (e.g. PHY reset, PHY PM settings, Gbits Ctrl) on link connection detected

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLI8255X' in ecdemo_cmdline) and not 'EXCLUDE_EMLLI8255X' in ecdemo_cmdline

    .. option:: -i8255x <instance> <mode>

        Hardware:   Intel Pro/100 network adapter card
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLICSS' in ecdemo_cmdline) and not 'EXCLUDE_EMLLICSS' in ecdemo_cmdline

    .. option:: -icss <instance> <mode> <masterflag> <refboard> [<PhyInterface> <PhyAddress>] [nophyreset] [tts <SendOffset>]

        Hardware:   Texas Instruments Board with PRUSS
            :<instance>:    ICSS Port (100 Mbit/s) 1 ... 4
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<MasterFlag>:  (m) Master (Initialize board, mdio, both phy) or (s) Slave
            :<RefBoard>:    am572x-idk | am571x-idk | am3359-icev2 | am574x

        Optional:
            :<PhyInterface>:    mii | osdriver
            :<PhyAddress>:  0 ... 31 (only for mii)

        Optional:
            :nophyreset:  NoPhyReset

        Optional:
            :tts: Enables Real-time Ethernet Driver Time Triggered Send (TTS)
            :<SendOffset>: TTS cyclic frame send offset from cycle start (usec)

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLICSSG' in ecdemo_cmdline) and not 'EXCLUDE_EMLLICSSG' in ecdemo_cmdline

    .. option:: -icssg <instance> <mode> <masterflag> <refboard>

        Hardware:   Texas Instruments AARCH64 Board with Gigabit PRUSS
            :<instance>:    ICSSG Port 1 ... 6
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
            :<MasterFlag>:  (m) Master (Initialize board, mdio, both phy) or (s) Slave
            :<RefBoard>:    am654x-idk

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLL9218I' in ecdemo_cmdline) and not 'EXCLUDE_EMLLL9218I' in ecdemo_cmdline

    .. option:: -l9218i <instance> <mode>

        Hardware:   SMSC LAN9218i/LAN9221
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLLAN743X' in ecdemo_cmdline) and not 'EXCLUDE_EMLLLAN743X' in ecdemo_cmdline

    .. option:: -lan743x <instance> <mode>

        Hardware:   Microchip LAN743x
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    1= Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLNDIS' in ecdemo_cmdline) and not 'EXCLUDE_EMLLNDIS' in ecdemo_cmdline

    .. option:: -ndis <IpAddress> <mode> [--name <AdapterName>] [DisablePromiscuousMode] [DisableForceBroadcast]

        Hardware:   Hardware independent, only available for Windows.
            :<IpAddress>:   IP address of network adapter card, e.g. 192.168.157.2 or 0.0.0.0 if name given
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

        Optional:
            :\-\-name:               Select network adapter by name
            :<AdapterName>:          Service name from HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkCards

        Optional:
            :DisablePromiscuousMode: Disable promiscuous mode

        Optional:
            :DisableForceBroadcast:

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLMULTIPLIER' in ecdemo_cmdline) and not 'EXCLUDE_EMLLEMLLMULTIPLIER' in ecdemo_cmdline

    .. option:: -multiplier <instance> <mode> [--type <type>] --port <port> --link <link parms>

        Hardware:       Beckhoff CUxxxx Ethernet-Port-Multiplier  
            :<instance>:        Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode, for now only polling mode is supported
            :\-\-port:     Multiplier port in use
            :<port>:       0 = X1, 1 = X2, ...
            :\-\-link:     Link parameter of network adapter connected to the uplink port
            :<link parms>: e.g. -intelgbe ...

        Optional:
            :\-\-type:    Multiplier type
            :<type>:      cu2508 = CU2508 Ethernet-Port-Multiplier | et2000 = ET2000 Multichannel Ethernet-Probe

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLREMOTE' in ecdemo_cmdline) and not 'EXCLUDE_EMLLREMOTE' in ecdemo_cmdline

    .. option:: -remote <instance> <mode> <src ip> <src port> <dst ip> <dst port> [--mac] [--rxbuffercnt]

        Hardware:   Hardware independent. Tunnels EtherCAT frames through a TCP socket

            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    1 = Polling mode
            :<src ip>:      Source adapter IP address (listen)
            :<src port>:    Source port number (listen)
            :<dst ip>:      Destination adapter IP address (connect)
            :<dst port>:    Destination port number (connect)
            
        Optional:
            :\-\-mac:           MAC address, formatted as xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx
            :\-\-rxbuffercnt:   Frame buffer count for interrupt service thread (IST)

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLR6040' in ecdemo_cmdline) and not 'EXCLUDE_EMLLR6040' in ecdemo_cmdline

    .. option:: -r6040 <instance> <mode>

        Hardware:   RDC R6040
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLRIN32' in ecdemo_cmdline) and not 'EXCLUDE_EMLLRIN32' in ecdemo_cmdline

    .. option:: -rin32m3 <instance> <mode>

        Hardware:   Renesas R-IN32M3-EC
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLRTL8139' in ecdemo_cmdline) and not 'EXCLUDE_EMLLRTL8139' in ecdemo_cmdline

    .. option:: -rtl8139 <instance> <mode>

        Hardware:   Realtek RTL8139
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLRTL8169' in ecdemo_cmdline) and not 'EXCLUDE_EMLLRTL8169' in ecdemo_cmdline

    .. option:: -rtl8169 <instance> <mode>

        Hardware:   Realtek RTL8168 / RTL8169 / RTL8111
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    0 = Interrupt mode | 1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLRZT1' in ecdemo_cmdline) and not 'EXCLUDE_EMLLRZT1' in ecdemo_cmdline

    .. option:: -rzt1 <instance>

        Hardware:   Renesas RZ/T1
            :<instance>:    Device instance 1 = Port 0 | 2 = Port 1

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLSHETH' in ecdemo_cmdline) and not 'EXCLUDE_EMLLSHETH' in ecdemo_cmdline

    .. option:: -sheth <instance> <mode> <RefBoard>

        Hardware:   Renesas RZG1 or Armadillo-800 EVA or MYIR Remi Pi (Renesas RZ/G2L) or Renesas RX72N Envision Kit
            :<instance>:    Device instance 1 = first, 2 = second, ...
            :<mode>:    1 = Polling mode
            :<RefBoard>:    rzg1e | a800eva | rzg2l | rx72n

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLSNARF' in ecdemo_cmdline) and not 'EXCLUDE_EMLLSNARF' in ecdemo_cmdline

    .. option:: -snarf <adapterName>

        Hardware:   Hardware independent, only available for VxWorks
            :<adapterName>: Adapter name, e.g. fei0

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLSOCKRAW' in ecdemo_cmdline) and not 'EXCLUDE_EMLLSOCKRAW' in ecdemo_cmdline

    .. option:: -sockraw <device> [mode] [--nommaprx] [--promiscuousmode]

        Hardware:   Hardware independent, only available for Linux.
            :<device>:  Network device, e.g. eth1

        Optional:
            :mode: 0 = Interrupt mode | 1 = Polling mode

        Optional:
            :\-\-nommaprx: Disable PACKET_MMAP for receive

        Optional:
            :\-\-promiscuousmode: Enable promiscuous mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLSOCKXDP' in ecdemo_cmdline) and not 'EXCLUDE_EMLLSOCKXDP' in ecdemo_cmdline

    .. option:: -sockxdp <instance> <mode> [queue] [xdpmode]

        Hardware:   Hardware independent, only available for Linux.
            :<device>:  Network device, e.g. eth1
            :<mode>:  0 = Interrupt mode | 1 = Polling mode

        Optional:
            :queue:  Queue Id, e.g. 0

        Optional:
            :xdpmode:  1 = SKB | 2 = DRV | 3 = HW | 4 = DRV_ZEROCOPY

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLSTM32ETH' in ecdemo_cmdline) and not 'EXCLUDE_EMLLSTM32ETH' in ecdemo_cmdline

    .. option:: -stm32eth <instance> <mode>

        Hardware: STM32H7 Ethernet
            :<instance>:  Device instance 1=first, 2=second, ...
            :<mode>:  1 = Polling mode

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLTAP' in ecdemo_cmdline) and not 'EXCLUDE_EMLLTAP' in ecdemo_cmdline

    .. option:: -tap <instance> <mode> <adapterName>

        OpenVPN's Windows TAP
            :<instance>:  Device instance 1=first, 2=second, ...
            :<mode>:  0 = Interrupt mode | 1 = Polling mode
            :<adapterName>:  Adapter name

.. ifconfig:: ('INCLUDE_EMLL_ALL' in ecdemo_cmdline or 'INCLUDE_EMLLWINPCAP' in ecdemo_cmdline) and not 'EXCLUDE_EMLLWINPCAP' in ecdemo_cmdline

    .. option:: -winpcap <ipAddress> <mode>

        Hardware:   Hardware independent, only available for Windows.
            :<ipAddress>:   IP address of network adapter card, e.g. 192.168.157.2
            :<mode>:    0 = Interrupt mode | 1 = Polling mode
