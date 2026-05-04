# Distributed Clocks in EtherCAT

In EtherCAT, **Distributed Clocks (DC)** means that multiple devices on the bus each have a local hardware clock (inside or associated with the **ESC**), and those clocks are **synchronized** so the EtherCAT system shares a **common time base**. The master configures which slave acts as the **reference clock** and aligns all other **DC-capable** slaves (and typically the master’s scheduling) to that reference.

This document focuses only on DC concepts, mechanisms, and usage—not on general EtherCAT framing or master stacks (see `ethercat.md`).

## What the term means

Beckhoff and the ETG describe Distributed Clocks as a **logical network of distributed clocks** inside the EtherCAT system:

- If a slave **supports DC**, it exposes clock hardware the master can discipline.
- One DC-capable slave is selected as the **reference clock** (sometimes called the **DC reference**). It represents the **EtherCAT system time** for the network.
- Other slaves (and the controller side, depending on implementation) **track** that reference under master configuration.

Not every slave must support DC; mixed networks are common, with only the nodes that need tight synchronization participating in DC.

## Why Distributed Clocks matter

DC provides a **shared notion of time** across nodes so that:

- **Coordinated motion** (multiple drives) can start or interpolate on the same tick.
- **Synchronous input sampling** and **synchronous output updates** reduce **bus-jitter** effects: actions are tied to aligned local times, not only to “when the frame arrived.”
- **Oversampling terminals** and **timestamped** events can be correlated across the machine.
- **Precise interrupts** or **PWM/DAQ** alignment can be scheduled relative to **SYNC** pulses derived from DC.

Published material often cites **clock alignment precision on the order of 100 ns** between participating nodes and **event jitter significantly below 1 µs** when DC is configured correctly—always verify on your specific topology, cables, and slave firmware.

## How synchronization works (conceptual)

1. **System time distribution**: The master sends datagrams that allow slaves to read and write **DC registers** (system time, offsets, delays). The reference slave’s time is the anchor.
2. **Offset correction**: Each slave adjusts its local clock to match the reference, accounting for **measured path delay** so that “now” means the same instant network-wide.
3. **Propagation delay measurement**: During startup (and optionally in operation), the master measures **signal propagation** from the reference to each slave. Without this, simply copying the reference timestamp would leave **systematic skew** due to cable length and per-hop delays.

The exact register workflow and state machine are defined in the EtherCAT protocol documentation; vendors’ master stacks and **ESI** files encode DC capability and default DC parameters per slave.

## Reference clock selection

- The master (or engineering tool) chooses the reference—often a **central I/O slice**, a **motion device**, or a slave at a **topologically favorable** position.
- Changing reference or hot-plugging may require **re-measuring delays** and **re-applying** DC parameters.

## SYNC signals and application timing

Many DC-capable slaves can generate **SYNC0** / **SYNC1** (or similarly named) hardware pulses derived from the disciplined clock. Applications use these to:

- Latch inputs and update outputs at **fixed phase** within the cycle.
- Align **servo loops** with **CiA 402** drive profiles over EtherCAT.

**SM sync** (Sync Manager event) and **DC sync** differ: SM sync ties events to **process data exchange**, while DC sync ties them to a **network-wide time line**. Drives and high-performance I/O often require DC for the lowest jitter.

## Configuration parameters engineers work with

Typical parameters (names vary by master/tooling) include:

- **Cycle time** and **shift times** (e.g., **Cyclic Shift**) to phase-align processing on the master with slave **SYNC** events.
- **AssignActivate** and vendor-specific DC flags in **ESI** that enable DC features on the slave.
- **Startup list** entries that write DC registers in the correct order during **INIT → PREOP → SAFEOP → OP**.

Misconfiguration often shows up as **DC state warnings**, **unstable SYNC**, or **occasional lost frames** under load—debugging usually combines **ENI/ESI** review with **ESC register** traces from the master.

## Simple mental model

Imagine several servo drives that must start motion at the same instant, or several input terminals that must sample at the same time. **Without DC**, actions track frame arrival and local ESC timing more loosely, so **network jitter** translates into **timing jitter**. **With DC**, the **local clocks** agree on the same instant, and **SYNC** edges fire **coherently** across slaves.

## Short definition

**Distributed Clocks** are EtherCAT’s **hardware-based time synchronization** mechanism: a **reference clock** on the bus disciplines other **DC-capable** slaves so the application can rely on a **shared system time** and **aligned hardware events**, not independent free-running local timing.

## Tooling and stacks

Both **open-source** masters (e.g., **SOEM**, **IgH** on PREEMPT_RT Linux) and **commercial** masters (e.g., **TwinCAT**, **Acontis EC-Master**) implement DC configuration and diagnostics; capabilities differ in **ENI generation**, **hot-connect**, and **diagnostic depth**. Always use a master and version confirmed by your slave vendors for DC-critical motion.

## Further reading

- ETG application notes and overview documents on **Distributed Clocks**.
- Vendor application notes for **motion** and **oversampling I/O** (often DC-specific wiring and parameter examples).
