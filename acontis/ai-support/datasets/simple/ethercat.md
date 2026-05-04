# EtherCAT overview

**EtherCAT** (Ethernet for Control Automation Technology) is an industrial Ethernet fieldbus standardized as **IEC 61158 Type 12** and **IEC 61784-2**. It is optimized for hard real-time control: short cycle times, deterministic behavior, and efficient use of bandwidth compared with classic “each node parses the full frame” Ethernet approaches.

The technology is promoted and evolved by the **EtherCAT Technology Group (ETG)**. Thousands of vendors ship **EtherCAT slaves** (I/O, drives, gateways, sensors), so systems are typically multi-vendor even when the master stack comes from one supplier.

## Topology and physical layer

- **Line, tree, or ring**: Slaves forward frames along the cable; a ring can add redundancy (often with a dedicated redundancy port on slaves that support it).
- **Physical layer**: Most common is **100 Mbit/s full-duplex** over twisted pair; **EtherCAT P** combines data and power on one cable for certain device classes. Fiber and other physical variants exist for long distances or noise immunity.

## How EtherCAT achieves low latency

EtherCAT uses **processing on the fly** (also described as **fly-by** or **cut-through** handling): each slave reads its outgoing data and inserts its incoming data **while the frame passes through**, with only a few nanoseconds of delay per hop. The frame effectively visits all slaves in order in one logical traversal.

The **EtherCAT master** (typically on a PC, industrial PC, or embedded controller) assembles one or more Ethernet frames containing **EtherCAT datagrams**. Each datagram can target a logical address, a position in the ring, or broadcast-style operations depending on configuration.

## Master and slave roles

- **Master**: Schedules cyclic and acyclic traffic, configures slaves (often via **CANopen over EtherCAT (CoE)** or vendor-specific mailboxes), maps process data to application variables, and—when used—coordinates **Distributed Clocks** (see `distributed_clocks.md`).
- **Slave**: Implements the EtherCAT **ESC** (EtherCAT Slave Controller)—either as ASIC, FPGA, or IP core—and exposes **Sync Managers**, **FMMU** (Fieldbus Memory Management Units), and mailbox protocols to the application processor on the device.

## Process data and sync managers

**Process data** (cyclic I/O) is exchanged through **Sync Managers (SM)** that gate access to ESC memory, often paired with **PDO**-like mappings in CoE. **Free Run**, **SM-synchronized**, and **DC-synchronized** modes determine whether outputs/inputs are aligned only to local ESC timing, to the bus cycle, or to a network-wide time base (Distributed Clocks).

## Mailbox and protocols on EtherCAT

Common mailbox protocols include:

- **CoE** (CANopen over EtherCAT): object dictionary, SDO, PDO mapping—very common for drives and generic I/O.
- **EoE** (Ethernet over EtherCAT): tunnels standard Ethernet for configuration or TCP/IP devices behind a slave.
- **FoE** (File over EtherCAT): firmware download and file transfer.
- **SoE** (Servo over EtherCAT): SERCOS profile over mailbox (often seen in motion).
- **VoE** (Vendor-specific over EtherCAT).

Slave capabilities are described in **ESI** (EtherCAT Slave Information) XML; masters use ESI to identify product features, PDO layout, and DC support.

## Performance characteristics (typical documentation ranges)

Exact numbers depend on topology, frame size, master implementation, and hardware. ETG and vendor materials often cite **sub-millisecond** cycle times for many machines, **high utilization** of 100 Mbit/s due to compact framing, and—when **Distributed Clocks** are used—**sub-microsecond jitter** for synchronized events. Treat these as order-of-magnitude guidance; always validate on target hardware.

## Open-source EtherCAT software (examples)

These are widely referenced in industry and academia; licensing and real-time behavior vary by integration (kernel, RTOS, or user space).

| Project / stack | Role | Notes |
|-----------------|------|--------|
| **SOEM** (Simple Open EtherCAT Master) | Master library (C) | Originated at RT-Labs; lightweight, used in many embedded and research stacks; often paired with a real-time OS or preempt-RT Linux for deterministic cycles. |
| **IgH EtherCAT Master** | Linux kernel master | GPL kernel module + userspace; mature integration with **PREEMPT_RT** Linux for cyclic control. |
| **EtherLab** (tooling / IgH ecosystem) | Configuration, testing | Community and tooling around EtherCAT on Linux (e.g., **ethercat** command-line tool for IgH). |
| **openCONFIGURATOR** (ETG) | Network configuration | Open tool support for ENI/XML configuration workflows used with multiple masters. |

Other stacks and bindings exist (language wrappers, ROS nodes built on SOEM, etc.); the table lists the most commonly cited open master implementations.

## Commercial EtherCAT software and platforms (examples)

| Vendor / product | Role | Notes |
|------------------|------|--------|
| **Beckhoff TwinCAT** | Master + runtime + IDE | Reference ecosystem for EtherCAT; extensive slave portfolio and DC tooling. |
| **Siemens** (e.g., SIMATIC, SINAMICS integration) | Master / motion / drives | EtherCAT as optional fieldbus depending on CPU/platform; common in process and factory automation. |
| **Acontis EC-Master / EC-Engineer** | Master stack + configuration | Commercial master used in embedded and PC-based controllers; supports many RTOS and OS ports. |
| **KPA EtherCAT Studio** | Configuration + master ecosystem | Used with various embedded and PC masters. |
| **National Instruments** (NI-Industrial Communications for EtherCAT) | Master on LabVIEW / PXI / CompactRIO | Common in test and measurement integrated with control. |
| **Other PLC / motion vendors** | Masters on selected CPUs | Examples include Bosch Rexroth, B&R, Omron, Rockwell (via gateways or partner stacks), and many others—**EtherCAT master support is product-line specific**; confirm for each controller model. |

Slave **chips** (ESC) and **modules** are available from vendors such as **Beckhoff**, **Texas Instruments**, **Microchip**, **Renesas**, and others; choosing ESC + PHY and a proven stack is standard for device makers.

## Safety and redundancy

- **Functional safety** over EtherCAT is standardized (e.g., **FSoE**—Safety over EtherCAT) so safety I/O can share the same cable with standard traffic subject to device and system certification.
- **Cable redundancy** and **ring** topologies reduce single-fault downtime when slaves and the master support the appropriate modes.

## Relationship to Distributed Clocks

**Distributed Clocks (DC)** are EtherCAT’s hardware-assisted time synchronization across slaves. They are optional per device but essential for the tightest synchronous sampling and motion. A dedicated note with terminology, mechanisms, and use cases is in **`distributed_clocks.md`**.

## Further reading (authoritative sources)

- [EtherCAT Technology Group (ETG)](https://www.ethercat.org)—specifications, conformance, and technology descriptions.
- IEC standards **61158** and **61784-2** for normative fieldbus definitions (licensed via national bodies or ETG).
